"""GF1N independent probe — native relation construction and contract envelope.

Derived ONLY from the original GF1G precommitted producer/consumer contract and
the GF1N commission.  It does not import, read or depend on the GF1M follow-up
candidate implementation.  The consumer under test is whichever physical module
the GF1G contract imports from the seated ``runtime_root``.

The envelope encodes the frozen contract:

* an unsupported native shape must fail closed at a typed construction or consumer
  boundary, with no downstream hash/support/signature;
* an accepted shape must be lossless: two distinct typed categories, exact support
  conservation, exact role binding, deterministic result hash and strict JSON
  (``allow_nan=False``, no duplicate object names) exchange;
* no untyped crash is acceptable at construction or consumption.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import os

_CONTRACT = None


def contract():
    """Load the original GF1G precommitted contract module (not the candidate)."""
    global _CONTRACT
    if _CONTRACT is None:
        path = os.environ.get("GF1G_CONTRACT") or os.environ["GF1J_GF1G_TEST"]
        spec = importlib.util.spec_from_file_location("gf1n_original_gf1g_contract", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _CONTRACT = module
    return _CONTRACT


def h():
    return contract()


def G():
    return contract().G


def CONS():
    return contract().CONS


# --------------------------------------------------------------------- strict JSON

_DUP = object()


def _no_dups(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("DUPLICATE_JSON_OBJECT_NAME:" + repr(key))
        out[key] = value
    return out


def strict_json(value):
    """Serialize and reparse strict JSON; reject non-finite and duplicate names."""
    text = json.dumps(value, sort_keys=True, allow_nan=False, ensure_ascii=False)
    json.loads(text, object_pairs_hook=_no_dups)
    return text


def json_strict_ok(value):
    try:
        return True, strict_json(value), None
    except Exception as exc:  # noqa: BLE001 - classification is the point
        return False, None, type(exc).__name__ + ":" + str(exc)


# --------------------------------------------------------------------- construction

def fields():
    """Mutable copy of the original native template fields (hash/object id removed)."""
    template = h()._template()
    f = dict(template.__dict__)
    f["conditional_count_profile"] = copy.deepcopy(f["conditional_count_profile"])
    f.pop("content_hash")
    f.pop("object_id")
    return f


def _rows(f, cd, td, counts, denoms, zero_state):
    rows = []
    for ci, c in enumerate(cd):
        cells = []
        for ti, t in enumerate(td):
            if counts is None:
                n = 1 if ci == ti else 0
            else:
                n = counts.get("%d%d" % (ci, ti), 0)
            cells.append({
                "target_state": t,
                "source_native_target": f["target_source_native_variable"],
                "joint_support_count": n,
                "joint_cell_state": "OBSERVED_POSITIVE" if n else zero_state,
            })
        denominator = (denoms or {}).get(str(ci), sum(c["joint_support_count"] for c in cells))
        rows.append({
            "condition_state": c,
            "source_native_conditioner": f["conditioner_source_native_variable"],
            "condition_denominator_support": denominator,
            "target_counts": tuple(cells),
        })
    return tuple(rows)


def relation(*, role="none", domain=None, counts=None, denoms=None, eligible=2,
             typed_state=None, zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
             empty_profile=False, forge_provenance=False, wrong_selfhash=False):
    """Build a real ``GenericNativePairRelation`` from the original template fields.

    ``role`` is ``condition``, ``target`` or ``none`` (template domains).  The
    original producer validates its own projection and may raise the typed
    ``GenericNativePairError`` before consumption; callers classify that.
    """
    f = fields()
    conditioner_domain = tuple(domain) if role in ("condition", "both") else tuple(f["conditioner_domain"])
    target_domain = tuple(domain) if role in ("target", "both") else tuple(f["target_domain"])
    f["conditioner_domain"] = conditioner_domain
    f["target_domain"] = target_domain

    if typed_state is not None:
        f["typed_state"] = typed_state
        f["producer_state_blocking"] = typed_state != "SUPPORTED"
        f["conditional_count_profile"] = ()
        f["eligible_joint_risk_total"] = eligible
    elif empty_profile:
        f["typed_state"] = "SUPPORTED"
        f["producer_state_blocking"] = False
        f["conditional_count_profile"] = ()
        f["eligible_joint_risk_total"] = eligible
    else:
        f["conditional_count_profile"] = _rows(
            f, conditioner_domain, target_domain, counts, denoms, zero_state)
        f["typed_state"] = "SUPPORTED"
        f["producer_state_blocking"] = False
        f["eligible_joint_risk_total"] = eligible

    if forge_provenance:
        ref_type = type(f["producer_provenance_refs"][0])
        auth_type = type(f["producer_authority_refs"][0])
        f["producer_provenance_refs"] = (
            ref_type("GF1N_FORGED_PROVENANCE", "urn:gf1n:forged:provenance", "0" * 64),)
        f["producer_authority_refs"] = (
            auth_type(authority_id="GF1N_FORGED_AUTHORITY",
                      authority_version="0.0.0",
                      authority_content_hash="0" * 64),)

    digest = h().G.semantic_hash(h().G._projection(f))
    if wrong_selfhash:
        digest = "0" * 64
    return h().G.GenericNativePairRelation(
        **f,
        content_hash=digest,
        object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + digest,
    )


# --------------------------------------------------------------------- assessment

def _sum_vectors(support_vectors):
    total = 0
    for value in support_vectors.values():
        total += sum(v for v in value.values())
    return total


def _is_hex64(value):
    return isinstance(value, str) and len(value) == 64 and all(
        c in "0123456789abcdef" for c in value)


def assess(*, role="none", domain=None, counts=None, denoms=None, eligible=2,
           typed_state=None, empty_profile=False, forge_provenance=False,
           wrong_selfhash=False, n_states=None, expected_support=None):
    """Build, consume and classify one native hostile shape.

    Returns ``{"outcome": ..., "result": ..., "strict": ..., "error": ...}`` where
    outcome is one of ``CONSTRUCTION_REFUSED``, ``CONSUMER_REFUSED``,
    ``ACCEPTED``, ``HOLD``, ``EMPTY``, ``ZERO``, ``NO_ELIGIBLE_RISK``,
    ``UNTYPED_CONSTRUCTION_CRASH`` or ``UNTYPED_CONSUMER_CRASH``.
    """
    try:
        rel = relation(role=role, domain=domain, counts=counts, denoms=denoms,
                       eligible=eligible, typed_state=typed_state,
                       empty_profile=empty_profile,
                       forge_provenance=forge_provenance,
                       wrong_selfhash=wrong_selfhash)
    except h().G.GenericNativePairError as exc:
        return {"outcome": "CONSTRUCTION_REFUSED",
                "error": type(exc).__name__ + ":" + str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"outcome": "UNTYPED_CONSTRUCTION_CRASH",
                "error": type(exc).__name__ + ":" + str(exc)}

    try:
        result = CONS()(rel)
    except Exception as exc:  # noqa: BLE001
        return {"outcome": "UNTYPED_CONSUMER_CRASH",
                "error": type(exc).__name__ + ":" + str(exc),
                "relation_hash": rel.content_hash}

    ok, text, err = json_strict_ok(result)
    base = {"result": result, "strict": text, "strict_ok": ok, "strict_error": err,
            "relation_hash": rel.content_hash, "relation_object_id": rel.object_id}

    decision = result.get("decision_state")
    if decision == "CONSUMER_RELATION_INTEGRITY_REJECTED":
        base["outcome"] = "CONSUMER_REFUSED"
    elif decision == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION":
        base["outcome"] = "INVALID"
    elif decision == "RESPONSE_INPUTS_VALID_EMPTY":
        base["outcome"] = "EMPTY"
    elif result.get("separation_class") == "UNDETERMINED_NO_ELIGIBLE_RISK":
        base["outcome"] = "NO_ELIGIBLE_RISK"
    elif result.get("separation_class") == "UNDETERMINED_ZERO_SUPPORT_RISK":
        base["outcome"] = "ZERO"
    elif decision == "PAIR_SUPPORT_SIGNATURE_COMPUTED":
        base["outcome"] = "ACCEPTED"
    elif result.get("separation_class") is None and result.get("downstream_value_produced") is False:
        base["outcome"] = "HOLD"
    else:
        base["outcome"] = "UNEXPECTED_STATE:" + repr(decision)

    if base["outcome"] == "ACCEPTED":
        checks = []
        checks.append(("strict_json", ok))
        checks.append(("separation_class", result.get("separation_class") in {
            "EXACT_PAIR_SEPARATION", "NO_PAIR_SEPARATION",
            "UNDETERMINED_NO_ELIGIBLE_RISK", "UNDETERMINED_ZERO_SUPPORT_RISK"}))
        checks.append(("downstream", result.get("downstream_value_produced") is True))
        checks.append(("owner", result.get("production_owner_commit") is False))
        checks.append(("hold", result.get("generic_native_semantics_hold") == "RETAINED"))
        checks.append(("hash", _is_hex64(result.get("result_hash"))))
        checks.append(("read_hash", result.get("read_relation_content_hash") == rel.content_hash))
        checks.append(("read_id", result.get("read_relation_object_id") == rel.object_id))
        support_vectors = result.get("support_vectors")
        expected = expected_support
        if expected is None and counts is not None:
            expected = sum(counts.values())
        if expected is None and typed_state is None and not empty_profile:
            expected = (n_states or (len(domain) if domain is not None else None) or 2)
        checks.append(("support_total", result.get("joint_support_total") == expected))
        checks.append(("support_vectors_dict", isinstance(support_vectors, dict)))
        if isinstance(support_vectors, dict):
            n = n_states or (len(domain) if domain is not None else 2)
            checks.append(("support_vectors_keys", len(support_vectors) == n))
            checks.append(("support_vectors_rows", all(len(v) == n for v in support_vectors.values())))
            checks.append(("support_vectors_total", _sum_vectors(support_vectors) == expected))
        positive = result.get("condition_states_with_positive_denominator")
        n = n_states or (len(domain) if domain is not None else 2)
        checks.append(("positive_denominators", isinstance(positive, list) and len(positive) == n))
        checks.append(("signature", isinstance(result.get("separation_signature"), str)
                       and bool(result.get("separation_signature"))))
        base["contract_checks"] = checks
        base["contract_ok"] = all(v for _, v in checks)
        base["first_strict"] = text
        base["second_strict"] = strict_json(CONS()(rel))
        base["deterministic"] = base["first_strict"] == base["second_strict"]
    return base


# --------------------------------------------------------------------- contract checks

def assert_refused(case, got):
    assert got["outcome"] in ("CONSTRUCTION_REFUSED", "CONSUMER_REFUSED"), got
    if got["outcome"] == "CONSUMER_REFUSED":
        result = got["result"]
        assert result.get("separation_class") is None, result
        assert result.get("downstream_value_produced") is False, result
        assert got["strict_ok"], got.get("strict_error")
        for forbidden in ("result_hash", "support_vectors", "separation_signature"):
            assert result.get(forbidden) in (None, "", {}, ()), (forbidden, result)


def assert_hold(case, got):
    assert got["outcome"] in ("HOLD", "CONSTRUCTION_REFUSED"), got
    if got["outcome"] == "HOLD":
        result = got["result"]
        assert result.get("separation_class") is None, result
        assert result.get("downstream_value_produced") is False, result
        assert result.get("generic_native_semantics_hold") == "RETAINED", result
        assert got["strict_ok"], got.get("strict_error")


def assert_failclosed(case, got):
    """Risk-bound failure: no separation, no downstream value, no fabricated hash.

    The frozen GF1G contract permits either a computed HOLD row or an explicit
    integrity rejection, but never a positive class or downstream value.
    """
    assert got["outcome"] in ("HOLD", "CONSTRUCTION_REFUSED", "CONSUMER_REFUSED"), got
    if got["outcome"] == "CONSUMER_REFUSED":
        assert_refused(case, got)
        return
    if got["outcome"] == "CONSTRUCTION_REFUSED":
        return
    result = got["result"]
    assert result.get("separation_class") is None, result
    assert result.get("downstream_value_produced") is False, result
    assert result.get("generic_native_semantics_hold") == "RETAINED", result
    assert got["strict_ok"], got.get("strict_error")


def assert_empty(case, got):
    assert got["outcome"] == "EMPTY", got
    assert got["result"].get("downstream_value_produced") is False, got["result"]
    assert got["strict_ok"], got.get("strict_error")


def assert_invalid(case, got):
    assert got["outcome"] == "INVALID", got
    assert got["result"].get("separation_class") is None, got["result"]
    assert got["result"].get("downstream_value_produced") is False, got["result"]
    assert got["strict_ok"], got.get("strict_error")


def assert_typed_zero(case, got):
    """Typed ZERO_SUPPORT native state: a refused result, no downstream value."""
    assert got["outcome"] == "ZERO", got
    assert got["result"].get("downstream_value_produced") is False, got["result"]
    assert got["strict_ok"], got.get("strict_error")


def assert_zero_class(case, got):
    """Valid supported risk with zero observed support: class is ZERO.

    The frozen GF1G G11 contract requires the zero-support class and strict
    exchange for this computed case; it does not require the downstream flag to
    be false (that applies to the typed ZERO_SUPPORT refusal branch).
    """
    assert got["outcome"] == "ZERO", got
    assert got["result"].get("separation_class") == "UNDETERMINED_ZERO_SUPPORT_RISK", got
    assert got["strict_ok"], got.get("strict_error")


def assert_no_risk(case, got):
    """Valid supported relation whose eligible risk set is empty.

    Frozen GF1G G9 requires the NO_ELIGIBLE_RISK class only; the computed result
    may carry its undetermined downstream flag, and strict exchange still holds.
    """
    assert got["outcome"] == "NO_ELIGIBLE_RISK", got
    assert got["result"].get("separation_class") == "UNDETERMINED_NO_ELIGIBLE_RISK", got
    assert got["strict_ok"], got.get("strict_error")


def assert_accepted_or_refused(case, got):
    """Finite shape: lossless acceptance or typed refusal; never an untyped crash."""
    assert got["outcome"] in ("ACCEPTED", "CONSTRUCTION_REFUSED", "CONSUMER_REFUSED"), got
    if got["outcome"] == "CONSUMER_REFUSED":
        assert_refused(case, got)
    if got["outcome"] in ("CONSTRUCTION_REFUSED", "CONSUMER_REFUSED"):
        return
    result = got["result"]
    assert got["strict_ok"], got.get("strict_error")
    assert result.get("decision_state") == "PAIR_SUPPORT_SIGNATURE_COMPUTED", result
    assert result.get("separation_class") == case.get("expect_class", "EXACT_PAIR_SEPARATION"), result
    assert result.get("downstream_value_produced") is True, result
    assert result.get("production_owner_commit") is False, result
    assert result.get("generic_native_semantics_hold") == "RETAINED", result
    n = case["n_states"]
    support = case.get("expected_support", n)
    assert result.get("joint_support_total") == support, result
    vectors = result.get("support_vectors")
    assert isinstance(vectors, dict) and len(vectors) == n, (type(vectors), result)
    assert all(isinstance(v, dict) and len(v) == n for v in vectors.values()), result
    assert _sum_vectors(vectors) == support, result
    positive = result.get("condition_states_with_positive_denominator")
    assert isinstance(positive, list) and len(positive) == n, result
    assert _is_hex64(result.get("result_hash")), result
    assert result.get("read_relation_content_hash") == got["relation_hash"], result
    assert result.get("read_relation_object_id") == got["relation_object_id"], result
    assert got.get("deterministic") is True, got


def assert_nonfinite(case, got):
    """Nonfinite is outside the strict-JSON ceiling.

    The frozen expectation is fail-closed at a typed boundary: construction
    refusal, an explicit integrity rejection, or a computed HOLD row with no
    separation and no downstream value.  A positive accepted result is a RED
    unless a future revision explicitly implements and proves a lossless strict
    exchange contract (not part of this freeze).
    """
    assert got["outcome"] in ("CONSTRUCTION_REFUSED", "CONSUMER_REFUSED", "HOLD"), got
    if got["outcome"] == "CONSUMER_REFUSED":
        assert_refused(case, got)
    elif got["outcome"] == "HOLD":
        result = got["result"]
        assert result.get("separation_class") is None, result
        assert result.get("downstream_value_produced") is False, result
        assert result.get("generic_native_semantics_hold") == "RETAINED", result
        assert got["strict_ok"], got.get("strict_error")


def assert_forged_owner_false(case, got):
    assert got["outcome"] in ("ACCEPTED", "CONSTRUCTION_REFUSED", "CONSUMER_REFUSED"), got
    if got["outcome"] != "ACCEPTED":
        return
    result = got["result"]
    assert result.get("production_owner_commit") is False, result
    assert result.get("generic_native_semantics_hold") == "RETAINED", result
    material = json.dumps(result, sort_keys=True).lower()
    assert "issuer" not in material or "issuer_authenticated" not in material, result
    assert got["strict_ok"], got.get("strict_error")
