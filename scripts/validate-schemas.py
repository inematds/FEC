#!/usr/bin/env python3
"""validate-schemas.py — valida cada manifesto JSON canônico contra seu schema.

PLAN item 95. Falha bloqueia merge.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PAIRS = [
    ("evals/v1/compat.json", "schemas/compat.schema.json"),
    ("evals/v1/revoked_versions.json", "schemas/revoked_versions.schema.json"),
    ("evals/v1/budgets.json", "schemas/budgets.schema.json"),
    ("evals/v1/models.json", "schemas/models.schema.json"),
    ("evals/v1/capabilities.json", "schemas/capabilities.schema.json"),
    ("evals/v1/alerts.json", "schemas/alerts.schema.json"),
    ("evals/v1/risk-acceptance.json", "schemas/risk-acceptance.schema.json"),
    ("evals/v1/checksums-revocation.json", "schemas/checksums-revocation.schema.json"),
]


def main() -> int:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema não instalado. Rode: pip install jsonschema>=4.21", file=sys.stderr)
        return 2

    errors: list[str] = []
    for data_path, schema_path in PAIRS:
        data_file = REPO / data_path
        schema_file = REPO / schema_path

        if not data_file.exists():
            errors.append(f"missing data file: {data_path}")
            continue
        if not schema_file.exists():
            errors.append(f"missing schema: {schema_path}")
            continue

        try:
            data = json.loads(data_file.read_text(encoding="utf-8"))
            schema = json.loads(schema_file.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            v = Draft202012Validator(schema)
            for err in v.iter_errors(data):
                path = "/".join(str(p) for p in err.path) or "(root)"
                errors.append(f"{data_path}:{path}: {err.message}")
            else:
                print(f"OK   {data_path}")
        except json.JSONDecodeError as exc:
            errors.append(f"{data_path}: invalid JSON: {exc}")

    # Schemas de quizzes: glob
    quiz_schema = json.loads((REPO / "schemas/quiz.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(quiz_schema)
    qv = Draft202012Validator(quiz_schema)
    for quiz_file in (REPO / "quizzes").glob("*.json"):
        try:
            data = json.loads(quiz_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{quiz_file}: invalid JSON: {exc}")
            continue
        for err in qv.iter_errors(data):
            path = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{quiz_file.relative_to(REPO)}:{path}: {err.message}")
        else:
            print(f"OK   {quiz_file.relative_to(REPO)}")

    if errors:
        print("\n--- VALIDATION ERRORS ---", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        print(f"\n{len(errors)} error(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
