# LICENSES-THIRD-PARTY — Manifesto de licenças de terceiros

> _CI bloqueia inclusão de fixture/screenshot/diagrama-base sem entrada aqui. PLAN item 44._

## Política

Todo conteúdo de terceiros incluído ou referenciado tem:

1. **Entrada neste arquivo** com fonte, licença, e uso permitido.
2. **Atribuição** no contexto onde aparece (legenda da figura, footnote, etc.).
3. **Licença compatível** com o resto do projeto (CC BY, CC BY-SA, MIT, Apache, domínio público, ou similar).

CI verifica: cada arquivo em `fixtures/` deve ter entrada aqui. Se não tem, falha.

## Fixtures

| Caminho | Fonte | Licença | Uso permitido | Atribuição em |
|---------|-------|---------|---------------|---------------|
| _(vazio — primeiros datasets serão adicionados em T3)_ | | | | |

### Datasets planejados

#### `fixtures/arxiv-cs-100/`
- **Fonte:** ArXiv (cs.LG / cs.CL abstracts).
- **Licença:** ArXiv abstracts são de domínio público para uso não-comercial / educacional sob fair use; texto integral varia. Manter apenas abstracts e metadados (título, autores, ID, ano).
- **Uso permitido:** RAG, indexação, eval — uso educacional não-comercial.
- **Atribuição:** "Dataset construído a partir de abstracts do ArXiv (arxiv.org), uso educacional. IDs originais preservados em `metadata.json`."

## Diagramas / SVGs

Diagramas em `assets/diagrams/` são originais ou derivados. Sem importar SVGs de terceiros sem entrada aqui.

| Arquivo | Fonte | Licença | Uso |
|---------|-------|---------|-----|
| `assets/diagrams/janela-contexto.dark.svg` | Original FEC (Mermaid render) | CC BY-SA 4.0 | — |
| `assets/diagrams/lost-in-the-middle.dark.svg` | Original FEC (inspirado em Liu et al. 2023, mas redesenhado) | CC BY-SA 4.0 | — |

## Screenshots / imagens raster

Evitamos screenshots de produtos de terceiros para reduzir superfície de licença. Quando inevitável:

| Arquivo | Origem | Licença / autorização | Atribuição |
|---------|--------|----------------------|-----------|
| _(vazio)_ | | | |

## Snippets de código importados

Código importado (ex.: utility de outro repo OSS) entra com licença + comentário de origem.

| Arquivo | Origem | Licença | Modificações |
|---------|--------|---------|--------------|
| _(vazio até importarmos algo)_ | | | |

## Papers citados (apenas link, não conteúdo)

ArXiv abstracts e DOIs em `bibliografia/T<n>.md` são links — não copiamos texto. Citação não exige entrada aqui (é fair use academic).

## Auditoria

`scripts/audit-licenses.py` (a implementar) percorre `fixtures/`, `assets/`, e checa que cada arquivo está listado aqui. Falha bloqueia release.

## Reportar uso indevido

Se você é detentor de direitos e identificou uso sem licença adequada: ver `runbooks/dataset-license-violation.md` e contate `security@inema.club`.
