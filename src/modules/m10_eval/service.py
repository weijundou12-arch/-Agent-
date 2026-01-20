# M10 评测与监控（Eval）——返回假指标

from __future__ import annotations
from src.core.schema_validation import validate_or_raise

REQ_SCHEMA = {
    "type": "object",
    "required": ["meta", "mode", "metrics"],
    "properties": {
        "meta": {"type": "object", "required": ["request_id", "trace_id"]},
        "mode": {"type": "string", "enum": ["offline", "online"]},
        "metrics": {"type": "array"},
        "dataset_ref": {"type": "string"},
        "run_ref": {"type": "string"},
    },
}
RESP_SCHEMA = {
    "type": "object",
    "required": ["metric_results", "report_ref", "audit"],
    "properties": {"metric_results": {"type": "object"}, "report_ref": {"type": "string"}, "audit": {"type": "array"}},
}

def handle_eval(req: dict) -> dict:
    """
    功能：离线评测/在线监控的统一输出。
    Stub：返回固定指标；真实版：读取日志、比对 golden set、计算 citation correctness 等。
    """
    validate_or_raise(REQ_SCHEMA, req, "M10.Request")
    metrics = req["metrics"]

    # Fake metrics
    results = {}
    for m in metrics:
        if m == "recall_at_k":
            results[m] = {"k": 10, "value": 0.87}
        elif m == "citation_correctness":
            results[m] = 0.96
        elif m == "hallucination_rate":
            results[m] = 0.008
        elif m == "tool_success":
            results[m] = 0.94
        elif m == "p95_latency":
            results[m] = 5.8
        elif m == "cost_per_1k":
            results[m] = 0.12
        else:
            results[m] = "NA"

    resp = {
        "metric_results": results,
        "report_ref": "s3://eval/reports/stub.html",
        "audit": [{"event_type": "EVAL_DONE", "detail": {"mode": req["mode"], "n": len(metrics)}}],
    }
    validate_or_raise(RESP_SCHEMA, resp, "M10.Response")
    return resp
