# Postmortems — incidentes públicos da FEC

> _Todo SEV-1 ou SEV-2 gera postmortem público dentro de 7 dias úteis. PLAN item 78.7._

## Template

Salve como `postmortems/<YYYY-MM-DD>-<slug>.md`:

```markdown
# Postmortem — <título>

**Data:** YYYY-MM-DD
**Severidade:** SEV-X
**Duração total:** Xh
**Autor:** @<maintainer>
**Status:** ⏳ em redação · 🔍 em revisão · ✅ publicado

## Resumo (TL;DR)

1-2 frases. O que aconteceu, qual o impacto, o que mudou para prevenir.

## Timeline (UTC)

- HH:MM — Detectado por <fonte> (synthetic monitor / aluno / Dependabot / ...)
- HH:MM — Triagem inicial; severidade classificada
- HH:MM — Mitigação primeira aplicada (ex.: banner, key revogada)
- HH:MM — Sucessor publicado (ex.: v1.0.1)
- HH:MM — Resolvido / status público atualizado

## Causa raiz

5 porquês.

1. Por que aconteceu? — ...
2. Por que isso? — ...
3. Por que isso? — ...
4. Por que isso? — ...
5. Por que isso? — _causa raiz_

## Impacto

- Quem foi afetado: <N> usuários / <segmento>.
- Como: <ex.: instalou versão vulnerável, lab parou de funcionar, etc.>.
- Custo: <$ se aplicável (budget / dano reputacional / horas de trabalho)>.

## O que funcionou

- ...
- ...

## O que NÃO funcionou

- ...
- ...

## Mitigação aplicada

- [link PR] — descrição.
- ...

## Prevenção (action items)

| # | Ação | Owner | Issue/PR | Prazo |
|---|------|-------|----------|-------|
| 1 | <ação> | @maintainer | [#123] | YYYY-MM-DD |
| 2 | ... | | | |

## Lições aprendidas

O que aprendemos sobre o sistema, processo, ou time.

## Apêndice: dados / logs

(Logs redatados; charts; queries do dashboard.)
```

## Postmortems anteriores

_(Vazio até o primeiro incidente.)_
