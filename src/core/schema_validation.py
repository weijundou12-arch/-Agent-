通用：Schema 校验 + 假数据

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict

import yaml
from jsonschema import Draft202012Validator
from src.core.errors import SchemaError

_SCHEMA_CACHE: dict[str, dict] = {}
_APP_CFG_CACHE: dict | None = None

def _load_app_cfg() -> dict:
    global _APP_CFG_CACHE
    if _APP_CFG_CACHE is not None:
        return _APP_CFG_CACHE
    cfg_path = os.environ.get("APP_CONFIG", "configs/app.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        _APP_CFG_CACHE = yaml.safe_load(f)
    return _APP_CFG_CACHE

def schema_dir() -> Path:
    cfg = _load_app_cfg()
    return Path(cfg["app"]["schema_dir"])

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_schema(schema_name: str) -> dict:
    """
    支持 $ref 引用同目录下 json 文件（common.json 等）。
    简化做法：把引用的 schema 也放入 resolver 的 store。
    """
    key = schema_name
    if key in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[key]

    base = schema_dir()
    target = base / schema_name
    if not target.exists():
        raise SchemaError(f"Schema not found: {target}")

    # load all schemas into store for local ref
    store: Dict[str, dict] = {}
    for p in base.glob("*.json"):
        sch = load_json(p)
        store[p.name] = sch

    sch = store[target.name]
    sch["_local_store"] = store  # stash for resolver
    _SCHEMA_CACHE[key] = sch
    return sch

def _resolve_ref(ref: str, store: dict[str, dict]) -> dict:
    # ref form: "common.json#/definitions/RequestMeta"
    if "#" in ref:
        fname, frag = ref.split("#", 1)
    else:
        fname, frag = ref, ""
    base = store.get(fname)
    if base is None:
        raise SchemaError(f"Unresolved $ref file: {fname}")
    node: Any = base
    if frag.startswith("/"):
        parts = frag.strip("/").split("/")
        for part in parts:
            node = node[part]
    elif frag.startswith("#/"):
        parts = frag[2:].split("/")
        for part in parts:
            node = node[part]
    return node

def _inline_refs(schema: Any, store: dict[str, dict]) -> Any:
    if isinstance(schema, dict):
        if "$ref" in schema:
            resolved = _resolve_ref(schema["$ref"], store)
            return _inline_refs(resolved, store)
        return {k: _inline_refs(v, store) for k, v in schema.items() if k != "_local_store"}
    if isinstance(schema, list):
        return [_inline_refs(x, store) for x in schema]
    return schema

def validate(schema: dict, instance: dict, where: str) -> None:
    store = schema.get("_local_store", {})
    inlined = _inline_refs(schema, store)
    try:
        Draft202012Validator(inlined).validate(instance)
    except Exception as e:
        raise SchemaError(f"[{where}] schema validation failed: {e}") from e
