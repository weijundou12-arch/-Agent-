from __future__ import annotations
from src.core.schema_validation import validate_or_raise

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "index_job_id", "doc_refs", "chunking"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "trace_id"]},
        "index_job_id": {"type": "string"},
        "doc_refs": {"type": "array"},
        "chunking": {"type": "object", "required": ["strategy", "max_tokens"]},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["index_job_id", "chunks_created", "vector_index", "bm25_index", "audit"],
    "properties": {
        "index_job_id": {"type": "string"},
        "chunks_created": {"type": "integer"},
        "vector_index": {"type": "string"},
        "bm25_index": {"type": "string"},
        "audit": {"type": "array"},
    },
}

def handle_index(req: dict) -> dict:
    """
    功能：把 doc_refs 变成可检索索引（向量/倒排/元数据）。
    Stub：返回假索引地址与 chunk 数；真实版接 Milvus/OpenSearch。
    """
    validate_or_raise(REQ_SCHEMA, req, "M3.Request")
    n_docs = len(req["doc_refs"])
    max_tokens = req["chunking"]["max_tokens"]
    chunks = max(1, n_docs * (max_tokens // 512))

    resp = {
        "index_job_id": req["index_job_id"],
        "chunks_created": chunks,
        "vector_index": "milvus://kb_vectors_stub",
        "bm25_index": "opensearch://kb_bm25_stub",
        "audit": [{"event_type": "BUILD_INDEX", "detail": {"docs": n_docs, "chunks": chunks}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M3.Response")
    return resp
