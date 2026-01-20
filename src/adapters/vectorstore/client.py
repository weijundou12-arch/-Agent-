from __future__ import annotations

class VectorStore:
    """Stub vector store. 生产可替换为 Milvus/FAISS。"""
    def search(self, query: str, k: int = 10) -> list[dict]:
        return []
