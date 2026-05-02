# Como contribuir com a FEC

Obrigado pelo interesse. Este projeto segue um plano endurecido (`PLAN.md`) com gates objetivos de qualidade. Contribuições são bem-vindas, mas precisam respeitar o escopo e os critérios.

## Antes de começar

1. Leia [`ESCOPO.md`](./ESCOPO.md) — confirme que sua ideia está dentro.
2. Leia [`PLAN.md`](./PLAN.md) (especialmente o contrato fixo de módulo, item 18) e o `RELATORIO-CLAUDEX.md`.
3. Para mudanças não-triviais, abra issue ANTES do PR — discuta abordagem.

## Tipos de contribuição

### Errata / correções pequenas

- Use o template `.github/ISSUE_TEMPLATE/errata.md`.
- PR direto também é aceito; rotule `errata`.
- CI valida (estrutura INEMA, sanitização, links internos).

### Dúvidas

- Use o template `duvida.md`. Não envie por e-mail — issue público beneficia outros alunos.

### Sugestão de novo conteúdo

- Issue com label `sugestao` PRIMEIRO.
- Para módulo novo ou mudança estrutural: **abra RFC em PR** modificando apenas `PLAN.md` e/ou `ESCOPO.md`. Discussão e aprovação acontecem no PR antes de escrever conteúdo.

### Conteúdo novo (módulo, projeto, exercício)

Todo módulo deve ter (PLAN item 18):

1. Front-matter com objetivo de aprendizagem mensurável (ligado a item do harness).
2. Conteúdo principal em seções ricas (não tudo dentro de tópicos expansíveis).
3. ≥6 sub-tópicos expansíveis com 3 subsessões INEMA cada ("O que é" / "Por que aprender" / "Conceitos-chave").
4. ≥3 ilustrações de tipos diferentes (Mermaid diagrama, comparação visual, tabela de decisão).
5. Exemplo de código mínimo executável (provider-neutral, com adaptadores linkados).
6. Exercício hands-on com teste automatizado em `pytest`.
7. Bibliografia datada com ≥3 referências.
8. Seção "Quando NÃO usar".

Tamanho-alvo: **2.500-4.500 palavras** (60-105 min totais com lab). CI bloqueia fora do range.

### fec_sdk e scripts

- `ruff` para lint Python; `pytest` para testes.
- Sandbox de tools (PLAN item 62a): qualquer mudança em `fec_sdk/sandbox/` precisa atualizar `tests/sandbox/test_traversal.py`.
- CODEOWNERS protege arquivos críticos — espere review de maintainer.

## Fluxo de PR

1. **Branch** a partir de `main`.
2. **PR pequenos** preferíveis. Modulo novo cabe em PR único; refatoração ampla, divida.
3. **CI tem que estar verde:**
   - `ci-fast.yml` (validate, lint-content, sandbox tests, gitleaks, freeze-evals, budgets) — bloqueante.
   - `ci-scheduled.yml` (axe, visual diff, link external) — verde antes do merge para conteúdo final.
4. **Sem `--no-verify` em commits.** Se hook falha, descubra a causa.
5. **Sem `--force-push` em PRs já em review.**

## Estilo

- **PT-BR** em todo conteúdo público. Comentários técnicos podem ser EN se citarem termos consagrados.
- **Sem hype:** veja "Política anti-hype" em `ESCOPO.md`. Termos banidos: "definitivo", "tudo o que você precisa", "10x developer".
- **Citação obrigatória** para toda alegação de ganho: paper datado OU run no harness (`evals/v1/runs/<id>`).

## Manifestos canônicos vs Markdown gerado

- `evals/v1/*.json` é a **fonte de verdade**. Edite o JSON, não o MD.
- Markdowns como `COMPAT.md`, `MODELOS.md`, `CAPACIDADES.md` têm header "_⚠️ Gerado de `<arquivo>.json`. NÃO edite manualmente._" — pre-commit hook regenera; CI valida `git diff --quiet` após render.

## Licenças aceitas em contribuições

Ao abrir PR, você concorda em licenciar:

- **Conteúdo** (texto, imagens, slides): CC BY-SA 4.0.
- **Código** (exemplos, exercícios, scripts): MIT.
- Conteúdo de terceiros DEVE entrar no manifesto `LICENSES-THIRD-PARTY.md` com fonte e licença compatível. CI bloqueia fixture sem entrada no manifesto.

## Code of Conduct

Curso colaborativo, vibe técnica e respeitosa. Sem ataques pessoais, sem hype vazio, foco no conteúdo. Quem viola é avisado uma vez e depois removido. Reportar comportamento problemático: `conduct@inema.club`.

## Precisando de ajuda?

- Issue com label `duvida`.
- Discord do INEMA: <https://inema.club> (canal `#fec`).

---

**Maintainers triam PRs e issues semanalmente.** Espere até ~7 dias para retorno em PR não-trivial.
