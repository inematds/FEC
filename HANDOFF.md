# HANDOFF — Passagem de plantão

> _Atualize ao fim de cada semana de rotação. PLAN item 90._

## Template

Copie e preencha:

```markdown
## Plantão: <YYYY-W##>

**De:** @<maintainer-saindo>
**Para:** @<maintainer-entrando>
**Período:** <data início> a <data fim>

### Incidentes durante o plantão
- [SEV-X] <breve> — resolvido / em aberto (link issue) / em postmortem

### Issues em aberto que precisam atenção
- [#123] <título> — severidade, status, próxima ação esperada
- ...

### Mudanças em flags / kill-switches
- `SMOKE-KILLSWITCH.json` — sem mudança / ligado em <data> por <motivo>, expected_off_until=<data>
- `BUDGETS-EXCEPTIONS.md` — sem nova exceção / nova exceção <id>

### Saúde do sistema (snapshot)
- auto-smoke (7d): <X> pass / <Y> fail
- Custo acumulado mês: $<valor> (vs target $60)
- Issues SEV-1 abertas: <N> (deveria ser 0)
- Issues SEV-2 abertas: <N>
- Synthetic monitor: <todos verdes / canais com problema>

### Tarefas planejadas para a próxima semana
- ...

### Notas / contexto não-óbvio
- ...
```

---

## Plantões anteriores

_(arquivo cresce abaixo conforme o curso for sendo desenvolvido e mantido)_

### Plantão: 2026-W18

**De:** N/A (primeiro plantão)
**Para:** _TBD_
**Período:** 2026-04-27 a 2026-05-03

#### Notas

Scaffolding inicial do repo concluído seguindo PLAN.md. Próximas semanas: build pipeline e piloto T1.1 (já parcialmente implementado).
