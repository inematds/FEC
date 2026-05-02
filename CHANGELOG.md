# Changelog — FEC

> _Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) + [SemVer](https://semver.org/lang/pt-BR/)._

## [Não publicado]

### Added
- Plano completo (`PLAN.md`) com 95 itens, 17 seções, endurecido por 5 rodadas adversariais (senior-eng, security/data-integrity, ops/SRE × 2 deepenings).
- Relatório do loop de planejamento (`RELATORIO-CLAUDEX.md`).
- Scaffolding inicial do repo:
  - Estrutura de diretórios completa (curso/, fec_sdk/, evals/v1/, schemas/, scripts/, runbooks/, etc.).
  - 8 schemas JSON canônicos (`schemas/*.schema.json`) — source of truth para automação.
  - 8 manifestos canônicos (`evals/v1/*.json`).
  - 4 workflows GitHub Actions (`ci-fast`, `ci-scheduled`, `ci-extended-compat`, `release`, `auto-smoke-watchdog`).
  - Documentação foundational: README, ESCOPO, PRE-REQUISITOS, SECURITY, RUNBOOK.
  - Licenças dual: CC BY-SA 4.0 (conteúdo) + MIT (código).
  - Landing page em formato INEMA (`index.html`) com mapa visual das 6 trilhas.
  - CSP policy pinada (`assets/csp/policy.txt`).
  - CODEOWNERS com proteção em workflows, evals/, manifestos JSON.

### Added (Chunk 2 + 3)
- **`fec_sdk/`** completo:
  - `__init__.py` + `errors.py` + `messages.py` (provider-neutral types)
  - `check_compat.py` com manifesto remoto assinado + cache + hard-fail
  - `sandbox/{filesystem.py,network.py}` jailed
  - `adapters/{base,mock,anthropic_adapter,openai_adapter,ollama_adapter}.py`
  - `data/revoked_versions.json` baseline embutido
  - `selftest()` ok
- **`tests/sandbox/test_traversal.py`** — bateria de **19 testes verdes** (gate de GA).
- **Scripts críticos:**
  - `validate-schemas.py` — valida 8 manifestos + quizzes
  - `validate.py` — INEMA structure check
  - `lint-content.py` — XSS hard checks (block) + word count/refs (strict)
  - `freeze-evals.py` — HASHES.lock content-addressed
  - `render-docs.py` — gera 6 MDs canônicos a partir de JSONs
  - `check-budgets.py` — orçamentos de assets/CI
  - `build-quiz.py` — quiz JSON → HTML escapado
  - `render-diagrams.sh` — Mermaid → SVG dual (dark + light)
- **Piloto T1.1 completo:**
  - `curso/trilha1/{index.html, modulo-1-1.html, modulo-1-2.html}` (passa em 8/8 regras INEMA)
  - 2 diagramas Mermaid em `assets/diagrams/src/`
  - `exercicios/modulo-1-1/{enunciado.md, starter/, test.py}` com 5 casos
  - `solucoes/modulo-1-1/solucao.py` (passa 5/5)
  - `quizzes/modulo-1-1.json` (5 perguntas) + snippet HTML
  - `exemplos/modulo-1-1/neutro.py` (provider-neutral)
  - `bibliografia/T1.md` (10 papers + 3 posts datados)
- **Esqueletos das trilhas T2-T6** (`index.html` com cards de módulos).
- **Pipeline Python/Node:** `pyproject.toml`, `package.json`, `tailwind.config.js`, `assets/css/inema.src.css` (com light mode override).
- **10 runbooks** em `runbooks/` cobrindo todas as classes de falha.
- **Documentação operacional:** `RELEASE-INCIDENT.md`, `ROTATION.md`, `HANDOFF.md`, `BREAK-GLASS.md`, `HOSTING-DECISION.md`, `OLLAMA-MATRIZ.md`, `MEDIDAS.md`, `REVISORES.md`, `REVIEW-RUBRIC.md`, `LICENSES-THIRD-PARTY.md`, `SBOM.md`, `SECURITY-SANDBOX.md`, `SAFETY-INJECTION.md`, `BUDGETS-EXCEPTIONS.md`, `COMPAT-RETIRED.md`.
- **6 MDs gerados** a partir de JSON: `COMPAT.md`, `MODELOS.md`, `CAPACIDADES.md`, `ALERTS.md`, `RISK-ACCEPTANCE.md`, `CHECKSUMS-REVOCATION.md`.
- **3 projetos GA com rubrics:** `projetos/{P1,P2,P5}/{README,RUBRIC}.md`.
- **Glossário inicial** com 30+ termos derivados dos módulos.
- **Postmortems template** em `postmortems/README.md`.
- **Lockfile inicial** em `releases/v1.0.0/lockfile.toml` (hashes pendentes — preenchidos pelo `release.yml`).
- **Banner de deprecação** em `assets/banners/deprecation.html` para uso em incidentes.
- **Dataset golden inicial** `evals/v1/datasets/FEC-GS-RAG-v1.json` (3/30 — restantes na fase de conteúdo).
- **Judge spec** `evals/v1/judges/groundedness.md`.

### CI passa (verificado localmente)
- `validate-schemas.py` ✅ 9 ok
- `validate.py` ✅ 2/2 módulos ok
- `lint-content.py --mode=block` ✅ 11 HTMLs limpos
- `freeze-evals.py --verify` ✅ 12 entries match
- `check-budgets.py` ✅ ok
- `render-docs.py --check` ✅ todos sincronizados
- `pytest tests/sandbox/` ✅ **19/19 verdes**
- `fec_sdk.selftest()` ✅ `{'sandbox': 'ok', 'import': 'ok'}`

### Próximos passos
- Conteúdo dos módulos T2-T6 (12 HTMLs faltam).
- Datasets `FEC-GS-AGENT-v1` (30) e `FEC-GS-INJECTION-v1` (20) preenchidos.
- Judge specs adicionais (`agent-correctness`, `injection-defense`).
- Adapters Anthropic/OpenAI/OSS testados com smoke real (após primeiras chaves).
- `tests/contracts/` (mocked provider contracts).
- `tests/visual/` (Playwright + axe).
- Convite a revisores externos.
- Primeira RC `v1.0.0-rc.1`.

---

## v1.0.0 — maio/2026 (alvo)

Primeiro release público. Conteúdo a ser preenchido conforme execução do plano.
