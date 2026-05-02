# COMPAT-RETIRED — Combinações de compatibilidade aposentadas

> _Quando uma combinação `course × fec_sdk × python × provedor` sai de `compat.json` para abrir espaço, ela vem para cá com data e motivo. PLAN item 83._

## Política

- Janela de suporte ativa: 2 releases × 2 minors `fec_sdk` × 2 minors SDK provedor × 2 minors Python.
- Ao mover combinação para fora do `core_combinations` ou `extended_combinations`, **PR explícito** atualiza `evals/v1/compat.json` E adiciona entrada aqui com:
  - data de aposentadoria
  - motivo (versão muito antiga / provedor deprecou / janela de suporte rolou)
  - última versão de `fec_sdk` que ainda funcionou nessa combo (testada)

## Aposentadoria registrada

_(Vazio na v1.0.0 — primeiras aposentadorias virão na v1.1+ quando rolarmos a janela.)_

## Exemplo de entrada futura

```markdown
### Python 3.10 × fec-sdk 1.0.x × anthropic 0.40

- **Aposentado em:** 2027-01-15
- **Motivo:** Python 3.10 saiu da janela de suporte ativa quando a v1.2.0 do curso passou a focar em 3.12/3.13.
- **Última versão suportada:** fec-sdk 1.1.3.
- **Workaround para alunos com Python 3.10:** continuar com fec-sdk 1.1.3 (lockfile da v1.1.x), OU upgrade para Python 3.12.
```
