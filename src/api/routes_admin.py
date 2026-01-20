from __future__ import annotations
from fastapi import APIRouter
from src.modules.m1_authz.service import authz
from src.modules.m2_ingest.service import ingest
from src.modules.m3_index.service import build_index
from src.modules.m4_retrieve.service import retrieve
from src.modules.m5_tools.service import exec_tool
from src.modules.m8_llm_router.service import route_llm
from src.modules.m9_memory.service import memory_op
from src.modules.m10_eval.service import eval_run
from src.modules.m7_orchestrator.service import workflow_clinical_infection

router = APIRouter(prefix="/v1", tags=["admin"])

@router.post("/m1/authz")
def api_authz(payload: dict): return authz(payload)

@router.post("/m2/ingest")
def api_ingest(payload: dict): return ingest(payload)

@router.post("/m3/index")
def api_index(payload: dict): return build_index(payload)

@router.post("/m4/retrieve")
def api_retrieve(payload: dict): return retrieve(payload)

@router.post("/m5/tools/exec")
def api_tools(payload: dict): return exec_tool(payload)

@router.post("/m8/llm/route")
def api_route(payload: dict): return route_llm(payload)

@router.post("/m9/memory")
def api_memory(payload: dict): return memory_op(payload)

@router.post("/m10/eval")
def api_eval(payload: dict): return eval_run(payload)

# 便捷工作流入口（演示用）
@router.post("/workflows/clinical_infection")
def api_workflow_infection(payload: dict):
    return workflow_clinical_infection(payload)
