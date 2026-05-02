# MEDIDAS — Métricas operacionais da FEC

> _Métricas declaradas e medidas. NÃO use stars/downloads como sinal de saúde. PLAN item 86._

## Saúde do CI

| Métrica | Fonte | Atualização | Atual |
|---------|-------|-------------|-------|
| `auto_smoke.pass_rate_7d` | dashboard.py | diário | _aguardando primeiro release_ |
| `auto_smoke.pass_rate_30d` | dashboard.py | diário | — |
| `auto_smoke.last_run_age_hours` | API GitHub | hourly | — |
| `bot_issue.oldest_open_age_days` | API GitHub | diário | — |
| `gh_actions.minutes_used_pct` | API GitHub Billing | semanal | — |

## Custo (PLAN item 48)

Lido via API de billing dos provedores (quando disponível) ou estimado por contagem de tokens × preço pinado.

| Tier | Limite mês | Atual | % usado |
|------|------------|-------|---------|
| auto-smoke total | $30 | _$0_ | _0%_ |
| production-smoke | $20 | _$0_ | _0%_ |
| release | $10 | _$0_ | _0%_ |
| **Total** | **$60** | _$0_ | _0%_ |

Alertas:
- 80% → SEV-3 + warning + Check Run `budget-status: neutral`.
- 100% → SEV-2 + cap nativo do provedor + bot abre PR de kill-switch.

## Saúde do conteúdo

| Métrica | Atual |
|---------|-------|
| Issues `errata` abertas | _aguardando publicação_ |
| Issues `errata` fechadas (30d) | — |
| Tempo médio fechamento `errata` por severidade | — |
| Links externos quebrados (lychee scheduled) | — |

## Saúde do uso (opt-in)

| Métrica | Atual |
|---------|-------|
| Alunos cadastrados em `FEC-BETA-FORM-v1` | — |
| Completion rate por módulo (auto-reportado) | — |
| Top 5 dúvidas (categorizadas em triagem) | — |

## Métricas vetadas como sinal de saúde

- ⛔ **Stars** sozinhas — ego metric.
- ⛔ **Downloads** sozinhos — não diferencia uso real de scraping.
- ⛔ **Tweets/posts** — ruído.

Estas servem como **contexto** para postmortems / planning, não como semáforo.

## Drills semestrais

| Data | Cenário | Tempo de resposta | Resultado |
|------|---------|-------------------|-----------|
| _futuro_ | SEV-2 dataset license violation | — | — |
| _futuro_ | Yank de SDK em TestPyPI | — | — |

## Auditoria de capacidade (semestral)

Tendência de tamanho do release zip, runtime de CI, budget mensal. Cortar se inflar.

| Snapshot | zip MB | ci-fast s | ci-scheduled min | mês $ |
|----------|--------|-----------|------------------|-------|
| 2026-05 (scaffolding) | _N/A ainda_ | — | — | $0 |

## Como atualizar

`scripts/dashboard.py` regenera os números diariamente em `docs/dashboard.html` (gh-pages, público).
Snapshot manual deste MD é ok; números detalhados ficam no dashboard.
