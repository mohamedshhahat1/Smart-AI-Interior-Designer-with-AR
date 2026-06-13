from collections.abc import Iterator

from fastapi import APIRouter, HTTPException, status
from minio.error import S3Error
from starlette.responses import StreamingResponse

from backend.app.services.storage_service import BUCKET_NAME, storage_service

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("/{object_path:path}", name="get_media")
def get_media(object_path: str) -> StreamingResponse:
    if not object_path or ".." in object_path.split("/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid media path")

    try:
        response = storage_service.client.get_object(BUCKET_NAME, object_path)
    except S3Error as exc:
        if exc.code in {"NoSuchKey", "NoSuchObject"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found") from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Media storage unavailable",
        ) from exc

    def stream() -> Iterator[bytes]:
        try:
            for chunk in response.stream(amt=64 * 1024):
                yield chunk
        finally:
            response.close()
            response.release_conn()

    return StreamingResponse(
        stream(),
        media_type=response.headers.get("Content-Type", "application/octet-stream"),
        headers={"Cache-Control": "public, max-age=3600"},
    )
