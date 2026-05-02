# Runbook — Release ruim publicado (SEV-1/2)

> **Esta é uma escalada do `RELEASE-INCIDENT.md`.** Use este runbook em conjunto.

## Sintomas

- Bug grave reportado em `v1.0.0` (ou mais recente).
- `synthetic-check` detectando drift, sha256 mismatch, ou install falhando.
- Beta tester reportando que `pip install fec-sdk==1.0.0 && fec_sdk.selftest()` não funciona.

## Severidade

| Caso | Sev |
|------|-----|
| Secret no zip; XSS publicado; sandbox quebrado | **SEV-1** |
| Bug que invalida P5 ou principal lab | **SEV-2** |
| Errata de conteúdo, link 404 | SEV-3 (não usa este runbook) |

## Procedimento de yank (SEV-1/2 do release)

Siga a checklist do [`RELEASE-INCIDENT.md`](../RELEASE-INCIDENT.md) literalmente. Resumo:

1. **Banner de deprecação** — PR rápido em `index.html` + `README.md` + atualizar `assets/banners/deprecation.html`.
2. **Edit do GitHub Release:** título com "⚠️ DEPRECATED — see vX.Y.Z"; assets renomeados com `-DEPRECATED-DO-NOT-USE`.
3. **Atualizar `evals/v1/checksums-revocation.json`** com sha256/blake3 do zip ruim, motivo, sucessor. `audit-evals.py` passa a falhar em qualquer referência a hash revogado.
4. **Não delete a tag** — preserva história.
5. **Publique `v1.0.1`** (ou `v1.0.0-revoked.1`) com fix:
   - Se SDK também quebrado, seguir `runbooks/sdk-yank.md` em paralelo.
   - Lockfile da nova release atualizado.
6. **Pages:** `rollback-pages.py` para `/latest/` apontar para sucessor; shell de deprecação em `/v1.0.0/index.html` se necessário.
7. **Zenodo:** novo depósito com `IsNewVersionOf` ligando ao DOI antigo + nota no original.
8. **Comunicação:**
   - Discussion fixada no repo.
   - Update no anúncio original (LinkedIn/X).
   - E-mail para alunos beta cadastrados.
   - GHSA público se aplicável.

## Postmortem

Obrigatório dentro de 7 dias. Salve em `postmortems/<data>-<slug>.md`.

## Prevenção

- Adicione caso ao gate de promoção rc→stable se não estava coberto.
- Adicione synthetic check específico se aplicável.
- Drill semestral validando o procedimento.
