"""Filesystem sandbox jailed (PLAN item 62a).

Defesas:
- root jailed em tempdir (`tempfile.mkdtemp`).
- deny absolute paths.
- deny `..` em qualquer segmento.
- deny symlinks (resolve antes de abrir e compara).
- cap de tamanho por arquivo (1 MB default) e por sessão (50 MB default).
- allowlist de extensões.

Tools que tocam filesystem DEVEM rodar dentro de uma instância de
`FilesystemSandbox`. Bateria `tests/sandbox/test_traversal.py` é gate de GA.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from types import TracebackType
from typing import Iterable

from fec_sdk.errors import SandboxViolation

DEFAULT_ALLOWED_EXTENSIONS: frozenset[str] = frozenset({
    ".txt", ".md", ".json", ".yaml", ".yml", ".csv", ".tsv", ".html", ".xml",
    ".py", ".js", ".log",
})

DEFAULT_MAX_FILE_BYTES = 1 * 1024 * 1024       # 1 MiB
DEFAULT_MAX_SESSION_BYTES = 50 * 1024 * 1024   # 50 MiB


class FilesystemSandbox:
    """Context manager que cria root jailed em tempdir e cleanup ao sair.

    Exemplo:
        >>> with FilesystemSandbox() as fs:
        ...     fs.write_text("note.txt", "hello")
        ...     fs.read_text("note.txt")
        'hello'
    """

    def __init__(
        self,
        *,
        prefix: str = "fec-sandbox-",
        max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
        max_session_bytes: int = DEFAULT_MAX_SESSION_BYTES,
        allowed_extensions: Iterable[str] = DEFAULT_ALLOWED_EXTENSIONS,
    ) -> None:
        self._prefix = prefix
        self._root: Path | None = None
        self._max_file_bytes = max_file_bytes
        self._max_session_bytes = max_session_bytes
        self._allowed_extensions = frozenset(allowed_extensions)
        self._bytes_written = 0

    # -- context manager --------------------------------------------------

    def __enter__(self) -> FilesystemSandbox:
        self._root = Path(tempfile.mkdtemp(prefix=self._prefix)).resolve(strict=True)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._root and self._root.exists():
            shutil.rmtree(self._root, ignore_errors=True)
        self._root = None

    # -- safety checks ----------------------------------------------------

    @property
    def root(self) -> Path:
        if self._root is None:
            raise SandboxViolation("Sandbox not entered (use 'with FilesystemSandbox() as fs:').", kind="lifecycle")
        return self._root

    def _safe_path(self, raw: str | os.PathLike[str]) -> Path:
        p = os.fspath(raw)
        if os.path.isabs(p):
            raise SandboxViolation(f"Absolute path forbidden: {p!r}", kind="absolute-path")
        # `..` em qualquer segmento (mesmo isolado, mesmo após normalização parcial)
        norm = os.path.normpath(p)
        if norm.startswith(".."):
            raise SandboxViolation(f"Path traversal forbidden: {p!r}", kind="path-traversal")
        for part in Path(p).parts:
            if part == "..":
                raise SandboxViolation(f"Path traversal forbidden in segment: {p!r}", kind="path-traversal")

        # construção sem resolução para checar symlink primeiro
        full_unresolved = self.root / p

        # symlink check em qualquer parte do caminho (incluindo o alvo) ANTES de resolve
        cur = full_unresolved
        while True:
            if cur.is_symlink():
                raise SandboxViolation(f"Symlink forbidden: {cur!r}", kind="symlink")
            if cur == self.root or cur.parent == cur:
                break
            cur = cur.parent

        # confina dentro do root mesmo após resolução
        full = full_unresolved.resolve(strict=False)
        try:
            full.relative_to(self.root.resolve(strict=True))
        except ValueError as exc:
            raise SandboxViolation(f"Path escapes sandbox root: {p!r}", kind="root-escape") from exc

        return full

    def _check_extension(self, path: Path) -> None:
        if path.suffix.lower() not in self._allowed_extensions:
            raise SandboxViolation(
                f"Extension {path.suffix!r} not in allowlist {sorted(self._allowed_extensions)}",
                kind="extension",
            )

    def _check_size(self, n_bytes: int) -> None:
        if n_bytes > self._max_file_bytes:
            raise SandboxViolation(
                f"File too large: {n_bytes} > {self._max_file_bytes}",
                kind="file-size",
            )
        if self._bytes_written + n_bytes > self._max_session_bytes:
            raise SandboxViolation(
                f"Session size cap exceeded: {self._bytes_written + n_bytes} > {self._max_session_bytes}",
                kind="session-size",
            )

    # -- public IO --------------------------------------------------------

    def write_text(self, rel_path: str, content: str) -> Path:
        full = self._safe_path(rel_path)
        self._check_extension(full)
        encoded = content.encode("utf-8")
        self._check_size(len(encoded))
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(encoded)
        self._bytes_written += len(encoded)
        return full

    def read_text(self, rel_path: str) -> str:
        full = self._safe_path(rel_path)
        self._check_extension(full)
        if full.stat().st_size > self._max_file_bytes:
            raise SandboxViolation(
                f"Refusing to read oversized file: {full.stat().st_size} > {self._max_file_bytes}",
                kind="file-size",
            )
        return full.read_text(encoding="utf-8")

    def list_dir(self, rel_path: str = ".") -> list[str]:
        full = self._safe_path(rel_path)
        if not full.is_dir():
            raise SandboxViolation(f"Not a directory: {rel_path!r}", kind="not-dir")
        return sorted(p.name for p in full.iterdir())

    def exists(self, rel_path: str) -> bool:
        try:
            return self._safe_path(rel_path).exists()
        except SandboxViolation:
            return False
