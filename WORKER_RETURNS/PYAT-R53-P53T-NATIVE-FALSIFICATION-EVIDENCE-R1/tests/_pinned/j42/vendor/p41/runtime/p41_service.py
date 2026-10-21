"""P41 generic progressive N9/N10E/N10W positioned possibility service.

Composes the accepted E04L apparatus (actual computed N10E/C1 provider,
learned-release read-through, original E04 consumers, M4/M5 selected world)
and the E03 N10W progressive chain into one versioned generic service.
No parent generator, no actor, no route probability, no invented estimator.
"""
from __future__ import annotations

from copy import deepcopy

import bootstrap  # noqa: F401  (installs staged apparatus on import)
from fixture import CONDITIONS, prepare
from readthrough import ReadThroughService
from product.nonparent import consume
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03

SERVICE_VERSION = "P41_GENERIC_POSSIBILITY_SERVICE@1"
SERVICE_SCHEMA = "PYAT_R41_P41_GENERIC_POSSIBILITY_RECEIPT@1"
PROVIDER_VERSIONS = {
    "n9_world": "E04_TEST_ONLY_SELECTED_WORLD_M4_M5@1",
    "n10e_empirical": "N10E_PUBLIC_SINGLE|C1_PUBLIC_MULTI_BINDING",
    "n10w_progressive": "E03_PROGRESSIVE_CHAIN@1",
    "n9_structural_consumer": "NONPARENT_OPTIONS@1",
    "learned_release": "E04L_M1_M2_B5_READTHROUGH@1",
}
CONSUMER_PERMISSIONS = {
    "NONPARENT_OPTIONS": "ADMITTED_TEST_ONLY",
    "GENERIC_POSITIONED_SUBJECT": "ADMITTED_TEST_ONLY",
    "CONCEPTION_SCENARIO_PROPOSALS": "CONSUMER_PERMISSION_UNISSUED",
    "SOROK_ACTOR": "REFUSED_ACTOR_FIREWALL",
    "HOUSEHOLD_DYAD": "REFUSED_SAMPLING_UNIT_FIREWALL",
}
NONAUTHORITATIVE_CONTRACT = (
    "P41_VERSIONED_CONSUMER_CONTRACT@1: NONAUTHORITATIVE read-only contract; "
    "consumes N9 selected-world and N10E receipt references only; no actor "
    "state, no personhood, no encounter or route probability; later competent "
    "approval required.")
FIREWALL_TEXT = (
    "distributions describe TEST_ONLY source risk sets; they are not a person, "
    "not an encounter, not a partner choice and not a route probability")


class P41ServiceError(ValueError):
    pass


class P41Service:
    def __init__(self, world=None):
        self.prepared = world or prepare()
        self.readthrough = ReadThroughService(self.prepared)
        self.provider = self.prepared.native_provider
        self.receipts = {}

    def structural_context(self, snapshot=None, world_part=True):
        if not world_part:
            return None
        snap = snapshot if snapshot is not None else self.prepared.snapshot
        material = consume(self.readthrough, snap)["material"]
        return dict(
            consumer="NONPARENT_OPTIONS",
            state=material["state"],
            routes={key: value["state"]
                    for key, value in material["structural_routes"].items()},
            route_probability=material.get("route_probability"),
            route_probability_reason=material.get("route_probability_reason"),
            actor_executions=material.get("actor_executions"),
            model_calls=material.get("model_calls"),
            snapshot_ref=material.get("snapshot_ref"))

    def _world_block(self, snapshot):
        material = snapshot.material
        selections = dict(mode=material["mode"], valid_at=material["valid_at"],
                          published_asof=material["published_asof"])
        rules = {}
        for key in ("training_access", "training_fee", "exit_cost",
                    "civil_open", "civil_sanction"):
            slot = material["fields"].get(key) or {}
            payload = slot.get("payload") or {}
            rules[key] = dict(value=payload.get("value"),
                              revision=payload.get("revision"),
                              publication=payload.get("publication"),
                              effective_from=payload.get("effective_from"))
        return dict(selection=selections, rules=rules,
                    permission_root="TEST_ONLY_E04_SOURCE_ROOT",
                    currentness="CURRENT_TEST_ONLY_SELECTION")

    def _step_view(self, step):
        return dict(
            target=step["target"],
            conditioners=[list(c) for c in step["conditioners"]],
            state=step["state"],
            route=step.get("route"),
            denominator=step["denominator"],
            cells=[dict(cell=c["cell"],
                        raw_numerator_support=c["raw_numerator_support"])
                   for c in step["cells"]],
            uncertainty=step.get("uncertainty"),
            evidence_ref=step.get("evidence_ref"),
            producer_fact_ref=step.get("producer_fact_ref"),
            producer_query_ref=step.get("producer_query_ref"),
            condition_witness_ref=step.get("condition_witness_ref"),
            model_rule_hash=step.get("model_rule_hash"),
            risk_set_ref=step.get("risk_set_ref"),
            release_ref=step.get("release_ref"),
            content_hash=step.get("content_hash"))

    def progressive(self, target="Y", conditions=CONDITIONS, *,
                    consumer="GENERIC_POSITIONED_SUBJECT", snapshot=None,
                    world_part=True):
        if consumer not in CONSUMER_PERMISSIONS:
            raise P41ServiceError("UNKNOWN_CONSUMER:" + str(consumer))
        permission = CONSUMER_PERMISSIONS[consumer]
        if permission.startswith("REFUSED"):
            raise P41ServiceError(permission + ":" + consumer)
        if permission == "CONSUMER_PERMISSION_UNISSUED":
            return dict(schema=SERVICE_SCHEMA, service=SERVICE_VERSION,
                        consumer=dict(name=consumer, permission_state=permission,
                                      contract=NONAUTHORITATIVE_CONTRACT),
                        state="CONSUMER_PERMISSION_UNISSUED",
                        receipt=None,
                        versioned_consumer_contract=NONAUTHORITATIVE_CONTRACT)
        ordered = tuple(tuple(c) for c in conditions)
        permit = self.provider.world["query_permits"].get(target) or {}
        if target == "Y":
            role_class = "FORWARD_AUTHORIZED"
        elif permit:
            role_class = "REVERSE_AUTHORIZED"
        else:
            raise P41ServiceError("TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE")
        trace_start = len(self.provider.trace)
        steps = self.provider.progressive(target, ordered)
        trace_consumptions = [entry for entry in self.provider.trace[trace_start:]
                              if entry.get("call") == "evaluate_positioned_subject_possibility"]
        positioned = []
        for index, step in enumerate(steps):
            entry = trace_consumptions[index] if index < len(trace_consumptions) else None
            if entry is not None:
                positioned.append(dict(result_state=entry.get("result_state"),
                                       consumer_result_hash=entry.get("consumer_result_hash"),
                                       same_evidence_object=entry.get("same_evidence_object"),
                                       source="LIVE_TRACE"))
            else:
                positioned.append(dict(result_state=step["state"],
                                       consumer_result_hash=None,
                                       same_evidence_object=True,
                                       source="CACHED_PRODUCTION_CONSUMPTION"))
        world = self._world_block(snapshot or self.prepared.snapshot)
        structural = self.structural_context(snapshot, world_part=world_part)
        step_views = [self._step_view(step) for step in steps]
        all_cells = [cell for step in step_views for cell in step["cells"]]
        receipt = dict(
            schema=SERVICE_SCHEMA, service=SERVICE_VERSION,
            providers=dict(PROVIDER_VERSIONS),
            query=dict(target=target,
                       ordered_conditions=[list(c) for c in ordered],
                       role_class=role_class,
                       role_authority_refs=[permit.get("target_ref")],
                       query_identity_hash=semantic_hash([target, ordered])),
            n9_world=world,
            n10e_steps=step_views,
            n10w=dict(
                progressive_chain_state=(
                    "EXACT_PROGRESSIVE_CHAIN" if all(
                        step["state"] == "EXACT_SUPPORTED" for step in step_views)
                    else "TYPED_PARTIAL_OR_UNKNOWN"),
                positioned_consumptions=positioned,
                progressive_update_identity=[
                    semantic_hash([target, ordered[:depth]])
                    for depth in range(1, len(ordered) + 1)]),
            minorities=dict(
                all_alternatives_preserved=all(
                    len(step["cells"]) >= 2 for step in step_views if step["cells"]),
                smallest_cell=min(
                    (cell for cell in all_cells),
                    key=lambda cell: cell["raw_numerator_support"],
                    default=None),
                raw_counts_exact=True),
            unknown=dict(
                zero_support_steps=[index + 1 for index, step in enumerate(step_views)
                                    if step["state"] == "ZERO_SUPPORT"],
                evidence_state=("NO_SUPPORTED_EVIDENCE" if any(
                    step["state"] == "ZERO_SUPPORT" for step in step_views)
                    else "EXACT_SUPPORT_ON_CONDITIONED_RISK_SET"),
                never_fabricated_zero=True),
            structural=structural,
            consumer=dict(name=consumer, permission_state=permission,
                          values_read="consumer material produced by the "
                                      "admitted nonparent consumer"),
            firewall=dict(
                actor_state_present=False, personhood_present=False,
                encounter_probability_present=False,
                sampling_unit="INDIVIDUAL_SOURCE_RISK_SET_TEST_ONLY",
                text=FIREWALL_TEXT),
            dependencies=["m4_m5_selected_world", "e04_catalog_rules",
                          "n10e_computed_provider", "c1_multi_binding",
                          "e03_progressive_chain", "e04_nonparent_consumer"],
            replay_grade="DETERMINISTIC_CONTENT_HASH_VERIFIABLE")
        receipt["content_hash"] = semantic_hash(
            {key: value for key, value in receipt.items() if key != "content_hash"})
        self.receipts[receipt["content_hash"]] = deepcopy(receipt)
        return receipt

    def e03_chain_receipt(self):
        chain = e03.run_progressive_chain()
        return dict(
            schema="PYAT_R41_P41_N10W_CHAIN_RECEIPT@1",
            machinery="E03_PROGRESSIVE_CHAIN@1",
            steps=[dict(step_id=step.step_id,
                        conditions=[list(c) for c in step.conditioners],
                        route=step.producer_route,
                        state=step.producer_fact_state,
                        denominator=step.raw_denominator_support,
                        cells={key: value["raw_numerator_support"]
                               for key, value in step.cells.items()})
                   for step in chain.steps],
            f8_consumptions=[dict(step_id=item["step_id"],
                                  result_state=item["result_state"])
                             for item in chain.f8_consumptions],
            effects=dict(chain.effects) if chain.effects else {})

    def review_point(self, target, condition):
        return self._step_view(self.provider.step(target, ((condition, 1),)))

    def historical(self, receipt_hash):
        return self.readthrough.historical_receipt(receipt_hash)

    def publish_rule_revision(self, key, value, *, effective_from, effective_to,
                              publication, revision):
        """Publish a TEST_ONLY structural rule revision through the E04 catalog."""
        catalog = self.readthrough.catalog
        catalog._publish(key, value, effective_from, effective_to, publication,
                         revision=revision)
        catalog.catalog_hash = semantic_hash(
            dict(records=catalog.records, empirical=catalog.empirical_identity()))

    def consumer_read(self, snapshot=None):
        """Actual original-consumer read (learned-release read-through path)."""
        return consume(self.readthrough,
                       snapshot if snapshot is not None else self.prepared.snapshot)

    def revoke(self, scope):
        result = self.readthrough.catalog.revoke(scope)
        return dict(scope=scope, revocation=result)

    def current_clock_snapshot(self, valid_at, published_asof):
        return self.readthrough.select(mode="AS_OF", valid_at=valid_at,
                                       published_asof=published_asof)
