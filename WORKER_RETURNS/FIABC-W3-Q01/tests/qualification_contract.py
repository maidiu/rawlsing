"""FIABC Wave-3 Q01 return-local qualification contract.

This module validates review witnesses only. It is not a PRE553 semantic owner,
not a production adapter, and not an execution/measurement backend.
"""
from __future__ import annotations

from typing import Any, Mapping


FROZEN_CANDIDATE_OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
EXPECTED_PACKAGING_BLOBS = {
    "lits_materializer": "9406bacfd928393f6a159a46216aa1f7ec129f34",
    "node4a": "504944f9533b7385d201076e2e834b8a9446dee8",
    "wvs_runtime_package": "e04e84b76f8b4eb53905276dd025938bf2e5f6fe",
    "wvs_projection_materializer": "11b28416aac5a4899706150721f2f8ac8bb6ee43",
}
EXPECTED_FROZEN_B_BLOB = "7c509c2098d0030f253344eb3f682471378812a8"
NEGATIVE_DIAGNOSTIC_INPUT_STATES = {
    "UNAVAILABLE", "NONCOMPARABLE", "UNDERPOWERED", "INVALID", "UNRESOLVED", "NOT_APPLICABLE"
}


class QualificationFailure(AssertionError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise QualificationFailure(code, message)


def _nonempty_list(payload: Mapping[str, Any], key: str) -> bool:
    value = payload.get(key)
    return isinstance(value, list) and len(value) > 0 and all(value)


def validate_diagnostic(payload: Mapping[str, Any]) -> None:
    _require(payload.get("public_family") != "EmpiricalFact@1.0.0",
             "Q01_DIAGNOSTIC_MUST_NOT_BE_EMPIRICAL_FACT",
             "diagnostic product cannot use EmpiricalFact public family")
    _require(payload.get("diagnostic_only") is True,
             "Q01_DIAGNOSTIC_MUST_BE_DIAGNOSTIC_ONLY",
             "diagnostic witness must declare diagnostic-only status")
    _require(payload.get("mints_or_mutates_empirical_fact") is False,
             "Q01_DIAGNOSTIC_CANNOT_MUTATE_EMPIRICAL_TRUTH",
             "diagnostic execution cannot mint or mutate EmpiricalFact")
    _require(payload.get("creates_semantic_authority") is False,
             "Q01_DIAGNOSTIC_CANNOT_CREATE_SEMANTIC_AUTHORITY",
             "diagnostic execution cannot create semantic authority")
    _require(payload.get("frontier_control") is False,
             "Q01_DIAGNOSTIC_CANNOT_CONTROL_FRONTIER",
             "diagnostic score cannot control exact I05 frontier")
    _require(payload.get("structural_authority_granted") is False,
             "Q01_DIAGNOSTIC_CANNOT_GRANT_STRUCTURAL_AUTHORITY",
             "diagnostic score cannot grant structural admission authority")
    for key in ("input_fact_refs", "input_query_refs", "release_refs", "authority_refs", "replay_refs"):
        _require(_nonempty_list(payload, key),
                 "Q01_DIAGNOSTIC_REPLAY_DETERMINANTS_INCOMPLETE",
                 f"diagnostic product must bind exact {key}")
    _require(bool(payload.get("product_identity")),
             "Q01_DIAGNOSTIC_PRODUCT_IDENTITY_MISSING",
             "diagnostic product requires exact replayable identity")
    if payload.get("input_state") in NEGATIVE_DIAGNOSTIC_INPUT_STATES:
        _require(payload.get("output_state") != "SUPPORTED",
                 "Q01_DIAGNOSTIC_NEGATIVE_STATE_COLLAPSE",
                 "negative/noncomparable/underpowered input cannot be promoted to supported")


def validate_effective_n(payload: Mapping[str, Any]) -> None:
    _require(payload.get("default_weight_selected") is False and payload.get("selected_weight_by_heuristic") is False,
             "Q01_EFFECTIVE_N_DEFAULT_WEIGHT_FORBIDDEN",
             "effective-N cannot infer/select a default weight")
    basis = payload.get("measure_basis")
    if basis == "RAW_UNWEIGHTED":
        _require(payload.get("effective_n") is None and payload.get("sum_w") is None and payload.get("sum_w2") is None,
                 "Q01_RAW_EFFECTIVE_N_MUST_BE_NONNUMERIC",
                 "RAW/unweighted workload cannot manufacture numeric effective-N")
        _require(payload.get("state") in {"NOT_APPLICABLE", "WEIGHT_NOT_AUTHORIZED"},
                 "Q01_RAW_EFFECTIVE_N_STATE_INVALID",
                 "RAW/unweighted effective-N must retain typed nonnumeric state")
        _require(payload.get("authorized_weight_ref") is None,
                 "Q01_RAW_EFFECTIVE_N_WEIGHT_REF_FORBIDDEN",
                 "RAW/unweighted witness cannot bind a made-up weight")
        return
    _require(basis == "GOVERNED_WEIGHTED",
             "Q01_EFFECTIVE_N_MEASURE_BASIS_UNRESOLVED",
             "numeric effective-N requires governed weighted basis")
    _require(payload.get("weight_authority_state") == "AUTHORIZED" and bool(payload.get("authorized_weight_ref")),
             "Q01_EFFECTIVE_N_WEIGHT_AUTHORITY_REQUIRED",
             "numeric effective-N requires exact authorized weight identity")
    _require(bool(payload.get("design_authority_ref")) and bool(payload.get("estimand_authority_ref")),
             "Q01_EFFECTIVE_N_DESIGN_ESTIMAND_AUTHORITY_REQUIRED",
             "design and estimand authority must remain explicit and separate")
    _require(payload.get("risk_set_scope") == payload.get("query_scope") == payload.get("weight_scope"),
             "Q01_EFFECTIVE_N_SCOPE_MISMATCH",
             "weight, risk-set and query scope must match exactly")
    sum_w = payload.get("sum_w")
    sum_w2 = payload.get("sum_w2")
    _require(isinstance(sum_w, (int, float)) and not isinstance(sum_w, bool) and sum_w > 0 and
             isinstance(sum_w2, (int, float)) and not isinstance(sum_w2, bool) and sum_w2 > 0,
             "Q01_EFFECTIVE_N_DEGENERATE_WEIGHT_SUM",
             "sum_w and sum_w2 must be positive observed authorized sums")
    expected = (sum_w * sum_w) / sum_w2
    actual = payload.get("effective_n")
    _require(isinstance(actual, (int, float)) and not isinstance(actual, bool) and abs(actual - expected) <= 1e-12,
             "Q01_EFFECTIVE_N_FORMULA_MISMATCH",
             "effective-N must equal sum_w^2/sum_w2")


def validate_candidate_c(payload: Mapping[str, Any]) -> None:
    _require(payload.get("candidate_identity") == "C" and payload.get("repository_identity") == "C",
             "Q01_CANDIDATE_C_B_SUBSTITUTION",
             "Candidate C must remain C even when source-backed realization matches B mechanics")
    _require(payload.get("candidate_owner_commit") == FROZEN_CANDIDATE_OWNER_COMMIT,
             "Q01_CANDIDATE_C_OWNER_IDENTITY_DRIFT",
             "frozen candidate owner commit changed")
    _require(payload.get("accelerator_required") is False,
             "Q01_CANDIDATE_C_ACCELERATOR_MUST_BE_OPTIONAL",
             "Candidate C must have a lawful zero-accelerator state")
    _require(payload.get("accelerators_nonauthoritative") is True,
             "Q01_CANDIDATE_C_ACCELERATOR_BECAME_AUTHORITY",
             "accelerators must remain nonauthoritative")
    accelerators = payload.get("accelerators")
    _require(isinstance(accelerators, list),
             "Q01_CANDIDATE_C_ACCELERATOR_SET_INVALID",
             "accelerator set must be explicit")
    _require("CACC3" not in accelerators,
             "Q01_CACC3_FORBIDDEN",
             "CACC3 is forbidden")
    source = payload.get("source")
    if source == "WVS7":
        _require(accelerators == [],
                 "Q01_WVS_ACCELERATOR_FORBIDDEN",
                 "WVS Candidate C must use zero accelerators")
    elif source == "LITS_I":
        _require(set(accelerators).issubset({"CACC1", "CACC2"}),
                 "Q01_LITS_ACCELERATOR_SCOPE_INVALID",
                 "LiTS Candidate C may use only CACC1/CACC2")
        workload = set(payload.get("workload_targets") or [])
        _require({"q310", "q311"}.issubset(workload),
                 "Q01_LITS_Q310_Q311_TRUNCATION",
                 "q310 and q311 may not be dropped from the frozen workload")
    else:
        raise QualificationFailure("Q01_CANDIDATE_C_SOURCE_UNRECOGNIZED", "source must be LITS_I or WVS7")
    _require(payload.get("outside_accelerator_fallback") == "EXACT_SOURCE_BACKED",
             "Q01_CANDIDATE_C_SOURCE_FALLBACK_REQUIRED",
             "out-of-accelerator work must use exact source-backed realization")
    _require(payload.get("semantic_core") == "COMMON_C11_I03_I05",
             "Q01_CANDIDATE_C_SEMANTIC_OWNER_DRIFT",
             "Candidate C must converge to common semantic core")


def validate_packaging(payload: Mapping[str, Any]) -> None:
    blobs = payload.get("blobs")
    _require(isinstance(blobs, Mapping),
             "Q01_PACKAGING_BLOB_DRIFT",
             "packaging witness must expose exact blobs")
    _require(all(blobs.get(key) == value for key, value in EXPECTED_PACKAGING_BLOBS.items()),
             "Q01_PACKAGING_BLOB_DRIFT",
             "one or more accepted derivative runtime blobs changed")
    _require(payload.get("frozen_candidate_owner_commit") == FROZEN_CANDIDATE_OWNER_COMMIT and
             payload.get("frozen_b_owner_blob") == EXPECTED_FROZEN_B_BLOB and
             payload.get("current_tree_b_substituted") is False,
             "Q01_FROZEN_CANDIDATE_OWNER_SUBSTITUTION",
             "current-tree lookalike cannot replace frozen candidate owner")
    _require(payload.get("historical_immutable_roots_preserved") is True,
             "Q01_HISTORICAL_IMMUTABLE_ROOT_MUST_BE_PRESERVED",
             "historical location alone does not make immutable authority/replay roots obsolete")
    _require(payload.get("semantic_ownership_moved") is False,
             "Q01_PACKAGING_CANNOT_MOVE_SEMANTIC_OWNERSHIP",
             "packaging repair cannot become semantic redesign")


def validate_oracle(payload: Mapping[str, Any]) -> None:
    freeze = payload.get("oracle_freeze_event")
    start = payload.get("candidate_start_event")
    _require(isinstance(freeze, int) and isinstance(start, int) and freeze < start and
             payload.get("candidate_outputs_seen_at_freeze") == 0,
             "Q01_ORACLE_NOT_PREOUTPUT_FROZEN",
             "oracle must be frozen before candidate start/output")
    _require(payload.get("candidate_owned_roots_consulted") == [],
             "Q01_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT",
             "oracle may not consult candidate-owned roots")
    dependencies = payload.get("expected_truth_dependencies")
    _require(isinstance(dependencies, list) and not any(str(x).startswith("candidate:") for x in dependencies) and
             payload.get("expected_truth_origin") in {
                 "EXACT_SOURCE_PLUS_FROZEN_CANDIDATE_NEUTRAL_AUTHORITY",
                 "IMMUTABLE_LITS_TRUTH_PLUS_CURRENT_CANDIDATE_NEUTRAL_REFS"
             },
             "Q01_ORACLE_DERIVED_FROM_CANDIDATE_OUTPUT",
             "expected truth cannot derive from candidate output/session/cache/repository")
    _require(payload.get("pairwise_equality_used_as_oracle") is False,
             "Q01_PAIRWISE_EQUALITY_IS_NOT_ORACLE_EQUALITY",
             "pairwise candidate equality cannot substitute for oracle agreement")
    _require(payload.get("self_replay_used_as_oracle") is False,
             "Q01_SELF_REPLAY_IS_NOT_INDEPENDENT_ORACLE",
             "same-candidate replay is repeatability, not independent truth")
    _require(payload.get("frontier_complete") is True,
             "Q01_ORACLE_PARTIAL_FRONTIER_FORBIDDEN",
             "oracle must cover complete fixed frontier")
    _require(payload.get("negative_state_distinctions_preserved") is True,
             "Q01_ORACLE_NEGATIVE_STATE_COLLAPSE",
             "oracle must preserve typed negative distinctions")
    _require(payload.get("authority_closure_exact") is True,
             "Q01_ORACLE_AUTHORITY_CLOSURE_STALE_OR_PARTIAL",
             "oracle must compare exact transitive authority/replay closure")
    _require(payload.get("oracle_hash_stable_after_candidate_start") is True and
             payload.get("candidate_output_can_fill_missing_oracle_field") is False,
             "Q01_ORACLE_MUTATED_AFTER_FREEZE",
             "candidate output cannot mutate/fill the frozen oracle")


def validate_accounting(payload: Mapping[str, Any]) -> None:
    process_ids = payload.get("process_ids")
    _require(isinstance(process_ids, Mapping) and len(process_ids) == 6 and len(set(process_ids.values())) == 6 and
             payload.get("rss_scope") == "CANDIDATE_PROCESS_LOCAL",
             "Q01_CANDIDATE_PROCESS_RSS_CONTAMINATION",
             "each source×candidate cell requires fresh process identity and candidate-local RSS")
    sessions = payload.get("sessions_at_start")
    _require(isinstance(sessions, Mapping) and len(sessions) == 6 and all(value == [] for value in sessions.values()) and
             payload.get("cross_candidate_state_leak") is False,
             "Q01_CANDIDATE_SESSION_STATE_LEAK",
             "prior candidate sessions/state must not be reachable at candidate start")
    write_counts = payload.get("metric_write_counts")
    _require(isinstance(write_counts, Mapping) and write_counts and all(value == 1 for value in write_counts.values()),
             "Q01_METRIC_OVERWRITE_FORBIDDEN",
             "canonical metric fields are write-once")
    uncaptured = payload.get("uncaptured_telemetry")
    _require(isinstance(uncaptured, Mapping) and uncaptured.get("state") == "MEASUREMENT_NOT_CAPTURED" and
             uncaptured.get("value") is None,
             "Q01_SYNTHETIC_ZERO_TELEMETRY_FORBIDDEN",
             "uncaptured telemetry must be typed null, not zero")
    _require(payload.get("io_measurement") == "OBSERVED_EVENT_COUNTERS" and
             payload.get("endpoint_size_used_as_io") is False,
             "Q01_ENDPOINT_SIZE_IS_NOT_IO",
             "read/write/rewrite bytes must be observed events, not endpoint size")
    _require(payload.get("scratch_high_water_observed") is True,
             "Q01_SCRATCH_PEAK_MUST_BE_HIGH_WATER",
             "scratch peak requires high-water observation")
    _require(payload.get("cpu_intervals_nonoverlapping") is True,
             "Q01_CPU_DOUBLE_COUNT_FORBIDDEN",
             "candidate-total/per-phase CPU cannot double-count overlapping intervals")
    _require(payload.get("lifecycle_actions_actual") is True,
             "Q01_LIFECYCLE_SURROGATE_FORBIDDEN",
             "rebuild/invalidation/stale/corrupt/interruption metrics require actual actions")


def validate_succession(payload: Mapping[str, Any]) -> None:
    if payload.get("overall_status") != "PASS":
        return
    _require(payload.get("deferred_preterminal_function") is False,
             "Q01_PREFLIGHT_ILLEGAL_PRETERMINAL_DEFERMENT",
             "preterminal obligation cannot be silently deferred")
    rows = payload.get("rows")
    _require(isinstance(rows, list) and rows,
             "Q01_PREFLIGHT_REQUIRED_CHAIN_MISSING",
             "PASS requires required obligation rows")
    for row in rows:
        if not row.get("required"):
            continue
        _require(row.get("repository_presence_only") is False,
                 "Q01_PREFLIGHT_REPOSITORY_PRESENCE_NOT_LIVE_CONSUMPTION",
                 "repository presence/importability cannot satisfy live consumption")
        _require(row.get("accepted_authority") is True,
                 "Q01_PREFLIGHT_SEMANTIC_AUTHORITY_MISSING",
                 "required row lacks accepted semantic authority")
        _require(row.get("current_owner") is True,
                 "Q01_PREFLIGHT_CURRENT_OWNER_MISSING",
                 "required row lacks current authoritative owner")
        _require(row.get("binding") is True,
                 "Q01_PREFLIGHT_EXECUTABLE_BINDING_MISSING",
                 "required row lacks executable binding")
        _require(row.get("live_receipt") is True,
                 "Q01_PREFLIGHT_LIVE_RECEIPT_MISSING",
                 "required row lacks exact post-repair live receipt")
        _require(row.get("negative_state_law") is True,
                 "Q01_PREFLIGHT_NEGATIVE_STATE_LAW_MISSING",
                 "required row lacks explicit negative-state law")
        _require(row.get("candidate_capability") is True,
                 "Q01_PREFLIGHT_SOURCE_CANDIDATE_CAPABILITY_UNPROVED",
                 "required source×candidate capability is unproved")
    _require(payload.get("oracle_pass") is True,
             "Q01_PREFLIGHT_ORACLE_UNRESOLVED",
             "succession PASS requires independent oracle closure")
    _require(payload.get("accounting_pass") is True,
             "Q01_PREFLIGHT_ACCOUNTING_UNRESOLVED",
             "succession PASS requires equal-work accounting closure")


def validate_terminal(payload: Mapping[str, Any]) -> None:
    if payload.get("overall_status") != "PASS":
        return
    _require(payload.get("terminal_level") == "I05_LEARNED_EMPIRICAL_PRODUCT" and
             payload.get("i05_complete") is True and payload.get("coverage_complete") is True,
             "Q01_TERMINAL_MUST_BE_COMPLETE_I05",
             "successful court cannot stop at physical/C11/I03/partial-I05")
    _require(payload.get("c11_pass") is True and payload.get("i03_pass") is True,
             "Q01_TERMINAL_INTERMEDIATE_INVARIANT_MISSING",
             "C11 and I03 remain mandatory intermediate invariants")
    _require(payload.get("constituent_i03_fact_closure") is True,
             "Q01_TERMINAL_CONSTITUENT_FACT_CLOSURE_MISSING",
             "I05 terminal must close its constituent I03 facts")
    for key in ("semantic_identity", "replay_identity", "output_identity"):
        _require(bool(payload.get(key)),
                 "Q01_TERMINAL_IDENTITY_INCOMPLETE",
                 f"terminal missing exact {key}")
    _require(payload.get("succession_preflight_pass") is True and payload.get("independent_oracle_pass") is True,
             "Q01_TERMINAL_EXTERNAL_GATE_RECEIPT_MISSING",
             "terminal verifier must consume independent preflight/oracle PASS")
    _require(payload.get("all_admitted_cells_terminalized") is True,
             "Q01_TERMINAL_ADMITTED_CELL_MISSING",
             "all admitted source×candidate cells must reach terminal")
    _require(payload.get("post_lifecycle_terminal_identity_reproduced") is True,
             "Q01_TERMINAL_REPLAY_IDENTITY_DRIFT",
             "later lifecycle operations must reproduce terminal identities")


VALIDATORS = {
    "diagnostic": validate_diagnostic,
    "effective_n": validate_effective_n,
    "candidate_c": validate_candidate_c,
    "packaging": validate_packaging,
    "oracle": validate_oracle,
    "accounting": validate_accounting,
    "succession": validate_succession,
    "terminal": validate_terminal,
}
