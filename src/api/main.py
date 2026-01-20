from __future__ import annotations
from fastapi import FastAPI
from src.api.middleware_audit import AuditMiddleware
from src.api.routes_agent import router as agent_router
from src.api.routes_admin import router as admin_router
from src.core.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(title="enterprise-med-agent", version="0.1.0")
app.add_middleware(AuditMiddleware)

app.include_router(agent_router)
app.include_router(admin_router)

@app.get("/health")
def health():
    return {"ok": True}
