"""Fail-closed LiTS current <-> ASTRA-D04-R2 substantive parity gate.

This module compares only canonical empirical substance that both historical
ASTRA and the current candidate-neutral PRE553 execution can lawfully express.
Historical whole-product/replay hashes remain provenance identities; they are
never required to equal current-schema execution identities.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from typing import Any, Mapping, Sequence

from rawlsing_next.fiabc_lits_i_d03_risk_set_authority import (
    AUTHORITY_CONTENT_HASH as D03_AUTHORITY_CONTENT_HASH,
    ROOTS as CURRENT_D03_ROOTS,
)
from rawlsing_next.fiabc_lits_cross_schema_candidate_identity import (
    candidate_semantics,
    g02_execution_candidate_hash,
    logical_candidate_key,
    logical_candidate_material,
)
from rawlsing_next.pre553_empirical_objects import canonical_json, canonicalize, exact_ref, semantic_hash

SUMMARY_SCHEMA = "FIABC_LITS_ASTRA_SHAPED_EMPIRICAL_SUMMARY@1.0.0"
PARITY_RECEIPT_SCHEMA = "FIABC_LITS_ASTRA_SUBSTANTIVE_PARITY_RECEIPT@1.0.0"

P0_RULE = "D02_P0_REAL_POSITIVE_CONTROL"
P1_RULE = "D02_P1_JOINT_DEPENDENCE"
P2_RULE = "D02_P2_HIGHER_ORDER_K3"
P3_RULE = "D02_P3_CONDITIONAL_REVERSAL"
P4_RULE = "D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS"

EXPECTED_LANE_COUNTS = {
    "P0": {"candidate_count": 5, "query_role_count": 5},
    "P1": {"candidate_count": 1, "query_role_count": 3},
    "P2": {"candidate_count": 18, "query_role_count": 36},
    "P3": {"candidate_count": 1, "query_role_count": 8},
    "P4": {"candidate_count": 25, "query_role_count": 25},
}
EXPECTED_TERMINAL_COUNTS = {
    "EVALUATED_SUPPORTED": 49,
    "EVALUATED_VALID_EMPTY": 1,
}
ASTRA_SOURCE_IDENTITY = {
    "source": "LITS_I",
    "sha256": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
    "rows": 29002,
    "variables": 1198,
}
EXPECTED_RISK_ROOTS = {
    "R2": {
        "count": 24897,
        "root": "f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3",
    },
    "R7": {
        "count": 28325,
        "root": "0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844",
    },
    "R27": {
        "count": 24630,
        "root": "f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29",
    },
}
P3_ROLES = (
    "POOLED_NEG",
    "POOLED_POS",
    "STRATUM:Q310V1:NEG",
    "STRATUM:Q310V1:POS",
    "STRATUM:Q310V2:NEG",
    "STRATUM:Q310V2:POS",
    "STRATUM:Q310V3:NEG",
    "STRATUM:Q310V3:POS",
)
PARITY_SECTIONS = (
    "frontier",
    "d03_risk_sets",
    "f02_selector_populations",
    "role_execution",
    "logical_candidate_identity",
    "role_risk_set_topology",
    "P0",
    "P1",
    "P2",
    "P3",
    "P4",
    "final_envelope",
)


class LitsAstraSubstantiveParityError(RuntimeError):
    pass


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LitsAstraSubstantiveParityError(f"{label} must be an exact mapping")
    return value


def _sequence(value: Any, label: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise LitsAstraSubstantiveParityError(f"{label} must be an exact sequence")
    if not allow_empty and not value:
        raise LitsAstraSubstantiveParityError(f"{label} may not be empty")
    return value


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise LitsAstraSubstantiveParityError(f"{label} must be an exact integer")
    return value


def _cell(value: Any) -> Any:
    """Normalize only ASTRA's known integer-vs-exact-decimal cell encoding split."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, Mapping) and set(value) == {"$exact_decimal"}:
        raw = value["$exact_decimal"]
        if not isinstance(raw, str):
            raise LitsAstraSubstantiveParityError("exact decimal cell token must be text")
        try:
            frac = Fraction(raw)
        except (ValueError, ZeroDivisionError) as exc:
            raise LitsAstraSubstantiveParityError("invalid exact decimal cell token") from exc
        if frac.denominator != 1:
            raise LitsAstraSubstantiveParityError("ASTRA parity admits integral target cells only")
        return frac.numerator
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_cell(item) for item in value]
    raise LitsAstraSubstantiveParityError(f"unsupported ASTRA target cell representation: {value!r}")


def _fraction_material(value: Any, label: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping) and set(value) == {"$exact_fraction"}:
        pair = _sequence(value["$exact_fraction"], label)
        if len(pair) != 2:
            raise LitsAstraSubstantiveParityError(f"{label} exact fraction arity drift")
        numerator = _integer(pair[0], label + ".numerator")
        denominator = _integer(pair[1], label + ".denominator")
        if denominator == 0:
            raise LitsAstraSubstantiveParityError(f"{label} exact fraction zero denominator")
        frac = Fraction(numerator, denominator)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)) and len(value) == 2:
        frac = Fraction(_integer(value[0], label + ".numerator"), _integer(value[1], label + ".denominator"))
    else:
        raise LitsAstraSubstantiveParityError(f"{label} exact fraction required")
    return {"$exact_fraction": [frac.numerator, frac.denominator]}


def _fraction_from_counts(numerator: int, denominator: int, label: str) -> Mapping[str, Any]:
    numerator = _integer(numerator, label + ".numerator")
    denominator = _integer(denominator, label + ".denominator")
    if denominator <= 0:
        raise LitsAstraSubstantiveParityError(f"{label} requires positive denominator")
    frac = Fraction(numerator, denominator)
    return {"$exact_fraction": [frac.numerator, frac.denominator]}


def _fraction_value(value: Mapping[str, Any]) -> Fraction:
    pair = value["$exact_fraction"]
    return Fraction(pair[0], pair[1])


def _sign(value: Fraction) -> int:
    return 1 if value > 0 else (-1 if value < 0 else 0)



SELECTOR_QUESTIONS = ("q310", "q311")
SELECTOR_KEYS = ("1", "2", "3", "MISSING")
F02_SELECTOR_ROOT_DOMAIN = "F02_SOURCE_ROW_ORDINAL_NATIVE_VALUE@1.0.0"


def _sha256_text(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value != value.lower()
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise LitsAstraSubstantiveParityError(f"{label} must be an exact lowercase sha256")
    return value


def _selector_populations(
    value: Any,
    label: str,
    *,
    row_root_field: str,
) -> Mapping[str, Any]:
    source = _mapping(value, label)
    if set(source) != set(SELECTOR_QUESTIONS):
        raise LitsAstraSubstantiveParityError(f"{label} must contain exact q310/q311 selector populations")
    questions = {}
    for question in SELECTOR_QUESTIONS:
        row = _mapping(source.get(question), f"{label}.{question}")
        counts = _mapping(row.get("counts"), f"{label}.{question}.counts")
        roots = _mapping(row.get("selector_roots"), f"{label}.{question}.selector_roots")
        if set(counts) != set(SELECTOR_KEYS) or set(roots) != set(SELECTOR_KEYS):
            raise LitsAstraSubstantiveParityError(
                f"{label}.{question} must contain exact 1/2/3/MISSING selector keys"
            )
        normalized_counts = {
            key: _integer(counts[key], f"{label}.{question}.counts.{key}")
            for key in SELECTOR_KEYS
        }
        if any(count < 0 for count in normalized_counts.values()):
            raise LitsAstraSubstantiveParityError(f"{label}.{question} selector count may not be negative")
        if sum(normalized_counts.values()) != ASTRA_SOURCE_IDENTITY["rows"]:
            raise LitsAstraSubstantiveParityError(
                f"{label}.{question} selector populations do not close over exact source rows"
            )
        normalized_roots = {
            key: _sha256_text(roots[key], f"{label}.{question}.selector_roots.{key}")
            for key in SELECTOR_KEYS
        }
        questions[question] = {
            "counts": normalized_counts,
            "row_root": _sha256_text(
                row.get(row_root_field), f"{label}.{question}.{row_root_field}"
            ),
            "selector_roots": normalized_roots,
        }
    return canonicalize({
        "root_domain": F02_SELECTOR_ROOT_DOMAIN,
        "root_equality": "REQUIRED_EXACT_SAME_CANONICAL_F02_SCAN_DOMAIN",
        "questions": questions,
    })


def _historical_risk_roots(
    role_receipt: Mapping[str, Any], replay_receipt: Mapping[str, Any]
) -> Mapping[str, Any]:
    role_roots = _mapping(role_receipt.get("risk_set_roots"), "ASTRA role risk_set_roots")
    replay_roots = _mapping(
        _mapping(replay_receipt.get("preoutcome"), "ASTRA replay preoutcome").get("d03_roots"),
        "ASTRA replay d03_roots",
    )
    normalized = {}
    for root_id in ("R2", "R7", "R27"):
        role = _mapping(role_roots.get(root_id), f"ASTRA role root {root_id}")
        replay = _mapping(replay_roots.get(root_id), f"ASTRA replay root {root_id}")
        row = {
            "count": _integer(role.get("count"), f"{root_id}.count"),
            "root": role.get("root"),
        }
        if row != {
            "count": _integer(replay.get("count"), f"replay {root_id}.count"),
            "root": replay.get("root"),
        }:
            raise LitsAstraSubstantiveParityError(f"historical ASTRA {root_id} roots disagree")
        if row != EXPECTED_RISK_ROOTS[root_id]:
            raise LitsAstraSubstantiveParityError(f"historical ASTRA {root_id} accepted root drift")
        normalized[root_id] = row
    return canonicalize(normalized)


def _current_risk_roots() -> Mapping[str, Any]:
    roots = {}
    for root_id in ("R2", "R7", "R27"):
        row = _mapping(CURRENT_D03_ROOTS.get(root_id), f"current D03 {root_id}")
        roots[root_id] = {
            "count": _integer(row.get("member_count"), f"current {root_id}.member_count"),
            "root": row.get("canonical_full_tsv_sha256"),
        }
    if canonicalize(roots) != canonicalize(EXPECTED_RISK_ROOTS):
        raise LitsAstraSubstantiveParityError("current D03 authority roots drift from accepted ASTRA truth")
    return canonicalize(roots)


def _historical_logical_identity(
    product: Mapping[str, Any],
) -> tuple[Mapping[str, str], Mapping[str, str], list[Mapping[str, Any]], Mapping[str, Any]]:
    """Recover shared logical keys while independently verifying native G02 hashes."""
    native_to_logical: dict[str, str] = {}
    p4_cell_to_logical: dict[str, str] = {}
    logical_rows: list[Mapping[str, Any]] = []
    native_rows: list[Mapping[str, Any]] = []

    def add(
        *,
        lane: str,
        parameters: Mapping[str, Any],
        native_hash: str | None = None,
        p4_cell: Any = None,
    ) -> str:
        semantics = candidate_semantics(lane=lane, parameters=parameters)
        key = logical_candidate_key(semantics)
        logical_rows.append(canonicalize({
            "logical_candidate_key": key,
            "logical_candidate_material": logical_candidate_material(semantics),
        }))
        expected_native = g02_execution_candidate_hash(semantics)
        if native_hash is not None:
            if not isinstance(native_hash, str) or len(native_hash) != 64:
                raise LitsAstraSubstantiveParityError("historical G02 native candidate hash malformed")
            if expected_native != native_hash:
                raise LitsAstraSubstantiveParityError(
                    f"historical G02 native hash does not match reconstructed candidate semantics for {lane}"
                )
            provenance_basis = "ASTRA_RECORDED_AND_G02_PREIMAGE_RECOMPUTED"
        else:
            native_hash = expected_native
            provenance_basis = "ACCEPTED_G02_PREIMAGE_DERIVED"
        if native_hash in native_to_logical:
            raise LitsAstraSubstantiveParityError("duplicate historical G02 native candidate hash")
        native_to_logical[native_hash] = key
        native_rows.append(canonicalize({
            "lane": lane,
            "logical_candidate_key": key,
            "g02_execution_candidate_hash": native_hash,
            "provenance_basis": provenance_basis,
        }))
        if p4_cell is not None:
            cell_key = canonical_json(_cell(p4_cell))
            if cell_key in p4_cell_to_logical:
                raise LitsAstraSubstantiveParityError("duplicate historical P4 logical target cell")
            p4_cell_to_logical[cell_key] = key
        return key

    for item in _sequence(product.get("P0_positive_controls"), "ASTRA P0"):
        add(
            lane="P0",
            parameters={"target_cell": _cell(item["target_cell"])},
            native_hash=item["candidate_hash"],
        )

    p1 = _mapping(product.get("P1_joint_dependence"), "ASTRA P1")
    add(lane="P1", parameters={}, native_hash=p1["candidate_hash"])

    for item in _sequence(product.get("P2_conditioned_frontier"), "ASTRA P2"):
        params = _mapping(item.get("parameters"), "ASTRA P2 parameters")
        normalized_params = {
            "q301_2": _integer(params.get("q301_2"), "ASTRA P2 q301_2"),
            "q310": _integer(params.get("q310"), "ASTRA P2 q310"),
            "q311": _integer(params.get("q311"), "ASTRA P2 q311"),
        }
        add(lane="P2", parameters=normalized_params, native_hash=item["candidate_hash"])

    p3 = _mapping(product.get("P3_conditional_reversal"), "ASTRA P3")
    add(
        lane="P3",
        parameters={"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]},
        native_hash=p3["candidate_hash"],
    )

    p4 = _mapping(product.get("P4_joint_5x5_target_support"), "ASTRA P4")
    for raw_cell in sorted(p4, key=lambda x: tuple(int(v) for v in x.split(","))):
        cell = [int(v) for v in raw_cell.split(",")]
        add(lane="P4", parameters={"target_cell": cell}, p4_cell=cell)

    logical_rows = sorted(logical_rows, key=lambda x: x["logical_candidate_key"])
    if len(logical_rows) != 50 or len({x["logical_candidate_key"] for x in logical_rows}) != 50:
        raise LitsAstraSubstantiveParityError("historical logical candidate frontier is not exact unique 50")
    if len(native_rows) != 50:
        raise LitsAstraSubstantiveParityError("historical logical frontier must preserve exactly 50 G02 native hashes")

    provenance = canonicalize({
        "native_hash_domain": "G02_EXECUTION_CANDIDATE_HASH",
        "native_hash_equality_with_current_required": False,
        "rows": sorted(native_rows, key=canonical_json),
    })
    return native_to_logical, p4_cell_to_logical, logical_rows, provenance


def _current_logical_identity(
    bindings: Sequence[Mapping[str, Any]],
) -> tuple[Mapping[str, Mapping[str, Any]], list[Mapping[str, Any]], Mapping[str, Any]]:
    by_native: dict[str, Mapping[str, Any]] = {}
    logical_rows: list[Mapping[str, Any]] = []
    provenance_rows: list[Mapping[str, Any]] = []
    for raw in _sequence(bindings, "current PRE553 logical candidate bindings"):
        row = _mapping(raw, "current PRE553 logical binding")
        native_hash = row.get("current_pre553_candidate_hash")
        key = row.get("logical_candidate_key")
        material = row.get("logical_candidate_material")
        if not isinstance(native_hash, str) or len(native_hash) != 64:
            raise LitsAstraSubstantiveParityError("current PRE553 native candidate hash malformed")
        if not isinstance(key, str) or len(key) != 64:
            raise LitsAstraSubstantiveParityError("current logical candidate key malformed")
        material_map = _mapping(material, "current logical candidate material")
        if semantic_hash(material_map) != key:
            raise LitsAstraSubstantiveParityError("current logical candidate key/material contradiction")

        binding_identity = row.get("binding_identity")
        binding_without_identity = {
            k: v for k, v in row.items() if k != "binding_identity"
        }
        if (
            not isinstance(binding_identity, str)
            or len(binding_identity) != 64
            or semantic_hash(canonicalize(binding_without_identity)) != binding_identity
        ):
            raise LitsAstraSubstantiveParityError("current logical binding identity/preimage contradiction")

        native_preimage = _mapping(
            row.get("current_pre553_native_candidate_preimage"),
            "current PRE553 native candidate preimage",
        )
        if semantic_hash(native_preimage) != native_hash:
            raise LitsAstraSubstantiveParityError("current PRE553 native candidate hash/preimage contradiction")
        expected_candidate_id = f"urn:rawlsing:pre553:i05:candidate:sha256:{native_hash}"
        if row.get("current_pre553_candidate_id") != expected_candidate_id:
            raise LitsAstraSubstantiveParityError("current PRE553 candidate id/hash contradiction")

        logical_semantics = _mapping(
            material_map.get("candidate_semantics"),
            "current logical candidate semantics",
        )
        if row.get("lane") != logical_semantics.get("lane"):
            raise LitsAstraSubstantiveParityError("current logical binding lane/material contradiction")
        if row.get("rule_id") != logical_semantics.get("rule_id"):
            raise LitsAstraSubstantiveParityError("current logical binding rule/material contradiction")
        if native_preimage.get("rule_id") != logical_semantics.get("rule_id"):
            raise LitsAstraSubstantiveParityError("current native/logical rule identity contradiction")
        if native_preimage.get("family") != logical_semantics.get("family"):
            raise LitsAstraSubstantiveParityError("current native/logical family identity contradiction")
        if canonicalize(native_preimage.get("validation")) != canonicalize(logical_semantics.get("validation")):
            raise LitsAstraSubstantiveParityError("current native/logical validation identity contradiction")

        role_bindings = {
            x["role"]: _mapping(x, "current logical role binding")
            for x in _sequence(row.get("role_bindings"), "current logical role bindings")
        }
        native_roles = {
            x["role"]: _mapping(x, "current native query role")
            for x in _sequence(native_preimage.get("query_roles"), "current native query roles")
        }
        logical_roles = {
            x["role"]: _mapping(x, "current shared logical query role")
            for x in _sequence(logical_semantics.get("query_roles"), "current shared logical query roles")
        }
        if set(role_bindings) != set(native_roles) or set(role_bindings) != set(logical_roles):
            raise LitsAstraSubstantiveParityError("current role identity topology contradiction")
        for role_name, binding_role in role_bindings.items():
            native_role = native_roles[role_name]
            logical_role = logical_roles[role_name]
            if canonicalize(binding_role.get("current_predicate_ref")) != canonicalize(native_role.get("predicate_ref")):
                raise LitsAstraSubstantiveParityError(f"current {role_name} predicate/native-preimage contradiction")
            if canonicalize(binding_role.get("current_query_ref")) != canonicalize(native_role.get("query_ref")):
                raise LitsAstraSubstantiveParityError(f"current {role_name} query/native-preimage contradiction")
            if binding_role.get("logical_query_template_id") != logical_role.get("query_template_id"):
                raise LitsAstraSubstantiveParityError(f"current {role_name} logical query-template contradiction")
            if canonicalize(binding_role.get("logical_condition_atom_ids")) != canonicalize(
                _mapping(logical_role.get("condition"), f"logical {role_name} condition").get("atom_ids")
            ):
                raise LitsAstraSubstantiveParityError(f"current {role_name} logical condition contradiction")

        if row.get("lane") == "P2":
            condition_predicate = role_bindings["CONDITION"].get("current_predicate_ref")
            if canonicalize(native_preimage.get("winning_predicate_ref")) != canonicalize(condition_predicate):
                raise LitsAstraSubstantiveParityError("current P2 winning/CONDITION predicate identity contradiction")

        if native_hash in by_native:
            raise LitsAstraSubstantiveParityError("duplicate current PRE553 native candidate hash")
        by_native[native_hash] = row
        logical_rows.append(canonicalize({
            "logical_candidate_key": key,
            "logical_candidate_material": material,
        }))
        provenance_rows.append(canonicalize({
            "lane": row.get("lane"),
            "logical_candidate_key": key,
            "pre553_i05_candidate_hash": native_hash,
            "role_bindings": row.get("role_bindings"),
        }))
    logical_rows = sorted(logical_rows, key=lambda x: x["logical_candidate_key"])
    if len(logical_rows) != 50 or len({x["logical_candidate_key"] for x in logical_rows}) != 50:
        raise LitsAstraSubstantiveParityError("current PRE553 logical candidate frontier is not exact unique 50")
    if len(provenance_rows) != 50:
        raise LitsAstraSubstantiveParityError("current PRE553 native provenance row count is not 50")
    provenance = canonicalize({
        "native_hash_domain": "PRE553_I05_CANDIDATE_HASH",
        "native_hash_equality_with_historical_required": False,
        "rows": sorted(provenance_rows, key=canonical_json),
    })
    return by_native, logical_rows, provenance


def _assert_current_binding_matches_receipt(
    receipt: Any,
    binding: Mapping[str, Any],
) -> None:
    identity = _mapping(receipt.candidate_identity, "current candidate identity")
    if identity.get("candidate_hash") != binding.get("current_pre553_candidate_hash"):
        raise LitsAstraSubstantiveParityError("current PRE553 binding/native hash mismatch")
    expected = {
        row["role"]: row
        for row in _sequence(binding.get("role_bindings"), "current logical role bindings")
    }
    actual = {
        row["role"]: row
        for row in _sequence(identity.get("query_roles"), "current receipt query roles")
    }
    if set(expected) != set(actual):
        raise LitsAstraSubstantiveParityError("current logical binding/receipt role-set mismatch")
    for role in expected:
        e = expected[role]
        a = _mapping(actual[role], f"current receipt role {role}")
        if canonicalize(a.get("predicate_ref")) != canonicalize(e.get("current_predicate_ref")):
            raise LitsAstraSubstantiveParityError(f"current {role} predicate identity drift")
        if canonicalize(a.get("query_ref")) != canonicalize(e.get("current_query_ref")):
            raise LitsAstraSubstantiveParityError(f"current {role} query identity drift")


def _role_rows_from_historical(
    product: Mapping[str, Any],
    roots: Mapping[str, Any],
    native_to_logical: Mapping[str, str],
    p4_cell_to_logical: Mapping[str, str],
) -> list[Mapping[str, Any]]:
    rows: list[Mapping[str, Any]] = []

    def add(lane: str, logical_key: str, role: str, root_id: str) -> None:
        rows.append(canonicalize({
            "lane": lane,
            "logical_candidate_key": logical_key,
            "role": role,
            "risk_set": root_id,
            "risk_set_count": roots[root_id]["count"],
            "risk_set_root": roots[root_id]["root"],
        }))

    for item in _sequence(product.get("P0_positive_controls"), "ASTRA P0"):
        add("P0", native_to_logical[item["candidate_hash"]], "BASE", "R2")

    p1 = _mapping(product.get("P1_joint_dependence"), "ASTRA P1")
    p1key = native_to_logical[p1["candidate_hash"]]
    add("P1", p1key, "JOINT", "R27")
    add("P1", p1key, "MARGINAL_0", "R2")
    add("P1", p1key, "MARGINAL_1", "R7")

    for item in _sequence(product.get("P2_conditioned_frontier"), "ASTRA P2"):
        key = native_to_logical[item["candidate_hash"]]
        add("P2", key, "BASELINE", "R7")
        add("P2", key, "CONDITION", "R7")

    p3 = _mapping(product.get("P3_conditional_reversal"), "ASTRA P3")
    p3key = native_to_logical[p3["candidate_hash"]]
    for role in P3_ROLES:
        add("P3", p3key, role, "R7")

    p4 = _mapping(product.get("P4_joint_5x5_target_support"), "ASTRA P4")
    for raw_cell in sorted(p4, key=lambda x: tuple(int(v) for v in x.split(","))):
        cell = [int(v) for v in raw_cell.split(",")]
        key = p4_cell_to_logical[canonical_json(cell)]
        add("P4", key, "BASE", "R27")

    return sorted(rows, key=canonical_json)

def normalize_accepted_astra_summary(
    *,
    product: Mapping[str, Any],
    role_receipt: Mapping[str, Any],
    replay_receipt: Mapping[str, Any],
) -> Mapping[str, Any]:
    product = _mapping(product, "ASTRA product")
    role_receipt = _mapping(role_receipt, "ASTRA role receipt")
    replay_receipt = _mapping(replay_receipt, "ASTRA replay receipt")
    if product.get("schema") != "ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0":
        raise LitsAstraSubstantiveParityError("unexpected ASTRA product schema")
    if role_receipt.get("schema") != "ASTRA_D04_R2_77_ROLE_EXECUTION_RECEIPT@1.0.0":
        raise LitsAstraSubstantiveParityError("unexpected ASTRA role receipt schema")
    if replay_receipt.get("schema") != "ASTRA_D04_R2_SOURCE_AND_REPLAY_RECEIPT@1.0.0":
        raise LitsAstraSubstantiveParityError("unexpected ASTRA replay receipt schema")

    source = _mapping(replay_receipt.get("source"), "ASTRA replay source")
    observed_source_identity = {
        "source": "LITS_I",
        "sha256": source.get("sha256"),
        "rows": source.get("rows"),
        "variables": source.get("variables"),
    }
    if observed_source_identity != ASTRA_SOURCE_IDENTITY:
        raise LitsAstraSubstantiveParityError("ASTRA historical source identity drift")

    frontier = _mapping(product.get("frontier"), "ASTRA frontier")
    preoutcome = _mapping(replay_receipt.get("preoutcome"), "ASTRA preoutcome")
    if (
        frontier.get("candidate_count") != 50
        or frontier.get("query_role_count") != 77
        or preoutcome.get("candidate_count") != 50
        or preoutcome.get("query_role_count") != 77
    ):
        raise LitsAstraSubstantiveParityError("ASTRA historical frontier is not exact 50/77")
    if frontier.get("preexecution_seal") != preoutcome.get("frontier_seal"):
        raise LitsAstraSubstantiveParityError("ASTRA historical frontier seal contradiction")

    lane_accounting = _mapping(product.get("lane_accounting"), "ASTRA lane accounting")
    roles_by_lane = _mapping(role_receipt.get("roles_by_lane"), "ASTRA roles_by_lane")
    for lane, expected in EXPECTED_LANE_COUNTS.items():
        lane_row = _mapping(lane_accounting.get(lane), f"ASTRA lane {lane}")
        if lane_row.get("candidate_count") != expected["candidate_count"]:
            raise LitsAstraSubstantiveParityError(f"ASTRA {lane} candidate count drift")
        if lane_row.get("query_role_count") != expected["query_role_count"]:
            raise LitsAstraSubstantiveParityError(f"ASTRA {lane} query-role count drift")
        if roles_by_lane.get(lane) != expected["query_role_count"]:
            raise LitsAstraSubstantiveParityError(f"ASTRA {lane} role receipt count drift")

    composition = _mapping(role_receipt.get("risk_set_composition"), "ASTRA risk composition")
    if composition.get("q301_2_roles") != "R2" or composition.get("q301_7_roles") != "R7":
        raise LitsAstraSubstantiveParityError("ASTRA marginal risk-set composition drift")
    if composition.get("joint_roles") != "R27":
        raise LitsAstraSubstantiveParityError("ASTRA joint risk-set composition drift")
    if composition.get("predictor_missingness_denominator_rule_added") is not False:
        raise LitsAstraSubstantiveParityError("ASTRA denominator law drift")

    roots = _historical_risk_roots(role_receipt, replay_receipt)
    selector_populations = _selector_populations(
        preoutcome.get("f02_selectors"),
        "ASTRA preoutcome f02_selectors",
        row_root_field="row_root",
    )
    (
        historical_native_to_logical,
        historical_p4_to_logical,
        logical_candidate_rows,
        native_candidate_provenance,
    ) = _historical_logical_identity(product)
    p0 = []
    recorded_logical_keys = []
    for item in _sequence(product.get("P0_positive_controls"), "ASTRA P0"):
        logical_key = historical_native_to_logical[item["candidate_hash"]]
        row = {
            "logical_candidate_key": logical_key,
            "target_cell": _cell(item["target_cell"]),
            "denominator": _integer(item["denominator"], "ASTRA P0 denominator"),
            "support": _integer(item["support"], "ASTRA P0 support"),
            "terminal_state": item["terminal_state"],
        }
        p0.append(row)
        recorded_logical_keys.append(row["logical_candidate_key"])
    p0.sort(key=lambda x: x["target_cell"])

    p1_raw = _mapping(product.get("P1_joint_dependence"), "ASTRA P1")
    p1_w = _mapping(p1_raw.get("first_exact_dependence_witness"), "ASTRA P1 witness")
    p1_logical_key = historical_native_to_logical[p1_raw["candidate_hash"]]
    p1 = {
        "logical_candidate_key": p1_logical_key,
        "terminal_state": p1_raw["terminal_state"],
        "first_exact_dependence_witness": {
            "cell": _cell(p1_w["cell"]),
            "joint_count": _integer(p1_w["joint_count"], "ASTRA P1 joint count"),
            "joint_denominator": _integer(p1_w["joint_denominator"], "ASTRA P1 joint denominator"),
            "marginal_0_count": _integer(p1_w["marginal_0_count"], "ASTRA P1 marginal 0 count"),
            "marginal_0_denominator": _integer(p1_w["marginal_0_denominator"], "ASTRA P1 marginal 0 denominator"),
            "marginal_1_count": _integer(p1_w["marginal_1_count"], "ASTRA P1 marginal 1 count"),
            "marginal_1_denominator": _integer(p1_w["marginal_1_denominator"], "ASTRA P1 marginal 1 denominator"),
        },
    }
    recorded_logical_keys.append(p1["logical_candidate_key"])
    p1_rel = p1["first_exact_dependence_witness"]
    if (
        p1_rel["joint_count"]
        * p1_rel["marginal_0_denominator"]
        * p1_rel["marginal_1_denominator"]
        == p1_rel["joint_denominator"]
        * p1_rel["marginal_0_count"]
        * p1_rel["marginal_1_count"]
    ):
        raise LitsAstraSubstantiveParityError(
            "ASTRA P1 recorded witness does not establish joint dependence"
        )

    p2 = []
    for item in _sequence(product.get("P2_conditioned_frontier"), "ASTRA P2"):
        witness = _mapping(item.get("first_exact_difference_witness"), "ASTRA P2 witness")
        params = _mapping(item.get("parameters"), "ASTRA P2 parameters")
        logical_key = historical_native_to_logical[item["candidate_hash"]]
        row = {
            "logical_candidate_key": logical_key,
            "parameters": {
                "q301_2": _integer(params.get("q301_2"), "ASTRA P2 q301_2"),
                "q310": _integer(params.get("q310"), "ASTRA P2 q310"),
                "q311": _integer(params.get("q311"), "ASTRA P2 q311"),
            },
            "terminal_state": item["terminal_state"],
            "first_exact_difference_witness": {
                "cell": _cell(witness["cell"]),
                "baseline_count": _integer(witness["baseline_count"], "ASTRA P2 baseline count"),
                "baseline_denominator": _integer(witness["baseline_denominator"], "ASTRA P2 baseline denominator"),
                "condition_count": _integer(witness["condition_count"], "ASTRA P2 condition count"),
                "condition_denominator": _integer(witness["condition_denominator"], "ASTRA P2 condition denominator"),
            },
        }
        p2.append(row)
        recorded_logical_keys.append(row["logical_candidate_key"])
    p2.sort(key=lambda x: x["logical_candidate_key"])

    p3_raw = _mapping(product.get("P3_conditional_reversal"), "ASTRA P3")
    p3_validation = _mapping(p3_raw.get("validation_details"), "ASTRA P3 validation")
    historical_rate_keys = {
        "POOLED_NEG": "POOLED_NEG",
        "POOLED_POS": "POOLED_POS",
        "Q310V1_NEG": "STRATUM:Q310V1:NEG",
        "Q310V1_POS": "STRATUM:Q310V1:POS",
        "Q310V2_NEG": "STRATUM:Q310V2:NEG",
        "Q310V2_POS": "STRATUM:Q310V2:POS",
        "Q310V3_NEG": "STRATUM:Q310V3:NEG",
        "Q310V3_POS": "STRATUM:Q310V3:POS",
    }
    historical_rates = _mapping(p3_validation.get("exact_rates"), "ASTRA P3 exact rates")
    if set(historical_rates) != set(historical_rate_keys):
        raise LitsAstraSubstantiveParityError("ASTRA P3 historical role-rate topology drift")
    exact_rates = {
        historical_rate_keys[role]: _fraction_material(value, f"ASTRA P3 {role}")
        for role, value in historical_rates.items()
    }
    computed_pooled_sign = _sign(
        _fraction_value(exact_rates["POOLED_POS"])
        - _fraction_value(exact_rates["POOLED_NEG"])
    )
    computed_stratum_signs = [
        _sign(
            _fraction_value(exact_rates[f"STRATUM:{stratum}:POS"])
            - _fraction_value(exact_rates[f"STRATUM:{stratum}:NEG"])
        )
        for stratum in ("Q310V1", "Q310V2", "Q310V3")
    ]
    recorded_pooled_sign = _integer(p3_validation["pooled_sign"], "ASTRA P3 pooled sign")
    recorded_stratum_signs = [
        _integer(x, "ASTRA P3 stratum sign") for x in p3_validation["stratum_signs"]
    ]
    if recorded_pooled_sign != computed_pooled_sign or recorded_stratum_signs != computed_stratum_signs:
        raise LitsAstraSubstantiveParityError("ASTRA P3 recorded signs contradict exact fractions")
    historical_reversal = (
        computed_pooled_sign != 0
        and bool(computed_stratum_signs)
        and all(sign != 0 and sign == computed_stratum_signs[0] for sign in computed_stratum_signs)
        and computed_stratum_signs[0] == -computed_pooled_sign
    )
    if p3_raw.get("terminal_state") != "EVALUATED_VALID_EMPTY" or historical_reversal:
        raise LitsAstraSubstantiveParityError("ASTRA P3 is not the accepted validation-negative valid-empty")
    p3_logical_key = historical_native_to_logical[p3_raw["candidate_hash"]]
    p3 = {
        "logical_candidate_key": p3_logical_key,
        "terminal_state": p3_raw["terminal_state"],
        "target_cell": _cell(p3_validation["target_cell"]),
        "exact_rates": canonicalize(exact_rates),
        "pooled_sign": recorded_pooled_sign,
        "stratum_signs": recorded_stratum_signs,
        "empty_mechanism": "VALIDATION_FALSE__NO_CONDITIONAL_REVERSAL",
    }
    recorded_logical_keys.append(p3["logical_candidate_key"])

    p4 = []
    for key, support in _mapping(product.get("P4_joint_5x5_target_support"), "ASTRA P4").items():
        cell = [int(v) for v in key.split(",")]
        if len(cell) != 2:
            raise LitsAstraSubstantiveParityError("ASTRA P4 cell arity drift")
        p4.append({
            "logical_candidate_key": historical_p4_to_logical[canonical_json(cell)],
            "target_cell": cell,
            "support": _integer(support, "ASTRA P4 support"),
        })
    p4.sort(key=lambda x: tuple(x["target_cell"]))

    terminal_counts = dict(_mapping(product.get("terminal_counts"), "ASTRA terminal counts"))
    if terminal_counts != EXPECTED_TERMINAL_COUNTS:
        raise LitsAstraSubstantiveParityError("ASTRA final terminal envelope drift")
    if role_receipt.get("role_count") != 77:
        raise LitsAstraSubstantiveParityError("ASTRA role count drift")
    if role_receipt.get("typed_role_states") != {"SUPPORTED": 77}:
        raise LitsAstraSubstantiveParityError("ASTRA role execution state drift")
    if role_receipt.get("role_result_reuse_count") != 0:
        raise LitsAstraSubstantiveParityError("ASTRA role reuse drift")

    return canonicalize({
        "schema": SUMMARY_SCHEMA,
        "frontier": {
            "candidate_count": 50,
            "query_role_count": 77,
            "frontier_seal": frontier["preexecution_seal"],
            "recorded_logical_candidate_keys": sorted(recorded_logical_keys),
            "lane_counts": EXPECTED_LANE_COUNTS,
        },
        "d03_risk_sets": roots,
        "f02_selector_populations": selector_populations,
        "role_execution": {
            "role_count": 77,
            "typed_role_states": {"SUPPORTED": 77},
            "role_result_reuse_count": 0,
            "roles_by_lane": {lane: EXPECTED_LANE_COUNTS[lane]["query_role_count"] for lane in EXPECTED_LANE_COUNTS},
        },
        "logical_candidate_identity": logical_candidate_rows,
        "native_candidate_provenance": native_candidate_provenance,
        "role_risk_set_topology": _role_rows_from_historical(
            product, roots, historical_native_to_logical, historical_p4_to_logical
        ),
        "P0": p0,
        "P1": p1,
        "P2": p2,
        "P3": p3,
        "P4": p4,
        "final_envelope": terminal_counts,
    })


def _fact_key(ref: Any) -> str:
    return exact_ref(ref, "current role fact ref").key


def _fact_cells(fact: Any) -> Mapping[str, tuple[Any, int]]:
    topology = _mapping(fact.target_topology, "current fact target_topology")
    rows = _sequence(topology.get("complete_cell_semantic_projection"), "current complete cell projection", allow_empty=True)
    out = {}
    for raw in rows:
        row = _mapping(raw, "current complete cell row")
        cell = _cell(row.get("cell"))
        key = canonical_json(cell)
        if key in out:
            raise LitsAstraSubstantiveParityError("duplicate current target cell")
        out[key] = (cell, _integer(row.get("raw_numerator_support"), "current cell support"))
    return out


def _role_fact(receipt: Any, role: str, facts_by_key: Mapping[str, Any]) -> Any:
    support = _mapping(receipt.support_uncertainty_state, "current support uncertainty state")
    refs_by_role = _mapping(support.get("query_role_fact_refs"), "current query_role_fact_refs")
    refs = _sequence(refs_by_role.get(role), f"current role {role} fact refs")
    if len(refs) != 1:
        raise LitsAstraSubstantiveParityError(f"current role {role} must resolve to exactly one LiTS fact")
    key = _fact_key(refs[0])
    if key not in facts_by_key:
        raise LitsAstraSubstantiveParityError(f"current role {role} fact preimage missing")
    return facts_by_key[key]


def _cell_support(fact: Any, target_cell: Any) -> int:
    key = canonical_json(_cell(target_cell))
    cells = _fact_cells(fact)
    if key not in cells:
        raise LitsAstraSubstantiveParityError(f"target cell {target_cell!r} absent from current fact topology")
    return cells[key][1]


def _first_distribution_difference(condition: Any, baseline: Any) -> Mapping[str, Any]:
    cc = _fact_cells(condition)
    bc = _fact_cells(baseline)
    if set(cc) != set(bc):
        raise LitsAstraSubstantiveParityError("P2 condition/baseline target domains differ")
    cd = _integer(condition.raw_denominator_support, "P2 condition denominator")
    bd = _integer(baseline.raw_denominator_support, "P2 baseline denominator")
    if cd <= 0 or bd <= 0:
        raise LitsAstraSubstantiveParityError("P2 accepted difference requires positive denominators")
    for key in sorted(cc, key=lambda k: canonical_json(cc[k][0])):
        cell, condition_count = cc[key]
        baseline_count = bc[key][1]
        if condition_count * bd != baseline_count * cd:
            return {
                "cell": cell,
                "baseline_count": baseline_count,
                "baseline_denominator": bd,
                "condition_count": condition_count,
                "condition_denominator": cd,
            }
    raise LitsAstraSubstantiveParityError("P2 candidate lacks exact first-difference witness")


def _first_joint_dependence(joint: Any, marginal_0: Any, marginal_1: Any) -> Mapping[str, Any]:
    jc = _fact_cells(joint)
    m0 = _fact_cells(marginal_0)
    m1 = _fact_cells(marginal_1)
    jd = _integer(joint.raw_denominator_support, "P1 joint denominator")
    d0 = _integer(marginal_0.raw_denominator_support, "P1 marginal 0 denominator")
    d1 = _integer(marginal_1.raw_denominator_support, "P1 marginal 1 denominator")
    if min(jd, d0, d1) <= 0:
        raise LitsAstraSubstantiveParityError("P1 accepted dependence requires positive denominators")
    rows = sorted(jc.values(), key=lambda x: tuple(x[0]))
    for cell, joint_count in rows:
        if not isinstance(cell, list) or len(cell) != 2:
            raise LitsAstraSubstantiveParityError("P1 joint cell arity drift")
        c0 = m0.get(canonical_json(cell[0]), (None, 0))[1]
        c1 = m1.get(canonical_json(cell[1]), (None, 0))[1]
        if joint_count * d0 * d1 != jd * c0 * c1:
            return {
                "cell": cell,
                "joint_count": joint_count,
                "joint_denominator": jd,
                "marginal_0_count": c0,
                "marginal_0_denominator": d0,
                "marginal_1_count": c1,
                "marginal_1_denominator": d1,
            }
    raise LitsAstraSubstantiveParityError("P1 current execution lacks exact dependence witness")


def _risk_members_count(fact: Any) -> int:
    refs = fact.semantic_fields.get("risk_set_member_refs")
    refs = _sequence(refs, "current risk_set_member_refs", allow_empty=True)
    return len(refs)


def _assert_role_risk(fact: Any, root_id: str, roots: Mapping[str, Any], label: str) -> None:
    observed = _risk_members_count(fact)
    expected = roots[root_id]["count"]
    if observed != expected:
        raise LitsAstraSubstantiveParityError(
            f"{label} executed over wrong risk set: observed risk members={observed}, expected {root_id}={expected}"
        )


def _current_role_topology_row(
    *, lane: str, key: Mapping[str, Any], role: str, root_id: str, fact: Any, roots: Mapping[str, Any]
) -> Mapping[str, Any]:
    _assert_role_risk(fact, root_id, roots, f"{lane}/{role}")
    return canonicalize({
        "lane": lane,
        **dict(key),
        "role": role,
        "risk_set": root_id,
        "risk_set_count": roots[root_id]["count"],
        "risk_set_root": roots[root_id]["root"],
    })


def normalize_current_lits_summary(
    *,
    result: Any,
    frontier_seal: str,
    selector_scan: Mapping[str, Any],
    logical_candidate_bindings: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any]:
    """Derive the ASTRA-shaped summary from the current candidate-neutral I05 result."""
    roots = _current_risk_roots()
    selector_populations = _selector_populations(
        selector_scan,
        "current F02 selector scan",
        row_root_field="row_semantic_root_sha256",
    )
    facts_by_key = {fact.ref.key: fact for fact in result.empirical_facts}
    receipts = sorted(result.receipts, key=lambda r: r.candidate_identity["candidate_hash"])
    candidate_count = _integer(result.candidate_count, "current candidate_count")
    role_count = sum(len(_sequence(r.candidate_identity.get("query_roles"), "current query roles")) for r in receipts)
    (
        current_binding_by_native,
        logical_candidate_rows,
        native_candidate_provenance,
    ) = _current_logical_identity(logical_candidate_bindings)
    receipt_hashes = {r.candidate_identity["candidate_hash"] for r in receipts}
    if receipt_hashes != set(current_binding_by_native):
        raise LitsAstraSubstantiveParityError(
            "current PRE553 execution receipts and source-free logical frontier bindings differ"
        )

    by_rule: dict[str, list[Any]] = {P0_RULE: [], P1_RULE: [], P2_RULE: [], P3_RULE: [], P4_RULE: []}
    terminal_counts = Counter()
    role_state_counts = Counter()
    role_rows: list[Mapping[str, Any]] = []
    recorded_logical_keys: list[str] = []

    for receipt in receipts:
        rule_id = receipt.candidate_identity.get("rule_id")
        if rule_id not in by_rule:
            raise LitsAstraSubstantiveParityError(f"current LiTS candidate outside frozen ASTRA rules: {rule_id!r}")
        binding = current_binding_by_native[receipt.candidate_identity["candidate_hash"]]
        _assert_current_binding_matches_receipt(receipt, binding)
        by_rule[rule_id].append(receipt)
        terminal_counts[receipt.coverage_state] += 1
        for role_row in _sequence(receipt.candidate_identity.get("query_roles"), "current query roles"):
            role = _mapping(role_row, "current query role").get("role")
            fact = _role_fact(receipt, role, facts_by_key)
            role_state_counts[fact.typed_state] += 1

    expected_rule_counts = {P0_RULE: 5, P1_RULE: 1, P2_RULE: 18, P3_RULE: 1, P4_RULE: 25}
    for rule_id, count in expected_rule_counts.items():
        if len(by_rule[rule_id]) != count:
            raise LitsAstraSubstantiveParityError(f"current {rule_id} candidate count drift")

    p0 = []
    for receipt in by_rule[P0_RULE]:
        identity = receipt.candidate_identity
        roles = [x["role"] for x in identity["query_roles"]]
        if roles != ["BASE"]:
            raise LitsAstraSubstantiveParityError("P0 exact role topology drift")
        fact = _role_fact(receipt, "BASE", facts_by_key)
        validation = _mapping(identity.get("validation"), "current P0 validation")
        target = _cell(validation.get("target_cell"))
        candidate_hash = identity["candidate_hash"]
        logical_key = current_binding_by_native[candidate_hash]["logical_candidate_key"]
        p0.append({
            "logical_candidate_key": logical_key,
            "target_cell": target,
            "denominator": _integer(fact.raw_denominator_support, "current P0 denominator"),
            "support": _cell_support(fact, target),
            "terminal_state": receipt.coverage_state,
        })
        recorded_logical_keys.append(logical_key)
        role_rows.append(_current_role_topology_row(
            lane="P0", key={"logical_candidate_key": logical_key}, role="BASE", root_id="R2", fact=fact, roots=roots
        ))
    p0.sort(key=lambda x: x["target_cell"])

    p1_receipt = by_rule[P1_RULE][0]
    p1_identity = p1_receipt.candidate_identity
    p1_hash = p1_identity["candidate_hash"]
    p1_logical_key = current_binding_by_native[p1_hash]["logical_candidate_key"]
    p1_roles = [x["role"] for x in p1_identity["query_roles"]]
    if p1_roles != ["JOINT", "MARGINAL_0", "MARGINAL_1"]:
        raise LitsAstraSubstantiveParityError("P1 exact role topology drift")
    p1_facts = {role: _role_fact(p1_receipt, role, facts_by_key) for role in p1_roles}
    p1 = {
        "logical_candidate_key": p1_logical_key,
        "terminal_state": p1_receipt.coverage_state,
        "first_exact_dependence_witness": _first_joint_dependence(
            p1_facts["JOINT"], p1_facts["MARGINAL_0"], p1_facts["MARGINAL_1"]
        ),
    }
    recorded_logical_keys.append(p1_logical_key)
    for role, root_id in (("JOINT", "R27"), ("MARGINAL_0", "R2"), ("MARGINAL_1", "R7")):
        role_rows.append(_current_role_topology_row(
            lane="P1", key={"logical_candidate_key": p1_logical_key}, role=role, root_id=root_id,
            fact=p1_facts[role], roots=roots
        ))

    p2 = []
    for receipt in by_rule[P2_RULE]:
        identity = receipt.candidate_identity
        roles = [x["role"] for x in identity["query_roles"]]
        if roles != ["CONDITION", "BASELINE"]:
            raise LitsAstraSubstantiveParityError("P2 exact role topology drift")
        condition = _role_fact(receipt, "CONDITION", facts_by_key)
        baseline = _role_fact(receipt, "BASELINE", facts_by_key)
        candidate_hash = identity["candidate_hash"]
        binding = current_binding_by_native[candidate_hash]
        logical_key = binding["logical_candidate_key"]
        semantics = _mapping(
            _mapping(binding["logical_candidate_material"], "P2 logical material").get("candidate_semantics"),
            "P2 logical candidate semantics",
        )
        parameters = _mapping(semantics.get("parameters"), "P2 logical parameters")
        p2.append({
            "logical_candidate_key": logical_key,
            "parameters": {
                "q301_2": _integer(parameters.get("q301_2"), "current P2 q301_2"),
                "q310": _integer(parameters.get("q310"), "current P2 q310"),
                "q311": _integer(parameters.get("q311"), "current P2 q311"),
            },
            "terminal_state": receipt.coverage_state,
            "first_exact_difference_witness": _first_distribution_difference(condition, baseline),
        })
        recorded_logical_keys.append(logical_key)
        for role, fact in (("BASELINE", baseline), ("CONDITION", condition)):
            role_rows.append(_current_role_topology_row(
                lane="P2", key={"logical_candidate_key": logical_key}, role=role, root_id="R7", fact=fact, roots=roots
            ))
    p2.sort(key=lambda x: x["logical_candidate_key"])

    p3_receipt = by_rule[P3_RULE][0]
    p3_identity = p3_receipt.candidate_identity
    p3_hash = p3_identity["candidate_hash"]
    p3_logical_key = current_binding_by_native[p3_hash]["logical_candidate_key"]
    roles = [x["role"] for x in p3_identity["query_roles"]]
    if set(roles) != set(P3_ROLES) or len(roles) != 8:
        raise LitsAstraSubstantiveParityError("P3 exact role topology drift")
    validation = _mapping(p3_identity.get("validation"), "current P3 validation")
    if validation.get("kind") != "CONDITIONAL_REVERSAL":
        raise LitsAstraSubstantiveParityError("P3 validator kind drift")
    target = _cell(validation.get("target_cell"))
    if p3_receipt.coverage_state != "EVALUATED_VALID_EMPTY" or p3_receipt.typed_state != "VALID_EMPTY":
        raise LitsAstraSubstantiveParityError("P3 terminal is not accepted valid-empty")
    p3_facts = {role: _role_fact(p3_receipt, role, facts_by_key) for role in P3_ROLES}
    for role, fact in p3_facts.items():
        if fact.typed_state != "SUPPORTED" or fact.raw_denominator_support <= 0:
            raise LitsAstraSubstantiveParityError(
                f"P3 valid-empty arose from non-supported role {role}, not the accepted false reversal validator"
            )
        role_rows.append(_current_role_topology_row(
            lane="P3", key={"logical_candidate_key": p3_logical_key}, role=role, root_id="R7", fact=fact, roots=roots
        ))
    rates = {
        role: _fraction_from_counts(_cell_support(fact, target), fact.raw_denominator_support, f"P3 {role}")
        for role, fact in p3_facts.items()
    }
    pooled_sign = _sign(_fraction_value(rates["POOLED_POS"]) - _fraction_value(rates["POOLED_NEG"]))
    strata = ("Q310V1", "Q310V2", "Q310V3")
    stratum_signs = [
        _sign(
            _fraction_value(rates[f"STRATUM:{stratum}:POS"])
            - _fraction_value(rates[f"STRATUM:{stratum}:NEG"])
        )
        for stratum in strata
    ]
    reversal = (
        pooled_sign != 0
        and bool(stratum_signs)
        and all(sign != 0 and sign == stratum_signs[0] for sign in stratum_signs)
        and stratum_signs[0] == -pooled_sign
    )
    if reversal:
        raise LitsAstraSubstantiveParityError("P3 is supported reversal, not accepted validation-negative valid-empty")
    p3 = {
        "logical_candidate_key": p3_logical_key,
        "terminal_state": p3_receipt.coverage_state,
        "target_cell": target,
        "exact_rates": canonicalize(rates),
        "pooled_sign": pooled_sign,
        "stratum_signs": stratum_signs,
        "empty_mechanism": "VALIDATION_FALSE__NO_CONDITIONAL_REVERSAL",
    }
    recorded_logical_keys.append(p3_logical_key)

    p4 = []
    for receipt in by_rule[P4_RULE]:
        identity = receipt.candidate_identity
        roles = [x["role"] for x in identity["query_roles"]]
        if roles != ["BASE"]:
            raise LitsAstraSubstantiveParityError("P4 exact role topology drift")
        validation = _mapping(identity.get("validation"), "current P4 validation")
        target = _cell(validation.get("target_cell"))
        if not isinstance(target, list) or len(target) != 2:
            raise LitsAstraSubstantiveParityError("P4 target topology drift")
        fact = _role_fact(receipt, "BASE", facts_by_key)
        candidate_hash = identity["candidate_hash"]
        logical_key = current_binding_by_native[candidate_hash]["logical_candidate_key"]
        p4.append({
            "logical_candidate_key": logical_key,
            "target_cell": target,
            "support": _cell_support(fact, target),
        })
        role_rows.append(_current_role_topology_row(
            lane="P4", key={"logical_candidate_key": logical_key}, role="BASE", root_id="R27", fact=fact, roots=roots
        ))
    p4.sort(key=lambda x: tuple(x["target_cell"]))

    roles_by_lane = {
        "P0": sum(len(r.candidate_identity["query_roles"]) for r in by_rule[P0_RULE]),
        "P1": sum(len(r.candidate_identity["query_roles"]) for r in by_rule[P1_RULE]),
        "P2": sum(len(r.candidate_identity["query_roles"]) for r in by_rule[P2_RULE]),
        "P3": sum(len(r.candidate_identity["query_roles"]) for r in by_rule[P3_RULE]),
        "P4": sum(len(r.candidate_identity["query_roles"]) for r in by_rule[P4_RULE]),
    }

    return canonicalize({
        "schema": SUMMARY_SCHEMA,
        "frontier": {
            "candidate_count": candidate_count,
            "query_role_count": role_count,
            "frontier_seal": frontier_seal,
            "recorded_logical_candidate_keys": sorted(recorded_logical_keys),
            "lane_counts": {
                lane: {
                    "candidate_count": len(by_rule[rule]),
                    "query_role_count": roles_by_lane[lane],
                }
                for lane, rule in (
                    ("P0", P0_RULE), ("P1", P1_RULE), ("P2", P2_RULE), ("P3", P3_RULE), ("P4", P4_RULE)
                )
            },
        },
        "d03_risk_sets": roots,
        "f02_selector_populations": selector_populations,
        "role_execution": {
            "role_count": role_count,
            "typed_role_states": dict(sorted(role_state_counts.items())),
            "role_result_reuse_count": 0,
            "roles_by_lane": roles_by_lane,
        },
        "logical_candidate_identity": logical_candidate_rows,
        "native_candidate_provenance": native_candidate_provenance,
        "role_risk_set_topology": sorted(role_rows, key=canonical_json),
        "P0": p0,
        "P1": p1,
        "P2": p2,
        "P3": p3,
        "P4": p4,
        "final_envelope": dict(sorted(terminal_counts.items())),
    })


def assert_substantive_parity(
    *,
    expected_summary: Mapping[str, Any],
    observed_summary: Mapping[str, Any],
    accepted_inputs: Sequence[Mapping[str, Any]],
    current_execution_identity: str,
    current_replay_identity: str,
) -> Mapping[str, Any]:
    expected = canonicalize(_mapping(expected_summary, "expected ASTRA summary"))
    observed = canonicalize(_mapping(observed_summary, "observed current summary"))
    if expected.get("schema") != SUMMARY_SCHEMA or observed.get("schema") != SUMMARY_SCHEMA:
        raise LitsAstraSubstantiveParityError("substantive parity summary schema drift")
    section_results = {}
    section_identities = {}
    for section in PARITY_SECTIONS:
        expected_section = canonicalize(expected.get(section))
        observed_section = canonicalize(observed.get(section))
        if expected_section != observed_section:
            raise LitsAstraSubstantiveParityError(
                f"LiTS current empirical substance drifted from accepted ASTRA section {section}"
            )
        section_results[section] = "PASS"
        section_identities[section] = {
            "status": "PASS",
            "expected_identity": semantic_hash(expected_section),
            "observed_identity": semantic_hash(observed_section),
        }

    historical_provenance = _mapping(
        expected.get("native_candidate_provenance"), "historical native candidate provenance"
    )
    current_provenance = _mapping(
        observed.get("native_candidate_provenance"), "current native candidate provenance"
    )
    if historical_provenance.get("native_hash_domain") != "G02_EXECUTION_CANDIDATE_HASH":
        raise LitsAstraSubstantiveParityError("historical candidate provenance domain drift")
    if current_provenance.get("native_hash_domain") != "PRE553_I05_CANDIDATE_HASH":
        raise LitsAstraSubstantiveParityError("current candidate provenance domain drift")
    historical_rows = {
        row["logical_candidate_key"]: row
        for row in _sequence(historical_provenance.get("rows"), "historical native provenance rows")
    }
    current_rows = {
        row["logical_candidate_key"]: row
        for row in _sequence(current_provenance.get("rows"), "current native provenance rows")
    }
    if len(historical_rows) != 50 or len(current_rows) != 50 or set(historical_rows) != set(current_rows):
        raise LitsAstraSubstantiveParityError(
            "historical/current native provenance is not bound to the same 50 logical candidates"
        )
    for logical_key in historical_rows:
        historical_hash = historical_rows[logical_key].get("g02_execution_candidate_hash")
        current_hash = current_rows[logical_key].get("pre553_i05_candidate_hash")
        if historical_hash == current_hash:
            raise LitsAstraSubstantiveParityError(
                "G02 and PRE553 native candidate identities must remain distinct provenance identities"
            )
        lane = current_rows[logical_key].get("lane")
        bindings = _sequence(current_rows[logical_key].get("role_bindings"), "current role bindings")
        if lane == "P2":
            by_role = {row["role"]: row for row in bindings}
            if set(by_role) != {"CONDITION", "BASELINE"}:
                raise LitsAstraSubstantiveParityError("P2 CONDITION/BASELINE binding topology missing")
            for role in ("CONDITION", "BASELINE"):
                for ref_name in ("current_predicate_ref", "current_query_ref"):
                    ref = _mapping(by_role[role].get(ref_name), f"P2 {role} {ref_name}")
                    if not isinstance(ref.get("content_hash"), str) or len(ref["content_hash"]) != 64:
                        raise LitsAstraSubstantiveParityError(
                            f"P2 {role} exact predicate/query identity malformed"
                        )

    if not isinstance(current_execution_identity, str) or len(current_execution_identity) != 64:
        raise LitsAstraSubstantiveParityError("current execution identity malformed")
    if not isinstance(current_replay_identity, str) or len(current_replay_identity) != 64:
        raise LitsAstraSubstantiveParityError("current replay identity malformed")

    expected_projection = canonicalize({section: expected[section] for section in PARITY_SECTIONS})
    observed_projection = canonicalize({section: observed[section] for section in PARITY_SECTIONS})
    expected_identity = semantic_hash(expected_projection)
    observed_identity = semantic_hash(observed_projection)
    if expected_identity != observed_identity:
        raise LitsAstraSubstantiveParityError("cross-schema logical parity projection identity mismatch")
    expected_document_identity = semantic_hash(expected)
    observed_document_identity = semantic_hash(observed)

    receipt = {
        "schema": PARITY_RECEIPT_SCHEMA,
        "status": "PASS__CURRENT_LITS_EMPIRICAL_SUBSTANCE_EXACTLY_CONSERVES_ACCEPTED_ASTRA_D04_R2",
        "accepted_astra_inputs": canonicalize(list(accepted_inputs)),
        "accepted_astra_source_identity": ASTRA_SOURCE_IDENTITY,
        "current_d03_authority_content_hash": D03_AUTHORITY_CONTENT_HASH,
        "current_execution_identity": current_execution_identity,
        "current_replay_identity": current_replay_identity,
        "expected_empirical_summary_identity": expected_identity,
        "observed_empirical_summary_identity": observed_identity,
        "empirical_summary_identity_scope": "PARITY_SECTIONS_WITH_CROSS_SCHEMA_LOGICAL_CANDIDATE_IDENTITY",
        "expected_summary_document_identity": expected_document_identity,
        "observed_summary_document_identity": observed_document_identity,
        "historical_native_candidate_hash_domain": "G02_EXECUTION_CANDIDATE_HASH",
        "current_native_candidate_hash_domain": "PRE553_I05_CANDIDATE_HASH",
        "native_candidate_hash_equality_required": False,
        "cross_schema_logical_candidate_key_required": True,
        "section_results": section_results,
        "section_identities": section_identities,
        "historical_current_whole_object_hash_equality_required": False,
        "whole_object_hashes_compared_across_schema_domains": False,
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_state_reused": False,
        "oracle_freeze_authorized": True,
    }
    receipt["parity_receipt_identity"] = semantic_hash(receipt)
    return canonicalize(receipt)


__all__ = [
    "D03_AUTHORITY_CONTENT_HASH",
    "LitsAstraSubstantiveParityError",
    "PARITY_RECEIPT_SCHEMA",
    "PARITY_SECTIONS",
    "SUMMARY_SCHEMA",
    "assert_substantive_parity",
    "normalize_accepted_astra_summary",
    "normalize_current_lits_summary",
]
