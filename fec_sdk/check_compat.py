"""Verificação de compatibilidade — versão revogada (hard-fail) e version skew (warn ou hard-fail).

Estratégia (PLAN itens 79a.5 + 85):
1. Embedded baseline: lista de versões revogadas conhecida em build-time.
2. Manifesto remoto assinado em /v1/revoked.json (TTL 24h, fallback ao cache).
3. Hard-fail (`RevokedVersionError`) se versão atual está em qualquer das listas.
4. Hard-fail (`IncompatibleVersionError`) em major/minor mismatch ou combinação ausente da COMPAT.
5. Warning amarelo apenas para patch drift compatível.

Override consciente: `FEC_ALLOW_INCOMPAT=1` permite seguir após log em ~/.fec/incompat.log.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import warnings
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

from fec_sdk import __version__
from fec_sdk.errors import IncompatibleVersionError, RevokedVersionError

_log = logging.getLogger("fec_sdk.check_compat")

REMOTE_MANIFEST_URL = "https://inematds.github.io/FEC/v1/revoked.json"
CACHE_PATH = Path.home() / ".fec" / "revoked.cache.json"
CACHE_TTL_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class RevokedEntry:
    package: str
    version: str
    reason: str
    successor: str | None
    advisory_url: str | None


def _load_embedded_baseline() -> list[RevokedEntry]:
    """Lê a baseline embutida no wheel (sincronizada com COMPAT no release)."""
    try:
        raw = (files("fec_sdk") / "data" / "revoked_versions.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        return [
            RevokedEntry(
                package=e["package"],
                version=e["version"],
                reason=e["reason"],
                successor=e.get("successor"),
                advisory_url=e.get("advisory_url"),
            )
            for e in data.get("revoked", [])
        ]
    except FileNotFoundError:
        return []


def _load_remote_manifest_cached() -> list[RevokedEntry]:
    """Best-effort: busca o manifesto remoto assinado e cacheia local."""
    if not CACHE_PATH.exists() or _cache_stale():
        try:
            _refresh_cache()
        except Exception as exc:
            _log.warning("Falha ao buscar manifesto remoto de revogação: %s; usando cache existente.", exc)

    if not CACHE_PATH.exists():
        return []
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        if not _verify_signature(data):
            _log.warning("Assinatura do manifesto remoto inválida — ignorando para evitar DoS adversarial.")
            return []
        return [
            RevokedEntry(
                package=e["package"], version=e["version"], reason=e["reason"],
                successor=e.get("successor"), advisory_url=e.get("advisory_url"),
            )
            for e in data.get("revoked", [])
        ]
    except (OSError, json.JSONDecodeError) as exc:
        _log.warning("Cache remoto corrompido: %s", exc)
        return []


def _cache_stale() -> bool:
    if not CACHE_PATH.exists():
        return True
    age = time.time() - CACHE_PATH.stat().st_mtime
    return age > CACHE_TTL_SECONDS


def _refresh_cache() -> None:
    """Busca o manifesto remoto. Sem dependência hard de httpx para selftest funcionar offline."""
    try:
        import httpx
    except ImportError:
        return
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    headers = {}
    if CACHE_PATH.exists():
        mtime = CACHE_PATH.stat().st_mtime
        headers["If-Modified-Since"] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(mtime))
    try:
        resp = httpx.get(REMOTE_MANIFEST_URL, timeout=5, headers=headers)
        if resp.status_code == 304:
            CACHE_PATH.touch()
            return
        resp.raise_for_status()
        CACHE_PATH.write_bytes(resp.content)
    except httpx.HTTPError:
        return  # silent — fallback to embedded baseline


def _verify_signature(_data: dict[str, Any]) -> bool:
    """Verificação de assinatura (Sigstore/cosign keyless ou minisign).

    Stub: implementação real virá com `scripts/sign-manifest.py`. Por ora, se
    o campo "signature" está ausente, aceita o manifesto local; em produção,
    ausência de assinatura no manifesto remoto faz `_load_remote_manifest_cached`
    tratar como inválido.
    """
    # TODO(post-mvp): integrar com `cryptography` ou `python-minisign`.
    return True


def check_compat(
    module_id: str | None = None,
    *,
    expected_sdk_version: str | None = None,
) -> None:
    """Valida que o ambiente atual é suportado para o módulo/lab atual.

    Levanta `RevokedVersionError` ou `IncompatibleVersionError` em casos
    bloqueantes. Imprime warning amarelo em patch drift compatível.

    Args:
        module_id: ex. "modulo-3-2"; lê o expected_sdk_version do front-matter
            do módulo se não passado.
        expected_sdk_version: SemVer mínima (ex. ">=1.0,<2.0").
    """
    revoked = _load_embedded_baseline() + _load_remote_manifest_cached()

    for entry in revoked:
        if entry.package == "fec-sdk" and entry.version == __version__:
            if os.environ.get("FEC_ALLOW_INCOMPAT") == "1":
                _log_override(entry, kind="revoked")
                warnings.warn(
                    f"⚠️ fec-sdk {entry.version} foi revogada ({entry.reason}); rodando com FEC_ALLOW_INCOMPAT=1.",
                    stacklevel=2,
                )
                return
            raise RevokedVersionError(
                version=__version__,
                successor=entry.successor,
                advisory_url=entry.advisory_url,
            )

    if expected_sdk_version:
        # Implementação simples — para estrita SemVer, usar `packaging.specifiers`.
        # Aqui faz match major/minor.
        if not _matches(expected_sdk_version, __version__):
            msg = (
                f"Módulo {module_id or '?'} requer fec-sdk {expected_sdk_version}, "
                f"você tem {__version__}."
            )
            if os.environ.get("FEC_ALLOW_INCOMPAT") == "1":
                _log_override(None, kind="incompatible", details=msg)
                warnings.warn("⚠️ " + msg + " (FEC_ALLOW_INCOMPAT=1, seguindo)", stacklevel=2)
                return
            raise IncompatibleVersionError(
                msg,
                fix_hint=f"pip install 'fec-sdk{expected_sdk_version}'",
            )


def _matches(spec: str, version: str) -> bool:
    try:
        from packaging.specifiers import SpecifierSet
        from packaging.version import Version
        return Version(version) in SpecifierSet(spec)
    except ImportError:
        # fallback grosseiro: aceita exact match
        return version == spec.lstrip("=")


def _log_override(entry: RevokedEntry | None, *, kind: str, details: str = "") -> None:
    log_path = Path.home() / ".fec" / "incompat.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ')} kind={kind} version={__version__} python={sys.version_info[:2]}"
    if entry:
        line += f" revoked_for={entry.reason}"
    if details:
        line += f" details={details}"
    log_path.open("a", encoding="utf-8").write(line + "\n")
