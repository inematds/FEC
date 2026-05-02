"""FEC SDK — cliente provider-neutral para a Formação de Engenharia de Contexto.

Importar este pacote NÃO faz I/O com a internet por default. `check_compat()`
faz o lookup remoto de revogação, mas é chamado apenas quando o usuário
executa código (em laboratórios e exemplos).
"""

from __future__ import annotations

__version__ = "1.0.0"

from fec_sdk.check_compat import (
    IncompatibleVersionError,
    RevokedVersionError,
    check_compat,
)
from fec_sdk.errors import FECSDKError, ProviderError
from fec_sdk.messages import Message, MessageRole, Tool, ToolCall, ToolResult

__all__ = [
    "Message",
    "MessageRole",
    "Tool",
    "ToolCall",
    "ToolResult",
    "FECSDKError",
    "ProviderError",
    "IncompatibleVersionError",
    "RevokedVersionError",
    "check_compat",
    "selftest",
    "__version__",
]


def selftest() -> dict[str, str]:
    """Smoke mínimo invocado por synthetic-check pós-publicação no PyPI.

    Não chama provedores; apenas valida que o pacote carrega e que o sandbox
    inicializa. Retorna dict simples para fácil parsing em CI.
    """
    from fec_sdk.sandbox import FilesystemSandbox

    with FilesystemSandbox() as fs:
        fs.write_text("ok.txt", "ok")
        content = fs.read_text("ok.txt")

    return {
        "version": __version__,
        "sandbox": "ok" if content == "ok" else "fail",
        "import": "ok",
    }
