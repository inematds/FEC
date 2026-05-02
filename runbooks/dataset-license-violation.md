# Runbook — Violação de licença de dataset/conteúdo

## Sintomas

- Issue / e-mail / DMCA reportando que o curso usa material com licença incompatível.
- Auditoria interna identificando fixture sem entrada em `LICENSES-THIRD-PARTY.md`.
- CI bloqueia PR que adiciona fixture sem licença.

## Severidade

**SEV-2** (ou SEV-1 se DMCA com prazo legal).

## Procedimento

1. **Identificar o ativo:** dataset, screenshot, abstract de paper, diagrama-base, código de terceiro.
2. **Verificar `LICENSES-THIRD-PARTY.md`:** está listado? Licença citada bate com a real?
3. **Avaliar resolução:**
   - **Fixture pode ser substituída?** Se há equivalente CC/MIT/domínio público, troque.
   - **Atribuição faltando?** Adicione no manifesto e nos módulos que usam.
   - **Licença incompatível e sem substituto?** Remova; reescreva sem o material; faça nova fixture sintética.
4. **Yank de release** se afetar release publicada (seguir `runbooks/bad-release.md`).
5. **PR de correção** referenciando o reporter (com permissão).

## Comunicação

- Resposta ao reporter dentro de 48h confirmando recebimento, mesmo que sem solução ainda.
- Update em `LICENSES-THIRD-PARTY.md`.
- Postmortem público se afetou release.

## Prevenção

- CI bloqueia fixture sem entrada no manifesto (PLAN item 44).
- Revisão técnica externa inclui auditoria de licenças.
- Política em `CONTRIBUTING.md`: PR com fixture exige declaração de fonte e licença compatível.
