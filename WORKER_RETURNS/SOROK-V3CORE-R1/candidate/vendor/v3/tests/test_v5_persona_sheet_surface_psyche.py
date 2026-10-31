from __future__ import annotations

import unittest

from v3.core.derived import compute_all_derived
from v3.core.state import BackboneState
from v3.io.persona_sheet import build_persona_sheet


def _surface_psyche_fixture() -> dict[str, object]:
    return {
        "schema_version": "v516_surface_psyche_profile",
        "domains": {
            "body_self": {
                "felt_register": "constriction_low_aperture_fatigue_disappearance_pull",
                "ordinary_attribution": "my_body_is_off_or_everything_gets_under_my_skin",
                "analyst_pressure_account": {"hidden": True},
                "nested": {
                    "pressure_flow_history": [{"stage": "hidden"}],
                    "per_domain_trace_delta": {"body_self": {"capacity.health": -1.0}},
                    "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS": {"body_self": {8: 1.0}},
                },
            }
        },
        "analyst_pressure_account": {"top_level": True},
        "pressure_flow_history": [{"stage": "hidden"}],
        "per_domain_trace_delta": {"body_self": {"capacity.health": -1.0}},
        "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS": {"body_self": {8: 1.0}},
    }


class TestPersonaSheetSurfacePsyche(unittest.TestCase):
    def test_build_persona_sheet_exports_sanitized_surface_psyche(self) -> None:
        state = BackboneState(year=2026, age=43)
        state.rendered_output = {"narrative_snapshot": {"scene": "A year passed."}, "dialogue_snippets": [], "consistency_check": {}}
        state.surface_psyche_profile = _surface_psyche_fixture()
        derived = compute_all_derived(state)

        sheet = build_persona_sheet(state, derived, identity_override={"country": "US", "given_name": "Test"})

        self.assertIn("surface_psyche", sheet)
        surface = sheet["surface_psyche"]
        self.assertNotIn("vitality_profile", surface)
        self.assertNotIn("analyst_pressure_account", surface)
        self.assertNotIn("pressure_flow_history", surface)
        self.assertNotIn("per_domain_trace_delta", surface)
        self.assertNotIn("DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS", surface)
        self.assertNotIn("analyst_pressure_account", surface["domains"]["body_self"])
        self.assertNotIn("nested", surface["domains"]["body_self"])

    def test_build_persona_sheet_keeps_voice_and_current_state_contract(self) -> None:
        state = BackboneState(year=2026, age=29)
        state.rendered_output = {"narrative_snapshot": {"scene": "A year passed."}, "dialogue_snippets": [], "consistency_check": {}}
        state.surface_psyche_profile = _surface_psyche_fixture()
        derived = compute_all_derived(state)

        sheet = build_persona_sheet(state, derived, identity_override={"country": "US", "given_name": "Test"})

        self.assertIn("identity", sheet)
        self.assertIn("current_state", sheet)
        self.assertIn("voice_profile", sheet)
        self.assertIn("surface_psyche", sheet)
        self.assertEqual(sheet["identity"]["age"], 29)
        self.assertIn("needs", sheet["current_state"])
        self.assertIn("speech_tics", sheet["voice_profile"])


if __name__ == "__main__":
    unittest.main()
