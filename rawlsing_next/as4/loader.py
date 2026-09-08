"""HB04 exact qualified A/B/C intake and successor-package loader.

This module is deliberately fail-closed.  It does not perform "latest" lookup,
remint runtime objects, rank candidates, or execute empirical source data.
"""
from __future__ import annotations

from dataclasses import dataclass
import base64
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    DiscoveryAuthority,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    canonical_json,
)

FREEZE_SHA256 = "906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88"
PREDICATE_CARRIER_BLOB = "037ede5626fd0446328042db9aa8240ebcd24f26"
QUERY_CARRIER_BLOB = "9a1a4886d148f94018023cd96ea99d684dbe2b15"
RUNTIME_BINDING_HASH = "8af38e94e1840b60461b1fead707332f250750295bb5902405836c77deb8ca5b"
DISCOVERY_AUTHORITY_HASH = "2e153a153c59bd0b920f8db376478ad1b07000710e79a158471490c11b610cea"
CANDIDATE_GRAMMAR_HASH = "7194b79298c97ff83575e43de472c0e0e1f1ba697d99c666dcba69266da51e06"
OFFICIAL_FRONTIER_HASH = "7aca4dbe1ccd36c48444d6858d378084e41aa30b3197662b6225753d5fc82e24"
REPLAY_CLOSURE_HASH = "45aeaba15ad003b0f734f7c54d68ec22de0e582840a8b239b4a58814e8ee4da1"
B13_FINAL_SEAL_HASH = "c041b7bbf17b9f494b4e3f59a6dd47ee078cb5b35c5c3593a404a2d6078903c3"
LITS1_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"

_ROUTE_A_IMPL_BLOB = "d4915e7e6755ba1850756aebff72f982f73a332b"
_ROUTE_A_TEST_BLOB = "25e905868a21bb36035269065b7bc3640201b7d8"
_ROUTE_C_IMPL_BLOB = "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"
_B16_SEAL_BLOB = "0ebf319c0e6695b077b9ca70b9119007fecfcdcd"
_B14_DRIVER_BLOB = "ea1ec20e0e56a513b13388eeaf0a1c2e067dd9d9"
_HQ23_BLOB = "bdf50129ac52a161dacd5859bc5b8bc60eaa65ac"
_HQ24_BLOB = "7a6755f9e5c07329dca72619a29bc2e4dbc86a10"
_FRONTIER_SNAPSHOT_BLOB = "2f2cbce9c9abaa61048424f2191b81b19847ccdd"

_BASE = Path("data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825")
_CAMPAIGN = _BASE / "PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1"
_FREEZE = _CAMPAIGN / "49A_HB04_QUALIFIED_ABC_INTAKE_FREEZE_R1.json"
_B13 = _CAMPAIGN / "WORKERS/B13_AS3R3_SUCCESSOR_DISCOVERY_FRONTIER_REPLAY_SEAL_R1"
_PRED = _BASE / "AS3R3_NODE5A_R2_REPLAY_SEAL/CANONICAL_PREDICATE_MANIFEST.json"
_QUERY = _CAMPAIGN / "WORKERS/B7_AS3R3_NODE5B_QUERY_MINT_REPLAY_R1/03_CANONICAL_QUERY_REPRESENTATIONS.json"
_A_IMPL = Path("rawlsing_next/pre553_r5_source_backed_adapter.py")
_A_TEST = Path("rawlsing_next/tests/test_pre553_r5_source_backed_adapter.py")
_C_IMPL = Path("rawlsing_next/pre553_route_c_accelerators.py")
_B16 = _CAMPAIGN / "WORKERS/B16_C05R2B_REAL_LITS1_PRODUCTION_I05_R1"
_B16_DRIVER = _B16 / "01_C05R2B_PRODUCTION_EXECUTION_DRIVER.py"
_B16_SEAL = _B16 / "14_C05R2B_FINAL_PRODUCTION_SEAL.json"
_B14_DRIVER = _CAMPAIGN / "WORKERS/B14_AS4I0_AS3R3_SUCCESSOR_REVALIDATION_R1/01_AS4I0_SUCCESSOR_REVALIDATION_DRIVER.py"
_HQ23 = _BASE / "23_AS3R2_ACCEPTANCE_AND_AS4_SYMMETRIC_CANDIDATE_EXECUTION_AUTHORIZATION.md"
_HQ24 = _BASE / "24_AS4_IMPLEMENTATION_READINESS_INVENTORY_AND_COMMON_HARNESS_BUILD_AUTHORIZATION.md"
_PIN_SNAPSHOT = Path("rawlsing_next/as4/pins/discovery_frontier_authority_snapshot.json")


class HB04FreezeError(RuntimeError):
    pass


def repository_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in (here, *here.parents):
        if (parent / "rawlsing_next").is_dir() and (parent / "data").is_dir():
            return parent
    raise HB04FreezeError("cannot locate Rawlsing repository root")


def _json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HB04FreezeError(f"cannot load exact JSON artifact {path}") from exc
    if not isinstance(value, Mapping):
        raise HB04FreezeError(f"exact JSON artifact is not one object: {path}")
    return value


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob_bytes(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _git_blob(path: Path) -> str:
    try:
        return _git_blob_bytes(path.read_bytes())
    except OSError as exc:
        raise HB04FreezeError(f"cannot read pinned artifact {path}") from exc


def _canonical_sha(value: Any) -> str:
    return _sha256_bytes(canonical_json(value).encode("utf-8"))


def _eq(observed: Any, expected: Any, label: str) -> None:
    if observed != expected:
        raise HB04FreezeError(f"{label} mismatch: expected {expected!r}, got {observed!r}")


def _ref_hash(value: Any, label: str) -> str:
    if not isinstance(value, Mapping):
        raise HB04FreezeError(f"{label} is not an exact ref")
    keys = {"kind", "object_id", "content_hash"}
    if set(value) != keys:
        raise HB04FreezeError(f"{label} exact-ref shape changed")
    ref = ExactRef(value["kind"], value["object_id"], value["content_hash"])
    return ref.content_hash


def _materialize(doc: Mapping[str, Any], cls):
    fields = doc.get("semantic_fields")
    if not isinstance(fields, Mapping):
        raise HB04FreezeError(f"{cls.__name__} canonical semantic fields missing")
    return cls(
        schema_id=doc.get("schema_id"),
        schema_version=doc.get("schema_version"),
        typed_state=doc.get("typed_state"),
        authority_snapshot_refs=doc.get("authority_snapshot_refs", ()),
        dependency_refs=doc.get("dependency_refs", ()),
        producer_replay_locator_or_reference_root=doc.get(
            "producer_replay_locator_or_reference_root"
        ),
        object_id=doc.get("object_id"),
        content_hash=doc.get("content_hash"),
        **fields,
    )


@dataclass(frozen=True)
class LoadedHB04Manifest:
    repo_root: Path
    freeze: Mapping[str, Any]
    intake_sha256: str
    discovery_authority: DiscoveryAuthority
    frontier_authority_snapshot: AuthoritySnapshot
    authority_registry_material: tuple[AuthoritySnapshot, ...]
    role_predicates: Mapping[str, EmpiricalPredicate]
    distinct_predicates: tuple[EmpiricalPredicate, ...]
    query_templates: tuple[EmpiricalQuerySpec, ...]
    candidate_grammar: Mapping[str, Any]
    official_frontier_ref: ExactRef
    replay_closure_ref: ExactRef
    runtime_binding_ref: ExactRef
    zero_remints: bool = True

    @property
    def candidate_order(self) -> tuple[str, ...]:
        return ("A", "B", "C")

    @property
    def source_sha256(self) -> str:
        return self.freeze["route_b"]["source_sha256"]

    @property
    def successor_identity_receipt(self) -> Mapping[str, Any]:
        return {
            "runtime_binding": self.runtime_binding_ref.as_dict(),
            "discovery_authority": self.discovery_authority.ref.as_dict(),
            "candidate_grammar_hash": CANDIDATE_GRAMMAR_HASH,
            "official_frontier": self.official_frontier_ref.as_dict(),
            "replay_closure": self.replay_closure_ref.as_dict(),
            "predicate_role_count": len(self.role_predicates),
            "distinct_predicate_count": len(self.distinct_predicates),
            "query_count": len(self.query_templates),
            "sole_alias": ["A000", "A1RAPP"],
            "zero_remints": self.zero_remints,
        }


def _validate_freeze(root: Path) -> Mapping[str, Any]:
    freeze = _json(root / _FREEZE)
    _eq(freeze.get("schema"), "HB04_QUALIFIED_ABC_INTAKE_FREEZE@1.0.0", "freeze schema")
    _eq(_canonical_sha(freeze), FREEZE_SHA256, "canonical HB04 intake freeze SHA-256")
    defs = freeze.get("candidate_definitions", {})
    _eq(defs.get("A"), "R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE", "Route-A definition")
    _eq(defs.get("B"), "SOURCE_BACKED_VIRTUAL_C11", "Route-B definition")
    _eq(defs.get("C"), "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS", "Route-C definition")
    _eq(tuple(defs.get("C_accelerators", ())), (
        "CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE",
        "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK",
    ), "Route-C accelerator inventory")

    a, b, c = freeze["route_a"], freeze["route_b"], freeze["route_c"]
    _eq(a.get("implementation_blob"), _ROUTE_A_IMPL_BLOB, "Route-A implementation pin")
    _eq(a.get("qualification_test_blob"), _ROUTE_A_TEST_BLOB, "Route-A test pin")
    _eq(b.get("final_production_seal_blob"), _B16_SEAL_BLOB, "Route-B final production seal pin")
    _eq(b.get("b14_adapted_driver_blob"), _B14_DRIVER_BLOB, "Route-B B14 driver pin")
    _eq(b.get("source_sha256"), LITS1_SOURCE_SHA256, "Route-B source pin")
    _eq(c.get("implementation_blob"), _ROUTE_C_IMPL_BLOB, "Route-C implementation pin")
    _eq(c.get("qualified_intake_identity"), "e8890b19ddcc9c1ee430fddcfd2cb47b8cccb2c3004975f03ec1f704e032ab10", "Route-C intake pin")

    package = freeze["common_successor_package"]
    expected = {
        "b13_final_seal": B13_FINAL_SEAL_HASH,
        "runtime_binding": RUNTIME_BINDING_HASH,
        "discovery_authority": DISCOVERY_AUTHORITY_HASH,
        "candidate_grammar": CANDIDATE_GRAMMAR_HASH,
        "official_frontier": OFFICIAL_FRONTIER_HASH,
        "preexecution_replay_closure": REPLAY_CLOSURE_HASH,
        "predicate_carrier_git_blob": PREDICATE_CARRIER_BLOB,
        "query_carrier_git_blob": QUERY_CARRIER_BLOB,
        "predicate_role_count": 19,
        "distinct_predicate_count": 18,
        "query_count": 3,
        "distinct_canonical_object_count": 21,
        "candidate_count": 82,
    }
    for key, value in expected.items():
        _eq(package.get(key), value, f"freeze common successor {key}")
    _eq(tuple(package.get("sole_alias", ())), ("A000", "A1RAPP"), "sole alias")
    _eq(freeze["governance"].get("hq23_blob"), _HQ23_BLOB, "HQ23 blob pin")
    _eq(freeze["governance"].get("hq24_blob"), _HQ24_BLOB, "HQ24 blob pin")
    return freeze


def _validate_local_pins(root: Path, freeze: Mapping[str, Any]) -> None:
    checks = (
        (_A_IMPL, _ROUTE_A_IMPL_BLOB, "Route-A implementation"),
        (_A_TEST, _ROUTE_A_TEST_BLOB, "Route-A qualification test"),
        (_C_IMPL, _ROUTE_C_IMPL_BLOB, "Route-C implementation"),
        (_B16_SEAL, _B16_SEAL_BLOB, "B16 final production seal"),
        (_B14_DRIVER, _B14_DRIVER_BLOB, "B14 successorized adapter bootstrap"),
        (_HQ23, _HQ23_BLOB, "HQ23 candidate definitions"),
        (_HQ24, _HQ24_BLOB, "HQ24 common harness contract"),
        (_PRED, PREDICATE_CARRIER_BLOB, "successor predicate carrier"),
        (_QUERY, QUERY_CARRIER_BLOB, "successor query carrier"),
        (_PIN_SNAPSHOT, _FRONTIER_SNAPSHOT_BLOB, "frontier authority snapshot pin"),
    )
    for path, expected, label in checks:
        _eq(_git_blob(root / path), expected, f"{label} Git blob")

    b16 = _json(root / _B16_SEAL)
    route_b = freeze["route_b"]
    _eq(b16.get("qualifying_driver_commit"), route_b["qualifying_driver_commit"], "B16 qualifying driver commit")
    _eq(b16.get("source_sha256"), LITS1_SOURCE_SHA256, "B16 source SHA")
    _eq(b16.get("zero_forbidden_transformed_persistence"), True, "B16 zero transformed persistence")
    bootstrap = (root / _B16_DRIVER).read_text(encoding="utf-8")
    expected_source = route_b["effective_driver_sha256"]
    if f'EXPECTED_SOURCE_SHA256="{expected_source}"' not in bootstrap:
        raise HB04FreezeError("B16 bootstrap no longer pins frozen effective driver SHA-256")


def _load_predicates(root: Path, binding: Mapping[str, Any]) -> tuple[Mapping[str, EmpiricalPredicate], tuple[EmpiricalPredicate, ...]]:
    carrier = _json(root / _PRED)
    _eq(carrier.get("canonical_predicate_count"), 18, "predicate carrier distinct count")
    _eq(carrier.get("source_role_count"), 19, "predicate carrier role count")
    bundle = carrier.get("canonical_representation_bundle")
    if not isinstance(bundle, Mapping) or bundle.get("encoding") != "gzip+base64":
        raise HB04FreezeError("predicate carrier encoding changed")
    try:
        compressed = base64.b64decode(bundle["base64"], validate=True)
        decoded = gzip.decompress(compressed)
    except Exception as exc:
        raise HB04FreezeError("predicate carrier decode failed") from exc
    _eq(len(compressed), bundle.get("gzip_byte_length"), "predicate carrier gzip length")
    _eq(len(decoded), bundle.get("decoded_byte_length"), "predicate carrier decoded length")
    _eq(_sha256_bytes(decoded), bundle.get("decoded_canonical_json_sha256_with_trailing_newline"), "predicate decoded SHA-256")
    try:
        rows = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise HB04FreezeError("predicate carrier canonical bundle is not JSON") from exc
    if not isinstance(rows, list) or len(rows) != 18:
        raise HB04FreezeError("predicate canonical bundle cardinality changed")
    by_hash: dict[str, EmpiricalPredicate] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise HB04FreezeError("predicate carrier row malformed")
        doc = row.get("canonical_representation")
        ref = row.get("ref")
        if not isinstance(doc, Mapping) or not isinstance(ref, Mapping):
            raise HB04FreezeError("predicate carrier row lacks canonical preimage/ref")
        obj = _materialize(doc, EmpiricalPredicate)
        _eq(obj.ref.as_dict(), dict(ref), "materialized successor predicate ref")
        canonical = canonical_json(doc).encode("utf-8")
        expected_rep = row.get("canonical_representation_sha256")
        if expected_rep is not None:
            _eq(_sha256_bytes(canonical), expected_rep, "predicate canonical representation SHA-256")
        if obj.content_hash in by_hash:
            raise HB04FreezeError("duplicate distinct predicate preimage")
        by_hash[obj.content_hash] = obj

    mappings = binding.get("predicate_role_mappings")
    if not isinstance(mappings, list) or len(mappings) != 19:
        raise HB04FreezeError("runtime binding role mappings changed")
    role_map: dict[str, EmpiricalPredicate] = {}
    for mapping in mappings:
        role = mapping.get("as3_id")
        h = mapping.get("successor_content_hash")
        if role in role_map or h not in by_hash:
            raise HB04FreezeError("runtime binding predicate role cannot resolve exactly")
        obj = by_hash[h]
        _eq(mapping.get("successor_object_id"), obj.object_id, "role predicate object_id")
        _eq(mapping.get("successor_kind"), obj.family, "role predicate family")
        role_map[role] = obj
    _eq(set(role_map), {
        "A000","A1V1","A1V2","A1V3","A1V4","A1V5","A1SSUB","A1SSPS","A1SMIS","A1RAPP",
        "A2V1","A2V2","A2V3","A2V4","A2V5","A2SSUB","A2SSPS","A2SMIS","A2RAPP",
    }, "exact predicate role set")
    aliases: dict[str, list[str]] = {}
    for role, obj in role_map.items():
        aliases.setdefault(obj.content_hash, []).append(role)
    nontrivial = sorted(tuple(sorted(v)) for v in aliases.values() if len(v) > 1)
    _eq(nontrivial, [("A000", "A1RAPP")], "sole predicate alias class")
    return role_map, tuple(sorted(by_hash.values(), key=lambda x: x.ref.key))


def _load_queries(root: Path, binding: Mapping[str, Any]) -> tuple[EmpiricalQuerySpec, ...]:
    carrier = _json(root / _QUERY)
    _eq(carrier.get("count"), 3, "query carrier count")
    rows = carrier.get("representations")
    if not isinstance(rows, list) or len(rows) != 3:
        raise HB04FreezeError("query carrier representations changed")
    by_hash: dict[str, EmpiricalQuerySpec] = {}
    for row in rows:
        doc = row.get("canonical_representation")
        ref = row.get("successor_query_ref")
        if not isinstance(doc, Mapping) or not isinstance(ref, Mapping):
            raise HB04FreezeError("query carrier row malformed")
        obj = _materialize(doc, EmpiricalQuerySpec)
        _eq(obj.ref.as_dict(), dict(ref), "materialized successor query ref")
        _eq(_sha256_bytes(canonical_json(doc).encode("utf-8")), row.get("canonical_representation_sha256"), "query canonical representation SHA-256")
        by_hash[obj.content_hash] = obj
    qb = binding.get("query_bindings")
    if not isinstance(qb, list) or len(qb) != 3:
        raise HB04FreezeError("runtime binding query mappings changed")
    ordered = []
    for row in qb:
        ref = row.get("successor_query_ref")
        if not isinstance(ref, Mapping) or ref.get("content_hash") not in by_hash:
            raise HB04FreezeError("runtime binding query cannot resolve exactly")
        obj = by_hash[ref["content_hash"]]
        _eq(obj.ref.as_dict(), dict(ref), "runtime binding query ref")
        ordered.append(obj)
    return tuple(ordered)


def load_hb04_manifest(*, root: Path | None = None, freeze_path: Path | None = None) -> LoadedHB04Manifest:
    repo = repository_root(root)
    freeze = _validate_freeze(repo) if freeze_path is None else _json(Path(freeze_path))
    if freeze_path is not None:
        _eq(_canonical_sha(freeze), FREEZE_SHA256, "supplied HB04 intake freeze SHA-256")
    _validate_local_pins(repo, freeze)

    binding = _json(repo / _B13 / "02_SUCCESSOR_RUNTIME_CATALOG_BINDING.json")
    seal = _json(repo / _B13 / "12_SUCCESSOR_DISCOVERY_AUTHORITY_FRONTIER_REPLAY_SEAL.json")
    _eq(_ref_hash(seal.get("successor_runtime_catalog_binding_ref"), "successor runtime binding"), RUNTIME_BINDING_HASH, "runtime binding ref")
    _eq(binding.get("predicate_role_mapping_count"), 19, "binding predicate role count")
    _eq(binding.get("distinct_predicate_count"), 18, "binding distinct predicate count")
    _eq(binding.get("query_mapping_count"), 3, "binding query count")
    _eq(binding.get("distinct_canonical_object_count"), 21, "binding canonical object count")
    _eq(binding.get("runtime_objects_reminted"), False, "runtime remint flag")
    _eq(tuple(binding.get("sole_alias", ())), ("A000", "A1RAPP"), "runtime sole alias")

    role_map, predicates = _load_predicates(repo, binding)
    queries = _load_queries(repo, binding)

    da_doc = _json(repo / _B13 / "03_SUCCESSOR_DISCOVERY_AUTHORITY.json")
    da = _materialize(da_doc, DiscoveryAuthority)
    _eq(da.content_hash, DISCOVERY_AUTHORITY_HASH, "successor DiscoveryAuthority materialization")

    grammar_doc = _json(repo / _B13 / "05_SUCCESSOR_CANDIDATE_GRAMMAR.json")
    grammar = grammar_doc.get("candidate_grammar")
    if not isinstance(grammar, Mapping):
        raise HB04FreezeError("successor candidate grammar material missing")
    _eq(grammar_doc.get("candidate_grammar_hash"), CANDIDATE_GRAMMAR_HASH, "candidate grammar hash")
    _eq(_canonical_sha(grammar), CANDIDATE_GRAMMAR_HASH, "candidate grammar material hash")
    _eq((len(grammar.get("atoms", ())), len(grammar.get("query_templates", ())), len(grammar.get("rules", ()))), (19, 3, 82), "grammar cardinalities")
    _eq(grammar.get("no_empirical_evaluation"), True, "grammar preexecution state")

    frontier_doc = _json(repo / _B13 / "06_SUCCESSOR_82_CANDIDATE_FRONTIER_MANIFEST.json")
    frontier_hash = _ref_hash(frontier_doc.get("official_frontier_ref"), "official frontier")
    _eq(frontier_hash, OFFICIAL_FRONTIER_HASH, "official frontier hash")
    _eq((frontier_doc.get("candidate_count"), len(frontier_doc.get("candidates", ()))), (82, 82), "frontier cardinality")
    _eq(frontier_doc.get("candidate_execution_count"), 0, "preexecution candidate count")
    _eq((frontier_doc.get("semantic_membership_change_count"), frontier_doc.get("addition_count"), frontier_doc.get("deletion_count")), (0, 0, 0), "frontier membership invariants")

    replay_doc = _json(repo / _B13 / "09_SUCCESSOR_PREEXECUTION_REPLAY_CLOSURE_RECEIPT.json")
    replay_ref = seal.get("successor_preexecution_replay_closure_ref")
    _eq(_ref_hash(replay_ref, "successor replay closure"), REPLAY_CLOSURE_HASH, "replay closure hash")
    _eq(replay_doc.get("candidate_count"), 82, "replay candidate count")
    _eq(replay_doc.get("candidate_execution_count"), 0, "replay candidate execution count")
    _eq(_ref_hash(replay_doc.get("successor_discovery_authority_ref"), "replay DA"), DISCOVERY_AUTHORITY_HASH, "replay DA")
    _eq(_ref_hash(replay_doc.get("successor_candidate_grammar_ref"), "replay grammar"), CANDIDATE_GRAMMAR_HASH, "replay grammar")
    _eq(_ref_hash(replay_doc.get("successor_official_frontier_ref"), "replay frontier"), OFFICIAL_FRONTIER_HASH, "replay frontier")
    _eq(_ref_hash(replay_doc.get("successor_runtime_catalog_binding_ref"), "replay binding"), RUNTIME_BINDING_HASH, "replay binding")

    snap_doc = _json(repo / _PIN_SNAPSHOT)
    snapshot = _materialize(snap_doc, AuthoritySnapshot)
    required = da.authority_snapshot_refs
    if snapshot.authority_ref not in required:
        raise HB04FreezeError("pinned frontier authority snapshot is not bound by successor DiscoveryAuthority")
    registry = AuthorityRegistry((snapshot,))
    registry.resolve_exact(snapshot.authority_ref)

    return LoadedHB04Manifest(
        repo_root=repo,
        freeze=freeze,
        intake_sha256=FREEZE_SHA256,
        discovery_authority=da,
        frontier_authority_snapshot=snapshot,
        authority_registry_material=(snapshot,),
        role_predicates=role_map,
        distinct_predicates=predicates,
        query_templates=queries,
        candidate_grammar=grammar,
        official_frontier_ref=ExactRef(
            seal["successor_official_frontier_ref"]["kind"],
            seal["successor_official_frontier_ref"]["object_id"],
            OFFICIAL_FRONTIER_HASH,
        ),
        replay_closure_ref=ExactRef(
            replay_ref["kind"], replay_ref["object_id"], REPLAY_CLOSURE_HASH
        ),
        runtime_binding_ref=ExactRef(
            seal["successor_runtime_catalog_binding_ref"]["kind"],
            seal["successor_runtime_catalog_binding_ref"]["object_id"],
            RUNTIME_BINDING_HASH,
        ),
    )


def reject_ungoverned_directive(value: Mapping[str, Any] | None) -> None:
    if not value:
        return
    forbidden = {"rank", "ranking", "score", "select", "selection", "winner", "recommend", "recommendation", "stop_early", "extra_accelerator", "cacc3"}
    present = forbidden.intersection(str(k).lower() for k in value)
    if present:
        raise HB04FreezeError(f"HB04 forbids ranking/selection/extra-accelerator directives: {sorted(present)!r}")


__all__ = [
    "FREEZE_SHA256",
    "LITS1_SOURCE_SHA256",
    "HB04FreezeError",
    "LoadedHB04Manifest",
    "load_hb04_manifest",
    "repository_root",
    "reject_ungoverned_directive",
]
