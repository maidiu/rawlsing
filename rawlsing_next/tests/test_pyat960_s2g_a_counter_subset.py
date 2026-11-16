"""A counterexample: M1 receipt fact must be in the retained M1 evidence chain.

B's repaired M1-to-S2F binding checked that M1 receipt/query/predicate refs were
members of the declared closure, but not that each retained discovery receipt's
owned empirical/validation facts were present in the disposition and bundle.
Removing one receipt fact from the bundle/disposition while retaining the
receipt ref was accepted by B's code and the actual world consumer still
returned exact supported.  This test freezes the repair.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_durable_learned_lifecycle import (
    DurableLearnedLifecycleError,
    open_learned_lifecycle,
    publish_learned_lifecycle,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
from rawlsing_next.pre553_learned_product_release import M2Repository
from rawlsing_next.tests.test_pyat960_s2g_durable_lifecycle import _artifact_case


def _row_ref(document) -> ExactRef:
    return ExactRef(
        f"{document['schema_id']}@{document['schema_version']}",
        document["object_id"],
        document["content_hash"],
    )


def _mutant_receipt_omission(tmp_path: Path):
    base = _artifact_case(tmp_path / "base")
    disposition = base["disposition"]
    determinant = disposition.determinant_explanation_receipt
    receipt = base["receipt"]
    victim = exact_ref(dict(receipt.empirical_fact_refs[0]))
    assert victim in set(disposition.empirical_fact_refs)

    bundle_doc = base["m1_bundle"].as_dict()
    fields = dict(bundle_doc["semantic_fields"])
    fields["empirical_facts"] = [
        row for row in fields["empirical_facts"] if _row_ref(row) != victim
    ]
    bundle_doc["semantic_fields"] = fields
    projection = {
        "schema_id": bundle_doc["schema_id"],
        "schema_version": bundle_doc["schema_version"],
        "semantic_fields": fields,
    }
    digest = semantic_hash(projection)
    bundle_doc["content_hash"] = digest
    bundle_doc["object_id"] = (
        "urn:rawlsing:pre553:m1:M1AdjudicationInputBundle:sha256:" + digest
    )
    new_bundle_ref = ExactRef("M1AdjudicationInputBundle@1.0.0", bundle_doc["object_id"], digest)
    new_determinant = dataclasses.replace(determinant, input_bundle_ref=new_bundle_ref)
    new_disposition = dataclasses.replace(
        disposition,
        empirical_fact_refs=tuple(
            ref for ref in disposition.empirical_fact_refs if ref != victim
        ),
        determinant_explanation_receipt_ref=new_determinant.ref,
        determinant_explanation_receipt=new_determinant,
    )
    executor = LearnedProductLifecycleExecutor()
    learned = i4.compose_learned_world(
        base["contract"],
        m2_repository=M2Repository(),
        lifecycle_executor=executor,
        m1_disposition=new_disposition,
    )
    assert learned.receipt.terminal_state == "RULE_SATISFIED"
    published = publish_learned_lifecycle(
        tmp_path / "mutant",
        learned=learned,
        executor=executor,
        determinants=base["determinants"],
        m1_input_bundle=bundle_doc,
        m1_family_rule_binding=base["binding"].as_dict(),
    )
    artifact = open_learned_lifecycle(
        published.artifact_path, expected_root=published.root_identity
    ).require_trusted()
    return base, artifact


def test_a_counter_receipt_fact_omission_is_refused(tmp_path):
    base, mutant = _mutant_receipt_omission(tmp_path)
    # The mutant is internally valid and opens under its own external pin; the
    # first consumer must still refuse because the M1 chain omitted a fact that
    # its retained receipt owns.
    with pytest.raises(DurableLearnedLifecycleError, match="receipt"):
        mutant.consume(base["s2f_receipt"].root_path)
    # The unmodified base artifact remains exact.
    restored = base["artifact"].consume(base["s2f_receipt"].root_path)
    assert restored.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert restored.consumer_result_hash == (
        base["composition"].consumer_result_or_null.result_hash
    )
