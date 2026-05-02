# Runbook — CVE em dependência

## Sintomas

- Dependabot abre PR com label `security`.
- Manual: aviso em CVE feed (httpx, pydantic, etc.).
- `audit-evals.py` falha com aviso de versão vulnerável.

## Severidade

| CVE em | Sev |
|--------|-----|
| Dep do `fec_sdk` runtime (httpx, pydantic, anthropic, openai) | **SEV-1** se exploitável; **SEV-2** se mitigado |
| Dep dev (pytest, ruff, mypy) | SEV-3 |
| Dep do build pipeline (mermaid-cli, tailwind) | SEV-3 (não vai para usuário final) |

## Procedimento

1. Avaliar exploitability:
   - `httpx` SSRF? Como `fec_sdk` usa? Apenas `revoked.json` fetch — superfície limitada.
   - Outros? Avaliar caso a caso.
2. Bumpar versão na `pyproject.toml` para a fixada que corrige.
3. Regerar `releases/v<X.Y.Z>/lockfile.toml` (com `pip-compile --generate-hashes`).
4. Rodar `tests/sandbox/` + `tests/contracts/` — TUDO precisa passar.
5. Patched release `X.Y.(Z+1)` se a CVE afeta runtime do usuário.
6. Para dev/build deps: bump em PR normal, sem release.

## Comunicação

- Para SEV-1/2: GHSA + nota em release notes.
- Para SEV-3: changelog do `fec_sdk`.

## Prevenção

- Dependabot habilitado.
- SHA-pinning em GitHub Actions (PLAN item 48a).
- Dep range `>=X.Y,<X.(Y+2)` no `pyproject.toml` — atualiza minor mas não major sem revisão.
