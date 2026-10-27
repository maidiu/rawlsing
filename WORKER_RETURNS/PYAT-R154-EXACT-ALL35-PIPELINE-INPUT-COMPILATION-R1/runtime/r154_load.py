"""Cold loader for R154 all35 store; constructs actual current native input objects."""
from __future__ import annotations

import dataclasses
import json
import sqlite3
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.schema import (
    SourceConfig,
    canonical_config_hash,
    load_source_config,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    build_source_backed_c11_repository,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
import sys
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "store" / "r154_all35.sqlite"


class LoadRefusal(ValueError):
    pass


def _b49():
    p = Path(__file__).resolve().parents[3] / ".r61" / "r150-scientific-native-input" / "inputs" / "pre553_inherited_source_rules.py"
    spec = importlib.util.spec_from_file_location("r154_loader_b49", p)
    mod = importlib.util.module_from_spec(spec); sys.modules["r154_loader_b49"] = mod; spec.loader.exec_module(mod)
    return mod


@dataclasses.dataclass(frozen=True)
class NativeInputPackage:
    source_id: str
    native_source_identity: NativeSourceIdentity
    original_wave_identity: OriginalWaveIdentity
    selected_source_rule_package: Any
    physical_column_count: int
    codebook_row_count: int
    evidence_item_count: int
    current_grant: dict[str, Any]
    native_workload_status: str


def _connect(path: Path = DB):
    if not path.is_file():
        raise LoadRefusal("STORE_MISSING")
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def load_source(source_id: str, db_path: Path = DB) -> NativeInputPackage:
    con = _connect(db_path)
    try:
        row = con.execute("select * from sources where source_id=?", (source_id,)).fetchone()
        if row is None:
            raise LoadRefusal("SOURCE_NOT_IN_STORE")
        pkg_row = con.execute("select package_json from native_packages where source_id=?", (source_id,)).fetchone()
        if pkg_row is None:
            raise LoadRefusal("NATIVE_PACKAGE_MISSING")
        pkg = json.loads(pkg_row["package_json"])
        ident_data = pkg["native_source_identity"]
        ident = NativeSourceIdentity(
            source_id=ident_data["source_id"], family=ident_data["family"], wave=ident_data["wave"],
            canonical_filename=ident_data["canonical_filename"],
            declared_sha256=ident_data["declared_sha256"],
            source_format=ident_data["source_format"], expected_rows=ident_data["expected_rows"])
        wave = pkg["original_wave_identity"]
        wave_obj = OriginalWaveIdentity(wave["atlas_id"], wave["dataset_id"], wave["source_family"], wave["wave"])
        b49 = _b49()
        material = pkg["selected_source_rule_package"]
        source_identity = b49.SourceIdentity(
            source_id=material["source"]["source_id"], family=material["source"]["family"],
            wave=material["source"]["wave"], canonical_filename=material["source"]["canonical_filename"],
            declared_sha256=material["source"]["declared_sha256"], size_bytes=int(row["bytes"]),
            source_format=material["source"]["source_format"], decoder_mode=material["source"]["decoder_mode"],
            expected_rows=int(row["physical_rows"]),
            documentary_unknowns=material["source"].get("documentary_unknowns", ""),
            authority_launch_class=material["source"].get("authority_launch_class", ""),
            observed_item_records=int(material["source"].get("observed_item_records") or 0))
        rules = tuple(b49.SelectedItemRule(
            implementation_id=r["implementation_id"], source_variable_code=r["source_variable_code"],
            disposition=r["disposition"], semantic_direction=r["semantic_direction"],
            routing_status=r["routing_status"], response_binding_status=r["response_binding_status"],
            status=r["status"], reason=r["reason"],
            authority_evidence_refs=tuple(r["authority_evidence_refs"]),
            exact_identity_sha256=r["exact_identity_sha256"]) for group in ("selected","held","excluded","superseded","unknown") for r in material.get(group, []))
        selected = tuple(r for r in rules if r.status == b49.U_CANDIDATE)
        held = tuple(r for r in rules if r.status == b49.HELD_UNRESOLVED)
        excluded = tuple(r for r in rules if r.status == b49.EXCLUDED_NON_U)
        superseded = tuple(r for r in rules if r.status == b49.SUPERSEDED)
        unknown = tuple(r for r in rules if r.status not in {b49.U_CANDIDATE,b49.HELD_UNRESOLVED,b49.EXCLUDED_NON_U,b49.SUPERSEDED})
        package = b49.SelectedSourceRulePackage(
            schema=material["schema"], package_id=material["package_id"], source=source_identity,
            as_of=material["as_of"], selected=selected, held=held, excluded=excluded,
            superseded=superseded, unknown=unknown,
            authority_object_identity=material["authority_object_identity"],
            package_hash=material["package_hash"])
        counts = con.execute("select count(*) from physical_columns where source_id=?", (source_id,)).fetchone()[0]
        cbc = con.execute("select count(*) from codebook_rows where source_id=?", (source_id,)).fetchone()[0]
        evc = con.execute("select count(*) from evidence where source_id=?", (source_id,)).fetchone()[0]
        return NativeInputPackage(
            source_id=source_id, native_source_identity=ident, original_wave_identity=wave_obj,
            selected_source_rule_package=package, physical_column_count=counts,
            codebook_row_count=cbc, evidence_item_count=evc,
            current_grant=pkg.get("current_source_grant") or {},
            native_workload_status=pkg.get("native_workload_status", "UNKNOWN"))
    finally:
        con.close()


@dataclasses.dataclass(frozen=True)
class PreparedNativeWorkload:
    """A prepared source-configuration construction, never an issued workload."""

    source_id: str
    config_id: str
    config_sha256: str
    source_sha256: str
    projection: Any
    repository: Any
    release: Any
    row_native_key_count: int
    native_calls: tuple[str, ...]
    status: str = "PREPARED_CONFIGURATION_ONLY__NOT_ISSUED_ORIGINAL_WORKLOAD"
    issued_original_workload: bool = False
    execution_permission_required: bool = True


def _source_row(source_id: str, db_path: Path = DB) -> dict[str, Any]:
    con = _connect(db_path)
    try:
        row = con.execute("select * from sources where source_id=?", (source_id,)).fetchone()
        if row is None:
            raise LoadRefusal("SOURCE_NOT_IN_STORE")
        return dict(row)
    finally:
        con.close()


def build_prepared_native_workload(
    source_id: str,
    config: SourceConfig | str | Path,
    source: ExactPhysicalCellStream | PhysicalSourceIncidence,
    *,
    db_path: Path = DB,
    row_native_keys: Any = None,
    cache: Any = None,
    batch_size: int = 10_000,
) -> PreparedNativeWorkload:
    """Delegate a prepared configuration to the existing source-backed C11 owner.

    This is configuration/native-construction preparation only.  It does not
    issue an original empirical workload, grant source execution, or replace the
    existing issued-workload owner.
    """
    if isinstance(config, (str, Path)):
        config = load_source_config(config)
    elif not isinstance(config, SourceConfig):
        config = SourceConfig(config)
    if config.source_id != source_id:
        raise LoadRefusal("SOURCE_CONFIGURATION_SOURCE_ID_MISMATCH")
    source_row = _source_row(source_id, db_path)
    if config.original_source_sha256 != source_row["current_sha256"]:
        raise LoadRefusal("SOURCE_CONFIGURATION_ORIGINAL_IDENTITY_MISMATCH")
    if not isinstance(source, (ExactPhysicalCellStream, PhysicalSourceIncidence)):
        raise LoadRefusal("PERMITTED_PHYSICAL_TRANSPORT_REQUIRED")
    if row_native_keys is None and config.document["respondents"].get("source_native_key_slot") is not None:
        row_native_keys = row_native_keys_from_transport(
            config,
            stream=source if isinstance(source, ExactPhysicalCellStream) else None,
            incidence=source if isinstance(source, PhysicalSourceIncidence) else None,
            batch_size=batch_size,
        )
    projection = build_governed_c11_projection(
        config,
        source_sha256=source.source_sha256,
        row_count=source.row_count,
        row_native_keys=row_native_keys,
    )
    repository, release = build_source_backed_c11_repository(
        source, projection, cache=cache, batch_size=batch_size)
    return PreparedNativeWorkload(
        source_id=source_id,
        config_id=config.config_id,
        config_sha256=canonical_config_hash(config),
        source_sha256=source.source_sha256,
        projection=projection,
        repository=repository,
        release=release,
        row_native_key_count=0 if row_native_keys is None else len(row_native_keys),
        native_calls=(
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.pre553_source_backed_c11_facade.build_source_backed_c11_repository",
        ),
    )


def build_native_workload(
    source_id: str,
    db_path: Path = DB,
    *,
    config: SourceConfig | str | Path | None = None,
    source: ExactPhysicalCellStream | PhysicalSourceIncidence | None = None,
    row_native_keys: Any = None,
    cache: Any = None,
    batch_size: int = 10_000,
):
    """Compatibility entry point.

    With an exact prepared config and a permitted physical transport it delegates
    to the real source-backed C11 constructor.  Without both inputs it preserves
    the historical current-grant refusal; it no longer refuses unconditionally.
    """
    if config is None and source is None:
        package = load_source(source_id, db_path)
        if package.current_grant.get("currentness") == "PENDING_EXACT_CURRENT_SOURCE_ISSUANCE":
            raise LoadRefusal("CURRENT_SOURCE_READ_GRANT_REQUIRED")
        raise LoadRefusal("PREPARED_NATIVE_CONSTRUCTION_REQUIRES_CONFIG_AND_PERMITTED_SOURCE")
    if config is None or source is None:
        raise LoadRefusal("PREPARED_NATIVE_CONSTRUCTION_REQUIRES_CONFIG_AND_PERMITTED_SOURCE")
    return build_prepared_native_workload(
        source_id, config, source, db_path=db_path,
        row_native_keys=row_native_keys, cache=cache, batch_size=batch_size)


def load_all(db_path: Path = DB) -> tuple[NativeInputPackage, ...]:
    con = _connect(db_path)
    try:
        ids = [r[0] for r in con.execute("select source_id from sources order by source_id")]
    finally:
        con.close()
    return tuple(load_source(sid, db_path) for sid in ids)
