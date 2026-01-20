from __future__ import annotations
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.logging import get_logger

logger = get_logger(__name__)

class AuditMiddleware(BaseHTTPMiddleware):
    """
    目标：
    - 给每个请求打 trace_id/request_id（优先从 body.meta 读取，其次 header）
    - 统一记录响应里返回的 audit 事件（如果存在）
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        body_bytes = await request.body()
        meta = {}
        if body_bytes:
            try:
                payload = json.loads(body_bytes.decode("utf-8"))
                meta = (payload.get("meta") or {}) if isinstance(payload, dict) else {}
            except Exception:
                meta = {}

        trace_id = meta.get("trace_id") or request.headers.get("x-trace-id") or "TRACE-UNKNOWN"
        request_id = meta.get("request_id") or request.headers.get("x-request-id") or "REQ-UNKNOWN"

        request.state.trace_id = trace_id
        request.state.request_id = request_id

        response = await call_next(request)

        # 读取响应内容以打印 audit（注意：这里是 MVP 简化；生产建议用日志管道/落库）
        try:
            if hasattr(response, "body_iterator"):
                # StreamingResponse 不好直接取，这里跳过
                return response
        except Exception:
            pass

        return response

