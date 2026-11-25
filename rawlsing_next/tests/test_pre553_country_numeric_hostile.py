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
    from rawlsing_next.pre553_source_backed_c11_facade import _PackedRoutingFacts
    scoped = replace(
        original, respondents=respondents,
        row_bindings=tuple(b for b in original.row_bindings if b.row_ordinal in chosen),
        routing=_PackedRoutingFacts(r for r in original.routing if r.scoped_respondent_ref["object_id"] in ids),
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
            route_ref=release.public_objects.routing.row_ref(0)
            self.assertEqual(repo.resolve_object_exact(route_ref).ref,route_ref)
            reader.close()
            with self.assertRaises(CountryCarrierError):
                repo.resolve_object_exact(route_ref)
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
                route_ref=release.public_objects.routing.row_ref(0)
                state["current"] = False
                with self.assertRaises(CountryCarrierError):
                    repo.resolve_object_exact(route_ref)
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
                # Historical #1345 measured two full rehashes per query.
                # V2 authenticates each selected lane against the external
                # root, after one full cold-open SHA check.
                import rawlsing_next.pre553_country_numeric_carrier as carrier
                with mock.patch.object(carrier, "_hash", wraps=_hash) as hashes:
                    rows = list(read.matching_rows({"v0": 0.0}))
                    self.assertEqual(rows, [1])
                    self.assertEqual(hashes.call_count, 0)
            self.assertLess(receipt.bytes,original_bytes)
            self.assertLess(receipt.bytes,1171456//2)
            print("HOSTILE_HIGH_CARDINALITY_NUMERIC_COST", {
                "source_rows": n, "native_columns": width + 1,
                "selected_rows": receipt.country_rows,
                "selected_cells": receipt.country_rows * (width + 1),
                "country_sqlite_bytes": receipt.bytes,
                "original_full_wave_sav_bytes": original_bytes,
                "relative_db_to_original": round(receipt.bytes / original_bytes, 3),
                "build_seconds": round(elapsed, 3),
                "full_carrier_rehashes_per_physical_query": 0,
                "grade": "SOURCEFREE_PHYSICAL_ONLY_NO_NATIVE_SCALE",
            })


    def test_binary_dictionary_preserves_exact_R5_exceptions_and_bits(self):
        import struct
        from decimal import Decimal
        from rawlsing_next.pre553_country_numeric_carrier import (
            _pack_dictionary,_read_dictionary,_encode_cell,_BINARY_DICTIONARY,
        )
        from rawlsing_next.pre553_r5_codec import R5OpaqueValue
        from rawlsing_next.pre553_physical_decoder import PhysicalCell,PhysicalMissingState
        values=[float(i)*1.000001 for i in range(512)]
        values.extend([-0.0,0.0,float("nan"),float("inf"),float("-inf"),None,
                       0,True,"0",2**100,-2**60,Decimal("-0.000"),
                       R5OpaqueValue("test",b"\x00\xff"),"a\x00é"])
        tokens=tuple(_encode_cell(PhysicalCell(i+1,1,"q",v,
            PhysicalMissingState.SYSTEM_MISSING if v is None else PhysicalMissingState.OBSERVED_STORAGE_VALUE,
            {"tag":"decl"} if i%13==0 else None,"label" if i%17==0 else None))
            for i,v in enumerate(values))
        packed=_pack_dictionary(tokens)
        self.assertTrue(packed.startswith(_BINARY_DICTIONARY))
        self.assertEqual(_read_dictionary(packed),tokens)
        self.assertNotEqual(tokens[512],tokens[513])
        # No type conflation: float zero, integer zero, bool, string distinct.
        self.assertEqual(len(set(tokens[517:521])),4)

    def test_typed_dictionary_exact_tokens_detached_mutation_and_real_reader(self):
        from decimal import Decimal
        from unittest import mock
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        from rawlsing_next.pre553_r5_codec import R5OpaqueValue
        from rawlsing_next.pre553_physical_decoder import PhysicalCell,PhysicalMissingState
        from rawlsing_next.pre553_country_numeric_carrier import NumericColumn
        # Force the binary lane, plus legacy token lane, with nested metadata
        # and exact exceptional raw values, including type distinctions.
        values=[float(i)*1.000001 for i in range(512)]
        values.extend([-0.0,0.0,float("nan"),float("inf"),float("-inf"),None,
                       0,True,"0",2**100,-2**60,Decimal("-0.000"),
                       R5OpaqueValue("test",b"\x00\xff"),"a\x00é",
                       {"raw":[1,{"nested":2}]}])
        cells=[PhysicalCell(i+1,1,"q",v,
            PhysicalMissingState.SYSTEM_MISSING if v is None else PhysicalMissingState.OBSERVED_STORAGE_VALUE,
            {"decl":{"nested":[7]}},["label",{"x":3}]) for i,v in enumerate(values)]
        tokens=tuple(carrier._encode_cell(x) for x in cells)
        binary=carrier._pack_dictionary(tokens)
        self.assertTrue(binary.startswith(carrier._BINARY_DICTIONARY))
        legacy=carrier.zlib.compress(carrier.canonical_json(tokens).encode("ascii"))
        for payload in (binary,legacy):
            typed=carrier._read_dictionary(payload,typed=True)
            self.assertEqual(tuple(typed),tokens)
            col=NumericColumn(tuple(range(1,len(tokens)+1)),tuple(range(len(tokens))),typed)
            original=NumericColumn(col.row_ordinals,col.codes,tokens)
            for v in (-0.0,0.0,0,True,"0",float("nan"),None,2**100):
                self.assertEqual(col.observed_codes_for(v),original.observed_codes_for(v))
            with mock.patch.object(carrier,"_decode_cell",side_effect=AssertionError("wire decode in typed reader")):
                self.assertEqual(tuple(carrier._encode_cell(x) for x in col.cells(1,"q")),tokens)
                cell=col.cell_at(0,1,"q")
                cell.source_missing_declaration["decl"]["nested"].append(999)
                cell.raw_value_label[1]["x"]=999
                raw=col.cell_at(len(tokens)-1,1,"q")
                raw.raw_value["raw"][1]["nested"]=999
                self.assertEqual(carrier._encode_cell(col.cell_at(0,1,"q")),tokens[0])
                self.assertEqual(carrier._encode_cell(col.cell_at(1,1,"q")),tokens[1])
                self.assertEqual(carrier._encode_cell(col.cell_at(len(tokens)-1,1,"q")),tokens[-1])
        # Actual repository consumer, including cached reconstruction, must
        # not fall back to the former token parser.
        with tempfile.TemporaryDirectory() as d:
            reader,repo,release,_=_country_repository(d,lambda:True)
            try:
                from rawlsing_next.pre553_empirical_objects import RespondentEvent
                bodies=release.public_objects.lane.bodies
                with mock.patch.object(carrier,"_decode_cell",side_effect=AssertionError("wire decode in native reader")):
                    for i in range(len(bodies)):
                        event=bodies.materialize(i)
                        self.assertIsInstance(event,RespondentEvent)
                        self.assertEqual(repo.resolve_object_exact(event.ref),event)
                    self.assertTrue(list(reader.iter_cells()))
                self.assertLessEqual(bodies.cache_bytes,8*1024*1024)
            finally:
                reader.close()

    def test_selected_lane_pin_and_external_root_refuse_substitution(self):
        import sqlite3
        from unittest import mock
        import rawlsing_next.pre553_country_numeric_carrier as carrier
        with tempfile.TemporaryDirectory() as d:
            reader,repo,release,ref=_country_repository(d,lambda:True)
            try:
                block,rows=next(reader._blocks())
                row=reader.db.execute("SELECT width,dict,codes FROM lanes WHERE block=? AND ordinal=1",(block,)).fetchone()
                real=reader.db
                class MutatedDB:
                    def execute(self,sql,args=()):
                        if sql.startswith("SELECT width,dict,codes"):
                            return self
                        return real.execute(sql,args)
                    def fetchone(self):
                        return row[0],row[1],row[2]+b"corruption"
                reader.db=MutatedDB()
                try:
                    with self.assertRaisesRegex(CountryCarrierError,"lane authentication failed"):
                        reader._column(block,rows,1)
                finally:
                    reader.db=real
                # Correct file hash alone cannot repair a substituted external root.
                with self.assertRaisesRegex(CountryCarrierError,"metadata mismatch|inventory"):
                    CountryReader(reader.path,replace(reader.receipt,lane_root="0"*64),require_current=lambda:True)
            finally:
                reader.close()

    def test_reopened_reader_detects_mutated_file_during_session(self):
        with tempfile.TemporaryDirectory() as d:
            reader,repo,release,ref=_country_repository(d,lambda:True)
            try:
                with reader.path.open("ab") as f:
                    f.write(b"changed")
                with self.assertRaises(CountryCarrierError):
                    list(reader.matching_rows({"G":"A"}))
                with self.assertRaises(CountryCarrierError):
                    repo.resolve_object_exact(ref)
            finally:
                reader.close()


    def test_legacy_country_v1_remains_readable_with_full_authentication(self):
        import sqlite3
        from unittest import mock
        import rawlsing_next.pre553_country_numeric_carrier as c
        from rawlsing_next.pre553_physical_decoder import PhysicalCell,PhysicalMissingState
        from dataclasses import asdict
        import json,zlib
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"legacy.sqlite"
            info=dict(source_sha256="1"*64,metadata_digest="2"*64,source_rows=1,
                country_variable="G",country_key=c.canonical_json(c._CODEC.encode("A")),country_rows=1)
            with sqlite3.connect(path) as db:
                db.executescript("CREATE TABLE meta(k TEXT PRIMARY KEY,v TEXT);"
                    "CREATE TABLE vars(ordinal INTEGER PRIMARY KEY,name TEXT);"
                    "CREATE TABLE blocks(id INTEGER PRIMARY KEY,n INTEGER,rows BLOB);"
                    "CREATE TABLE lanes(block INTEGER,ordinal INTEGER,width INTEGER,dict BLOB,codes BLOB);")
                db.executemany("INSERT INTO meta VALUES(?,?)",[(k,c.canonical_json(v)) for k,v in
                    dict(schema=c.LEGACY_SCHEMA,**info).items()])
                db.execute("INSERT INTO vars VALUES(1,'G')")
                db.execute("INSERT INTO blocks VALUES(0,1,?)",(c._pack([1],8),))
                token=c._encode_cell(PhysicalCell(1,1,"G","A",PhysicalMissingState.OBSERVED_STORAGE_VALUE,None,None))
                db.execute("INSERT INTO lanes VALUES(0,1,1,?,?)",
                    (zlib.compress(c.canonical_json([token]).encode("ascii")),c._pack([0],1)))
            receipt=c.CountryReceipt(**info,sha256=c._hash(path),bytes=path.stat().st_size)
            self.assertIsNone(receipt.lane_root)
            with c.CountryReader(path,receipt,require_current=lambda:True) as reader:
                with mock.patch.object(c,"_hash",wraps=c._hash) as hashes:
                    self.assertEqual(list(reader.matching_rows({"G":"A"})),[1])
                    self.assertEqual(hashes.call_count,2)
