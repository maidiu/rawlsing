"""HQ266 G01 -- G1 owner-only C1 -> REAL G2 -> authenticated F8 selected ingress.

SOURCE-FREE. TEST-ONLY UNISSUED MODEL/USE REFS. NOT AN EE14 GRANT. NOT A TRUST ROOT.
NOT DEPLOYED SECURITY. G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY.

WHAT THIS IS
------------
An owner-controlled entrypoint whose public surface accepts ONLY a fixed, enumerated,
data-only q1/q2 request. It cannot receive evidence, a C1 result, predicates, witness
callbacks, an authority registry, a model rule, an applicability receipt, a grant ref, a
currentness token, or any schema that could embed an executable object.

HQ266 G01 CORRECTION (replaces the HQ262 scope-hash stand-in)
-------------------------------------------------------------
The previous candidate hashed an owner-local applicability-scope dictionary and then
called the low-level F8 evaluator directly, bypassing the accepted applicability owner and
the accepted G2 binder entirely. That is HQ263 R01 finding **F1** and is removed here.

This ingress now runs the COMPLETE accepted chain, in this order:

  1. the owner itself calls the C1 producer with the OWNER-HELD original XOR source, the
     ORIGINAL predicate-grammar query authority and the matching registry -- the caller
     supplies only a cell name;
  2. the ACTUAL native C1 typed states are read, and a non-``SUPPORTED`` state is refused
     with that real state before any F8 evaluation (F4);
  3. the owner-held EXPECTED C1 identity must first be COMPLETE, exact and typed
     (every one of the 19 required keys present, none extraneous, each with its exact
     builtin type) -- refused at owner construction and again immediately before the
     comparison (D1) -- then the produced C1 identity / evidence / authority /
     provenance is authenticated DEEPLY, field-by-field over that closed required set,
     against the non-mutable owner-held material, not a length-of-hash test (F3) --
     and refusal happens BEFORE any F8 invocation;
  4. the REAL ``resolve_service_source_applicability`` owner builds the receipt;
  5. the REAL ``bind_service_applicability_to_f8_scope`` binder builds the G2 binding;
  6. the REAL ``evaluate_bound_positioned_subject_possibility`` consumes the UNCHANGED
     C1 evidence object and its result is required to equal the direct C1 result.

The returned receipt is a TECHNICAL ORIGIN RECEIPT binding the complete C1 identity
preimage, risk and denominator material, source and release, the exact G2
request/receipt/replay identities and the F8 result hash. It is not an issued EE14 grant,
not an independently administered root, and not runtime remote proof. ``authorizing`` is
always ``False``.

NO G0b is fabricated. No locally hashed scope stand-in remains. The accepted binder is
never bypassed.

HQ268 G01 MINIMAL REPAIR (D1 / D2)
----------------------------------
D1  The owner-held expected C1 identity is COMPLETE, exact and typed BEFORE it is
    trusted: refused at owner construction and again immediately before the
    field-by-field comparison, so authentication can never be vacuous and an
    incomplete owner setup reaches no applicability, G2 or F8 call. This is an
    internal owner-setup completeness invariant -- NOT an independent cryptographic
    trust root and NOT a source-authorized preimage.

D2  ``g2_receipt_hash`` is the ACCEPTED owner's own
    ``CandidateClassApplicabilityReceipt.replay_identity()``, never a locally
    re-derived subset of receipt fields, and ``origin_receipt_hash`` transitively
    includes it.

BOUNDED RESIDUAL (R2) -- exactly what is frozen, and what is not
----------------------------------------------------------------
FROZEN: the owner-held expected identity (deeply, at every level) and the ``_source``
and ``_cells`` containers (read-only mappings, so item assignment, deletion and the
mutating methods are all refused).

NOT FROZEN: the NESTED objects inside ``_source`` -- universe, release_ref,
repository, respondents -- remain the owner's own shared objects. The container freeze
is deliberately SHALLOW, because deep-converting those objects would change the
semantic ref objects the accepted C1/G2 owners consume, which is out of scope here.
Consequently mutating the dict handed in at construction does NOT reach the ingress,
but an in-process principal that already holds a nested object can still mutate it.
This is a trusted-harness limitation. It is not a custody root, not a trust root, and
not deployed security; the separate observation that the expected identity is derived
by re-executing the same owner compose is likewise a development invariant, not an
independent preimage.

Threat model: the bounded external DATA-ONLY service client fixed by HQ262. It does NOT
close G1 against a malicious principal executing arbitrary Python inside the owner
process; that case is explicitly UNPROVED and is out of scope.

G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional, Tuple

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import pre553_service_source_applicability as SA
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.pre553_empirical_objects import semantic_hash

CONTRACT = "HQ266_G01_OWNER_ONLY_C1_G2_F8_SELECTED_INGRESS@1"

# The ONLY cells a data-only client may name. This is a closed enumeration.
ALLOWED_CELLS = ("q1", "q2")

# The ONLY keys a data-only request may carry. Anything else is refused.
ALLOWED_REQUEST_KEYS = ("cell", "stratum_ids")

# --------------------------------------------------------------------------
# Pinned ORIGINAL predicate-grammar query authority for the four-respondent XOR
# source (HQ253 T01 witness e609be4f68 / test blob 17300a405d). The ingress
# refuses any other authority object, which structurally forbids substituting
# `test_pre553_analytical_composition._query_snapshot()` for the grammar
# authority (HQ266 hard_forbidden USE_QUERY_SNAPSHOT_AS_GRAMMAR_QUERY_AUTHORITY).
# --------------------------------------------------------------------------
PINNED_AUTHORITY_KIND = "PREDICATE_GRAMMAR"
PINNED_AUTHORITY_ID = "I03-AUTH-c1-at09-xor"
PINNED_AUTHORITY_VERSION = "1.0.0"
PINNED_AUTHORITY_CONTENT_HASH = (
    "7fbd015d4d45c533fdb2b9e48082544f284167a7dff5713e897a112b3bc94257")
PINNED_GOVERNED_OPERATIONS = ("I03-OP-c1-at09-xor",)
PINNED_GOVERNED_FAMILIES = (
    "EmpiricalFact@1.0.0",
    "EmpiricalPredicate@1.0.0",
    "EmpiricalQuerySpec@1.0.0",
)
# The rejected substitute's identity, refused explicitly rather than left implicit.
FORBIDDEN_AUTHORITY_IDS = ("C1-AT07-QUERY",)

#: Native C1 fact states that are allowed to proceed to G2 binding and F8.
#: Every other native state is refused with its REAL state and with ZERO F8 calls.
C1_PROCEED_STATES = frozenset({"SUPPORTED"})

#: The complete accepted native empirical fact-state vocabulary. Any value outside
#: this set is itself refused as an unknown native state rather than being coerced.
NATIVE_C1_FACT_STATES = frozenset({
    "SUPPORTED", "OBSERVED_ZERO", "ZERO_SUPPORT", "ZERO_OVERLAP", "LOW_SUPPORT",
    "NONCOMPARABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNCERTAINTY_UNQUANTIFIED",
    "UNRESOLVED", "VALID_EMPTY", "INTEGRITY_FAILURE",
})

# --------------------------------------------------------------------------
# D1 -- owner-held expected C1 identity COMPLETENESS (HQ268).
#
# The previous comparison was guarded by `if k in expected`, so any key absent
# from the owner-held expectation was silently never compared: owner setup could
# pass owner_identity={"q1": {}, "q2": {}} and still be issued a selected
# technical receipt. The required set below is exact and closed. Incomplete,
# mistyped or extraneous owner material is refused at owner construction AND
# again immediately before the comparison, so authentication can never be
# vacuous. This is an internal owner-setup completeness invariant, NOT an
# independent cryptographic trust root (R1) and NOT deployed security.
# --------------------------------------------------------------------------

#: The complete, exact, closed set of owner-held expected C1 identity keys.
#: Every one of these is compared on every admitted serve -- none is optional.
REQUIRED_IDENTITY_KEYS = frozenset({
    "composed_result_identity_hash",
    "producer_predicate_key",
    "producer_query_key",
    "producer_fact_key",
    "condition_binding_witness_key",
    "consumer_query_key",
    "risk_set_key",
    "denominator_member_keys",
    "raw_denominator_support",
    "evidence_ref_key",
    "source_universe_key",
    "release_key",
    "evidence_state",
    "retained_conditioner_ids",
    "evidence_authority_keys",
    "evidence_provenance_keys",
    "target_question_key",
    "source_universe_key_owner",
    "release_key_owner",
})

#: Exact builtin type required for each expected value. ``type(v) is T`` (never
#: isinstance), so a ``bool`` cannot satisfy ``raw_denominator_support`` and no
#: subclass can satisfy a scalar field.
IDENTITY_KEY_TYPES = {
    "composed_result_identity_hash": str,
    "producer_predicate_key": str,
    "producer_query_key": str,
    "producer_fact_key": str,
    "condition_binding_witness_key": str,
    "consumer_query_key": str,
    "risk_set_key": str,
    "denominator_member_keys": tuple,
    "raw_denominator_support": int,
    "evidence_ref_key": str,
    "source_universe_key": str,
    "release_key": str,
    "evidence_state": str,
    "retained_conditioner_ids": tuple,
    "evidence_authority_keys": tuple,
    "evidence_provenance_keys": tuple,
    "target_question_key": str,
    "source_universe_key_owner": str,
    "release_key_owner": str,
}


def _require_complete_identity(expected: Any, cell: str) -> None:
    """D1 fail-closed gate: owner expectation must be complete, exact and typed.

    Called at owner construction for every permitted cell AND again inside
    ``_authenticate`` immediately before the field-by-field comparison, so a
    partially populated expectation can never reach the comparison and can never
    reach applicability / G2 / F8. Raises ``SelectedIngressAuthenticationError``
    carrying the exact missing and mistyped keys.
    """
    if not isinstance(expected, Mapping):
        raise SelectedIngressAuthenticationError(
            "owner-held expected C1 identity for cell %r must be a mapping of the "
            "complete required key set; got %s" % (cell, type(expected).__name__),
            mismatched_fields=("owner_identity[%s]" % cell,),
            missing_keys=tuple(sorted(REQUIRED_IDENTITY_KEYS)))
    if not isinstance(expected, dict) and type(expected) is not MappingProxyType:
        # accepted mappings only: plain dict (construction input) or the deep-frozen
        # MappingProxyType this module itself installs. No other mapping type.
        raise SelectedIngressAuthenticationError(
            "owner-held expected C1 identity for cell %r must be a plain mapping" % cell,
            mismatched_fields=("owner_identity[%s]" % cell,),
            missing_keys=tuple(sorted(REQUIRED_IDENTITY_KEYS)))
    missing = tuple(sorted(REQUIRED_IDENTITY_KEYS - set(expected)))
    if missing:
        raise SelectedIngressAuthenticationError(
            "owner-held expected C1 identity for cell %r is INCOMPLETE (%d of %d "
            "required keys absent); authentication may not proceed vacuously. "
            "missing keys: %s"
            % (cell, len(missing), len(REQUIRED_IDENTITY_KEYS), ", ".join(missing)),
            mismatched_fields=missing,
            missing_keys=missing)
    extraneous = tuple(sorted(set(expected) - REQUIRED_IDENTITY_KEYS))
    if extraneous:
        raise SelectedIngressAuthenticationError(
            "owner-held expected C1 identity for cell %r carries %d key(s) outside "
            "the exact required set; unknown keys: %s"
            % (cell, len(extraneous), ", ".join(extraneous)),
            mismatched_fields=extraneous,
            missing_keys=())
    mistyped = tuple(sorted(
        k for k in REQUIRED_IDENTITY_KEYS
        if type(expected[k]) is not IDENTITY_KEY_TYPES[k]))
    if mistyped:
        raise SelectedIngressAuthenticationError(
            "owner-held expected C1 identity for cell %r carries wrong builtin types "
            "for: %s" % (cell, ", ".join(
                "%s (expected %s, got %s)" % (k, IDENTITY_KEY_TYPES[k].__name__,
                                              type(expected[k]).__name__)
                for k in mistyped)),
            mismatched_fields=mistyped,
            missing_keys=())


class SelectedIngressError(Exception):
    """Typed refusal from the owner-only selected ingress."""


class SelectedIngressPermissionError(SelectedIngressError):
    """Owner permission for the requested cell is absent.

    Returned instead of fabricating a real T1/G0b permission. This error is NEVER used
    to report a native C1 negative state -- see SelectedIngressC1StateError for that.
    """


class SelectedIngressC1StateError(SelectedIngressError):
    """The C1 producer returned a NATIVE negative/unsupported typed state.

    Carries the ACTUAL native state so a caller can never mistake an intrinsic C1
    outcome for a missing G0b permission (HQ263 R01 F4).
    """

    def __init__(self, message: str, *, native_state: str,
                 producer_fact_state: Optional[str]) -> None:
        super().__init__(message)
        self.native_state = native_state
        self.producer_fact_state = producer_fact_state
        #: This refusal happens BEFORE the applicability owner and BEFORE F8.
        self.f8_invoked = False
        self.applicability_invoked = False


class SelectedIngressAuthenticationError(SelectedIngressError):
    """Produced C1 identity/evidence failed deep authentication.

    Raised BEFORE any F8 invocation (HQ263 R01 F3), and before applicability / G2
    as well when the owner-held expectation itself is incomplete (HQ268 D1).

    ``mismatched_fields`` carries every required field that failed to authenticate,
    whether it was absent or present-but-different. ``missing_keys`` carries only
    the absent subset, so an incomplete owner setup is distinguishable from a
    complete expectation holding a different value.
    """

    def __init__(self, message: str, *, mismatched_fields: Tuple[str, ...],
                 missing_keys: Tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.mismatched_fields = tuple(mismatched_fields)
        self.missing_keys = tuple(missing_keys)
        self.f8_invoked = False


class SelectedIngressG2Error(SelectedIngressError):
    """The accepted applicability/G2 owner refused, or no source was admitted.

    Kept separate from SelectedIngressC1StateError so an intrinsic C1 negative is never
    attributed to G2/G0b and a G2 refusal is never attributed to C1.
    """

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.f8_invoked = False


@dataclass(frozen=True)
class SelectedRequest:
    """The complete data-only request surface.

    Two closed fields. Both are plain scalars or a tuple of plain scalars. There is no
    field through which evidence, a C1 result, a hash, an authority, a registry, a
    callback, or any object at all can be supplied.
    """

    cell: str
    stratum_ids: Tuple[str, ...]


@dataclass(frozen=True)
class CellPlan:
    """OWNER-HELD per-cell C1 construction plan.

    Pure data. The trusted constructor supplies it; a data-only client never does.
    """

    cell: str
    conditions: Tuple[Tuple[str, str, Any], ...]
    target_question: str
    tag: str
    stratum_ids: Tuple[str, ...]
    model_rule: Any


@dataclass(frozen=True)
class ApplicabilityMaterial:
    """OWNER-HELD, REAL (test-only, unissued) applicability construction material.

    These are the genuine inputs to the ACCEPTED ``resolve_service_source_applicability``
    owner. They are NOT a locally hashed scope dictionary and NOT an EE14 grant.
    """

    service_id: str
    service_authority_ref: AuthorityRef
    target_use_ref: ExactRef
    population_scope_ref: ExactRef
    geography_scope_ref: ExactRef
    effective_time_or_interval_ref: ExactRef
    candidate_class_ref: ExactRef
    target_use_permission_refs: Tuple[ExactRef, ...]
    binding_authority_ref: AuthorityRef
    admission_authority_ref: AuthorityRef
    binding_request_id: str
    #: "ADMITTED" for the positive path. Any other accepted SA decision yields a
    #: genuinely inadmissible source, which the ingress reports as its OWN typed
    #: NO_ADMITTED_SOURCE reason rather than as a C1 state.
    admission_decision: str = "ADMITTED"
    admission_basis_refs: Tuple[ExactRef, ...] = ()


@dataclass(frozen=True)
class SelectedIngressReceipt:
    """TECHNICAL origin receipt. NOT an EE14 grant, NOT a root, NOT runtime proof.

    Binds: the C1 identity and evidence preimage, the C1 risk/denominator material, the
    source and release, the EXACT G2 request/receipt/replay identities and the F8 result
    hash. A caller who retains only the F8 number cannot reconstruct it.
    """

    contract: str
    cell: str
    # -- C1 identity / preimage --
    c1_identity_hash: str
    c1_evidence_ref_key: str
    c1_evidence_projection_hash: str
    c1_evidence_authority_keys: Tuple[str, ...]
    c1_evidence_provenance_keys: Tuple[str, ...]
    c1_producer_predicate_key: str
    c1_producer_query_key: str
    c1_producer_fact_key: str
    c1_condition_witness_key: str
    # -- C1 risk / denominator --
    c1_risk_set_key: str
    c1_denominator_member_keys: Tuple[str, ...]
    c1_raw_denominator_support: int
    # -- source / release --
    source_universe_key: str
    release_key: str
    # -- exact G2 request / receipt / replay --
    g2_service_request_set_identity: str
    g2_receipt_outcome: str
    #: Exact ``CandidateClassApplicabilityReceipt.replay_identity()`` of the accepted
    #: owner's own receipt -- i.e. semantic_hash over the receipt's complete twelve-
    #: field material. Never a locally re-derived subset (HQ268 D2).
    g2_receipt_hash: str
    g2_binding_request_id: str
    g2_binding_hash: str
    g2_permission_keys: Tuple[str, ...]
    g2_query_authority_id: str
    g2_query_authority_content_hash: str
    g2_replay_protocol_key: str
    # -- F8 --
    f8_result_hash: str
    f8_result_state: str
    f8_matches_direct_c1: bool
    # -- receipt --
    origin_receipt_hash: str
    authorizing: bool = False


def _validate_request(request: Any) -> SelectedRequest:
    """Enforce the data-only contract with EXACT builtin types (HQ263 R01 F5).

    Refuses subclasses of ``SelectedRequest``, subclasses of ``str`` and subclasses of
    ``tuple``, so the public method really does accept only plain builtin scalars.
    """
    if type(request) is not SelectedRequest:
        raise SelectedIngressError(
            "selected ingress accepts only the exact builtin SelectedRequest data-only "
            "shape (subclasses are refused)")
    if type(request.cell) is not str:
        raise SelectedIngressError("request cell must be an exact builtin str")
    if request.cell not in ALLOWED_CELLS:
        raise SelectedIngressError(
            "selected ingress cell must be one of %r" % (ALLOWED_CELLS,))
    if type(request.stratum_ids) is not tuple:
        raise SelectedIngressError(
            "stratum_ids must be an exact builtin tuple of plain strings")
    if not request.stratum_ids:
        raise SelectedIngressError("stratum_ids must be a non-empty tuple of plain strings")
    for s in request.stratum_ids:
        if type(s) is not str or not s:
            raise SelectedIngressError(
                "stratum_ids entries must be exact builtin non-empty str values")
    # Belt and braces: no field of the request may carry a non-scalar object.
    for k in ALLOWED_REQUEST_KEYS:
        v = getattr(request, k, None)
        if not isinstance(v, (str, tuple)):
            raise SelectedIngressError(
                "request field %r must be a scalar or tuple of scalars" % k)
    return request


def _deep_freeze(value: Any) -> Any:
    """Recursively convert owner-held material into immutable builtins.

    MappingProxyType at every level, tuples instead of lists, so a post-construction
    nested mutation raises rather than silently rebinding custody (HQ263 R01 F5).
    """
    if isinstance(value, Mapping):
        return MappingProxyType({k: _deep_freeze(v) for k, v in dict(value).items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, tuple):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, set):
        return frozenset(_deep_freeze(v) for v in value)
    return value


def _asdict(obj: Any) -> Mapping[str, Any]:
    """Exact ``.as_dict()`` for canonical refs, otherwise ``dict(...)``."""
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    if isinstance(obj, Mapping):
        return dict(obj)
    return dict(obj)


class OwnerOnlySelectedIngress:
    """Owner-only selected ingress over the ACCEPTED C1 -> G2 -> F8 chain.

    Construction registers OWNER-HELD material: the original XOR source, the original
    predicate-grammar query authority, the matching registry, the per-cell C1 plans, the
    real applicability material, the COMPLETE expected C1 identity, and the owner-built
    C1 compose callable. That is a TRUSTED HARNESS operation and is explicitly NOT runtime
    remote proof. The public `serve` surface is data-only.

    An incomplete, mistyped or extraneous owner-held expected identity is refused here,
    at construction (D1); it is re-checked immediately before the comparison, so it can
    never reach applicability, G2 or F8.

    WHAT IS FROZEN (see the module BOUNDED RESIDUAL note): the expected identity is
    deeply frozen; ``_source`` and ``_cells`` are read-only containers. The NESTED
    objects inside ``_source`` are still the owner's shared objects -- shallow container
    freezing only. See the module docstring for the full, exact statement.
    """

    def __init__(
        self,
        *,
        source: Mapping[str, Any],
        qauth: Any,
        registry: Any,
        cells: Mapping[str, CellPlan],
        applicability: ApplicabilityMaterial,
        owner_identity: Mapping[str, Mapping[str, Any]],
        c1_compose: Callable[..., Any],
    ) -> None:
        """TRUSTED HARNESS SETUP ONLY -- never remote, never data-only."""
        missing = set(ALLOWED_CELLS) - set(cells)
        if missing:
            raise SelectedIngressError(
                "owner setup must register owner-held plans for cells %r" % (sorted(missing),))
        for cell in ALLOWED_CELLS:
            plan = cells[cell]
            if type(plan) is not CellPlan or plan.cell != cell:
                raise SelectedIngressError(
                    "owner setup plan for cell %r must be the exact builtin CellPlan "
                    "registered under that cell" % cell)
        # ---- the ORIGINAL predicate-grammar query authority is pinned and verified ----
        self._qauth = qauth
        self._verify_query_authority(qauth)
        if registry is None:
            raise SelectedIngressError("owner setup must register the authority registry")
        if not callable(c1_compose):
            raise SelectedIngressError("owner setup must register the owner-built C1 compose")
        if not isinstance(source, Mapping) or "release_ref" not in source or "universe" not in source:
            raise SelectedIngressError(
                "owner setup must register the original XOR source carrying release_ref "
                "and universe")
        # ---- R2: the live owner containers are read-only mappings ----
        # Shallow container freeze only: the nested objects (universe, release_ref,
        # respondents, ...) stay the owner's own shared objects. Converting them
        # would change the semantic refs the accepted C1/G2 owners consume, which is
        # explicitly out of scope here. See the class docstring BOUNDED RESIDUAL note.
        self._source = MappingProxyType(dict(source))
        self._registry = registry
        self._cells = MappingProxyType({k: cells[k] for k in ALLOWED_CELLS})
        self._applicability = applicability
        # ---- D1: owner-held expectation must be COMPLETE, exact and typed ----
        # Refused here, at owner construction, BEFORE any request can be served and
        # therefore before applicability / G2 / F8 can ever be reached. Re-checked
        # again inside _authenticate immediately before the comparison.
        if not isinstance(owner_identity, Mapping):
            raise SelectedIngressAuthenticationError(
                "owner-held expected C1 identity must be a mapping of the complete "
                "required key set for every permitted cell; got %s"
                % type(owner_identity).__name__,
                mismatched_fields=("owner_identity",),
                missing_keys=tuple(sorted(REQUIRED_IDENTITY_KEYS)))
        for cell in ALLOWED_CELLS:
            if cell not in owner_identity:
                raise SelectedIngressAuthenticationError(
                    "owner-held expected C1 identity is missing cell %r entirely; "
                    "authentication may not proceed vacuously" % cell,
                    mismatched_fields=("owner_identity[%s]" % cell,),
                    missing_keys=tuple(sorted(REQUIRED_IDENTITY_KEYS)))
            _require_complete_identity(owner_identity[cell], cell)
        # non-mutable owner-held expected identity, deeply frozen
        self._owner_identity = _deep_freeze(dict(owner_identity))
        self._c1_compose = c1_compose
        self._frozen = True

    # -- pinned query-authority verification (HQ266 hard forbidden substitute) --

    @staticmethod
    def _authority_fields(qauth: Any) -> Mapping[str, Any]:
        fields = getattr(qauth, "semantic_fields", None)
        if not isinstance(fields, Mapping):
            raise SelectedIngressError(
                "owner-held query authority carries no semantic_fields; the original "
                "predicate-grammar AuthoritySnapshot is required")
        return fields

    def _verify_query_authority(self, qauth: Any) -> None:
        f = self._authority_fields(qauth)
        kind = f.get("authority_kind")
        aid = f.get("authority_id")
        if aid in FORBIDDEN_AUTHORITY_IDS:
            raise SelectedIngressError(
                "query authority %r is a snapshot-style substitute; the original "
                "predicate-grammar authority %r is required and no substitute is accepted"
                % (aid, PINNED_AUTHORITY_ID))
        if kind != PINNED_AUTHORITY_KIND:
            raise SelectedIngressError(
                "query authority_kind must be %r, got %r"
                % (PINNED_AUTHORITY_KIND, kind))
        if aid != PINNED_AUTHORITY_ID:
            raise SelectedIngressError(
                "query authority_id must be the original %r, got %r"
                % (PINNED_AUTHORITY_ID, aid))
        if f.get("authority_version") != PINNED_AUTHORITY_VERSION:
            raise SelectedIngressError("query authority_version is not the pinned original")
        if f.get("authority_content_hash") != PINNED_AUTHORITY_CONTENT_HASH:
            raise SelectedIngressError("query authority_content_hash is not the pinned original")
        if tuple(f.get("governed_operations") or ()) != PINNED_GOVERNED_OPERATIONS:
            raise SelectedIngressError(
                "query authority governed_operations must be the pinned XOR authority's")
        if tuple(sorted(f.get("governed_object_families") or ())) != \
                tuple(sorted(PINNED_GOVERNED_FAMILIES)):
            raise SelectedIngressError(
                "query authority governed_object_families must be exactly the three "
                "grammar families")

    # -- trusted harness introspection (read-only, NOT a public data surface) --

    def owner_scope_material(self) -> Mapping[str, Any]:
        """Deeply immutable owner material. Replaces the removed scope-hash stand-in."""
        return _deep_freeze({
            "contract": CONTRACT,
            "applicability": self._applicability,
            "owner_identity": self._owner_identity,
            "query_authority_id": PINNED_AUTHORITY_ID,
            "query_authority_content_hash": PINNED_AUTHORITY_CONTENT_HASH,
            "cells": {k: {"cell": v.cell, "conditions": v.conditions,
                          "target_question": v.target_question, "tag": v.tag,
                          "stratum_ids": v.stratum_ids}
                      for k, v in self._cells.items()},
            "source_release_key": self._source["release_ref"].object_id,
            "source_universe_key": self._source["universe"].ref.object_id,
        })

    def cells(self) -> Tuple[str, ...]:
        return ALLOWED_CELLS

    # ------------------------------------------------------------------ serve

    def serve(self, request: Any) -> SelectedIngressReceipt:
        """The ONLY public entrypoint. Data-only."""
        req = _validate_request(request)

        plan = self._cells.get(req.cell)
        if plan is None:
            raise SelectedIngressError("cell %r is not registered by the owner" % req.cell)

        # ---- 1. OWNER CALLS C1 ITSELF with owner-held source/authority/registry. ----
        composed, consumer_query = self._call_c1(plan)

        # ---- 2. READ THE ACTUAL NATIVE C1 TYPED STATES (F4). Zero F8 on refusal. ----
        evidence = self._require_supported_c1(composed, plan)

        # ---- 3. stratum grain must match what C1 actually retained ----
        retained = tuple(getattr(evidence, "retained_conditioner_ids", ()))
        if retained != tuple(req.stratum_ids):
            raise SelectedIngressError(
                "C1-originated evidence grain %r does not match the requested "
                "stratum_ids %r; no substitution is permitted"
                % (retained, tuple(req.stratum_ids)))

        # ---- 4. DEEP AUTHENTICATION against non-mutable owner-held material (F3).
        #         Refuses BEFORE any F8 invocation.
        self._authenticate(composed, evidence, req)

        # ---- 5. REAL applicability owner -> authentic receipt ----
        receipt = self._resolve_applicability()

        # ---- 6. REAL accepted G2 binder -> binding ----
        g2_request, binding = self._bind_g2(receipt, plan)

        # ---- 7. REAL bound-F8 evaluation with the UNCHANGED C1 evidence object ----
        out = B.evaluate_bound_positioned_subject_possibility(
            binding=binding, request=g2_request, receipt=receipt,
            query=consumer_query, rule=plan.model_rule, evidence=(evidence,))

        # ---- 8. full result/material parity with the direct C1 result ----
        direct = getattr(composed, "consumer_result_or_null", None)
        matches_direct = (
            direct is not None
            and out.result_hash == direct.result_hash
            and out.material() == direct.material()
        )
        if not matches_direct:
            raise SelectedIngressG2Error(
                "bound F8 result does not equal the direct C1 result for cell %r; "
                "parity is required" % req.cell,
                reason_code="BOUND_F8_DIRECT_C1_PARITY_FAILURE")

        # ---- 9. TECHNICAL ORIGIN RECEIPT: binds everything, authorizing=False ----
        return self._build_receipt(req, composed, evidence, receipt, g2_request,
                                   binding, out)

    # -------------------------------------------------------------- internals

    def _call_c1(self, plan: CellPlan) -> Tuple[Any, Any]:
        """Call the owner-built C1 producer with the OWNER-HELD source and authority.

        The caller never supplies these, so the compose step cannot be steered to a
        different source, release or query authority.
        """
        produced = self._c1_compose(
            source=self._source,
            qauth=self._qauth,
            registry=self._registry,
            conditions=plan.conditions,
            target_question=plan.target_question,
            tag=plan.tag,
        )
        if isinstance(produced, tuple) and len(produced) == 2:
            composed, consumer_query = produced
        else:
            raise SelectedIngressError(
                "owner-built C1 compose must return (composition, consumer_query)")
        if composed is None or consumer_query is None:
            raise SelectedIngressError("owner-built C1 compose returned an incomplete product")
        return composed, consumer_query

    def _require_supported_c1(self, composed: Any, plan: CellPlan) -> Any:
        """F4: read the REAL native states; never relabel them as a missing G0b."""
        analytical_state = getattr(composed, "analytical_state", None)
        producer_fact_state = getattr(composed, "producer_fact_state", None)
        evidence = getattr(composed, "possibility_slice_evidence_or_null", None)

        for label, value in (("analytical_state", analytical_state),
                             ("producer_fact_state", producer_fact_state)):
            if value is None:
                raise SelectedIngressC1StateError(
                    "C1 producer returned no %s for cell %r; the native state cannot be "
                    "read" % (label, plan.cell),
                    native_state="UNKNOWN_OR_UNRESOLVED",
                    producer_fact_state=producer_fact_state)
            if value not in NATIVE_C1_FACT_STATES:
                raise SelectedIngressC1StateError(
                    "C1 producer returned %s %r for cell %r, which is outside the accepted "
                    "native empirical fact-state vocabulary"
                    % (label, value, plan.cell),
                    native_state="UNKNOWN_OR_UNRESOLVED",
                    producer_fact_state=producer_fact_state)

        if evidence is None:
            # The real native state is reported. This is NOT a permission/G0b claim.
            raise SelectedIngressC1StateError(
                "C1 producer produced no possibility slice evidence for cell %r because "
                "its native state is %r (producer fact state %r); this is an intrinsic C1 "
                "outcome and is NOT a missing-EE14-G0b condition"
                % (plan.cell, analytical_state, producer_fact_state),
                native_state=analytical_state,
                producer_fact_state=producer_fact_state)

        if analytical_state not in C1_PROCEED_STATES or \
                producer_fact_state not in C1_PROCEED_STATES:
            raise SelectedIngressC1StateError(
                "C1 native state %r / %r for cell %r is not a proceeding state; G2 binding "
                "and F8 are not exercised (intrinsic C1 outcome, no G0b is implied)"
                % (analytical_state, producer_fact_state, plan.cell),
                native_state=analytical_state,
                producer_fact_state=producer_fact_state)
        return evidence

    def _authenticate(self, composed: Any, evidence: Any, req: SelectedRequest) -> None:
        """F3: structured deep authentication BEFORE any F8 invocation.

        Compares the produced C1 identity and evidence material field-by-field against
        the non-mutable owner-held expectation. Not a length-of-hash or regex test.

        D1: the owner-held expectation is re-validated for COMPLETENESS here, right
        before the comparison, so an incomplete expectation can never produce a
        vacuous pass. The comparison then iterates the closed required key set, so
        every required field is compared -- a field is never skipped because it is
        absent from the expectation, and an absent key can no longer be skipped.
        This runs before applicability / G2 / F8, so an incomplete owner setup
        reaches none of them.
        """
        expected = self._owner_identity.get(req.cell)
        if expected is None:
            raise SelectedIngressAuthenticationError(
                "owner held no expected C1 identity for cell %r" % req.cell,
                mismatched_fields=("owner_identity",),
                missing_keys=tuple(sorted(REQUIRED_IDENTITY_KEYS)))

        # ---- D1 fail-closed gate: completeness before any comparison ----
        _require_complete_identity(expected, req.cell)

        observed = {
            "composed_result_identity_hash": getattr(
                composed, "composed_result_identity_hash", None),
            "producer_predicate_key": _key(getattr(composed, "producer_predicate_ref", None)),
            "producer_query_key": _key(getattr(composed, "producer_query_ref", None)),
            "producer_fact_key": _key(getattr(composed, "producer_fact_ref", None)),
            "condition_binding_witness_key": _key(getattr(
                composed, "condition_binding_witness_ref_or_hash", None)),
            "consumer_query_key": _key(getattr(composed, "consumer_query_ref", None)),
            "risk_set_key": _key(getattr(composed, "risk_set_ref", None)),
            "denominator_member_keys": tuple(
                _key(r) for r in (getattr(composed, "denominator_member_refs", ()) or ())),
            "raw_denominator_support": getattr(composed, "raw_denominator_support", None),
            "evidence_ref_key": _key(getattr(evidence, "evidence_ref", None)),
            "source_universe_key": _key(getattr(evidence, "source_universe_ref", None)),
            "release_key": _key(getattr(evidence, "release_ref", None)),
            "evidence_state": getattr(evidence, "evidence_state", None),
            "retained_conditioner_ids": tuple(
                getattr(evidence, "retained_conditioner_ids", ()) or ()),
            "evidence_authority_keys": tuple(
                _key(a) for a in (getattr(evidence, "authority_refs", ()) or ())),
            "evidence_provenance_keys": tuple(
                _key(p) for p in (getattr(evidence, "provenance_refs", ()) or ())),
            "target_question_key": _key(getattr(evidence, "target_ref", None)),
        }

        # the source and release the ingress itself holds are authoritative too
        observed["source_universe_key_owner"] = self._source["universe"].ref.object_id
        observed["release_key_owner"] = self._source["release_ref"].object_id

        # internal drift guard: the builder must cover the closed required set
        # exactly, so neither side can silently diverge from REQUIRED_IDENTITY_KEYS.
        observed_missing = tuple(sorted(REQUIRED_IDENTITY_KEYS - set(observed)))
        observed_extra = tuple(sorted(set(observed) - REQUIRED_IDENTITY_KEYS))
        if observed_missing or observed_extra:
            raise SelectedIngressAuthenticationError(
                "observed C1 identity builder does not cover REQUIRED_IDENTITY_KEYS "
                "exactly (missing: %s; extra: %s); authentication would not be "
                "exhaustive" % (list(observed_missing), list(observed_extra)),
                mismatched_fields=observed_missing + observed_extra,
                missing_keys=observed_missing)

        # every required field is compared -- membership of the expectation is
        # irrelevant, because completeness was already proven above
        mismatches = tuple(
            sorted(k for k in REQUIRED_IDENTITY_KEYS if observed[k] != expected[k]))
        if mismatches:
            raise SelectedIngressAuthenticationError(
                "produced C1 identity/evidence does not authenticate against non-mutable "
                "owner-held material for cell %r; mismatched fields: %s"
                % (req.cell, ", ".join(mismatches)),
                mismatched_fields=mismatches,
                missing_keys=())

        if not getattr(evidence, "authority_refs", None) or \
                not getattr(evidence, "provenance_refs", None):
            raise SelectedIngressAuthenticationError(
                "C1-originated evidence lacks authority/provenance custody material",
                mismatched_fields=("evidence_authority_keys", "evidence_provenance_keys"))

    def _resolve_applicability(self) -> Any:
        """The REAL accepted applicability owner. No local scope hash anywhere."""
        universe = self._source["universe"].ref
        mat = self._applicability
        candidate_class = SA.CandidateClassBinding(
            candidate_class_ref=_asdict(mat.candidate_class_ref),
            candidate_source_universe_refs=[universe.as_dict()],
            binding_authority_ref=_asdict(mat.binding_authority_ref),
            declared_population_scope_ref=_asdict(mat.population_scope_ref),
            declared_geography_scope_ref=_asdict(mat.geography_scope_ref),
        )
        service_request = SA.ServiceApplicabilityRequest.build(
            service_id=mat.service_id,
            service_authority_ref=_asdict(mat.service_authority_ref),
            target_use_ref=_asdict(mat.target_use_ref),
            population_scope_ref=_asdict(mat.population_scope_ref),
            geography_scope_ref=_asdict(mat.geography_scope_ref),
            effective_time_or_interval_ref=_asdict(mat.effective_time_or_interval_ref),
            candidate_class_ref=_asdict(mat.candidate_class_ref),
            release_identity_ref=self._source["release_ref"].as_dict(),
            target_use_permission_refs=[_asdict(p) for p in mat.target_use_permission_refs],
            candidate_source_universe_refs=[universe.as_dict()],
        )
        if mat.admission_decision == "ADMITTED":
            records = [SA.ApplicabilityAuthorityRecord(
                universe, mat.admission_decision, _asdict(mat.admission_authority_ref))]
        else:
            records = [SA.ApplicabilityAuthorityRecord(
                universe, mat.admission_decision,
                basis_refs=tuple(mat.admission_basis_refs))]

        receipt = SA.resolve_service_source_applicability(
            service_request, candidate_class, records)

        # Distinguish "no admitted source" from an admitted source with missing evidence.
        admissible = receipt.admissible_source_universe_refs_as_set()
        if universe.as_dict() not in admissible:
            raise SelectedIngressG2Error(
                "applicability owner admitted no source universe for this service and "
                "use (NO_ADMITTED_SOURCE); this is an applicability outcome, not a C1 "
                "native negative and not a fabricated G0b",
                reason_code="NO_ADMITTED_SOURCE")
        return receipt

    def _bind_g2(self, receipt: Any, plan: CellPlan) -> Tuple[Any, Any]:
        """The REAL accepted G2 binder with exact permission/release/source coherence."""
        mat = self._applicability
        universe = self._source["universe"].ref
        g2_request = B.ServiceApplicabilityF8ScopeBindingRequest(
            binding_request_id=mat.binding_request_id,
            service_request_set_identity=receipt.service_request_set_identity,
            candidate_class_ref=ExactRef(**dict(_asdict(mat.candidate_class_ref))),
            service_id=mat.service_id,
            target_use_ref=mat.target_use_ref,
            release_identity_ref=self._source["release_ref"],
            bound_target_use_permission_refs=tuple(mat.target_use_permission_refs),
            binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
            requested_source_universe_ref=universe,
            # NO fabricated CURRENT. Nothing in this ingress claims a current/as-of result.
            requested_currentness_claim=None,
            requested_purpose=None,
        )
        # the SAME owner-held per-cell model rule is used for binding and for the bound
        # evaluation, so the two can never disagree about which cell's rule applies.
        return g2_request, B.bind_service_applicability_to_f8_scope(
            request=g2_request, receipt=receipt, rule=plan.model_rule)

    def _build_receipt(self, req, composed, evidence, receipt, g2_request,
                       binding, out) -> SelectedIngressReceipt:
        plan = self._cells[req.cell]
        qf = self._authority_fields(self._qauth)
        ev_material = _evidence_material(evidence)

        ev_hash = semantic_hash(
            evidence.semantic_projection() if hasattr(evidence, "semantic_projection")
            else ev_material)

        binding_material = binding.material()
        binding_hash = semantic_hash(_plain(binding_material))

        # ---- D2: G2 replay identity comes from the ACCEPTED OWNER ----
        # The previous implementation hand-rolled six of the receipt's twelve
        # material fields, so receipt_id, no_applicable_source,
        # candidate_class_binding, request_key, canonical_replay_only_order and
        # authorised_authority did not discriminate this hash at all, and the value
        # was not transitively bound by the accepted owner's own replay identity.
        # The accepted owner already defines the exact primitive -- see
        # CandidateClassApplicabilityReceipt.replay_identity(), which is
        # semantic_hash(self._material()). We take it from there and do not
        # re-derive anything locally.
        g2_receipt_hash = receipt.replay_identity()

        origin_material = {
            "contract": CONTRACT,
            "cell": req.cell,
            "stratum_ids": list(req.stratum_ids),
            # C1 identity / preimage
            "c1_identity_hash": getattr(composed, "composed_result_identity_hash", None),
            "c1_evidence_ref_key": _key(evidence.evidence_ref),
            "c1_evidence_projection_hash": ev_hash,
            "c1_evidence_authority_keys": [_key(a) for a in evidence.authority_refs],
            "c1_evidence_provenance_keys": [_key(p) for p in evidence.provenance_refs],
            "c1_producer_predicate_key": _key(composed.producer_predicate_ref),
            "c1_producer_query_key": _key(composed.producer_query_ref),
            "c1_producer_fact_key": _key(composed.producer_fact_ref),
            "c1_condition_witness_key": _key(
                composed.condition_binding_witness_ref_or_hash),
            "c1_consumer_query_key": _key(composed.consumer_query_ref),
            # risk / denominator
            "c1_risk_set_key": _key(composed.risk_set_ref),
            "c1_denominator_member_keys": [_key(r) for r in composed.denominator_member_refs],
            "c1_raw_denominator_support": composed.raw_denominator_support,
            "c1_analytical_state": composed.analytical_state,
            "c1_producer_fact_state": composed.producer_fact_state,
            # source / release
            "source_universe_key": self._source["universe"].ref.object_id,
            "release_key": self._source["release_ref"].object_id,
            # exact G2 request / receipt / replay
            "g2_service_request_set_identity": receipt.service_request_set_identity,
            "g2_receipt_outcome": receipt.outcome,
            "g2_receipt_hash": g2_receipt_hash,
            # D2 residual: the accepted owner's own _material() -- and therefore
            # replay_identity() -- does NOT include canonical_replay_only_order, so
            # binding it only inside g2_receipt_hash would leave it unbound. The
            # origin layer binds it directly. (The adopted SA owner is read-only; the
            # ingress may only add, never redefine, what it carries.)
            "g2_canonical_replay_only_order": list(receipt.canonical_replay_only_order),
            "g2_binding_request_id": g2_request.binding_request_id,
            "g2_binding_hash": binding_hash,
            "g2_permission_keys": [p.object_id
                                   for p in g2_request.bound_target_use_permission_refs],
            "g2_query_authority_id": qf.get("authority_id"),
            "g2_query_authority_content_hash": qf.get("authority_content_hash"),
            "g2_replay_protocol_key": dict(qf.get("replay_protocol_ref") or {}).get(
                "object_id"),
            "g2_currentness": g2_request.requested_currentness_claim,
            # F8
            "f8_result_hash": out.result_hash,
            "f8_result_state": out.result_state,
            "f8_matches_direct_c1": True,
            # technical only
            "authorizing": False,
        }

        return SelectedIngressReceipt(
            contract=CONTRACT,
            cell=req.cell,
            c1_identity_hash=origin_material["c1_identity_hash"],
            c1_evidence_ref_key=origin_material["c1_evidence_ref_key"],
            c1_evidence_projection_hash=ev_hash,
            c1_evidence_authority_keys=tuple(origin_material["c1_evidence_authority_keys"]),
            c1_evidence_provenance_keys=tuple(
                origin_material["c1_evidence_provenance_keys"]),
            c1_producer_predicate_key=origin_material["c1_producer_predicate_key"],
            c1_producer_query_key=origin_material["c1_producer_query_key"],
            c1_producer_fact_key=origin_material["c1_producer_fact_key"],
            c1_condition_witness_key=origin_material["c1_condition_witness_key"],
            c1_risk_set_key=origin_material["c1_risk_set_key"],
            c1_denominator_member_keys=tuple(
                origin_material["c1_denominator_member_keys"]),
            c1_raw_denominator_support=composed.raw_denominator_support,
            source_universe_key=origin_material["source_universe_key"],
            release_key=origin_material["release_key"],
            g2_service_request_set_identity=receipt.service_request_set_identity,
            g2_receipt_outcome=receipt.outcome,
            g2_receipt_hash=g2_receipt_hash,
            g2_binding_request_id=g2_request.binding_request_id,
            g2_binding_hash=binding_hash,
            g2_permission_keys=tuple(origin_material["g2_permission_keys"]),
            g2_query_authority_id=origin_material["g2_query_authority_id"],
            g2_query_authority_content_hash=origin_material[
                "g2_query_authority_content_hash"],
            g2_replay_protocol_key=origin_material["g2_replay_protocol_key"],
            f8_result_hash=out.result_hash,
            f8_result_state=out.result_state,
            f8_matches_direct_c1=True,
            origin_receipt_hash=semantic_hash(origin_material),
            authorizing=False,
        )


def _key(ref: Any) -> str:
    """Stable key for an ExactRef / AuthorityRef / plain ref-like value.

    ExactRef carries ``object_id``; AuthorityRef carries ``authority_id``. Both resolve
    here so owner-held expectations and observed material always compare like for like.
    """
    if ref is None:
        return ""
    if isinstance(ref, str):
        return ref
    for attr in ("object_id", "authority_id"):
        value = getattr(ref, attr, None)
        if isinstance(value, str) and value:
            return value
    if isinstance(ref, Mapping):
        for attr in ("object_id", "authority_id", "key"):
            value = ref.get(attr)
            if isinstance(value, str) and value:
                return value
    value = getattr(ref, "key", None)
    if isinstance(value, str) and value:
        return value
    return str(ref)


def _plain(value: Any) -> Any:
    """Convert mappingproxy / nested owner material into plain builtins for hashing."""
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in dict(value).items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_plain(v) for v in value), key=repr)
    return value


def _evidence_material(evidence: Any) -> Mapping[str, Any]:
    return {
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "source_universe_ref": evidence.source_universe_ref.as_dict(),
        "release_ref": evidence.release_ref.as_dict(),
        "target_ref": evidence.target_ref.as_dict(),
        "retained_conditioner_ids": list(evidence.retained_conditioner_ids),
        "evidence_state": evidence.evidence_state,
        "geometry": _plain(evidence.geometry),
        "raw_support": _plain(evidence.raw_support),
        "uncertainty_state": evidence.uncertainty_state,
        "provenance_refs": [p.as_dict() for p in evidence.provenance_refs],
        "authority_refs": [a.as_dict() for a in evidence.authority_refs],
    }
