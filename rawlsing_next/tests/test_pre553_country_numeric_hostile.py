"""Independent hostile sourcefree checks against PR #1341 at 37cab231.

A negative court for existing C11Repository's exact-object ingress: every country-
backed object access must respect the same live-reader / currentness boundary as
resolve_release_exact.  No original survey data or custody documents.
"""
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from rawlsing_next.pre553_country_numeric_carrier import (
    CountryReader, CountryCarrierError, build_country,
)
from rawlsing_next.pre553_physical_decoder import PHYSICAL_METADATA_CONTRACT
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


def _country_repository(folder, current):
    fx = _fixture("country-hostile-object-current")
    incidence = replace(fx["incidence"], file_metadata={
        "contract_schema": PHYSICAL_METADATA_CONTRACT,
        "raw_layout_declarations": {}, "normalized_geometry": {},
        "display_metadata": {}, "decoder_identity": {"fixture": "country-hostile-object-current"},
    })
    original = fx["projection"]
    chosen = (1, 3)
    respondents = tuple(original.respondents[i - 1] for i in chosen)
    ids = {r.ref.object_id for r in respondents}
    scoped = replace(
        original, respondents=respondents,
        row_bindings=tuple(b for b in original.row_bindings if b.row_ordinal in chosen),
        routing=tuple(r for r in original.routing if r.scoped_respondent_ref["object_id"] in ids),
    )
    path = Path(folder) / "country.sqlite"
    receipt = build_country(incidence, country_variable="G", country_value="A",
                            output=path, require_current=current, block_rows=1)
    reader = CountryReader(path, receipt, require_current=current)
    repo, release = reader.native_repository(scoped, current_authorities=fx["authorities"])
    non_event = release.public_objects.non_events[0]
    # Prove we target a genuine non-event public C11 member, not an unavailable ref.
    assert non_event.schema_id != "RespondentEvent"
    assert repo.resolve_object_exact(non_event.ref) == non_event
    return reader, repo, release, non_event.ref


class HostileCountryCurrentness(unittest.TestCase):
    def test_closed_reader_refuses_direct_non_event_object_resolution(self):
        with tempfile.TemporaryDirectory() as d:
            reader, repo, release, ref = _country_repository(d, lambda: True)
            reader.close()
            with self.assertRaises(CountryCarrierError):
                repo.resolve_release_exact(release.release_ref)
            # This exact-object path must not evade the same country custody.
            with self.assertRaises(CountryCarrierError):
                repo.resolve_object_exact(ref)

    def test_revoked_country_refuses_direct_non_event_object_resolution(self):
        with tempfile.TemporaryDirectory() as d:
            state = {"current": True}
            def current():
                return state["current"]
            reader, repo, release, ref = _country_repository(d, current)
            try:
                state["current"] = False
                with self.assertRaises(CountryCarrierError):
                    repo.resolve_release_exact(release.release_ref)
                with self.assertRaises(CountryCarrierError):
                    repo.resolve_object_exact(ref)
            finally:
                reader.close()
