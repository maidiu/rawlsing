"""N10E fresh-process replay runner.

Builds the frozen AT07 fixture law from scratch in a fresh interpreter, runs the
public provider, and prints the provider receipt / result / composition / evidence
identities as JSON. Nothing is shared with the in-process court except the frozen
fixture module and the committed implementation.
"""
from __future__ import annotations

import json
import sys

from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.tests import n10e_empirical_slice_fixture as fx


def main(argv: list[str]) -> int:
    direction = argv[1] if len(argv) > 1 else "forward"
    case = fx.build_provider_case(direction)
    result = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    evidence = result.generated_evidence_or_null
    consumer = result.consumer_result_or_null
    payload = {
        "direction": direction,
        "provider_state": result.provider_state,
        "receipt_ref_hash": result.receipt_ref.content_hash,
        "receipt_ref_object_id": result.receipt_ref.object_id,
        "result_identity_hash": result.result_identity_hash,
        "evidence_ref_hash": None if evidence is None else evidence.evidence_ref.content_hash,
        "consumer_result_hash": None if consumer is None else consumer.result_hash,
        "consumer_result_state": None if consumer is None else consumer.result_state,
        "composed_result_identity_hash": (
            result.composition_result.composed_result_identity_hash
        ),
        "producer_fact_ref_hash": result.composition_result.producer_fact_ref.content_hash,
        "raw_denominator_support": result.composition_result.raw_denominator_support,
        "cell_numerators": (
            None
            if evidence is None
            else {
                cell["cell"]: cell["raw_numerator_support"]
                for cell in evidence.geometry["cells"]
            }
        ),
    }
    sys.stdout.write(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
