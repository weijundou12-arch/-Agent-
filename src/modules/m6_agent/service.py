# M6 Agent（规划/执行/重试）——用假“生成器”代替 LLM

from __future__ import annotations
from src.core.schema_validation import validate_or_raise
from src.modules.m4_retrieve.service import handle_retrieve
from src.modules.m5_tools.service import handle_tool_exec
from src.modules.m8_llm_router.service import handle_route

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "task", "inputs", "constraints"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "role", "dept", "trace_id"]},
        "task": {"type": "string"},
        "inputs": {"type": "object"},
        "constraints": {"type": "object", "required": ["max_steps", "max_tool_calls", "must_cite"]},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["final_answer", "plan", "tool_calls", "citations", "status", "audit"],
    "properties": {
        "final_answer": {"type": "string"},
        "plan": {"type": "array"},
        "tool_calls": {"type": "array"},
        "citations": {"type": "array"},
        "status": {"type": "string"},
        "audit": {"type": "array"},
    },
}

def _fake_llm_generate(task: str, facts: dict, snippets: list) -> str:
    """Stub LLM：用规则拼一个“像真实输出”的答案。"""
    abx_hours = facts.get("abx_hours")
    pct = facts.get("pct_trend", [])
    spo2 = facts.get("spo2_min")
    cite_hint = snippets[0]["citation"]["doc_id"] if snippets else "N/A"
    return (
        f"基于结构化数据：抗菌药已用{abx_hours}小时，PCT趋势{pct}，最低SpO2={spo2}。\n"
        f"建议：1) 复核培养/耐药风险；2) 按指南48–72h无效策略调整方案；3) 生成病程草稿待确认。\n"
        f"证据来源：{cite_hint}。"
    )

def handle_agent(req: dict) -> dict:
    """
    功能：Agent (plan->tool->retrieve->compose) 的最小闭环。
    Stub：调用 M8 选模型（仅记录）、M5 查 SQL、M4 做 RAG、最后用假 LLM 生成。
    """
    validate_or_raise(REQ_SCHEMA, req, "M6.Request")
    meta = req["meta"]

    plan = ["选择模型", "查询结构化数据(SQL)", "检索指南证据(RAG++)", "生成建议与草稿"]
    tool_calls = []
    citations = []

    # 1) 路由模型（只记录，不真实调用）
    route = handle_route({
        "meta": {"request_id": meta["request_id"], "trace_id": meta["trace_id"]},
        "task_type": "qa_cited",
        "input": {},
        "policy_flags": {"pii_forbidden_external": True, "max_cost_level": "mid"},
    })
    tool_calls.append({"tool": "llm_route", "result": route["model_selected"]})

    # 2) Tool: query_sql
    tool = handle_tool_exec({
        "meta": {"request_id": meta["request_id"], "user_id": meta["user_id"], "trace_id": meta["trace_id"]},
        "tool_name": "query_sql",
        "tool_version": "v1",
        "arguments": {"adm_id": req["inputs"].get("adm_id", "A2026-001928")},
    })
    tool_calls.append({"tool": "query_sql", "ref": tool["result"].get("sql_id"), "ok": tool["ok"]})

    # 3) Retrieve: RAG++
    rag = handle_retrieve({
        "meta": {"request_id": meta["request_id"], "user_id": meta["user_id"], "dept": meta["dept"], "trace_id": meta["trace_id"]},
        "query": req["task"],
        "context": {"need_citations": True},
        "retrieve_params": {"k": 5, "use_structured_first": True, "rerank": True},
    })
    snippets = rag["snippets"]
    facts = rag["structured_facts"]
    citations = [s["citation"] for s in snippets]

    # 4) Compose answer (fake)
    final_answer = _fake_llm_generate(req["task"], facts, snippets)

    resp = {
        "final_answer": final_answer,
        "plan": plan,
        "tool_calls": tool_calls,
        "citations": citations,
        "status": "success",
        "audit": [{"event_type": "AGENT_RUN", "detail": {"steps": len(plan)}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M6.Response")
    return resp
