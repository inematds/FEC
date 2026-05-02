# P5 — Pipeline em produção

**Status:** GA · entrega final do curso. Após T6.1.
**Tempo estimado:** 6-10h.

## Objetivo

Pegue o **P2** (agente com tools) e adicione:

1. **Evals offline** com golden de 50 entradas que VOCÊ define.
2. **Tracing dashboard** simples (HTML estático local lendo seus traces).
3. **Defesa contra prompt injection** com red-team mínimo (golden FEC-GS-INJECTION-v1, ≥18/20 bloqueados).

## Critérios bloqueantes (gate de "completo curso")

Ver [`RUBRIC.md`](./RUBRIC.md). Resumo:

- [ ] **Sandbox verde** (herdado de P2, ainda gate).
- [ ] **Golden de 50 entradas** que VOCÊ definiu, com gabarito + comentário.
- [ ] **≥18/20 payloads do FEC-GS-INJECTION-v1 bloqueados**.
- [ ] Dashboard local (HTML estático) com pelo menos: pass rate por step, tool call latency, distribuição de custo.
- [ ] **p95 latência ≤ FEC-BUDGET-LAT-v1** (definido em budgets.json).
- [ ] Documentação de operação: como roda em prod, como monitora, como rollback.

## Conhecimento aplicado

- TUDO. Este é o "pipeline em produção" — integra T1 (custo, atenção), T2 (versionamento), T3 ou T4 (RAG ou agente), T6 (eval, observabilidade, segurança).

## Defesa contra injection (PLAN item 62, SAFETY-INJECTION.md)

- Input guard (sanitização do user prompt).
- Output guard (filtro de saída antes de retornar ao usuário ou tool).
- Allow-list de tools por contexto (separar "tools de leitura" de "tools de escrita").
- Spotlight (Anthropic 2024): delimitar conteúdo recuperado de instrução.

## Submissão

Branch `projetos/p5-<seu-handle>`. PR com label `projeto:P5`.

## Certificação INEMA

P5 aprovado + quiz final do curso ≥80% = elegível para certificado FEC v1.0 (página HTML personalizada). Sem promessa exagerada — não vale dinheiro, vale demonstração de capacidade.
