# Runbook — Zenodo mirror offline

## Sintomas

- Alerta `ZENODO-DOWN-AT-RELEASE` durante `release.yml`.
- DOI não resolve.
- Synthetic monitor reportando Zenodo 5xx.

## Severidade

**SEV-2.** Zenodo é mirror para arquivamento durável (DOI), não canal primário. GitHub Release é canal primário.

## Procedimento

### Durante release ativo (Zenodo cai antes do upload)

1. **NÃO bloqueie o release principal.** GitHub Release publica primeiro com `continue-on-error: true` no job `zenodo-mirror`.
2. **Anote em `BUDGETS-EXCEPTIONS.md`** ou diretamente em CHANGELOG.md: "Zenodo mirror adiado para vYYY/Z devido a outage em <data>".
3. **Quando Zenodo voltar:** reexecute o workflow `zenodo-mirror` standalone via `workflow_dispatch` com mesma versão.
   - Idempotency key garante que não duplica depósito.
   - sha256 do zip deve bater com `CHECKSUMS.txt` do Release.

### Pós-release (DOI antigo não resolve)

1. **Não delete depósitos no Zenodo** — não é possível (intencional).
2. **Use "Versions" do Zenodo** se precisar substituir: novo depósito com `IsNewVersionOf` apontando ao DOI quebrado.
3. Atualize links se possível.

## Comunicação

- README/docs apontam para GitHub Release como canal canônico.
- Aviso explícito em `RUNBOOK.md` sobre fallback.
- Se DOI publicado em paper acadêmico, usuário deve contatar maintainers.

## Prevenção

- Zenodo é fallback, não primário (PLAN item 49).
- `release.yml` `continue-on-error` em job Zenodo evita bloquear release principal.
- Auditoria mensal de DOIs ativos via synthetic monitor.
