"""Sandbox jailed para tools — PLAN item 62a.

Filesystem: root em tempdir; deny absolute paths, `..`, symlinks; cap de tamanho.
Network: egress negado por default; opt-in por host/porta.
Process: helpers explícitos, sem subprocess direto.

Bateria de testes em `tests/sandbox/test_traversal.py` é gate de GA.
"""

from fec_sdk.sandbox.filesystem import FilesystemSandbox
from fec_sdk.sandbox.network import NetworkPolicy

__all__ = ["FilesystemSandbox", "NetworkPolicy"]
