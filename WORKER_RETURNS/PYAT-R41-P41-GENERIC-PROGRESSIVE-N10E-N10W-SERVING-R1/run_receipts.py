"""Generate the P41 receipt artifacts (deterministic, TEST_ONLY, no wall clock)."""
import json
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKET / "runtime"))
import bootstrap  # noqa: E402

bootstrap.install()
from fixture import prepare, ref  # noqa: E402
from p41_service import PROVIDER_VERSIONS, P41Service  # noqa: E402


def cells_of(material):
    return [{cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]}
            for step in material["empirical"]["steps"]]


def main():
    out = PACKET

    base = P41Service()
    base_receipt = base.progressive()
    reverse = base.progressive(target="A", conditions=(("Y", 1),))
    changed = P41Service(prepare(same_marginals=True)).progressive()
    support_loss = P41Service(prepare(support_loss=True)).progressive()
    measured_null = P41Service(prepare(measured_null=True)).progressive()

    revision_service = P41Service()
    revision_service.publish_rule_revision(
        "training_fee", 6, effective_from="2027-01-01", effective_to="2028-01-01",
        publication="2027-06-01", revision=2)
    revision_service.publish_rule_revision(
        "exit_cost", 8, effective_from="2027-01-01", effective_to="2028-01-01",
        publication="2027-06-01", revision=2)
    revised = revision_service.progressive(
        snapshot=revision_service.current_clock_snapshot("2027-09-01", "2027-09-01"))
    early = revision_service.progressive(
        snapshot=revision_service.current_clock_snapshot("2026-06-01", "2026-04-15"))

    conditioning = dict(
        schema="PYAT_R41_P41_COMPUTED_PROGRESSIVE_CONDITIONING_RECEIPTS@1",
        providers=dict(PROVIDER_VERSIONS),
        base_progressive=_summarize(base_receipt),
        reverse_role=_summarize(reverse),
        learned_same_marginals=_summarize(changed),
        structural_rule_revision_fixed_empirical=dict(
            revised=_summarize(revised), early_clock=_summarize(early)),
        support_loss=_summarize(support_loss),
        measured_null=_summarize(measured_null))
    (out / "computed_progressive_conditioning_receipts.json").write_text(
        json.dumps(conditioning, indent=2, sort_keys=True) + "\n")

    consumer_base = base.consumer_read()
    consumer_changed = P41Service(prepare(same_marginals=True)).consumer_read()
    values_read = dict(
        schema="PYAT_R41_P41_GENERIC_CONSUMER_VALUES_READ@1",
        consumer="NONPARENT_OPTIONS",
        base=dict(receipt_hash=consumer_base["receipt_hash"],
                  state=consumer_base["material"]["state"],
                  steps_cells=cells_of(consumer_base["material"]),
                  learned_release_bindings=[
                      read.get("learned_release_binding")
                      for read in consumer_base["material"]["values_read"]
                      if read.get("channel") == "empirical"]),
        same_marginals=dict(receipt_hash=consumer_changed["receipt_hash"],
                            state=consumer_changed["material"]["state"],
                            steps_cells=cells_of(consumer_changed["material"])))
    (out / "generic_consumer_values_read.json").write_text(
        json.dumps(values_read, indent=2, sort_keys=True) + "\n")

    firewall = dict(
        schema="PYAT_R41_P41_ACTOR_FIREWALL_RECEIPT@1",
        receipt_content_hash=base_receipt["content_hash"],
        firewall=base_receipt["firewall"],
        route_probability=base_receipt["structural"]["route_probability"],
        route_probability_reason=base_receipt["structural"]["route_probability_reason"],
        actor_executions=base_receipt["structural"]["actor_executions"],
        model_calls=base_receipt["structural"]["model_calls"],
        sampling_unit_firewall=dict(
            individual="LAWFUL_TEST_ONLY_INDIVIDUAL_SOURCE_RISK_SET",
            household_or_dyad="REFUSED_SAMPLING_UNIT_FIREWALL",
            reason="no linkage authority exists for a dyad sampling unit"))
    (out / "actor_firewall_receipt.json").write_text(
        json.dumps(firewall, indent=2, sort_keys=True) + "\n")

    invalidation_service = P41Service()
    before = invalidation_service.consumer_read()
    civil_invalidation = invalidation_service.readthrough.invalidate("civil_sanction")
    after_civil = invalidation_service.consumer_read()
    empirical_service = P41Service()
    empirical_service.readthrough.invalidate("empirical")
    consumer_after_empirical = empirical_service.consumer_read()
    no_current = prepare()
    no_current_service = P41Service(no_current)
    archived_source = no_current_service.consumer_read()
    selected = no_current.composition.b5_selection_receipt
    no_current.lifecycle.declare_no_current(
        selected.selection_key_ref,
        expected_previous_receipt_ref=selected.ref,
        event_authority_ref=ref("LifecycleAuthority", "none"),
        event_rule_ref=ref("LifecycleRule", "none"),
        reason_ref=ref("Reason", "none"),
        selection_attestation_ref=ref("SelectionAttestation", "none"))
    fresh_refusal = None
    try:
        no_current_service.consumer_read()
        fresh_refusal = "NO_REFUSAL"
    except ValueError as exc:
        fresh_refusal = type(exc).__name__ + ": " + str(exc)[:120]
    archived = no_current_service.historical(archived_source["receipt_hash"])
    serving = dict(
        schema="PYAT_R41_P41_CURRENT_HISTORICAL_SERVING_INVALIDATION@1",
        clock_matrix=dict(
            early_2026=_summarize(early), late_2027=_summarize(revised)),
        structural_selective_invalidation=dict(
            scope="civil_sanction",
            affected_receipts=len(civil_invalidation["invalidated_for_fresh_use"]),
            unaffected_receipts=len(civil_invalidation["unaffected"]),
            after_routes={key: value["state"] for key, value in
                          after_civil["material"]["structural_routes"].items()},
            empirical_steps_unchanged=(
                cells_of(after_civil["material"]) == cells_of(before["material"]))),
        source_permission_revocation=dict(
            scope="empirical",
            consumer_state=consumer_after_empirical["material"]["state"],
            consumer_steps=consumer_after_empirical["material"]["empirical"]["steps"],
            producer_channel_steps=[
                step["state"] for step in empirical_service.progressive()["n10e_steps"]]),
        declared_no_current=dict(
            fresh_serve_refusal=fresh_refusal,
            archived=dict(archival_only=archived["archival_only"],
                          fresh_use_authorized=archived["fresh_use_authorized"],
                          material_equal=archived["material"] == archived_source["material"])))
    (out / "current_historical_serving_invalidation.json").write_text(
        json.dumps(serving, indent=2, sort_keys=True) + "\n")
    print("receipts written")


def _summarize(receipt):
    return dict(
        content_hash=receipt["content_hash"],
        query=receipt["query"],
        steps=[dict(conditioners=step["conditioners"], route=step["route"],
                    state=step["state"], denominator=step["denominator"],
                    cells={cell["cell"]: cell["raw_numerator_support"]
                           for cell in step["cells"]},
                    uncertainty=step["uncertainty"])
               for step in receipt["n10e_steps"]],
        n10w_state=receipt["n10w"]["progressive_chain_state"],
        unknown=receipt["unknown"],
        routes=(receipt["structural"]["routes"] if receipt["structural"] else None))


if __name__ == "__main__":
    main()
