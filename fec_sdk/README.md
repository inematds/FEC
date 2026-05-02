# fec-sdk

Cliente provider-neutral da [Formação de Engenharia de Contexto (FEC)](https://github.com/inematds/FEC).

## Instalação

```bash
pip install fec-sdk
# com providers específicos:
pip install 'fec-sdk[anthropic]'
pip install 'fec-sdk[openai]'
pip install 'fec-sdk[ollama]'
pip install 'fec-sdk[all]'
```

Em laboratórios do curso, use o lockfile da release para garantir reprodutibilidade:

```bash
pip install --require-hashes -r releases/v1.0.0/lockfile.toml
```

## Uso mínimo

```python
from fec_sdk import Message, MessageRole, check_compat
from fec_sdk.adapters import get_adapter

# Verifica compatibilidade do ambiente com o módulo atual
check_compat("modulo-3-2", expected_sdk_version=">=1.0,<2.0")

# Cliente provider-neutral
client = get_adapter("anthropic", model="claude-sonnet-4-6")

resp = client.chat([
    Message(role=MessageRole.SYSTEM, content="Você é um assistente conciso."),
    Message(role=MessageRole.USER, content="O que é 'lost in the middle'?"),
])

print(resp.content)
print(f"tokens: in={resp.input_tokens} out={resp.output_tokens}")
```

## Sandbox

```python
from fec_sdk.sandbox import FilesystemSandbox

with FilesystemSandbox() as fs:
    fs.write_text("note.txt", "olá")
    print(fs.read_text("note.txt"))
# diretório limpo automaticamente ao sair
```

## Selftest (sem rede)

```python
from fec_sdk import selftest
print(selftest())  # {'version': '1.0.0', 'sandbox': 'ok', 'import': 'ok'}
```

## Política

- **Determinístico por default:** `temperature=0`, sem seed implícita.
- **Sem I/O na importação** (exceto `check_compat()` quando explicitamente chamado).
- **Erros tipados** (`ProviderError`, `SandboxViolation`, `RevokedVersionError`, `IncompatibleVersionError`) — não exceções genéricas.

Licença: MIT (ver [LICENSE-CODE](../LICENSE-CODE)).
