from __future__ import annotations
from src.modules.m2_ingest.service import ingest

def main():
    payload = {
        "meta": {
            "request_id": "REQ-JOB-INGEST",
            "timestamp": "2026-01-20T10:00:00+01:00",
            "tenant_id": "HOSP-001",
            "user_id": "admin",
            "role": "admin",
            "dept": "IT",
            "trace_id": "TRACE-JOB-INGEST"
        },
        "source": "file",
        "data_type": "doc",
        "items": [{"title": "指南A"}, {"title": "制度B"}]
    }
    print(ingest(payload))

if __name__ == "__main__":
    main()
