# Architecture (MVP)

- FastAPI 提供统一 HTTP 入口
- 10 模块分层：AuthZ/数据接入/索引/RAG检索/工具/Agent/工作流/模型路由/记忆/评测
- configs/schemas 做契约校验：保证模块间协作稳定
