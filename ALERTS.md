# ALERTS — Mapeamento métrica → severidade → ação

> _⚠️ **Gerado de `evals/v1/alerts.json`.** NÃO edite manualmente — mudanças no MD são sobrescritas. Edite o JSON via PR (CODEOWNERS protege)._

Consumido pelo `dashboard.py` e pelos runbooks.

| ID | Métrica | Condição | Sev | Owner | Ação | Runbook |
|-----|---------|----------|-----|-------|------|---------|
| `AUTO-SMOKE-FAIL-2D` | `auto_smoke.consecutive_failures` | >=2 consecutive scheduled runs failing | **SEV-2** | on-call-primary | Diagnose with runbooks/smoke-failure.md within 24h business hours. | [runbooks/smoke-failure.md](./runbooks/smoke-failure.md) |
| `AUTO-SMOKE-MISSED` | `auto_smoke.last_run_age_hours` | >26h without a scheduled run (workflow silently disabled) | **SEV-2** | on-call-primary | Re-enable workflow and investigate. | [runbooks/smoke-failure.md](./runbooks/smoke-failure.md) |
| `GITLEAKS-MAINTAINER-PR` | `gitleaks.blocked_in_maintainer_pr` | Any block in CI-fast on a maintainer PR | **SEV-1** | security | Immediate key rotation + audit. Use BREAK-GLASS.md if needed. | [runbooks/secret-exposure.md](./runbooks/secret-exposure.md) |
| `BUDGET-80` | `budget.monthly_used_pct` | >80% and <100% | **SEV-3** | maintainer | Warning + Check Run neutral. Investigate cost spike. | [runbooks/smoke-failure.md](./runbooks/smoke-failure.md) |
| `BUDGET-100` | `budget.monthly_used_pct` | >=100% | **SEV-2** | maintainer | Provider native cap engaged. Bot opens kill-switch PR. Promotion blocked. | [runbooks/smoke-failure.md](./runbooks/smoke-failure.md) |
| `ZENODO-DOWN-AT-RELEASE` | `synthetic.zenodo_status` | Zenodo unreachable during release publication | **SEV-2** | maintainer | Publish GitHub Release first; retry Zenodo when available; checksums must still match. | [runbooks/zenodo-down.md](./runbooks/zenodo-down.md) |
| `PYPI-INSTALL-FAIL` | `synthetic.pypi_install` | 3 consecutive failures of pip install --require-hashes in clean venv | **SEV-1** | on-call-primary | Canonical install path broken. Check checksum revocation list and PyPI metadata. | [runbooks/pypi-down.md](./runbooks/pypi-down.md) |
| `PAGES-CHECKSUM-DRIFT` | `synthetic.pages_checksum_match` | Served HTML sha256 differs from pages-checksums.txt | **SEV-1** | on-call-primary | Drift on immutable versioned path. Investigate deployment integrity. | [runbooks/pages-down.md](./runbooks/pages-down.md) |
| `ERRATA-SEV1-MISSED` | `errata.sev1_response_age_hours` | >2h within release-window OR >8h business-hours outside window | **SEV-1** | on-call-secondary | Escalate to secondary on-call. | [runbooks/bad-release.md](./runbooks/bad-release.md) |
| `KILLSWITCH-AGE` | `killswitch.age_hours_without_expected_off_until` | >48h enabled without expected_off_until | **SEV-2** | maintainer | Resolve underlying issue or document expected_off_until. | [runbooks/smoke-failure.md](./runbooks/smoke-failure.md) |
