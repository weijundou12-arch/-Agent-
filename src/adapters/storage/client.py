from __future__ import annotations

class StorageClient:
    """Stub storage. 生产可对接 MinIO/S3。"""
    def put(self, key: str, data: bytes) -> str:
        return f"s3://stub/{key}"
