#!/usr/bin/env python3
"""check-budgets.py — orçamento de assets/CI. PLAN item 91.

Bloqueante em ci-fast e release.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# PLAN item 91 — orçamentos
ZIP_MAX_BYTES = 80 * 1024 * 1024     # release zip ≤ 80 MB
SVG_MAX_BYTES_EACH = 300 * 1024      # SVG por imagem ≤ 300 KB
SVG_MAX_PER_MODULE = 8
SVG_MAX_TOTAL_PER_MODULE_BYTES = 1_500_000
REPO_MAX_BYTES = 500 * 1024 * 1024


def check_svgs() -> list[str]:
    """Cada SVG ≤300 KB; cada módulo ≤8 SVGs e ≤1.5 MB de SVG."""
    errors: list[str] = []
    by_module: dict[str, list[Path]] = {}

    for svg in REPO.rglob("*.svg"):
        if "node_modules" in svg.parts or "venv" in svg.parts:
            continue
        if svg.stat().st_size > SVG_MAX_BYTES_EACH:
            errors.append(f"SVG > 300KB: {svg.relative_to(REPO)} ({svg.stat().st_size} bytes)")

        # tentar atribuir a um módulo
        for part in svg.parts:
            if part.startswith("modulo-"):
                by_module.setdefault(part, []).append(svg)
                break

    for module, svgs in by_module.items():
        if len(svgs) > SVG_MAX_PER_MODULE:
            errors.append(f"{module}: {len(svgs)} SVGs (max {SVG_MAX_PER_MODULE})")
        total = sum(s.stat().st_size for s in svgs)
        if total > SVG_MAX_TOTAL_PER_MODULE_BYTES:
            errors.append(f"{module}: SVG total {total} bytes (max {SVG_MAX_TOTAL_PER_MODULE_BYTES})")
    return errors


def check_repo_size() -> list[str]:
    """Repo (excl. .git) ≤ 500 MB."""
    total = 0
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        if any(part in {".git", "node_modules", ".venv", "__pycache__", "dist", "build"} for part in p.parts):
            continue
        total += p.stat().st_size
    if total > REPO_MAX_BYTES:
        return [f"Repo size {total} bytes > {REPO_MAX_BYTES} (500 MB)"]
    return []


def check_release_zip() -> list[str]:
    """Se existe dist/fec-*.zip, deve ser ≤ 80 MB."""
    errors: list[str] = []
    for zipf in (REPO / "dist").glob("fec-*.zip") if (REPO / "dist").exists() else []:
        size = zipf.stat().st_size
        if size > ZIP_MAX_BYTES:
            errors.append(f"Release zip {zipf.name} {size} bytes > {ZIP_MAX_BYTES} (80 MB)")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(check_svgs())
    errors.extend(check_repo_size())
    errors.extend(check_release_zip())

    if errors:
        print("--- BUDGET ERRORS ---", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        print("\nVer PLAN item 91. Adicione exceção em BUDGETS-EXCEPTIONS.md se necessário.", file=sys.stderr)
        return 1
    print("OK — budgets respected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
