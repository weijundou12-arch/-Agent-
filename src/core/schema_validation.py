from __future__ import annotations
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


def validate_or_raise(schema: dict, instance: dict, where: str) -> None:
    """
    Validate JSON-like dict against a JSON Schema.
    Raise ValueError with readable message when validation fails.
    """
    try:
        Draft202012Validator(schema).validate(instance)
    except ValidationError as e:
        path = ".".join([str(p) for p in e.path]) if e.path else "<root>"
        raise ValueError(f"[{where}] schema validation failed at {path}: {e.message}") from e
