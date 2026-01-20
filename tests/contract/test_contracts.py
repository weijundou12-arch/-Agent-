from __future__ import annotations
import pytest
from src.modules.m7_orchestrator.service import workflow_clinical_infection
from src.modules.m1_authz.service import authz

def meta():
    return {
        "request_id": "REQ-TST-001",
        "timestamp": "2026-01-20T10:00:00+01:00",
        "tenant_id": "HOSP-001",
        "user_id": "U1023",
        "role": "doctor",
        "dept": "ICU",
        "trace_id": "TRACE-TST-001"
    }

def test_workflow_clinical_infection_runs():
    out = workflow_clinical_infection({"meta": meta(), "adm_id": "A2026-001928"})
    assert out["workflow"] == "clinical_infection"
    assert "artifacts" in out and len(out["artifacts"]) >= 1
    assert "summary" in out and isinstance(out["summary"], str)

def test_authz_researcher_denied_patient_record():
    out = authz({
        "meta": {**meta(), "role": "researcher"},
        "action": "read",
        "resource": {"resource_type": "patient_record", "resource_id": "A2026-001928"},
        "payload": {"text": "姓名张三 身份证1234567890"}
    })
    assert out["allowed"] is False
