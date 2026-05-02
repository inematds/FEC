# SECURITY-SANDBOX — Modelo de ameaça do sandbox de tools

> _Detalha o sandbox em `fec_sdk/sandbox/`. PLAN item 62a._

## Escopo do sandbox

Tools que executam código por instrução do modelo (filesystem, processo, rede) DEVEM rodar dentro de uma `FilesystemSandbox` e/ou consultar `NetworkPolicy`. Aplica-se a:

- P2 — Agente com tools.
- P5 — Pipeline em produção.
- Qualquer lab nas trilhas T4 que tenha tool com side-effect.

## Defesas implementadas

### Filesystem (`fec_sdk/sandbox/filesystem.py`)

- **Root jailed em `tempfile.mkdtemp()`** — sandbox por sessão, cleanup automático no `__exit__`.
- **Deny absolute paths** — `/etc/passwd` rejeitado.
- **Deny `..` em qualquer segmento** — incluindo `..//..//.env`.
- **Deny symlinks** — checados antes de `resolve()` para não vazar caminho.
- **Cap de tamanho** — default 1 MB por arquivo, 50 MB por sessão.
- **Allowlist de extensões** — `.txt`, `.md`, `.json`, `.yaml`, `.csv`, `.py`, etc.

### Network (`fec_sdk/sandbox/network.py`)

- **Egress negado por default** — `NetworkPolicy()` é deny-all.
- **Opt-in por host:porta** — `pol.allow("api.anthropic.com", 443)`.
- **Localhost só com flag explícita** — `NetworkPolicy(allow_localhost=True)`.

### Tests obrigatórios

`tests/sandbox/test_traversal.py` — bateria de **19 testes** cobrindo:
- absolute path
- `..` em vários formatos (`..//..//`, `a/../../`)
- `~/.aws/credentials`
- `.env` na raiz
- symlink apontando para fora
- extension allowlist
- file size cap
- session size cap
- root escape via normalization
- network deny-all
- localhost opt-in

**Falha em qualquer um BLOQUEIA o módulo/projeto afetado de virar GA.**

## Superfície fora do escopo

O sandbox **não cobre**:

- **Novos tipos de side-effect** (GUI, periféricos, sockets unix custom). Quem adiciona, estende `fec_sdk/sandbox/` E adiciona testes.
- **Side-channels** — timing, espaço em disco fora do tempdir, etc.
- **Vulnerabilidade do próprio Python** — depende da segurança do interpretador.
- **`subprocess` direto** — não é exposto pelo sandbox; quem precisar (não devia) faz fora da sandbox e isso é red flag em review.

## Política

- Toda PR que adiciona tool com side-effect ATUALIZA `tests/sandbox/test_traversal.py` com casos novos.
- CODEOWNERS protege `fec_sdk/sandbox/` — review de maintainer obrigatório.
- Auditoria de segurança trimestral revisita esta superfície.

## Reportar vulnerabilidade

Use o canal em [`SECURITY.md`](./SECURITY.md). NÃO abra issue público antes de patched release + GHSA.
