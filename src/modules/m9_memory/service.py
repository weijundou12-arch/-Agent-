#M9 长期记忆（Memory）——用内存 dict 模拟

from __future__ import annotations
from src.core.schema_validation import validate_or_raise

# In-memory KV store (stub)
_STORE: dict = {}

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "op", "namespace", "key"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "trace_id"]},
        "op": {"type": "string", "enum": ["get", "set", "append", "delete"]},
        "namespace": {"type": "string"},
        "key": {"type": "string"},
        "value": {"type": "object"},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["ok", "value", "audit"],
    "properties": {"ok": {"type": "boolean"}, "value": {"type": "object"}, "audit": {"type": "array"}},
}

def handle_memory(req: dict) -> dict:
    """
    功能：长期记忆（用户偏好/任务状态/项目配置）。
    Stub：内存字典；真实版：DB + 可删除 + 审计 + TTL + 权限隔离。
    """
    validate_or_raise(REQ_SCHEMA, req, "M9.Request")
    meta = req["meta"]
    ns = req["namespace"]
    key = f"{meta['user_id']}::{ns}::{req['key']}"
    op = req["op"]

    if op == "get":
        val = _STORE.get(key, {})
        ok = True
    elif op == "set":
        _STORE[key] = req.get("value", {})
        val = _STORE[key]
        ok = True
    elif op == "append":
        cur = _STORE.get(key, {"items": []})
        cur.setdefault("items", []).append(req.get("value", {}))
        _STORE[key] = cur
        val = cur
        ok = True
    elif op == "delete":
        _STORE.pop(key, None)
        val = {}
        ok = True
    else:
        val = {"error": "unknown op"}
        ok = False

    resp = {"ok": ok, "value": val, "audit": [{"event_type": "MEMORY_OP", "detail": {"op": op, "key": key}}]}
    validate_or_raise(RESP_SCHEMA, resp, "M9.Response")
    return resp
