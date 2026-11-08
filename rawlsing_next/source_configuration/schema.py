"""Public schema surface for R157 source configurations."""
from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

SCHEMA_ID = "PYAT_R157_SOURCE_CONFIGURATION@1.0.0"
CONFIG_PURPOSE_SOURCE = "SOURCE_PREPARATION"
CONFIG_PURPOSE_FIXTURE = "NONRESPONDENT_FIXTURE"
CONFIG_PURPOSE_EXAMPLE = "P0_EXAMPLE_FIXTURE"
IDENTITY_CLASS_ORIGINAL = "ORIGINAL_SOURCE"
IDENTITY_CLASS_FIXTURE = "NONRESPONDENT_FIXTURE"


@dataclass(frozen=True)
class SourceConfig:
    """Validated, serialized source configuration.

    ``document`` is the exact JSON-shaped config.  Native objects are
    reconstructed by the factory, never cached as pre-invented source witnesses.
    """

    document: Mapping[str, Any]
    path: Path | None = None

    def __post_init__(self) -> None:
        from .validator import validate_source_config as _validate
        _validate(self.document)

    @property
    def config_id(self) -> str:
        return self.document["config_id"]

    @property
    def source_id(self) -> str:
        return self.document["identity"]["source_id"]

    @property
    def config_purpose(self) -> str:
        return self.document["config_purpose"]

    @property
    def identity_class(self) -> str:
        return self.document["binding"]["identity_class"]

    @property
    def active_source_sha256(self) -> str:
        return self.document["binding"]["source_sha256"]

    @property
    def active_row_count(self) -> int:
        return self.document["binding"]["row_count"]

    @property
    def original_source_sha256(self) -> str:
        return self.document["identity"]["expected_source_sha256"]

    @property
    def fixture_provenance(self) -> Mapping[str, Any] | None:
        return self.document["binding"].get("fixture_provenance")

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(dict(self.document))


def validate_source_config(document: Any) -> None:
    """Public validator entry point; raises SourceConfigurationSchemaError."""
    from .validator import validate_source_config as _validate
    _validate(document)


def load_source_config(path: str | Path) -> SourceConfig:
    """Load and validate a JSON source configuration from *path*."""
    path = Path(path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read source configuration {path}: {exc}") from exc
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"source configuration {path} is not valid UTF-8 JSON: {exc}") from exc
    return SourceConfig(document, path=path)


def canonical_config_hash(config: SourceConfig | Mapping[str, Any]) -> str:
    """Deterministic SHA-256 of the JSON-shaped config (not a native object hash).

    Exact source values may be represented as JSON floats (for example a decoded
    SAV numeric token).  This is a byte/config identity, not a semantic object
    identity, so ordinary deterministic JSON is used instead of the native
    semantic canonicalizer, which deliberately forbids binary floats.
    """
    document = config.document if isinstance(config, SourceConfig) else config
    material = json.dumps(
        document, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def config_file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
