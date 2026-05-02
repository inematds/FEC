# Pré-requisitos — Formação de Engenharia de Contexto

Antes de começar, confirme que você tem:

## Conhecimento

- [ ] Já chamou uma API LLM via HTTP ou SDK (Anthropic, OpenAI, ou similar) ao menos uma vez.
- [ ] Lê e escreve **Python intermediário**: classes, decorators, async/await, type hints, `pytest`.
- [ ] Conhece **JSON Schema** o suficiente para entender uma definição com `properties`, `required`, `oneOf`.
- [ ] Sabe usar `git`/GitHub: branch, PR, code review.
- [ ] Confortável em terminal Linux/macOS (ou WSL).

## Acesso a provedores (≥1, ideal: 2)

- [ ] Conta em **pelo menos 1 provedor LLM** (Anthropic, OpenAI, Google AI Studio, ou similar) com chave de API ativa.
- [ ] Idealmente uma segunda — facilita os módulos que comparam comportamento provider-neutral.
- [ ] **Sem orçamento?** Cada módulo tem caminho com **OSS local (Ollama)** marcado com badge "rodável grátis" — ver `OLLAMA-MATRIZ.md`. Quando OSS não cobre o lab, há **simulação por gravação** em `fixtures/recorded/`.

## Hardware

| Caminho | RAM mínima | GPU | Disco |
|---------|-----------|-----|-------|
| **Cloud-only (API paga)** | 8 GB | qualquer | 5 GB |
| **OSS local — modelos pequenos (≤7B)** | 16 GB | opcional (CPU funciona, mais lento) | 20 GB |
| **OSS local — modelos médios (8-13B)** | 24 GB OU GPU 8 GB+ | opcional | 30 GB |
| **OSS local — modelos grandes (>13B) ou multi-agente** | 32 GB OU GPU 24 GB+ | recomendado | 50 GB |

Detalhes por lab em [`OLLAMA-MATRIZ.md`](./OLLAMA-MATRIZ.md).

## Software

- **Python 3.11 ou 3.12** (versões testadas — ver [`COMPAT.md`](./COMPAT.md)).
- **Git** ≥2.30.
- **Node.js** ≥20 (apenas para construir os assets locais — Tailwind, Mermaid CLI; alunos que só consomem o conteúdo não precisam).
- **Ollama** ≥0.5 (apenas se for usar caminho OSS).
- **Editor** com suporte a Python (VS Code, PyCharm, etc.).

## Tempo

A FEC v1.0 tem **10 módulos GA + 4 beta + 3 projetos cumulativos**.

| Carga | Estimativa |
|-------|-----------|
| Por módulo | 60-105 min (leitura ~25-45 min + lab 30-60 min) |
| Trilha completa | ~6-10 h |
| Projetos GA (P1, P2, P5) | 4-8 h cada |
| Curso completo (todos GA) | **~80-120 h** distribuídos no seu ritmo |

---

## Não preenche os pré-requisitos?

Sem problema — comece por:

- **Python intermediário:** [Real Python — Intermediate Quickstart](https://realpython.com/learning-paths/python-3-introduction/) ou *Fluent Python* (Luciano Ramalho).
- **APIs LLM básicas:** quickstart oficial do provedor que você escolher (Anthropic, OpenAI, Google AI).
- **JSON Schema:** [json-schema.org/learn](https://json-schema.org/learn/).

Quando tiver familiaridade básica, volte e siga a Trilha 1.

---

## Checagem de prontidão (5 min)

Em terminal, rode:

```bash
python --version          # esperar 3.11.x ou 3.12.x
pip --version
git --version
node --version            # opcional, ≥20 se for buildar assets

# Quando o fec_sdk estiver publicado:
# pip install fec-sdk==<release>
# python -c "from fec_sdk import selftest; selftest()"
```

Tudo verde? Você está pronto. Vá para [README.md → Comece aqui](./README.md#comece-aqui).
