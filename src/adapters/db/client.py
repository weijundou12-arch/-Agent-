from __future__ import annotations

class DBClient:
    """Stub DB client. 生产可替换为 SQLAlchemy / asyncpg / pymysql 等。"""
    def query(self, sql: str, params: dict | None = None) -> list[dict]:
        return []
