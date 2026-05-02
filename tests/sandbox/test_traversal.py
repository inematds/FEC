"""Bateria de traversal/exfiltração — PLAN item 62a.

Estes testes são GATE DE GA. Falha aqui bloqueia merge no projeto/módulo afetado.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from fec_sdk.errors import SandboxViolation
from fec_sdk.sandbox import FilesystemSandbox, NetworkPolicy


# ---------- filesystem ------------------------------------------------------

class TestFilesystemTraversal:
    def test_absolute_path_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation, match="Absolute path"):
                fs.write_text("/etc/passwd", "x")

    def test_dotdot_segment_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation, match="traversal"):
                fs.write_text("../../etc/passwd", "x")

    def test_double_slash_dotdot_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation, match="traversal"):
                fs.write_text("..//..//.env", "secret")

    def test_dotdot_in_middle_segment_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation, match="traversal"):
                fs.write_text("a/../../etc/passwd", "x")

    def test_aws_credentials_path_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation):
                fs.read_text(os.path.expanduser("~/.aws/credentials"))

    def test_dotenv_at_root_blocked(self) -> None:
        with FilesystemSandbox() as fs:
            # `.env` é absoluto se passado com /; relativo é OK *desde que* extensão permita
            with pytest.raises(SandboxViolation):
                fs.write_text("/.env", "SECRET=1")

    def test_symlink_pointing_outside_blocked(self, tmp_path: Path) -> None:
        # Cria symlink antes do sandbox
        outside = tmp_path / "outside.txt"
        outside.write_text("secret")

        with FilesystemSandbox() as fs:
            link_target = fs.root / "link.txt"
            link_target.symlink_to(outside)

            with pytest.raises(SandboxViolation, match="Symlink"):
                fs.read_text("link.txt")

    def test_extension_allowlist(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation, match="Extension"):
                fs.write_text("malware.exe", "MZ")

    def test_file_size_cap(self) -> None:
        with FilesystemSandbox(max_file_bytes=100) as fs:
            with pytest.raises(SandboxViolation, match="too large"):
                fs.write_text("big.txt", "x" * 200)

    def test_session_size_cap(self) -> None:
        with FilesystemSandbox(max_file_bytes=10_000, max_session_bytes=100) as fs:
            fs.write_text("a.txt", "x" * 60)
            with pytest.raises(SandboxViolation, match="Session"):
                fs.write_text("b.txt", "x" * 60)

    def test_legitimate_use_works(self) -> None:
        with FilesystemSandbox() as fs:
            fs.write_text("note.md", "# título\n\nconteúdo")
            assert fs.read_text("note.md").startswith("# título")
            assert fs.exists("note.md")
            assert "note.md" in fs.list_dir(".")

    def test_subdir_allowed(self) -> None:
        with FilesystemSandbox() as fs:
            fs.write_text("data/notes/a.md", "x")
            assert fs.exists("data/notes/a.md")

    def test_cleanup_on_exit(self) -> None:
        with FilesystemSandbox() as fs:
            captured = fs.root
            fs.write_text("a.txt", "x")
            assert captured.exists()
        assert not captured.exists()

    def test_root_escape_via_normalization(self) -> None:
        with FilesystemSandbox() as fs:
            with pytest.raises(SandboxViolation):
                fs.write_text("ok/../../escape.txt", "x")


# ---------- network ---------------------------------------------------------

class TestNetworkPolicy:
    def test_default_deny_all(self) -> None:
        pol = NetworkPolicy()
        with pytest.raises(SandboxViolation, match="Network egress"):
            pol.check("api.evil.com", 443)

    def test_allowlist_specific_host(self) -> None:
        pol = NetworkPolicy().allow("api.anthropic.com", 443)
        pol.check("api.anthropic.com", 443)  # nada lança

    def test_allowlist_wrong_port(self) -> None:
        pol = NetworkPolicy().allow("api.anthropic.com", 443)
        with pytest.raises(SandboxViolation):
            pol.check("api.anthropic.com", 8080)

    def test_localhost_off_by_default(self) -> None:
        pol = NetworkPolicy()
        with pytest.raises(SandboxViolation):
            pol.check("127.0.0.1", 11434)

    def test_localhost_opt_in(self) -> None:
        pol = NetworkPolicy(allow_localhost=True)
        pol.check("localhost", 11434)
        pol.check("127.0.0.1", 11434)
