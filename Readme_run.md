# enterprise-med-agent (MVP Stub)

企业级医疗/业务智能体平台（最小可运行 stub）：
- 10 模块架构：AuthZ、Ingest、Index、RAG++ Retrieve、Tools、Agent、Workflow、LLM Router、Memory、Eval
- 私有化与合规模块：脱敏、审计链路、模型路由策略插槽
- 可运行 FastAPI 服务 + contract tests

## Quick Start

### 1) 安装依赖
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

2) 启动服务
uvicorn src.api.main:app --reload --port 8000

3) 运行一次工作流 demo
curl -s http://127.0.0.1:8000/v1/workflows/clinical_infection \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "request_id": "REQ-001",
      "timestamp": "2026-01-20T10:00:00+01:00",
      "tenant_id": "HOSP-001",
      "user_id": "U1023",
      "role": "doctor",
      "dept": "ICU",
      "trace_id": "TRACE-001"
    },
    "adm_id": "A2026-001928"
  }' | python -m json.tool

Endpoints

POST /v1/m1/authz

POST /v1/m2/ingest

POST /v1/m3/index

POST /v1/m4/retrieve

POST /v1/m5/tools/exec

POST /v1/m6/agent/run

POST /v1/m7/orchestrator/run

POST /v1/m8/llm/route

POST /v1/m9/memory

POST /v1/m10/eval

工作流快捷入口：

POST /v1/workflows/clinical_infection


---

## `docker-compose.yml`
```yaml
version: "3.9"

services:
  app:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      - APP_ENV=dev
      - APP_CONFIG=configs/app.yaml
    command: >
      bash -lc "pip install -e . &&
                uvicorn src.api.main:app --host 0.0.0.0 --port 8000"
    ports:
      - "8000:8000"
