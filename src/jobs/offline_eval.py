from __future__ import annotations
from src.modules.m10_eval.service import eval_run

def main():
    payload = {
        "meta": {
            "request_id": "REQ-JOB-EVAL",
            "timestamp": "2026-01-20T10:00:00+01:00",
            "tenant_id": "HOSP-001",
            "user_id": "admin",
            "role": "admin",
            "dept": "IT",
            "trace_id": "TRACE-JOB-EVAL"
        },
        "mode": "offline",
        "metrics": ["recall_at_k","citation_correctness","hallucination_rate","tool_success","p95_latency","cost_per_1k"]
    }
    print(eval_run(payload))

if __name__ == "__main__":
    main()
