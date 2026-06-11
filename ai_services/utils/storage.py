import io
import logging
import os

logger = logging.getLogger(__name__)

BUCKET_NAME = "smart-interior"


class AIStorageService:
    """Minimal MinIO client so the AI service can persist generated images and
    return a publicly reachable URL instead of a local container path."""

    def __init__(self):
        self._client = None
        self.endpoint = os.getenv("MINIO_ENDPOINT", "")
        self.public_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT", "") or self.endpoint
        self.access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.secure = os.getenv("MINIO_SECURE", "false").lower() == "true"

    @property
    def enabled(self) -> bool:
        return bool(self.endpoint)

    @property
    def client(self):
        if self._client is None:
            from minio import Minio

            self._client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )
            self._ensure_bucket()
        return self._client

    def _ensure_bucket(self):
        try:
            if not self._client.bucket_exists(BUCKET_NAME):
                self._client.make_bucket(BUCKET_NAME)
        except Exception:
            logger.exception("Could not ensure MinIO bucket exists")

    def upload_bytes(self, object_name: str, data: bytes, content_type: str = "image/jpeg") -> str:
        self.client.put_object(
            BUCKET_NAME,
            object_name,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        endpoint = self.public_endpoint or self.endpoint
        scheme = "https" if self.secure else "http"
        return f"{scheme}://{endpoint}/{BUCKET_NAME}/{object_name}"


storage_service = AIStorageService()
