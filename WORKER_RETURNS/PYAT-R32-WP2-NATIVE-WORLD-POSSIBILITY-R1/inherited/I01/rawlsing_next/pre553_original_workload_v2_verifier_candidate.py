"""PYAT HQ280 PV3 A04T - independent V2 no-drop verifier CANDIDATE.

This module is deliberately **stdlib-only**: it imports nothing from
``rawlsing_next`` — not the v2 candidate, not the A04 binder, not the accepted
owners.  It operates purely on plain-data payloads (JSON-able mappings), which
is the strongest independence statement available: there is no import path by
which it could trust a candidate-computed key.

What it does, from first principles
-----------------------------------
1. Takes a **separately authored frozen expected payload**: raw fields only
   (source, wave, item, form, slot, semantic_op_class, roles, target,
   condition_order, measure_kind, authority, risk, topology, consumer, state,
   hold_reason).  Optional supplied key strings are accepted ONLY to be
   checked — any divergence from independent recomputation is
   ``KEY_PREIMAGE_MISMATCH``.
2. **Reconstructs every identity itself** (documentary item, semantic
   operation, dispatch operation, expected work, consumer obligation,
   attempt, output) from the raw fields, using its own canonical hash over
   the published v2 grammar.  Same digest for the same preimage is expected;
   the independence lies in separate authorship plus recompute-and-compare,
   never trust.
3. Joins produced jobs to expected operations by **exact owner dispatch-ref
   equality** (the caller's issued query/discovery/predicate refs as plain
   dicts) — never by candidate-computed keys.
4. Classifies typed outcomes with its **own** result table; unknown owner
   states are never promoted.
5. Audits A05 migration per record and per set; declares NONREPRESENTABLE
   where no lawful mapping exists.  It never claims a v2 key equals an A05 key.
6. Checks custodian structural consistency (recomputed frontier vs claimed
   digest) but ALWAYS reports ``EXTERNAL_CUSTODIAN_ISSUER_HOLD``: a matching
   hash proves integrity, never external authentication.
7. Treats consumer receipts as **purported/modelled**; the structural join may
   pass while ``actual_consumer_court`` separately holds
   ``REAL_CONSUMER_MODELLED_NOT_EXECUTED``.

Scope ceiling: source-free development only.  No provenance authentication,
no REAL_EXECUTION approval, no consumer-execution claim, no authority
invention.  A structural PASS here is not external custody.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping


VERIFIER_CONTRACT_ID = "PYAT_HQ280_A04T_V2_INDEPENDENT_VERIFIER_CANDIDATE@1.0.0"
VERIFIER_SCHEMA = "HQ280_PV3_A04T_V2_VERIFIER@1.0.0"
ACCEPTED_EXPECTED_SCHEMA = "HQ280_PV3_A04S_CANONICAL_V2@1.0.0"

SEMANTIC_OP_CLASSES = frozenset({
    "UNARY_DISTRIBUTION",
    "PAIR_RESPONSE_COTRAVEL",
    "NONSCALAR_TOPOLOGY_PRESERVATION",
    "BOUNDED_DISCOVERY",
})

DISPATCH_CLASSES = frozenset({
    "I03_UNARY_OR_JOINT_QUERY",
    "I05_BOUNDED_DISCOVERY",
})

SEMANTIC_TO_DISPATCH = {
    "UNARY_DISTRIBUTION": "I03_UNARY_OR_JOINT_QUERY",
    "PAIR_RESPONSE_COTRAVEL": "I03_UNARY_OR_JOINT_QUERY",
    "NONSCALAR_TOPOLOGY_PRESERVATION": "I03_UNARY_OR_JOINT_QUERY",
    "BOUNDED_DISCOVERY": "I05_BOUNDED_DISCOVERY",
}

MEASURE_KINDS = frozenset({"RAW", "GOVERNED_WEIGHTED"})
EXPECTED_STATES = frozenset({"RUNNABLE", "HELD", "DENIED", "SOURCE_NONAPPLICABLE"})

MEASURED_RESULT_CLASSES = frozenset({
    "MEASURED_POSITIVE",
    "TOPOLOGY_PRESERVED",
    "MEASURED_ZERO_IN_SUPPORTED_RISK_SET",
})
ADMISSIBLE_NULL_CLASS = "MEASURED_NULL"
FORBIDDEN_NULL_SOURCES = frozenset({
    "AUTHORITY_UNAVAILABLE", "ZERO_DENOMINATOR", "UNEXECUTED", "UNVISITED",
})
NEVER_SUCCESS_CLASSES = frozenset({
    "PARTIAL", "ADAPTIVE_PARTIAL", "UNVISITED", "UNAVAILABLE",
})

# A05's own operation vocabulary (for the migration audit only; the verifier
# never imports or executes the A05 oracle).
A05_OP_CLASSES = frozenset({
    "UNARY_DISTRIBUTION",
    "PAIR_RESPONSE_COTRAVEL",
    "NONSCALAR_TOPOLOGY_PRESERVATION",
})


class VerifierError(ValueError):
    """The independent verifier refuses this payload or join."""


class PayloadError(VerifierError):
    """The separately authored expected payload is malformed."""


class ProducedError(VerifierError):
    """The produced manifest/outcome data is malformed."""


_CANON = dict(sort_keys=True, separators=(",", ":"))


def _h(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, **_CANON).encode()).hexdigest()


def _req_str(record: Mapping[str, Any], name: str) -> str:
    value = record.get(name)
    if not isinstance(value, str) or not value:
        raise PayloadError(f"record field {name!r} must be a nonempty string")
    return value


def _req_str_list(record: Mapping[str, Any], name: str) -> list:
    value = record.get(name)
    if not isinstance(value, list) or not value or not all(
        isinstance(x, str) and x for x in value
    ):
        raise PayloadError(f"record field {name!r} must be a nonempty string list")
    return list(value)


# --------------------------------------------------------------------------
# 1. Independent key reconstruction (own code path, published v2 grammar)
# --------------------------------------------------------------------------
def reconstruct_item_key(r: Mapping[str, Any], version: str) -> str:
    return _h({
        "kind": "V2_DOCUMENTARY_ITEM",
        "source": _req_str(r, "source"),
        "wave": _req_str(r, "wave"),
        "item": _req_str(r, "item"),
        "form": _req_str(r, "form"),
        "slot": _req_str(r, "slot"),
        "version": version,
    })


def reconstruct_semantic_op_key(r: Mapping[str, Any], version: str) -> str:
    op_class = _req_str(r, "semantic_op_class")
    if op_class not in SEMANTIC_OP_CLASSES:
        raise PayloadError(f"unsupported semantic_op_class {op_class!r}")
    measure = r.get("measure_kind", "RAW")
    if measure not in MEASURE_KINDS:
        raise PayloadError(f"unsupported measure_kind {measure!r}")
    return _h({
        "kind": "V2_SEMANTIC_OPERATION",
        "semantic_op_class": op_class,
        "roles": _req_str_list(r, "semantic_roles"),
        "target": _req_str(r, "target"),
        "condition_order": list(r.get("condition_order", [])),
        "measure_kind": measure,
        "version": version,
    })


def reconstruct_dispatch_op_key(r: Mapping[str, Any], version: str) -> str:
    op_class = _req_str(r, "semantic_op_class")
    if op_class not in SEMANTIC_OP_CLASSES:
        raise PayloadError(f"unsupported semantic_op_class {op_class!r}")
    dispatch = SEMANTIC_TO_DISPATCH[op_class]
    measure = r.get("measure_kind", "RAW")
    if measure not in MEASURE_KINDS:
        raise PayloadError(f"unsupported measure_kind {measure!r}")
    return _h({
        "kind": "V2_DISPATCH_OPERATION",
        "dispatch_class": dispatch,
        "roles": _req_str_list(r, "semantic_roles"),
        "target": _req_str(r, "target"),
        "condition_order": list(r.get("condition_order", [])),
        "measure_kind": measure,
        "version": version,
    })


def reconstruct_expected_key(item_k: str, sem_k: str, disp_k: str,
                             r: Mapping[str, Any], version: str) -> str:
    return _h({
        "kind": "V2_EXPECTED_WORK",
        "item_key": item_k,
        "semantic_operation_key": sem_k,
        "dispatch_operation_key": disp_k,
        "source_identity": _req_str(r, "source_identity"),
        "authority_ref": _req_str(r, "authority_ref"),
        "risk_identity": _req_str(r, "risk_identity"),
        "topology_identity": _req_str(r, "topology_identity"),
        "version": version,
    })


def reconstruct_consumer_obligation_key(exp_k: str, consumer: str,
                                        version: str) -> str:
    return _h({
        "kind": "V2_CONSUMER_OBLIGATION",
        "expected_work_key": exp_k,
        "consumer": consumer,
        "version": version,
    })


def reconstruct_attempt_key(exp_k: str, attempt: int, version: str) -> str:
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
        raise PayloadError("attempt_index must be a positive integer")
    return _h({
        "kind": "V2_EXECUTION_ATTEMPT",
        "expected_work_key": exp_k,
        "attempt_index": attempt,
        "version": version,
    })


def reconstruct_output_identity(exp_k: str, result_type: str,
                                value: Any, version: str) -> str:
    return _h({
        "kind": "V2_OUTPUT_IDENTITY",
        "expected_work_key": exp_k,
        "result_type": result_type,
        "value": value,
        "version": version,
    })


_SUPPLIED_KEY_FIELDS = (
    "documentary_item_key", "semantic_operation_key",
    "dispatch_operation_key", "expected_work_key",
    "consumer_obligation_key",
)


def reconstruct_record(raw: Mapping[str, Any], version: str) -> dict:
    """Recompute every identity from raw fields; check supplied keys."""
    if not isinstance(raw, Mapping):
        raise PayloadError("expected record must be a mapping")
    state = raw.get("state", "RUNNABLE")
    if state not in EXPECTED_STATES:
        raise PayloadError(f"invalid state {state!r}")
    hold_reason = raw.get("hold_reason")
    if state != "RUNNABLE" and not hold_reason:
        raise PayloadError(f"{state} record must carry a hold reason")
    if state == "RUNNABLE" and hold_reason is not None:
        raise PayloadError("RUNNABLE record cannot carry a hold reason")
    multiplicity = raw.get("multiplicity", 1)
    if (not isinstance(multiplicity, int) or isinstance(multiplicity, bool)
            or multiplicity < 1):
        raise PayloadError("multiplicity must be a positive integer")

    item_k = reconstruct_item_key(raw, version)
    sem_k = reconstruct_semantic_op_key(raw, version)
    disp_k = reconstruct_dispatch_op_key(raw, version)
    exp_k = reconstruct_expected_key(item_k, sem_k, disp_k, raw, version)
    consumer = _req_str(raw, "required_consumer")
    cok = reconstruct_consumer_obligation_key(exp_k, consumer, version)

    recomputed = {
        "documentary_item_key": item_k,
        "semantic_operation_key": sem_k,
        "dispatch_operation_key": disp_k,
        "expected_work_key": exp_k,
        "consumer_obligation_key": cok,
    }
    key_mismatches = {}
    for field in _SUPPLIED_KEY_FIELDS:
        supplied = raw.get(field)
        if supplied is not None and supplied != recomputed[field]:
            key_mismatches[field] = {
                "supplied": supplied, "recomputed": recomputed[field],
            }
    return {
        "raw": dict(raw),
        "state": state,
        "runnable": state == "RUNNABLE",
        "recomputed": recomputed,
        "key_mismatches": key_mismatches,
    }


def freeze_payload(payload: Mapping[str, Any]) -> dict:
    """Validate + freeze a separately authored payload. Fail closed."""
    if not isinstance(payload, Mapping):
        raise PayloadError("expected payload must be a mapping")
    schema = payload.get("schema")
    if schema != ACCEPTED_EXPECTED_SCHEMA:
        raise PayloadError(
            f"payload schema {schema!r} is not the accepted v2 schema "
            f"{ACCEPTED_EXPECTED_SCHEMA!r}; matching version tokens are not proof"
        )
    raw_records = payload.get("declarations")
    if not isinstance(raw_records, list) or not raw_records:
        raise PayloadError("payload declarations must be a nonempty list")
    version = payload.get("version", ACCEPTED_EXPECTED_SCHEMA)
    records = [reconstruct_record(r, version) for r in raw_records]
    if not any(r["runnable"] for r in records):
        raise PayloadError("payload contains no RUNNABLE expected work")

    seen: dict[str, int] = {}
    for i, r in enumerate(records):
        k = r["recomputed"]["expected_work_key"]
        if k in seen:
            raise PayloadError(
                f"duplicate recomputed expected_work_key "
                f"(records {seen[k]} and {i}): two declarations collapse "
                f"onto one semantic identity"
            )
        seen[k] = i

    runnable_keys = sorted(
        r["recomputed"]["expected_work_key"] for r in records if r["runnable"]
    )
    return {
        "schema": schema,
        "version": version,
        "records": records,
        "runnable_keys": runnable_keys,
        "frontier_digest": _h({"frontier": runnable_keys, "version": version}),
    }


# --------------------------------------------------------------------------
# 2. Result classification (own table; unknown states never promoted)
# --------------------------------------------------------------------------
def classify_result(typed_state: Any, *, null_source: Any = None,
                    denominator: Any = None) -> str:
    if not isinstance(typed_state, str) or not typed_state:
        return "MISSING_TYPED_RESULT"
    # Zero-denominator check precedes every promotion: a SUPPORTED-class
    # state over a zero denominator is not a measurement.
    if denominator == 0 and typed_state not in (
            "ZERO_SUPPORT", "MEASURED_NULL", "MEASURED_ZERO_DENOMINATOR"):
        return "ZERO_DENOMINATOR_NOT_TYPED"
    table = {
        "SUPPORTED": "MEASURED_POSITIVE",
        "DISCOVERED_RESULT_SUPPORTED": "MEASURED_POSITIVE",
        "OBSERVED_ZERO": "MEASURED_ZERO_IN_SUPPORTED_RISK_SET",
        "VALID_EMPTY": "TOPOLOGY_PRESERVED",
    }
    if typed_state in table:
        return table[typed_state]
    if typed_state == ADMISSIBLE_NULL_CLASS:
        if null_source in FORBIDDEN_NULL_SOURCES:
            return "FALSE_EMPIRICAL_NULL"
        return ADMISSIBLE_NULL_CLASS
    if typed_state in NEVER_SUCCESS_CLASSES:
        return typed_state
    if typed_state in (
        "ZERO_SUPPORT", "NOT_APPLICABLE", "NOT_ELIGIBLE", "ZERO_OVERLAP",
        "INSUFFICIENT_SUPPORT", "NONCOMPARABLE", "INSUFFICIENT_EVIDENCE",
        "UNRESOLVED", "NOT_ASKED", "INAPPLICABLE",
        "COVERAGE_LIMITED", "PRUNED_BY_AUTHORITY",
    ):
        return typed_state
    if denominator == 0 and typed_state not in ("MEASURED_ZERO_DENOMINATOR",):
        return "ZERO_DENOMINATOR_NOT_TYPED"
    return f"OWNER_TYPED_{typed_state}"


# --------------------------------------------------------------------------
# 3. The join: produced data (plain) vs frozen expectation (recomputed)
# --------------------------------------------------------------------------
@dataclass
class IndependentVerdict:
    ok: bool
    failures: list = field(default_factory=list)
    holds: list = field(default_factory=list)
    expected_keys: list = field(default_factory=list)
    job_keys: list = field(default_factory=list)
    omitted: list = field(default_factory=list)
    extra: list = field(default_factory=list)
    visible_non_runnable: list = field(default_factory=list)
    result_classes: dict = field(default_factory=dict)
    unsatisfied_consumers: list = field(default_factory=list)
    frontier_digest: str = ""
    recomputed_frontier_digest: str = ""

    def fail(self, code: str, detail: Any = "") -> None:
        self.failures.append({"code": code, "detail": detail})

    def hold(self, code: str, detail: Any = "") -> None:
        self.holds.append({"code": code, "detail": detail})

    def failure_codes(self) -> list:
        return sorted({str(f["code"]) for f in self.failures})

    def hold_codes(self) -> list:
        return sorted({str(h["code"]) for h in self.holds})


def _ref_dict(value: Any, name: str) -> dict:
    if not isinstance(value, Mapping):
        raise ProducedError(f"produced {name} must be a mapping")
    if set(value) != {"kind", "object_id", "content_hash"}:
        raise ProducedError(f"produced {name} has the wrong shape")
    for k in ("kind", "object_id", "content_hash"):
        if not isinstance(value[k], str) or not value[k]:
            raise ProducedError(f"produced {name}.{k} must be a nonempty string")
    return dict(value)


def _owner_refs_match_job(rec: dict, job_ref: dict, unit: Mapping[str, Any]) -> bool:
    """Cross-check a claimed expectation against the unit's actual owner refs.

    The producer's claim (which expectation this job fulfills) is verified
    against the independently known declared dispatch refs for that
    expectation.  A claim pointing at the wrong owner inputs fails, even when
    the claimed key itself is a member of the expected set.
    """
    raw = rec["raw"]
    disp = SEMANTIC_TO_DISPATCH[raw["semantic_op_class"]]
    if disp == "I03_UNARY_OR_JOINT_QUERY":
        want_job = raw.get("query_ref")
        if not isinstance(want_job, Mapping) or json.dumps(
                want_job, **_CANON) != json.dumps(job_ref, **_CANON):
            return False
        want_pred = raw.get("predicate_ref")
        got_pred = unit.get("predicate_ref")
        if not isinstance(want_pred, Mapping) or not isinstance(got_pred, Mapping):
            return False
        return (json.dumps(want_pred, **_CANON)
                == json.dumps(got_pred, **_CANON))
    want_disc = raw.get("discovery_authority_ref")
    if not isinstance(want_disc, Mapping):
        return False
    return (json.dumps(want_disc, **_CANON) == json.dumps(job_ref, **_CANON))


def verify(frozen: Mapping[str, Any], produced: Mapping[str, Any]) -> IndependentVerdict:
    """Outer-join verification. Expectation comes ONLY from recomputation."""
    v = IndependentVerdict(ok=True)
    if not isinstance(produced, Mapping):
        raise ProducedError("produced data must be a mapping")

    records = frozen["records"]
    by_key = {r["recomputed"]["expected_work_key"]: r for r in records}
    expected_keys = set(frozen["runnable_keys"])
    v.expected_keys = sorted(expected_keys)
    v.frontier_digest = frozen["frontier_digest"]
    v.recomputed_frontier_digest = frozen["frontier_digest"]

    # 0. supplied-key integrity: never trust, always recompute-and-compare
    for r in records:
        for fname, mismatch in r["key_mismatches"].items():
            v.fail("KEY_PREIMAGE_MISMATCH", {
                "field": fname,
                "item": r["raw"].get("item"),
                "supplied": mismatch["supplied"],
                "recomputed": mismatch["recomputed"],
            })

    # index expected records by owner dispatch ref (exact dict equality)
    by_job_ref: dict[str, dict] = {}
    by_pred_ref: dict[str, dict] = {}
    for r in records:
        if not r["runnable"]:
            continue
        raw = r["raw"]
        disp = SEMANTIC_TO_DISPATCH[raw["semantic_op_class"]]
        if disp == "I03_UNARY_OR_JOINT_QUERY":
            q = raw.get("query_ref")
            p = raw.get("predicate_ref")
            if not isinstance(q, Mapping) or not isinstance(p, Mapping):
                v.fail("MISSING_OWNER_DISPATCH_REF", {
                    "expected_work_key": r["recomputed"]["expected_work_key"],
                    "item": raw.get("item")})
                continue
            qkey = json.dumps(q, **_CANON)
            if qkey in by_job_ref:
                v.fail("DUPLICATE_OWNER_JOB_REF", {"query_ref": q})
            else:
                by_job_ref[qkey] = r
            by_pred_ref[qkey] = p
        else:
            d = raw.get("discovery_authority_ref")
            if not isinstance(d, Mapping):
                v.fail("MISSING_OWNER_DISPATCH_REF", {
                    "expected_work_key": r["recomputed"]["expected_work_key"],
                    "item": raw.get("item")})
                continue
            dkey = json.dumps(d, **_CANON)
            if dkey in by_job_ref:
                v.fail("DUPLICATE_OWNER_JOB_REF", {"discovery_authority_ref": d})
            else:
                by_job_ref[dkey] = r

    units = produced.get("units")
    if not isinstance(units, list):
        raise ProducedError("produced units must be a list")
    seen_units: dict[str, dict] = {}
    matched: dict[str, dict] = {}
    extra_claimed: list = []
    for u in units:
        if not isinstance(u, Mapping):
            raise ProducedError("produced unit must be a mapping")
        job_ref = _ref_dict(u.get("job_ref"), "unit.job_ref")
        ukey = json.dumps(job_ref, **_CANON)
        if ukey in seen_units:
            v.fail("DUPLICATE_CONSTRUCTED_JOB", {"job_ref": job_ref})
            continue
        seen_units[ukey] = u
        # Claimed-key path: when the producer asserts which expectation each
        # job fulfills, the assertion itself is checked — then cross-checked
        # against the independently recomputed owner refs.  A claim for an
        # unknown expectation is an unauthorized extra even when the owner
        # refs coincide with a known job (same-count/different-keys).
        claimed = u.get("claimed_expected_work_key")
        if claimed is not None:
            if not isinstance(claimed, str) or not claimed:
                v.fail("MALFORMED_CLAIMED_KEY", {"job_ref": job_ref})
                continue
            rec = by_key.get(claimed)
            if rec is None:
                v.fail("UNAUTHORIZED_EXTRA_JOB", {
                    "claimed_expected_work_key": claimed,
                    "job_ref": job_ref})
                extra_claimed.append(claimed)
                continue
            exp_k = claimed
            if exp_k in matched:
                v.fail("DUPLICATE_CONSTRUCTED_JOB", {"job_ref": job_ref})
                continue
            matched[exp_k] = u
            if not _owner_refs_match_job(rec, job_ref, u):
                v.fail("CLAIMED_JOB_REF_MISMATCH", {
                    "expected_work_key": exp_k, "job_ref": job_ref})
                continue
        else:
            rec = by_job_ref.get(ukey)
            if rec is None:
                v.fail("UNAUTHORIZED_EXTRA_JOB", {"job_ref": job_ref})
                continue
            exp_k = rec["recomputed"]["expected_work_key"]
            if exp_k in matched:
                v.fail("DUPLICATE_CONSTRUCTED_JOB", {"job_ref": job_ref})
                continue
            matched[exp_k] = u
        # predicate fidelity for I03 jobs
        want_pred = by_pred_ref.get(ukey)
        if want_pred is not None:
            got_pred = u.get("predicate_ref")
            if (not isinstance(got_pred, Mapping)
                    or json.dumps(got_pred, **_CANON) != json.dumps(want_pred, **_CANON)):
                v.fail("PREDICATE_SUBSTITUTION", {
                    "expected_work_key": exp_k, "job_ref": job_ref})
        # release fidelity
        rels = u.get("release_refs")
        if not isinstance(rels, list) or not rels:
            v.fail("MISSING_RELEASE_REF", {"expected_work_key": exp_k})
        for rel in rels:
            _ref_dict(rel, "unit.release_refs[]")

    v.job_keys = sorted(matched)
    omitted = sorted(expected_keys - set(matched))
    v.omitted = omitted
    if omitted:
        v.fail("EXPECTED_OPERATION_OMITTED", omitted)
    extra_a05_style = sorted(set(matched) - expected_keys)
    v.extra = sorted(set(extra_a05_style) | set(extra_claimed))
    if extra_a05_style:
        v.fail("UNAUTHORIZED_EXTRA_JOB", extra_a05_style)

    # source identity on both sides: the frozen expectation must name the
    # executed source, AND every constructed job's own declared identity
    # must name it too (a lying submission is visible as omission+extra AND
    # as an explicit constructed-side mismatch).
    exec_sha = produced.get("executed_source_sha", "")
    for r in records:
        if not r["runnable"]:
            continue
        if r["raw"].get("source_identity") != exec_sha:
            v.fail("SOURCE_IDENTITY_MISMATCH", {
                "expected_work_key": r["recomputed"]["expected_work_key"],
                "side": "DECLARED_EXPECTATION",
                "declared_source_identity": r["raw"].get("source_identity"),
                "executed_source_sha": exec_sha,
            })
    for exp_k, u in matched.items():
        if not isinstance(u, Mapping):
            continue
        declared_src = u.get("declared_source_identity")
        if declared_src is not None and declared_src != exec_sha:
            v.fail("SOURCE_IDENTITY_MISMATCH", {
                "expected_work_key": exp_k,
                "side": "CONSTRUCTED_JOB",
                "declared_source_identity": declared_src,
                "executed_source_sha": exec_sha,
            })
    # Unmatched (extra) jobs are checked too: a job whose own declared
    # source differs from the executed source is a source lie regardless
    # of whether its claimed key belongs to the expected set.
    matched_ids = {id(u) for u in matched.values()}
    for u in units:
        if not isinstance(u, Mapping) or id(u) in matched_ids:
            continue
        declared_src = u.get("declared_source_identity")
        if declared_src is not None and declared_src != exec_sha:
            try:
                job_ref_u = _ref_dict(u.get("job_ref"), "unit.job_ref")
            except ProducedError:
                job_ref_u = u.get("job_ref")
            v.fail("SOURCE_IDENTITY_MISMATCH", {
                "side": "CONSTRUCTED_JOB_UNMATCHED",
                "job_ref": job_ref_u,
                "declared_source_identity": declared_src,
                "executed_source_sha": exec_sha,
            })
    exec_rel = produced.get("executed_release_ref")
    if isinstance(exec_rel, Mapping):
        exec_rel_d = _ref_dict(exec_rel, "executed_release_ref")
        # Every produced unit is checked, matched or not: a foreign release
        # on an unmatched (extra) job is still a forged release.
        for u in units:
            if not isinstance(u, Mapping):
                continue
            try:
                job_ref_u = _ref_dict(u.get("job_ref"), "unit.job_ref")
            except ProducedError:
                continue
            for rel in u.get("release_refs", []) or []:
                if (isinstance(rel, Mapping)
                        and json.dumps(rel, **_CANON) != json.dumps(exec_rel_d, **_CANON)):
                    v.fail("FORGED_RELEASE", {
                        "job_ref": job_ref_u,
                        "unit_release_ref": rel,
                        "executed_release_ref": exec_rel_d,
                    })

    # typed results
    result_classes: dict[str, str] = {}
    for exp_k in sorted(expected_keys):
        rec = by_key[exp_k]
        u = matched.get(exp_k)
        if u is None:
            result_classes[exp_k] = "UNEXECUTED"
            v.fail("EXPECTED_OPERATION_OMITTED", exp_k)
            continue
        states = u.get("result_typed_states")
        if not isinstance(states, list) or not states:
            result_classes[exp_k] = "MISSING_TYPED_RESULT"
            v.fail("MISSING_TYPED_RESULT", exp_k)
            continue
        null_sources = u.get("null_sources") or [None] * len(states)
        denominators = u.get("denominators") or [None] * len(states)
        if len(states) != int(rec["raw"].get("multiplicity", 1)):
            result_classes[exp_k] = "MULTIPLICITY_MISMATCH"
            v.fail("EXPECTED_MULTIPLICITY_MISMATCH", {
                "expected_work_key": exp_k,
                "expected": rec["raw"].get("multiplicity", 1),
                "observed": len(states)})
            continue
        if len(states) == 1:
            klass = classify_result(
                states[0],
                null_source=null_sources[0] if null_sources else None,
                denominator=denominators[0] if denominators else None)
        else:
            klass = "MULTIPLICITY_MISMATCH"
        result_classes[exp_k] = klass
        if klass == "FALSE_EMPIRICAL_NULL":
            v.fail("FALSE_EMPIRICAL_NULL", {
                "expected_work_key": exp_k,
                "null_source": (null_sources[0] if null_sources else None)})
        elif klass in NEVER_SUCCESS_CLASSES:
            # A never-success class can never satisfy a runnable expectation,
            # claimed as success or not.
            v.fail("PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS", {
                "expected_work_key": exp_k, "class": klass,
                "reported_success": bool(u.get("reported_success", False))})
        elif klass in ("COVERAGE_LIMITED", "PRUNED_BY_AUTHORITY"):
            # Legitimate typed outcomes of a completed run — but presenting
            # them AS success is mispromotion.
            if u.get("reported_success", False):
                v.fail("PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS", {
                    "expected_work_key": exp_k, "class": klass})
        elif klass == "ZERO_DENOMINATOR_NOT_TYPED":
            v.fail("ZERO_DENOMINATOR_NOT_TYPED", exp_k)
        elif klass.startswith("OWNER_TYPED_") or klass in (
                "ZERO_SUPPORT", "NOT_APPLICABLE", "NOT_ELIGIBLE",
                "ZERO_OVERLAP", "INSUFFICIENT_SUPPORT", "NONCOMPARABLE",
                "INSUFFICIENT_EVIDENCE", "UNRESOLVED", "NOT_ASKED",
                "INAPPLICABLE", "COVERAGE_LIMITED", "PRUNED_BY_AUTHORITY"):
            pass  # typed non-success, conserved without promotion
    v.result_classes = result_classes

    # candidate own-_dk / co-topic used as a joint warrant, two sides:
    # (a) a frozen expectation declaring a co-topic joint is malformed and
    #     fails here, regardless of production;
    # (b) a produced job whose producer-declared condition order shares one
    #     topic base is a fake joint even when its claimed key is unknown
    #     (the fake lives in the submission, which the verifier never sees
    #     except through produced data).
    def _cotopic(cond: Any) -> bool:
        if not isinstance(cond, list) or len(cond) < 2:
            return False
        base = lambda s: s[:-3] if isinstance(s, str) and s.endswith("_dk") else s
        return base(cond[0]) == base(cond[1])

    for r in records:
        if not r["runnable"]:
            continue
        cond = list(r["raw"].get("condition_order", []))
        if _cotopic(cond):
            v.fail("CANDIDATE_OWN_DK_JOINT", {
                "expected_work_key": r["recomputed"]["expected_work_key"],
                "item": r["raw"].get("item"),
                "condition_order": cond,
                "basis": "recomputed expectation own condition order",
            })
    for u in units:
        if not isinstance(u, Mapping):
            continue
        cond = u.get("declared_condition_order")
        if _cotopic(cond):
            try:
                job_ref_u = _ref_dict(u.get("job_ref"), "unit.job_ref")
            except ProducedError:
                job_ref_u = u.get("job_ref")
            v.fail("CANDIDATE_OWN_DK_JOINT", {
                "job_ref": job_ref_u,
                "condition_order": cond,
                "basis": "produced job producer-declared condition order",
            })

    # held / denied / NA stay visible and never runnable
    visible = set()
    for row in produced.get("held_export", []) or []:
        if isinstance(row, Mapping) and "expected_work_key" in row:
            visible.add(row["expected_work_key"])
    nonrun = []
    for r in records:
        if r["runnable"]:
            continue
        k = r["recomputed"]["expected_work_key"]
        nonrun.append(k)
        if k in matched:
            v.fail("HELD_OR_DENIED_WORK_EXECUTED", {
                "item": r["raw"].get("item"), "state": r["raw"].get("state")})
        if k not in visible:
            v.fail("HELD_OR_DENIED_WORK_NOT_VISIBLE", {
                "item": r["raw"].get("item"), "state": r["raw"].get("state")})
    v.visible_non_runnable = sorted(nonrun)

    # consumer obligations: structural join on purported receipts; real
    # consumption is NEVER claimed here (see actual_consumer_court).
    receipts = produced.get("consumer_receipts", []) or []
    satisfied = set()
    for c in receipts:
        if isinstance(c, Mapping) and "expected_work_key" in c and "consumer" in c:
            satisfied.add((c["expected_work_key"], c["consumer"]))
    unsatisfied = []
    for r in records:
        if not r["runnable"]:
            continue
        k = r["recomputed"]["expected_work_key"]
        consumer = r["raw"]["required_consumer"]
        if (k, consumer) not in satisfied:
            unsatisfied.append({"expected_work_key": k, "consumer": consumer,
                                "item": r["raw"].get("item")})
    v.unsatisfied_consumers = unsatisfied
    if unsatisfied:
        v.fail("REQUIRED_CONSUMER_OMITTED", unsatisfied)

    # standing holds: structural verification can never authenticate these
    v.hold("EXTERNAL_CUSTODIAN_ISSUER_HOLD", {
        "reason": "hash/timestamp consistency is integrity, not external "
                  "authentication; no competent independent authority established"})
    v.hold("REAL_CONSUMER_MODELLED_NOT_EXECUTED", {
        "reason": "purported receipts satisfy the structural join only; "
                  "no real consumer was executed in this scope"})
    v.ok = not v.failures
    return v


def actual_consumer_court(verdict: IndependentVerdict,
                          authenticated_receipts: Any = None) -> dict:
    """Separate court: was anything ACTUALLY consumed?

    Modelled receipts NEVER satisfy this court.  Only independently
    authenticated consumer receipts (outside this scope) could, and none
    exist here — so this court always holds.
    """
    if authenticated_receipts:
        return {"verdict": "HOLD",
                "reason": "authenticated receipt class not established in "
                          "this scope; purported receipts are modelled"}
    return {"verdict": "HOLD",
            "reason": "no authenticated consumer receipts exist; modelled "
                      "receipts satisfy the structural join only",
            "code": "REAL_CONSUMER_MODELLED_NOT_EXECUTED"}


def custodian_check(frozen: Mapping[str, Any],
                    custodian: Any) -> dict:
    """Structural custodian check + unconditional external-auth hold.

    Recomputes the frontier digest from the frozen payload and compares it to
    the claimed digest.  A match proves self-consistency ONLY.  A mismatch
    proves forgery or drift.  Either way the external-authentication question
    stays HELD.
    """
    recomputed = frozen["frontier_digest"]
    out: dict[str, Any] = {
        "recomputed_frontier_digest": recomputed,
        "hold": "EXTERNAL_CUSTODIAN_ISSUER_HOLD",
        "timestamp_trusted": False,
        "signature_trusted": False,
    }
    if not isinstance(custodian, Mapping):
        out.update({"consistent": False,
                    "finding": "CUSTODIAN_ABSENT",
                    "detail": "no custodian record supplied"})
        return out
    claimed = custodian.get("frozen_frontier_digest", "")
    out["claimed_frontier_digest"] = claimed
    out["timestamp_recorded"] = custodian.get("custodian_timestamp")
    out["timestamp_note"] = ("caller-supplied timestamp is recorded, never "
                             "trusted as time")
    if claimed != recomputed:
        out.update({"consistent": False,
                    "finding": "CUSTODIAN_MISMATCH",
                    "detail": "claimed frontier digest does not match the "
                              "independently recomputed frontier"})
        return out
    out.update({"consistent": True,
                "finding": "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN",
                "detail": "digests match: integrity holds, external custody "
                          "does not follow"})
    return out


# --------------------------------------------------------------------------
# 4. Audited A05 migration mapping (injective or NONREPRESENTABLE)
# --------------------------------------------------------------------------
def audit_a05_migration(records: list) -> dict:
    """Per-record triple mapping + set-level injectivity verdict.

    A v2 expected_work_key can NEVER equal an A05 expected_work_key
    (different kind tags, different preimage shapes, different versions), so
    full-key equality is unconditionally NONREPRESENTABLE.  The audit records
    the (semantic_op_class, roles, target) triple correspondence where the
    grammar genuinely overlaps, and fails the SET closed if two records share
    one A05 triple (lossy coercion refused).
    """
    per_record = []
    triple_owners: dict[str, list] = {}
    for r in records:
        raw = r["raw"] if isinstance(r, dict) and "raw" in r else r
        if not isinstance(raw, Mapping):
            continue
        if raw.get("state", "RUNNABLE") != "RUNNABLE":
            continue
        op = raw.get("semantic_op_class")
        roles = tuple(raw.get("semantic_roles", []))
        target = raw.get("target")
        measure = raw.get("measure_kind", "RAW")
        cond = list(raw.get("condition_order", []))
        triple = (op, roles, target)
        reasons = []
        triple_mappable = True
        if op not in A05_OP_CLASSES:
            triple_mappable = False
            reasons.append(f"op class {op!r} has no A05 counterpart")
        if measure != "RAW":
            triple_mappable = False
            reasons.append(
                f"measure {measure!r} has no A05 distinction; coercing to "
                f"RAW would collide distinct operations")
        if cond:
            triple_mappable = False
            reasons.append(
                f"condition_order {cond!r} has no A05 field; coercing would "
                f"collapse q(C|A) and q(C|A,B) onto one A05 key")
        key = json.dumps({"op": op, "roles": list(roles), "target": target},
                         **_CANON)
        triple_owners.setdefault(key, []).append(raw.get("item"))
        per_record.append({
            "item": raw.get("item"),
            "semantic_op_class": op,
            "triple": {"op_class": op, "roles": list(roles), "target": target},
            "triple_mappable_to_a05": triple_mappable,
            "full_key_equal_to_a05": False,
            "full_key_verdict": "NONREPRESENTABLE",
            "full_key_reason": ("v2 and A05 key preimages differ in kind tag, "
                                "fields and version; equality is impossible"),
            "triple_reasons": reasons,
        })
    collisions = {k: v for k, v in triple_owners.items() if len(v) > 1}
    set_injective = not collisions
    return {
        "per_record": per_record,
        "a05_triples_shared_by_multiple_records": collisions,
        "set_level_triple_mapping_injective": set_injective,
        "set_verdict": ("INJECTIVE_TRIPLE_MAPPING"
                        if set_injective else
                        "NONREPRESENTABLE__SHARED_A05_TRIPLE_WOULD_COLLIDE"),
        "note": ("Even an injective triple mapping does not join v2 and A05 "
                 "key sets: A05 verifies keys IT computes; translated v2 keys "
                 "cannot satisfy that check. The old A05 oracle stays valid "
                 "for its own contract only."),
    }


__all__ = [
    "VERIFIER_CONTRACT_ID",
    "VERIFIER_SCHEMA",
    "ACCEPTED_EXPECTED_SCHEMA",
    "SEMANTIC_OP_CLASSES",
    "DISPATCH_CLASSES",
    "SEMANTIC_TO_DISPATCH",
    "MEASURE_KINDS",
    "EXPECTED_STATES",
    "MEASURED_RESULT_CLASSES",
    "ADMISSIBLE_NULL_CLASS",
    "FORBIDDEN_NULL_SOURCES",
    "NEVER_SUCCESS_CLASSES",
    "A05_OP_CLASSES",
    "VerifierError",
    "PayloadError",
    "ProducedError",
    "reconstruct_item_key",
    "reconstruct_semantic_op_key",
    "reconstruct_dispatch_op_key",
    "reconstruct_expected_key",
    "reconstruct_consumer_obligation_key",
    "reconstruct_attempt_key",
    "reconstruct_output_identity",
    "reconstruct_record",
    "freeze_payload",
    "classify_result",
    "IndependentVerdict",
    "verify",
    "actual_consumer_court",
    "custodian_check",
    "audit_a05_migration",
]
