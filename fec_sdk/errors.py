"""Hierarquia de erros do fec_sdk."""

from __future__ import annotations


class FECSDKError(Exception):
    """Base de todos os erros do fec_sdk."""


class ProviderError(FECSDKError):
    """Falha em chamada a provedor externo (rede, auth, rate limit, etc.)."""

    def __init__(self, message: str, *, provider: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class SandboxViolation(FECSDKError):
    """Tool tentou operação fora do sandbox (path traversal, network, etc.)."""

    def __init__(self, message: str, *, kind: str) -> None:
        super().__init__(message)
        self.kind = kind  # "path-traversal", "absolute-path", "symlink", "size", "network", ...


class RevokedVersionError(FECSDKError):
    """fec_sdk atual está na lista de versões revogadas (manifesto local + remoto)."""

    def __init__(self, version: str, successor: str | None, advisory_url: str | None) -> None:
        msg = f"fec-sdk {version} foi revogada"
        if successor:
            msg += f"; atualize com: pip install -U fec-sdk=={successor}"
        if advisory_url:
            msg += f" (advisory: {advisory_url})"
        super().__init__(msg)
        self.version = version
        self.successor = successor
        self.advisory_url = advisory_url


class IncompatibleVersionError(FECSDKError):
    """Combinação (course × fec_sdk × python × provedor) não suportada na COMPAT.md."""

    def __init__(self, message: str, *, fix_hint: str | None = None) -> None:
        full = message + (f"\n\nCorreção sugerida: {fix_hint}" if fix_hint else "")
        super().__init__(full)
        self.fix_hint = fix_hint
