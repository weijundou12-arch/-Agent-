from __future__ import annotations
import re
from src.core.schema_validation import load_schema, validate

M = load_schema("m1_auth.json")

def _redact_text(text: str) -> str:
    # MVP：简单规则脱敏（生产：NER + 规则库）
    text = re.sub(r"(身份证[:：]?\s*)\d{6,}", r"\1***", text)
    text = re.sub(r"(电话[:：]?\s*)\d{7,}", r"\1***", text)
    text = re.sub(r"(姓名[:：]?\s*)\S+", r"\1***", text)
    return text

def authz(req: dict) -> dict:
    validate(M["request"], req, "M1.Request")
    meta = req["meta"]
    resource_type = req["resource"]["resource_type"]

    # MVP 权限：researcher 禁止读 patient_record
    allowed = True
    if resource_type == "patient_record" and meta["role"] == "researcher":
        allowed = False

    payload = req.get("payload", {}) or {}
    redacted = dict(payload)
    if "text" in redacted and isinstance(redacted["text"], str):
        redacted["text"] = _redact_text(redacted["text"])

    resp = {
        "allowed": allowed,
        "redacted_payload": redacted,
        "audit": [{
            "event_type": "AUTHZ_ALLOW" if allowed else "AUTHZ_DENY",
            "detail": {"role": meta["role"], "resource_type": resource_type}
        }]
    }
    validate(M["response"], resp, "M1.Response")
    return resp
