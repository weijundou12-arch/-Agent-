# Security & Compliance (MVP Notes)

- M1：权限与脱敏插槽（researcher 访问 patient_record 拒绝）
- M8：PII 禁止外发策略插槽（forbid external）
- 审计：每个响应返回 audit[]，生产应落库并可回放
- 输出：仅“建议草稿”，不直接下医嘱
