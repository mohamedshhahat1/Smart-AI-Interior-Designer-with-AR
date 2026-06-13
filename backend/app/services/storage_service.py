import io
import json
import logging
from datetime import timedelta
from typing import Optional
from urllib.parse import unquote, urlparse

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
            self._set_public_read_policy()
        except S3Error as e:
            logger.error("Failed to create bucket: %s", e)

    def _set_public_read_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"],
                }
            ],
        }
        try:
            self._client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))
            logger.info("Set public read policy on bucket: %s", BUCKET_NAME)
        except S3Error as e:
            logger.warning("Failed to set bucket policy: %s", e)

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

    def _scheme(self) -> str:
        return "https" if settings.minio_secure else "http"

    def get_internal_url(self, object_name: str) -> str:
        """URL reachable from within the docker network (e.g. by the AI service)."""
        return f"{self._scheme()}://{settings.minio_endpoint}/{BUCKET_NAME}/{object_name}"

    def get_public_url(self, object_name: str) -> str:
        """URL reachable by external clients (browser / phone)."""
        endpoint = settings.minio_public_endpoint or settings.minio_endpoint
        return f"{self._scheme()}://{endpoint}/{BUCKET_NAME}/{object_name}"

    def to_public_url(self, url: Optional[str]) -> Optional[str]:
        """Convert a stored internal MinIO URL into a public-facing one.
        Leaves the URL untouched when no public endpoint is configured or when
        it does not point at the internal endpoint."""
        if not url or not settings.minio_public_endpoint:
            return url
        internal = settings.minio_endpoint
        public = settings.minio_public_endpoint
        for scheme in ("http://", "https://"):
            prefix = f"{scheme}{internal}"
            if url.startswith(prefix):
                return f"{scheme}{public}" + url[len(prefix):]
        return url

    def get_object_name(self, url: Optional[str]) -> Optional[str]:
        """Extract the MinIO object name from an internal or public object URL."""
        if not url:
            return None

        parsed = urlparse(url)
        path = unquote(parsed.path if parsed.scheme else url).lstrip("/")
        bucket_prefix = f"{BUCKET_NAME}/"
        if path.startswith(bucket_prefix):
            return path[len(bucket_prefix):]
        return None


storage_service = StorageService()
