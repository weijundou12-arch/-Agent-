from __future__ import annotations
from fastapi import APIRouter
from src.modules.m6_agent.service import run_agent
from src.modules.m7_orchestrator.service import run_orchestrator

router = APIRouter(prefix="/v1", tags=["agent"])

@router.post("/m6/agent/run")
def api_run_agent(payload: dict):
    return run_agent(payload)

@router.post("/m7/orchestrator/run")
def api_run_orchestrator(payload: dict):
    return run_orchestrator(payload)
