#M8 多模型路由（Router

from __future__ import annotations
from src.core.schema_validation import validate_or_raise

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "task_type", "input", "policy_flags"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "trace_id"]},
        "task_type": {"type": "string"},
        "input": {"type": "object"},
        "policy_flags": {"type": "object", "required": ["pii_forbidden_external", "max_cost_level"]},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["model_selected", "fallback_chain", "limits", "audit"],
    "properties": {
        "model_selected": {"type": "string"},
        "fallback_chain": {"type": "array"},
        "limits": {"type": "object"},
        "audit": {"type": "array"},
    },
}

def handle_route(req: dict) -> dict:
    """
    功能：根据任务类型+合规标记选择模型（国产/云/专用）。
    Stub：根据 pii_forbidden_external 选择 local；真实版：成本/延迟/质量路由+限流降级。
    """
    validate_or_raise(REQ_SCHEMA, req, "M8.Request")
    flags = req["policy_flags"]
    if flags["pii_forbidden_external"]:
        model = "qwen2.5-72b-local"
        fallback = ["qwen2.5-32b-local"]
    else:
        model = "qwen2.5-72b-local"
        fallback = ["qwen2.5-32b-local", "gpt-4o-mini-cloud"]

    resp = {
        "model_selected": model,
        "fallback_chain": fallback,
        "limits": {"rpm": 120, "tpm": 200000},
        "audit": [{"event_type": "ROUTE_MODEL", "detail": {"selected": model}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M8.Response")
    return resp
