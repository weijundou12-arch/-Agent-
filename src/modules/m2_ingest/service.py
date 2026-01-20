from __future__ import annotations
from src.core.schema_validation import validate_or_raise

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "source", "data_type", "items"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "trace_id"]},
        "source": {"type": "string"},
        "data_type": {"type": "string"},
        "items": {"type": "array"},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["accepted", "rejected", "item_refs", "audit"],
    "properties": {
        "accepted": {"type": "integer"},
        "rejected": {"type": "integer"},
        "item_refs": {"type": "array"},
        "audit": {"type": "array"},
    },
}

def handle_ingest(req: dict) -> dict:
    """
    功能：接入数据（文档/结构化/影像/时序），返回 item_refs。
    Stub：不落盘，仅生成引用 ID；真实版对接 DB/MinIO/Kafka。
    """
    validate_or_raise(REQ_SCHEMA, req, "M2.Request")
    data_type = req["data_type"]
    items = req["items"]

    refs = [f"{data_type}:{i}" for i in range(len(items))]
    resp = {
        "accepted": len(items),
        "rejected": 0,
        "item_refs": refs,
        "audit": [{"event_type": "INGEST", "detail": {"data_type": data_type, "n": len(items)}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M2.Response")
    return resp
