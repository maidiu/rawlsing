"""Governed-court wrapper for frozen OBL059 R10 bounded repair."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R10/governed_bounded_court_r10.py"

spec = importlib.util.spec_from_file_location("_obl059_r10_bounded_repair_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R10 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R10BoundedRepair(module.CourtR10):
    def test_122_all_ordered_cross_carrier_negative_to_positive_mutations_use_entry_view(self):
        # Cover all ordered pairs among opportunity + three evidence components.
        nodes = (
            "opportunity",
            "subject_classification",
            "actor_activation",
            "developmental_phase",
        )
        for target in nodes:
            for mutator in nodes:
                if target == mutator:
                    continue
                with self.subTest(target=target, mutator=mutator):
                    packet, carriers = module.make_all_custom()
                    repair, expected = module.make_invalid(target, carriers, packet)
                    field, valid_value = repair
                    target_carrier = carriers[target]
                    module.install_side_effect(
                        packet,
                        carriers,
                        mutator,
                        lambda target_carrier=target_carrier, field=field, valid_value=valid_value: target_carrier.replace(field, valid_value),
                    )
                    self.assert_negative_r10(packet, expected)

        # Top-level evidence carrier changes every later semantic carrier.
        for target in nodes:
            with self.subTest(target=target, mutator="evidence"):
                packet, carriers = module.make_all_custom()
                repair, expected = module.make_invalid(target, carriers, packet)
                field, valid_value = repair
                target_carrier = carriers[target]
                module.install_side_effect(
                    packet,
                    carriers,
                    "evidence",
                    lambda target_carrier=target_carrier, field=field, valid_value=valid_value: target_carrier.replace(field, valid_value),
                )
                self.assert_negative_r10(packet, expected)

        # Other carriers changing the evidence parent's initially missing actor slot.
        for mutator in ("opportunity", "subject_classification", "developmental_phase"):
            with self.subTest(target="evidence", mutator=mutator):
                packet, carriers = module.make_all_custom()
                valid_actor = carriers["actor_activation"]
                carriers["evidence"].replace("actor_activation", None)
                evidence_carrier = carriers["evidence"]
                module.install_side_effect(
                    packet,
                    carriers,
                    mutator,
                    lambda evidence_carrier=evidence_carrier, valid_actor=valid_actor: evidence_carrier.replace("actor_activation", valid_actor),
                )
                self.assert_negative_r10(packet, "ACTOR_ACTIVATION_EVIDENCE_MISSING")
