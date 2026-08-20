from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from importlib import import_module
from pathlib import Path

EXACT_BASE_SHA = "53ebe82da36187c38aec305109a9482c433dd0e3"
ASSIGNMENT_ID = "PRE553-W03-R15-001"
RETURN_TOKEN = "PRE553_R15_WHOLE_MACHINE_HOSTILE_ACCEPTANCE_COMPLETE"


@dataclass(frozen=True)
class HostileCase:
    case_id: str
    attack: str
    verdict: str
    delegate_module: str | None
    delegate_test: str | None
    smallest_repair_if_failure: str
    note: str = ""


HOSTILE_CASES = (
    HostileCase(
        "R15-H01",
        "source plurality collapse",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_objects_authority",
        "test_source_universes_and_relation_kinds_do_not_collapse",
        "Restore exact universe-scoped identity and require operation-specific relation authority; do not pool by alias/provenance.",
    ),
    HostileCase(
        "R15-H02",
        "typed absence collapse",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_objects_authority",
        "test_typed_absence_and_observed_zero_do_not_collapse",
        "Restore typed-state identity at the public object boundary; do not encode governed absence as null/missing row.",
    ),
    HostileCase(
        "R15-H03",
        "observed zero vs zero-support collapse",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_observed_zero_is_not_zero_support",
        "Restore denominator/risk-set-aware fact typing so observed zero and zero support remain distinct.",
    ),
    HostileCase(
        "R15-H04",
        "respondent/event dedup information loss",
        "PASS",
        "rawlsing_next.tests.test_pre553_c11_repository_ingest",
        "test_event_multiplicity_preserved_without_value_deduplication",
        "Deduplicate only exact duplicate event identity; preserve lawful repeated/multiselect event multiplicity.",
    ),
    HostileCase(
        "R15-H05",
        "routing/risk-set substitution",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_equal_denominator_counts_different_risk_member_sets_do_not_collapse",
        "Restore exact member-set/routing identity; never substitute denominator equality for risk-set equality.",
    ),
    HostileCase(
        "R15-H06",
        "weight repair/default",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_missing_or_invalid_weight_fails_closed_without_default_one",
        "Remove implicit weight repair/default and return a typed unavailable weighted result unless exact treatment authority exists.",
    ),
    HostileCase(
        "R15-H07",
        "authority fallback",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_objects_authority",
        "test_authority_lookup_is_exact_and_has_no_latest_default_or_fuzzy_lane",
        "Require exact authority id/version/content-hash resolution; delete latest/default/fuzzy/nearest fallback.",
    ),
    HostileCase(
        "R15-H08",
        "replay/version drift",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_tampered_query_predicate_or_replay_reference_fails_closed",
        "Restore immutable historical predicate/query/fact/replay refs and fail closed on identity mismatch.",
    ),
    HostileCase(
        "R15-H09",
        "carrier record to ontology promotion",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_objects_authority",
        "test_carrier_internal_and_deferred_names_cannot_substitute_public_families",
        "Keep carrier/internal records non-semantic; require an explicit governed public semantic object instead of retyping storage shape.",
    ),
    HostileCase(
        "R15-H10",
        "EmpiricalFact to structural proposition without I04 authority",
        "PASS",
        None,
        None,
        "Restore exact named, hash-bound positive I04 admission gating; only ADMITTED may project to frozen M1 direct basis. Do not infer structural meaning from carrier, discovery, provenance, or repository presence.",
        "Integrated convergence: accepted I04 is present; H10 passes only when every non-ADMITTED decision remains nonpositive and I04 does not own V553 temporal decisions or mint temporal objects.",
    ),
    HostileCase(
        "R15-H11",
        "survey to psyche/persona",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_query_execution_has_zero_structural_actor_v3_v2_effect",
        "Restore zero direct actor/V3/V2 effect on population empirical objects; remove any psyche/persona projection.",
    ),
    HostileCase(
        "R15-H12",
        "structural prior to actor-state mutation",
        "PASS",
        "rawlsing_next.tests.test_whole_machine_integration",
        "test_H08_prior_to_actor_state_shortcut_has_zero_effect",
        "Restore the M5 peer-only effect and require a separately owned actor transition authority for actor-state mutation.",
    ),
    HostileCase(
        "R15-H13",
        "source repository presence to permission",
        "PASS",
        "rawlsing_next.tests.test_whole_machine_integration",
        "test_H05_permission_by_presence_never_widens",
        "Restore monotone permission intersection; repository/index/locator presence must never widen producer/V557 authority.",
    ),
    HostileCase(
        "R15-H14",
        "negative authority disappearing downstream",
        "PASS",
        "rawlsing_next.tests.test_whole_machine_integration",
        "test_H01_temporal_negative_laundering",
        "Preserve exact-use negatives through admission/routing/publication; do not downgrade a blocking negative to later positive evidence.",
    ),
    HostileCase(
        "R15-H15",
        "mutation of frozen M1-M6/render/PSEPF semantics",
        "PASS",
        None,
        None,
        "Restore the exact frozen blob from the accepted clean-sideline baseline; R15 has no authority to modify downstream semantics.",
    ),
    HostileCase(
        "R15-H16",
        "source disagreement becomes actor uncertainty",
        "PASS",
        "rawlsing_next.tests.test_whole_machine_integration",
        "test_H11_source_disagreement_cannot_become_actor_uncertainty",
        "Keep source disagreement population-empirical; require current actor-safe authority before any behavioral uncertainty effect.",
    ),
    HostileCase(
        "R15-H17",
        "multi-universe composition without exact relation bundle",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_authorized_composite_without_exact_relation_bundle_is_noncomparable",
        "Require exact pooling, nonduplication and estimand-composition authorities or return NONCOMPARABLE.",
    ),
    HostileCase(
        "R15-H18",
        "missing exact C11 release repaired by latest/default",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_query",
        "test_missing_exact_c11_release_is_typed_unavailable_without_latest_fallback",
        "Require the exact sealed release ref and return typed unavailable when absent; do not select latest/default.",
    ),
    HostileCase(
        "R15-H19",
        "generated actor/structural position used as empirical predicate carrier",
        "PASS",
        "rawlsing_next.tests.test_pre553_empirical_objects_authority",
        "test_predicate_canonicalizes_commutative_children_but_not_semantic_leaf_meaning",
        "Restore empirical predicate leaf-type law; generated structural/actor position is not an empirical coordinate conditioner without a separate comparator authority.",
    ),
)

MANDATORY_ATTACKS = frozenset(
    {
        "source plurality collapse",
        "typed absence collapse",
        "observed zero vs zero-support collapse",
        "respondent/event dedup information loss",
        "routing/risk-set substitution",
        "weight repair/default",
        "authority fallback",
        "replay/version drift",
        "carrier record to ontology promotion",
        "EmpiricalFact to structural proposition without I04 authority",
        "survey to psyche/persona",
        "structural prior to actor-state mutation",
        "source repository presence to permission",
        "negative authority disappearing downstream",
        "mutation of frozen M1-M6/render/PSEPF semantics",
    }
)

# Git blob SHA pins at the exact R15 base.  These are acceptance guards, not
# mutable-latest references.
FROZEN_BLOB_PINS = {
    # PRE553 I01
    "rawlsing_next/pre553_empirical_objects.py": "91974c52ce8c0acafa939be0d7d83f4a5c8085b7",
    "rawlsing_next/pre553_empirical_authority.py": "6714340facfe186c6cc521884cc85ab6340ad989",
    "rawlsing_next/tests/test_pre553_empirical_objects_authority.py": "b73e2fbd983ea8642b5de9614ab8a17ac0e07f51",
    # PRE553 I02
    "rawlsing_next/pre553_c11_repository.py": "67c6eb6494522cd11aab1b93d0e73f9cef6036f3",
    "rawlsing_next/pre553_c11_ingest.py": "332d3d0907a2de9a34cf828299f6125a1d2ddac5",
    "rawlsing_next/pre553_c11_integrity.py": "bda39b1ccd22f27ae24476207a7f3f3e9025b698",
    "rawlsing_next/tests/test_pre553_c11_repository_ingest.py": "31f731093aaafff7ecd4ca5a8c2c9a8e05a46936",
    # PRE553 I03
    "rawlsing_next/_pre553_query_common.py": "6b38b0b749961358b65b31871a8cd5ca4a98fe77",
    "rawlsing_next/_pre553_query_eval.py": "4a37830eb23ee03949b8bb3563e6dac802501a58",
    "rawlsing_next/_pre553_query_predicate.py": "524043996f21110b25a05f0f08bce056e0fa357e",
    "rawlsing_next/pre553_empirical_query.py": "d81e4ebebaf314ad39b4c56452f9331811c7e3a0",
    "rawlsing_next/tests/test_pre553_empirical_query.py": "4134bb60376d05c9d32ac877f1d89a680a6a9292",
    # Frozen V553-V558 / actor-safe sideline
    "rawlsing_next/m1_temporal_v554_admission_dedup.py": "e8bd6376720a2de132b384e7771d71d8d39cf261",
    "rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py": "e6471ace122466988bb17019f70816a59a04f1f7",
    "rawlsing_next/m2_v555_atomic_route.py": "deef8a60613635a10faf7d89cd8cdf0c3b8a0710",
    "rawlsing_next/tests/test_m2_v555_atomic_route.py": "8c641da532889f0a43e6bd4a5dbb5f8f0fb711ce",
    "rawlsing_next/m3_v556_higher_order_structural.py": "a4749541273c921ebe4ff7a0b91460bb1e016b87",
    "rawlsing_next/tests/test_m3_v556_higher_order_structural.py": "fd8ed8b4cfcfa932229534921e7ed9c3f43e657a",
    "rawlsing_next/m4_v557_v558_publication_repository.py": "9005308fb06686b593783666e77d06619645b2bb",
    "rawlsing_next/tests/test_m4_v557_v558_publication_repository.py": "f29a06ba2d3e43786a5562cae86a356721c6b922",
    "rawlsing_next/m5_runtime_rsc_peer_prior.py": "18735bdb31a220aed032aa722574d685e2bdddf5",
    "rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py": "ef4faaa84b24b9b6ca62ae7eaa29018d57439c0c",
    "rawlsing_next/m6_actor_safe_expression.py": "74d9701cdc7dabccf61eb5089498db290c1efd9c",
    "rawlsing_next/tests/test_m6_actor_safe_expression.py": "a8e5b466a118413104783728aac3733416893993",
    "rawlsing_next/render_bounded_expression.py": "eef88095d1d647b5332aa5186a3a5df218fcf9f8",
    "rawlsing_next/tests/test_render_bounded_expression.py": "80bdec5d9dc66603c1bc0fcbdf7506a56b2b0f35",
    "rawlsing_next/v3_psepf_zero_positive_guard.py": "e0528d65215cb431196570c38bac4eae94217a1b",
    "rawlsing_next/tests/test_psepf_zero_positive_guard.py": "21cfdee118d70d41def6ba654bbada5214cc1112",
    "rawlsing_next/tests/test_whole_machine_integration.py": "e5fb1c4f5cc1979bbd0bbc38b48a2f03d318f72d",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def run_delegate(case: HostileCase) -> None:
    if not case.delegate_module or not case.delegate_test:
        raise AssertionError(f"{case.case_id} has no delegated executable proof")
    module = import_module(case.delegate_module)
    test_fn = getattr(module, case.delegate_test)
    test_fn()


def case_by_id(case_id: str) -> HostileCase:
    for case in HOSTILE_CASES:
        if case.case_id == case_id:
            return case
    raise KeyError(case_id)


def matrix_rows() -> tuple[dict[str, str], ...]:
    return tuple(
        {
            "case_id": case.case_id,
            "attack": case.attack,
            "verdict": case.verdict,
            "smallest_repair_if_failure": case.smallest_repair_if_failure,
            "note": case.note,
        }
        for case in HOSTILE_CASES
    )
