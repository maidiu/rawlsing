"""Conditional R1L-C repair machinery for the WVS7 P2F2 validation-authority defect.

This module is deliberately inert.  It does not adopt a successor authority or
Lock2 on import, does not execute I05, and does not inspect empirical outcomes.
Fan-in must first provide independently accepted R1L-A provenance and R1L-B
succession holdings.  Only then can these deterministic constructors be used.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    materialize_public_object,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    ExactRef,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)


CONTRACT_ID = "FIABC_LM2_R1L_C_VALIDATION_AUTHORITY_SUCCESSOR_PREP@1.0.0"
ACTIVATION_SCHEMA = "FIABC_LM2_R1L_VALIDATION_PROVENANCE_ACTIVATION@1.0.0"
SUCCESSION_SCHEMA = "FIABC_LM2_R1L_LOCK2_SUCCESSION_ACTIVATION@1.0.0"
SUCCESSOR_REPLAY_KIND = "FIABC_LM2_R1L_DISCOVERY_AUTHORITY_SUCCESSOR_REPLAY@1.0.0"
LOCK2_PREP_SCHEMA = "FIABC_LM2_R1L_LOCK2_SUCCESSOR_PREPARATION@1.0.0"
PACKAGE_PREP_SCHEMA = "FIABC_LM2_R1L_RUNTIME_PACKAGE_SUCCESSOR_PREPARATION@1.0.0"

SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
PREDECESSOR_DISCOVERY_HASH = "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab"
CANDIDATE_GRAMMAR_HASH = "a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6"
PREDECESSOR_LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
PREDECESSOR_REPLAY = "b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490"

CANONICAL_VALIDATION_KINDS = tuple(sorted((
    "TARGET_CELL_SUPPORTED",
    "JOINT_NOT_PRODUCT_OF_MARGINALS",
    "DISTRIBUTION_DIFFERS_FROM_BASELINE",
)))
EXPECTED_FAMILY_COUNTS = {
    "BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25,
    "BRANCH_CONDITIONED_DISTRIBUTION": 10,
    "PAIR_RESPONSE_COTRAVEL": 1,
    "UNARY_SOCIAL_FORK": 10,
}
EXPECTED_COUNTS = {
    "authorities": 6,
    "predicates": 11,
    "queries": 3,
    "discovery_authorities": 1,
    "candidates": 46,
}
ALLOWED_STABLE_CLASSIFICATIONS = frozenset({
    "MAY_REMAIN_EXACT",
    "MUST_REPLAY_BUT_EXPECTED_SAME",
    "OUTSIDE_INVALIDATION",
})


class ValidationAuthorityRepairError(ValueError):
    """Conditional repair input is not authorized or not exactly conserved."""


@dataclass(frozen=True)
class FrozenP2F2Context:
    package: Mapping[str, Any]
    catalog: RuntimeObjectCatalog
    predecessor: DiscoveryAuthority
    candidate_hashes: tuple[str, ...]
    family_counts: Mapping[str, int]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationAuthorityRepairError(message)


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _validation_inventory(grammar: Mapping[str, Any]) -> tuple[str, ...]:
    rules = grammar.get("rules")
    _require(
        isinstance(rules, Sequence) and not isinstance(rules, (str, bytes, bytearray)),
        "candidate grammar rules must be an exact sequence",
    )
    kinds: set[str] = set()
    for rule in rules:
        _require(isinstance(rule, Mapping), "candidate grammar rule must be a mapping")
        validation = rule.get("validation")
        _require(isinstance(validation, Mapping), "candidate grammar validation must be a mapping")
        kind = validation.get("kind")
        _require(isinstance(kind, str) and kind, "candidate grammar validation kind missing")
        kinds.add(kind)
    return tuple(sorted(kinds))


def validate_requested_validation_kinds(
    requested: Iterable[str],
    *,
    independently_authorized: Iterable[str],
    grammar_used: Iterable[str] = CANONICAL_VALIDATION_KINDS,
) -> tuple[str, ...]:
    """Validate one exact minimal validation-kind envelope.

    Independently-authorized kinds are an authority ceiling, not an invitation
    to enlarge this repair.  The successor is deliberately exact to the frozen
    grammar's used kinds.
    """
    req = tuple(sorted(set(requested)))
    auth = frozenset(independently_authorized)
    used = tuple(sorted(set(grammar_used)))
    _require(req == used, "successor validation envelope must equal exact frozen grammar use")
    _require(set(req) <= auth, "requested validation kind lacks independent pre-outcome authority")
    for value in req:
        upper = value.upper()
        _require(value not in {"*", "ALL"}, "wildcard/ALL validation authority forbidden")
        _require("*" not in value and upper != "ANY", "adaptive/wildcard validation authority forbidden")
    _require(req == CANONICAL_VALIDATION_KINDS, "R1L-C minimal repair admits only the exact three frozen kinds")
    return req


def validate_frozen_p2f2_package(package: Mapping[str, Any]) -> FrozenP2F2Context:
    _require(isinstance(package, Mapping), "P2F2 runtime package must be a mapping")
    _require(package.get("source_sha256") == SOURCE_SHA256, "WVS7 source identity drift")
    _require(package.get("lock2") == PREDECESSOR_LOCK2, "predecessor Lock2 drift")
    _require(package.get("replay") == PREDECESSOR_REPLAY, "predecessor replay drift")
    _require(package.get("discovery_authority_hash") == PREDECESSOR_DISCOVERY_HASH,
             "predecessor DiscoveryAuthority drift")
    _require(package.get("counts") == EXPECTED_COUNTS, "P2F2 runtime-package cardinality drift")

    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=package.get("authority_documents", ()),
        predicate_documents=package.get("predicate_documents", ()),
        query_documents=package.get("query_documents", ()),
        discovery_authority_documents=package.get("discovery_authority_documents", ()),
    )
    _require(len(catalog.discovery_authorities) == 1, "exactly one frozen DiscoveryAuthority required")
    predecessor = catalog.discovery_authorities[0]
    _require(predecessor.content_hash == PREDECESSOR_DISCOVERY_HASH,
             "frozen DiscoveryAuthority exact identity mismatch")
    grammar_ref = exact_ref(predecessor.candidate_grammar_ref, "candidate_grammar_ref")
    _require(grammar_ref.content_hash == CANDIDATE_GRAMMAR_HASH, "candidate grammar identity drift")
    grammar = predecessor.candidate_universe_definition
    _require(_validation_inventory(grammar) == CANONICAL_VALIDATION_KINDS,
             "frozen candidate grammar validation-kind inventory drift")
    rules = predecessor.validation_rules
    _require(isinstance(rules, Mapping), "predecessor validation_rules malformed")
    _require("kinds" not in rules, "predecessor defect unexpectedly absent; do not layer successor twice")

    receipt = package.get("lock2_receipt")
    _require(isinstance(receipt, Mapping), "Lock2 issuer receipt missing")
    _require(receipt.get("lock2_hash") == PREDECESSOR_LOCK2, "Lock2 receipt identity drift")
    material = receipt.get("lock2_material")
    _require(isinstance(material, Mapping), "Lock2 material missing")
    _require(material.get("discovery_authority_ref") == predecessor.ref.as_dict(),
             "Lock2 material does not bind exact predecessor DiscoveryAuthority")
    _require(material.get("candidate_grammar_ref") == grammar_ref.as_dict(),
             "Lock2 material candidate grammar drift")
    hashes = tuple(material.get("candidate_hashes", ()))
    _require(len(hashes) == 46 and len(set(hashes)) == 46, "exact 46-candidate frontier required")
    _require(tuple(sorted(hashes)) == hashes, "candidate hashes must retain canonical order")
    _require(all(_is_sha256(h) for h in hashes), "candidate hash malformed")
    family_counts = receipt.get("family_counts")
    _require(family_counts == EXPECTED_FAMILY_COUNTS, "candidate family shape drift")

    replay_currentness = package.get("replay_currentness")
    _require(isinstance(replay_currentness, Mapping), "replay currentness missing")
    _require(replay_currentness.get("replay_hash") == PREDECESSOR_REPLAY,
             "replay currentness identity drift")
    replay_binding = replay_currentness.get("replay_binding")
    _require(isinstance(replay_binding, Mapping), "replay binding missing")
    _require(replay_binding.get("discovery_authority_ref") == predecessor.ref.as_dict(),
             "replay binding does not bind predecessor DiscoveryAuthority")
    _require(tuple(replay_binding.get("candidate_hashes", ())) == hashes,
             "replay candidate frontier drift")

    return FrozenP2F2Context(
        package=deepcopy(dict(package)),
        catalog=catalog,
        predecessor=predecessor,
        candidate_hashes=hashes,
        family_counts=dict(family_counts),
    )


def validate_provenance_activation(evidence: Mapping[str, Any]) -> Mapping[str, Any]:
    _require(isinstance(evidence, Mapping), "R1L-A activation evidence must be a mapping")
    _require(evidence.get("schema") == ACTIVATION_SCHEMA, "R1L-A activation schema mismatch")
    _require(evidence.get("status") == "PASS", "R1L-A provenance court has not passed")
    _require(evidence.get("independently_authorized") is True,
             "validation kinds are not independently authorized")
    _require(evidence.get("authority_basis") == "INDEPENDENT_PREOUTCOME_AUTHORITY",
             "outcome-derived or grammar-self-authorizing basis forbidden")
    _require(evidence.get("preoutcome") is True, "authority must predate empirical outcomes")
    _require(evidence.get("empirical_outcomes_consulted") == 0,
             "empirical outcomes may not parent validation authority")
    _require(evidence.get("candidate_outputs_consulted") == 0,
             "candidate output may not parent validation authority")
    _require(evidence.get("candidate_owned_parent_refs") in ([], ()),
             "candidate-owned authority parent forbidden")
    kinds = validate_requested_validation_kinds(
        evidence.get("authorized_validation_kinds", ()),
        independently_authorized=evidence.get("authorized_validation_kinds", ()),
    )
    _require(kinds == CANONICAL_VALIDATION_KINDS, "R1L-A authorized kind inventory drift")

    parent_refs_raw = evidence.get("authority_parent_refs")
    _require(
        isinstance(parent_refs_raw, Sequence)
        and not isinstance(parent_refs_raw, (str, bytes, bytearray))
        and bool(parent_refs_raw),
        "one or more exact pre-outcome authority parent refs required",
    )
    parent_refs = tuple(sorted({authority_ref(x) for x in parent_refs_raw}, key=lambda x: x.key))
    provenance_ref = exact_ref(evidence.get("provenance_receipt_ref"), "provenance_receipt_ref")
    _require(_is_sha256(provenance_ref.content_hash), "provenance receipt identity malformed")
    return {
        **dict(evidence),
        "authorized_validation_kinds": kinds,
        "authority_parent_refs": parent_refs,
        "provenance_receipt_ref": provenance_ref,
    }


def _successor_replay_ref(
    predecessor: DiscoveryAuthority,
    activation: Mapping[str, Any],
) -> ExactRef:
    material = {
        "schema": SUCCESSOR_REPLAY_KIND,
        "predecessor_discovery_authority_ref": predecessor.ref.as_dict(),
        "candidate_grammar_ref": exact_ref(
            predecessor.candidate_grammar_ref, "candidate_grammar_ref"
        ).as_dict(),
        "validation_kinds": list(CANONICAL_VALIDATION_KINDS),
        "authority_parent_refs": [x.as_dict() for x in activation["authority_parent_refs"]],
        "provenance_receipt_ref": activation["provenance_receipt_ref"].as_dict(),
        "empirical_outcomes_consulted": 0,
        "candidate_outputs_consulted": 0,
    }
    digest = semantic_hash(material)
    return ExactRef(
        SUCCESSOR_REPLAY_KIND,
        f"urn:rawlsing:pre553:fiabc-lm2-r1l:discovery-successor-replay:sha256:{digest}",
        digest,
    )


def build_conditional_discovery_successor(
    predecessor: DiscoveryAuthority,
    provenance_evidence: Mapping[str, Any],
) -> DiscoveryAuthority:
    _require(isinstance(predecessor, DiscoveryAuthority), "exact predecessor DiscoveryAuthority required")
    _require(predecessor.content_hash == PREDECESSOR_DISCOVERY_HASH,
             "unexpected predecessor DiscoveryAuthority identity")
    activation = validate_provenance_activation(provenance_evidence)

    projection = predecessor.semantic_projection()
    fields = deepcopy(projection["semantic_fields"])
    _require(exact_ref(fields["candidate_grammar_ref"]).content_hash == CANDIDATE_GRAMMAR_HASH,
             "candidate grammar mutation forbidden")
    _require(_validation_inventory(fields["candidate_universe_definition"]) == CANONICAL_VALIDATION_KINDS,
             "candidate grammar validation use drift")
    old_rules = fields["validation_rules"]
    _require(isinstance(old_rules, Mapping) and "kinds" not in old_rules,
             "predecessor validation-rule defect shape drift")
    fields["validation_rules"] = {
        **dict(old_rules),
        "kinds": list(CANONICAL_VALIDATION_KINDS),
    }

    old_refs = tuple(predecessor.authority_snapshot_refs)
    all_refs = tuple(sorted(set((*old_refs, *activation["authority_parent_refs"])), key=lambda x: x.key))
    successor = DiscoveryAuthority(
        typed_state=predecessor.typed_state,
        authority_snapshot_refs=all_refs,
        dependency_refs=predecessor.dependency_refs,
        producer_replay_locator_or_reference_root=_successor_replay_ref(predecessor, activation),
        **fields,
    )
    validate_conditional_discovery_successor(
        predecessor,
        successor,
        provenance_evidence,
    )
    return successor


def validate_conditional_discovery_successor(
    predecessor: DiscoveryAuthority,
    successor: DiscoveryAuthority,
    provenance_evidence: Mapping[str, Any],
) -> DiscoveryAuthority:
    activation = validate_provenance_activation(provenance_evidence)
    _require(predecessor.content_hash == PREDECESSOR_DISCOVERY_HASH,
             "predecessor DiscoveryAuthority identity drift")
    _require(successor.content_hash != predecessor.content_hash,
             "semantic preimage change must change DiscoveryAuthority identity")
    _require(successor.typed_state == predecessor.typed_state, "typed state mutation forbidden")
    _require(tuple(successor.dependency_refs) == tuple(predecessor.dependency_refs),
             "DiscoveryAuthority dependency mutation forbidden")

    old_fields = predecessor.semantic_projection()["semantic_fields"]
    new_fields = successor.semantic_projection()["semantic_fields"]
    for key in sorted(set(old_fields) | set(new_fields)):
        if key == "validation_rules":
            continue
        _require(
            canonical_json(old_fields.get(key)) == canonical_json(new_fields.get(key)),
            f"DiscoveryAuthority semantic field mutation forbidden: {key}",
        )

    old_rules = dict(old_fields["validation_rules"])
    new_rules = dict(new_fields["validation_rules"])
    _require("kinds" not in old_rules, "predecessor unexpectedly already grants validation kinds")
    _require({k: v for k, v in new_rules.items() if k != "kinds"} == old_rules,
             "non-kind validation-rule mutation forbidden")
    validate_requested_validation_kinds(
        new_rules.get("kinds", ()),
        independently_authorized=activation["authorized_validation_kinds"],
        grammar_used=_validation_inventory(new_fields["candidate_universe_definition"]),
    )
    _require(
        exact_ref(new_fields["candidate_grammar_ref"]).content_hash == CANDIDATE_GRAMMAR_HASH,
        "candidate grammar ref mutation forbidden",
    )

    allowed_refs = set(predecessor.authority_snapshot_refs) | set(activation["authority_parent_refs"])
    _require(set(successor.authority_snapshot_refs) == allowed_refs,
             "successor authority closure may contain only predecessor refs plus proven pre-outcome parents")
    _require(
        exact_ref(successor.producer_replay_locator_or_reference_root)
        == _successor_replay_ref(predecessor, activation),
        "successor replay/fingerprint root drift",
    )
    return successor


def validate_succession_activation(evidence: Mapping[str, Any]) -> Mapping[str, Any]:
    _require(isinstance(evidence, Mapping), "R1L-B succession evidence must be a mapping")
    _require(evidence.get("schema") == SUCCESSION_SCHEMA, "R1L-B succession schema mismatch")
    _require(evidence.get("status") == "PASS", "R1L-B succession court has not passed")
    _require(evidence.get("predecessor_lock2") == PREDECESSOR_LOCK2,
             "R1L-B predecessor Lock2 mismatch")
    classifications = evidence.get("classifications")
    _require(isinstance(classifications, Mapping), "R1L-B classifications missing")
    _require(classifications.get("DiscoveryAuthority") == "MUST_CHANGE",
             "successor DiscoveryAuthority must be admitted as changed")
    _require(classifications.get("Lock2") == "MUST_CHANGE",
             "Lock2 succession must be explicit")
    for key in ("candidate_grammar", "candidate_hashes", "predicates", "query_templates",
                "universe", "risk_set", "measure_basis"):
        value = classifications.get(key)
        _require(value in ALLOWED_STABLE_CLASSIFICATIONS,
                 f"R1L-C repair cannot activate when {key} requires semantic change")
    _require(evidence.get("candidate_pruning_allowed") is False,
             "candidate pruning must remain forbidden")
    _require(evidence.get("candidate_addition_allowed") is False,
             "candidate addition must remain forbidden")
    return {**dict(evidence), "classifications": dict(classifications)}


def prepare_lock2_successor(
    context: FrozenP2F2Context,
    successor: DiscoveryAuthority,
    provenance_evidence: Mapping[str, Any],
    succession_evidence: Mapping[str, Any],
    *,
    replayed_candidate_hashes: Sequence[str] | None = None,
) -> Mapping[str, Any]:
    validate_conditional_discovery_successor(
        context.predecessor, successor, provenance_evidence
    )
    succession = validate_succession_activation(succession_evidence)
    classifs = succession["classifications"]

    if classifs["candidate_hashes"] == "MUST_REPLAY_BUT_EXPECTED_SAME":
        _require(replayed_candidate_hashes is not None,
                 "R1L-B requires source-free candidate replay before Lock2 emission")
        hashes = tuple(replayed_candidate_hashes)
        _require(hashes == context.candidate_hashes,
                 "candidate replay differs from frozen exact 46-candidate frontier")
    else:
        hashes = context.candidate_hashes
        if replayed_candidate_hashes is not None:
            _require(tuple(replayed_candidate_hashes) == hashes,
                     "optional candidate replay changed frozen frontier")

    package = context.package
    replay_currentness = package["replay_currentness"]
    replay_binding = deepcopy(dict(replay_currentness["replay_binding"]))
    replay_binding["discovery_authority_ref"] = successor.ref.as_dict()
    replay_binding["candidate_hashes"] = list(hashes)

    refs = {canonical_json(x): x for x in replay_binding.get("authority_refs", ())}
    for ref in successor.authority_snapshot_refs:
        refs[canonical_json(ref.as_dict())] = ref.as_dict()
    replay_binding["authority_refs"] = [refs[key] for key in sorted(refs)]
    successor_replay_hash = semantic_hash(replay_binding)
    _require(successor_replay_hash != PREDECESSOR_REPLAY,
             "changed DiscoveryAuthority must transitively change exact replay identity")

    predecessor_material = package["lock2_receipt"]["lock2_material"]
    lock2_material = deepcopy(dict(predecessor_material))
    lock2_material["discovery_authority_ref"] = successor.ref.as_dict()
    lock2_material["candidate_hashes"] = list(hashes)
    lock2_material["replay_hash"] = successor_replay_hash
    _require(
        lock2_material["candidate_grammar_ref"]["content_hash"] == CANDIDATE_GRAMMAR_HASH,
        "candidate grammar mutation forbidden during Lock2 reissue",
    )
    successor_lock2_hash = semantic_hash(lock2_material)
    _require(successor_lock2_hash != PREDECESSOR_LOCK2,
             "changed Lock2 preimage must not retain predecessor identity")

    material = {
        "schema": LOCK2_PREP_SCHEMA,
        "activated": False,
        "predecessor_lock2": PREDECESSOR_LOCK2,
        "predecessor_replay": PREDECESSOR_REPLAY,
        "successor_discovery_authority_ref": successor.ref.as_dict(),
        "successor_replay_hash": successor_replay_hash,
        "successor_lock2_hash": successor_lock2_hash,
        "candidate_grammar_ref": lock2_material["candidate_grammar_ref"],
        "candidate_count": 46,
        "candidate_hashes": list(hashes),
        "family_counts": dict(context.family_counts),
        "replay_binding": replay_binding,
        "lock2_material": lock2_material,
        "provenance_receipt_ref": validate_provenance_activation(provenance_evidence)[
            "provenance_receipt_ref"
        ].as_dict(),
        "succession_court_ref": exact_ref(
            succession_evidence.get("succession_court_ref"), "succession_court_ref"
        ).as_dict(),
        "empirical_outcomes_consulted": 0,
        "candidate_outputs_consulted": 0,
        "source_access": False,
    }
    return canonicalize(material)


def prepare_runtime_package_successor(
    context: FrozenP2F2Context,
    successor: DiscoveryAuthority,
    lock2_preparation: Mapping[str, Any],
    *,
    additional_authority_documents: Iterable[Mapping[str, Any]] = (),
) -> Mapping[str, Any]:
    _require(lock2_preparation.get("schema") == LOCK2_PREP_SCHEMA,
             "Lock2 successor preparation packet required")
    _require(lock2_preparation.get("activated") is False,
             "R1L-C emits preparation only, never activation")

    out = deepcopy(dict(context.package))
    old_predicates = canonical_json(out["predicate_documents"])
    old_queries = canonical_json(out["query_documents"])

    new_authorities = list(out["authority_documents"])
    for document in additional_authority_documents:
        obj = materialize_public_object(document)
        _require(obj.schema_id == "AuthoritySnapshot",
                 "only exact AuthoritySnapshot provenance documents may be appended")
        if all(existing.get("content_hash") != obj.content_hash for existing in new_authorities):
            new_authorities.append(obj.as_dict())
    new_authorities.sort(key=lambda d: (
        d["semantic_fields"]["authority_id"],
        d["semantic_fields"]["authority_version"],
        d["semantic_fields"]["authority_content_hash"],
    ))

    out["schema"] = PACKAGE_PREP_SCHEMA
    out["status"] = "CONDITIONAL_R1L_SUCCESSOR_PREPARED__NOT_ADOPTED"
    out["lock2"] = lock2_preparation["successor_lock2_hash"]
    out["replay"] = lock2_preparation["successor_replay_hash"]
    out["discovery_authority_hash"] = successor.content_hash
    out["authority_documents"] = new_authorities
    out["discovery_authority_documents"] = [successor.as_dict()]
    out["counts"] = {
        **dict(out["counts"]),
        "authorities": len(new_authorities),
        "discovery_authorities": 1,
        "candidates": 46,
    }

    receipt = deepcopy(dict(out["lock2_receipt"]))
    receipt["disposition"] = "CONDITIONAL_R1L_SUCCESSOR_PREPARED__NOT_ADOPTED"
    receipt["lock2_hash"] = lock2_preparation["successor_lock2_hash"]
    receipt["lock2_material"] = deepcopy(lock2_preparation["lock2_material"])
    receipt["replay_hash"] = lock2_preparation["successor_replay_hash"]
    receipt["source_access"] = False
    receipt["outcome_computation"] = False
    out["lock2_receipt"] = receipt

    replay_currentness = deepcopy(dict(out["replay_currentness"]))
    replay_currentness["replay_binding"] = deepcopy(lock2_preparation["replay_binding"])
    replay_currentness["replay_hash"] = lock2_preparation["successor_replay_hash"]
    replay_currentness["source_access"] = False
    out["replay_currentness"] = replay_currentness

    _require(canonical_json(out["predicate_documents"]) == old_predicates,
             "predicate mutation forbidden in conditional package")
    _require(canonical_json(out["query_documents"]) == old_queries,
             "query-template mutation forbidden in conditional package")
    _require(out["lock2_receipt"]["lock2_material"]["candidate_grammar_ref"]["content_hash"]
             == CANDIDATE_GRAMMAR_HASH, "candidate grammar mutation forbidden")
    return canonicalize(out)


__all__ = [
    "CONTRACT_ID",
    "ACTIVATION_SCHEMA",
    "SUCCESSION_SCHEMA",
    "LOCK2_PREP_SCHEMA",
    "PACKAGE_PREP_SCHEMA",
    "SOURCE_SHA256",
    "PREDECESSOR_DISCOVERY_HASH",
    "CANDIDATE_GRAMMAR_HASH",
    "PREDECESSOR_LOCK2",
    "PREDECESSOR_REPLAY",
    "CANONICAL_VALIDATION_KINDS",
    "ValidationAuthorityRepairError",
    "FrozenP2F2Context",
    "validate_requested_validation_kinds",
    "validate_frozen_p2f2_package",
    "validate_provenance_activation",
    "build_conditional_discovery_successor",
    "validate_conditional_discovery_successor",
    "validate_succession_activation",
    "prepare_lock2_successor",
    "prepare_runtime_package_successor",
]
