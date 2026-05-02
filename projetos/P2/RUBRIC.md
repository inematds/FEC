# P2 — Rubrica

## Bloqueantes

| # | Critério | Como verificar |
|---|----------|----------------|
| 1 | `tests/sandbox/test_traversal.py` verde | `pytest tests/sandbox/` — 19/19 passa |
| 2 | 30/30 traços-canário passam | `python eval.py --traces tests/canarios/` |
| 3 | Sem loop infinito (timeout ≤ 30s por chamada) | Tracing inclui step count e wall time |
| 4 | Tracing estruturado por step | Cada `traces/<id>.json` tem entries por step com timestamp, tool name, args (sanitizadas), result, next |
| 5 | Recovery de 5+ modos de falha | `report.md` documenta com exemplos |
| 6 | Custo médio ≤ FEC-BUDGET-AGENT-v1 | `metrics.json` |
| 7 | Tools usam sandbox / NetworkPolicy | Code review |
| 8 | Determinístico em traços canário | Sementes fixas; reruns idênticos |

## Crédito extra

- Comparação ReAct vs. planner/executor com mesma tarefa, ambos passando, ablation de custo/qualidade.
- Defesa básica contra prompt injection nos tool inputs (preview de T6).

## Anti-patterns

- ❌ Tool que faz `os.system(...)` ou `subprocess.run(...)` direto.
- ❌ Agente sem `max_iterations` — risco de loop infinito.
- ❌ "Recovery" que só ignora erro silenciosamente.
- ❌ Tool que escreve fora do sandbox.
