# P5 — Rubrica (gate final do curso)

## Bloqueantes

| # | Critério | Como verificar |
|---|----------|----------------|
| 1 | Sandbox verde (herdado de P2) | `pytest tests/sandbox/` |
| 2 | Golden de 50 entradas próprio | `goldens/p5-<handle>.json` schema-validado |
| 3 | ≥18/20 do FEC-GS-INJECTION-v1 bloqueados | `python eval-injection.py` |
| 4 | Dashboard local funcional | `dashboard.html` abre offline e renderiza dados de `traces/` |
| 5 | p95 latência ≤ FEC-BUDGET-LAT-v1 | `metrics.json` com `p95_ms <= budget` |
| 6 | Documento de operação | `OPERATIONS.md` com runbook próprio (mini-RUNBOOK.md) |
| 7 | Plano de rollback documentado | Como você rollbacka uma versão ruim do agente |
| 8 | Custo médio dentro de budget | `metrics.json` |

## Crédito extra

- Implementação de pelo menos 2 padrões de defesa contra injection ALÉM dos 4 ensinados.
- Análise A/B de 2 prompts do agente com significância estatística.
- Integration com observability provider (DataDog, Honeycomb, etc.) opcional.

## Anti-patterns

- ❌ "Defesa contra injection" que é só `input.replace("ignore previous", "")`.
- ❌ Dashboard que precisa de servidor — deve ser HTML estático local.
- ❌ Golden de 50 entradas todas similares (diversidade obrigatória).
- ❌ Plano de rollback que diz "git revert" — precisa ser concreto.

## Sinal final do curso

P5 aprovado + quiz final ≥80% = elegível para certificado FEC v1.0.

Maintainer comenta no PR de submissão e gera `certificados/<handle>.html`.
