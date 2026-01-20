from __future__ import annotations
from fastapi import FastAPI, HTTPException
from src.core.fake_data import utcnow_iso

# Modules
from src.modules.m1_authz.service import handle_authz
from src.modules.m2_ingest.service import handle_ingest
from src.modules.m3_index.service import handle_index
from src.modules.m4_retrieve.service import handle_retrieve
from src.modules.m5_tools.service import handle_tool_exec
from src.modules.m6_agent.service import handle_agent
from src.modules.m7_orchestrator.service import handle_workflow
from src.modules.m8_llm_router.service import handle_route
from src.modules.m9_memory.service import handle_memory
from src.modules.m10_eval.service import handle_eval

app = FastAPI(title="Enterprise Med Agent (Stub)", version="0.1.0")


def _wrap(handler, payload: dict):
    """统一错误包装：把 schema 校验或业务错误变成 400"""
    try:
        return handler(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/health")
def health():
    return {"ok": True, "ts": utcnow_iso()}

# 10 modules endpoints (stub)
@app.post("/v1/m1/authz")
def m1(payload: dict): return _wrap(handle_authz, payload)

@app.post("/v1/m2/ingest")
def m2(payload: dict): return _wrap(handle_ingest, payload)

@app.post("/v1/m3/index")
def m3(payload: dict): return _wrap(handle_index, payload)

@app.post("/v1/m4/retrieve")
def m4(payload: dict): return _wrap(handle_retrieve, payload)

@app.post("/v1/m5/tools/exec")
def m5(payload: dict): return _wrap(handle_tool_exec, payload)

@app.post("/v1/m6/agent/run")
def m6(payload: dict): return _wrap(handle_agent, payload)

@app.post("/v1/m7/workflow/run")
def m7(payload: dict): return _wrap(handle_workflow, payload)

@app.post("/v1/m8/llm/route")
def m8(payload: dict): return _wrap(handle_route, payload)

@app.post("/v1/m9/memory")
def m9(payload: dict): return _wrap(handle_memory, payload)

@app.post("/v1/m10/eval")
def m10(payload: dict): return _wrap(handle_eval, payload)
