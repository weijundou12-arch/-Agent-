from __future__ import annotations
import uuid

def new_trace_id() -> str:
    return f"TRACE-{uuid.uuid4().hex[:12]}"

def new_request_id() -> str:
    return f"REQ-{uuid.uuid4().hex[:12]}"
