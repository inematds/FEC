# PLAN.md — Formação de Engenharia de Contexto (FEC)

**Repo alvo:** github.com/inematds/FEC
**Release alvo:** v1.0.0 — maio/2026 (MVP definido), com tracks pós-lançamento explicitamente rotuladas
**Formato:** INEMA.CLUB (HTML estáticas, Tailwind, dark/light), seguindo `references/MASTER_COMPLETO.md`
**Idioma:** PT-BR
**Estilo:** padrões **provider-neutral primeiro**, exemplos canônicos em Python; adaptadores Anthropic/OpenAI/OSS apenas onde a capacidade é específica
**Volume v1.0:** 6 trilhas, **10 módulos GA** + **4 módulos rotulados "beta/pós-lançamento"** + **3 projetos GA** (P1, P2, P5) + 2 projetos opcionais

---

## 1. Definição do produto e diferencial editorial

1. **Tese editorial (uma frase, fixada no README):** "Engenharia de Contexto é a disciplina de projetar, montar, comprimir, persistir e avaliar a janela de contexto que um modelo recebe — não 'prompt engineering' enfeitado." Guia recortes e diferencia a FEC de cursos genéricos.
2. **Pré-requisitos explícitos** (`PRE-REQUISITOS.md`): API LLM via HTTP/SDK, Python intermediário, JSON Schema, conta em ≥1 provedor. Quem não tiver é redirecionado para curso introdutório (link).
3. **Persona-alvo:** engenheiro de software / ML que vai colocar agente em produção. Marcado por nível ("builder solo / eng. de produto / eng. de plataforma") em cada módulo.
4. **Resultados de aprendizagem por trilha** são medíveis e ancorados no **harness de avaliação congelado** (item 30): ex. "T3 — agente RAG ≥0.85 em groundedness no golden set FEC-GS-RAG-v1, custo ≤ orçamento FEC-BUDGET-RAG-v1." Sem placeholder; sem golden definido, a trilha não fecha.
5. **Política anti-hype (`ESCOPO.md`):** o que está fora — fine-tuning extensivo (cobrimos só quando substitui contexto), filosofia de IA, "gurus" sem evidência. Permite o aluno saber o que NÃO terá.
6. **Status declarado por módulo e projeto:** cada página tem badge `GA` ou `beta`. `beta` significa rascunho público com aviso. Status visível no índice e no front-matter HTML.

## 2. Arquitetura do currículo (6 trilhas; 10 módulos GA + 4 beta)

7. **T1 — Fundamentos de Contexto (emerald, 2 GA):** 1.1 janela, atenção, "lost in the middle"; 1.2 tokens, custo, limites práticos por modelo (tabela viva em `MODELOS.md`).
8. **T2 — Engenharia da Mensagem (blue, 2 GA):** 2.1 estrutura (system, few-shot, XML/JSON, ordem, ancoragem); 2.2 templates, versionamento de prompt, **eval primer** (definir que toda mudança de prompt entra com mini-eval — semente da disciplina).
9. **T3 — RAG e Recuperação (purple, 2 GA + 1 beta):** 3.1 indexação (chunking, embeddings, BM25/híbrido); 3.2 reranking, *contextual retrieval*, citações; **3.3 (beta) RAG agêntico/self-RAG** — beta para reduzir escopo e estabilizar GA.
10. **T4 — Tools, Agentes e Multi-Agente (amber, 2 GA + 1 beta):** 4.1 tool/function calling provider-neutral + adaptadores; 4.2 agentes single (ReAct, planner/executor); **4.3 (beta) multi-agente e MCP** — beta porque MCP e padrões multi-agente ainda mudam rápido.
11. **T5 — Memória, Compressão e Persistência (teal, 1 GA + 1 beta):** 5.1 memória curto/longo prazo, summarização hierárquica, compressão; **5.2 (beta) prompt caching e context distillation** — beta porque caching é fortemente provider-specific (item 14).
12. **T6 — Avaliação, Observabilidade e Produção (rose, 1 GA + 1 beta):** 6.1 evals (golden, LLM-as-judge e vieses), tracing, prompt injection, custo; **6.2 (beta) operacionalização avançada** (A/B em produção, canários).
13. **Mapa de dependências** (Mermaid em `index.html`): linhas sólidas para módulos GA, tracejadas para beta. Aluno vê o caminho mínimo para o "certificado v1.0".

## 3. Padrões provider-neutral vs. específicos (regra firme)

14. **Hierarquia de ensino** em todo módulo que toca capacidade não-portável:
    1. **Padrão neutro primeiro** (ex.: "monte mensagens com seções estáveis no início para maximizar reuso de cache de qualquer provedor").
    2. **Realização concreta em provedor canônico** do módulo (ex.: Anthropic prompt caching) com benchmark.
    3. **Equivalentes em outros provedores** (com badge "parcialmente equivalente" / "não disponível, usar adaptador X / mockar").
    4. **Tabela `CAPACIDADES.md`** consolidada: capacidade × provedor × status (nativo / adaptador / não suportado / mock).
15. **Exemplos de código:** **Python provider-neutral é canônico** (`fec_sdk/` mínimo: cliente abstrato, mensagens, tools, retries). Cada módulo tem adaptadores `anthropic.py`, `openai.py`, `oss.py` apenas para o que NÃO cabe na abstração. Reduz manutenção drasticamente vs. "três dialetos paralelos".
16. **Capacidades não-portáveis com plano de aterrissagem:** prompt caching, structured outputs nativos, long context (>200k), tool calling com modos avançados, MCP. Cada uma tem (a) por que a abstração não cobre, (b) fallback simulado, (c) exemplo provider-específico, (d) custo de portar.

## 4. Estrutura de cada módulo (contrato fixo, anti-inconsistência)

17. **Tamanho realista por módulo:** alvo **2.500-4.500 palavras** (revisado para baixo) → leitura ~25-45 min + lab 30-60 min = **60-105 min totais**, declarado no front-matter. Acima do teto vira 2 módulos. Estimativa calibrada por módulo-piloto T1.1 antes de produzir o resto.
18. **Toda página de módulo tem 7 seções obrigatórias** (alinhadas a `references/MASTER_COMPLETO.md`):
    1. abertura com objetivo de aprendizagem mensurável (ligado a item do harness, item 30);
    2. **conteúdo principal em seções ricas** (não todo conteúdo dentro de "tópicos expansíveis" — tópicos expansíveis são para sub-blocos, conforme MASTER);
    3. ≥6 sub-tópicos expansíveis com as 3 subsessões INEMA ("O que é" / "Por que aprender" / "Conceitos-chave");
    4. ≥3 ilustrações de tipos diferentes (item 25);
    5. exemplo de código mínimo executável (provider-neutral; adaptadores linkados);
    6. exercício hands-on com teste automatizado (item 38);
    7. bibliografia datada com ≥3 referências.
19. **Eval-thinking desde o início:** T1.1 introduz "toda mudança em contexto exige eval mínimo"; T2.2 ensina o template; T3-T5 aplicam; T6.1 aprofunda. Não empurrar para o fim.
20. **"Quando NÃO usar"** obrigatório em todo padrão técnico — RAG, agente, multi-agente, memória, caching. Falta = entrega bloqueada.

## 5. Projetos cumulativos (3 GA + 2 opcionais)

21. **P1 GA — "Buscador citável"** (após T2-T3.2): RAG sobre dataset público fixado (`fixtures/arxiv-cs-100/`), responde com citações; eval no golden `FEC-GS-RAG-v1` (item 31). Critério: groundedness ≥0.85.
22. **P2 GA — "Agente com tools"** (após T4.1-T4.2): combina busca local + cálculo + leitura de arquivo, com tracing (item 35). Critério: passa em 30/30 traços-canário; sem loops infinitos; **bateria sandbox (item 62a) verde**.
23. **P5 GA — "Pipeline em produção"** (após T6.1): pega P2, adiciona evals offline, golden de 50 entradas, tracing dashboard, defesa contra prompt injection (item 47). Entrega final do curso. **Gate de sandbox + golden de injection (`FEC-GS-INJECTION-v1`) ≥18/20 bloqueados** antes de virar GA.
24. **P3/P4 OPCIONAIS** (rotulados "post-launch", ficam em `projetos/post-launch/`): "Sistema multi-agente" e "Memória que escala". Não bloqueiam v1.0.
25. **Rubric objetivo por projeto** (`projetos/<id>/RUBRIC.md`): critérios passam/falham (ex.: "≥1 teste de injection passa", "p95 latência ≤ orçamento FEC-BUDGET-LAT-v1", "groundedness ≥0.85"). Sem rubric, projeto não é "completo".

## 6. Harness de avaliação congelado (FEC-EVAL-v1)

26. **Conjunto fixado por release** sob `evals/v1/`, versionado no Git e publicado na Release zip. Contém:
    - **Datasets golden:** `FEC-GS-RAG-v1` (50 perguntas + docs em `fixtures/arxiv-cs-100/`), `FEC-GS-AGENT-v1` (30 traços-canário), `FEC-GS-INJECTION-v1` (20 payloads sandboxed).
    - **Modelos pinados** para reprodutibilidade: 1 modelo "frontier", 1 "low-cost", 1 OSS local (Ollama). IDs exatos + data, ex.: `claude-sonnet-4-6@2026-04`, `gpt-5-mini@2026-04`, `qwen2.5-7b-instruct@q4_K_M`.
    - **Judge prompt** versionado (`evals/v1/judges/groundedness.md`), com calibração contra 30 amostras humanas (Cohen κ ≥0.6 documentado).
    - **Sementes** fixadas; temperature 0; máximo 3 reruns para variância.
    - **Orçamentos** explícitos: `FEC-BUDGET-RAG-v1` (≤ X tokens entrada, Y saída por query), `FEC-BUDGET-LAT-v1` (p95 ≤ Z ms local), `FEC-BUDGET-COST-v1` (≤ R$ por 1k queries no provedor canônico do módulo). Valores numéricos definidos no piloto T1+T3 antes de qualquer outro módulo fechar.
    - **Citação padrão:** todo benchmark citado no curso roda no harness; valores reportados com modelo, data, hash do dataset, custo. Toda alegação de "X% melhor" linka o run que produziu o número.
27. **Política de evidência:** alegação técnica sem run no harness OU citação a paper datado é flagrada por `lint-content.py` (item 42). Sem cherry-pick.
28. **CHANGELOG do harness** (`evals/CHANGELOG.md`): mudança no judge ou dataset gera novo sufixo (`-v2`) — runs antigos continuam reproduzíveis.
28a. **Imutabilidade verificável do harness** (defesa contra "ajuste invisível" de números):
    - **Manifestos content-addressed:** cada run em `evals/v1/runs/<run-id>/manifest.json` registra `sha256` de `dataset/`, `judges/`, `MODELOS-SMOKE.md`, `BUDGETS.md`, prompt do módulo testado, e versão do `fec_sdk`. `manifest.schema.json` valida estrutura no CI.
    - **Trava de versão:** `scripts/freeze-evals.py` recalcula hashes dos arquivos sob `evals/v1/` (excluindo `runs/`) e compara com `evals/v1/HASHES.lock`. Mismatch sem bump de versão (`v1` → `v2`) bloqueia merge.
    - **CODEOWNERS:** `evals/**`, `MODELOS.md`, `CAPACIDADES.md`, `BUDGETS.md` exigem revisão de 2 maintainers; nada vai por self-merge.
    - **Auditoria pública:** `scripts/audit-evals.py` (rodável por qualquer um) percorre todas as alegações numéricas dos módulos (regex `\d+(\.\d+)?%|\d+x` perto de `evals/v1/runs/<id>`) e confirma que o run-id existe, que o manifesto bate com os hashes atuais, e que o número no texto bate com `metrics.json` do run. Falha quebra release.
    - **Branch protection** em `evals/v1/**` (push-direto negado, PR + 2 reviews + status check `freeze-evals` verde).

## 7. Padrão visual e durabilidade de assets (máximo de ilustrações)

29. **Cada módulo tem ≥3 ilustrações de tipos diferentes:** (a) diagrama de arquitetura/fluxo; (b) comparação visual antes/depois ou "ruim vs. bom"; (c) tabela de decisão ou matriz. Bloqueia entrega.
30. **Mermaid pré-renderizado em build, não em runtime.** Pipeline (`scripts/render-diagrams.sh`) usa `@mermaid-js/mermaid-cli` para gerar **dois SVGs** por diagrama (`<id>.dark.svg`, `<id>.light.svg`); HTML troca via CSS `prefers-color-scheme` ou data-attribute do toggle. Resolve adaptação ao tema, falha de rede no aluno e CSP.
31. **Tailwind: build local, não CDN.** `tailwindcss` no devDependencies → CSS purificado (`assets/css/inema.css`) versionado e servido localmente. CDN só em modo dev. Garante release zip funcional offline.
32. **Biblioteca de diagramas reutilizáveis** em `assets/diagrams/`: "anatomia da mensagem", "fluxo RAG", "loop ReAct", "hierarquia de memória", "ciclo de eval". Versionados.
33. **Acessibilidade:** todo SVG/diagrama tem `<title>` e `aria-label`; tabelas têm `<caption>`; informação nunca só na cor (cor + ícone/texto). axe-core no CI scheduled.
34. **Release zip auditado:** workflow desconecta rede e abre `index.html` em headless Chromium; falha quebra release.
34a. **Pipeline de conteúdo seguro contra XSS** (todo conteúdo contribuído passa por aqui antes de virar HTML estático):
    - **Markdown → HTML** com renderer determinístico (`markdown-it` configurado **sem `html: true`**); saída passa por **DOMPurify** (allowlist de tags/atributos definida em `scripts/sanitize-config.json`); `on*` handlers, `javascript:`, `data:` (exceto imagens whitelisted) banidos.
    - **JSON do quiz** (`quizzes/*.json`) tem `quiz.schema.json` validado; texto renderizado com `textContent`/template escapado, nunca `innerHTML` direto. Build falha em campo não-string ou tag suspeita.
    - **SVGs** (Mermaid pré-renderizado e ilustrações) passam por **svg-hush** ou DOMPurify modo SVG: removem `<script>`, `foreignObject`, `on*`, referências externas (`href` para http(s) externo bloqueado). `scripts/sanitize-svg.py` no build.
    - **CSP estrita** servida via `<meta http-equiv="Content-Security-Policy">` em todas as páginas: `default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'none'; frame-src 'self'; base-uri 'none'; form-action 'none'`. Sem `unsafe-inline` nem `unsafe-eval`. Nada de scripts externos (Tailwind/Mermaid são build-time, item 30-31).
    - **Iframes de modal** (item 7 do MASTER INEMA): `sandbox="allow-same-origin"` (sem `allow-scripts`); `src` validado contra allowlist relativa do repo.
    - **CI:** `lint-content.py` quebra em `<script>`, `on\w+=`, `javascript:`, `<iframe` sem `sandbox`; teste de aceitação injeta payloads conhecidos (XSS cheat-sheet) em fixtures e confirma que sanitização neutraliza; release zip verifica CSP via Playwright.

## 8. Profundidade técnica (anti-superficialidade)

35. **Bibliografia mínima por trilha** (`bibliografia/T<n>.md`): ≥10 referências (papers ArXiv com ID, posts datados com autor, RFCs/specs). Datado para o aluno saber o que envelheceu.
36. **Toda alegação de ganho** roda no harness (item 26) ou cita paper com link, data, e *delta numérico replicado*. Sem isso, o item é cortado.
37. **Glossário derivado, não inventado** (`GLOSSARIO.md`): script `scripts/build-glossary.py` extrai termos efetivamente referenciados nos módulos (com âncoras `<dfn>`); só termos com ≥1 backlink entram. Tamanho final emerge do conteúdo (estimado 50-90, não pré-fixado).
38. **Política "papers congelados na release"**: lista de refs congelada na tag `v1.0.0`, mas cada módulo carrega front-matter `atualizado-em: YYYY-MM-DD` e `errata-em: <link>`; trimestralmente revisor abre PR com "updated as of" — refs vivas sem invalidar URLs antigas.

## 9. Exercícios e auto-avaliação (rigor)

39. **Cada módulo GA tem 1 exercício "código mínimo"** (15-30 min) + 1 desafio **opcional** (rotulado "avançado", 1-2h). Exercício mínimo tem teste em `exercicios/<modulo>/test.py` rodável com `pytest`.
40. **Distribuição única de soluções:** `solucoes/` no main repo, **escondidas atrás de spoiler** (HTML `<details>` "Ver solução") + arquivo Python comentado. Sem branches separadas (descartado por conflitar com layout). CI valida que cada exercício tem (a) starter, (b) teste, (c) solução, todos coerentes.
41. **Quiz de 5 perguntas/módulo** em `quizzes/<modulo>.json` renderizado por `scripts/build-quiz.py`. Quiz final do curso (40 questões) com critério ≥80% para "certificado FEC v1.0" (página HTML personalizada — sem promessa exagerada).

## 10. Estrutura do repositório FEC

42. **Layout** (alinhado ao formato INEMA):
    ```
    FEC/
    ├── README.md                  # vitrine: objetivo, mapa Mermaid das trilhas, badges, "comece aqui"
    ├── ESCOPO.md, PRE-REQUISITOS.md, GLOSSARIO.md, CHANGELOG.md
    ├── MODELOS.md, CAPACIDADES.md, REVISORES.md, MEDIDAS.md
    ├── SECURITY.md, SECURITY-SANDBOX.md, SAFETY-INJECTION.md, SBOM.md
    ├── RUNBOOK.md, ALERTS.md, RELEASE-INCIDENT.md, ROTATION.md, HANDOFF.md, COMPAT.md, COMPAT-RETIRED.md
    ├── BREAK-GLASS.md, RISK-ACCEPTANCE.md, HOSTING-DECISION.md
    ├── CHECKSUMS-REVOCATION.md, BUDGETS-EXCEPTIONS.md
    ├── schemas/{compat.schema.json, revoked_versions.schema.json, budgets.schema.json, models.schema.json, capabilities.schema.json, alerts.schema.json, risk-acceptance.schema.json, checksums-revocation.schema.json}
    ├── evals/v1/{compat.json, revoked_versions.json, budgets.json, models.json, capabilities.json, alerts.json, risk-acceptance.json, checksums-revocation.json}
    ├── assets/csp/policy.txt
    ├── runbooks/{smoke-failure.md, secret-exposure.md, bad-release.md, provider-deprecation.md, dependency-cve.md, dataset-license-violation.md, sdk-yank.md, pages-down.md, pypi-down.md, zenodo-down.md}
    ├── postmortems/<data>-<slug>.md
    ├── releases/v<X.Y.Z>/lockfile.toml
    ├── CODEOWNERS, .gitleaks.toml
    ├── LICENSE (CC-BY-SA 4.0 conteúdo) + LICENSE-CODE (MIT) + LICENSES-THIRD-PARTY.md
    ├── index.html                 # landing INEMA
    ├── curso/trilha[1-6]/{index.html, modulo-X-Y.html}
    ├── fec_sdk/                   # cliente abstrato + adaptadores
    ├── exemplos/<modulo>/{neutro.py, anthropic.py, openai.py, oss.py}
    ├── exercicios/<modulo>/{enunciado.md, starter/, test.py}
    ├── solucoes/<modulo>/         # com aviso "spoiler" no HTML
    ├── projetos/{P1, P2, P5}/ + projetos/post-launch/{P3, P4}/
    ├── quizzes/*.json
    ├── evals/v1/{datasets/, judges/, runs/, BUDGETS.md, CHANGELOG.md}
    ├── fixtures/                  # datasets pequenos redistribuíveis
    ├── assets/{css/inema.css, diagrams/{src/, *.dark.svg, *.light.svg}, img/}
    ├── bibliografia/T<n>.md
    ├── scripts/{validate.py, lint-content.py, build-quiz.py, render-diagrams.sh, build-glossary.py, smoke-providers.py, freeze-evals.py, audit-evals.py, sanitize-svg.py, redact.py, check-budgets.py, build-compat.py, dashboard.py, check-killswitch-age.py, check-rc-gates.py, audit-pages.py, synthetic-check.py, validate-schemas.py, render-docs.py, rollback-pages.py, sign-manifest.py}
    └── .github/workflows/{ci-fast.yml, ci-scheduled.yml, release.yml}
    ```
43. **README como vitrine**, otimizado para primeira-leitura (não regra de tamanho): mapa visual, status v1.0, "comece aqui em 5 min", contribuição, licença. Overflow vai para docs linkados.
44. **Licenciamento explícito de terceiros (`LICENSES-THIRD-PARTY.md`):** manifesto fonte → licença → uso permitido para todo dataset, screenshot, diagrama-base, abstract de paper. CI bloqueia inclusão de fixture sem entrada no manifesto. Fixtures redistribuíveis preferidas; quando inviável, link estável (HuggingFace ID) + atribuição.
45. **CONTRIBUTING.md:** templates de issue (errata / dúvida / sugestão), processo de PR (RFC para nova trilha), checklist mínimo. Triagem semanal documentada.

## 11. Pipeline de CI (split fast/scheduled, realista)

46. **`ci-fast.yml` (PR e push, alvo <90s):**
    - `validate.py` (estrutura INEMA: 6 sub-tópicos, 3 subsessões, link INEMA, light-mode CSS, badge GA/beta) — bloqueia.
    - link checker INTERNO (links relativos do repo) — bloqueia.
    - lint Python dos exemplos/exercícios (ruff) + `pytest` em `exercicios/*/test.py` mockados — bloqueia.
    - **contract tests dos providers** (mocks gravados via `respx`/VCR, sem rede) — bloqueia.
47. **`ci-scheduled.yml` (diário e antes de release, sem limite estrito):**
    - link checker EXTERNO (lychee com cache, falhas viram issues automáticas, não bloqueio).
    - axe-core em todas as páginas — bloqueia release.
    - render de Mermaid e diff visual (Playwright) — bloqueia release.
    - spellcheck PT-BR (avisa).
    - `lint-content.py` (palavras 2.5k-4.5k, ≥3 refs, "Quando NÃO usar", evidência ligada ao harness) — bloqueia release.
    - `smoke-providers.py` (item 48).
48. **Smoke tests reais com guarda-rails — orçamentos coerentes** (corrige inconsistência $5/mês vs $1/dia):
    - **Orçamentos por tier e provedor** declarados em `evals/v1/BUDGETS.md` (substitui o número monolítico `FEC-CI-BUDGET`):
      | Tier | Por dia | Por mês | Cap nativo do provedor | Comentário |
      |------|---------|---------|----------------------|-----------|
      | `auto-smoke` por provedor | $0.50 | $10 | sim (key low-priv) | 3 provedores = ~$30/mês |
      | `production-smoke` | n/a (manual) | $20 | sim | usado 2-4x por release |
      | `release` | n/a (manual) | $10 | sim | usado 1-2x por release |
      | **Total mensal alvo** | — | **≤$60/mês** | — | folga de 20% para investigação |
    - **Soma mensal acumulada** medida em `MEDIDAS.md` (lida via API de billing dos provedores quando disponível, ou estimada por contagem de tokens × preço pinado).
    - **Budget exhausted é estado NÃO-VERDE** (não silencia smoke; resolve contradição "automático vs só humano via PR"):
      - **Defesa primária (provider-side, não muda flag protegido):** cap nativo do provedor (`max_spend` na key) corta o gasto sem precisar tocar em arquivo do repo. É autoritativo.
      - **Sinalização ao gate (lado do repo, sem editar `SMOKE-KILLSWITCH.json`):** `auto-smoke` ao detectar 80%+ do mês emite **GitHub Check Run** dedicado `budget-status` com `conclusion: neutral` e annotation com porcentagem; em 100% emite `conclusion: failure`. **`check-rc-gates.py` consulta o último Check Run `budget-status`** e bloqueia promoção quando `failure`; sem precisar mudar arquivo protegido.
      - **Bot PR como caminho documentado** (apenas para casos em que humanos QUEREM declarar manutenção prolongada): `auto-smoke` em 100% pode abrir um PR (label `automated:budget-killswitch`) que altera `SMOKE-KILLSWITCH.json` com `expected_off_until`, mas **só merge por humano** (CODEOWNERS exige). PR fica aberto; humano decide.
      - **Em outras palavras:** automatização rápida acontece via Check Run (não-protegido) e cap do provedor; mudança no arquivo protegido (kill-switch persistente) continua sendo só humano via PR — sem contradição.
      - 80% do mês → SEV-3 + warning no canal + Check Run `neutral`.
      - 100% do mês → SEV-2 + cap do provedor já cortou + Check Run `failure` + bot abre PR sugerindo kill-switch persistente.
      - **Bloqueia promoção rc→stable** sempre que o Check Run mais recente for `failure`/`neutral`, porque smoke não pode provar saúde sem rodar.
    - prompts canários determinísticos, retry com backoff, falha consistente abre issue e desativa o job até resolver. Modelos versionados em `evals/v1/MODELOS-SMOKE.md`.
48a. **Higiene de segredos no CI — três tiers de smoke** (resolve aprovação manual virar gargalo):
    - **Tier A — `auto-smoke` (diário, automático, sem aprovação):** roda em scheduled na main protegida; usa **`FEC_SMOKE_LOWPRIV`** (key dedicada com cap nativo do provedor de **$1/dia**, escopo só inferência, sem billing/admin); 5-10 prompts canários determinísticos; latência ≤30s. Sem aprovação manual = sem rubber-stamping. Nunca acessa `release` environment. Falha gera issue automática (item 71a).
    - **Tier B — `production-smoke` (manual, antes de release):** roda no **GitHub Environment `production-smoke`** com `required reviewers` (≥1 maintainer); usa **`FEC_SMOKE_PROD`** (cap $5/run); cobre os 3 modelos pinados em todos os módulos GA. Aprovação manual aqui é evento, não rotina.
    - **Tier C — `release` (manual, gate de tag):** Environment `release` com `required reviewers` distintos do tier B; só `release.yml` lê seus secrets.
    - **Alerta de execução perdida:** workflow `auto-smoke-watchdog.yml` (scheduled hourly) verifica que `auto-smoke` rodou nas últimas 26h via API GitHub; se não, abre issue `[FEC-AUTO] auto-smoke missed` e notifica owner. Captura "scheduled silenciosamente desativado".
    - **GitHub Environments protegidos** (`production-smoke`, `release`): secrets só visíveis a esses jobs; `deployment branch policy = main`.
    - **`pull_request_target` proibido** para qualquer workflow que receba secrets; `pull_request` sem secrets para forks. Forks rodam só CI-fast sem secrets.
    - **CODEOWNERS bloqueante** para `.github/workflows/**`, `scripts/smoke-providers.py`, `scripts/render-diagrams.sh`, `scripts/build-quiz.py`, `evals/**`, `MODELOS.md`, `BUDGETS.md` — exige aprovação de maintainer.
    - **Least-privilege:** API keys do smoke são keys dedicadas com escopo restrito + budget cap nativo do provedor (não confiar só no kill-switch local).
    - **Redação obrigatória de logs** (`scripts/redact.py` filtra padrões de chave, JWT, e respostas com >N chars); `actions/setup-*` configurados para não logar secrets.
    - **Secret scanning + push protection** habilitados no repo; `gitleaks` no CI-fast como bloqueio.
    - **`pinact`/SHA-pinning** de todas as actions de terceiros (sem `@v3` flutuante); Dependabot atualiza com PRs revisados.
49. **Gate de release v1.0** (`release.yml` manual, processo atômico):
    - **Draft Release primeiro:** workflow gera o zip, calcula `sha256` e `blake3` de cada artefato, escreve `CHECKSUMS.txt` assinado.
    - **Verificação:** roda CI-fast + scheduled completo + auditoria do zip offline (item 34) + verificação de assinaturas dos revisores (item 50) + diff contra release anterior (artefatos novos têm hash novo; idênticos reusam hash).
    - **Tag protegida:** branch protection inclui `tag protection rules` para `v*.*.*` (só maintainer assina).
    - **Finalização atômica:** só converte draft→published depois de checksums validados; mirror Zenodo recebe **mesmo zip + mesmo CHECKSUMS** via API com idempotency key (deposition ID); mismatch aborta.
    - **Retries são seguros:** workflow lê estado do draft existente, compara hashes; nunca sobrescreve assets — se hash diverge, falha e exige resolução manual.
    - **Concurrency:** `concurrency: group: release-${{ github.ref }}` com `cancel-in-progress: false` para evitar dois releases concorrentes.

## 12. Revisão técnica externa (gate, com protocolo definido)

50. **Protocolo de peer review:**
    - **2 revisores por trilha** (≥1 sênior na área específica). Lista nomeada em `REVISORES.md`.
    - **Perfil mínimo:** experiência em produção com LLM ≥1 ano, ou autoria de paper/post relevante na área. Curadoria do INEMA.
    - **Rubrica padrão** (`REVIEW-RUBRIC.md`): correção técnica, clareza, exercícios reproduzíveis, refs adequadas. Resposta sim/não por critério com comentário.
    - **SLA:** 7 dias úteis após receber bundle PDF + repo tag.
    - **Freeze date:** 14 dias antes do release; após freeze, só hot-fixes.
    - **Compensação:** menção em `REVISORES.md` + voucher do INEMA (definir antes do convite).
51. **Fallback se revisor falha:** trilha sem assinatura suficiente é publicada como `beta` em vez de `GA`, sinalizada no índice. Não bloqueia o release inteiro.

## 13. Ollama / caminho gratuito (com matriz testada)

52. **Matriz de hardware/modelo testada** (`OLLAMA-MATRIZ.md`): para cada lab, quais modelos OSS rodam e em que hardware mínimo (CPU + 16GB RAM, GPU 8GB, GPU 24GB). Ex.: T3 RAG roda com `qwen2.5-7b` em 16GB; T4.3 multi-agente exige 24GB ou API.
53. **Quando OSS não cobre:** lab marcado "requer API paga (créditos free elegíveis)" com link para programas (ex.: créditos iniciais Anthropic/OpenAI) E **versão simulada** com respostas gravadas (`fixtures/recorded/`) para o aluno completar a lógica sem chamar API.
54. **Capacidades fora de OSS local 2026-Q2** (assumindo o estado do momento): long context >128k confiável, tool calling avançado robusto, prompt caching nativo. Cada uma marcada na tabela e ensinada com adaptador/mock.

## 14. Edge cases pedagógicos e operacionais

55. **Modelo citado fica obsoleto:** páginas usam classes ("modelo de raciocínio de fronteira", "low-cost") + 1 exemplo concreto datado. `MODELOS.md` consolidado, atualizável sem reescrever módulos.
56. **API muda (deprecação):** exemplos versionados (`exemplos/<modulo>/anthropic/v2026-05/`). Smoke test scheduled detecta; CHANGELOG nota.
57. **Aluno não tem API key paga:** caminho OSS testado (item 52) ou simulação por gravação (item 53).
58. **Frameworks (LangChain/LangGraph) mudam:** preferir SDK puro do provedor + `fec_sdk` próprio. Quando usar framework, fixar versão e justificar; opcional, não pré-requisito.
59. **Dataset 404:** fixtures pequenas em `fixtures/` (com licença em `LICENSES-THIRD-PARTY.md`) ou HuggingFace ID estável. Nunca URL aleatória.
60. **Aluno "trapaceia" no quiz:** quiz é auto-avaliação. Para certificação séria, exige entrega de P5 com rubric.
61. **Plágio / paráfrase descuidada:** todo trecho que parafraseia cita fonte; checklist de revisão; política em `CONTRIBUTING.md`.
62. **Prompt injection — modelo de ameaça sandboxed (`SAFETY-INJECTION.md`):**
    - **In-scope:** payloads contra agentes hipotéticos do curso (sandbox local), classes documentadas (jailbreak básico, exfiltração de tool, tool poisoning).
    - **Out-of-scope:** payloads contra produtos reais nomeados; bypass de safety models específicos; armas/biológicos.
    - **Apresentação:** payloads em fixtures testáveis, não em texto corrido copy-paste; aluno roda em sandbox; redação evita que o módulo vire "manual de ataque".
    - **Defesas ensinadas:** input/output guard, allow-list de tools, separação de escopo do prompt do usuário, *spotlight* (Anthropic 2024).
62a. **Sandbox obrigatório de tools (`fec_sdk/sandbox/`)** para todo lab que dê acesso a sistema de arquivos, processo ou rede:
    - **Filesystem:** root jailed em diretório temporário do lab (`tempfile.mkdtemp` por sessão), **deny absolute paths**, deny `..`, deny symlinks (resolve antes de abrir e compara), tamanho máximo por arquivo (default 1 MB) e por sessão (default 50 MB), allowlist de extensões.
    - **Rede:** **egress negado por default**; opt-in por host/porta com allowlist explícita por lab. DNS bloqueado fora da allowlist. Localhost só se o lab declarar.
    - **Processo:** sem `subprocess` direto; helpers expõem só os comandos necessários; CPU/wallclock cap por chamada.
    - **Tests obrigatórios** antes de P2/P5 ou qualquer módulo virar GA: bateria `tests/sandbox/test_traversal.py` (tenta ler `~/.aws/credentials`, `/etc/passwd`, `.env`, `..//..//.env`, symlink para fora, arquivo binário gigante, exfiltração via DNS, bind socket inesperado). CI-fast roda; falha bloqueia merge no projeto/módulo afetado.
    - **Documentado** em `SECURITY-SANDBOX.md` com superfície de ataque assumida e limitações conhecidas.
63. **Conteúdo divisivo (ex.: comparações entre provedores):** linguagem factual, baseada em harness; sem juízo qualitativo sem run.

## 15. Cronograma realista até maio/2026 (pré-mortem aplicado)

64. **Premissa:** v1.0 é MVP definido (10 GA + 3 projetos). Beta sai junto, com aviso. Só assim cabe.
65. **Plano** (assumindo equipe pequena, 2-3 autores + 1 revisor técnico interno):
    - **Sem 1:** scaffolding (repo, CI fast/scheduled, templates HTML, lib de diagramas, **piloto T1.1 fechado**), define orçamentos numéricos do harness pelo piloto.
    - **Sem 2:** T1 (resto), T2 completo, harness FEC-EVAL-v1 fechado (datasets, judges, modelos pinados).
    - **Sem 3:** T3.1, T3.2, T4.1; primeira passada de P1.
    - **Sem 4:** T4.2, T5.1, T6.1; P2 escrito.
    - **Sem 5:** módulos beta (3.3, 4.3, 5.2, 6.2 — sem gate de qualidade GA), P5.
    - **Sem 6:** **freeze para review externo**; revisores trabalham; autores corrigem só hot-fixes.
    - **Sem 7:** axe-core + visual diff + smoke + release zip auditado; **publica `v1.0.0-rc.1`** (Pre-release) e abre canal beta com ≥30 alunos voluntários; gates de promoção (item 74) rodam por ≥7 dias; aprovado tudo, **promove o MESMO artefato** (re-tag) para `v1.0.0` — anúncio público só após.
66. **Marcos com critério "feito":** módulo GA = passa CI-fast + CI-scheduled + 2 assinaturas em `REVISORES.md` + harness gera número para a alegação central. Sem critério, não fecha.
67. **Plano de corte se atrasar (definido AGORA):** ordem de degradação — (i) joga 6.2 e 5.2 para post-launch; (ii) reduz P5 a "guia + checklist" sem rubric automatizado; (iii) adia T4.3; (iv) lança T4.2 como beta. Acima disso, adia release.

## 16. Lançamento, manutenção e governança

68. **Anúncio em maio/2026:** post no blog INEMA + LinkedIn + Twitter/X com mapa visual. Sem hype ("definitivo", "tudo o que você precisa"). Linkar bibliografia e harness para credibilidade.
69. **Métricas pós-lançamento (`MEDIDAS.md`):** stars, issues abertas/fechadas/triadas, PRs, completion rate via formulário opcional, erratas. Revisão semestral; thread de retrospectiva pública.
70. **Plano de updates:** trimestral curto (atualiza `MODELOS.md`, links externos quebrados, errata); anual maior (módulo afetado por mudança técnica significativa) — documentado no CHANGELOG.
71. **Governança de issues:** templates fixos, triagem semanal, label `errata`/`duvida`/`sugestao`/`beta-feedback`, owner rotativo.
71a. **Idempotência de issues automatizadas** (smoke/CI scheduled):
    - **`concurrency: group: smoke-${{ github.workflow }}`** com `cancel-in-progress: true` em jobs scheduled — sem runs sobrepostos.
    - **Idempotency key estável** ao abrir issue: `[FEC-AUTO] <job>:<canary-id>:<failure-class>` no título; script busca issue aberta com mesmo título antes de criar; se existir, **comenta** em vez de duplicar.
    - **Kill-switch como flag única protegida:** estado em `evals/v1/SMOKE-KILLSWITCH.json` (campo `enabled: bool`, `reason`, `since`, `expected_off_until`); CODEOWNERS-protegido; jobs não escrevem no flag — só humanos via PR.
    - **Kill-switch é estado NÃO-VERDE** (corrige falsa-aprovação na promoção rc→stable):
      - smoke desligado **não exit 0**: emite status `neutral`/`skipped` distinto via API GitHub Checks (`conclusion: neutral, status: completed, title: "kill-switched"`).
      - badge no `dashboard.html` mostra "smoke: KILL-SWITCHED desde <data>" — não confundível com verde.
      - **alarme de idade do kill-switch** (`scripts/check-killswitch-age.py`, scheduled hourly): se ligado por >48h sem `expected_off_until` ou >prazo declarado, abre issue SEV-2 e notifica owner. Captura "kill-switch eterno".
      - kill-switch ligado **bloqueia promoção rc→stable** (gate item 74) — `auto-smoke` precisa estar ativo; `kill-switched` ≠ ok.
    - **Auto-close** quando job verde N runs seguidos (config em `SMOKE-KILLSWITCH.json`).
72. **Backup e mirror:** Release zip estável (`fec-v1.0.0-2026-05-XX.zip`) verificado offline; anexado à GitHub Release; também espelhado em mirror público (Zenodo ou similar com DOI) para arquivamento.

---

## 17. Operações: canais, rollback, compatibilidade, observabilidade, capacidade

### 17.1 Canais de release (rc → stable, gate de promoção)

73. **Três canais publicados:**
    - `dev` — main; o que está sendo escrito; **não anunciado**.
    - `rc` (Release Candidate) — tag `v1.0.0-rc.N`, GitHub Pre-release, anunciado só para **canal beta** (≥30 alunos voluntários durante 7-14 dias antes do GA). Site exibe banner "Versão candidata".
    - `stable` — tag `v1.0.0`, GitHub Release. Anúncio público só após gates abaixo.
74. **Gates de promoção rc → stable** (todos verdes; senão estende rc ou adia GA):
    - **Burn-down de issues — política endurecida** (corrige normalização de defeitos sérios):
      - **zero em aberto** nas classes bloqueantes: `security`, `data-integrity`, `sandbox`, `licensing`, `lab-breaking` (lab GA não roda), `injection-bypass`. Workaround **não** desbloqueia.
      - **zero `severity:critical`** em qualquer classe.
      - **`severity:high` em outras classes:** ≤3 com workaround documentado **e** registro nominal em `RISK-ACCEPTANCE.md` assinado por ≥2 maintainers **e** disclosure visível no Release notes ("Known issues") + banner no site.
      - script `scripts/check-rc-gates.py` lê labels via API GitHub e bloqueia promoção; lista o que falta.
    - **Smoke (real, não kill-switched):** **7 dias com ≥6 execuções PASS reais** de `auto-smoke` (kill-switch inativo na janela; estados `neutral/skipped` não contam); `production-smoke` aprovado e verde nas últimas 72h; budget acumulado ≤80% do mês.
    - **Uso real:** ≥10 alunos beta concluíram pelo menos T1 + 1 trilha técnica; pesquisa mínima respondida (`FEC-BETA-FORM-v1`).
    - **Audit:** `audit-evals.py` (item 28a) verde; release zip auditado offline (item 34); CSP verificada (item 34a); **synthetic monitor** (item 89a) verde nas últimas 24h.
    - **Promoção é por re-tag do MESMO commit/artefato:** `v1.0.0` aponta para o commit do último `rc` aprovado; zip e checksums são reusados (não rebuild). Garante "ship the same bits we tested".
74a. **Cobertura "same bits" para TODOS os artefatos públicos** (corrige fuga via Pages/source archive/PyPI):
    - **Release zip nomeado é o canal canônico de download** — README do projeto direciona para ele explicitamente. Disclaimer no README: "downloads automáticos do GitHub (`Source code (zip/tar.gz)`) **não são auditados**; use o asset nomeado `fec-vX.Y.Z.zip`".
    - **GitHub Pages — paths versionados imutáveis** (corrige drift por rebuild diário e rollback parcial):
      - **Estrutura de URL:**
        - `/v1.0.0/` — build do release `v1.0.0` (HTML, CSS, SVG); **imutável após deploy**, nunca rebuilta.
        - `/v1.0.0-rc.N/` — buildss de RC, igualmente imutáveis; preservados pós-stable como histórico.
        - `/latest/` — alias (HTML redirect ou `<meta refresh>` minimal) para a versão `stable` atual; **único path que muda em rollback**.
        - `/status/` — dashboard, `revoked.json` assinado (item 79a.5), synthetic status; rebuilda de hora em hora; **NÃO contém conteúdo do curso**.
      - **Deploy versionado:** `release.yml` faz upload de `pages/v1.0.0/` para o branch `gh-pages` em path correspondente; nunca sobrescreve `/v1.0.0/` existente; `actions/deploy-pages@<sha>` configurado para preservar paths de versões anteriores.
      - **Rollback de uma versão ruim** (`scripts/rollback-pages.py`):
        - opção A — **swap do alias:** `/latest/` passa a apontar para a última versão GA boa (PR no branch `gh-pages` editando o redirect); URLs diretas `/v1.0.0/...` continuam servindo, mas cada página GA inclui **shell de deprecação carregado dinamicamente do `/status/banners.json`** (assinado) que injeta banner "esta versão foi deprecada, ir para /latest/".
        - opção B — **shell global de deprecação:** se SEV-1 grave, `rollback-pages.py` reescreve **apenas `index.html` de cada `vX.Y.Z` ruim** para shell mínimo "esta versão foi retirada, ir para /latest/". Mantém URLs vivos sem servir conteúdo comprometido.
      - **Auditoria:** `release.yml` gera `pages/v1.0.0/checksums.txt`; `audit-pages.py` baixa `https://inematds.github.io/FEC/v1.0.0/...` e diffa contra checksums; mismatch (drift, rebuild não autorizado) bloqueia promoção e dispara SEV-1.
      - **Promoção rc→stable:** alias `/latest/` só é flipado APÓS todos os gates de item 74 verdes; rebuild de `/status/` continua diário e não toca em `/v1.0.0/`.
      - **CSP — alinhada ao modelo de hosting** (corrige expectativa de header em GitHub Pages):
        - GitHub Pages **não permite** custom response headers para sites Pages padrão; CSP é declarada via `<meta http-equiv="Content-Security-Policy">` **na primeira tag dentro de `<head>`** (antes de qualquer `<link>`/`<style>`).
        - `audit-pages.py` valida pela parsing do HTML servido: meta CSP presente, na posição correta, exatamente como gerada (string match com versão pinada em `assets/csp/policy.txt`).
        - Synthetic monitor verifica meta CSP, não header — declarado em `RUNBOOK.md`.
        - **Roadmap declarado:** se proteções por header forem necessárias (ex.: `Strict-Transport-Security`, `Content-Security-Policy-Report-Only` em duplicata, `X-Frame-Options`), migrar para Cloudflare Pages ou Netlify (suporte nativo a `_headers`); decisão registrada em `HOSTING-DECISION.md` antes de v1.1.
    - **PyPI `fec_sdk` — protocolo de "build once, publish later"** (corrige `1.0.0rcN` ≠ `1.0.0` e impossibilidade de overwrite no PyPI):
      1. **Build determinístico do wheel de versão FINAL durante RC**: workflow gera `fec_sdk-1.0.0-py3-none-any.whl` e `.tar.gz` (não `1.0.0rcN`) com `SOURCE_DATE_EPOCH` fixado, `--no-build-isolation` controlado; calcula `sha256` e `blake3`.
      2. **Distribuição de RC sem PyPI público:** o wheel `1.0.0` é anexado **como asset do GitHub Pre-release `v1.0.0-rc.N`** + publicado em **TestPyPI** sob `1.0.0rcN` (alias para tracking, mas o teste real usa o wheel asset).
      3. **Smoke do RC:** `pip install --require-hashes -r releases/v1.0.0/lockfile.toml` consome o wheel `1.0.0` direto do GitHub asset (URL + hash); assim o aluno-beta exercita literalmente os bytes que serão promovidos.
      4. **Promoção:** workflow `release.yml` faz `twine upload` dos **mesmos arquivos** (mesmo `sha256`/`blake3` recalculados no upload) ao PyPI público sob `1.0.0`; PyPI não permite overwrite, mas como nunca subimos `1.0.0` antes, isso é first-write.
      5. **Verificação pós-upload:** `pip download fec-sdk==1.0.0 --no-deps --dest /tmp` em ambiente limpo; recalcula sha256/blake3 e exige bate exatamente com os hashes do RC. Mismatch → SEV-1 + yank imediato.
      6. **Lockfile da release** já carrega o hash final; `pip install --require-hashes` no synthetic check (item 89a) prova continuamente que PyPI serve os mesmos bytes auditados.
    - **GitHub source archive (auto):** não é canal suportado; se alguém usar, README diz "use o asset nomeado". `audit-evals.py` ignora source archives.
    - **Zenodo:** já content-addressed (item 49); confirma que sha256 do zip enviado bate com o sha256 do asset do GitHub Release.
75. **Cadência mínima de RC:** 7 dias entre `rc.N` e `stable`; cada bug crítico encontrado em rc reseta o relógio.

### 17.2 Runbook de incidente de release (`RUNBOOK.md` + `RELEASE-INCIDENT.md`)

76. **Severidades — SLA honesto com janelas declaradas** (resolve inconsistência "2h vs best-effort fora de hora"):
    - **SEV-1** (secret vazado, malware no zip, prompt injection com exfil real demonstrada, XSS na página publicada, sandbox quebrado em prod):
      - **Janela 24/7 estendida nos 14 dias pós-release** (rc + GA + 7d): **resposta ≤2h** com on-call primário + secundário em rotação 12h.
      - **Fora da janela (rotina):** **mitigação automática ≤2h** (revogação de chave, banner de deprecação, takedown de PyPI/Pages via workflow), **resposta humana ≤8h em horário comercial BR** ou ≤4h fim-de-semana melhor-esforço. SLA declarado, não escondido.
      - **Break-glass pré-autorizado:** owner secundário tem permissão prévia para (a) editar GitHub Release notes, (b) trocar `index.html` para incluir banner via `assets/banners/deprecation.html`, (c) yank no PyPI, (d) rotação de secrets — sem precisar acordar terceiros. Permissões documentadas em `BREAK-GLASS.md`; uso gera entrada de auditoria automática.
    - **SEV-2** (módulo GA com erro técnico que invalida exercício; benchmark errado; quebra de licença; provider deprecation que invalida lab; `auto-smoke` 2 dias seguidos red): **≤24h em horário comercial BR**, melhor-esforço fora.
    - **SEV-3** (errata de conteúdo, link quebrado, falha de a11y individual): **≤7 dias úteis.**
77. **Owner on-call rotativo** entre maintainers (rotação semanal em `ROTATION.md`); janela pós-release tem **primário + secundário** explícitos; SEV-1/2 acionam owner via canal acordado (Discord/Slack do INEMA, definido em `RUNBOOK.md`); alarme via webhook do GitHub Actions; **PagerDuty/equivalente opcional** para SEV-1 na janela estendida — se a equipe não comportar, SLA SEV-1 fora da janela é narrado honestamente como ≤8h.
78. **Procedimento de rollback / yank de release ruim:**
    1. **Banner de deprecação** em `index.html` e `README.md` (PR rápido, label `release-incident`) — banner é template em `assets/banners/deprecation.html` com data, severidade, link para errata.
    2. **GitHub Release editado** para "⚠️ DEPRECATED — see vX.Y.Z" no título; assets antigos **renomeados** com sufixo `-DEPRECATED-DO-NOT-USE` (GitHub não permite delete de assets de Release tagged sem perda de auditoria, mas permite rename/edit).
    3. **`CHECKSUMS-REVOCATION.md`** (lista de checksums revogados, com data, motivo, sucessor): atualizado com sha256/blake3 do zip ruim. `audit-evals.py` consulta a lista e falha em qualquer referência a hash revogado.
    4. **Tag NÃO é deletada** (preserva história e quebra menos quem já clonou); em vez disso, publica `v1.0.1` (ou `v1.0.0-revoked.1`) com fix; tag `v1.0.0` recebe edit no Release notes apontando para sucessor.
    5. **Zenodo:** depósito original NÃO pode ser deletado; usa "Versions" para depositar successor com nota de relação `IsNewVersionOf` + nota de deprecação no original (campo "Note"). DOI antigo continua resolvendo mas leva a página com aviso.
    6. **Comunicação:** post fixado no repo (`Discussions`); update no anúncio original (LinkedIn/X); e-mail para alunos beta cadastrados.
    7. **Postmortem público em `postmortems/<data>-<slug>.md`** dentro de 7 dias úteis (template fixo: timeline, causa raiz, mitigação, prevenção). Sem postmortem, incidente não fecha.
79. **Checklist de yank** (`RELEASE-INCIDENT.md`) é seguido linearmente; cada passo tem owner e prazo; failure modes do próprio runbook (ex.: "Zenodo offline") têm fallback documentado.
79a. **Rollback de pacote `fec_sdk` no PyPI** (corrige caminho de incidente faltando para SDK instalável):
    1. **PyPI yank:** `pypi-yank` na versão afetada (`pip install fec-sdk==X.Y.Z` ainda resolve para quem fixou explicitamente, mas resolvers preferem versão não-yanked). Yank justificado em `pyproject.toml`/release notes.
    2. **GHSA + OSV advisory:** abrir `GitHub Security Advisory` ligado ao repo, com CVSS, descrição, versões afetadas, versão corrigida; publicação automática para o OSV via integração GitHub.
    3. **Denylist em `COMPAT.md`:** seção `revoked_versions` (lista de `fec-sdk==X.Y.Z` revogadas com motivo, data, sucessor); `build-compat.py` remove combinações revogadas da matriz; `audit-evals.py` falha em qualquer release que liste versão revogada como suportada.
    4. **Patched release:** publica `X.Y.(Z+1)` com fix; release notes citam GHSA; lockfile do curso (`releases/v<X.Y.Z>/lockfile.toml`) atualizado para apontar para a versão patched.
    5. **Hard-fail em runtime — manifesto remoto assinado** (corrige limitação de wheel imutável):
       - `fec_sdk` ao iniciar busca **`https://inematds.github.io/FEC/v1/revoked.json`** (manifesto público em `/status/` no Pages, ver item 74b) com `If-Modified-Since` + cache local em `~/.fec/revoked.cache.json` (TTL 24h, `max-age` honrado, fallback ao cache se rede falha).
       - Manifesto é **assinado** com chave do projeto (Sigstore/cosign keyless OU `minisign`); chave pública embutida no wheel; assinatura inválida → ignora cache, log warning, NÃO faz hard-fail (defesa contra DoS adversarial: atacante que sequestre Pages não pode bloquear todos os usuários).
       - Wheel também embute **lista mínima conhecida em build-time** (`revoked_versions.json` interna) — defesa de baseline; manifesto remoto **adiciona** a essa lista, não substitui.
       - Se versão atual está na lista (embutida OU remota assinada) → `import fec_sdk` levanta `RevokedVersionError` com link para upgrade.
       - **Limitação declarada honestamente em `SECURITY.md`:** "wheels já instalados sem rede não receberão revogações novas; lockfile/`COMPAT.md`/synthetic check são as defesas autoritativas. O hard-fail em runtime é uma rede de segurança best-effort, não uma garantia." Sem promessa enganosa.
       - **Defesa primária:** `audit-evals.py` + `build-compat.py` consultam **manifesto canônico em `evals/v1/revoked_versions.json`** (machine-readable, item 95) e bloqueiam release se lockfile aponta para versão revogada — esta é a garantia firme; runtime é complemento.
    6. **Aviso aos alunos:** banner de deprecação (item 78.1) menciona explicitamente "atualize via `pip install -U fec-sdk`"; mensagem de erro do `RevokedVersionError` traz instrução exata.
    7. **Postmortem:** mesmo formato do item 78.7.
80. **Drill semestral:** simular SEV-2 em ambiente de staging do repo (fork) **incluindo cenário de yank de SDK no TestPyPI** e cronometrar resposta. Resultado em `MEDIDAS.md`.

### 17.3 Compatibilidade e versionamento (`COMPAT.md` + lockfiles)

81. **`fec_sdk` é artefato versionado:** publicado em PyPI (`pip install fec-sdk==1.0.0`) e fixado por release. SemVer estrita; major bump quebra API; minor adiciona; patch corrige. CHANGELOG do `fec_sdk` separado em `fec_sdk/CHANGELOG.md`.
82. **Lockfiles por release** (`releases/v1.0.0/lockfile.toml`):
    - versão exata de `fec_sdk`, de cada SDK de provedor (`anthropic==X`, `openai==Y`, `ollama-python==Z`), de `markdown-it`, `DOMPurify`, Tailwind, Mermaid CLI, Playwright, axe-core.
    - hashes dos modelos pinados (`MODELOS-SMOKE.md`).
    - hash do harness (`HASHES.lock` referenciado).
    - `requirements.lock` (Python) gerado por `uv pip compile` ou `pip-compile` com `--generate-hashes`.
    - `package-lock.json` (Node) committado.
83. **Matriz de compatibilidade** (`COMPAT.md`, gerada por `scripts/build-compat.py`):
    - colunas: `course_release` × `fec_sdk` × `python` (3.11 / 3.12) × provedor (versões SDK suportadas).
    - linhas: módulos GA + projetos.
    - célula: `OK` / `OK com nota` / `não suportado` / `revoked` (item 79a).
    - **Cardinalidade limitada (anti-explosão de combinações):**
      - **janela de suporte declarada:** 2 releases do curso, 2 minor versions do `fec_sdk`, 2 minor versions de cada SDK de provedor, 2 minors do Python (3.11/3.12 hoje; rola para 3.12/3.13 quando 3.13 estabilizar). Combinações fora da janela viram `extended-compat`.
      - `build-compat.py` aplica **cap rígido de 24 combinações testadas** no `ci-scheduled` (CI principal); resto vai para `ci-extended-compat.yml` (rodando só semanal e antes de release, sem orçamento de minutos críticos).
      - mudança que estoura o cap exige PR explícito atualizando janela de suporte (e abandonando linhas antigas em `COMPAT-RETIRED.md` com data) — sem inflação invisível.
    - CI scheduled (matrix `core`) roda os exercícios contra cada combinação `core`; CI extended (semanal) roda `core ∪ extended`; falha invalida a célula.
84. **Política de quebra de compatibilidade:** uma vez publicado `v1.0.0`, `fec_sdk` 1.x não pode quebrar API até `v2.0.0` do curso (≥6 meses). Modelos pinados podem virar deprecados pelo provedor — `MODELOS.md` marca, mas exemplos antigos continuam executáveis via fallback gravado (`fixtures/recorded/<modelo>/`) por 12 meses.
85. **Detecção de version skew em runtime — fail-fast por classe** (corrige "tudo é só warning"):
    - `fec_sdk.check_compat(module_id)` lê o front-matter (`expected_sdk_version`, `fec_release`, `python`) e a `COMPAT.md` embutida.
    - **Hard-fail (raise `IncompatibleVersionError`):**
      - versão revogada (item 79a.5);
      - major mismatch (`fec-sdk 2.x` com módulo `1.x`);
      - minor abaixo do mínimo declarado;
      - combinação `(course × sdk × python × provedor)` ausente da matriz de suporte (`COMPAT.md`).
    - **Warning amarelo (continua):** patch drift dentro do major/minor compatível; provedor com adapter "parcialmente equivalente" para o lab atual.
    - Mensagem de erro inclui comando exato de correção (`pip install fec-sdk==X.Y.Z`) e link para `COMPAT.md`. Aluno não fica em estado inválido silencioso.
    - **Override consciente:** variável `FEC_ALLOW_INCOMPAT=1` permite seguir só após confirmação explícita; uso é logado em `~/.fec/incompat.log` para alunos que reportarem bug.

### 17.4 Observabilidade e on-call (`RUNBOOK.md` + `ALERTS.md`)

86. **Métricas declaradas e medidas, não vaidosas:**
    - **Saúde do CI:** taxa de pass/fail de `auto-smoke` (7d/30d), idade da issue mais antiga aberta por bot, runs perdidos via watchdog, custo acumulado vs. orçamento `FEC-CI-BUDGET`.
    - **Saúde do conteúdo:** issues `errata` abertas/fechadas (7d/30d), tempo médio de fechamento de errata por severidade, links externos quebrados (scheduled link checker).
    - **Saúde de uso (opt-in):** alunos cadastrados no formulário beta, completion rate por módulo (auto-reportado), perguntas mais comuns (categorizadas em triagem).
    - **Métricas vetadas:** stars sozinha, downloads sozinhos — só servem como contexto, nunca como sinal de saúde.
87. **Dashboard reproduzível:** `scripts/dashboard.py` lê GitHub API (issues, workflows) + `MEDIDAS.md` e gera `docs/dashboard.html` estático no `gh-pages`; rebuilt diário; URL pública. Maintainer abre 1 vez por semana; alunos podem auditar.
88. **`ALERTS.md` mapeia métrica → severidade → owner → ação:**
    - `auto-smoke fail 2 dias seguidos` → SEV-2 → on-call → seguir runbook smoke-failure.
    - `gitleaks bloqueia em PR de maintainer` → SEV-1 → revogação imediata + rotação de keys.
    - `budget-cost > 80% mês` → SEV-3 → warning no canal; > 100% → SEV-2 + kill-switch.
    - `errata SEV-1 não atende ≤2h` → escala para owner secundário.
    - `mirror Zenodo offline ao publicar release` → SEV-2 → fallback documentado (publicar GitHub Release primeiro, Zenodo depois quando voltar).
89. **Playbooks por classe de falha** (`runbooks/`): `smoke-failure.md`, `secret-exposure.md`, `bad-release.md`, `provider-deprecation.md`, `dependency-cve.md`, `dataset-license-violation.md`, `sdk-yank.md`, `pages-down.md`, `pypi-down.md`, `zenodo-down.md`. Cada um: sintomas, diagnóstico em 5 min, mitigação, comunicação, postmortem trigger.
89a. **Synthetic monitoring de canais públicos** (`scripts/synthetic-check.py`, scheduled hourly + on-demand pós-release):
    - **GitHub Pages:** HTTP 200 em `/`, `/curso/trilha1/`, `/curso/trilha1/modulo-1-1.html`; sha256 do HTML servido bate com `pages-checksums.txt` (item 74a); CSP headers presentes; offline-rendering test em headless Chromium roda sem console error.
    - **GitHub Release assets:** baixa `fec-vX.Y.Z.zip` e `CHECKSUMS.txt` da última release `stable`; verifica sha256/blake3 contra a lista; se mismatch → SEV-1 (asset corrompido/rotacionado).
    - **Zenodo mirror:** GET DOI via API; baixa o zip do depósito; verifica sha256 igual ao do GitHub. Falha → SEV-2 + checa `runbooks/zenodo-down.md`.
    - **PyPI:** em ambiente virtual limpo, `pip install fec-sdk==<version> --require-hashes` usando lockfile da release; importa e roda smoke mínimo (`fec_sdk.selftest()`); falha → SEV-1 (instalação canônica quebrou).
    - **Falhas:** abrem issue idempotente (item 71a) com label `severity:high` + `synthetic` + canal afetado; 3 falhas seguidas no PyPI/Pages escalam para SEV-1.
    - **Status público:** resultado vai para `docs/status.html` (gh-pages) — alunos veem se um canal está fora antes de reportarem bug.
90. **On-call ergonômico:**
    - rotação semanal documentada (`ROTATION.md`); maintainer pode declinar com 48h de antecedência.
    - "horário comercial BR" (09-19 BRT em dias úteis) é o default; SEV-1 fora disso é melhor-esforço, não SLA.
    - handoff escrito (`HANDOFF.md` template) entre rotações; itens em aberto declarados.

### 17.5 Capacidade e orçamento de assets

91. **Orçamentos numéricos no CI** (`scripts/check-budgets.py`, bloqueia release se exceder):
    - **Tamanho do release zip:** ≤80 MB (alvo 40-60 MB). Inclui HTML, CSS, SVG pré-renderizados, fixtures pequenas. Datasets >5 MB ficam fora do zip e linkam HuggingFace ID estável.
    - **SVG por módulo:** ≤8 ilustrações; ≤300 KB cada após otimização (`svgo`); ≤1.5 MB total por módulo.
    - **Mermaid pré-renderizado:** ≤30 diagramas por trilha; nodes por diagrama ≤25 (legibilidade).
    - **Imagens raster:** evitar; quando necessário, AVIF/WebP, ≤200 KB.
    - **Repo total:** ≤500 MB (sem LFS). Fixtures grandes vão para `fixtures-external/` linkado, não committado.
92. **Orçamentos de CI:**
    - `ci-fast` ≤90s **wall** (matrix permitida; cada shard ≤90s); cache do uv/npm/pip obrigatório; falha por timeout = bloqueio.
    - `ci-scheduled` ≤30 min wall; sharding por trilha (6 shards paralelos); axe + Playwright em paralelo.
    - **GitHub Actions minutes:** orçamento de 2.000 min/mês declarado em `MEDIDAS.md`; alerta a 70% e 90%; >100% pausa scheduled non-essential.
    - **Concurrency** definida por workflow para evitar runs paralelos desnecessários (release single-flight; smoke single-flight; PR-fast pode paralelo).
    - Cache de `npm`/`uv`/`pip-compile`/`Playwright browsers`/`Mermaid CLI fontes` declarado e medido (hit rate em `MEDIDAS.md`).
93. **Quando exceder budget:** `check-budgets.py` lista qual módulo/asset estourou; PR ou bloqueia ou registra exceção em `BUDGETS-EXCEPTIONS.md` com justificativa e prazo de redução. Sem exceção em branco.
94. **Auditoria semestral de capacidade:** revisar tendência de tamanho/runtime; cortar se inflar; documentar em `MEDIDAS.md`.

### 17.6 Manifestos canônicos machine-readable (Markdown gerado)

95. **Source-of-truth = JSON validado por schema; Markdown é renderização** (corrige automação dependente de parsing frágil):
    - **Manifestos canônicos** sob `evals/v1/` e raiz, todos com `*.schema.json` em `schemas/`:
      - `compat.json` — matriz de compatibilidade (canônica para `build-compat.py`, `fec_sdk.check_compat`).
      - `revoked_versions.json` — versões revogadas do `fec_sdk` (canônica para `audit-evals.py`, runtime hard-fail, manifesto remoto).
      - `budgets.json` — orçamentos por tier/provedor/dia/mês (canônica para `check-budgets.py`, `auto-smoke`).
      - `models.json` — modelos pinados por papel (frontier/low-cost/oss) e versão (canônica para `MODELOS.md`).
      - `capabilities.json` — capacidade × provedor × status (canônica para `CAPACIDADES.md`).
      - `checksums-revocation.json` — releases revogados.
      - `risk-acceptance.json` — exceções aceitas com assinaturas (canônica para `check-rc-gates.py`).
      - `alerts.json` — métrica → severidade → owner → ação (canônica para `dashboard.py` e `runbooks/`).
    - **Schemas validados em CI** (`scripts/validate-schemas.py`, bloqueia merge); JSON Schema 2020-12; campos obrigatórios com tipos exatos.
    - **Markdown é gerado** por `scripts/render-docs.py` a partir dos JSONs (`COMPAT.md`, `MODELOS.md`, `CAPACIDADES.md`, `BUDGETS.md`, `CHECKSUMS-REVOCATION.md`, `RISK-ACCEPTANCE.md`, `ALERTS.md` — todos com header "_⚠️ Gerado de `<arquivo>.json`. NÃO edite manualmente._"). Pre-commit hook regenera; CI confirma `git diff --quiet` após render.
    - **Edits humanos:** vão direto no JSON via PR (CODEOWNERS protege); reviewers leem o JSON e o diff do MD gerado simultaneamente (fácil de auditar).
    - **Bot/scripts** sempre leem o JSON, nunca o MD; eliminar regex/parsing de Markdown da automação crítica (`audit-evals.py`, `check-rc-gates.py`, `check-budgets.py`, `build-compat.py`, `fec_sdk.check_compat`, `synthetic-check.py`).
    - **Versionamento:** mudanças em qualquer JSON canônico exigem bump em `evals/v1/HASHES.lock` (item 28a) ou são de outro domínio coberto por seu próprio versionamento; bump de versão major do schema requer migration script em `scripts/migrate-schema-vN-to-vM.py`.

---

**Observação operacional:** este plano descreve **conteúdo curricular + pipeline de execução**. A estrutura HTML específica (cores, componentes, light mode) segue o formato INEMA.CLUB já estabelecido (skill `formato-curso`); na implementação, consultar `references/MASTER_COMPLETO.md` para não duplicar especificação visual.

---

## Changelog (revisões pós-review)

### Round 1 — Codex senior-engineer review

**Aceitos integralmente:**
- **HIGH 1 (escopo não fecha):** v1.0 redefinida como **MVP nomeado** — 10 módulos GA + 4 beta + 3 projetos GA + 2 opcionais; cronograma com **plano de corte definido a priori** (item 67); status `GA`/`beta` declarado por página (itens 6, 9-12, 24).
- **HIGH 2 (métricas com placeholder):** criada **seção 6 — harness FEC-EVAL-v1 congelado** (itens 26-28): datasets nomeados, modelos pinados, judges com Cohen κ, sementes, orçamentos numéricos definidos no piloto T1+T3 antes de qualquer outro módulo fechar.
- **HIGH 3 (provider-agnostic vs específico):** seção 3 reescrita (itens 14-16) — neutro primeiro, `fec_sdk` canônico, adaptadores só onde a abstração não cobre, `CAPACIDADES.md` consolidada com status nativo/adaptador/não-suportado/mock.
- **HIGH 4 (alegações sem evidência):** **toda alegação técnica roda no harness ou cita paper datado** com delta replicado; `lint-content.py` flagra (itens 27, 36).
- **HIGH 5 (workload por módulo inconsistente):** alvo reduzido a **2.5-4.5k palavras**, total 60-105 min, calibrado pelo **piloto T1.1** antes de produzir o resto; desafios marcados `opcional/avançado` (itens 17, 39).
- **HIGH 6 (review externo não staffado):** seção 12 nova (itens 50-51) com perfil, lista nomeada, rubrica, SLA 7 dias, freeze 14 dias antes, compensação, **fallback de degradar para beta** se faltar assinatura.

- **MED (formato INEMA ambíguo):** item 18 alinha conteúdo principal a "seções ricas" + sub-tópicos expansíveis para sub-blocos, conforme `MASTER_COMPLETO.md`. Plano não duplica spec visual (segue a skill `formato-curso`).
- **MED (Ollama hand-waved):** seção 13 nova (itens 52-54) com matriz testada de hardware/modelo; capacidades fora do OSS local marcadas e ensinadas com adaptador/mock.
- **MED (durabilidade Tailwind/Mermaid CDN):** itens 30-31 mudam para **Tailwind buildado local** e **Mermaid pré-renderizado em build** (dois SVGs por diagrama, dark/light); item 34 audita release zip offline em headless Chromium.
- **MED (Mermaid dark/light hand-waved):** resolvido pelo pré-render dual SVG (item 30) — sem dependência de re-render em runtime.
- **MED (CI <2min não credível):** seção 11 reescrita (itens 46-49) com **split ci-fast (<90s) vs ci-scheduled** — link externo, axe, visual diff, smoke, lint-content rodam scheduled.
- **MED (smoke real perigoso):** item 48 — orçamento `$5/mês`, kill-switch, secrets dedicados, prompts canários determinísticos, retry/backoff, falha abre issue e desativa job.
- **MED (licença não cobre terceiros):** item 44 + arquivo `LICENSES-THIRD-PARTY.md` como manifesto bloqueante no CI.
- **MED (prompt injection vago):** item 62 — `SAFETY-INJECTION.md` com modelo de ameaça sandboxed, in/out-of-scope, payloads em fixtures (não copy-paste em texto), defesas explícitas.
- **MED (soluções com path conflitante):** item 40 escolhe modelo único — `solucoes/` no main com `<details>` spoiler, sem branch separada; CI valida coerência starter/teste/solução.
- **MED (eval empurrado para T6):** item 19 introduz "eval-thinking" desde T1.1, template em T2.2, aplicação em T3-T5, aprofundamento em T6.

- **LOW (70-90 páginas não bate):** removido número fictício; itens 42-43 deixam o layout falar.
- **LOW (glossário 80-120 inventado):** item 37 — `build-glossary.py` deriva de termos efetivamente referenciados; tamanho emerge.
- **LOW (README 200 linhas arbitrário):** item 43 — otimiza para primeira-leitura, sem regra de tamanho.
- **LOW (papers congelados ficam stale):** item 38 — congela na release + front-matter `atualizado-em` + revisão trimestral via PR; refs vivas sem invalidar URLs.

**Rejeitados:** nenhum. Todas as findings foram tratadas como materiais.

**Adições de própria iniciativa (consequência das mudanças):**
- `CAPACIDADES.md`, `OLLAMA-MATRIZ.md`, `SAFETY-INJECTION.md`, `LICENSES-THIRD-PARTY.md`, `REVIEW-RUBRIC.md` adicionados à estrutura do repo (item 42).
- Mirror Zenodo com DOI (item 72) para arquivamento durável independente de GitHub.

### Round 2 — Codex security & data-integrity review

**Aceitos integralmente:**
- **HIGH 1 (sandbox de tools em P2/P5):** **item 62a novo** — `fec_sdk/sandbox/` com root jailed em `tempfile.mkdtemp`, deny absolute paths/`..`/symlinks, tamanho/extensão limitados, **egress de rede negado por default** com allowlist opt-in, sem `subprocess` direto. **Bateria `tests/sandbox/test_traversal.py`** (lê `~/.aws/credentials`, `/etc/passwd`, `.env`, `..//..//.env`, symlink-out, exfil DNS) bloqueia merge no projeto/módulo afetado. Itens 22 e 23 atualizados com **gates explícitos**: P2 só vira GA com bateria sandbox verde; P5 exige sandbox + golden `FEC-GS-INJECTION-v1` ≥18/20 bloqueados. `SECURITY-SANDBOX.md` documenta superfície e limitações.
- **HIGH 2 (smoke com secrets):** **item 48a novo** — GitHub Environments protegidos (`production-smoke`, `release`) com required reviewers e deployment branch policy = main; `pull_request_target` proibido; forks rodam só CI-fast sem secrets; **CODEOWNERS bloqueante** em `.github/workflows/**`, `scripts/smoke-providers.py`, `evals/**`, `MODELOS.md`, `BUDGETS.md`; keys com escopo restrito + budget cap nativo do provedor; **`scripts/redact.py`** filtra logs; **gitleaks** + secret scanning + push protection no CI-fast como bloqueio; **SHA-pinning** de actions de terceiros + Dependabot.
- **MED 1 (XSS no pipeline estático):** **item 34a novo** — Markdown via `markdown-it` sem `html: true` + DOMPurify; quiz JSON com `quiz.schema.json` validado e `textContent`/template escape (nunca `innerHTML`); SVG sanitizado via `svg-hush`/DOMPurify SVG (remove `<script>`, `foreignObject`, `on*`, hrefs externos); **CSP estrita** sem `unsafe-inline`/`unsafe-eval`, `default-src 'none'`, `connect-src 'none'`; iframes de modal com `sandbox="allow-same-origin"` (sem `allow-scripts`) e `src` na allowlist relativa; CI quebra em payloads conhecidos (XSS cheat-sheet) e Playwright valida CSP no release zip.
- **MED 2 (harness sem trava de imutabilidade):** **item 28a novo** — manifestos content-addressed em `evals/v1/runs/<run-id>/manifest.json` com `sha256` de dataset/judges/MODELOS-SMOKE/BUDGETS/prompt do módulo/`fec_sdk`; `manifest.schema.json` validado no CI; `freeze-evals.py` compara hashes contra `evals/v1/HASHES.lock` e bloqueia mismatch sem bump de versão; CODEOWNERS exige 2 reviews em `evals/**`/`MODELOS.md`/`CAPACIDADES.md`/`BUDGETS.md`; **`audit-evals.py` público** percorre alegações numéricas dos módulos e confirma run-id, manifesto e bate número com `metrics.json`; branch protection em `evals/v1/**`.
- **MED 3 (release não atômico):** **item 49 reescrito** — Draft Release primeiro, gera `sha256`/`blake3` + `CHECKSUMS.txt` assinado; verificação roda CI completo + auditoria offline + assinaturas de revisores + diff contra release anterior; tag protegida via tag protection rules; finalização atômica só após checksums OK; **mirror Zenodo recebe mesmo zip + mesmo CHECKSUMS via API com idempotency key**; retries são idempotentes (lê estado do draft, compara hashes, nunca sobrescreve); `concurrency: group: release-*` com `cancel-in-progress: false`.

- **LOW (issues/kill-switch sob runs sobrepostos):** **item 71a novo** — `concurrency` no smoke (`cancel-in-progress: true`); idempotency key estável no título da issue (`[FEC-AUTO] <job>:<canary-id>:<failure-class>`) com comentário em vez de duplicação; **kill-switch único protegido em `evals/v1/SMOKE-KILLSWITCH.json`** (CODEOWNERS-protegido, escrito só por humanos via PR); auto-close após N runs verdes seguidos.

- **Layout do repo:** adicionados `SECURITY.md`, `SECURITY-SANDBOX.md`, `SBOM.md`, `CODEOWNERS`, `.gitleaks.toml` + scripts `freeze-evals.py`, `audit-evals.py`, `sanitize-svg.py`, `redact.py` (item 42).

**Rejeitados:** nenhum.

### Round 3 — Codex ops & SRE review

**Aceitos integralmente:**
- **HIGH 1 (sem caminho de rollback após release ruim):** **seção 17.2 nova** (itens 76-80) com severidades SEV-1/2/3 e SLAs (2h/24h/7d), owner on-call rotativo (`ROTATION.md`), procedimento de yank passo-a-passo (banner de deprecação, edit do GitHub Release com sufixo `-DEPRECATED-DO-NOT-USE`, **`CHECKSUMS-REVOCATION.md`** consultado por `audit-evals.py`, `v1.0.1` como sucessor sem deletar tag, Zenodo `IsNewVersionOf` + nota no original, comunicação multi-canal, **postmortem público em `postmortems/`** dentro de 7 dias úteis com template fixo). Drill semestral simulando SEV-2.

- **MED 1 (smoke required-reviewers vira gargalo OU rubber-stamp):** **item 48a reescrito em três tiers** — `auto-smoke` diário automático com key low-priv `FEC_SMOKE_LOWPRIV` ($1/dia, escopo só inferência) sem aprovação manual; `production-smoke` manual antes de release; `release` separado com reviewers distintos. **`auto-smoke-watchdog.yml`** (hourly) detecta job perdido via API GitHub e abre issue `[FEC-AUTO] auto-smoke missed` — captura "scheduled silenciosamente desativado".
- **MED 2 (sem RC/canais):** **seção 17.1 nova** (itens 73-75) — três canais (`dev`, `rc`, `stable`); `v1.0.0-rc.N` como Pre-release, anunciado só ao canal beta (≥30 alunos por 7-14 dias); **gates de promoção** (zero `severity:critical`, ≤3 `severity:high` com workaround, 7d de auto-smoke verde, ≥10 alunos beta concluindo T1+1 técnica, audit verde); **promoção é re-tag do MESMO commit/artefato** ("ship the same bits we tested"). Item 65 (cronograma sem 7) ajustado para publicar RC antes do anúncio público.
- **MED 3 (version skew client/server/SDK/evals):** **seção 17.3 nova** (itens 81-85) — `fec_sdk` publicado em PyPI versionado (SemVer estrita, CHANGELOG separado); **lockfiles por release** (`releases/v1.0.0/lockfile.toml` + `requirements.lock` com `--generate-hashes` + `package-lock.json`); **matriz de compatibilidade** (`COMPAT.md` gerada por `build-compat.py`) com `course × fec_sdk × python × provedor` rodando matrix em CI scheduled; política "1.x não quebra API até 2.0 (≥6 meses)"; modelos deprecados continuam executáveis via `fixtures/recorded/<modelo>/` por 12 meses; **detecção runtime** (`fec_sdk.__version__` vs `expected_sdk_version` no front-matter) imprime warning amarelo.
- **MED 4 (observabilidade vaidosa, on-call sem ergonomia):** **seção 17.4 nova** (itens 86-90) — métricas declaradas e medidas (saúde CI, conteúdo, uso opt-in; **stars/downloads vetados como sinal de saúde**); **dashboard reproduzível** via `scripts/dashboard.py` em `gh-pages` (público, auditável); **`ALERTS.md`** mapeia métrica→severidade→owner→ação (auto-smoke fail 2 dias = SEV-2; gitleaks = SEV-1; budget >80% = SEV-3, >100% = SEV-2 + kill-switch; mirror Zenodo offline = fallback documentado); **`runbooks/`** com playbooks por classe de falha (smoke-failure, secret-exposure, bad-release, provider-deprecation, dependency-cve, dataset-license-violation); on-call ergonômico (rotação semanal, decline ≥48h antes, "horário comercial BR" como default, SEV-1 fora é melhor-esforço, handoff escrito).

- **LOW (capacidade sem orçamento):** **seção 17.5 nova** (itens 91-94) — `check-budgets.py` bloqueia release se exceder: zip ≤80 MB (alvo 40-60), SVG ≤8 por módulo / ≤300 KB cada / ≤1.5 MB total, Mermaid ≤30 por trilha / nodes ≤25, repo total ≤500 MB; **`ci-fast` ≤90s wall**, **`ci-scheduled` ≤30 min** sharded por trilha (6 shards); **GitHub Actions minutes ≤2.000/mês** com alertas 70%/90% e pausa scheduled em >100%; cache obrigatório com hit rate medido em `MEDIDAS.md`; exceções em `BUDGETS-EXCEPTIONS.md` com prazo de redução; auditoria semestral de tendência.

- **Layout do repo:** adicionados `RUNBOOK.md`, `ALERTS.md`, `RELEASE-INCIDENT.md`, `ROTATION.md`, `HANDOFF.md`, `COMPAT.md`, `CHECKSUMS-REVOCATION.md`, `BUDGETS-EXCEPTIONS.md`, `runbooks/`, `postmortems/`, `releases/v<X.Y.Z>/lockfile.toml` + scripts `check-budgets.py`, `build-compat.py`, `dashboard.py`.

**Rejeitados:** nenhum.

### Round 4 — Codex ops & SRE deepening

**Aceitos integralmente:**
- **HIGH 1 (kill-switch falsifica gate "7d verde"):** **item 71a estendido** — kill-switch desligado emite estado `neutral/kill-switched` distinto via Checks API (não `success`); badge no dashboard distingue; **`check-killswitch-age.py`** alarma quando `>48h` ligado sem `expected_off_until`. **Item 74 endurecido:** "Smoke real (não kill-switched): 7 dias com ≥6 PASS reais; estados `neutral/skipped` não contam"; kill-switch ativo bloqueia promoção.
- **HIGH 2 (PyPI sem caminho de yank):** **item 79a novo** — PyPI yank, **GHSA + OSV advisory**, **denylist em `COMPAT.md` (`revoked_versions`)** consumida por `audit-evals.py` e `build-compat.py`, patched release com lockfile atualizado, **runtime hard-fail (`RevokedVersionError`)** lendo `revoked_versions.json` embutido no pacote, banner com `pip install -U`, postmortem obrigatório. `runbooks/sdk-yank.md` adicionado. Drill semestral inclui yank em TestPyPI.

- **MED 1 ("same bits" não cobre Pages/source archive/PyPI):** **item 74a novo** — release zip nomeado é canal canônico (README aponta explicitamente; "GitHub auto-archives não auditados"); **`audit-pages.py`** baixa o site servido e diffa contra `pages-checksums.txt`; **PyPI** usa builds reproduzíveis (`SOURCE_DATE_EPOCH`), `pip install --require-hashes` no smoke pós-publicação, checksums no Release; Zenodo já content-addressed e cruzado com sha256 do Release.
- **MED 2 (version skew só warning):** **item 85 reescrito** — `fec_sdk.check_compat()` faz **hard-fail (`IncompatibleVersionError`)** em revoked / major mismatch / minor abaixo do mínimo / combinação ausente da `COMPAT.md`; warning amarelo apenas para patch drift compatível ou adapter "parcialmente equivalente"; mensagem de erro inclui comando exato; override `FEC_ALLOW_INCOMPAT=1` é logado em `~/.fec/incompat.log`.
- **MED 3 (SLA SEV-1 "2h vs best-effort" inconsistente):** **item 76 reescrito** — janela 24/7 estendida (rc + GA + 7d) com primário+secundário, ≤2h; **fora da janela: mitigação automática ≤2h** (revogação de chave, banner, takedown via workflow) + resposta humana ≤8h horário comercial / ≤4h fim-de-semana melhor-esforço — declarado, não escondido. **`BREAK-GLASS.md`** com permissões pré-autorizadas (editar Release notes, banner, yank PyPI, rotação de secrets) com auditoria automática. PagerDuty opcional; quando ausente, narração honesta como ≤8h.
- **MED 4 (sem synthetic monitoring de canais públicos):** **item 89a novo** — `synthetic-check.py` hourly + on-demand pós-release valida GitHub Pages (HTTP + sha256 + CSP + offline rendering), Release assets (sha256/blake3 contra `CHECKSUMS.txt`), Zenodo (sha256 vs GitHub), **PyPI em venv limpo com `pip install --require-hashes` + `fec_sdk.selftest()`**; falhas geram issue idempotente; 3 falhas seguidas em PyPI/Pages escalam para SEV-1; **`docs/status.html`** público em gh-pages. `runbooks/{pages-down,pypi-down,zenodo-down}.md` adicionados.
- **MED 5 (orçamentos $5/mês vs $1/dia inconsistentes):** **item 48 reescrito** — tabela coerente em `evals/v1/BUDGETS.md`: `auto-smoke` $0.50/dia × 3 provedores ≈ $30/mês; `production-smoke` $20/mês; `release` $10/mês; **alvo total ≤$60/mês com 20% folga**. Soma medida em `MEDIDAS.md`; budget exhausted é estado **NÃO-VERDE** (80% = SEV-3 warning, 100% = SEV-2 + kill-switch automatizado com `expected_off_until = início do próximo mês`); **bloqueia promoção rc→stable** quando smoke desativado.
- **MED 6 (rc gate aceita 3 high-severity):** **item 74 endurecido** — **zero em aberto** nas classes bloqueantes (`security`, `data-integrity`, `sandbox`, `licensing`, `lab-breaking`, `injection-bypass`); workaround **não** desbloqueia. ≤3 `severity:high` em outras classes só com **`RISK-ACCEPTANCE.md` assinado por ≥2 maintainers + disclosure no Release notes (Known issues) + banner no site**. `check-rc-gates.py` lê via API GitHub e bloqueia.

- **LOW (matriz de compat sem cap):** **item 83 estendido** — janela de suporte declarada (2 releases × 2 minors `fec_sdk` × 2 minors SDK provedor × 2 minors Python); **cap rígido de 24 combinações no `ci-scheduled` core**; resto vai para `ci-extended-compat.yml` (semanal, fora do orçamento crítico de 30 min); estourar cap exige PR explícito atualizando janela e movendo linhas antigas para `COMPAT-RETIRED.md`.

- **Layout do repo:** adicionados `BREAK-GLASS.md`, `RISK-ACCEPTANCE.md`, `COMPAT-RETIRED.md`, `runbooks/{sdk-yank,pages-down,pypi-down,zenodo-down}.md` + scripts `check-killswitch-age.py`, `check-rc-gates.py`, `audit-pages.py`, `synthetic-check.py`.

**Rejeitados:** nenhum.

### Round 5 — Codex ops & SRE deepening (final, hard stop)

**Aceitos integralmente:**
- **HIGH 1 (PyPI same-bits: `1.0.0rcN` ≠ `1.0.0`):** **item 74a (PyPI) reescrito** com protocolo "build once, publish later":
  1. wheel `1.0.0` (versão final, não `rcN`) é buildado **durante o RC** com `SOURCE_DATE_EPOCH` fixado;
  2. distribuído como **asset do GitHub Pre-release `v1.0.0-rc.N`** + `1.0.0rcN` no TestPyPI só para tracking — RC real exercita o wheel `1.0.0` via lockfile com hash;
  3. promoção sobe os **mesmos arquivos** ao PyPI público sob `1.0.0` (first-write, sem overwrite);
  4. verificação pós-upload: `pip download` em ambiente limpo + recálculo de sha256/blake3 contra hashes auditados; mismatch → SEV-1 + yank imediato.
- **HIGH 2 (`RevokedVersionError` embutido não protege wheels já instalados):** **item 79a.5 reescrito** — manifesto remoto **assinado** em `https://inematds.github.io/FEC/v1/revoked.json` (Sigstore/cosign keyless ou minisign), cache local `~/.fec/revoked.cache.json` com TTL 24h e `If-Modified-Since`, fallback ao cache em rede off; chave pública embutida no wheel; assinatura inválida não-bloqueia (defesa contra DoS por sequestro de Pages). **Limitação declarada honestamente em `SECURITY.md`:** wheel offline já instalado não recebe revogações novas — runtime é rede de segurança best-effort, não garantia. **Defesa primária firme:** lockfile + `compat.json` + `audit-evals.py` bloqueiam release que aponta para versão revogada.
- **HIGH 3 (Pages não imutável/versionada → drift e rollback parcial):** **item 74a (Pages) reescrito** — paths versionados imutáveis: `/v1.0.0/`, `/v1.0.0-rc.N/`, `/latest/` (alias), `/status/` (separado, dashboard/revoked.json/synthetic). Deploy nunca sobrescreve `/vX.Y.Z/` existente. **`scripts/rollback-pages.py`** com duas opções: (A) swap do alias `/latest/` + shell de deprecação dinâmico via `/status/banners.json` assinado; (B) reescrita de `index.html` da versão ruim para shell mínimo de deprecação. Promoção rc→stable só flipa `/latest/` após gates verdes; `/status/` rebuilda diariamente sem tocar em `/v<X.Y.Z>/`.

- **MED 1 (CSP via header inexistente em GitHub Pages):** **item 74a (Pages, sub-bullet CSP)** alinhado ao modelo — CSP via `<meta http-equiv>` na primeira tag dentro de `<head>`; `audit-pages.py` valida via parsing do HTML servido (string match contra `assets/csp/policy.txt` pinado); synthetic monitor verifica meta CSP, não header (declarado em `RUNBOOK.md`). **`HOSTING-DECISION.md`** documenta roadmap: se headers reais forem necessários (HSTS, X-Frame-Options), migrar para Cloudflare Pages / Netlify antes de v1.1.
- **MED 2 (kill-switch automático vs só humano):** **item 48 (Budget exhausted) reescrito** sem contradição — defesa primária é **cap nativo do provedor** (autoritativo, fora do repo); sinalização ao gate é **GitHub Check Run `budget-status`** (`neutral` em 80%, `failure` em 100%) consumido por `check-rc-gates.py`, não toca em arquivo protegido. Mudança no flag persistente `SMOKE-KILLSWITCH.json` continua sendo **apenas via PR humano**, mas bot pode **abrir** PR (label `automated:budget-killswitch`) que humano decide se merga. Sem contradição.

- **LOW (automação dependendo de parsing de Markdown):** **seção 17.6 nova (item 95)** — JSON validado por schema é source-of-truth para `compat`, `revoked_versions`, `budgets`, `models`, `capabilities`, `checksums-revocation`, `risk-acceptance`, `alerts`; **Markdown é gerado** por `render-docs.py` com header "_⚠️ Gerado de `<arquivo>.json`. NÃO edite manualmente._"; pre-commit hook regenera; CI confirma `git diff --quiet` após render. Bots/scripts críticos leem só o JSON, eliminando regex de Markdown da automação.

- **Layout do repo:** adicionados `HOSTING-DECISION.md`, `schemas/*.schema.json` para todos os 8 manifestos, `evals/v1/*.json` correspondentes, `assets/csp/policy.txt` + scripts `validate-schemas.py`, `render-docs.py`, `rollback-pages.py`, `sign-manifest.py`.

**Rejeitados:** nenhum.

### Estado final do plano após 5 rounds

- **62 itens originais** → **95 itens detalhados** após 5 rodadas adversariais (3 personas: senior-eng, security/data-integrity, ops/SRE × 2).
- **6 seções originais** → **17 seções**, com seção 17 (Operações: canais, rollback, compat, observabilidade, capacidade, manifestos JSON) construída inteiramente a partir das findings.
- **Total de findings tratadas:** 6 high + 10 med + 4 low (R1) + 2 high + 3 med + 1 low (R2) + 1 high + 4 med + 1 low (R3) + 2 high + 6 med + 1 low (R4) + 3 high + 2 med + 1 low (R5) = **14 high + 25 med + 8 low = 47 findings, todas aceitas**.
- **Plano agora é executável** com gates objetivos, runbooks por classe de falha, manifestos canônicos auditáveis, e SLAs honestos.
