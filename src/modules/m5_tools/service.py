from __future__ import annotations
from src.core.schema_validation import validate_or_raise
from src.core.fake_data import FAKE_SQL_ROWS

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "tool_name", "tool_version", "arguments"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "trace_id"]},
        "tool_name": {"type": "string"},
        "tool_version": {"type": "string"},
        "arguments": {"type": "object"},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["ok", "result", "audit"],
    "properties": {"ok": {"type": "boolean"}, "result": {"type": "object"}, "audit": {"type": "array"}},
}

def handle_tool_exec(req: dict) -> dict:
    """
    功能：统一工具执行入口（SQL/API/Python/VLM）。
    Stub：只实现 query_sql；真实版：工具注册表 + 参数校验 + 沙箱 + 权限 + 审计。
    """
    validate_or_raise(REQ_SCHEMA, req, "M5.Request")
    tool = req["tool_name"]

    if tool == "query_sql":
        result = {"sql_id": "SQL_021", "rows": FAKE_SQL_ROWS}
        ok = True
    else:
        # Stub：未知工具直接失败（真实版应返回可解释错误码）
        result = {"message": f"unknown tool: {tool}"}
        ok = False

    resp = {"ok": ok, "result": result, "audit": [{"event_type": "TOOL_EXEC", "detail": {"tool": tool}}]}
    validate_or_raise(RESP_SCHEMA, resp, "M5.Response")
    return resp
