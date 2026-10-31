from __future__ import annotations

import sys
import unittest
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.derived import compute_all_derived
from v3.core.state import BackboneState
from v3.io.persona_sheet import build_persona_sheet


class TestPersonaSheetIntegrity(unittest.TestCase):
    def test_field_provenance_records_defaulted_fields_and_coherence_warnings(self) -> None:
        state = BackboneState(year=2026, age=31)
        derived = compute_all_derived(state)
        sheet = build_persona_sheet(
            state,
            derived,
            identity_override={
                "country": "MDV",
                "locality": "Bogota",
                "languages": ["English", "or mute"],
                "_source_provenance": {
                    "ethnic": {"source_family": "provided", "fallback_used": False},
                    "religion_language": {
                        "source_family": "provided",
                        "source_method": "manual",
                        "fallback_used": False,
                        "language_found": True,
                        "fallback_reason": "",
                    },
                    "location": {
                        "source_family": "geonames",
                        "geo_country_code_used": "BR",
                        "city_found": True,
                        "fallback_used": False,
                        "fallback_reason": "",
                    },
                },
            },
        )

        metadata = sheet["metadata"]
        self.assertEqual(metadata["field_provenance"]["given_name"]["source"], "defaulted")
        self.assertEqual(metadata["field_provenance"]["country"]["canonical_name"], "Maldives")
        self.assertEqual(metadata["language_integrity"]["status"], "invalid_labels_found")
        self.assertEqual(metadata["field_provenance"]["field_integrity"], "degraded")
        self.assertIn("_coherence_warnings", metadata["field_provenance"])
        self.assertIn("geo country BR", metadata["field_provenance"]["_coherence_warnings"][0])


if __name__ == "__main__":
    unittest.main()
