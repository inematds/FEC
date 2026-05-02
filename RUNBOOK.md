# RUNBOOK — Operações da FEC

> _Para incidentes graves de release, ver também [`RELEASE-INCIDENT.md`](./RELEASE-INCIDENT.md)._
> _Mapa métrica → severidade → owner → ação: [`ALERTS.md`](./ALERTS.md) (gerado de `evals/v1/alerts.json`)._

## Severidades e SLA

| Severidade | Definição | SLA |
|------------|-----------|-----|
| **SEV-1** | Secret vazado, malware no zip, prompt injection com exfil real demonstrada, XSS na página publicada, sandbox quebrado em produção. | **Janela 24/7 nos 14 dias pós-release** (rc + GA + 7d): ≤2h com primário+secundário em rotação 12h. Fora da janela: mitigação automática ≤2h (revogação, banner, takedown) + resposta humana ≤8h em horário comercial BR / ≤4h fim-de-semana melhor-esforço. |
| **SEV-2** | Módulo GA com erro técnico que invalida exercício; benchmark errado; quebra de licença; provider deprecation que invalida lab; auto-smoke 2 dias seguidos red. | ≤24h em horário comercial BR. |
| **SEV-3** | Errata de conteúdo, link quebrado, falha de a11y individual. | ≤7 dias úteis. |

## On-call

- Rotação semanal documentada em [`ROTATION.md`](./ROTATION.md).
- Janela pós-release tem **primário + secundário** explícitos.
- Maintainer pode declinar com ≥48h de antecedência.
- Handoff escrito entre rotações em [`HANDOFF.md`](./HANDOFF.md).
- Canal acordado: **Discord do INEMA** (configurar webhook do GitHub Actions para o canal `#fec-oncall`).

## Permissões pré-autorizadas (break-glass)

Owner secundário tem autorização prévia para:

1. Editar GitHub Release notes (incluir aviso de deprecação).
2. Trocar `index.html` para banner via `assets/banners/deprecation.html`.
3. Yank no PyPI (`pypi-yank fec-sdk==X.Y.Z`).
4. Rotação de secrets (`FEC_SMOKE_LOWPRIV_*`).

Ver detalhes e auditoria em [`BREAK-GLASS.md`](./BREAK-GLASS.md).

## Playbooks por classe de falha

Seguir o runbook correspondente:

| Sintoma | Runbook |
|---------|---------|
| auto-smoke red 2+ dias | [`runbooks/smoke-failure.md`](./runbooks/smoke-failure.md) |
| Secret vazado / gitleaks bloqueando | [`runbooks/secret-exposure.md`](./runbooks/secret-exposure.md) |
| Release ruim publicado | [`runbooks/bad-release.md`](./runbooks/bad-release.md) |
| Provider deprecou modelo pinado | [`runbooks/provider-deprecation.md`](./runbooks/provider-deprecation.md) |
| CVE em dependência | [`runbooks/dependency-cve.md`](./runbooks/dependency-cve.md) |
| Dataset com problema de licença | [`runbooks/dataset-license-violation.md`](./runbooks/dataset-license-violation.md) |
| `fec_sdk` precisa ser yanked do PyPI | [`runbooks/sdk-yank.md`](./runbooks/sdk-yank.md) |
| GitHub Pages servindo conteúdo errado | [`runbooks/pages-down.md`](./runbooks/pages-down.md) |
| `pip install fec-sdk` falhando | [`runbooks/pypi-down.md`](./runbooks/pypi-down.md) |
| Zenodo mirror offline | [`runbooks/zenodo-down.md`](./runbooks/zenodo-down.md) |

## Observabilidade

- **Dashboard público:** `docs/dashboard.html` (gh-pages, gerado por `scripts/dashboard.py` diariamente).
- **Synthetic monitor:** `scripts/synthetic-check.py` (hourly, item 89a). Status em `docs/status.html`.
- **Métricas declaradas em [`MEDIDAS.md`](./MEDIDAS.md):** saúde CI (auto-smoke 7d/30d), saúde conteúdo (errata aberta/fechada), saúde uso (opt-in via formulário), custo acumulado vs orçamento.
- **Métricas vetadas como sinal de saúde:** stars, downloads (servem só como contexto).

## Postmortem

Todo incidente SEV-1 ou SEV-2 exige postmortem público em `postmortems/<data>-<slug>.md` dentro de **7 dias úteis**. Template:

```markdown
# Postmortem — <título>

**Data:** YYYY-MM-DD
**Severidade:** SEV-X
**Duração:** Xh
**Owner:** @maintainer

## Resumo (TL;DR)
1-2 frases.

## Timeline (UTC)
- HH:MM Detectado por <fonte>
- HH:MM Mitigação aplicada
- HH:MM Resolvido

## Causa raiz
Análise de 5 porquês.

## Impacto
Quem foi afetado, como.

## Mitigação
O que foi feito agora.

## Prevenção
Mudanças para não acontecer de novo (com PRs/issues vinculados).

## Lições
O que aprendemos sobre o sistema.
```

## Drill semestral

Simular SEV-2 em fork do repo + cenário de yank de SDK em TestPyPI. Cronometrar resposta. Resultado em `MEDIDAS.md`.
