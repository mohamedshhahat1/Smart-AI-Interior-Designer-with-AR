import io
import logging
from datetime import timedelta

from minio import Minio
from minio.error import S3Error

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

BUCKET_NAME = "smart-interior"


class StorageService:
    def __init__(self):
        self._client = None

    @property
    def client(self) -> Minio:
        if self._client is None:
            self._client = Minio(
                settings.minio_endpoint,
                access_key=settings.minio_access_key,
                secret_key=settings.minio_secret_key,
                secure=settings.minio_secure,
            )
            self._ensure_bucket()
        return self._client

    def _ensure_bucket(self):
        try:
            if not self._client.bucket_exists(BUCKET_NAME):
                self._client.make_bucket(BUCKET_NAME)
                logger.info("Created MinIO bucket: %s", BUCKET_NAME)
        except S3Error as e:
            logger.error("Failed to create bucket: %s", e)

    def upload_bytes(self, object_name: str, data: bytes, content_type: str = "image/jpeg") -> str:
        self.client.put_object(
            BUCKET_NAME,
            object_name,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return object_name

    def get_presigned_url(self, object_name: str, expires: timedelta = timedelta(hours=2)) -> str:
        return self.client.presigned_get_object(BUCKET_NAME, object_name, expires=expires)

    def get_internal_url(self, object_name: str) -> str:
        return f"http://{settings.minio_endpoint}/{BUCKET_NAME}/{object_name}"


storage_service = StorageService()
