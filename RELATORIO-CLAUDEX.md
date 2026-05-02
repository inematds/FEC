# Relatório do Loop Claudex — Plano FEC

**Review ID:** `20260502-051307-beec7a`
**Data:** 2026-05-02
**Tempo total:** 28m 57s
**Modo:** plan (5 rounds adversariais)
**Tópico:** Curso master avançado de Engenharia de Contexto (Formação de Engenharia de Contexto - FEC), 12-16 módulos, formato INEMA.CLUB, publicação maio/2026 em github.com/inematds/FEC

---

## Configuração da execução

- **Escopo escolhido na entrevista:** Curso master (12-16 módulos) com projetos práticos.
- **Restrições:** PT-BR, agnóstico de provedor (Claude, GPT, Gemini, open-source).
- **Prioridades:** máximo de ilustrações, conteúdo profundo (papers/benchmarks), exercícios práticos cumulativos.

---

## Findings por round (todas aceitas)

| Round | Persona | High | Medium | Low |
|-------|---------|-----:|-------:|----:|
| 1 | Senior-engineer review | 6 | 10 | 4 |
| 2 | Security & data-integrity | 2 | 3 | 1 |
| 3 | Ops & SRE | 1 | 4 | 1 |
| 4 | Ops & SRE (deepening) | 2 | 6 | 1 |
| 5 | Ops & SRE (deepening) | 3 | 2 | 1 |
| **Total** | — | **14** | **25** | **8** |

**Total: 47 findings — todas aceitas, zero rejeitadas.**

---

## Round 1 — Senior-engineer review

### High
- Escopo + cronograma não fecham para maio/2026 com 14 módulos, 70-90 páginas, 5 projetos, CI, a11y, review externo.
- Métricas duras com placeholders (`groundedness ≥0.85`, `cost <X`, `p95 <X`).
- "Provider-agnostic" conflita com capacidades específicas (caching, MCP, structured outputs).
- "Paper para cada padrão" sem harness reproduzível convida cherry-pick.
- Carga por módulo inconsistente (4-7k palavras + 3 dialetos + diagramas + quiz + projeto não cabem em 45-75 min).
- Review externo é gate, mas sem staffing/protocolo.

### Medium
- Contrato INEMA ambíguo (tópicos expansíveis em módulos vs índices).
- Caminho Ollama "free" ignora gaps de hardware/capacidade.
- Tailwind CDN + Mermaid runtime + iframes geram risco de durabilidade/CSP/offline.
- Mermaid dark/light hand-waved.
- CI <2min não é credível com link check + Mermaid + axe + spellcheck + content lint.
- Smoke real mensal pode vazar secrets, queimar budget, falhar não-deterministicamente.
- Licença não cobre terceiros (datasets, screenshots, ArXiv abstracts).
- Spec de prompt injection vago.
- Soluções em branch separado vs path `/solucoes/`.
- Eval/observabilidade empurrados para T6 mesmo quando P1-P4 precisam antes.

### Low
- "70-90 páginas" não bate com layout.
- Glossário 80-120 termos pode descolar do conteúdo.
- README 200 linhas é arbitrário.
- "Papers congelados" envelhece em campo que muda rápido.

---

## Round 2 — Security & data-integrity review

### High
- P2/P5 sem sandbox de filesystem/path allowlist — agentes podem ler `.env`, `~/.aws/credentials`, etc.
- Smoke com secrets pode executar scripts repo-controlados; merge malicioso vaza keys ou queima budget.

### Medium
- Pipeline estático sem sanitização — Markdown/quiz/SVG/HTML viram stored XSS.
- Harness "frozen" sem imutabilidade verificável — datasets/judges/budgets podem mudar sem version bump.
- Release/mirror não atômico — retry após crash pode deixar tag, GitHub assets e Zenodo apontando para zips diferentes.

### Low
- Issues automáticas duplicam sob runs sobrepostos / kill-switch inconsistente.

---

## Round 3 — Ops & SRE review

### High
- Sem caminho de rollback após `v1.0.0` ruim publicado e mirrored — usuários continuam baixando zip comprometido.

### Medium
- Smoke com required-reviewers vira gargalo OU rubber-stamp.
- Sem RC/canais staged — anúncio amplo expõe todos os usuários a defeito de release.
- Compatibilidade entre static pages, `fec_sdk`, exemplos, harness, adapters não governada.
- Observabilidade pós-launch é vaidosa (stars) + triagem semanal — incidentes severos passam batido.

### Low
- "Máximo de ilustrações" sem orçamento de capacidade — repo/CI/Playwright crescem até quebrar.

---

## Round 4 — Ops & SRE deepening

### High
- RC promotion gate falsamente satisfeito quando kill-switch desliga `auto-smoke` (exit 0 ≠ pass real).
- `fec_sdk` no PyPI sem caminho de yank/advisory/denylist — versão vulnerável continua instalável.

### Medium
- "Same bits" rc→stable não cobre source archives, Pages output, PyPI packages.
- Version skew só warning permite alunos rodarem combos não-suportados produzindo benchmarks inválidos.
- SEV-1 ≤2h vs "fora do horário = best-effort" é inconsistente — sexta à noite não cumpre target.
- Sem synthetic monitoring de canais públicos — Pages/Release/Zenodo/PyPI podem quebrar com CI verde.
- `FEC-CI-BUDGET: $5/mês` vs `FEC_SMOKE_LOWPRIV: $1/dia` são incoerentes.
- RC gate aceitando até 3 high-severity normaliza shipping com defeitos sérios.

### Low
- Matriz de compat sem cardinalidade limitada — combinations explodem ao longo do tempo.

---

## Round 5 — Ops & SRE deepening (final)

### High
- PyPI não satisfaz "same bits" porque `1.0.0rcN` ≠ `1.0.0` e PyPI não permite overwrite.
- `RevokedVersionError` em wheel imutável não atualiza após instalação.
- GitHub Pages não tratado como canal versionado/imutável — rebuilds diários driftam o site.

### Medium
- `audit-pages.py` espera CSP em header, mas GitHub Pages usa `<meta>` (header não suportado).
- Item 48 diz kill-switch automatizado em 100% budget; item 71a diz que só humanos via PR podem mudar o flag protegido — contradição.

### Low
- `COMPAT.md`, `BUDGETS.md`, `CHECKSUMS-REVOCATION.md` em Markdown forçam parsing frágil em automação crítica.

---

## Estado final do plano

- **62 → 95 itens** numerados.
- **6 → 17 seções**, com Seção 17 (Operações) construída inteiramente a partir das findings: canais rc/stable, runbook de incidente, compat matrix com cap, observabilidade declarada, orçamentos de capacidade, manifestos JSON canônicos.
- Plano executável com gates objetivos, runbooks por classe de falha, manifestos canônicos auditáveis, SLAs honestos e caminho de rollback completo (Pages, PyPI, Zenodo, secrets).

### Documentos canônicos definidos (machine-readable)

`schemas/*.schema.json` validam: `compat.json`, `revoked_versions.json`, `budgets.json`, `models.json`, `capabilities.json`, `risk-acceptance.json`, `checksums-revocation.json`, `alerts.json`. Markdown é gerado pelos JSONs (não editado à mão).

### Runbooks por classe de falha

`runbooks/` cobre: smoke-failure, secret-exposure, bad-release, provider-deprecation, dependency-cve, dataset-license-violation, sdk-yank, pages-down, pypi-down, zenodo-down.

### Scripts de automação previstos

`scripts/`: validate, lint-content, build-quiz, render-diagrams, build-glossary, smoke-providers, freeze-evals, audit-evals, sanitize-svg, redact, check-budgets, build-compat, dashboard, check-killswitch-age, check-rc-gates, audit-pages, synthetic-check, validate-schemas, render-docs, rollback-pages, sign-manifest.

---

## Avaliação honesta

O loop atingiu o teto de 5 rounds com findings materiais ainda surgindo no round 5 — o que é normal para um plano dessa amplitude. Cada round trouxe sinal genuíno, especialmente nos rounds 4 e 5 (deepening de Ops/SRE expôs detalhes que só apareceriam depois do incidente real).

O plano atual está num estado **executável e auditável**, com:
- escopo MVP recortado (10 módulos GA + 4 beta);
- harness de avaliação congelado e content-addressed;
- sandbox de tools com bateria de testes obrigatória;
- secrets/CI/release com defesa em profundidade;
- rollback documentado para todos os canais (GitHub Release, Pages versionada, PyPI, Zenodo);
- SLAs honestos com janela 24/7 estendida pós-release.

Mais um ou dois rounds provavelmente trariam refinamentos (não fundações). Recomendação: **partir para execução** começando pelo scaffolding + piloto T1.1, que calibra os orçamentos numéricos antes do resto fechar.

---

## Artefatos

- **Plano:** `/home/nmaldaner/projetos/FEC/PLAN.md` (95 itens + Changelog completo de 5 rounds).
- **Findings dos 5 rounds:** `.claude/claudex/20260502-051307-beec7a/findings-round-{1,2,3,4,5}.md`.
- **Transcripts completos do Codex:** `.claude/claudex/20260502-051307-beec7a/round-{1..5}.log` (preservados).
