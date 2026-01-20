# M7 工作流编排（临床/科研/运营）

from __future__ import annotations
from src.core.schema_validation import validate_or_raise
from src.modules.m6_agent.service import handle_agent

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "workflow", "params"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "user_id", "role", "dept", "trace_id"]},
        "workflow": {"type": "string"},
        "params": {"type": "object"},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["workflow", "artifacts", "summary", "audit"],
    "properties": {
        "workflow": {"type": "string"},
        "artifacts": {"type": "array"},
        "summary": {"type": "string"},
        "audit": {"type": "array"},
    },
}

def handle_workflow(req: dict) -> dict:
    """
    功能：把 Agent 变成业务产品：临床感染评估 / 科研队列 / 运营异常解释。
    Stub：只实现 clinical_infection，返回两个 artifact ref（草稿+报告）。
    """
    validate_or_raise(REQ_SCHEMA, req, "M7.Request")
    workflow = req["workflow"]
    meta = req["meta"]

    if workflow != "clinical_infection":
        # Stub：其他 workflow 留空（你后续继续补）
        resp = {
            "workflow": workflow,
            "artifacts": [],
            "summary": f"Stub: workflow={workflow} 尚未实现",
            "audit": [{"event_type": "WORKFLOW_PARTIAL", "detail": {"workflow": workflow}}],
        }
        validate_or_raise(RESP_SCHEMA, resp, "M7.Response")
        return resp

    # 1) 调用 Agent
    agent_out = handle_agent({
        "meta": meta,
        "task": "评估ICU患者感染风险并给出下一步抗菌策略，生成病程草稿。",
        "inputs": {"adm_id": req["params"].get("adm_id", "A2026-001928")},
        "constraints": {"max_steps": 6, "max_tool_calls": 8, "must_cite": True},
    })

    # 2) 产物（真实版会写回 EMR、生成 PDF、触发审批流等）
    artifacts = [
        {"artifact_type": "note_draft", "artifact_ref": f"emr_draft:N-{meta['request_id']}"},
        {"artifact_type": "report", "artifact_ref": f"s3://reports/{req['params'].get('adm_id','A')}-infection.pdf"},
    ]

    resp = {
        "workflow": workflow,
        "artifacts": artifacts,
        "summary": agent_out["final_answer"],
        "audit": [{"event_type": "WORKFLOW_DONE", "detail": {"workflow": workflow}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M7.Response")
    return resp
