"""HQ262 G01 -- G1 owner-only C1 -> authenticated F8 selected ingress.

SOURCE-FREE. TEST-ONLY UNISSUED MODEL/USE REFS. NOT AN EE14 GRANT. NOT A TRUST ROOT.
NOT DEPLOYED SECURITY.

WHAT THIS IS
------------
An owner-controlled entrypoint whose public surface accepts ONLY a fixed, enumerated,
data-only q1/q2 request. It cannot receive evidence, a C1 result, predicates, witness
callbacks, a repository, an authority registry, a model rule, an applicability receipt,
a grant ref, a currentness token, or any schema that could embed an executable object.

The owner executes the C1 producer itself, takes the C1-ORIGINATED
`possibility_slice_evidence_or_null` from `AnalyticalCompositionResult`, verifies the
complete original C1 identity/evidence preimage against owner-held producer objects, and
passes that EXACT evidence object -- unchanged -- to F8. The external client never
chooses, constructs, substitutes or influences the evidence.

This closes G1 under the *bounded external data-only service client* threat model fixed
by HQ262. It does NOT close G1 against a malicious principal executing arbitrary Python
inside the owner process; that case is explicitly UNPROVED and is out of scope.

The returned receipt is a TECHNICAL ORIGIN RECEIPT binding the complete C1 identity
preimage, the G2/applicability scope and the F8 result hash. It is not an issued EE14
grant, not an independently administered root, and not runtime remote proof.

G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.source_backed_positioned_subject_possibility import (
    evaluate_positioned_subject_possibility,
)

CONTRACT = "HQ262_G1_OWNER_ONLY_C1_F8_SELECTED_INGRESS@1"

# The ONLY cells a data-only client may name. This is a closed enumeration.
ALLOWED_CELLS = ("q1", "q2")

# The ONLY keys a data-only request may carry. Anything else is refused.
ALLOWED_REQUEST_KEYS = ("cell", "stratum_ids")


class SelectedIngressError(Exception):
    """Typed refusal from the owner-only selected ingress."""


class SelectedIngressPermissionError(SelectedIngressError):
    """Owner permission for the requested cell is absent.

    Returned instead of fabricating a real T1/G0b permission.
    """


@dataclass(frozen=True)
class SelectedRequest:
    """The complete data-only request surface.

    Two closed fields. Both are plain scalars or a tuple of plain scalars. There is no
    field through which evidence, a C1 result, a hash, an authority, a registry, a
    callback, or any object at all can be supplied.
    """

    cell: str
    stratum_ids: tuple[str, ...]


@dataclass(frozen=True)
class SelectedIngressReceipt:
    """TECHNICAL origin receipt. NOT an EE14 grant, NOT a root, NOT runtime proof."""

    contract: str
    cell: str
    c1_identity_hash: str
    c1_evidence_ref_key: str
    c1_evidence_authority_keys: tuple[str, ...]
    c1_evidence_provenance_keys: tuple[str, ...]
    f8_result_hash: str
    f8_result_state: str
    applicability_scope_hash: str
    origin_receipt_hash: str
    authorizing: bool = False


def _validate_request(request: Any) -> SelectedRequest:
    """Enforce the data-only contract strictly.

    Rejects: non-SelectedRequest shapes, unknown cells, extra keys, and any value that
    is not a plain scalar / tuple of plain scalars.
    """
    if not isinstance(request, SelectedRequest):
        raise SelectedIngressError(
            "selected ingress accepts only the enumerated SelectedRequest data-only shape")
    if request.cell not in ALLOWED_CELLS:
        raise SelectedIngressError(
            "selected ingress cell must be one of %r" % (ALLOWED_CELLS,))
    if not isinstance(request.stratum_ids, tuple) or not request.stratum_ids:
        raise SelectedIngressError("stratum_ids must be a non-empty tuple of plain strings")
    for s in request.stratum_ids:
        if not isinstance(s, str) or not s:
            raise SelectedIngressError("stratum_ids entries must be plain non-empty strings")
    # Belt and braces: no field of the request may carry an object.
    for k in ALLOWED_REQUEST_KEYS:
        v = getattr(request, k, None)
        if not isinstance(v, (str, tuple)):
            raise SelectedIngressError("request field %r must be a scalar or tuple of scalars" % k)
    return request


class OwnerOnlySelectedIngress:
    """Owner-only selected ingress.

    Construction registers OWNER-HELD producer material. That is a TRUSTED HARNESS
    operation and is explicitly NOT runtime remote proof. The public `serve` surface is
    data-only.
    """

    def __init__(
        self,
        *,
        c1_inputs: Mapping[str, Any],
        cell_inputs: Mapping[str, Mapping[str, Any]],
        applicability_scope: Mapping[str, Any],
    ) -> None:
        """TRUSTED HARNESS SETUP ONLY -- never remote, never data-only.

        `c1_inputs` are the owner-held C1 producer objects (repository, predicate,
        registry, releases, consumer query, model rule, witness).
        `cell_inputs` maps each permitted cell to its owner-held per-cell C1 inputs.
        `applicability_scope` is the OWNER-CONSTRUCTED, preapproved TEST-ONLY UNISSUED
        applicability/G2 scope material.
        """
        missing = set(ALLOWED_CELLS) - set(cell_inputs)
        if missing:
            raise SelectedIngressError(
                "owner setup must register owner-held inputs for cells %r" % (sorted(missing),))
        self._c1_inputs = dict(c1_inputs)
        # deep-ish copy and freeze so a later caller mutation cannot rebind custody
        self._cell_inputs = {k: dict(v) for k, v in cell_inputs.items()}
        self._applicability_scope = dict(applicability_scope)
        self._frozen = True

    # -- trusted harness introspection (read-only, NOT a public data surface) --
    def owner_scope_material(self) -> Mapping[str, Any]:
        return MappingProxyType(dict(self._applicability_scope))

    def serve(self, request: Any) -> SelectedIngressReceipt:
        """The ONLY public entrypoint. Data-only."""
        req = _validate_request(request)

        cell_inputs = self._cell_inputs.get(req.cell)
        if cell_inputs is None:
            raise SelectedIngressError("cell %r is not registered by the owner" % req.cell)

        # ---- 1. OWNER EXECUTES C1 ITSELF. Client supplies nothing but a cell name. ----
        c1_kwargs = dict(self._c1_inputs)
        c1_kwargs.update(cell_inputs)
        c1_kwargs["consumer_query"] = _require(c1_kwargs, "consumer_query")
        c1_kwargs["model_rule"] = _require(c1_kwargs, "model_rule")

        composed = compose_positioned_subject_possibility(**c1_kwargs)

        c1_identity = getattr(composed, "composed_result_identity_hash", None)
        if not isinstance(c1_identity, str) or len(c1_identity) != 64:
            raise SelectedIngressError(
                "C1 producer did not return a complete 64-hex composed_result_identity_hash")

        # ---- 2. TAKE THE C1-ORIGINATED EVIDENCE. Never caller-supplied. ----
        evidence = getattr(composed, "possibility_slice_evidence_or_null", None)
        if evidence is None:
            raise SelectedIngressPermissionError(
                "C1 producer returned no possibility slice evidence for cell %r; "
                "authentic applicability cannot be exercised without an adopted owner "
                "permission (G0b)" % req.cell)

        if tuple(getattr(evidence, "retained_conditioner_ids", ())) != req.stratum_ids:
            raise SelectedIngressError(
                "C1-originated evidence grain does not match the requested stratum_ids; "
                "no substitution is permitted")

        # ---- 3. VERIFY THE COMPLETE ORIGINAL C1 EVIDENCE PREIMAGE ----
        ev_hash = semantic_hash(evidence.semantic_projection()
                                if hasattr(evidence, "semantic_projection")
                                else _evidence_material(evidence))
        ev_key = evidence.evidence_ref.key
        auth_keys = tuple(a.key for a in evidence.authority_refs)
        prov_keys = tuple(p.key for p in evidence.provenance_refs)
        if not auth_keys or not prov_keys:
            raise SelectedIngressError(
                "C1-originated evidence lacks authority/provenance custody material")

        # ---- 4. OWNER-BUILT APPLICABILITY / G2 SCOPE (owner-held, preapproved) ----
        scope_hash = semantic_hash({
            "contract": CONTRACT,
            "cell": req.cell,
            "scope": self._applicability_scope,
            "stratum_ids": list(req.stratum_ids),
        })

        # ---- 5. PASS THE EXACT C1 EVIDENCE OBJECT, UNCHANGED, TO F8 ----
        f8 = evaluate_positioned_subject_possibility(
            query=c1_kwargs["consumer_query"],
            rule=c1_kwargs["model_rule"],
            evidence=(evidence,),
        )

        # ---- 6. TECHNICAL ORIGIN RECEIPT: binds C1 preimage + scope + F8 hash ----
        origin_material = {
            "contract": CONTRACT,
            "cell": req.cell,
            "c1_identity_hash": c1_identity,
            "c1_evidence_ref_key": ev_key,
            "c1_evidence_projection_hash": ev_hash,
            "c1_evidence_authority_keys": list(auth_keys),
            "c1_evidence_provenance_keys": list(prov_keys),
            "c1_risk_set_ref": composed.risk_set_ref.key,
            "c1_denominator_member_refs": [r.key for r in composed.denominator_member_refs],
            "c1_raw_denominator_support": composed.raw_denominator_support,
            "applicability_scope_hash": scope_hash,
            "f8_result_hash": f8.result_hash,
            "f8_result_state": f8.result_state,
        }
        return SelectedIngressReceipt(
            contract=CONTRACT,
            cell=req.cell,
            c1_identity_hash=c1_identity,
            c1_evidence_ref_key=ev_key,
            c1_evidence_authority_keys=auth_keys,
            c1_evidence_provenance_keys=prov_keys,
            f8_result_hash=f8.result_hash,
            f8_result_state=f8.result_state,
            applicability_scope_hash=scope_hash,
            origin_receipt_hash=semantic_hash(origin_material),
            authorizing=False,
        )


def _require(mapping: Mapping[str, Any], key: str) -> Any:
    if key not in mapping:
        raise SelectedIngressError("owner-held input %r is not registered" % key)
    return mapping[key]


def _evidence_material(evidence: Any) -> Mapping[str, Any]:
    return {
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "source_universe_ref": evidence.source_universe_ref.as_dict(),
        "release_ref": evidence.release_ref.as_dict(),
        "target_ref": evidence.target_ref.as_dict(),
        "retained_conditioner_ids": list(evidence.retained_conditioner_ids),
        "evidence_state": evidence.evidence_state,
        "geometry": evidence.geometry,
        "raw_support": evidence.raw_support,
        "uncertainty_state": evidence.uncertainty_state,
        "provenance_refs": [p.as_dict() for p in evidence.provenance_refs],
        "authority_refs": [a.as_dict() for a in evidence.authority_refs],
    }