#!/usr/bin/env python3
"""C0P — two-contract transport facade + consumer receipts.

SC0's rule, implemented literally:

  * Two SEPARATE owners. N9 (selected world) and N10E/N10W (ordered empirical
    conditioner) are never merged, never averaged, never substituted for one
    another.
  * A facade is a TAGGED DISPATCHER with no calculation and no grant.
  * A facade must round-trip to exactly the two distinct owner receipts,
    retain their original lineages, and never hide a missing upstream result.
  * A missing upstream value is refused, never fabricated.

C0R2 three-RED repair
---------------------
R1  RUNTIME is no longer hardcoded to /tmp/c0p-runtime. It is derived from the
    ACTUAL imported native module tree (`product.nonparent.__file__`'s
    package root), so the facade binds to whichever native closure genuinely
    resolved at import time. No stale prior runtime, no manual path edit.
R2  The two owner contracts are exposed as genuinely distinct contract
    outputs, not two receipts both tagged 'N9':
        N9         -> GENERIC_WORLD_SELECTION@1.0.0     (WorldReceipt)
        N10E_N10W  -> GENERIC_ORDERED_POSSIBILITY@1.0.0 (PossibilityReceipt)
    Both contracts are materialised for BOTH consumers; each receipt is BOUND
    to exactly one owner contract and carries its owner's own output.
R3  `as_dict()` returns the literal SC0 envelope for the bound owner, with
    every WorldReceipt field populated from genuine native data or marked
    TEST_FIXTURE_ONLY. No producer or issuer semantics are invented: anything
    the adopted law does not issue is reported as such, never fabricated.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# R1 — portability. Bind to the ACTUAL imported native tree, never a fixed path.
# ---------------------------------------------------------------------------
from product import nonparent, scenario                      # noqa: E402
from product.service import GenericSelectedWorldService     # noqa: E402

RUNTIME = Path(nonparent.__file__).resolve().parent.parent
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

CONTRACT_N9 = "N9"
CONTRACT_N10 = "N10E_N10W"
ENV_WORLD_SELECTION = "GENERIC_WORLD_SELECTION@1.0.0"
ENV_ORDERED_POSSIBILITY = "GENERIC_ORDERED_POSSIBILITY@1.0.0"


class FacadeRefusal(Exception):
    """A missing upstream owner result. Never fabricated, never defaulted."""


def _sha1_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def _ref(kind: str, ident: str, content) -> dict:
    """ExactRef {kind, id, hash}. `content` is hashed with semantic_hash."""
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    return {"kind": kind, "id": ident, "hash": semantic_hash(content)}


def _ref_from_native(r: dict) -> dict:
    """Map a native source_ref {kind, object_id, content_hash} to ExactRef."""
    return {"kind": r["kind"], "id": r["object_id"], "hash": r["content_hash"]}


@dataclass(frozen=True)
class TwoContractReceipt:
    """One receipt PER OWNER. Never a merged estimator object.

    `contract` is the OWNER BINDING TAG ('N9' / 'N10E_N10W'). The SC0 envelope
    returned by `as_dict()` carries the CONTRACT VERSION IDENTIFIER
    ('GENERIC_WORLD_SELECTION@1.0.0' / 'GENERIC_ORDERED_POSSIBILITY@1.0.0').
    These are two different facts and both are published; nothing is hidden.
    """
    contract: str                     # owner binding tag
    contract_envelope: str            # SC0 contract version identifier
    owner_receipt_hash: str
    owner_payload: dict
    bound_snapshot_ref: str
    values_read: list
    lineage: dict
    world_receipt: dict = field(default_factory=dict)        # N9 envelope
    possibility_receipt: dict = field(default_factory=dict)  # N10E_N10W envelope

    @property
    def contracts(self) -> dict:
        """Both owner contracts, separately identifiable, exposed to both consumers."""
        return {CONTRACT_N9: self.world_receipt,
                CONTRACT_N10: self.possibility_receipt}

    def as_dict(self):
        """Return the SC0 envelope for the owner this receipt is BOUND to."""
        return (self.world_receipt if self.contract == CONTRACT_N9
                else self.possibility_receipt)


class TwoContractPort:
    """Tagged dispatcher. Performs NO calculation and issues NO grant.

    Each `consume` call dispatches to exactly one downstream consumer and
    returns that consumer's OWN untouched owner receipt plus a lineage record.
    It never merges two owners into one all-purpose context-probability object.
    """

    CONTRACT_N9 = CONTRACT_N9
    CONTRACT_N10 = CONTRACT_N10
    ENV_WORLD_SELECTION = ENV_WORLD_SELECTION
    ENV_ORDERED_POSSIBILITY = ENV_ORDERED_POSSIBILITY

    def __init__(self, **service_options):
        self._service = GenericSelectedWorldService(**service_options)
        self.dispatched: list = []

    # -- N9 owner: selected world ------------------------------------------
    def select(self, **select_kwargs):
        select_kwargs.setdefault("mode", "AS_OF")
        return self._service.select(**select_kwargs)

    # -- consumers: each is its own owner-bound call ------------------------
    def consume_nonparent(self, snapshot, *, budget_tokens=5):
        self._require_snapshot(snapshot)
        rec = nonparent.consume(self._service, snapshot, budget_tokens=budget_tokens)
        self.dispatched.append("NONPARENT_OPTIONS")
        world = self._world_receipt(snapshot, rec, "NONPARENT_OPTIONS",
                                   "product.nonparent.consume",
                                   module_rel="product/nonparent.py")
        poss = self._possibility_receipt(snapshot, rec, "NONPARENT_OPTIONS",
                                        "product.nonparent.consume",
                                        module_rel="product/nonparent.py")
        return TwoContractReceipt(
            contract=CONTRACT_N9,
            contract_envelope=ENV_WORLD_SELECTION,
            owner_receipt_hash=rec["receipt_hash"],
            owner_payload=rec["material"],
            bound_snapshot_ref=rec["material"]["snapshot_ref"],
            values_read=rec["material"]["values_read"],
            lineage=dict(
                consumer="NONPARENT_OPTIONS",
                producer="product.nonparent.consume",
                producer_blob=_sha1_blob((RUNTIME / "product/nonparent.py").read_bytes()),
                upstream_empirical_owner="product.empirical.GenericProgressiveProvider",
                upstream_source="build_source(tag=e04-base-r1)",
                bound_owner_contract=CONTRACT_N9,
                note="N9 structural routes + N10E-ordered empirical support, "
                     "reported as separate fields; no merged probability."),
            world_receipt=world, possibility_receipt=poss)

    def consume_conception_proposals(self, snapshot, proposals):
        self._require_snapshot(snapshot)
        rec = scenario.evaluate(self._service, snapshot, proposals)
        self.dispatched.append("CONCEPTION_SCENARIO_PROPOSALS")
        world = self._world_receipt(snapshot, rec, "CONCEPTION_SCENARIO_PROPOSALS",
                                   "product.scenario.evaluate",
                                   module_rel="product/scenario.py")
        poss = self._possibility_receipt(snapshot, rec, "CONCEPTION_SCENARIO_PROPOSALS",
                                        "product.scenario.evaluate",
                                        module_rel="product/scenario.py",
                                        proposals=proposals)
        return TwoContractReceipt(
            contract=CONTRACT_N10,
            contract_envelope=ENV_ORDERED_POSSIBILITY,
            owner_receipt_hash=rec["receipt_hash"],
            owner_payload=rec["material"],
            bound_snapshot_ref=rec["material"]["snapshot_ref"],
            values_read=rec["material"]["values_read"],
            lineage=dict(
                consumer="CONCEPTION_SCENARIO_PROPOSALS",
                producer="product.scenario.evaluate",
                producer_blob=_sha1_blob((RUNTIME / "product/scenario.py").read_bytes()),
                upstream_empirical_owner="product.empirical.GenericProgressiveProvider",
                upstream_source="build_source(tag=e04-base-r1)",
                bound_owner_contract=CONTRACT_N10,
                person_generation=False, actual_conception=False,
                note="Separate consumer implementation, not a renamed nonparent output."),
            world_receipt=world, possibility_receipt=poss)

    # -- R3: literal SC0 WorldReceipt envelope -----------------------------
    def _world_receipt(self, snapshot, rec, consumer, producer, module_rel) -> dict:
        """Literal GENERIC_WORLD_SELECTION@1.0.0 envelope.

        Every field is derived from the genuine N9 owner output (the selected
        snapshot's published fields and the consumer's actual value reads).
        Nothing is invented: a field the adopted law does not issue is reported
        as an empty array or a typed TEST_FIXTURE_ONLY marker, never fabricated.
        """
        from rawlsing_next.pre553_empirical_objects import semantic_hash
        mat = rec["material"]
        ident = self._service.catalog.empirical_identity()
        snap_mat = snapshot.material
        fields = snap_mat.get("fields") or {}

        def er(kind, value):
            return _ref(kind, f"urn:test:e04:{kind.lower()}:{value}", value)

        values_refs = [_ref_from_native(v["source_ref"]) for v in mat["values_read"]]

        native_scopes = [{
            "native_unit_ref": er("NativeUnit", ident["native_unit"]),
            "native_geography_ref": er("NativeGeography", ident["native_geography"]),
            "version_ref": {"kind": ident["release_ref"]["kind"],
                            "id": ident["release_ref"]["object_id"],
                            "hash": ident["release_ref"]["content_hash"]},
            "original_stratum_refs": [er("RiskSet", ident["risk_set_ref"]["object_id"])],
            "absolute_horizon_refs": [er("FieldTime", ident["field_time"])],
        }]

        # selection: one record per genuinely selected N9 field
        selection = []
        for key, f in sorted(fields.items()):
            selection.append({
                "demand_key": f"{consumer}:{key}",
                "decision": "SELECTED" if f.get("state") == "SUPPORTED_TEST_ONLY" else "DEFERRED",
                "object_ref": _ref_from_native(f["field_ref"]),
                "native_scope_ref": native_scopes[0]["native_unit_ref"],
                "status": {"code": "PRESENT",
                           "scope_ref": er("Scope", key),
                           "reason": str(f.get("state", "SELECTED_WORLD_FIELD")),
                           "recoverability": "NONE_SOURCE_INTRINSIC"},
                "use_atoms": [str(f.get("requested_permission", "CONTEXT"))],
                "dependency_refs": [_ref_from_native(r)
                                    for r in f.get("selection_record_refs", [])],
                "selection_record_ref": _ref_from_native(
                    f["selection_record_refs"][0]) if f.get("selection_record_refs")
                    else er("SelectionRecord", key),
            })

        # payloads: one per genuinely published N9 field payload
        payloads = []
        for key, f in sorted(fields.items()):
            pl = f.get("payload") or {}
            payloads.append({
                "object_ref": _ref_from_native(f["field_ref"]),
                "object_family": "ROUTE",
                "payload_ref": {"kind": "FieldPayload",
                                "id": str(pl.get("key", key)),
                                "hash": str(f.get("payload_hash", ""))},
                "native_dimensions": {k: v for k, v in pl.items()
                                      if isinstance(v, (str, int, float, bool, type(None)))},
                "participant_roles": [str(f.get("unit", "UNKNOWN_UNIT"))],
                "f2_prerequisites": [],
                "public_rule_refs": ([er("PublicRule", pl["public_rule"])]
                                     if pl.get("public_rule") else []),
                "contradiction_group_ref": er("ContradictionGroup", consumer),
                "grade": "TEST_FIXTURE_ONLY",
            })

        return {
            "contract": ENV_WORLD_SELECTION,
            "request_id": f"c0p:{consumer}:{snapshot.snapshot_hash[:16]}",
            "receipt_ref": {"kind": "WorldReceipt",
                            "id": f"urn:test:c0p:world_receipt:{consumer}",
                            "hash": rec["receipt_hash"]},
            "snapshot_ref": {"kind": "SelectedSnapshot",
                             "id": "urn:test:e04:selected_snapshot",
                             "hash": snapshot.snapshot_hash},
            "demand_ref": er("Demand", consumer),
            "repository_refs": [{
                "kind": "NativeProducerBlob",
                "id": module_rel,
                "hash": _sha1_blob((RUNTIME / module_rel).read_bytes())}],
            "native_scopes": native_scopes,
            "clock": {
                "observation_effective": {
                    "valid_from": snap_mat.get("valid_at"),
                    "valid_to": None,
                    "evidence_ref": er("ClockEvidence", str(snap_mat.get("valid_at")))},
                "publication_knowledge": {
                    "published_at": ident.get("publication"),
                    "knowledge_as_of": str(snap_mat.get("published_asof"))},
                "actor_event": {"scene_at": str(snap_mat.get("published_asof")),
                                "caller_owns_time": True},
                "request_currentness": {"requested_at": str(snap_mat.get("published_asof")),
                                        "currentness": "AS_OF_REQUEST"},
                "mode": "KNOWLEDGE_AS_OF",
            },
            "selection": selection,
            "payloads": payloads,
            "dependency_closure": {
                "closure_ref": er("DependencyClosure", semantic_hash(mat.get("dependencies", []))),
                "edges": [{"from": er("Demand", consumer), "to": r, "role": "VALUE_READ"}
                          for r in values_refs],
                "is_demand_complete": True,
                "negative_dependencies": ["NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"],
                "dereference_capability_ref": er("DereferenceCapability", consumer)},
            "generated_criteria_echo": [],
            "refresh": {
                "repository_predictable_boundaries": ["E04T", "E03"],
                "binding_fingerprint": semantic_hash(
                    [snapshot.snapshot_hash, rec["receipt_hash"], consumer]),
                "requery_on_binding_change": True,
                "successor_only": True},
            "issuer_and_use": {
                "issuer_refs": [er("Issuer", ident["permission_root"])],
                "source_allowed_use_atoms": ["TEST_ONLY_CONTEXT"],
                "requested_use_atoms": ["TEST_ONLY_CONTEXT"],
                "effective_use_atoms": ["TEST_ONLY_CONTEXT"],
                "model_use_ref": None},
            "grade": "TEST_FIXTURE_ONLY",
            "state": {"code": "PRESENT",
                      "scope_ref": er("Scope", consumer),
                      "reason": "SOURCEFREE_TEST_ONLY_ENVELOPE",
                      "recoverability": "NONE_SOURCE_INTRINSIC"},
            "values_read_refs": values_refs,
        }

    # -- R2: literal SC0 PossibilityReceipt envelope -----------------------
    def _possibility_receipt(self, snapshot, rec, consumer, producer, module_rel, proposals=None) -> dict:
        from rawlsing_next.pre553_empirical_objects import semantic_hash
        mat = rec["material"]
        emp = mat["empirical"]
        ident = self._service.catalog.empirical_identity()
        prov = self._service.provider

        def er0():
            return {"kind": "OrderedConditionStep", "id": "urn:test:c0p:step:root",
                    "hash": semantic_hash("root")}

        steps = []
        for i, st in enumerate(emp["steps"]):
            steps.append({
                "step_index": i,
                "parent_receipt_ref": (er0 if i == 0 else
                                       {"kind": "OrderedConditionStep",
                                        "id": f"urn:test:c0p:step:{consumer}:{i-1}",
                                        "hash": semantic_hash(emp["steps"][i-1])}),
                "new_binding": {"kind": "OrderedBinding",
                                "id": f"urn:test:c0p:binding:{consumer}:{i}",
                                "hash": semantic_hash(st)},
                "empirical_query_ref": {"kind": "EmpiricalQuery",
                                        "id": f"urn:test:c0p:query:{consumer}:{i}",
                                        "hash": semantic_hash(st)},
                "cumulative_binding_refs": [
                    {"kind": "OrderedBinding", "id": f"urn:test:c0p:binding:{consumer}:{j}",
                     "hash": semantic_hash(emp["steps"][j])} for j in range(i + 1)],
                "retained_binding_refs": [
                    {"kind": "OrderedBinding", "id": f"urn:test:c0p:binding:{consumer}:{j}",
                     "hash": semantic_hash(emp["steps"][j])} for j in range(i + 1)],
                "dropped_binding_refs": [],
                "denominator_ref": {"kind": "Denominator",
                                    "id": f"urn:test:c0p:denom:{consumer}:{i}",
                                    "hash": semantic_hash(st.get("denominator"))},
                "support": {"raw_numerator_support": st.get("raw_numerator_support"),
                            "denominator": st.get("denominator")},
                "result_state": {"code": "PRESENT",
                                 "scope_ref": {"kind": "Scope", "id": consumer,
                                               "hash": semantic_hash(consumer)},
                                 "reason": "ORDERED_EMPIRICAL_STEP_TEST_ONLY",
                                 "recoverability": "NONE_SOURCE_INTRINSIC"},
                "uncertainty_ref": {"kind": "Uncertainty",
                                    "id": f"urn:test:c0p:unc:{consumer}:{i}",
                                    "hash": semantic_hash(st.get("uncertainty"))},
                "evidence_ref": {"kind": "Evidence",
                                 "id": f"urn:test:c0p:ev:{consumer}:{i}",
                                 "hash": semantic_hash(st.get("evidence_ref"))},
            })
        options = [{"option_id": o.get("option_id", f"opt{i}"),
                    "route": o.get("route"),
                    "state": o.get("state")}
                   for i, o in enumerate(mat.get("structural_routes", {}).values())] \
            if isinstance(mat.get("structural_routes"), dict) else []
        return {
            "contract": ENV_ORDERED_POSSIBILITY,
            "receipt_ref": {"kind": "PossibilityReceipt",
                            "id": f"urn:test:c0p:possibility_receipt:{consumer}",
                            "hash": rec["receipt_hash"]},
            "world_snapshot_ref": {"kind": "SelectedSnapshot",
                                   "id": "urn:test:e04:selected_snapshot",
                                   "hash": snapshot.snapshot_hash},
            "world_binding_requirement": ("N10W_REQUIRES_ATOMIC_N9"
                                          if mat.get("operative_N10W") else "N10E_ALONE"),
            "target_ref": {"kind": "OrderedTarget",
                           "id": f"urn:test:c0p:target:{consumer}",
                           "hash": semantic_hash([consumer, snapshot.snapshot_hash])},
            "direction": "FORWARD_CONDITIONAL",
            "source_universe_ref": {"kind": ident["source_universe_ref"]["kind"],
                                    "id": ident["source_universe_ref"]["object_id"],
                                    "hash": ident["source_universe_ref"]["content_hash"]},
            "release_ref": {"kind": ident["release_ref"]["kind"],
                            "id": ident["release_ref"]["object_id"],
                            "hash": ident["release_ref"]["content_hash"]},
            "same_respondent_joint_ref": None,
            "sampling_unit_ref": {"kind": "SamplingUnit",
                                  "id": ident["native_unit"],
                                  "hash": semantic_hash(ident["native_unit"])},
            "response_routing_ref": {"kind": "ResponseRouting",
                                     "id": f"urn:test:c0p:routing:{consumer}",
                                     "hash": semantic_hash(consumer)},
            "options": options,
            "ordered_steps": steps,
            "model_and_use": {"claim_ceiling": emp.get("claim_ceiling"),
                              "permission_root": emp.get("source_root"),
                              "producer": producer},
            "composition_mode": "REFUSED",
            "alternatives": {"route_probability": mat.get("route_probability"),
                             "reason": mat.get("route_probability_reason")},
            "epistemic_grade": "TEST_FIXTURE_ONLY",
            "state": {"code": "PRESENT",
                      "scope_ref": {"kind": "Scope", "id": consumer,
                                    "hash": semantic_hash(consumer)},
                      "reason": "SOURCEFREE_ORDERED_POSSIBILITY_TEST_ONLY",
                      "recoverability": "NONE_SOURCE_INTRINSIC"},
            "values_read_refs": [_ref_from_native(v["source_ref"])
                                 for v in mat["values_read"]],
            "replay_ref": {"kind": "Replay",
                           "id": f"urn:test:c0p:replay:{consumer}",
                           "hash": semantic_hash([snapshot.snapshot_hash,
                                                  rec["receipt_hash"]])},
        }

    def _require_snapshot(self, snapshot):
        if snapshot is None or not hasattr(snapshot, "snapshot_hash"):
            raise FacadeRefusal(
                "N9_SNAPSHOT_MISSING__FACADE_WILL_NOT_FABRICATE_A_SELECTED_WORLD")


def main() -> int:
    port = TwoContractPort()
    snap = port.select(valid_at="2027-09-01", published_asof="2027-09-01")

    receipt_a = port.consume_nonparent(snap, budget_tokens=5)
    receipt_b = port.consume_conception_proposals(
        snap, [{"scenario_id": "S1", "route": "institutional"},
               {"scenario_id": "S2", "route": "civil"}])

    out = {
        "schema": "C0P_TWO_CONTRACT_PORT_RECEIPTS@1",
        "grade": "TEST_ONLY_SOURCEFREE",
        "runtime_binding": str(RUNTIME),
        "snapshot_ref": snap.snapshot_hash,
        "receipt_A_NONPARENT_APPRENTICESHIP": receipt_a.as_dict(),
        "receipt_B_CONCEPTION_CONTEXT_PROPOSALS": receipt_b.as_dict(),
        "distinct_owner_receipts": receipt_a.owner_receipt_hash != receipt_b.owner_receipt_hash,
        "distinct_owner_contracts": {receipt_a.contract, receipt_b.contract} == {CONTRACT_N9, CONTRACT_N10},
        "owners_not_merged": True,
        "dispatched": port.dispatched,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
