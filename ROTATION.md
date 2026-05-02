# ROTATION — On-call rotativo

> _Atualize quando trocar maintainers; nas duas semanas pós-release, exibir primário+secundário._

## Política (PLAN itens 77, 90)

- **Rotação semanal** entre maintainers. Cada um cobre 1 semana de plantão.
- **Janela 24/7 estendida nos 14 dias pós-release** (rc + GA + 7d): primário **e** secundário em rotação 12h.
- **Decline** com ≥48h de antecedência — outro maintainer assume.
- **"Horário comercial BR"** = 09-19 BRT em dias úteis. SEV-1 fora disso é melhor-esforço (≤8h horário comercial; ≤4h fim-de-semana melhor-esforço).
- Drill de incidente semestral.

## Rotação atual

| Semana (ISO) | Primário | Secundário (apenas em janela pós-release) | Notas |
|--------------|----------|-------------------------------------------|-------|
| 2026-W18 | _TBD_ | _TBD_ | Pré-RC scaffolding |
| 2026-W19 | _TBD_ | _TBD_ | Build T1-T2 |
| ... | | | |

**Janela 24/7 estendida (pós-release v1.0.0):**

| Data | Primário | Secundário | Permissões break-glass |
|------|----------|------------|------------------------|
| 2026-MM-DD a +14d | _TBD_ | _TBD_ | Sim (ver `BREAK-GLASS.md`) |

## Como assumir um plantão

1. Leia o último `HANDOFF.md`.
2. Verifique `docs/status.html` — algum incidente em aberto?
3. Notifique-se em `#fec-oncall` (Discord do INEMA).
4. Mantenha o telefone/notificação ativos durante a janela.

## Como passar o plantão

Preencha `HANDOFF.md` no fim da sua semana com:
- Issues em aberto (severidade + status).
- Mudanças em `SMOKE-KILLSWITCH.json` ou flags durante seu plantão.
- Pulse do `auto-smoke` (rate de pass/fail).
- Alertas que dispararam e como você resolveu.
