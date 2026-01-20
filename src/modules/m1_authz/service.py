M1 身份/权限/脱敏（AuthZ）

from __future__ import annotations
from src.core.schema_validation import validate_or_raise

# 简化 schema：只校验你最需要的字段（可继续加）
REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "action", "resource", "payload"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "role", "dept", "trace_id"]},
        "action": {"type": "string"},
        "resource": {"type": "object", "required": ["resource_type", "resource_id"]},
        "payload": {"type": "object"},
    },
}

RESP_SCHEMA = {
    "type": "object",
    "required": ["allowed", "redacted_payload", "pii", "audit"],
    "properties": {
        "allowed": {"type": "boolean"},
        "redacted_payload": {"type": "object"},
        "pii": {"type": "object", "required": ["contains_pii"]},
        "audit": {"type": "array"},
    },
}

def _simple_redact(text: str) -> str:
    # Stub: 真实版应做 NER + 规则（姓名/身份证/手机号/地址等）
    return text.replace("身份证", "***").replace("姓名", "***")

def handle_authz(req: dict) -> dict:
    """
    功能：判断是否允许访问 + 对 payload 做脱敏（演示用）
    中国企业落地：必须有权限隔离、审计留痕、PII 处理策略。
    """
    validate_or_raise(REQ_SCHEMA, req, "M1.Request")
    meta = req["meta"]
    role = meta["role"]
    resource_type = req["resource"]["resource_type"]

    # Stub 权限规则：医生/药师可读 patient_record；研究者不可直接读
    allowed = True
    if resource_type == "patient_record" and role == "researcher":
        allowed = False

    payload = req["payload"]
    redacted = payload.copy()
    if "text" in redacted and isinstance(redacted["text"], str):
        redacted["text"] = _simple_redact(redacted["text"])

    resp = {
        "allowed": allowed,
        "redacted_payload": redacted,
        "pii": {"contains_pii": "text" in payload},
        "audit": [{"event_type": "AUTHZ_ALLOW" if allowed else "AUTHZ_DENY", "detail": {"role": role}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M1.Response")
    return resp
