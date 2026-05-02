# SBOM — Software Bill of Materials

> _Gerado por release. Caminho canônico em `releases/v<X.Y.Z>/sbom.spdx.json` (SPDX 2.3) ou `sbom.cyclonedx.json`._

## Política

- Cada release publica um SBOM machine-readable em SPDX ou CycloneDX.
- Geração via `scripts/build-sbom.sh` (a implementar) usando `syft`/`pip-licenses`/equivalente.
- Anexado à GitHub Release como asset.
- Verificado no synthetic monitor pós-release.

## Componentes do `fec_sdk` (v1.0.0)

Dependências runtime (de `pyproject.toml`):

| Componente | Versão | Licença | Origem |
|-----------|--------|---------|--------|
| httpx | >=0.27,<1 | BSD-3-Clause | https://github.com/encode/httpx |
| pydantic | >=2.7,<3 | MIT | https://github.com/pydantic/pydantic |
| tenacity | >=8.5,<10 | Apache-2.0 | https://github.com/jd/tenacity |

Optional extras:

| Extra | Componente | Versão | Licença |
|-------|-----------|--------|---------|
| anthropic | anthropic | >=0.40,<1 | MIT |
| openai | openai | >=1.50,<2 | Apache-2.0 |
| google | google-generativeai | >=0.8,<1 | Apache-2.0 |
| ollama | ollama | >=0.5,<1 | MIT |

## Componentes do build pipeline (não vão para usuário final)

| Componente | Versão | Licença |
|-----------|--------|---------|
| @mermaid-js/mermaid-cli | 11.4.2 | MIT |
| @playwright/test | 1.49.0 | Apache-2.0 |
| @axe-core/playwright | 4.10.0 | MPL-2.0 |
| tailwindcss | 3.4.17 | MIT |
| dompurify | 3.2.3 | MPL-2.0 / Apache-2.0 |
| svgo | 3.3.2 | MIT |

## Licenças no agregado

- Conteúdo do curso: **CC BY-SA 4.0**.
- Código (fec_sdk, scripts, exemplos, exercícios): **MIT**.
- Dependências runtime: **MIT, BSD-3-Clause, Apache-2.0** — todas compatíveis com MIT.
- Dependências dev/build: variadas; não vão para usuário.

## Verificação

`scripts/audit-licenses.py` percorre dependências resolvidas no lockfile e flagra licenças não listadas aqui ou incompatíveis.

## CVE / advisory

- Dependabot habilitado.
- Auditoria mensal de `pip-audit` / `npm audit`.
- Vulnerabilidades altas/críticas seguem `runbooks/dependency-cve.md`.
