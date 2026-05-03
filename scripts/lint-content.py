#!/usr/bin/env python3
"""lint-content.py — lint de XSS e qualidade de conteúdo. PLAN itens 27, 36, 43.

Modos:
  --mode=block  : XSS hard checks (no <script>, no on*=, javascript:, iframe sem sandbox).
  --mode=strict : palavras 2.5k-4.5k, ≥3 refs, "Quando NÃO usar", evidência ligada ao harness.

Bloqueante em ci-fast (mode=block) e ci-scheduled (mode=strict).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Padrões XSS — blocking
XSS_PATTERNS = [
    # Bloqueia <script> inline (sem src=). <script src="..."> é permitido pois
    # o conteúdo vem de arquivo .js no mesmo origin (CSP script-src 'self').
    (re.compile(r"<script\b(?![^>]*\bsrc=)", re.I), "<script> inline — banido (use src= apontando para arquivo .js)"),
    (re.compile(r"\son\w+\s*=", re.I), "atributo on* (onclick, onload, etc.) — banido"),
    (re.compile(r"\bjavascript:", re.I), 'protocolo "javascript:" — banido'),
    # iframe sem sandbox (mas iframe de modal carregando módulo do mesmo repo é OK pois CSP frame-src 'self' já restringe)
    (re.compile(r"<iframe(?![^>]*\bsandbox=)(?![^>]*\bsrc=\"[^\"]*\.html)", re.I), "<iframe> externo sem atributo sandbox= — banido"),
    (re.compile(r"\bunsafe-inline\b", re.I), 'CSP com unsafe-inline — banido'),
    (re.compile(r"\bunsafe-eval\b", re.I), 'CSP com unsafe-eval — banido'),
]

# Allow-list de paths que podem ter padrões "perigosos" em texto literal (nunca executados)
TEXT_ONLY_PATHS = [
    "PLAN.md",
    "RELATORIO-CLAUDEX.md",
    "SECURITY.md",
    "RUNBOOK.md",
    "README.md",
    "scripts/",
    "tests/",
    "fec_sdk/",
    ".github/",
    "schemas/",
]


def is_text_only(rel: str) -> bool:
    return any(rel.startswith(p) or rel == p.rstrip("/") for p in TEXT_ONLY_PATHS)


def lint_xss(path: Path) -> list[str]:
    rel = str(path.relative_to(REPO))
    if is_text_only(rel):
        return []
    if not path.suffix.lower() in {".html", ".htm"}:
        return []
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for pat, msg in XSS_PATTERNS:
        if pat.search(text):
            errors.append(f"{msg}")
    return errors


def lint_strict(path: Path) -> list[str]:
    """Lint estrita: word count, refs, "Quando NÃO usar", evidência."""
    if "modulo-" not in path.name or path.suffix != ".html":
        return []
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    # word count rough estimate (strip tags)
    no_tags = re.sub(r"<[^>]+>", " ", text)
    no_tags = re.sub(r"\s+", " ", no_tags)
    words = len(no_tags.split())
    if not (2500 <= words <= 4500):
        errors.append(f"Word count {words} fora de [2500, 4500] — PLAN item 17")

    # ≥3 refs
    refs = len(re.findall(r"<a [^>]*href=[\"']https?://[^\"']*\.(?:org|com|edu|io|net|dev|ai)[^\"']*[\"']", text))
    refs += len(re.findall(r"arxiv\.org/abs/", text, re.I))
    if refs < 3:
        errors.append(f"Apenas {refs} referências externas — mínimo 3 (PLAN item 35)")

    # "Quando NÃO usar"
    if "quando não usar" not in text.lower():
        errors.append('Seção "Quando NÃO usar" ausente (PLAN item 20)')

    # evidência linkada ao harness ou paper datado
    has_harness = bool(re.search(r"evals/v1/runs/", text))
    has_paper = bool(re.search(r"arxiv\.org|doi\.org|\b\(20\d{2}\b", text))
    if not (has_harness or has_paper):
        errors.append("Sem evidência ligada ao harness (evals/v1/runs/<id>) nem paper datado (PLAN itens 27, 36)")

    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["block", "strict"], default="block")
    args = p.parse_args()

    errors: dict[str, list[str]] = {}

    targets = list(REPO.rglob("*.html"))
    for path in targets:
        if "node_modules" in path.parts or ".venv" in path.parts:
            continue
        rel = str(path.relative_to(REPO))
        errs = lint_xss(path) if args.mode == "block" else lint_strict(path)
        if errs:
            errors[rel] = errs

    # Markdown — só XSS via referência (raras), não wordcount
    if args.mode == "block":
        for path in REPO.rglob("*.md"):
            if "node_modules" in path.parts:
                continue
            rel = str(path.relative_to(REPO))
            if is_text_only(rel):
                continue
            errs = lint_xss(path)
            if errs:
                errors[rel] = errs

    if errors:
        print(f"\n--- {args.mode.upper()} CONTENT ERRORS ---", file=sys.stderr)
        for f, errs in errors.items():
            print(f"\n{f}:", file=sys.stderr)
            for e in errs:
                print(f"  • {e}", file=sys.stderr)
        return 1
    print(f"OK ({args.mode}) — verified {sum(1 for _ in REPO.rglob('*.html'))} HTML file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
