# Runbook — GitHub Pages servindo conteúdo errado

## Sintomas

- Synthetic monitor (`PAGES-CHECKSUM-DRIFT`) detecta sha256 do HTML servido ≠ `pages-checksums.txt` da release.
- Beta tester reportando 404 ou conteúdo desatualizado em `inematds.github.io/FEC/v1.0.0/...`.
- Sem CSP nas respostas (verificar via `synthetic-check.py`).

## Severidade

**SEV-1** se drift de checksum em path versionado imutável (`/v1.0.0/`) — significa deploy comprometido OU bug de deploy.

## Procedimento

1. **Verifique o deploy:** rerun do `release.yml` `publish-pages-versioned` job? Foi acidentalmente reexecutado?
2. **Compare o que está servido vs. o que está em `gh-pages`:**
   - `git fetch origin gh-pages && git checkout gh-pages`
   - confronte `v1.0.0/` local com a URL pública
3. **Rollback de Pages** via `scripts/rollback-pages.py` se confirmado:
   - opção A — flip do alias `/latest/` para sucessor.
   - opção B — shell de deprecação em `index.html` da versão afetada.
4. **Investigue causa raiz:** workflow editado? Token comprometido? Rebuild diário do `/status/` invadiu `/v1.0.0/`?

## Comunicação

- Banner em `index.html` (raiz) avisando "Pages incidente em <data>".
- Issue público com label `incident`.
- Postmortem em `postmortems/`.

## Prevenção

- Path versionado imutável (`/v1.0.0/` nunca rebuilta — PLAN item 74a).
- `audit-pages.py` no release.yml gate.
- Branch protection em `gh-pages` para changes em `/v*/` exigirem PR.
