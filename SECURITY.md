# Política de Segurança — FEC

## Reportando vulnerabilidades

Encontrou vulnerabilidade no `fec_sdk`, em conteúdo do curso, no pipeline de release ou na infraestrutura?

**Não abra issue público.**

Use **GitHub Security Advisories**: <https://github.com/inematds/FEC/security/advisories/new>.

Como alternativa, e-mail para `security@inema.club` (chave pública em `SECURITY.asc` quando disponível).

### Resposta esperada

| Severidade | Janela | SLA |
|------------|--------|-----|
| **SEV-1** (secret vazado, malware, exfil real, XSS publicado, sandbox quebrado) | 14 dias pós-release (RC + GA + 7d) | ≤2h, primário+secundário 24/7 |
| SEV-1 (rotina) | fora da janela | mitigação automática ≤2h (revogação, banner, takedown) + resposta humana ≤8h em horário comercial BR / ≤4h fim-de-semana melhor-esforço |
| SEV-2 (técnica que invalida lab/benchmark) | qualquer | ≤24h em horário comercial BR |
| SEV-3 (errata, link, a11y individual) | qualquer | ≤7 dias úteis |

Detalhes em [`RUNBOOK.md`](./RUNBOOK.md) e [`RELEASE-INCIDENT.md`](./RELEASE-INCIDENT.md).

## Escopo

Cobrimos:

- Código do `fec_sdk` (incluindo sandbox de tools).
- Pipeline de CI/CD (workflows GitHub Actions).
- Conteúdo HTML publicado (XSS, CSP, sanitização).
- Pacotes publicados (PyPI, GitHub Release zip, Zenodo mirror).
- Manifestos canônicos (`evals/v1/*.json` e schemas).

NÃO cobrimos (out-of-scope mas relevante reportar):

- Bugs em LLMs de provedores (reportar ao provedor).
- Segurança de aplicações que ALUNOS construírem (responsabilidade do aluno).
- Vulnerabilidades em dependências third-party não usadas pelo `fec_sdk` (mas reporta no advisory original).

## Limitações declaradas honestamente

### Manifesto remoto de revogação

`fec_sdk.check_compat()` busca `https://inematds.github.io/FEC/v1/revoked.json` (assinado) ao iniciar para detectar versões revogadas em runtime.

**Limitação:** wheels já instalados que rodam **sem rede** ou com cache local de revogação ainda válido (TTL 24h) **não receberão revogações novas** até a próxima conexão.

**Defesas autoritativas (firmes):**
- `evals/v1/revoked_versions.json` (canônico em git, validado em CI).
- `releases/<v>/lockfile.toml` com `--require-hashes` em `pip install`.
- `audit-evals.py` no CI bloqueia release que aponta para versão revogada.
- Synthetic monitor diário verifica a integridade dos canais públicos.

O hard-fail em runtime via `RevokedVersionError` é uma **rede de segurança best-effort**, não garantia. Para garantia firme, mantenha `pip install` com lockfile e verifique antes de cada uso crítico.

### Manifesto remoto sob ataque DoS

Se atacante sequestrar `inematds.github.io/FEC/v1/revoked.json` e servir manifesto inválido (assinatura quebrada), `fec_sdk` ignora o cache remoto, loga warning, e usa **apenas** a baseline embutida no wheel — ou seja, atacante NÃO consegue bloquear todos os usuários ao quebrar Pages. Trade-off: revogações novas não chegam até atacante perder o controle.

### Sandbox de tools

`fec_sdk/sandbox/` impede traversal/exfiltração via filesystem/rede em cenários cobertos pela `tests/sandbox/test_traversal.py`. Sandbox **não é solução completa**: alunos que adicionam novos tipos de side-effect (ex.: GUI, peripherals) precisam estender o sandbox. Documentado em [`SECURITY-SANDBOX.md`](./SECURITY-SANDBOX.md).

### Prompt injection no conteúdo

`SAFETY-INJECTION.md` define modelo de ameaça sandboxed. Payloads ficam em fixtures testáveis, não em texto corrido — para que a página não vire "manual de ataque". Cobertura é educacional, não exaustiva.

## Disclosure responsável

- Damos **90 dias** entre o reporte e disclosure público (ou 7 dias após o fix se for liberado antes).
- Crédito ao reporter no `SECURITY-ADVISORY-<id>.md` (a menos que peça anonimato).
- Sem programa de bug bounty no momento.

## Auditoria

Você pode auditar o histórico de runs de eval em `evals/v1/runs/` (content-addressed por sha256). `audit-evals.py` é público e roda contra qualquer release.

GHSA + OSV advisories em <https://github.com/inematds/FEC/security/advisories>.
