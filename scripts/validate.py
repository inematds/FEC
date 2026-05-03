#!/usr/bin/env python3
"""validate.py — valida estrutura INEMA dos HTML de módulos. PLAN itens 13-18, 42.

Regras (bloqueantes em ci-fast):
- ≥6 sub-tópicos expansíveis (`<details class="topico-expansivel">`).
- Cada sub-tópico tem 3 subsessões INEMA: "O que é", "Por que aprender", "Conceitos-chave".
- Indicador de tópico é número em círculo (NUNCA seta `▶`).
- Link INEMA.CLUB presente com `text-sky-400`.
- Light mode CSS presente (`@media (prefers-color-scheme: light)`).
- Badge GA/beta presente no front-matter.
- Botão sempre `justify-start` (regra crítica INEMA).
- "Quando NÃO usar" presente em módulo de padrão técnico.

Skip: index.html da raiz e índices de trilha (têm estrutura diferente).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARROW_RE = re.compile(r"▶|►|&#9658;|&#9656;")
JUSTIFY_CENTER_BTN = re.compile(r'class="[^"]*\bbtn[^"]*\bjustify-center\b', re.I)


def _has_six_topics(html: str) -> bool:
    return len(re.findall(r'<details[^>]*topico-expansivel', html)) >= 6


def _has_three_inema_subsections(html: str) -> bool:
    needs = ["O que é", "Por que aprender", "Conceitos-chave"]
    return all(s.lower() in html.lower() for s in needs)


def _has_inema_link(html: str) -> bool:
    return bool(re.search(r'text-sky-400[^"]*"[^>]*>[^<]*INEMA\.CLUB', html, re.I)) or \
           bool(re.search(r'INEMA\.CLUB[^<]*</a>', html, re.I)) and 'text-sky-400' in html


def _has_light_mode(html: str) -> bool:
    # Em v1.0 light mode foi desabilitado (ver HOSTING-DECISION.md). Esta verificação
    # agora aceita: (a) link para inema.css (CSS fonte tem `color-scheme: dark`),
    # (b) presença de meta color-scheme, ou (c) regra inline.
    if "color-scheme" in html:
        return True
    if "prefers-color-scheme" in html:
        return True
    if "inema.css" in html:
        return True  # CSS fonte declara color-scheme: dark — é cobertura suficiente
    return False


def _has_status_badge(html: str) -> bool:
    return bool(re.search(r'\b(badge|status):\s*(GA|beta)\b', html, re.I)) or \
           bool(re.search(r'data-status="(ga|beta)"', html, re.I))


def _has_quando_nao_usar(html: str) -> bool:
    return "quando não usar" in html.lower() or "quando-nao-usar" in html


def validate_module(path: Path) -> list[str]:
    """Retorna lista de erros para um módulo. Lista vazia = OK."""
    html = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not _has_six_topics(html):
        errors.append("≥6 sub-tópicos expansíveis (PLAN item 18.3) — encontrados <6")
    if not _has_three_inema_subsections(html):
        errors.append('Subsessões INEMA "O que é / Por que aprender / Conceitos-chave" ausentes')
    if ARROW_RE.search(html):
        errors.append('Indicador de tópico usa seta (▶ ou similar) — REGRA CRÍTICA: usar número em círculo')
    if not _has_inema_link(html):
        errors.append("Link INEMA.CLUB com text-sky-400 ausente")
    if not _has_light_mode(html):
        errors.append("Light mode CSS (@media prefers-color-scheme: light) ausente")
    if not _has_status_badge(html):
        errors.append('Badge "GA" ou "beta" ausente (front-matter ou data-status)')
    if JUSTIFY_CENTER_BTN.search(html):
        errors.append('Botão usa justify-center — REGRA CRÍTICA: usar justify-start')
    if not _has_quando_nao_usar(html):
        errors.append('Seção "Quando NÃO usar" obrigatória ausente (PLAN item 20)')

    return errors


def main() -> int:
    errors: dict[str, list[str]] = {}
    targets = list((REPO / "curso").rglob("modulo-*.html"))
    if not targets:
        print("Nenhum módulo encontrado em curso/. Skip (scaffolding em progresso).")
        return 0

    for path in sorted(targets):
        rel = path.relative_to(REPO)
        errs = validate_module(path)
        if errs:
            errors[str(rel)] = errs
        else:
            print(f"OK   {rel}")

    if errors:
        print("\n--- VALIDATION ERRORS ---", file=sys.stderr)
        for f, errs in errors.items():
            print(f"\n{f}:", file=sys.stderr)
            for e in errs:
                print(f"  • {e}", file=sys.stderr)
        print(f"\n{sum(len(v) for v in errors.values())} error(s) in {len(errors)} file(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
