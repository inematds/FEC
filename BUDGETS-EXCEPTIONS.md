# BUDGETS-EXCEPTIONS — Exceções de orçamento

> _Quando algum asset/CI excede budget de `BUDGETS.md` ou `check-budgets.py`, registra-se aqui com prazo de redução. Sem exceção em branco. PLAN item 93._

## Política

- Exceção exige PR aprovado por 2 maintainers.
- Cada exceção tem **prazo de redução** declarado.
- Auditoria semestral remove exceções expiradas (status: resolvido OU promovido a budget oficial).

## Exceções ativas

_(Vazio. Primeira exceção esperada quando T4.3/P3 (multi-agente) introduzir traços maiores.)_

## Template de entrada

```markdown
### EXC-NNNN — <breve>

- **Tipo:** zip / SVG / mermaid / repo / ci-fast / ci-scheduled / actions-minutes
- **Item afetado:** <caminho ou métrica>
- **Excede em:** <quanto>
- **Justificativa:** <razão pedagógica/operacional>
- **Prazo de redução:** YYYY-MM-DD
- **Plano:** <como pretendemos voltar para budget>
- **Aprovado em:** YYYY-MM-DD por @maintainer1, @maintainer2
- **Issue de tracking:** [#NNN]
```

## Auditoria semestral

| Data | Exceções abertas | Resolvidas no semestre | Promovidas a budget |
|------|-----------------|------------------------|---------------------|
| 2026-Q4 | 0 | — | — |
