#!/bin/bash
# MinIO bucket initialization script
# Run after MinIO container is healthy

set -e

MINIO_ENDPOINT="${MINIO_ENDPOINT:-localhost:9000}"
MINIO_ACCESS_KEY="${MINIO_ACCESS_KEY:-minioadmin}"
MINIO_SECRET_KEY="${MINIO_SECRET_KEY:-minioadmin}"

echo "Configuring MinIO at $MINIO_ENDPOINT..."

mc alias set minio http://$MINIO_ENDPOINT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

echo "Creating buckets..."
mc mb --ignore-existing minio/room-images
mc mb --ignore-existing minio/generated-designs
mc mb --ignore-existing minio/furniture-models
mc mb --ignore-existing minio/thumbnails

echo "Setting bucket policies..."
mc anonymous set download minio/thumbnails
mc anonymous set download minio/furniture-models

echo "MinIO setup complete!"
echo "Buckets created:"
mc ls minio/
