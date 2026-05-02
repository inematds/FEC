# Runbook — Yank de `fec-sdk` no PyPI (SEV-1)

## Sintomas

- Vulnerabilidade descoberta em `fec-sdk==X.Y.Z` publicada.
- Bug grave que invalida labs (lab-breaking).
- License issue.
- Reporter externo (GHSA, alguma issue).

## Severidade

**SEV-1** quase sempre — pacote publicado em PyPI tem alcance amplo e instalado por terceiros. Janela 24/7 pós-release ≤2h.

## Procedimento (alinhado a PLAN item 79a)

### 1. PyPI yank (≤30 min)

```bash
# Não é "delete" — yank apenas marca como "não preferida" para resolvers.
# Quem fixou explicitamente ainda recebe; quem usa range não recebe mais.
twine yank fec-sdk==X.Y.Z --reason "Brief reason; see GHSA-..."
```

### 2. GHSA + OSV advisory (≤2h)

- Em GitHub: `Security → Advisories → New advisory`.
- Severidade CVSS, descrição, versões afetadas, versão corrigida (se já houver).
- Publicação automática para o OSV via integração GitHub.

### 3. Atualizar denylist (≤2h)

`evals/v1/revoked_versions.json` (CODEOWNERS-protegido):

```json
{
  "revoked": [
    {
      "package": "fec-sdk",
      "version": "X.Y.Z",
      "reason": "security",
      "revoked_at": "2026-MM-DDTHH:MM:SSZ",
      "successor": "X.Y.(Z+1)",
      "advisory_url": "https://github.com/inematds/FEC/security/advisories/GHSA-..."
    }
  ]
}
```

`render-docs.py` atualiza `MODELOS.md` (não — é `revoked_versions` que é renderizada apenas via auditoria pública). `audit-evals.py` passa a falhar em qualquer release que liste a versão como suportada.

### 4. Release patched (`X.Y.(Z+1)`) (≤24h)

- PR com fix.
- Build determinístico via `release.yml`.
- Lockfile atualizado.
- Manifesto remoto `https://inematds.github.io/FEC/v1/revoked.json` regenerado e re-assinado.

### 5. Manifesto remoto assinado

`scripts/sign-manifest.py` regenera `revoked.json` com assinatura. Deploy em `gh-pages` na sub-path `/v1/`.

`fec_sdk.check_compat()` em runtime busca este manifesto (TTL 24h) e levanta `RevokedVersionError` em versões revogadas.

### 6. Comunicação

- Banner de deprecação em `index.html` + página da release antiga.
- Mensagem do `RevokedVersionError` traz comando exato: `pip install -U fec-sdk==X.Y.(Z+1)`.
- Discord, e-mail para beta testers.
- Tweet/post curto se vulnerabilidade pública.

## Limitação a declarar

Wheels já instalados que **rodam offline ou com cache local válido** (TTL 24h) NÃO recebem revogação até próxima conexão ou expiração do cache. `SECURITY.md` documenta isso explicitamente.

## Postmortem

Obrigatório. Foco: como o bug entrou em release; por que `tests/sandbox/`, `audit-evals.py`, ou peer review não pegaram.

## Drill semestral

Simular yank em **TestPyPI** (não em PyPI público). Cronometrar resposta. Resultado em `MEDIDAS.md`.
