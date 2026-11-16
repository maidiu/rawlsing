"""Candidate-neutral PRE553 A/B/C parity oracle.

This module implements the FIABC Wave-3 I05 court-owned parity oracle.  It is
deliberately outside candidate ownership: expected truth is frozen before any
candidate output exists and may depend only on exact source identity, accepted
candidate-neutral authority, bounded physical-representation authority, common
semantic producers, and explicitly accepted immutable prior empirical
evidence.

The oracle does not execute or select a candidate, does not infer semantics,
and does not turn pairwise/self-replay equality into parity.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    Pre553IntegrityError,
    canonical_json,
    canonicalize,
    semantic_hash,
)

ORACLE_SCHEMA = "RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0"
FREEZE_SCHEMA = "RAWLSING_FIABC_PARITY_ORACLE_FREEZE_RECEIPT@1.0.0"
MATCH_SCHEMA = "RAWLSING_FIABC_CANDIDATE_ORACLE_MATCH_RECEIPT@1.0.0"
THREE_WAY_SCHEMA = "RAWLSING_FIABC_THREE_WAY_PARITY_RECEIPT@1.0.0"
WVS_MATERIALIZER_CONTRACT = "RAWLSING_FIABC_WVS7_ORACLE_MATERIALIZER@1.0.0"

LITS_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS7_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"

LITS_SOURCE_ROWS = 29002
LITS_SOURCE_VARIABLES = 1198
LITS_CANDIDATE_COUNT = 50
LITS_QUERY_ROLE_COUNT = 77
WVS7_SOURCE_ROWS = 97220
WVS7_SOURCE_VARIABLES = 613

LITS_PROJECTION_IDENTITY = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
LITS_C11_RELEASE_IDENTITY = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
LITS_C11_REPLAY_IDENTITY = "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
LITS_FRONTIER_SEAL = "ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea"
LITS_LEARNED_PRODUCT_IDENTITY = "47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d"
LITS_SEMANTIC_REPLAY_IDENTITY = "301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5"
LITS_ASTRA_D04_R2_COMMIT = "e631de162c582423639b7067a4f36b29f8aa4d89"

# Immutable predecessor identities retained only for historical audit. They do
# not drive the current live WVS7 constitution.
WVS7_PREDECESSOR_LOCK2_IDENTITY = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
WVS7_PREDECESSOR_LOCK2_REPLAY_IDENTITY = "b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490"
WVS7_PREDECESSOR_DISCOVERY_AUTHORITY = "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab"

# Current successor constitution adopted by the final six-cell court.
WVS7_LOCK2_IDENTITY = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
WVS7_LOCK2_REPLAY_IDENTITY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"
WVS7_DISCOVERY_AUTHORITY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
WVS7_EMPIRICAL_UNIVERSE = "f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e"
WVS7_RISK_SET = "0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7"
WVS7_MEASURE_BASIS = "6ed5d61b77c8d77affeb4b49b55c2cc23a4c25dbd65d02719c6ab7a3069a3c79"

WVS7_ORDERED_CANDIDATE_HASHES = (
    "086db8ffe5f2dc47306de3281be5ea555388f3c47212c29b232cde7fc1cd09b7",
    "0fa0d790a357f6e4fab8bd08b1df9f53f7f22d6b0853f36c0e25596c13bbdaeb",
    "1a191126b02c0b534468a7baea96c73e65f8f07af007311dcc12f91af28eb49f",
    "220ff93ece0357c26179c6a67c9850dbc005d70ec99f64493b710cdd5f1ff043",
    "278f2f831b58039c86a5d95d783d414c0356a800d90201ae59847e2587aef25d",
    "35fe5b926610e0d02eb1d0798b3649c4eb9c06787cefcaec7bb50e0f4303205f",
    "3958bfd4f0f3fa3fcc166a4a8059b9cfd3c5a98b22c60b489c0b34534b664864",
    "3d532bf802894239b33621cd955f4cee2c40f05c4582559197ef5bd3dddcedb6",
    "450a77d48ea1eb448e01d088c7ac66ef21ebb75848485698710779e20624adcf",
    "4a611696d84b8647db9e8cb024d437f2a77017472564a4800244d793a4012093",
    "4bf2e6562bea21f96d7fd0d512989cc62266641fafe4d4b8f492e70ee71e1d28",
    "4f6e63eacf1fa167ca9d5774e9a97eb1499a59cc2bc2fa78c64b00122fb24458",
    "5446f54856292505cb0ab6eef5ea1a7005fb6bd7d535c61f2b78d4c3c1e2c21c",
    "59b234834bee1cf89579afca65e4624dde8750a6e6c9690ed2ff5e30c76f7199",
    "5a0e5321a572b5298faeffb25e22f391c5c57759b54d61c33a5690ec4116ebae",
    "6033764e9409052146c9991ce8ff4eeefddf3bb702f0299d08b5f71a92b6fca7",
    "6741818010b1088cb5c95a80a707536d7981ce20a8317231ccc294f9c62061c8",
    "737d867a0e17e3110e9a7f913f405afc0c1b9647a9a82e64188681ffabe15e25",
    "74587360e042f4d152696bfd3e5d2bb77b2330c2c6bd3bd7716587bcec149b56",
    "7cc3ad7d08f27dfb3f87ab5811b20b7484584e02a70d84aac195013a165d2766",
    "85a228d50115765f64ff90ba90ccecb687cef71f63838c84f1e81f94594b6cde",
    "85ebfd5bdf815a961e56d5c5792f83bf4cf3d3c9134ad56a860eec2b8bb3c69a",
    "933e8682da61e968ca332843ab42237e58bcfc6fa09311929180a32c1f20af06",
    "96d3ed1cac75cc22fbafc4ad2cd3a2b8946d5133f8f4d9cccfb142d781729514",
    "9d962fa8e5e2c242682f5b8ea6dacfd1dbb142134ce2f8b4b98953495e17d56b",
    "9f31f61dd05db2a241a8c3082e4474f5fb5882fc436607e58cdd6d119f75a647",
    "a166d220c5ca26a7e1ae102595bd3013d6d738cd245617cd79a9186aeba3c7f9",
    "a8c6754129f24fe766cd60cb15eed65af0504eed0ab417e021dbf65ed602de17",
    "ad71e360764b82352f866702157ee86f06a56cb6d03ee19cbb7bcfd0fb0f0278",
    "aea48622e086f5996b6174b54256b9e7d902b7e50d9c1d32bf54ec495fc8d95d",
    "aefe4c88846f0811c87f924e16ca2734de11b8198f283e4381540cf3916ea53d",
    "b4214a0f5d27edc9740b28e17aaddb23c0dc32c557e0f7f565c9605da9a9feb7",
    "b873a42a8c73c8f5a55972977833529c2e7f37781d74543dacc33425a3487f60",
    "bd3e60d44875eef49d5ba7c06e24668b5c8627e95591962522a78bfc9163fee6",
    "be0dfc5dd5f886a8a8e8aa0382dbf45f1253eb21a50a74690cadda7286966ecc",
    "bf7cac0b15beaffe30e32400979cb1928dbc6c6fca1ed965ff91028ad2eae97c",
    "cbd23c963898d8337f4f89a08a250a086360165a56331f63a3d92730b7c96f59",
    "d40dba4693c88b5fec409d35a7cd00b6cd87b98206b364440c2b69e8e572928b",
    "e39bec57ef82a68a8c06fe722e977ca858bb4444a5039019572cf6bc98b85008",
    "e93cba874ef9e1505a4384d590e6c69786de8dee52acb154bd1ecb55c8622600",
    "eac60cf8deaaf06fbf1d5fc3cf474dc28b3345ffa0fcd073c5b2be563c5507d1",
    "ebf05c3549b6d6a6555e69b41b7e7f319677f3bab8ba5eb61f741a699a3d84a6",
    "ee5d5ef18f9d601b0cad193ebbf4dd3726f70dbac75e4cff2dd205015ff857f2",
    "f09bc9f137767c0ba1d67f0f07f99948a7a77a8fd37280f9202788c04d93447a",
    "f62e7e358576312ee6e7100819c8a4965c7b092aff0f782a9d7605813dca2338",
    "fc4a4531e57777e63def74bb4d77d3c58621e9a6ef7277ae36c618d199b1861a",
)
WVS7_FAMILY_COUNTS = {
    "UNARY_SOCIAL_FORK": 10,
    "PAIR_RESPONSE_COTRAVEL": 1,
    "BRANCH_CONDITIONED_DISTRIBUTION": 10,
    "BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25,
}

REQUIRED_CANDIDATES = ("A", "B", "C")

ALLOWED_DEPENDENCY_OWNER_CLASSES = frozenset({
    "EXACT_SOURCE",
    "ACCEPTED_AUTHORITY",
    "BOUNDED_PHYSICAL_REPRESENTATION_AUTHORITY",
    "COMMON_SEMANTIC_PRODUCER",
    "ACCEPTED_IMMUTABLE_PRIOR_EMPIRICAL_PRODUCT",
    "COURT_NEUTRAL",
})
FORBIDDEN_DEPENDENCY_OWNER_CLASSES = frozenset({
    "CANDIDATE",
    "CANDIDATE_A",
    "CANDIDATE_B",
    "CANDIDATE_C",
    "CANDIDATE_OUTPUT",
    "CANDIDATE_REPOSITORY",
    "CANDIDATE_CACHE",
    "CANDIDATE_SESSION",
    "CANDIDATE_TRANSFORMED_CARRIER",
})

NEGATIVE_STATE_LAW = {
    "physical_vs_semantic_missing": {
        "distinct": True,
        "physical_states": (
            "SYSTEM_MISSING",
            "FORMAT_USER_MISSING_VALUE",
            "FORMAT_USER_MISSING_RANGE",
            "FORMAT_EXTENDED_MISSING",
            "SOURCE_CELL_ABSENT_OR_UNREPRESENTED",
            "PHYSICAL_STATE_UNKNOWN",
        ),
        "semantic_state_requires_governed_binding": True,
    },
    "routing_state_distinctions": (
        "ROUTING_UNKNOWN",
        "RULE_UNAVAILABLE",
        "INAPPLICABLE",
        "NOT_ASKED",
        "NOT_ELIGIBLE",
        "ELIGIBLE_APPLICABLE",
    ),
    "typed_absence_distinctions": (
        "UNKNOWN",
        "MISSING",
        "NOT_APPLICABLE",
        "NONCOMPARABLE",
        "DEFERRED",
        "VALID_EMPTY",
        "INTEGRITY_FAILURE",
    ),
    "topology_distinctions": (
        "NO_EVENT",
        "ALL_MISSING",
        "EMPTY_MULTISELECT",
        "INCOMPATIBLE_TOPOLOGY",
    ),
    "source_relation_state": "DISTINCT_BY_DEFAULT__POSITIVE_RELATION_REQUIRES_EXACT_AUTHORITY",
    "valid_empty_distinction": "VALID_EMPTY_IS_NOT_UNAVAILABLE_UNRESOLVED_OR_INTEGRITY_FAILURE",
    "denied_noncomparable_distinction": "DENIED_AND_NONCOMPARABLE_ARE_NONSCALAR_TYPED_STATES",
    "governance_blocked_state": "BLOCKED_OR_MANUAL_REVIEW_IS_GOVERNANCE_NOT_EMPIRICAL_DATA",
}

FAILURE_DISPOSITIONS = {
    "oracle_identity": "FAIL_CLOSED__ORACLE_MUTATED",
    "source_identity": "FAIL_CLOSED__SOURCE_IDENTITY_MISMATCH",
    "authority_closure": "FAIL_CLOSED__AUTHORITY_CLOSURE_MISMATCH",
    "frontier_manifest": "FAIL_CLOSED__FRONTIER_INCOMPLETE_OR_DRIFT",
    "fact_manifest": "FAIL_CLOSED__SEMANTIC_FACT_MISMATCH",
    "learned_product": "FAIL_CLOSED__LEARNED_PRODUCT_MISMATCH",
    "replay_manifest": "FAIL_CLOSED__PROVENANCE_MISMATCH",
    "exact_ref_manifest": "FAIL_CLOSED__EXACTREF_MISMATCH",
    "negative_state_manifest": "FAIL_CLOSED__TYPED_ABSENCE_COLLAPSE",
    "court_constitution_refs": "FAIL_CLOSED__AUTHORITY_CLOSURE_MISMATCH",
    "projection_and_release_refs": "FAIL_CLOSED__C11_RELEASE_DRIFT",
}


class ParityOracleError(Pre553IntegrityError):
    """Base class for fail-closed oracle contract violations."""


class OracleIndependenceError(ParityOracleError):
    """Expected truth is not causally independent of candidate output/state."""


class OracleMismatchError(ParityOracleError):
    """A candidate observation does not match the frozen oracle."""

    def __init__(self, dimension: str, disposition: str):
        self.dimension = dimension
        self.disposition = disposition
        super().__init__(f"{disposition}: {dimension}")


@dataclass(frozen=True)
class FreezeContext:
    freeze_sequence: int
    candidate_outputs_seen: int = 0
    candidate_owned_roots_consulted: tuple[str, ...] = ()
    candidate_owned_state_reused: bool = False
    candidate_output_first_sequence: int | None = None

    def validate(self) -> None:
        if not isinstance(self.freeze_sequence, int) or isinstance(self.freeze_sequence, bool):
            raise OracleIndependenceError("freeze_sequence must be an integer event ordinal")
        if self.freeze_sequence < 0:
            raise OracleIndependenceError("freeze_sequence must be nonnegative")
        if self.candidate_outputs_seen != 0:
            raise OracleIndependenceError("oracle must freeze before any candidate output exists")
        if self.candidate_owned_roots_consulted:
            raise OracleIndependenceError("candidate-owned roots may not be consulted by the oracle")
        if self.candidate_owned_state_reused:
            raise OracleIndependenceError("oracle state may not be mounted into a candidate lifecycle")
        if (
            self.candidate_output_first_sequence is not None
            and self.freeze_sequence >= self.candidate_output_first_sequence
        ):
            raise OracleIndependenceError("oracle freeze must causally precede first candidate output")


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ParityOracleError(f"{name} must be a mapping")
    return value


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ParityOracleError(f"{name} must be a sequence")
    return value


def _sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ParityOracleError(f"{name} must be a lowercase sha256")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ParityOracleError(f"{name} must be a lowercase sha256") from exc
    if value.lower() != value:
        raise ParityOracleError(f"{name} must be a lowercase sha256")
    return value


def _sorted_canonical_set(values: Sequence[Any]) -> list[Any]:
    material = [canonicalize(v) for v in values]
    by_json = {canonical_json(v): v for v in material}
    if len(by_json) != len(material):
        raise ParityOracleError("exact closure contains duplicate canonical members")
    return [by_json[key] for key in sorted(by_json)]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_candidate_neutral_provenance(provenance: Mapping[str, Any]) -> None:
    dependencies = _sequence(provenance.get("dependencies"), "oracle_build_provenance.dependencies")
    if not dependencies:
        raise OracleIndependenceError("oracle provenance must bind its exact dependencies")
    for index, dependency in enumerate(dependencies):
        dep = _mapping(dependency, f"oracle dependency {index}")
        owner = dep.get("owner_class")
        if owner in FORBIDDEN_DEPENDENCY_OWNER_CLASSES:
            raise OracleIndependenceError(f"candidate-owned dependency forbidden: {owner}")
        if owner not in ALLOWED_DEPENDENCY_OWNER_CLASSES:
            raise OracleIndependenceError(f"unrecognized dependency owner class: {owner!r}")
    if provenance.get("candidate_outputs_used") not in (None, [], (), 0):
        raise OracleIndependenceError("candidate output may not define expected truth")
    if provenance.get("pairwise_candidate_vote") not in (None, False):
        raise OracleIndependenceError("candidate majority/pairwise vote may not define expected truth")
    if provenance.get("first_successful_candidate_as_golden") not in (None, False):
        raise OracleIndependenceError("first successful candidate may not define expected truth")


def _validate_source_identity(source: str, identity: Mapping[str, Any]) -> None:
    expected = {
        "LITS_I": (LITS_SOURCE_SHA256, LITS_SOURCE_ROWS, LITS_SOURCE_VARIABLES),
        "WVS7": (WVS7_SOURCE_SHA256, WVS7_SOURCE_ROWS, WVS7_SOURCE_VARIABLES),
    }.get(source)
    if expected is None:
        raise ParityOracleError(f"unsupported source-local court: {source}")
    sha, rows, variables = expected
    if identity.get("source") != source:
        raise ParityOracleError("source identity source-name drift")
    if identity.get("sha256") != sha:
        raise ParityOracleError("source sha256 drift")
    if identity.get("rows") != rows or identity.get("variables") != variables:
        raise ParityOracleError("source shape drift")


def _validate_terminal_identity(product: Mapping[str, Any], source: str) -> None:
    for key in ("product_identity", "semantic_identity", "replay_identity", "exact_output_identity"):
        _sha(product.get(key), f"expected_learned_product.{key}")
    coverage = _mapping(product.get("coverage"), "expected_learned_product.coverage")
    expected_candidates = LITS_CANDIDATE_COUNT if source == "LITS_I" else 46
    if coverage.get("candidate_count") != expected_candidates:
        raise ParityOracleError("I05 terminal coverage candidate count drift")
    if source == "LITS_I":
        if coverage.get("query_role_count") != LITS_QUERY_ROLE_COUNT:
            raise ParityOracleError("LiTS I05 terminal coverage must bind 77 query roles")
        if coverage.get("typed_terminal_counts") != {
            "EVALUATED_SUPPORTED": 49,
            "EVALUATED_VALID_EMPTY": 1,
        }:
            raise ParityOracleError("LiTS I05 typed terminal coverage drift")
        # The current carrier-neutral receipt/replay use different schemas from
        # the historical ASTRA product/replay. Their current identities are
        # frozen here; the immutable ASTRA identities are verified separately
        # from prior_product/prior_replay_receipt in build_lits_i_oracle().


def _validate_frontier(source: str, frontier: Mapping[str, Any], facts: Sequence[Any]) -> None:
    hashes = list(_sequence(frontier.get("ordered_candidate_hashes"), "frontier ordered_candidate_hashes"))
    for value in hashes:
        _sha(value, "candidate_hash")
    if len(set(hashes)) != len(hashes):
        raise ParityOracleError("frontier contains duplicate candidate hashes")

    fact_hashes = []
    for index, raw in enumerate(facts):
        fact = _mapping(raw, f"fact_manifest[{index}]")
        candidate_hash = fact.get("candidate_hash")
        _sha(candidate_hash, f"fact_manifest[{index}].candidate_hash")
        if not isinstance(fact.get("typed_state"), str) or not fact["typed_state"]:
            raise ParityOracleError("every expected fact must preserve an explicit typed_state")
        fact_hashes.append(candidate_hash)

    if source == "LITS_I":
        if frontier.get("candidate_count") != LITS_CANDIDATE_COUNT or len(hashes) != LITS_CANDIDATE_COUNT:
            raise ParityOracleError("LiTS frontier must contain exactly 50 candidates")
        if frontier.get("query_role_count") != LITS_QUERY_ROLE_COUNT:
            raise ParityOracleError("LiTS frontier must bind exactly 77 query roles")
        if frontier.get("frontier_seal") != LITS_FRONTIER_SEAL:
            raise ParityOracleError("LiTS frontier seal drift")
    elif source == "WVS7":
        if frontier.get("candidate_count") != 46 or len(hashes) != 46:
            raise ParityOracleError("WVS7 frontier must contain exactly 46 candidates")
        if tuple(hashes) != WVS7_ORDERED_CANDIDATE_HASHES:
            raise ParityOracleError("WVS7 exact ordered Lock2 frontier drift")
        family_counts = _mapping(frontier.get("family_counts"), "WVS7 frontier family_counts")
        if canonicalize(family_counts) != canonicalize(WVS7_FAMILY_COUNTS):
            raise ParityOracleError("WVS7 frozen family shape must be exact 10/1/10/25")
    if fact_hashes != hashes:
        raise ParityOracleError(
            "expected fact manifest must cover the complete canonical frontier in exact order"
        )


def _validate_constitution(source: str, constitution: Mapping[str, Any], projection: Mapping[str, Any]) -> None:
    if source == "LITS_I":
        required_projection = {
            "projection_identity": LITS_PROJECTION_IDENTITY,
            "c11_release_identity": LITS_C11_RELEASE_IDENTITY,
            "c11_replay_identity": LITS_C11_REPLAY_IDENTITY,
        }
        for key, value in required_projection.items():
            if projection.get(key) != value:
                raise ParityOracleError(f"LiTS {key} drift")
    elif source == "WVS7":
        required = {
            "lock2_hash": WVS7_LOCK2_IDENTITY,
            "lock2_replay_hash": WVS7_LOCK2_REPLAY_IDENTITY,
            "discovery_authority": WVS7_DISCOVERY_AUTHORITY,
            "empirical_universe": WVS7_EMPIRICAL_UNIVERSE,
            "risk_set": WVS7_RISK_SET,
            "measure_basis": WVS7_MEASURE_BASIS,
        }
        for key, value in required.items():
            if constitution.get(key) != value:
                raise ParityOracleError(f"WVS7 constitution drift: {key}")


def _build_oracle_content(
    *,
    source: str,
    source_identity: Mapping[str, Any],
    court_constitution_refs: Mapping[str, Any],
    semantic_authority_closure: Sequence[Any],
    projection_and_release_refs: Mapping[str, Any],
    frontier_manifest: Mapping[str, Any],
    expected_fact_manifest: Sequence[Any],
    expected_learned_product: Mapping[str, Any],
    replay_manifest: Mapping[str, Any],
    exact_ref_manifest: Sequence[Any],
    oracle_build_provenance: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_source_identity(source, source_identity)
    _assert_candidate_neutral_provenance(oracle_build_provenance)
    facts = list(_sequence(expected_fact_manifest, "expected_fact_manifest"))
    _validate_frontier(source, frontier_manifest, facts)
    _validate_constitution(source, court_constitution_refs, projection_and_release_refs)
    _validate_terminal_identity(expected_learned_product, source)

    closure = _sorted_canonical_set(_sequence(semantic_authority_closure, "semantic_authority_closure"))
    refs = _sorted_canonical_set(_sequence(exact_ref_manifest, "exact_ref_manifest"))
    if not closure:
        raise ParityOracleError("semantic authority closure may not be empty")
    if not refs:
        raise ParityOracleError("exact-ref manifest may not be empty")

    content = {
        "schema": ORACLE_SCHEMA,
        "source": source,
        "source_identity": canonicalize(source_identity),
        "court_constitution_refs": canonicalize(court_constitution_refs),
        "semantic_authority_closure": closure,
        "projection_and_release_refs": canonicalize(projection_and_release_refs),
        "frontier_manifest": canonicalize(frontier_manifest),
        "expected_fact_manifest": canonicalize(facts),
        "expected_learned_product": canonicalize(expected_learned_product),
        "replay_manifest": canonicalize(replay_manifest),
        "exact_ref_manifest": refs,
        "negative_state_manifest": canonicalize(NEGATIVE_STATE_LAW),
        "oracle_build_provenance": canonicalize(oracle_build_provenance),
    }
    content["authority_closure_digest"] = semantic_hash(content["semantic_authority_closure"])
    content["frontier_digest"] = semantic_hash(content["frontier_manifest"])
    return content


def freeze_oracle(content: Mapping[str, Any], freeze: FreezeContext) -> dict[str, Any]:
    """Freeze a validated oracle before candidate output exists."""
    freeze.validate()
    body = canonicalize(_mapping(content, "oracle content"))
    if body.get("schema") != ORACLE_SCHEMA:
        raise ParityOracleError("oracle content schema mismatch")
    if "freeze_receipt" in body or "oracle_identity_sha256" in body:
        raise ParityOracleError("oracle content must be unfrozen")
    _assert_candidate_neutral_provenance(_mapping(body["oracle_build_provenance"], "oracle provenance"))

    identity = semantic_hash(body)
    frozen = dict(body)
    frozen["oracle_identity_sha256"] = identity
    frozen["freeze_receipt"] = {
        "schema": FREEZE_SCHEMA,
        "oracle_identity_sha256": identity,
        "freeze_sequence": freeze.freeze_sequence,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "candidate_output_first_sequence": freeze.candidate_output_first_sequence,
        "state": "FROZEN_READ_ONLY",
    }
    return canonicalize(frozen)


def verify_frozen_oracle(oracle: Mapping[str, Any]) -> str:
    """Recompute the frozen body identity and re-check independence invariants."""
    frozen = dict(_mapping(oracle, "oracle"))
    receipt = _mapping(frozen.pop("freeze_receipt", None), "freeze_receipt")
    identity = frozen.pop("oracle_identity_sha256", None)
    _sha(identity, "oracle_identity_sha256")
    if semantic_hash(frozen) != identity:
        raise OracleIndependenceError("frozen oracle content mutated after freeze")
    if receipt.get("schema") != FREEZE_SCHEMA or receipt.get("oracle_identity_sha256") != identity:
        raise OracleIndependenceError("freeze receipt does not bind oracle identity")
    FreezeContext(
        freeze_sequence=receipt.get("freeze_sequence"),
        candidate_outputs_seen=receipt.get("candidate_outputs_seen"),
        candidate_owned_roots_consulted=tuple(receipt.get("candidate_owned_roots_consulted") or ()),
        candidate_owned_state_reused=bool(receipt.get("candidate_owned_state_reused")),
        candidate_output_first_sequence=receipt.get("candidate_output_first_sequence"),
    ).validate()
    _assert_candidate_neutral_provenance(
        _mapping(frozen["oracle_build_provenance"], "oracle_build_provenance")
    )
    return identity


def build_lits_i_oracle(
    *,
    prior_product: Mapping[str, Any],
    prior_replay_receipt: Mapping[str, Any],
    source_identity: Mapping[str, Any],
    court_constitution_refs: Mapping[str, Any],
    semantic_authority_closure: Sequence[Any],
    projection_and_release_refs: Mapping[str, Any],
    frontier_manifest: Mapping[str, Any],
    comparison_fact_manifest: Sequence[Any],
    expected_learned_product: Mapping[str, Any],
    replay_manifest: Mapping[str, Any],
    exact_ref_manifest: Sequence[Any],
    oracle_build_provenance: Mapping[str, Any],
    freeze: FreezeContext,
) -> dict[str, Any]:
    """Build LiTS oracle from immutable ASTRA-D04-R2 truth plus current neutral refs."""
    product = _mapping(prior_product, "prior_product")
    replay = _mapping(prior_replay_receipt, "prior_replay_receipt")
    if product.get("schema") != "ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0":
        raise ParityOracleError("unexpected LiTS accepted prior product schema")
    if product.get("full_execution_product_sha256") != LITS_LEARNED_PRODUCT_IDENTITY:
        raise ParityOracleError("LiTS accepted prior product hash drift")
    if product.get("semantic_replay_hash") != LITS_SEMANTIC_REPLAY_IDENTITY:
        raise ParityOracleError("LiTS accepted prior semantic replay drift")
    if product.get("terminal_counts") != {
        "EVALUATED_SUPPORTED": 49,
        "EVALUATED_VALID_EMPTY": 1,
    }:
        raise ParityOracleError("LiTS accepted prior typed terminal counts drift")
    prior_frontier = _mapping(product.get("frontier"), "prior_product.frontier")
    if prior_frontier.get("candidate_count") != LITS_CANDIDATE_COUNT:
        raise ParityOracleError("LiTS accepted prior frontier candidate count drift")
    if prior_frontier.get("query_role_count") != LITS_QUERY_ROLE_COUNT:
        raise ParityOracleError("LiTS accepted prior frontier role count drift")
    if prior_frontier.get("preexecution_seal") != LITS_FRONTIER_SEAL:
        raise ParityOracleError("LiTS accepted prior frontier seal drift")
    execution = _mapping(replay.get("execution"), "prior_replay_receipt.execution")
    source = _mapping(replay.get("source"), "prior_replay_receipt.source")
    if source.get("sha256") != LITS_SOURCE_SHA256:
        raise ParityOracleError("LiTS accepted prior source identity drift")
    if not execution.get("byte_identical"):
        raise ParityOracleError("LiTS accepted prior replay is not byte-identical")
    if execution.get("run_1_output_sha256") != LITS_LEARNED_PRODUCT_IDENTITY:
        raise ParityOracleError("LiTS accepted prior run-1 product drift")
    if execution.get("run_2_output_sha256") != LITS_LEARNED_PRODUCT_IDENTITY:
        raise ParityOracleError("LiTS accepted prior run-2 product drift")
    preoutcome = _mapping(replay.get("preoutcome"), "prior_replay_receipt.preoutcome")
    if preoutcome.get("candidate_count") != LITS_CANDIDATE_COUNT or preoutcome.get("query_role_count") != LITS_QUERY_ROLE_COUNT:
        raise ParityOracleError("LiTS accepted prior replay frontier cardinality drift")
    if preoutcome.get("frontier_seal") != LITS_FRONTIER_SEAL:
        raise ParityOracleError("LiTS accepted prior replay frontier seal drift")

    provenance = dict(_mapping(oracle_build_provenance, "oracle_build_provenance"))
    provenance["accepted_prior_empirical_anchor"] = {
        "commit": LITS_ASTRA_D04_R2_COMMIT,
        "product_identity": LITS_LEARNED_PRODUCT_IDENTITY,
        "semantic_replay_identity": LITS_SEMANTIC_REPLAY_IDENTITY,
    }
    content = _build_oracle_content(
        source="LITS_I",
        source_identity=source_identity,
        court_constitution_refs=court_constitution_refs,
        semantic_authority_closure=semantic_authority_closure,
        projection_and_release_refs=projection_and_release_refs,
        frontier_manifest=frontier_manifest,
        expected_fact_manifest=comparison_fact_manifest,
        expected_learned_product=expected_learned_product,
        replay_manifest=replay_manifest,
        exact_ref_manifest=exact_ref_manifest,
        oracle_build_provenance=provenance,
    )
    return freeze_oracle(content, freeze)


def materialize_wvs7_oracle(
    *,
    source_path: Path,
    frozen_authority: Mapping[str, Any],
    neutral_materializer: Callable[[Path, Mapping[str, Any]], Mapping[str, Any]],
    freeze: FreezeContext,
) -> dict[str, Any]:
    """Materialize WVS expected truth from exact bytes + frozen neutral authority.

    The callable is an integration seam for the common source-backed
    C11 -> I03 -> I05 semantic path.  It receives no candidate identifier,
    repository, cache, session, or candidate output.
    """
    if not isinstance(source_path, Path) or not source_path.is_file():
        raise ParityOracleError("WVS7 exact source file is required for materialization")
    if _sha256_file(source_path) != WVS7_SOURCE_SHA256:
        raise ParityOracleError("WVS7 source sha256 drift")
    freeze.validate()
    authority = canonicalize(_mapping(frozen_authority, "frozen_authority"))
    if authority.get("source") not in (None, "WVS7"):
        raise ParityOracleError("WVS7 frozen authority source drift")

    material = neutral_materializer(source_path, authority)
    material = _mapping(material, "neutral_materializer result")
    if material.get("contract") != WVS_MATERIALIZER_CONTRACT:
        raise ParityOracleError("WVS7 neutral materializer contract mismatch")
    provenance = _mapping(material.get("oracle_build_provenance"), "oracle_build_provenance")
    _assert_candidate_neutral_provenance(provenance)

    content = _build_oracle_content(
        source="WVS7",
        source_identity=_mapping(material.get("source_identity"), "source_identity"),
        court_constitution_refs=_mapping(material.get("court_constitution_refs"), "court_constitution_refs"),
        semantic_authority_closure=_sequence(material.get("semantic_authority_closure"), "semantic_authority_closure"),
        projection_and_release_refs=_mapping(material.get("projection_and_release_refs"), "projection_and_release_refs"),
        frontier_manifest=_mapping(material.get("frontier_manifest"), "frontier_manifest"),
        expected_fact_manifest=_sequence(material.get("expected_fact_manifest"), "expected_fact_manifest"),
        expected_learned_product=_mapping(material.get("expected_learned_product"), "expected_learned_product"),
        replay_manifest=_mapping(material.get("replay_manifest"), "replay_manifest"),
        exact_ref_manifest=_sequence(material.get("exact_ref_manifest"), "exact_ref_manifest"),
        oracle_build_provenance=provenance,
    )
    return freeze_oracle(content, freeze)


def freeze_wvs7_oracle_from_common_material(
    *,
    material: Mapping[str, Any],
    freeze: FreezeContext,
) -> dict[str, Any]:
    """Freeze WVS7 expected truth from already materialized candidate-neutral common C11 work.

    Unlike materialize_wvs7_oracle this source-free seam never opens source
    bytes.  The supplied material must already bind the exact WVS7 source
    identity, Lock2 constitution, full 46-candidate frontier, semantic authority
    closure, expected facts/product, replay manifest, exact refs, and
    candidate-neutral provenance under the existing oracle contract.
    """
    freeze.validate()
    material = _mapping(material, "common C11 oracle material")
    if material.get("contract") != WVS_MATERIALIZER_CONTRACT:
        raise ParityOracleError("WVS7 neutral materializer contract mismatch")
    provenance = _mapping(material.get("oracle_build_provenance"), "oracle_build_provenance")
    _assert_candidate_neutral_provenance(provenance)
    content = _build_oracle_content(
        source="WVS7",
        source_identity=_mapping(material.get("source_identity"), "source_identity"),
        court_constitution_refs=_mapping(material.get("court_constitution_refs"), "court_constitution_refs"),
        semantic_authority_closure=_sequence(material.get("semantic_authority_closure"), "semantic_authority_closure"),
        projection_and_release_refs=_mapping(material.get("projection_and_release_refs"), "projection_and_release_refs"),
        frontier_manifest=_mapping(material.get("frontier_manifest"), "frontier_manifest"),
        expected_fact_manifest=_sequence(material.get("expected_fact_manifest"), "expected_fact_manifest"),
        expected_learned_product=_mapping(material.get("expected_learned_product"), "expected_learned_product"),
        replay_manifest=_mapping(material.get("replay_manifest"), "replay_manifest"),
        exact_ref_manifest=_sequence(material.get("exact_ref_manifest"), "exact_ref_manifest"),
        oracle_build_provenance=provenance,
    )
    return freeze_oracle(content, freeze)


def validate_candidate_observation(
    oracle: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one candidate against the immutable oracle, never against peers."""
    oracle_identity = verify_frozen_oracle(oracle)
    observed = _mapping(observation, "candidate observation")
    candidate = observed.get("candidate")
    if candidate not in REQUIRED_CANDIDATES:
        raise OracleMismatchError("candidate", "FAIL_CLOSED__UNKNOWN_CANDIDATE")
    if observed.get("oracle_identity_sha256") != oracle_identity:
        raise OracleMismatchError("oracle_identity", FAILURE_DISPOSITIONS["oracle_identity"])

    comparisons = (
        ("source_identity", "source_identity"),
        ("court_constitution_refs", "court_constitution_refs"),
        ("semantic_authority_closure", "authority_closure"),
        ("projection_and_release_refs", "projection_and_release_refs"),
        ("frontier_manifest", "frontier_manifest"),
        ("fact_manifest", "fact_manifest"),
        ("learned_product", "learned_product"),
        ("replay_manifest", "replay_manifest"),
        ("exact_ref_manifest", "exact_ref_manifest"),
        ("negative_state_manifest", "negative_state_manifest"),
    )
    oracle_keys = {
        "fact_manifest": "expected_fact_manifest",
        "learned_product": "expected_learned_product",
    }
    for observed_key, dimension in comparisons:
        expected_key = oracle_keys.get(observed_key, observed_key)
        if canonicalize(observed.get(observed_key)) != canonicalize(oracle.get(expected_key)):
            raise OracleMismatchError(dimension, FAILURE_DISPOSITIONS[dimension])

    expected_authority_digest = oracle.get("authority_closure_digest")
    expected_frontier_digest = oracle.get("frontier_digest")
    if observed.get("authority_closure_digest") != expected_authority_digest:
        raise OracleMismatchError("authority_closure", FAILURE_DISPOSITIONS["authority_closure"])
    if observed.get("frontier_digest") != expected_frontier_digest:
        raise OracleMismatchError("frontier_manifest", FAILURE_DISPOSITIONS["frontier_manifest"])

    return canonicalize({
        "schema": MATCH_SCHEMA,
        "status": "PASS__INDEPENDENT_ORACLE_MATCH",
        "source": oracle["source"],
        "candidate": candidate,
        "oracle_identity_sha256": oracle_identity,
        "self_replay_ok": observed.get("self_replay_ok"),
        "self_replay_used_as_expected_truth": False,
        "matched_dimensions": (
            "SOURCE_IDENTITY",
            "COURT_CONSTITUTION",
            "AUTHORITY_CLOSURE",
            "PROJECTION_AND_RELEASE",
            "FULL_FRONTIER",
            "I03_FACTS_AND_TYPED_STATES",
            "I05_LEARNED_PRODUCT",
            "SEMANTIC_REPLAY_OUTPUT_IDENTITIES",
            "EXACT_REFS",
            "NEGATIVE_STATE_LAW",
        ),
    })


def validate_three_way_parity(
    oracle: Mapping[str, Any],
    observations: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Require A, B and C to match the same independent oracle individually."""
    oracle_identity = verify_frozen_oracle(oracle)
    if set(observations) != set(REQUIRED_CANDIDATES):
        raise OracleMismatchError(
            "three_way_gate",
            "NO_THREE_WAY_PASS__CANDIDATE_MISSING_OR_FAILED",
        )
    receipts = []
    for candidate in REQUIRED_CANDIDATES:
        observed = _mapping(observations[candidate], f"candidate {candidate} observation")
        if observed.get("candidate") != candidate:
            raise OracleMismatchError(
                "three_way_gate",
                "FAIL_CLOSED__CANDIDATE_IDENTITY_SUBSTITUTION",
            )
        receipts.append(validate_candidate_observation(oracle, observed))
    if {receipt["oracle_identity_sha256"] for receipt in receipts} != {oracle_identity}:
        raise OracleMismatchError("three_way_gate", "FAIL_CLOSED__ORACLE_IDENTITY_SPLIT")
    return canonicalize({
        "schema": THREE_WAY_SCHEMA,
        "status": "PASS__A_B_C_MATCH_ONE_FROZEN_CANDIDATE_NEUTRAL_ORACLE",
        "source": oracle["source"],
        "oracle_identity_sha256": oracle_identity,
        "candidates": REQUIRED_CANDIDATES,
        "pairwise_agreement_used_as_truth": False,
        "self_replay_used_as_truth": False,
        "candidate_match_receipts": receipts,
    })


__all__ = [
    "ALLOWED_DEPENDENCY_OWNER_CLASSES",
    "FAILURE_DISPOSITIONS",
    "FreezeContext",
    "LITS_ASTRA_D04_R2_COMMIT",
    "LITS_C11_RELEASE_IDENTITY",
    "LITS_C11_REPLAY_IDENTITY",
    "LITS_FRONTIER_SEAL",
    "LITS_LEARNED_PRODUCT_IDENTITY",
    "LITS_PROJECTION_IDENTITY",
    "LITS_SEMANTIC_REPLAY_IDENTITY",
    "LITS_SOURCE_SHA256",
    "MATCH_SCHEMA",
    "NEGATIVE_STATE_LAW",
    "ORACLE_SCHEMA",
    "OracleIndependenceError",
    "OracleMismatchError",
    "ParityOracleError",
    "REQUIRED_CANDIDATES",
    "THREE_WAY_SCHEMA",
    "WVS7_DISCOVERY_AUTHORITY",
    "WVS7_EMPIRICAL_UNIVERSE",
    "WVS7_LOCK2_IDENTITY",
    "WVS7_LOCK2_REPLAY_IDENTITY",
    "WVS7_MEASURE_BASIS",
    "WVS7_ORDERED_CANDIDATE_HASHES",
    "WVS7_FAMILY_COUNTS",
    "WVS7_RISK_SET",
    "WVS7_SOURCE_SHA256",
    "WVS_MATERIALIZER_CONTRACT",
    "build_lits_i_oracle",
    "freeze_oracle",
    "freeze_wvs7_oracle_from_common_material",
    "materialize_wvs7_oracle",
    "validate_candidate_observation",
    "validate_three_way_parity",
    "verify_frozen_oracle",
]
