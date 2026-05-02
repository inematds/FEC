# Runbook — `pip install fec-sdk` falhando

## Sintomas

- Synthetic monitor (`PYPI-INSTALL-FAIL`) red — 3 falhas consecutivas em venv limpo.
- Aluno reporta `ERROR: No matching distribution found for fec-sdk==X.Y.Z`.
- `pip install --require-hashes` falha em hash mismatch.

## Severidade

**SEV-1** — canal canônico de instalação está quebrado.

## Procedimento

1. **Verifique status do PyPI:** [status.python.org](https://status.python.org). Outage geral? Aguardar.
2. **Se versão específica não resolve:**
   - Foi yankada? Verifique `evals/v1/revoked_versions.json`.
   - Subiu corretamente? Verifique `release.yml` log do `publish-pypi`.
3. **Hash mismatch (`--require-hashes`):**
   - Recompute sha256 do wheel disponibilizado pelo PyPI: `pip download fec-sdk==X.Y.Z --no-deps`.
   - Compare com `releases/v<X.Y.Z>/lockfile.toml` e `CHECKSUMS.txt` da Release.
   - **Se mismatch:** PyPI servindo bytes diferentes do que foi auditado → SEV-1, **yank imediato** e investigação.
4. **Mitigação interim:** anuncie alternativa: `pip install <URL do GitHub Release wheel>` com hash explicit.
5. **Patched release `X.Y.(Z+1)`** se foi yank legítimo.

## Comunicação

- Banner: "PyPI install temporariamente quebrado. Use: ..." com URL do Release asset.
- Discord, e-mail beta.
- Update em `docs/status.html`.

## Prevenção

- Trusted Publishing (sem token) — reduz superfície de ataque.
- Build determinístico com `SOURCE_DATE_EPOCH` fixado — `verify-pypi-post-upload.sh` valida hash pós-publicação.
- Cap de monthly upload no PyPI? Não aplicável; mas Trusted Publishing já protege.
