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

    def test_high_cardinality_numeric_roundtrip_and_cost_witness(self):
        """Numerical exactness and realistic sparse-dictionary cost, not a policy PASS."""
        import hashlib
        import time
        import pandas as pd
        import numpy as np
        import pyreadstat
        from unittest import mock
        from rawlsing_next.pre553_physical_decoder import decode_sav
        from rawlsing_next.pre553_country_numeric_carrier import _encode_cell, _hash
        n, width = 1600, 40
        base = np.arange(n, dtype=np.float64)
        frame = pd.DataFrame({
            "v" + str(i): base * (1.000001 + i * 0.00001) + i * 0.001
            for i in range(width)
        })
        frame.insert(0, "country", np.where(np.arange(n) % 2 == 0, 1, 2))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)
            original = path / "original.sav"
            pyreadstat.write_sav(frame, str(original))
            original_bytes = original.stat().st_size
            digest = hashlib.sha256(original.read_bytes()).hexdigest()
            with decode_sav(original, expected_source_sha256=digest) as incidence:
                key = next(incidence.iter_native_column("country")).raw_value
                expected = [
                    (c.row_ordinal, c.variable_ordinal, _encode_cell(c))
                    for c in incidence.iter_country_cells("country", key)
                ]
                started = time.monotonic()
                receipt = build_country(
                    incidence, country_variable="country", country_value=key,
                    output=path / "country.sqlite", require_current=lambda: True,
                    block_rows=128,
                )
                elapsed = time.monotonic() - started
            self.assertEqual(receipt.country_rows, n // 2)
            with CountryReader(path / "country.sqlite", receipt, require_current=lambda: True) as read:
                actual = [
                    (c.row_ordinal, c.variable_ordinal, _encode_cell(c))
                    for c in read.iter_cells()
                ]
                self.assertEqual(actual, expected)
                # Even a one-variable GROUP intersection requires two full
                # carrier SHA-256 rehashes under the current cold-reader API.
                import rawlsing_next.pre553_country_numeric_carrier as carrier
                with mock.patch.object(carrier, "_hash", wraps=_hash) as hashes:
                    rows = list(read.matching_rows({"v0": 0.0}))
                    self.assertEqual(rows, [1])
                    self.assertEqual(hashes.call_count, 2)
            print("HOSTILE_HIGH_CARDINALITY_NUMERIC_COST", {
                "source_rows": n, "native_columns": width + 1,
                "selected_rows": receipt.country_rows,
                "selected_cells": receipt.country_rows * (width + 1),
                "country_sqlite_bytes": receipt.bytes,
                "original_full_wave_sav_bytes": original_bytes,
                "relative_db_to_original": round(receipt.bytes / original_bytes, 3),
                "build_seconds": round(elapsed, 3),
                "full_carrier_rehashes_per_physical_query": 2,
                "grade": "SOURCEFREE_PHYSICAL_ONLY_NO_NATIVE_SCALE",
            })
