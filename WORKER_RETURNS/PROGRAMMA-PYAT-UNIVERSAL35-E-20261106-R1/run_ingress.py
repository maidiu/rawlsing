#!/usr/bin/env python3
"""Cold-use interface for the existing FIELD FORGE empirical ingress owner."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent
REPO = RETURN.parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
INTERFACE = RETURN / "INTERFACE.json"


def _json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def _summary(out) -> dict:
    relation = out.relation
    return {
        "test_only_sourcefree": True,
        "state": out.state,
        "fact_ref": out.fact_ref.as_dict(),
        "query_ref": out.query_ref.as_dict(),
        "relation_ref": None if relation is None else relation.ref.as_dict(),
        "relation_typed_state": None if relation is None else relation.typed_state,
        "condition_denominators": (
            None if relation is None
            else [row["condition_denominator_support"] for row in relation.conditional_count_profile]
        ),
        "bridge_state": out.bridge_state,
        "bridge_refusal": out.bridge_refusal,
        "refusal_code": out.refusal_code,
        "refusal_detail": out.refusal_detail,
        "structural_grant": out.structural_grant,
        "structural_state": out.structural_state,
    }


def _gt2_case():
    from rawlsing_next.pre553_field_forge_empirical_ingress import ingest_empirical_fact
    from rawlsing_next.tests.test_field_forge_conditional_support import _fixture

    query, fact, conditioner, target = _fixture()
    return _summary(ingest_empirical_fact(
        fact=fact, query=query, conditioner_ref=conditioner, target_ref=target,
    ))


def _n10e_case():
    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )
    from rawlsing_next.pre553_field_forge_empirical_ingress import ingest_empirical_fact
    from rawlsing_next.tests import c1_03_join_fixture as jf
    from rawlsing_next.tests.c1_at08_at13_fixture import make_model_rule

    built = jf.a_forward_composition()
    provider = provide_empirical_possibility_slice(
        repository=built["source"]["repo"],
        empirical_query=built["query"],
        predicate=built["predicate"],
        authority_registry=built["registry"],
        release_refs=(built["source"]["release_ref"],),
        consumer_query=built["consumer_query"],
        model_rule=make_model_rule(built["source"]["universe"].ref, "ingress-cold-use"),
        condition_binding_witness=built["witness"],
    )
    fact = provider.composition_result.producer_result.facts[0]
    out = ingest_empirical_fact(fact=fact, query=built["query"])
    result = _summary(out)
    result["n10e_provider_state"] = provider.provider_state
    result["n10e_producer_route"] = provider.composition_result.producer_route
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="sorok-field-forge-empirical-ingress")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("abi", help="print the frozen ingress ABI")
    selftest = sub.add_parser("selftest", help="run sourcefree current-owner cases")
    selftest.add_argument("--case", choices=("all", "gt2", "n10e"), default="all")
    args = parser.parse_args(argv)
    if args.command == "abi":
        print(INTERFACE.read_text())
        return 0
    cases = {}
    if args.case in {"all", "gt2"}:
        cases["gt2_two_target_existing_ff_profile"] = _gt2_case()
    if args.case in {"all", "n10e"}:
        cases["n10e_current_i03_one_target_ff_refusal"] = _n10e_case()
    print(_json({"schema": "SOROK_FF_INGRESS_SELFTEST@1", "cases": cases}))
    return 0 if all(case["state"] for case in cases.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
