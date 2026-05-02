# Runbook — `auto-smoke` falhando

## Sintomas

- Issue automática `[FEC-AUTO] auto-smoke:<provider>:<class>` aberta.
- Workflow `ci-scheduled.auto-smoke` red por 2+ runs consecutivos.
- Check Run `budget-status` em `failure` (budget esgotado) ou `neutral` (kill-switched).

## Severidade

- 1 dia red → SEV-3 (warning).
- 2 dias seguidos red → **SEV-2** (PLAN ALERT `AUTO-SMOKE-FAIL-2D`).
- Em janela 24/7 pós-release → SEV-2 escala para SEV-1 se afeta release.

## Diagnóstico em 5 min

1. Abrir o run mais recente em GitHub Actions.
2. Buscar nos logs (já redatados via `redact.py`):
   - `ProviderError`: rede, auth, rate limit?
   - `AssertionError` em canário: o modelo mudou comportamento?
   - Timeout: latência do provedor disparou?
3. Verificar `evals/v1/SMOKE-KILLSWITCH.json` — está `enabled: true`? Se sim, ver `since` e `expected_off_until`.
4. Verificar Check Run `budget-status` mais recente.
5. Verificar `synthetic-check.py` — outros canais (Pages/PyPI/Zenodo) também down?

## Mitigação

| Causa | Ação |
|-------|------|
| Provider rate limit | Reduzir frequência (ex.: `cron 17 18 * * *` se diário sobrecarrega), aguardar 1h, retry. |
| Modelo deprecou | Seguir `runbooks/provider-deprecation.md`. Atualizar `evals/v1/models.json`. |
| Mudança de comportamento (drift) | Investigar canário falhante. Atualizar canário se a mudança é benigna; abrir issue se é regressão real. |
| Auth/secrets | Rotacionar via `BREAK-GLASS.md`. NUNCA commitar key. |
| Budget esgotado | Cap nativo do provedor já cortou. Investigar gasto inesperado. Se justificado, abrir PR aumentando `budgets.json` (CODEOWNERS-protegido). |
| Kill-switch ativado | Verificar quem ligou e por quê (`reason` em SMOKE-KILLSWITCH.json). Se resolvido, abrir PR desligando. |

## Comunicação

- Comentar na issue automática com diagnóstico (não fechar manualmente; auto-close após N runs verdes).
- Em SEV-2, postar em `#fec-oncall` com link para o run e ETA.

## Postmortem

Trigger: causa raiz não-óbvia, mais de 1 dia para resolver, ou impacto em alunos beta. Template em `RUNBOOK.md#postmortem`.

## Prevenção

- Canário muito sensível a drift do provedor → relaxar para padrão estável.
- Provedor quebra com frequência → mover para `extended` em `compat.json`.
