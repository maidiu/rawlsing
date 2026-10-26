"""Cold loader for R154 all35 store; constructs actual current native input objects."""
from __future__ import annotations

import dataclasses
import json
import sqlite3
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity
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


def build_native_workload(source_id: str, db_path: Path = DB):
    package = load_source(source_id, db_path)
    if package.current_grant.get("currentness") == "PENDING_EXACT_CURRENT_SOURCE_ISSUANCE":
        raise LoadRefusal("CURRENT_SOURCE_READ_GRANT_REQUIRED")
    raise LoadRefusal("NATIVE_WORKLOAD_ISSUANCE_NOT_IMPLEMENTED_WITHOUT_CURRENT_GRANT")


def load_all(db_path: Path = DB) -> tuple[NativeInputPackage, ...]:
    con = _connect(db_path)
    try:
        ids = [r[0] for r in con.execute("select source_id from sources order by source_id")]
    finally:
        con.close()
    return tuple(load_source(sid, db_path) for sid in ids)
