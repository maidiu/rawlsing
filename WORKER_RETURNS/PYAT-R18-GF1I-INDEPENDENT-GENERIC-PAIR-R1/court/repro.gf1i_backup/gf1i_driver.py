"""GF1I — independent reviewer driver.

Deliberately does NOT import ``gf1_native`` (which imports the absent
``gf1_pair_support_consumer``). It re-uses the SAME accepted owner chain
(accepted C11/I03/I05/P01), the SAME frozen sourcefree fixture and the SAME
installed TEST_ONLY owner, and drives the candidate relation module directly.

Every falsifier in this file was authored by the independent reviewer and
frozen in 01_FROZEN_GENERIC_PAIR_AND_ROLE_ORACLE.json before execution.
"""
from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path

C = Path(__file__).resolve().parent            # .../GF1I-...-R1/court
RT = C / "runtime_root"
sys.path[:0] = [str(C / "repro"), str(RT), str(RT / "candidate/repro"), str(C / "frozen_pv2i/repro")]

import gf1_bootstrap as GB                                   # noqa: E402  (reattests 74 on import)
import pv2_sourcefree_fixture as PV2F                        # noqa: E402
import pv3_candidate as PV3                                  # noqa: E402
from fixture_owner import FixtureOwnerControl                # noqa: E402
from rawlsing_next._pre553_query_common import ExactRef      # noqa: E402
from rawlsing_next.field_forge_conditional_support import (  # noqa: E402
    produce_exact_conditional_support_profile as ACCEPTED_PRODUCE,
    replay_exact_conditional_support_profile as ACCEPTED_REPLAY,
)
from generic_native_pair_relation import (                   # noqa: E402
    GENERIC_RELATION_OWNER,
    GENERIC_CONSUMER_ID,
    produce_generic_native_pair_relation,
    replay_generic_native_pair_relation,
    GenericNativePairError,
    GenericPermissionWideningError,
)


def _profile_of(material):
    """condenser |condition -> |target: joint support| (PV3N exact native shape)."""
    return {
        str(x["condition_state"]): {
            "denominator": x["condition_denominator_support"],
            "targets": {str(t["target_state"]): t["joint_support_count"]
                        for t in x["target_counts"]},
        }
        for x in material["conditional_count_profile"]
    }


def prepare(profile="BASELINE", root=None):
    owner = FixtureOwnerControl(profile, provision=False)
    api = PV3.RequestAPI(owner.client(), owner._attest)
    installation = dict(
        pid=__import__("os").getpid(),
        expected_root=owner.installation.expected_root,
        register_root=owner.installation.register_root,
        complete_expected=json.loads(owner.installation.expected_json),
        profile=profile,
        source_editions=[dict(ns=ns, edition=ed) for ns, ed in owner.installation.source_editions],
    )
    root = Path(root) if root else RT / f"gf1i_run_{profile}"
    if profile == "BASELINE":
        fx = PV2F.pv2_sourcefree_fixture(root)
    else:
        row, value = (2, "1") if profile == "R2_Y1" else (1, "0")
        fx = __import__("common", fromlist=["make_numeric_fixture"]).make_numeric_fixture(
            root, row=row, new_value=value)
    assert fx["expected"].payload_json == owner.installation.expected_json, \
        "ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT"
    return owner, api, fx, installation


def run_native(profile="BASELINE", root=None):
    owner, api, fx, installation = prepare(profile=profile, root=root)
    report = api.run_sourcefree_with_register(
        expected=fx["expected"], selected_scopes=fx["plans"],
        register=fx["register"], scope_metadata=tuple(fx["meta"]))
    return dict(profile=profile, installation=installation, report=report,
                plans=fx["plans"], owner=owner, api=api)


def collect_link_material(bundle):
    """Pull each real consumer's producer fact/query from the live P01 catalog."""
    out, proofs = [], []
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


def produce_all(bundle):
    """Produce a generic relation for every live consumer link."""
    links, _ = collect_link_material(bundle)
    relations = []
    for link in links:
        material = link["material"]
        roles = material["roles"]
        rel = produce_generic_native_pair_relation(
            joint_fact=link["fact"], joint_query=link["query"],
            conditioner_ref=ExactRef(**roles["CONDITIONER"]["ref"]),
            target_ref=ExactRef(**roles["TARGET"]["ref"]),
            producer_permission_ceiling=tuple(material["producer_permission_ceiling"]),
            relation_permission_ceiling=tuple(material["relation_permission_ceiling"]),
        )
        relations.append(dict(link=link, relation=rel))
    return relations