# RELEASE-INCIDENT — Checklist de yank de release ruim

> _Para SEV-1/SEV-2 em release publicada. Use junto com `RUNBOOK.md` e `runbooks/bad-release.md`._

## Severidades

- **SEV-1:** secret no zip, malware, exfil real, XSS em produção, sandbox quebrado.
- **SEV-2:** módulo GA com erro técnico que invalida lab, benchmark errado, quebra de licença.

## Checklist linear (siga em ordem; cada passo tem owner e prazo)

### Passo 1 — Confirmar incidente (≤30 min)

- [ ] Reproduzir o problema localmente (se possível).
- [ ] Identificar versão afetada (`v1.0.0`, `v1.0.0-rc.X`, etc.).
- [ ] Identificar artefatos afetados (zip, wheel, Pages, Zenodo).
- [ ] Classificar severidade.

### Passo 2 — Banner de deprecação (≤1h)

- [ ] PR no banner: `assets/banners/deprecation.html` atualizado com data, severidade, link.
- [ ] PR em `index.html` e `README.md` adicionando o banner via `<picture>` ou inline.
- [ ] Merge com label `release-incident` (CODEOWNERS aprovam rápido).
- [ ] Pages rebuild verifica via `synthetic-check.py`.

### Passo 3 — Editar GitHub Release (≤2h)

- [ ] Título atualizado: `⚠️ DEPRECATED — see vX.Y.Z` (X.Y.Z = sucessor).
- [ ] Notes editadas: bloco "## ⚠️ Deprecated" no topo com motivo + link para sucessor.
- [ ] Assets renomeados via `gh release upload --clobber` com sufixo `-DEPRECATED-DO-NOT-USE`.
- [ ] **NÃO delete a tag** — preserva história e quebra menos quem clonou.

### Passo 4 — `evals/v1/checksums-revocation.json` (≤2h)

PR atualizando o manifesto:

```json
{
  "revoked": [{
    "release": "v1.0.0",
    "artifact": "fec-v1.0.0.zip",
    "sha256": "<hash do zip ruim>",
    "blake3": "<hash blake3>",
    "reason": "<security|data-integrity|lab-breaking|...>",
    "revoked_at": "2026-MM-DDTHH:MM:SSZ",
    "successor": "v1.0.1",
    "advisory_url": "https://github.com/inematds/FEC/security/advisories/GHSA-..."
  }]
}
```

`render-docs.py` regenera `CHECKSUMS-REVOCATION.md`.
`audit-evals.py` passa a falhar em qualquer release que aponte para hash revogado.

### Passo 5 — Pages rollback (≤2h)

- [ ] `scripts/rollback-pages.py` opção A (swap `/latest/` para sucessor) OU opção B (shell de deprecação em `/v1.0.0/index.html`).
- [ ] `synthetic-check.py` verifica que `/latest/` aponta para sucessor.

### Passo 6 — Sucessor `v1.0.1` (≤24h)

- [ ] Branch a partir do commit do `v1.0.0` + fix.
- [ ] Smoke + tests verdes.
- [ ] Release via `release.yml` workflow_dispatch.
- [ ] Lockfile atualizado (`releases/v1.0.1/lockfile.toml`).
- [ ] Verificação pós-upload no PyPI.
- [ ] Zenodo successor com `IsNewVersionOf` apontando ao DOI antigo.

### Passo 7 — Comunicação (≤24h pós-banner)

- [ ] **GitHub Discussion fixada** com timeline e instrução de upgrade.
- [ ] Update no anúncio original (LinkedIn/X).
- [ ] **E-mail para alunos beta cadastrados** (lista em `MEDIDAS.md` opt-in).
- [ ] Discord post em `#fec-announcements`.
- [ ] **GHSA público** se SEV-1 segurança (gera CVE).

### Passo 8 — Postmortem (≤7 dias úteis)

Salvar em `postmortems/<YYYY-MM-DD>-<slug>.md` usando template em `RUNBOOK.md#postmortem`. Inclui:

- Timeline UTC com cada passo do checklist e duração.
- Causa raiz (5 porquês).
- Por que gates de promoção (PLAN item 74) não pegaram.
- Mudanças nos gates / runbooks / código para prevenir.

### Passo 9 — Drill subsequente

Próximo drill semestral exercita o cenário específico que ocorreu. Update em `MEDIDAS.md`.

## Failure modes do próprio runbook

| Se... | Fallback |
|-------|----------|
| Zenodo offline | Seguir `runbooks/zenodo-down.md`. Não bloqueia release principal. |
| PyPI offline | Seguir `runbooks/pypi-down.md`. Comunique URL alternativa. |
| Pages offline | `index.html` no asset zip do GitHub Release como contingência. |
| Maintainer único disponível | Use `BREAK-GLASS.md` para ações pré-autorizadas; postmortem captura sub-staffing. |
