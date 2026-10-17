"""Cross-schema logical candidate identity for LiTS ASTRA/G02 <-> current PRE553.

Historical G02 execution-candidate hashes and current PRE553 I05 candidate hashes
are native provenance identities in different canonical domains.  This module
defines a third, shared logical identity from the frozen D02 candidate semantics
that both domains independently realize.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_discovery_exact import I05_CONTRACT_ID
from rawlsing_next.pre553_empirical_objects import canonical_json, canonicalize, semantic_hash


LOGICAL_CONTRACT = "FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0"
G02_CONTRACT_ID = "PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_REAL_EXECUTION_AND_REPLAY_R2@1.0.0"
G02_D02_FRONTIER_BLOB = "5399a3f64642c8d9f8a0644db0adc15d38642971"
G02_F02_FRONTIER_READOPTION_HASH = "07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851"

P0_RULE = "D02_P0_REAL_POSITIVE_CONTROL"
P1_RULE = "D02_P1_JOINT_DEPENDENCE"
P2_RULE = "D02_P2_HIGHER_ORDER_K3"
P3_RULE = "D02_P3_CONDITIONAL_REVERSAL"
P4_RULE = "D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS"

RULE_TO_LANE = {
    P0_RULE: "P0",
    P1_RULE: "P1",
    P2_RULE: "P2",
    P3_RULE: "P3",
    P4_RULE: "P4",
}

ATOM_REFS = {
    "A000": "ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0",
    "A1V1": "082157ea8f31fe0d209c6241552116108e3e3917f7ddb7a49fa365ad5362aeeb",
    "A1V5": "9ba962d35fc630686b7538ae22dbabe2f5b51fe8c7b3473beab901214b1db43c",
    "Q310V1": "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "Q310V2": "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "Q310V3": "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "Q311V1": "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "Q311V2": "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "Q311V3": "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}
QUERY_REFS = {
    "T_Q301_2_RAW": "8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44",
    "T_Q301_7_RAW": "deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7",
    "T_Q301_2_Q301_7_RAW": "ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053",
}
SAME_RESPONDENT_BINDING = "EXACT_SOURCE_ROW_WITHIN_F02_COMPOSITE_RELEASE"

FAMILY_BY_RULE = {
    P0_RULE: "BOUNDED_K_WAY_RESPONSE_CONFIGURATION",
    P1_RULE: "PAIR_RESPONSE_COTRAVEL",
    P2_RULE: "BOUNDED_K_WAY_RESPONSE_CONFIGURATION",
    P3_RULE: "CONDITIONAL_REVERSAL_OR_SIMPSON",
    P4_RULE: "MINORITY_OR_NONMODAL_DEPARTURE",
}
FORM_BY_RULE = {
    P0_RULE: "BASE_QUERY",
    P1_RULE: "JOINT_DEPENDENCE",
    P2_RULE: "AND_CARTESIAN_GROUPS",
    P3_RULE: "REVERSAL_GRID",
    P4_RULE: "BASE_QUERY",
}


class CrossSchemaCandidateIdentityError(RuntimeError):
    pass


def _exact_decimal(value: int) -> Mapping[str, str]:
    if type(value) is not int:
        raise CrossSchemaCandidateIdentityError("exact decimal candidate value must be int")
    return {"$exact_decimal": str(value)}


def _exact_int(value: Any, label: str) -> int:
    if type(value) is int:
        return value
    if isinstance(value, Mapping) and set(value) == {"$exact_decimal"}:
        raw = value["$exact_decimal"]
        if isinstance(raw, str) and raw.lstrip("-").isdigit():
            return int(raw)
    raise CrossSchemaCandidateIdentityError(f"{label} is not an exact integer value")


def _ref(kind: str, digest: str) -> Mapping[str, str]:
    return {
        "kind": kind,
        "object_id": f"urn:rawlsing:pre553:{kind.split('@', 1)[0]}:sha256:{digest}",
        "content_hash": digest,
    }


def _condition(atom_ids: Sequence[str]) -> Mapping[str, Any]:
    ids = list(atom_ids)
    if not ids or any(atom not in ATOM_REFS for atom in ids):
        raise CrossSchemaCandidateIdentityError("logical condition contains unknown/empty atom set")
    return {
        "op": "AND" if len(ids) > 1 else "ATOM",
        "atom_ids": ids,
        "atom_refs": [_ref("EmpiricalPredicate@1.0.0", ATOM_REFS[a]) for a in ids],
        "same_respondent_binding": SAME_RESPONDENT_BINDING,
    }


def _role(role: str, query_template_id: str, atom_ids: Sequence[str]) -> Mapping[str, Any]:
    if query_template_id not in QUERY_REFS:
        raise CrossSchemaCandidateIdentityError("unknown logical query template")
    return {
        "role": role,
        "query_template_id": query_template_id,
        "query_template_ref": _ref("EmpiricalQuerySpec@1.0.0", QUERY_REFS[query_template_id]),
        "condition": _condition(atom_ids),
    }


def candidate_semantics(*, lane: str, parameters: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
    """Return the exact shared logical candidate semantics for one frozen lane member."""
    p = dict(parameters or {})
    if lane == "P0":
        cell = _exact_int(p.get("target_cell"), "P0 target_cell")
        if cell not in range(1, 6):
            raise CrossSchemaCandidateIdentityError("P0 target cell outside 1..5")
        rule = P0_RULE
        params = {"target_cell": _exact_decimal(cell)}
        validation = {"kind": "TARGET_CELL_SUPPORTED", "target_cell": _exact_decimal(cell)}
        roles = [_role("BASE", "T_Q301_2_RAW", ["A000"])]
    elif lane == "P1":
        if p:
            raise CrossSchemaCandidateIdentityError("P1 parameters must be empty")
        rule = P1_RULE
        params = {}
        validation = {"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"}
        roles = [
            _role("JOINT", "T_Q301_2_Q301_7_RAW", ["A000"]),
            _role("MARGINAL_0", "T_Q301_2_RAW", ["A000"]),
            _role("MARGINAL_1", "T_Q301_7_RAW", ["A000"]),
        ]
    elif lane == "P2":
        q2 = _exact_int(p.get("q301_2"), "P2 q301_2")
        q310 = _exact_int(p.get("q310"), "P2 q310")
        q311 = _exact_int(p.get("q311"), "P2 q311")
        if q2 not in (1, 5) or q310 not in (1, 2, 3) or q311 not in (1, 2, 3):
            raise CrossSchemaCandidateIdentityError("P2 parameter tuple outside frozen Cartesian frontier")
        rule = P2_RULE
        params = {"q301_2": q2, "q310": q310, "q311": q311}
        atoms = [f"A1V{q2}", f"Q310V{q310}", f"Q311V{q311}"]
        validation = {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}
        roles = [
            _role("CONDITION", "T_Q301_7_RAW", atoms),
            _role("BASELINE", "T_Q301_7_RAW", ["A000"]),
        ]
    elif lane == "P3":
        if p and p != {"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]}:
            raise CrossSchemaCandidateIdentityError("P3 parameters drift")
        rule = P3_RULE
        params = {"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]}
        validation = {"kind": "CONDITIONAL_REVERSAL", "target_cell": _exact_decimal(5)}
        roles = [
            _role("POOLED_POS", "T_Q301_7_RAW", ["A1V5"]),
            _role("POOLED_NEG", "T_Q301_7_RAW", ["A1V1"]),
        ]
        for q310 in (1, 2, 3):
            roles.extend([
                _role(f"STRATUM:Q310V{q310}:POS", "T_Q301_7_RAW", [f"Q310V{q310}", "A1V5"]),
                _role(f"STRATUM:Q310V{q310}:NEG", "T_Q301_7_RAW", [f"Q310V{q310}", "A1V1"]),
            ])
    elif lane == "P4":
        cell = p.get("target_cell")
        if not isinstance(cell, Sequence) or isinstance(cell, (str, bytes)) or len(cell) != 2:
            raise CrossSchemaCandidateIdentityError("P4 target cell must have arity 2")
        q2, q7 = (_exact_int(cell[0], "P4 q301_2"), _exact_int(cell[1], "P4 q301_7"))
        if q2 not in range(1, 6) or q7 not in range(1, 6):
            raise CrossSchemaCandidateIdentityError("P4 target cell outside 5x5 domain")
        rule = P4_RULE
        target = [_exact_decimal(q2), _exact_decimal(q7)]
        params = {"target_cell": target}
        validation = {"kind": "TARGET_CELL_SUPPORTED", "target_cell": target}
        roles = [_role("BASE", "T_Q301_2_Q301_7_RAW", ["A000"])]
    else:
        raise CrossSchemaCandidateIdentityError(f"unknown logical lane {lane!r}")

    return canonicalize({
        "lane": lane,
        "rule_id": rule,
        "family": FAMILY_BY_RULE[rule],
        "form": FORM_BY_RULE[rule],
        "parameters": params,
        "validation": validation,
        "query_roles": roles,
    })


def logical_candidate_material(semantics: Mapping[str, Any]) -> Mapping[str, Any]:
    return canonicalize({"contract": LOGICAL_CONTRACT, "candidate_semantics": canonicalize(semantics)})


def logical_candidate_key(semantics: Mapping[str, Any]) -> str:
    return semantic_hash(logical_candidate_material(semantics))


def g02_execution_candidate_hash(semantics: Mapping[str, Any]) -> str:
    """Recompute the native G02 hash from its accepted producer preimage."""
    return semantic_hash({
        "contract": G02_CONTRACT_ID,
        "d02_frontier_blob": G02_D02_FRONTIER_BLOB,
        "f02_frontier_readoption_hash": G02_F02_FRONTIER_READOPTION_HASH,
        "candidate_semantics": canonicalize(semantics),
    })


def _ast_contains(tree: Any, target: Any) -> bool:
    if canonical_json(tree) == canonical_json(target):
        return True
    if isinstance(tree, Mapping):
        return any(_ast_contains(v, target) for v in tree.values())
    if isinstance(tree, Sequence) and not isinstance(tree, (str, bytes)):
        return any(_ast_contains(v, target) for v in tree)
    return False


def _atoms_in_predicate(predicate: Any, primitives: Mapping[str, Any]) -> set[str]:
    tree = predicate.predicate_ast
    found = {
        atom_id
        for atom_id, primitive in primitives.items()
        if atom_id in ATOM_REFS and _ast_contains(tree, primitive.predicate_ast)
    }
    return found


def _query_semantics_without_condition(query: Any) -> Mapping[str, Any]:
    fields = dict(query.semantic_fields)
    fields.pop("condition_predicate_ref", None)
    return canonicalize(fields)


def _binding_for_current_candidate(candidate: Any, primitives: Mapping[str, Any], queries: Mapping[str, Any]) -> Mapping[str, Any]:
    if candidate.rule_id not in RULE_TO_LANE:
        raise CrossSchemaCandidateIdentityError("current candidate outside frozen D02 rules")
    lane = RULE_TO_LANE[candidate.rule_id]

    if lane in {"P0", "P4"}:
        params = {"target_cell": candidate.validation.get("target_cell")}
    elif lane == "P1":
        params = {}
    elif lane == "P2":
        condition_role = next((x for x in candidate.query_roles if x.role == "CONDITION"), None)
        if condition_role is None:
            raise CrossSchemaCandidateIdentityError("current P2 CONDITION role absent")
        found = _atoms_in_predicate(condition_role.predicate, primitives)
        q2 = [x for x in ("A1V1", "A1V5") if x in found]
        q310 = [x for x in ("Q310V1", "Q310V2", "Q310V3") if x in found]
        q311 = [x for x in ("Q311V1", "Q311V2", "Q311V3") if x in found]
        if len(q2) != 1 or len(q310) != 1 or len(q311) != 1:
            raise CrossSchemaCandidateIdentityError(
                f"current P2 CONDITION does not expose exact frozen atom tuple: {sorted(found)!r}"
            )
        extras = found - {"A000", q2[0], q310[0], q311[0]}
        if extras:
            raise CrossSchemaCandidateIdentityError(f"current P2 CONDITION has extra frozen atoms: {sorted(extras)!r}")
        params = {
            "q301_2": int(q2[0][-1]),
            "q310": int(q310[0][-1]),
            "q311": int(q311[0][-1]),
        }
    else:
        params = {"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]}

    semantics = candidate_semantics(lane=lane, parameters=params)
    if candidate.family != semantics["family"] or candidate.rule_id != semantics["rule_id"]:
        raise CrossSchemaCandidateIdentityError("current candidate family/rule drift")
    if canonicalize(candidate.validation) != canonicalize(semantics["validation"]):
        raise CrossSchemaCandidateIdentityError("current candidate validation drift from shared logical semantics")

    current_by_role = {x.role: x for x in candidate.query_roles}
    expected_roles = semantics["query_roles"]
    if set(current_by_role) != {x["role"] for x in expected_roles}:
        raise CrossSchemaCandidateIdentityError("current candidate role topology drift")

    role_bindings = []
    for expected in expected_roles:
        role = current_by_role[expected["role"]]
        template_id = expected["query_template_id"]
        template = queries.get(template_id)
        if template is None:
            raise CrossSchemaCandidateIdentityError(f"current query template missing: {template_id}")
        if _query_semantics_without_condition(role.query) != _query_semantics_without_condition(template):
            raise CrossSchemaCandidateIdentityError(
                f"current {lane}/{role.role} query semantics drift from frozen template {template_id}"
            )
        found = _atoms_in_predicate(role.predicate, primitives)
        required = set(expected["condition"]["atom_ids"])
        # Current PRE553 composes the universal A000 baseline into generated
        # conditions where historical G02 treated it as an implicit universe.
        allowed = set(required)
        allowed.add("A000")
        if not required <= found or not found <= allowed:
            raise CrossSchemaCandidateIdentityError(
                f"current {lane}/{role.role} condition atoms drift: expected={sorted(required)!r} "
                f"observed={sorted(found)!r}"
            )
        role_bindings.append({
            "role": role.role,
            "logical_query_template_id": template_id,
            "logical_condition_atom_ids": list(expected["condition"]["atom_ids"]),
            "current_predicate_ref": role.predicate.ref.as_dict(),
            "current_query_ref": role.query.ref.as_dict(),
        })

    native_preimage = canonicalize({
        "contract": I05_CONTRACT_ID,
        "family": candidate.family,
        "rule_id": candidate.rule_id,
        "winning_predicate_ref": candidate.winning_predicate.ref.as_dict(),
        "query_roles": [
            {
                "role": role.role,
                "predicate_ref": role.predicate.ref.as_dict(),
                "query_ref": role.query.ref.as_dict(),
            }
            for role in candidate.query_roles
        ],
        "validation": candidate.validation,
        "ancestry_refs": [ref.as_dict() for ref in candidate.ancestry_refs],
    })
    recomputed_native = semantic_hash(native_preimage)
    if recomputed_native != candidate.candidate_hash:
        raise CrossSchemaCandidateIdentityError("current PRE553 native candidate hash/preimage contradiction")
    expected_candidate_id = f"urn:rawlsing:pre553:i05:candidate:sha256:{recomputed_native}"
    if candidate.candidate_id != expected_candidate_id:
        raise CrossSchemaCandidateIdentityError("current PRE553 native candidate id/hash contradiction")

    key = logical_candidate_key(semantics)
    binding = canonicalize({
        "logical_candidate_key": key,
        "logical_candidate_material": logical_candidate_material(semantics),
        "current_pre553_candidate_hash": candidate.candidate_hash,
        "current_pre553_candidate_id": candidate.candidate_id,
        "current_pre553_native_candidate_preimage": native_preimage,
        "rule_id": candidate.rule_id,
        "lane": lane,
        "role_bindings": role_bindings,
    })
    return canonicalize({
        **binding,
        "binding_identity": semantic_hash(binding),
    })


def current_pre553_logical_candidate_bindings(
    *,
    candidates: Sequence[Any],
    primitives: Mapping[str, Any],
    queries: Mapping[str, Any],
) -> tuple[Mapping[str, Any], ...]:
    bindings = tuple(
        sorted(
            (_binding_for_current_candidate(c, primitives, queries) for c in candidates),
            key=lambda x: x["logical_candidate_key"],
        )
    )
    if len(bindings) != 50:
        raise CrossSchemaCandidateIdentityError("current PRE553 logical frontier must contain exactly 50 candidates")
    keys = [x["logical_candidate_key"] for x in bindings]
    native = [x["current_pre553_candidate_hash"] for x in bindings]
    if len(set(keys)) != 50 or len(set(native)) != 50:
        raise CrossSchemaCandidateIdentityError("current PRE553 logical/native candidate identities are not unique")
    return bindings


__all__ = [
    "LOGICAL_CONTRACT",
    "G02_CONTRACT_ID",
    "G02_D02_FRONTIER_BLOB",
    "G02_F02_FRONTIER_READOPTION_HASH",
    "P0_RULE", "P1_RULE", "P2_RULE", "P3_RULE", "P4_RULE",
    "RULE_TO_LANE", "ATOM_REFS", "QUERY_REFS",
    "CrossSchemaCandidateIdentityError",
    "candidate_semantics",
    "logical_candidate_material",
    "logical_candidate_key",
    "g02_execution_candidate_hash",
    "current_pre553_logical_candidate_bindings",
]
