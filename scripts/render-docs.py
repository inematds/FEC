#!/usr/bin/env python3
"""render-docs.py — gera Markdown a partir dos JSONs canônicos. PLAN item 95.

Saída sempre tem header de aviso "_⚠️ Gerado de <arquivo>.json. NÃO edite manualmente._"
Pre-commit hook regenera; CI confirma `git diff --quiet` após render.

Uso:
    python scripts/render-docs.py            # regenera todos
    python scripts/render-docs.py --check    # exit 1 se algum diff
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

REPO = Path(__file__).resolve().parent.parent

WARNING = "> _⚠️ **Gerado de `{src}`.** NÃO edite manualmente — mudanças no MD são sobrescritas. Edite o JSON via PR (CODEOWNERS protege)._\n\n"


def render_compat() -> str:
    src = "evals/v1/compat.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# COMPAT — Matriz de Compatibilidade\n\n", WARNING.format(src=src)]
    sw = data["support_window"]
    out.append("## Janela de suporte\n\n")
    out.append(f"- **Releases do curso:** {', '.join(sw['course_releases'])}\n")
    out.append(f"- **fec_sdk minors:** {', '.join(sw['fec_sdk_minors'])}\n")
    out.append(f"- **Python minors:** {', '.join(sw['python_minors'])}\n")
    for prov, vers in sw["provider_sdk_minors"].items():
        out.append(f"- **{prov} SDK minors:** {', '.join(vers)}\n")
    out.append("\n")

    for label, key in [("Core combinations (testadas em ci-scheduled)", "core_combinations"),
                        ("Extended combinations (semanais)", "extended_combinations")]:
        out.append(f"## {label}\n\n")
        combos = data.get(key, [])
        if not combos:
            out.append("_Nenhuma combinação registrada ainda._\n\n")
            continue
        out.append("| Course | fec_sdk | Python | Provedor (SDK) | Status | Nota |\n")
        out.append("|--------|---------|--------|----------------|--------|------|\n")
        for c in combos:
            prov = f"{c['provider']['name']} ({c['provider']['sdk_version']})"
            out.append(f"| {c['course_release']} | {c['fec_sdk']} | {c['python']} | {prov} | {c['status']} | {c.get('note', '')} |\n")
        out.append("\n")
    return "".join(out)


def render_models() -> str:
    src = "evals/v1/models.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# MODELOS — Pinned por release\n\n", WARNING.format(src=src)]
    out.append(f"**Release:** {data['release']} · **Pinado em:** {data.get('pinned_at', 'N/A')}\n\n")
    out.append("| Papel | Provedor | ID | Janela | Notas |\n")
    out.append("|-------|----------|-----|--------|-------|\n")
    for role, m in data["roles"].items():
        cw = m.get("context_window", "—")
        out.append(f"| {role} | {m['provider']} | `{m['id']}` | {cw} | {m.get('notes', '')} |\n")
    out.append("\n## Política\n\n")
    out.append("- IDs incluem data de pinagem (ex.: `claude-sonnet-4-6@2026-04`).\n")
    out.append("- Modelo deprecado pelo provedor: continua executável via `fixtures/recorded/<modelo>/` por 12 meses.\n")
    out.append("- Mudança aqui exige bump em `evals/v1/HASHES.lock` (PLAN item 28a).\n")
    return "".join(out)


def render_capabilities() -> str:
    src = "evals/v1/capabilities.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# CAPACIDADES — Por provedor\n\n", WARNING.format(src=src)]
    out.append("**Status:** `native` (suporte direto), `adapter` (via `fec_sdk`), `mock` (simulação por gravação), `not_supported`.\n\n")
    for cap in data["capabilities"]:
        out.append(f"## {cap['name']} (`{cap['id']}`)\n\n")
        if cap.get("description"):
            out.append(f"{cap['description']}\n\n")
        if cap.get("taught_in_modules"):
            out.append(f"_Ensinado em:_ {', '.join('`' + m + '`' for m in cap['taught_in_modules'])}\n\n")
        out.append("| Provedor | Status | Notas |\n|----------|--------|-------|\n")
        for prov, info in cap["providers"].items():
            out.append(f"| {prov} | {info['status']} | {info.get('notes', '')} |\n")
        out.append("\n")
    return "".join(out)


def render_alerts() -> str:
    src = "evals/v1/alerts.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# ALERTS — Mapeamento métrica → severidade → ação\n\n", WARNING.format(src=src)]
    out.append("Consumido pelo `dashboard.py` e pelos runbooks.\n\n")
    out.append("| ID | Métrica | Condição | Sev | Owner | Ação | Runbook |\n")
    out.append("|-----|---------|----------|-----|-------|------|---------|\n")
    for a in data["alerts"]:
        out.append(f"| `{a['id']}` | `{a['metric']}` | {a['condition']} | **{a['severity']}** | {a['owner_role']} | {a['action']} | [{a['runbook']}](./{a['runbook']}) |\n")
    return "".join(out)


def render_risk_acceptance() -> str:
    src = "evals/v1/risk-acceptance.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# RISK-ACCEPTANCE — Aceites de risco residual\n\n", WARNING.format(src=src)]
    out.append("Apenas `severity:high` em classes NÃO bloqueantes. Classes `security`, `data-integrity`, `sandbox`, `licensing`, `lab-breaking`, `injection-bypass` **não podem** estar aqui (PLAN item 74).\n\n")
    accs = data.get("acceptances", [])
    if not accs:
        out.append("_Nenhum aceite de risco ativo._\n")
        return "".join(out)
    for a in accs:
        out.append(f"## {a['id']} — {a['class']}\n\n")
        out.append(f"- **Issue:** {a['issue']}\n- **Release:** {a['release']}\n- **Workaround:** {a['workaround']}\n")
        out.append(f"- **Disclosure:** {a['release_notes_disclosure']}\n- **Expira em:** {a['expires_at']}\n")
        out.append(f"- **Assinaturas ({len(a['signers'])}):**\n")
        for s in a["signers"]:
            out.append(f"  - {s['maintainer']} (em {s['signed_at']})\n")
        out.append("\n")
    return "".join(out)


def render_checksums_revocation() -> str:
    src = "evals/v1/checksums-revocation.json"
    data = json.loads((REPO / src).read_text())
    out = [f"# CHECKSUMS-REVOCATION — Releases revogadas\n\n", WARNING.format(src=src)]
    out.append("Lista de hashes de artefatos revogados. Consultada por `audit-evals.py` e `synthetic-check.py`.\n\n")
    revs = data.get("revoked", [])
    if not revs:
        out.append("_Nenhum artefato revogado._\n")
        return "".join(out)
    for r in revs:
        out.append(f"## {r['release']} — {r['artifact']}\n\n")
        out.append(f"- **Motivo:** {r['reason']}\n- **Revogado em:** {r['revoked_at']}\n- **Sucessor:** `{r['successor']}`\n")
        out.append(f"- **sha256:** `{r['sha256']}`\n- **blake3:** `{r['blake3']}`\n")
        if r.get("advisory_url"):
            out.append(f"- **Advisory:** {r['advisory_url']}\n")
        out.append("\n")
    return "".join(out)


TARGETS = {
    "COMPAT.md": render_compat,
    "MODELOS.md": render_models,
    "CAPACIDADES.md": render_capabilities,
    "ALERTS.md": render_alerts,
    "RISK-ACCEPTANCE.md": render_risk_acceptance,
    "CHECKSUMS-REVOCATION.md": render_checksums_revocation,
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="exit 1 if any file would change")
    args = p.parse_args()

    changed: list[str] = []
    for filename, renderer in TARGETS.items():
        new = renderer()
        target = REPO / filename
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        if old != new:
            changed.append(filename)
            if not args.check:
                target.write_text(new, encoding="utf-8")
                print(f"WROTE {filename}")
        else:
            print(f"OK    {filename}")

    if args.check and changed:
        print(f"\nDIFF: {len(changed)} file(s) need regeneration: {', '.join(changed)}", file=sys.stderr)
        print("Rode: python scripts/render-docs.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
