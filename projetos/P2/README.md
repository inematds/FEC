# P2 — Agente com tools

**Status:** GA · entrega após T4.1-T4.2.
**Tempo estimado:** 4-6h.

## Objetivo

Construa um agente single que combina **3 tools** (busca local + cálculo + leitura de arquivo), com tracing por step. Foco em loops infinitos, recovery, tool errors.

## O que entregar

- `agent.py` — agente em ReAct ou planner/executor (sua escolha, justifique).
- `tools/` — implementações dos 3 tools, todas dentro de `FilesystemSandbox`.
- `traces/` — output de tracing de pelo menos 30 chamadas distintas.
- `report.md` — análise de modos de falha encontrados e como o agente recupera.

## Critérios bloqueantes

Ver [`RUBRIC.md`](./RUBRIC.md). Resumo:

- [ ] **Bateria sandbox (`tests/sandbox/test_traversal.py`) verde.** P2 não pode virar GA com sandbox quebrado.
- [ ] Passa em **30/30 traços-canário** sem loop infinito.
- [ ] Tracing por step (entrada, decisão, tool call, resultado, próximo step).
- [ ] Recuperação documentada de pelo menos 5 modos de falha (tool retorna erro, JSON inválido, tool indisponível, etc.).
- [ ] Custo médio ≤ orçamento definido em `evals/v1/budgets.json` (`FEC-BUDGET-AGENT-v1`).

## Sandbox obrigatório

Todo tool que toca filesystem usa `FilesystemSandbox`. Tools que tocam rede usam `NetworkPolicy` com allowlist explícita. Bateria de testes em `tests/sandbox/` é gate.

## Conhecimento aplicado

- T1.1 (atenção) → ordem do system prompt + ancoragem da query.
- T2.2 (versionamento) → prompt do agente versionado e testado.
- T4.1 (tool calling) → schemas JSON, validação, error handling.
- T4.2 (agentes) → ReAct loop, condições de parada, recovery.
- T6.1 (eval) → traços-canário com tracing.

## Quando NÃO fazer este projeto

- Se você não terminou T4.2.
- Se a tarefa real é classificação simples — não precisa de agente, use prompt direto.

## Submissão

Branch `projetos/p2-<seu-handle>`. PR com label `projeto:P2`.
