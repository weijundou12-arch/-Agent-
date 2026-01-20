#RAG++

from __future__ import annotations
from src.core.schema_validation import validate_or_raise
from src.core.fake_data import FAKE_SNIPPETS, FAKE_FACTS

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "query", "context", "retrieve_params"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "dept", "trace_id"]},
        "query": {"type": "string"},
        "context": {"type": "object", "required": ["need_citations"]},
        "retrieve_params": {"type": "object", "required": ["k", "use_structured_first", "rerank"]},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["snippets", "structured_facts", "audit"],
    "properties": {
        "snippets": {"type": "array"},
        "structured_facts": {"type": "object"},
        "audit": {"type": "array"},
    },
}

def handle_retrieve(req: dict) -> dict:
    """
    功能：RAG++ 检索：结构化优先 + 文档证据片段 + 引用。
    Stub：返回固定 snippets + facts；真实版：DB facts + 向量检索 + rerank + 权限过滤。
    """
    validate_or_raise(REQ_SCHEMA, req, "M4.Request")
    k = int(req["retrieve_params"]["k"])
    snippets = FAKE_SNIPPETS[: max(1, min(k, len(FAKE_SNIPPETS)))]

    resp = {
        "snippets": snippets,
        "structured_facts": FAKE_FACTS,
        "audit": [{"event_type": "RAG_RETRIEVE", "detail": {"k": k, "structured_first": True}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M4.Response")
    return resp
