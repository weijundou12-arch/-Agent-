from __future__ import annotations
from datetime import datetime, timezone

# ---- Fake patient facts (structured) ----
FAKE_PATIENT = {
    "adm_id": "A2026-001928",
    "dept": "ICU",
    "dx_icd10": ["J18.9", "A41.9"],
}

FAKE_FACTS = {
    "abx_hours": 52,
    "crp": 156,
    "pct_trend": [0.9, 2.1],
    "spo2_min": 88,
    "temp_max": 39.2,
}

# ---- Fake guideline snippets (unstructured) ----
FAKE_SNIPPETS = [
    {
        "text": "抗菌药 48–72h 无效应复核病原学、评估耐药风险并调整方案。",
        "citation": {"doc_id": "G-ABX-2025-08", "section": "3.2.1", "span": "48-72h无效处理", "score": 0.82},
    },
    {
        "text": "ICU 重症感染需评估耐药菌风险并尽快获取培养结果。",
        "citation": {"doc_id": "ICU-POLICY-2025-10", "section": "2.1", "span": "ICU耐药风险评估", "score": 0.78},
    },
]

# ---- Fake SQL rows / tool results ----
FAKE_SQL_ROWS = [
    {"abx": "PIPTA", "hours": 52, "crp": 156, "pct": 2.1, "spo2_min": 88, "temp_max": 39.2},
]

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
