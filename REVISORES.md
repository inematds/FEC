# REVISORES — Peer review externo

> _Lista de revisores assinados por trilha. PLAN itens 50-51._

## Política

- **2 revisores por trilha** (≥1 sênior na área específica).
- **Perfil mínimo:** experiência em produção com LLM ≥1 ano OU autoria de paper/post relevante.
- **Rubrica:** [`REVIEW-RUBRIC.md`](./REVIEW-RUBRIC.md).
- **SLA:** 7 dias úteis após receber bundle PDF + repo tag.
- **Freeze date:** 14 dias antes do release; após freeze, só hot-fixes.
- **Compensação:** menção neste arquivo + voucher do INEMA.
- **Fallback:** trilha sem assinatura suficiente sai como `beta` em vez de `GA`.

## Convites enviados (status)

| Trilha | Revisor 1 | Status | Revisor 2 | Status |
|--------|-----------|--------|-----------|--------|
| T1 — Fundamentos | _convite a enviar_ | — | _convite a enviar_ | — |
| T2 — Mensagem | _convite a enviar_ | — | _convite a enviar_ | — |
| T3 — RAG | _convite a enviar_ | — | _convite a enviar_ | — |
| T4 — Tools/Agentes | _convite a enviar_ | — | _convite a enviar_ | — |
| T5 — Memória | _convite a enviar_ | — | _convite a enviar_ | — |
| T6 — Avaliação | _convite a enviar_ | — | _convite a enviar_ | — |

> _Status pode ser: convidado / aceitou / em revisão / aprovou / declinou._

## Assinaturas (após aprovação)

Quando o revisor aprovar a trilha, adicionar:

```markdown
### T1 — Fundamentos

- ✅ <Nome>, <afiliação>, revisado em YYYY-MM-DD. Rubrica preenchida em `reviews/T1-revisor1.md`.
- ✅ <Nome>, <afiliação>, revisado em YYYY-MM-DD. Rubrica preenchida em `reviews/T1-revisor2.md`.
```

(Vazio até primeiros aprovações.)

## Conflito de interesse

- Revisor declara COI ANTES de revisar.
- Revisor não pode ser autor da trilha.
- Revisor não pode ter relação financeira ativa com o INEMA.
- Em conflito não resolvido: maintainers + 1 revisor adicional decidem.
