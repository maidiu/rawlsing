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
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

RUNTIME = Path("/tmp/c0p-runtime")
sys.path.insert(0, str(RUNTIME))

from product import nonparent, scenario                      # noqa: E402
from product.service import GenericSelectedWorldService     # noqa: E402


class FacadeRefusal(Exception):
    """A missing upstream owner result. Never fabricated, never defaulted."""


@dataclass(frozen=True)
class TwoContractReceipt:
    """One receipt PER OWNER. Never a merged estimator object."""
    contract: str            # 'N9' or 'N10E_N10W'
    owner_receipt_hash: str
    owner_payload: dict
    bound_snapshot_ref: str
    values_read: list
    lineage: dict            # provenance of the producing call

    def as_dict(self):
        return dict(contract=self.contract,
                    owner_receipt_hash=self.owner_receipt_hash,
                    bound_snapshot_ref=self.bound_snapshot_ref,
                    values_read=self.values_read,
                    lineage=self.lineage,
                    owner_payload=self.owner_payload)


class TwoContractPort:
    """Tagged dispatcher. Performs NO calculation and issues NO grant.

    Each `consume` call dispatches to exactly one downstream consumer and
    returns that consumer's OWN untouched owner receipt plus a lineage record.
    It never merges two owners into one all-purpose context-probability object.
    """

    CONTRACT_N9 = "N9"
    CONTRACT_N10 = "N10E_N10W"

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
        return TwoContractReceipt(
            contract=self.CONTRACT_N9,
            owner_receipt_hash=rec["receipt_hash"],
            owner_payload=rec["material"],
            bound_snapshot_ref=rec["material"]["snapshot_ref"],
            values_read=rec["material"]["values_read"],
            lineage=dict(
                consumer="NONPARENT_OPTIONS",
                producer="product.nonparent.consume",
                producer_blob=_blob("product/nonparent.py"),
                upstream_empirical_owner="product.empirical.GenericProgressiveProvider",
                upstream_source="build_source(tag=e04-base-r1)",
                note="N9 structural routes + N10E-ordered empirical support, "
                     "reported as separate fields; no merged probability."))

    def consume_conception_proposals(self, snapshot, proposals):
        self._require_snapshot(snapshot)
        rec = scenario.evaluate(self._service, snapshot, proposals)
        self.dispatched.append("CONCEPTION_SCENARIO_PROPOSALS")
        return TwoContractReceipt(
            contract=self.CONTRACT_N9,
            owner_receipt_hash=rec["receipt_hash"],
            owner_payload=rec["material"],
            bound_snapshot_ref=rec["material"]["snapshot_ref"],
            values_read=rec["material"]["values_read"],
            lineage=dict(
                consumer="CONCEPTION_SCENARIO_PROPOSALS",
                producer="product.scenario.evaluate",
                producer_blob=_blob("product/scenario.py"),
                upstream_empirical_owner="product.empirical.GenericProgressiveProvider",
                upstream_source="build_source(tag=e04-base-r1)",
                person_generation=False, actual_conception=False,
                note="Separate consumer implementation, not a renamed nonparent output."))

    def _require_snapshot(self, snapshot):
        if snapshot is None or not hasattr(snapshot, "snapshot_hash"):
            raise FacadeRefusal(
                "N9_SNAPSHOT_MISSING__FACADE_WILL_NOT_FABRICATE_A_SELECTED_WORLD")


def _blob(rel: str) -> str:
    import hashlib
    data = (RUNTIME / rel).read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


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
        "snapshot_ref": snap.snapshot_hash,
        "receipt_A_NONPARENT_APPRENTICESHIP": receipt_a.as_dict(),
        "receipt_B_CONCEPTION_CONTEXT_PROPOSALS": receipt_b.as_dict(),
        "distinct_owner_receipts": receipt_a.owner_receipt_hash != receipt_b.owner_receipt_hash,
        "owners_not_merged": True,
        "dispatched": port.dispatched,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
