"""R17 GF1 — real native source-free chain driver.

Physically executes the ACCEPTED original machinery and then a NEW NAMESPACED
TEST_ONLY generic PAIR relation owner + a named downstream consumer.

  1. real C11 source validation / repository ingestion   (accepted native)
  2. real I03 empirical query                           (accepted native)
  3. real I05 bounded discovery selection               (accepted native)
  4. real P01 durable batch + UnitExecutionReceipt      (accepted native)
  5. ACCEPTED specialized Field Forge GT2 Q86B/Q86A relation  (independent comparator,
     used UNMODIFIED as the comparison object)
  6. NEW NAMESPACED generic PAIR relation owner         (GF1 TEST_ONLY candidate)
  7. NEW NAMESPACED named consumer reading that relation object (GF1 TEST_ONLY)

Nothing here edits, renames, xfails, skips or relabels the specialized GT2 owner,
its risk, its consumer outputs, or the original raw failing assertion.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gf1_bootstrap as GB                       # noqa: E402  (reattests 74 blobs on import)
import pv2_sourcefree_fixture as PV2F            # noqa: E402
import pv3_candidate as PV3                      # noqa: E402
from fixture_owner import FixtureOwnerControl    # noqa: E402
from rawlsing_next._pre553_query_common import ExactRef, semantic_hash  # noqa: E402
from rawlsing_next.field_forge_conditional_support import (             # noqa: E402
    produce_exact_conditional_support_profile as ACCEPTED_PRODUCE,
    replay_exact_conditional_support_profile as ACCEPTED_REPLAY,
    ExactConditionalSupportProfile as ACCEPTED_PROFILE,
)

from generic_native_pair_relation import (            # noqa: E402  (NEW, GF1 candidate)
    GENERIC_RELATION_OWNER,
    GENERIC_CONSUMER_ID,
    produce_generic_native_pair_relation,
    replay_generic_native_pair_relation,
    GenericNativePairRelation,
)
from gf1_pair_support_consumer import compute_pair_support_signature  # noqa: E402


def profile_of(material: dict) -> dict:
    """Condenser |condition -> |target: joint support| — PV3N's exact native shape."""
    return {
        str(x["condition_state"]): {
            "denominator": x["condition_denominator_support"],
            "targets": {str(t["target_state"]): t["joint_support_count"] for t in x["target_counts"]},
        }
        for x in material["conditional_count_profile"]
    }


def prepare(profile="BASELINE", policy=None, root=None):
    """Real owner installation + real frozen source-free fixture."""
    owner = FixtureOwnerControl(profile, policy_path=policy, provision=False)
    api = PV3.RequestAPI(owner.client(), owner._attest)
    installation = dict(
        pid=__import__("os").getpid(),
        expected_root=owner.installation.expected_root,
        register_root=owner.installation.register_root,
        complete_expected=json.loads(owner.installation.expected_json),
        profile=profile,
        source_editions=[dict(ns=ns, edition=ed) for ns, ed in owner.installation.source_editions],
    )
    root = Path(root) if root else GB.RT / "gf1_run"
    if profile == "BASELINE":
        fx = PV2F.pv2_sourcefree_fixture(root)
    else:
        # Genuine physical intervention: create REAL altered cells before owner validation.
        row, value = (2, "1") if profile == "R2_Y1" else (1, "0")
        fx = __import__("common", fromlist=["make_numeric_fixture"]).make_numeric_fixture(
            root, row=row, new_value=value)
    assert fx["expected"].payload_json == owner.installation.expected_json, \
        "ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT"
    return owner, api, fx, installation


def run_native(profile="BASELINE", policy=None, root=None):
    """Physically run the whole accepted chain and return a full receipt bundle."""
    owner, api, fx, installation = prepare(profile=profile, policy=policy, root=root)
    report = api.run_sourcefree_with_register(
        expected=fx["expected"], selected_scopes=fx["plans"],
        register=fx["register"], scope_metadata=tuple(fx["meta"]))
    return dict(profile=profile, installation=installation, report=report,
                plans=fx["plans"], owner=owner, api=api)


def collect_link_material(bundle):
    """Pull each real consumer's producer fact/query out of the live P01 catalog."""
    out = []
    proofs = []
    for s in bundle["plans"]:
        proof = PV3.reconcile_journal(s.p01_kwargs["session"])
        proofs.append(proof)
        receipts = {p["unit_key"]: p["receipt_projection"] for p in proof}
        for link in bundle["report"]["links"]:
            if link["original_expected_work_key"] not in s.original_work_keys:
                continue
            m = link["consumer_material"]
            unit_key = ExactRef(**link["batch_unit_ref"]).key
            receipt = receipts[unit_key]
            if link["owner_job_ref"]["kind"].startswith("EmpiricalQuerySpec"):
                fact = s.p01_kwargs["resolve_fact"](ExactRef(**link["producer_result_ref"]))
                query = s.p01_kwargs["runtime_catalog"].resolve_query_exact(
                    ExactRef(**m["producer_query_ref"]))
                kind = "QUERY"
            else:
                outcome = s.p01_kwargs["resolve_discovery"](
                    ExactRef(**receipt["result_refs"][0]))
                facts = [f for f in outcome.empirical_facts
                         if f.ref.as_dict() == link["producer_result_ref"]]
                assert len(facts) == 1
                fact = facts[0]
                query = next(q for q in outcome.executed_queries
                             if q.ref.as_dict() == m["producer_query_ref"])
                kind = "DISCOVERY"
            out.append(dict(work_key=link["original_expected_work_key"],
                            owner_job_ref=link["owner_job_ref"], kind=kind,
                            fact=fact, query=query, material=m, unit_key=unit_key))
    return out, proofs