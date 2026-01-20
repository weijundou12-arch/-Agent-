from __future__ import annotations
from src.modules.m3_index.service import build_index

def main():
    payload = {
        "meta": {
            "request_id": "REQ-JOB-IDX",
            "timestamp": "2026-01-20T10:00:00+01:00",
            "tenant_id": "HOSP-001",
            "user_id": "admin",
            "role": "admin",
            "dept": "IT",
            "trace_id": "TRACE-JOB-IDX"
        },
        "index_job_id": "IDX-001",
        "doc_refs": ["doc:0","doc:1"],
        "chunking": {"strategy": "section_based", "max_tokens": 800}
    }
    print(build_index(payload))

if __name__ == "__main__":
    main()
