"""Network policy para sandbox: egress negado por default; opt-in por host/porta.

Para uso real em runtime, monkey-patch `socket` e `httpx`/`requests` clients
para checar contra `NetworkPolicy`. Este módulo expõe a política — a aplicação
acontece em `tools/` específicos do lab.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field

from fec_sdk.errors import SandboxViolation


@dataclass(frozen=True)
class AllowedHost:
    """Entrada na allowlist."""
    host: str
    ports: frozenset[int] = field(default_factory=frozenset)


@dataclass
class NetworkPolicy:
    """Política. Default: deny-all egress; opt-in pela `allow()`."""

    allowlist: list[AllowedHost] = field(default_factory=list)
    allow_localhost: bool = False

    def allow(self, host: str, *ports: int) -> "NetworkPolicy":
        self.allowlist.append(AllowedHost(host=host, ports=frozenset(ports)))
        return self

    def check(self, host: str, port: int) -> None:
        if self.allow_localhost and host in {"127.0.0.1", "::1", "localhost"}:
            return
        for entry in self.allowlist:
            if entry.host == host and (not entry.ports or port in entry.ports):
                return
        raise SandboxViolation(
            f"Network egress denied: {host}:{port} not in allowlist",
            kind="network",
        )

    # Helper para integrar com socket.getaddrinfo monkeypatch (opcional).
    def install_socket_guard(self) -> None:
        original = socket.getaddrinfo

        def guarded(host: str | None, port: int | None, *args, **kwargs):  # type: ignore[no-untyped-def]
            if host is not None and port is not None:
                self.check(host, port)
            return original(host, port, *args, **kwargs)

        socket.getaddrinfo = guarded  # type: ignore[assignment]
