# HOSTING-DECISION — Decisão de hospedagem da v1.0

## Decisão atual (v1.0)

**Hospedagem:** GitHub Pages.

**Justificativa:**

- Zero custo, alta disponibilidade.
- Deploy via `actions/deploy-pages` no `release.yml`.
- Branch protection + CODEOWNERS no `gh-pages` evita pushes diretos.
- Path versionado imutável `/v<X.Y.Z>/` (PLAN item 74a) garante "ship the same bits we tested".

## Limitação aceita

GitHub Pages **não suporta custom response headers**. Consequência:

- **CSP** é declarada via `<meta http-equiv="Content-Security-Policy">` na primeira tag dentro de `<head>`.
- `Strict-Transport-Security`, `X-Frame-Options` e `Referrer-Policy` reais não são possíveis (apenas `<meta name=referrer>` para o último).
- `audit-pages.py` valida CSP via parsing do HTML servido (string match contra `assets/csp/policy.txt`).

Esta limitação está dentro do escopo de risco aceito para v1.0. Documentada em `SECURITY.md`.

## Quando migrar (gatilho para v1.1+)

Migrar para **Cloudflare Pages** ou **Netlify** se qualquer dos seguintes for verdade:

- Auditoria de segurança externa exige headers reais (HSTS, X-Frame-Options).
- Monitor de subresource integrity (SRI) precisar de `Content-Security-Policy-Report-Only` em duplicata.
- Latência de Pages tornar-se problema (improvável; CDN do GitHub Pages é razoável).
- Necessidade de `_headers` file ou middleware (ex.: rate-limit em `/status/revoked.json`).

## Plano de migração (se acionado)

1. RFC + PR atualizando este documento.
2. Workflow paralelo `release-cloudflare.yml` que sobe os mesmos artefatos para Cloudflare Pages.
3. DNS: `inematds.github.io/FEC/v1.1.0/` permanece; novo CNAME `fec.inema.club` aponta para Cloudflare.
4. Synthetic monitor passa a checar headers reais.
5. Migração escalonada — Pages continua servindo versões antigas.

## Custos a considerar

- **Cloudflare Pages:** gratuito até 500 builds/mês; build determinístico no `release.yml` faz isso fácil.
- **Netlify:** gratuito até 100GB/mês; mais que suficiente.
- **Custom domain:** `fec.inema.club` ou similar; SSL automático.

## Quem decide

Decisão documentada via PR neste arquivo + 2 maintainers + 1 revisor externo (security).
