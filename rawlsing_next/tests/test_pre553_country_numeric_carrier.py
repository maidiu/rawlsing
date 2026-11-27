"""Actual generated SAV/DTA -> country compact codes -> exact cold physical replay."""
import hashlib
from pathlib import Path
import tempfile
import unittest
import pandas as pd
import pyreadstat
from rawlsing_next.pre553_physical_decoder import decode_sav,decode_dta
from rawlsing_next.pre553_country_numeric_carrier import (
    build_country,CountryReader,CountryCarrierError,_encode_cell
)

class CountryNumeric(unittest.TestCase):
    def test_writer_scalar_memo_exact_tokens_and_bounded_fallback(self):
        from decimal import Decimal
        from dataclasses import replace
        from unittest.mock import patch
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        from rawlsing_next.pre553_physical_decoder import PhysicalCell,PhysicalMissingState
        from rawlsing_next.pre553_r5_codec import R5OpaqueValue
        state=PhysicalMissingState.OBSERVED_STORAGE_VALUE
        values=(False,True,0,1,0.,-0.,1.,None,"0","é",b"0",2**100,
                Decimal("0.00"),float("nan"),float("inf"),0.12345,
                R5OpaqueValue("x",b"abc"),{"v":[1]}, "x"*1025)
        cells=[PhysicalCell(i+1,1,"q",value,state,None,label)
               for i,value in enumerate(values) for label in (None,True,0,-0.,"0")]
        oracle=[carrier._encode_cell(c) for c in cells]
        memo=carrier._CellTokenMemo(16)
        with patch.object(carrier,"_encode_cell",wraps=carrier._encode_cell) as encode:
            self.assertEqual([memo.token(c) for c in cells],oracle)
            self.assertEqual([memo.token(c) for c in cells],oracle)
            self.assertLess(encode.call_count,2*len(cells))
            self.assertLessEqual(len(memo.entries),16)
        c=cells[0]
        self.assertNotEqual(memo.token(c),memo.token(replace(c,raw_value=0)))
        self.assertNotEqual(memo.token(replace(c,raw_value=0.)),memo.token(replace(c,raw_value=-0.)))
        # Mutable metadata is evaluated on every request, never memoized.
        declaration={"nested":[1]}
        c=replace(c,source_missing_declaration=declaration)
        before=memo.token(c)
        declaration["nested"][0]=2
        self.assertNotEqual(before,memo.token(c))
        self.assertEqual(memo.token(c),carrier._encode_cell(c))
        with self.assertRaises(AttributeError):
            memo.token(replace(cells[0],missing_state=state.value))
        # Disabled cache uses the exact original codec.
        self.assertEqual([carrier._CellTokenMemo(0).token(c) for c in cells],oracle)

    def test_writer_memo_preserves_persistent_bytes_and_census(self):
        from unittest.mock import patch
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/"source.sav"
            pyreadstat.write_sav(pd.DataFrame({
                "country":[1.]*65,
                "categorical":[float(i%5) for i in range(65)],
                "unique":[i*1.000123 for i in range(65)],
                "text":["é" if i%2 else "0" for i in range(65)],
            }),str(src))
            def build(path):
                with decode_sav(src) as inc:
                    return build_country(inc,country_variable="country",country_value=1.,
                         output=path,block_rows=16,require_current=lambda:True)
            with patch.object(carrier._CellTokenMemo,"token",lambda self,c:carrier._encode_cell(c)):
                old=build(root/"old.sqlite")
            new=build(root/"new.sqlite")
            self.assertEqual(old,new)
            self.assertEqual((root/"old.sqlite").read_bytes(),(root/"new.sqlite").read_bytes())
            with CountryReader(root/"new.sqlite",new,require_current=lambda:True) as read:
                self.assertEqual(list(read.matching_rows({"categorical":2.})),list(range(3,66,5)))

    def test_opaque_dictionary_accounting_counts_payload_once(self):
        from rawlsing_next.pre553_country_numeric_carrier import _TypedCellDictionary
        from rawlsing_next.pre553_r5_codec import R5OpaqueValue
        from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
        blob=b"x"*(1024*1024)
        opaque=R5OpaqueValue("fixture",blob)
        state=PhysicalMissingState.OBSERVED_STORAGE_VALUE.value
        small=_TypedCellDictionary(((R5OpaqueValue("fixture",b"x"),state,None,None),))
        big=_TypedCellDictionary(((opaque,state,None,None),))
        repeated=_TypedCellDictionary(((opaque,state,None,None),(opaque,state,None,"label")))
        self.assertGreaterEqual(big.retained_bytes(),len(blob))
        # CPython's shared-key instance dictionaries can vary slightly in size.
        self.assertGreater(big.retained_bytes()-small.retained_bytes(),len(blob)-4096)
        self.assertLess(repeated.retained_bytes()-big.retained_bytes(),4096)

    def test_emitted_header_preserves_distinct_identities_and_fallback(self):
        from types import SimpleNamespace
        from rawlsing_next._pre553_c11_execution_view import (
            _CountryHeaderBuilder,_COUNTRY_EVENT_PREFIX,_COUNTRY_OCCURRENCE_PREFIX,
            _COUNTRY_GROUP_PREFIX,_PackedCountrySelectors,_compact_identity)
        from rawlsing_next.pre553_empirical_objects import ExactRef,RespondentEvent
        h="a"*64;occ="b"*64;group="c"*64
        q=ExactRef("question","q","d"*64)
        universe=ExactRef("universe","u","e"*64)
        respondent=ExactRef("respondent","r","f"*64)
        event=SimpleNamespace(ref=ExactRef(RespondentEvent.FAMILY,_COUNTRY_EVENT_PREFIX+h,h),
            typed_state="OBSERVED",native_question_ref=q,canonical_question_ref_if_authorized=q,
            component_or_subitem_ref=None,authority_snapshot_refs=(),raw_response_value=1,
            canonical_response_value_if_authorized=1,multiplicity_order_rank_fields={},
            response_event_id_or_deterministic_index=_COUNTRY_OCCURRENCE_PREFIX+occ,
            event_group_id=_COUNTRY_GROUP_PREFIX+group,empirical_universe_ref=universe,
            scoped_respondent_ref=respondent,dependency_refs=(respondent,q))
        builder=_CountryHeaderBuilder()
        first=builder.add(event,source_coordinates=(17,9,2))
        second=builder.add(event,source_coordinates=(17,9,3))
        self.assertEqual(first.event_identity,bytes.fromhex(h))
        self.assertEqual(first.occurrence_identity,bytes.fromhex(occ))
        self.assertEqual(first.group_identity,bytes.fromhex(group))
        self.assertEqual(first.ref,event.ref)
        self.assertEqual(first.event_group_id,event.event_group_id)
        self.assertEqual(first.response_event_id_or_deterministic_index,
                         event.response_event_id_or_deterministic_index)
        self.assertEqual(first.source_coordinates,(17,9,2))
        self.assertIs(first.payload,second.payload)
        self.assertEqual(first.selector.ref,event.ref)
        # A future noncanonical producer may not be silently rewritten.
        event.ref=ExactRef(RespondentEvent.FAMILY,"foreign:"+h,h)
        event.response_event_id_or_deterministic_index="foreign:"+occ
        event.event_group_id=b"opaque group"
        third=builder.add(event,source_coordinates=(17,9,4))
        self.assertEqual(third.ref,event.ref)
        self.assertEqual(third.event_group_id,event.event_group_id)
        self.assertEqual(third.selector.response_event_id_or_deterministic_index,
                         event.response_event_id_or_deterministic_index)
        self.assertEqual(_compact_identity(_COUNTRY_OCCURRENCE_PREFIX+occ.upper(),_COUNTRY_OCCURRENCE_PREFIX),
                         (_COUNTRY_OCCURRENCE_PREFIX+occ.upper(),))
        old=_PackedCountrySelectors.build((third,),SimpleNamespace(hashes=bytes.fromhex(h)))
        self.assertIs(type(old),tuple)
        self.assertEqual(old[0],third.selector)
        # The exact same occurrence ID can legitimately recur in a different
        # group, so the compact sufficient proof must fall back, not reject.
        from dataclasses import replace
        from unittest.mock import patch
        from rawlsing_next import pre553_c11_integrity as integrity
        different=replace(first,occurrence_identity=b"x"*32)
        with patch.object(integrity,"canonical_json",
                          side_effect=AssertionError("redundant full occurrence encoding")):
            integrity.ensure_distinct_event_occurrences((first,different))
        group2=replace(first,group_identity=b"y"*32)
        self.assertFalse(integrity._country_occurrence_ids_distinct((first,group2)))
        integrity.ensure_distinct_event_occurrences((first,group2))
        with self.assertRaisesRegex(integrity.C11IntegrityError,"duplicate response occurrence"):
            integrity.ensure_distinct_event_occurrences((first,second))
        self.assertFalse(integrity._country_occurrence_ids_distinct((first,third)))
        # Foreign string fallback spelling of a canonical ID must not evade
        # the complete composite duplicate check.
        alias=replace(first,occurrence_identity=(first.response_event_id_or_deterministic_index,))
        with self.assertRaisesRegex(integrity.C11IntegrityError,"duplicate response occurrence"):
            integrity.ensure_distinct_event_occurrences((first,alias))

    def test_packed_selector_filters_before_object_materialization(self):
        from array import array
        from unittest.mock import patch
        from rawlsing_next._pre553_c11_execution_view import (
            _PackedCountrySelectors,_EventLane,_RespondentEvents,_country_respondent_events)
        from rawlsing_next.pre553_empirical_objects import ExactRef
        q=("question","q","a"*64);other=("question","other","b"*64)
        payloads=(("OBSERVED",q,q,None,(),1,1,{}),
                  ("MISSING",other,q,q,(),None,None,{}))
        n=64
        digests=b"".join(hashlib.sha256(str(i).encode()).digest() for i in range(n))
        packed=_PackedCountrySelectors(digests,digests,
            memoryview(array("I",(i%2 for i in range(n))).tobytes()).cast("I"),payloads)
        lane=_EventLane(None,packed)
        oracle=_RespondentEvents(_EventLane(None,tuple(packed)),tuple(range(n)))
        for rows in (tuple(range(10)),tuple(range(n))):
            actual=_country_respondent_events(lane,rows)
            expected=_RespondentEvents(oracle.lane,rows)
            for target in (q,other):
                for native in (False,True):
                    for component in (False,True):
                        for states in (None,frozenset({"OBSERVED"}),frozenset({"MISSING"}),frozenset()):
                            args=dict(native_only=native,include_component=component,states=states)
                            self.assertEqual(tuple(actual.select(ExactRef(*target),**args)),
                                tuple(expected.select(ExactRef(*target),**args)))
            # A negative state selector must not construct even one object.
            with patch.object(_PackedCountrySelectors,"__getitem__",
                    side_effect=AssertionError("rejected selector materialized")):
                self.assertEqual(tuple(actual.select(ExactRef(*q),states=frozenset())),())

    def test_packed_lane_digest_geometry_and_coherently_rehashed_gap(self):
        import sqlite3
        from dataclasses import replace
        from rawlsing_next.pre553_country_numeric_carrier import (
            _PackedLaneDigests,_manifest_root)
        ordinals=(2,9,31)
        expected={(b,j):hashlib.sha256(f"{b}:{j}".encode()).digest()
                  for b in range(7) for j in ordinals}
        pins=_PackedLaneDigests(ordinals,b"".join(expected.values()))
        self.assertEqual(len(pins),len(expected))
        self.assertEqual(len(pins._digests),32*len(expected))
        for key,digest in expected.items():
            self.assertEqual(pins.get(key),digest)
        for key in ((-1,2),(7,2),(0,3)):
            self.assertIsNone(pins.get(key))
        with self.assertRaises(CountryCarrierError):
            _PackedLaneDigests(ordinals,b"bad")
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/"source.sav";path=root/"country.sqlite"
            pyreadstat.write_sav(pd.DataFrame({"country":[1.,1.,1.],"q":[2.,3.,4.]}),str(src))
            with decode_sav(src) as incidence:
                receipt=build_country(incidence,country_variable="country",country_value=1.,
                    output=path,require_current=lambda:True,block_rows=1)
            with CountryReader(path,receipt,require_current=lambda:True) as read:
                self.assertIsInstance(read._lane_auth,_PackedLaneDigests)
                self.assertEqual(list(read.matching_rows({"q":3.})),[2])
            # Rehash a structurally incomplete rectangle. Content authentication
            # alone cannot establish completeness, even with a matching root.
            with sqlite3.connect(path) as db:
                db.execute("DELETE FROM lanes WHERE block=1 AND ordinal=(SELECT min(ordinal) FROM vars)")
                root_hash=_manifest_root(db.execute("SELECT ordinal,name FROM vars ORDER BY ordinal"),
                    db.execute("SELECT id,n,digest FROM blocks ORDER BY id"),
                    db.execute("SELECT block,ordinal,digest FROM lanes ORDER BY block,ordinal"))
                import json
                db.execute("UPDATE meta SET v=? WHERE k='lane_root'",(json.dumps(root_hash),))
            bad=replace(receipt,lane_root=root_hash,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size)
            with self.assertRaisesRegex(CountryCarrierError,"inventory"):
                CountryReader(path,bad,require_current=lambda:True)

    def test_virtual_event_order_and_packed_posting_differential(self):
        from rawlsing_next._pre553_c11_execution_view import (
            _CountryEventEntries,_EventRead,_EventLane,_country_respondent_events,_RespondentEvents)
        from rawlsing_next.pre553_empirical_objects import ExactRef
        base=("a","b","c")
        for boundary in range(4):
            for count in (0,1,97):
                seq=_CountryEventEntries(base,boundary,count)
                oracle=base[:boundary]+tuple(range(count))+base[boundary:]
                self.assertEqual(tuple(seq),oracle)
                self.assertEqual(seq[::-2],oracle[::-2])
                for i in range(-len(oracle),len(oracle)):
                    self.assertEqual(seq[i],oracle[i])
                with self.assertRaises(IndexError):
                    _=seq[len(oracle)]
                with self.assertRaises(TypeError):
                    _=seq[0.5]
        target=("question","q","a"*64)
        other=("question","other","b"*64)
        selectors=tuple(_EventRead(("event",str(i),hashlib.sha256(str(i).encode()).hexdigest()),
            "OBSERVED" if i%3 else "MISSING",target if i%2 else other,
            target if i%5 else other,target if i%7==0 else None,(),i,i,{},str(i))
            for i in range(103))
        lane=_EventLane(None,selectors)
        rows=tuple(range(len(selectors)))
        old=_RespondentEvents(lane,rows)
        new=_country_respondent_events(lane,rows)
        self.assertTrue(new.rows.readonly)
        self.assertEqual(tuple(new.rows),rows)
        self.assertEqual(new.rows.nbytes,4*len(rows))
        for q in (target,other):
            for native in (False,True):
                for component in (False,True):
                    for states in (None,frozenset({"OBSERVED"}),frozenset({"MISSING"}),frozenset()):
                        args=dict(native_only=native,include_component=component,states=states)
                        self.assertEqual(tuple(new.select(ExactRef(*q),**args)),
                                         tuple(old.select(ExactRef(*q),**args)))
        from dataclasses import replace
        same=_EventLane(None,tuple(replace(s,_canonical_question_identity=s._native_question_identity)
                                   for s in selectors))
        shared=_country_respondent_events(same,rows)
        self.assertIs(shared.question_rows[0],shared.question_rows[1])

    def test_native_column_pushdown_retains_exact_full_stream_cells(self):
        from unittest.mock import patch
        from rawlsing_next.pre553_physical_decoder import _bounded_rows_per_chunk, MIN_READ_ROWS
        from rawlsing_next.pre553_country_numeric_carrier import country_census
        # Non-first country column, heterogeneous physical types, many
        # unrequested columns, and multiple batches. Use actual SAV and DTA.
        for ext,writer,decoder in (("sav",pyreadstat.write_sav,decode_sav),
                                   ("dta",pyreadstat.write_dta,decode_dta)):
            with self.subTest(ext=ext), tempfile.TemporaryDirectory() as d:
                src=Path(d)/("wide."+ext)
                data={"unused_text":["x","y","z","u","v","w"],
                      "country":[1,2,1,float("nan"),2,1]}
                data.update({f"unused_{i}":[i+j for j in range(6)] for i in range(96)})
                writer(pd.DataFrame(data),str(src))
                with decoder(src) as incidence:
                    expected=[c for c in incidence.iter_cells(batch_size=17)
                              if c.variable_name=="country"]
                    real=pyreadstat.read_file_in_chunks
                    calls=[]
                    def observe(*args,**kwargs):
                        calls.append(dict(kwargs))
                        yield from real(*args,**kwargs)
                    with patch.object(pyreadstat,"read_file_in_chunks",side_effect=observe):
                        actual=list(incidence.iter_native_column("country",batch_size=3))
                        census=country_census(incidence,country_variable="country",
                                               require_current=lambda:True)
                    self.assertEqual(len(actual),len(expected))
                    self.assertEqual([(c.row_ordinal,c.variable_ordinal,_encode_cell(c)) for c in actual],
                                     [(c.row_ordinal,c.variable_ordinal,_encode_cell(c)) for c in expected])
                    self.assertEqual([c.row_ordinal for c in actual],list(range(1,7)))
                    self.assertTrue(all(c.variable_ordinal==expected[0].variable_ordinal for c in actual))
                    self.assertEqual(sum(census["observed"].values()),5)
                    self.assertEqual(sum(census["held"].values()),1)
                    self.assertEqual(len(calls),2)
                    self.assertTrue(all(c.get("usecols")==["country"] for c in calls))
                    self.assertEqual(calls[0]["chunksize"],_bounded_rows_per_chunk(
                        1,3,floor_rows=MIN_READ_ROWS if ext=="dta" else 1))
                    with self.assertRaisesRegex(ValueError,"unknown native column"):
                        list(incidence.iter_native_column("not_a_source_column"))

    def test_manifest_stream_matches_exact_v2_canonical_preimage(self):
        from rawlsing_next.pre553_country_numeric_carrier import _manifest_root, SCHEMA
        from rawlsing_next.pre553_r5_codec import canonical_json
        for n,p in ((0,0),(1,1),(3,7),(37,101)):
            variables=tuple((j,("é雪"+str(j))) for j in range(p))
            blocks=tuple((i,i+1,hashlib.sha256(f"block{i}".encode()).digest()) for i in range(n))
            lanes=tuple((i,j,hashlib.sha256(f"lane{i}:{j}".encode()).digest())
                        for i in range(n) for j in range(p))
            oracle=hashlib.sha256(canonical_json([
                SCHEMA,list(variables),[[i,k,d.hex()] for i,k,d in blocks],
                [[i,j,d.hex()] for i,j,d in lanes],
            ]).encode("ascii")).hexdigest()
            self.assertEqual(_manifest_root(iter(variables),iter(blocks),iter(lanes)),oracle)
            if len(lanes)>1:
                self.assertNotEqual(_manifest_root(variables,blocks,reversed(lanes)),oracle)
            if lanes:
                self.assertNotEqual(_manifest_root(variables,blocks,lanes[:-1]),oracle)

    def test_real_formats_and_direct_intersection(self):
        for ext,writer,decoder in (("sav",pyreadstat.write_sav,decode_sav),
                                   ("dta",pyreadstat.write_dta,decode_dta)):
            with self.subTest(ext=ext), tempfile.TemporaryDirectory() as d:
                p=Path(d)
                src=p/("source."+ext)
                frame=pd.DataFrame({"country":[1,2,1,2,1,2],
                     "q":[3,3,4,4,3,2],"other":[9,8,7,6,5,4],
                     "text":["a","b","a","b","c","a"]})
                writer(frame,str(src))
                source_sha=hashlib.sha256(src.read_bytes()).hexdigest()
                with decoder(src,expected_source_sha256=source_sha) as incidence:
                    original=list(incidence.iter_cells())
                    country_value=next(c.raw_value for c in original if c.variable_name=="country")
                    q_value=next(c.raw_value for c in original if c.variable_name=="q")
                    receipt=build_country(incidence,country_variable="country",country_value=country_value,
                        output=p/"one.sqlite",require_current=lambda:None,block_rows=2)
                    self.assertEqual(receipt.country_rows,3)
                    self.assertEqual(receipt.source_rows,6)
                    with self.assertRaises(CountryCarrierError):
                        build_country(incidence,country_variable="country",country_value=country_value,
                            output=p/"one.sqlite",require_current=lambda:None)
                # No original source is needed for physical cold replay.
                src.unlink()
                with CountryReader(p/"one.sqlite",receipt,require_current=lambda:None) as read:
                    self.assertEqual(list(read.row_ordinals()),[1,3,5])
                    expected=[(c.row_ordinal,c.variable_ordinal,_encode_cell(c)) for c in original if c.row_ordinal in (1,3,5)]
                    actual=[(c.row_ordinal,c.variable_ordinal,_encode_cell(c)) for c in read.iter_cells()]
                    self.assertEqual(actual,expected)
                    self.assertEqual(list(read.matching_rows({"country":country_value,"q":q_value})),[1,5])
                    self.assertEqual(read.db.execute("SELECT count(*) FROM lanes").fetchone()[0],8)
                    with self.assertRaises(CountryCarrierError):
                        read.native_release(None)
                with self.assertRaises(CountryCarrierError):
                    CountryReader(p/"one.sqlite",receipt,require_current=lambda:False)
                with (p/"one.sqlite").open("ab") as out:
                    out.write(b"corruption")
                with self.assertRaises(CountryCarrierError):
                    CountryReader(p/"one.sqlite",receipt,require_current=lambda:None)

    def test_cancel_build_no_published_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"source.sav"
            pyreadstat.write_sav(pd.DataFrame({"country":[1,1,2],"q":[2,3,4]}),str(src))
            with decode_sav(src) as incidence:
                value=next(incidence.iter_cells()).raw_value
                checks=[0]
                def live():
                    checks[0]+=1
                    return checks[0]<2
                with self.assertRaises(CountryCarrierError):
                    build_country(incidence,country_variable="country",country_value=value,
                                  output=p/"cancel.sqlite",require_current=live,block_rows=1)
            self.assertFalse((p/"cancel.sqlite").exists())
            self.assertEqual(list(p.glob(".country-*")),[])

    def test_country_scoped_native_c11_and_actual_i03_match_direct_replay(self):
        from dataclasses import replace
        from rawlsing_next.pre553_physical_decoder import PHYSICAL_METADATA_CONTRACT
        from rawlsing_next.pre553_source_backed_c11_facade import (
            ExactPhysicalCellStream, build_validated_source_backed_c11_release_from_stream)
        from rawlsing_next.pre553_c11_repository import C11Repository
        from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
        from rawlsing_next.pre553_empirical_query import execute_empirical_query
        from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture, _source_dict
        from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _branch_predicate, _query
        fx=_fixture("country-compact")
        # Existing sourcefree governed fixture; its G coordinate stands in for
        # an explicit country code. This does not issue real country authority.
        inc=replace(fx["incidence"],file_metadata={
            "contract_schema":PHYSICAL_METADATA_CONTRACT,
            "raw_layout_declarations":{}, "normalized_geometry":{},
            "display_metadata":{}, "decoder_identity":{"fixture":"country-compact"},
        })
        chosen=(1,3)
        original=fx["projection"]
        respondents=tuple(original.respondents[i-1] for i in chosen)
        refs={x.ref.as_dict()["object_id"] for x in respondents}
        subset=replace(original,respondents=respondents,
            row_bindings=tuple(x for x in original.row_bindings if x.row_ordinal in chosen),
            routing=tuple(x for x in original.routing
                if x.scoped_respondent_ref["object_id"] in refs))
        cells=tuple(c for c in inc.iter_cells() if c.row_ordinal in chosen)
        direct=build_validated_source_backed_c11_release_from_stream(
            ExactPhysicalCellStream(inc.source_sha256,len(chosen),lambda:iter(cells)),subset)
        from rawlsing_next.pre553_source_backed_c11_facade import _PackedRoutingFacts
        subset=replace(subset,routing=_PackedRoutingFacts(iter(subset.routing)))
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"country.sqlite"
            rec=build_country(inc,country_variable="G",country_value="A",
                    output=path,require_current=lambda:None,block_rows=1)
            with CountryReader(path,rec,require_current=lambda:None) as reader:
                with self.assertRaises(CountryCarrierError):
                    reader.native_release(original)
                from unittest.mock import patch
                # The new path may not first construct the old full public
                # event graph and then call the old compactor.
                from unittest.mock import PropertyMock
                from rawlsing_next._pre553_c11_execution_view import _CountryEventHeader
                with patch("rawlsing_next.pre553_source_backed_c11_facade._compact_public_objects",
                           side_effect=AssertionError("eager event graph compactor")), patch.object(
                           _CountryEventHeader,"selector",new_callable=PropertyMock,
                           side_effect=AssertionError("validated header expanded before selection")):
                    compact_repo,compact=reader.native_repository(subset,current_authorities=fx['authorities'])
                # A copied transport cannot substitute its physical cell factory.
                from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
                tripwire=replace(reader._native_stream(subset),
                    cell_iter_factory=lambda:(_ for _ in ()).throw(AssertionError("foreign cell factory")))
                _, rebound=build_source_backed_c11_repository(tripwire,subset,current_authorities=fx["authorities"])
                self.assertEqual(rebound.release_ref,compact.release_ref)
                from rawlsing_next.pre553_empirical_objects import semantic_hash
                self.assertEqual(compact.replay_manifest.content_hash,
                                 semantic_hash(compact.replay_manifest.semantic_projection()))
                from rawlsing_next._pre553_c11_execution_view import _CompactPublicObjects
                self.assertIsInstance(compact.public_objects,_CompactPublicObjects)
                from rawlsing_next.pre553_country_numeric_carrier import _CountryEventBodies
                self.assertIsInstance(compact.public_objects.lane.bodies,_CountryEventBodies)
                self.assertEqual(compact.release_ref,direct.release_ref)
                self.assertEqual(compact.replay_manifest.ref,direct.replay_manifest.ref)
                from rawlsing_next.pre553_c11_integrity import _PackedClosureRefs
                from rawlsing_next.pre553_empirical_objects import URN_PREFIX,RespondentEvent
                packed=compact.replay_manifest.closure_refs
                self.assertIsInstance(packed,_PackedClosureRefs)
                self.assertEqual(tuple(packed),direct.replay_manifest.closure_refs)
                self.assertEqual(compact.replay_manifest.as_dict(),direct.replay_manifest.as_dict())
                self.assertEqual(packed[-1],direct.replay_manifest.closure_refs[-1])
                self.assertEqual(packed[::-2],direct.replay_manifest.closure_refs[::-2])
                self.assertIs(compact.public_objects.lane.bodies.hashes,
                    packed.digest_lane(RespondentEvent.FAMILY,f"{URN_PREFIX}:RespondentEvent:sha256:"))
                # Preserve ordering, duplicates, arbitrary external IDs and
                # full string identity rather than assuming any hash suffix.
                from rawlsing_next.pre553_empirical_objects import ExactRef,canonical_json
                arbitrary=ExactRef("external|kind","external-ü-"+ "a"*64,"a"*64)
                sample=(packed[0],arbitrary,packed[-1],packed[-1])
                repacked=_PackedClosureRefs.pack(sample)
                self.assertEqual(tuple(repacked),sample)
                self.assertEqual(hash(repacked),hash(sample))
                self.assertEqual(b"["+b",".join(repacked.canonical_ref_bytes())+b"]",
                    canonical_json([ref.as_dict() for ref in sample]).encode("utf-8"))
                self.assertNotEqual(repacked,_PackedClosureRefs.pack(sample[:-1]))
                self.assertNotEqual(repacked,_PackedClosureRefs.pack(sample[::-1]))
                from rawlsing_next.pre553_c11_integrity import C11IntegrityError
                kind=RespondentEvent.FAMILY
                prefix=f"{URN_PREFIX}:RespondentEvent:sha256:"
                for bad in (((kind,prefix,b"x"*31),),((kind,prefix+"wrong",b"x"*32),)):
                    with self.assertRaises(C11IntegrityError):
                        _PackedClosureRefs(bad,(1,))
                with self.assertRaises(C11IntegrityError):
                    _PackedClosureRefs(((kind,prefix,b"x"*32),),(2,))
                self.assertEqual(tuple(x.ref for x in compact.public_objects),tuple(x.ref for x in direct.public_objects))
                from rawlsing_next._pre553_c11_execution_view import _CountryEventEntries
                self.assertIsInstance(compact.public_objects.entries.base,_CountryEventEntries)
                self.assertEqual(tuple(x.ref for x in compact.public_objects[::-3]),
                                 tuple(x.ref for x in direct.public_objects[::-3]))
                self.assertEqual(tuple(x.ref for x in compact.public_objects.exact_entries()),
                                 tuple(x.ref for x in direct.public_objects))
                from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
                routes=tuple(x for x in direct.public_objects if isinstance(x,RoutingEligibilityFact))
                self.assertEqual(len(compact.public_objects.routing),len(routes))
                for route in routes:
                    self.assertEqual(compact_repo.resolve_object_exact(route.ref).as_dict(),route.as_dict())
                    self.assertNotIn(route.ref.key,compact_repo._objects)
                    self.assertNotIn(route.ref.key,compact_repo._country_object_guards)
                    with self.assertRaises(KeyError):
                        compact_repo.resolve_object_exact(ExactRef(route.ref.kind,"wrong",route.ref.content_hash))
                from rawlsing_next.pre553_empirical_objects import RespondentEvent,ExactRef
                events=[x for x in direct.public_objects if isinstance(x,RespondentEvent)]
                lane=compact.public_objects.lane
                from rawlsing_next._pre553_c11_execution_view import _PackedCountrySelectors,_EventRead
                self.assertIsInstance(lane.selectors,_PackedCountrySelectors)
                self.assertIs(lane.selectors.hashes,lane.bodies.hashes)
                self.assertEqual(len(lane.selectors.occurrence_hashes),32*len(events))
                self.assertTrue(lane.selectors.codes.readonly)
                self.assertEqual(lane.selectors[::-2],tuple(lane.selectors)[::-2])
                for selector,event in zip(lane.selectors,events):
                    self.assertIs(type(selector),_EventRead)
                    for field in ("ref","typed_state","native_question_ref",
                        "canonical_question_ref_if_authorized","component_or_subitem_ref",
                        "authority_snapshot_refs","raw_response_value",
                        "canonical_response_value_if_authorized","multiplicity_order_rank_fields",
                        "response_event_id_or_deterministic_index"):
                        observed=getattr(selector,field)
                        expected=getattr(event,field)
                        if isinstance(observed,ExactRef) and not isinstance(expected,ExactRef):
                            from rawlsing_next.pre553_empirical_objects import exact_ref
                            expected=exact_ref(expected)
                        self.assertEqual(observed,expected)
                self.assertEqual(lane.bodies.locator_bytes,40*len(events))
                self.assertTrue(lane.bodies.direct)
                from rawlsing_next import pre553_source_backed_c11_facade as facade
                with patch.object(facade,"_event",wraps=facade._event) as constructs, patch(
                        "rawlsing_next.pre553_carrier_execution.materialize_public_object",
                        side_effect=AssertionError("redundant event wire reconstruction")):
                    for event in events:
                        self.assertEqual(compact_repo.resolve_object_exact(event.ref),event)
                        self.assertNotIn(event.ref.key,compact_repo._objects)
                        self.assertNotIn(event.ref.key,compact_repo._country_object_guards)
                    self.assertEqual(constructs.call_count,len(events))
                # Compare the inherited expanded-event compatibility
                # reconstruction on the identical reader and exact events.
                enumerating=_CountryEventBodies(reader,subset,tuple(events))
                self.assertFalse(enumerating.direct)
                with patch.object(facade,"_event",wraps=facade._event) as old_constructs:
                    for i,event in enumerate(events):
                        self.assertEqual(enumerating.materialize(i),event)
                self.assertGreater(old_constructs.call_count,len(events))
                print("RELAY_EVENT_RECONSTRUCTION",{"events":len(events),
                      "direct_constructor_calls":len(events),
                      "enumerating_constructor_calls":old_constructs.call_count,
                      "locator_bytes":lane.bodies.locator_bytes})
                # A duplicate physical value rule must not be laundered
                # through the new shared lookup dictionary.
                first=subset.response_slots[0]
                ambiguous=replace(subset,response_slots=(replace(first,
                    values=first.values+(first.values[0],)),*subset.response_slots[1:]))
                with self.assertRaisesRegex(CountryCarrierError,"ambiguous physical value rules"):
                    reader.native_repository(ambiguous,current_authorities=fx["authorities"])
                # Deliberate locator substitution must never produce a different
                # positive exact object even when the addressed cell is valid.
                bodies=lane.bodies
                original_codes=bodies.question_codes
                from array import array
                wrong=array("I",original_codes)
                alternate=next(i for i,v in enumerate(wrong) if v!=wrong[0])
                wrong[0]=wrong[alternate]
                bodies.question_codes=memoryview(wrong.tobytes()).cast("I")
                try:
                    with self.assertRaises(CountryCarrierError):
                        bodies.materialize(0)
                finally:
                    bodies.question_codes=original_codes
                self.assertEqual(bodies.materialize(0),events[0])
                mixed=C11Repository((compact,))
                # A wrong object ID may not exploit a matching digest.
                with self.assertRaises(KeyError):
                    mixed.resolve_object_exact(ExactRef(events[0].ref.kind,"wrong",events[0].ref.content_hash))
                # Verify every exact route/risk posting and absence against
                # the original tuple traversal, including cache attestation.
                from rawlsing_next._pre553_query_predicate import _build_release_index,_question_matches
                from rawlsing_next._pre553_query_common import _ref_field
                from rawlsing_next.pre553_empirical_query import _i03_index_attestation,_i03_index_attestation_matches
                idx=_build_release_index(compact,subset.universes[0].ref)
                self.assertIsNotNone(idx.routing_lookup)
                for respondent,facts in idx.routing_by_respondent.items():
                    for fact in facts:
                        target=_ref_field(fact,"question_or_target_ref")
                        risk=_ref_field(fact,"risk_set_ref")
                        want=tuple(x for x in facts if _question_matches(x,target) and _ref_field(x,"risk_set_ref")==risk)
                        self.assertEqual(idx.routing_lookup(respondent=respondent,target=target.key,risk_set=risk.key),want)
                        from rawlsing_next._pre553_c11_execution_view import _RoutingRead
                        selected=idx.routing_lookup.select(respondent=respondent,target=target.key,risk_set=risk.key)
                        self.assertTrue(all(type(x) is _RoutingRead for x in selected))
                        self.assertEqual(tuple(x.ref for x in selected),tuple(x.ref for x in want))
                        for x,y in zip(selected,want):
                            self.assertEqual((x.typed_state,x.routing_state,x.applicability_state,x.authority_snapshot_refs),
                                             (y.typed_state,y.routing_state,y.applicability_state,y.authority_snapshot_refs))
                            self.assertEqual(x.member_set_replay_ref,_ref_field(y,"member_set_replay_ref"))
                        self.assertEqual(tuple(x.ref for x in idx.routing_lookup.select_target(
                            respondent=respondent,target=target.key)),
                            tuple(x.ref for x in facts if _question_matches(x,target)))
                    self.assertEqual(idx.routing_lookup(respondent=respondent,target="absent",risk_set="absent"),())
                attestation=_i03_index_attestation(idx)
                object.__setattr__(idx,"routing_lookup",None)
                self.assertFalse(_i03_index_attestation_matches(idx,attestation))
                a=_source_dict(fx,C11Repository((direct,)),direct)
                b=_source_dict(fx,compact_repo,compact)
                qa=_query_authority("country-compact")
                pred=_branch_predicate(a,qa,members=respondents,tag="country")
                registry=AuthorityRegistry((*fx["authorities"],qa))
                for measure in ("RAW","GOVERNED_WEIGHTED"):
                    with self.subTest(measure=measure):
                        query=_query(a,qa,pred,("Y",),measure=measure,tag="country-"+measure)
                        x=execute_empirical_query(repository=a["repo"],query=query,predicate=pred,
                            authority_registry=registry,release_refs=(direct.release_ref,))
                        y=execute_empirical_query(repository=b["repo"],query=query,predicate=pred,
                            authority_registry=registry,release_refs=(compact.release_ref,))
                        self.assertEqual(x,y)
                        self.assertTrue(x.facts)
                        self.assertTrue(all(f.typed_state=="SUPPORTED" for f in x.facts))
            # A returned native repository cannot continue serving cached
            # selectors after its country reader has closed.
            with self.assertRaises(CountryCarrierError):
                compact_repo.resolve_release_exact(compact.release_ref)
            with self.assertRaises(CountryCarrierError):
                compact_repo.resolve_object_exact(events[0].ref)

    def test_native_preimage_packed_source_preserves_detached_replay(self):
        from dataclasses import replace
        from rawlsing_next.pre553_source_native_preimage_adapter import (
            NativeSourceIdentity,NativeSourcePackage,NativeSourceRule,
            NativePreimageRefusal,materialize_native_preimages,_PackedNativeRows,
            GovernedRowOccurrencePlan,VariableOccurrencePlan,OccurrenceBinding)
        from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
        from rawlsing_next.pre553_country_numeric_carrier import _encode_cell
        from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
        from rawlsing_next.pre553_physical_decoder import PhysicalCell,PhysicalMissingState
        fx=_fixture("packed-native-preimage")
        inc=fx["incidence"]
        package=NativeSourcePackage(NativeSourceIdentity(
            "packed-source","TEST","1","source.sav",inc.source_sha256,"SYNTHETIC",3),
            (NativeSourceRule("x","X"),NativeSourceRule("y","Y")),coordinate_variable="G")
        cells=tuple(inc.iter_cells())
        # Non-governed sparse cells, ordinal variation, noncanonical input
        # order and detached metadata must survive, even if not used by I03.
        cells=tuple(c for c in cells if not (c.row_ordinal==2 and c.variable_name=="W"))
        cells=tuple(replace(c,variable_ordinal=99) if c.row_ordinal==3 and c.variable_name=="W" else c for c in cells)
        cells=tuple(reversed(cells))
        calls=[0]
        def once():
            calls[0]+=1
            if calls[0]>1:
                raise AssertionError("source reread")
            return iter(cells)
        direct=materialize_native_preimages(package=package,incidence=ExactPhysicalCellStream(
            inc.source_sha256,3,lambda:iter(cells)))
        compact=materialize_native_preimages(package=package,incidence=ExactPhysicalCellStream(
            inc.source_sha256,3,once),compact_cells=True,compact_routing=True)
        self.assertEqual(compact.bundle_hash,direct.bundle_hash)
        self.assertEqual(compact.projection.cache_identity,direct.projection.cache_identity)
        self.assertEqual(compact.release.replay_manifest.ref,direct.release.replay_manifest.ref)
        self.assertEqual(compact.respondent_rows,direct.respondent_rows)
        def material(stream):
            return [(c.row_ordinal,c.variable_ordinal,c.variable_name,_encode_cell(c)) for c in stream.iter_cells()]
        self.assertEqual(material(compact.physical_stream),material(direct.physical_stream))
        self.assertEqual(material(compact.physical_stream),material(direct.physical_stream))
        self.assertEqual(calls,[1])
        with self.assertRaises(NativePreimageRefusal):
            _PackedNativeRows.build(iter((*cells,cells[0])),3)
        with self.assertRaises(NativePreimageRefusal):
            _PackedNativeRows.build((c for c in cells if c.row_ordinal!=1),3)
        # A caller-supplied non-decoder-normalized date must not acquire
        # a different physical representation merely by choosing packing.
        import datetime
        changed=(replace(c,raw_value=datetime.date(2020,1,1)) if c.variable_name=="W" else c for c in cells)
        with self.assertRaises(NativePreimageRefusal):
            _PackedNativeRows.build(changed,3)
        # Repeated respondent/occasion: equal response values are distinct
        # events, explicit ordering and source binding survive replay.
        sha=inc.source_sha256
        repeated=[]
        for row,rid,occasion,value in ((1,"a","t1","1"),(2,"a","t2","1"),(3,"b","t1","0")):
            for ordinal,name,raw in ((1,"X",value),(2,"G","A"),(3,"RID",rid),(4,"TIME",occasion)):
                repeated.append(PhysicalCell(row,ordinal,name,raw,PhysicalMissingState.OBSERVED_STORAGE_VALUE,None))
        plan=GovernedRowOccurrencePlan("RID","TIME",(VariableOccurrencePlan("X","REPEATED_MEASUREMENT",(
            OccurrenceBinding("t1","t1",{"kind":"REPEATED_MEASUREMENT","index":0}),
            OccurrenceBinding("t2","t2",{"kind":"REPEATED_MEASUREMENT","index":1}))),),{"a":"A","b":"B"})
        package=replace(package,selected=(NativeSourceRule("x","X"),))
        stream=ExactPhysicalCellStream(sha,3,lambda:iter(repeated))
        a=materialize_native_preimages(package=package,incidence=stream,row_occurrence_plan=plan)
        b=materialize_native_preimages(package=package,incidence=stream,row_occurrence_plan=plan,compact_cells=True,compact_routing=True)
        self.assertEqual(a.bundle_hash,b.bundle_hash)
        self.assertEqual(a.projection.cache_identity,b.projection.cache_identity)
        self.assertEqual(a.occurrence_bindings,b.occurrence_bindings)
        self.assertEqual(a.respondent_rows,b.respondent_rows)
        self.assertEqual(material(a.physical_stream),material(b.physical_stream))

    def test_country_set_resume_and_missing_country_census(self):
        from rawlsing_next.pre553_country_numeric_carrier import country_census,build_country_set
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"source.sav"
            pyreadstat.write_sav(pd.DataFrame({"country":[1,2,1,None,2],"q":[2,3,4,5,6]}),str(src))
            root=p/"countries";root.mkdir()
            with decode_sav(src) as inc:
                census=country_census(inc,country_variable="country",require_current=lambda:None)
                self.assertEqual(sum(census["observed"].values()),4)
                self.assertEqual(sum(census["held"].values()),1)
                first=list(build_country_set(inc,country_variable="country",root=root,require_current=lambda:None))
                self.assertEqual(len(first),2)
                resumed=list(build_country_set(inc,country_variable="country",root=root,
                    require_current=lambda:None,retained_receipts=tuple(r for _,r in first)))
                self.assertEqual(first,resumed)
                rows=[]
                for path,receipt in resumed:
                    with CountryReader(path,receipt,require_current=lambda:None) as reader:
                        rows.extend(reader.row_ordinals())
                self.assertEqual(sorted(rows),[1,2,3,5])

    def test_country_actual_issued_batch_durable_cold_s04_ff01(self):
        from dataclasses import replace
        from rawlsing_next.pre553_physical_decoder import PHYSICAL_METADATA_CONTRACT
        from rawlsing_next.pre553_source_backed_c11_facade import (
            ExactPhysicalCellStream,build_validated_source_backed_c11_release_from_stream)
        from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
        from rawlsing_next.pre553_empirical_objects import semantic_hash
        from rawlsing_next.pre553_issued_workload import (
            NativeWorkload,IssuedWorkloadRecord,canonical,operation_jobs)
        from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
        from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
        from rawlsing_next.pre553_saved_durable_delivery import execute_publish_country,open_country_product
        from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
        from rawlsing_next.tests.test_pre553_empirical_query import (
            _ref,_query_authority,_branch_predicate,_query,_predicate,_response_leaf)
        from rawlsing_next.tests.test_pre553_discovery_exact import (
            _atom,_d_auth,_discovery_authority,_grammar,_qt,_rule)
        fx=_fixture("country-durable")
        inc=replace(fx["incidence"],file_metadata={
            "contract_schema":PHYSICAL_METADATA_CONTRACT,
            "raw_layout_declarations":{}, "normalized_geometry":{},
            "display_metadata":{}, "decoder_identity":{"fixture":"country-durable"},
        })
        chosen=(1,3)
        original=fx["projection"]
        respondents=tuple(original.respondents[i-1] for i in chosen)
        refs={x.ref.object_id for x in respondents}
        projection=replace(original,respondents=respondents,
            row_bindings=tuple(x for x in original.row_bindings if x.row_ordinal in chosen),
            routing=tuple(x for x in original.routing if x.scoped_respondent_ref["object_id"] in refs))
        cells=tuple(c for c in inc.iter_cells() if c.row_ordinal in chosen)
        direct=build_validated_source_backed_c11_release_from_stream(
            ExactPhysicalCellStream(inc.source_sha256,len(chosen),lambda:iter(cells)),projection)
        qa=_query_authority("country-durable")
        da=_d_auth("country-durable-discovery")
        base=_branch_predicate(fx,qa,members=respondents,tag="country-durable-all")
        atom=_predicate(fx,qa,_response_leaf(fx,qa,"X","1"),tag="country-durable-x")
        query=_query(fx,qa,base,("X","Y"),tag="country-durable-joint")
        unary=_query(fx,qa,base,("Y",),tag="country-durable-y")
        grammar=_grammar(operation="I03-OP-country-durable-discovery",
            atoms=[_atom("ALL",base,"BRANCH"),_atom("X1",atom,"RESPONSE")],
            templates=[_qt("Y",unary)],
            rules=[_rule("pair","PAIR_RESPONSE_COTRAVEL","SINGLE_ATOM",atom_ids=("X1",),
                baseline_atom_id="ALL",query_template_id="Y",
                validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})])
        discovery=_discovery_authority(fx,grammar,da)
        cat=RuntimeObjectCatalog((*fx["authorities"],qa,da),(base,atom),(query,unary),(discovery,))
        requests=tuple(I03ExecutionRequest(q.ref,base.ref) for q in (query,unary))
        ds=(discovery.ref,)
        jobs=operation_jobs(requests,ds)
        root=semantic_hash({"fixture":"country-durable"})
        frontier=semantic_hash({"jobs":jobs,"root":root})
        decision=_ref("TEST_ONLY_DECISION","country-durable")
        host,purpose="test-country","TEST_ONLY_COUNTRY_DURABLE"
        descriptor=dict(source_edition=inc.source_sha256,native_item_ids=["X","Y"],
            release_tag=projection.instrument_release_id,routing_and_risk={"fixture":True},
            carrier={"kind":"COUNTRY_NUMERIC"},country_and_population={"fixture":"A"},
            weight_design_estimand={"measure":"RAW"},missing_and_occurrence_policy={"fixture":True},
            target_conditioner_roles={"joint":["X","Y"]})
        workload=NativeWorkload(decision_ref=decision,source_factory_ref=_ref("TEST_ONLY_FACTORY","country-durable"),
            descriptor=canonical(descriptor),projection=projection,catalog=cat,requests=requests,
            discoveries=ds,original_u_root=root,expected_frontier_root=frontier)
        record=IssuedWorkloadRecord(decision_ref=decision,source_permission_ref=_ref("TEST_ONLY_SOURCE_PERMISSION","country"),
            scientific_permission_refs=(_ref("TEST_ONLY_SCIENCE_PERMISSION","country"),),
            host=host,purpose=purpose,source_sha256=inc.source_sha256,
            envelope_sha256=semantic_hash(workload.envelope()),original_u_root=root,
            expected_frontier_root=frontier,expected_jobs=jobs,currentness="CURRENT_GRANTED",
            scope="TEST_ONLY_SOURCEFREE",native_universe_refs=(fx["universe"].ref,))
        resolver=TestOnlyDecisionResolver(record)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);path=p/"country.sqlite";products=p/"products";products.mkdir()
            receipt=build_country(inc,country_variable="G",country_value="A",output=path,require_current=lambda:None)
            # Exercise the same exact I03/I05 owners explicitly before the
            # Batch court, so a failure retains its real exception, not only
            # the scheduler's privacy-preserving failure code.
            from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
            with CountryReader(path,receipt,require_current=lambda:None) as reader:
                repo,rel=reader.native_repository(projection,current_authorities=cat.authorities)
                executor=CarrierNeutralResearchExecutor(repo,(rel.release_ref,),cat)
                group=executor.grouped_i03_scope()
                try:
                    for req in requests:
                        executor.execute_i03(query_ref=req.query_ref,predicate_ref=req.predicate_ref,group_scope=group)
                    executor.execute_i05(discovery_authority_ref=discovery.ref,group_scope=group)
                finally:
                    group.close()
            pub=execute_publish_country(workload,resolver,host=host,purpose=purpose,
                country_path=path,country_receipt=receipt,root_dir=products)
            self.assertTrue(pub.complete)
            self.assertEqual(pub.batch_census["unit_count"],3)
            path.unlink()
            cold=open_country_product(pub.receipt.root_path,expected_root=pub.receipt.root_identity,
                expected_release_ref=direct.release_ref,country_receipt=receipt,workload=workload,
                resolver=resolver,host=host,purpose=purpose)
            # Physical transport is compact but the canonical root and
            # all cold reader identities are unchanged. Old plain manifests
            # remain readable, and ambiguous/corrupt transports fail closed.
            from rawlsing_next import pre553_durable_empirical_closure as durable
            from rawlsing_next.pre553_empirical_objects import canonical_json
            root_path=Path(pub.receipt.root_path)
            packed_path=root_path/durable.COMPACT_MANIFEST_NAME
            plain_path=root_path/durable.MANIFEST_NAME
            packed=packed_path.read_bytes()
            plain=canonical_json(cold._closure.manifest).encode("utf-8")
            self.assertLess(len(packed),len(plain))
            self.assertEqual(pub.receipt.manifest_bytes,len(packed))
            plain_path.write_bytes(plain)
            try:
                with self.assertRaises(durable.DurableEmpiricalClosureError):
                    durable.open_empirical_closure(root_path,expected_root=pub.receipt.root_identity)
                packed_path.unlink()
                legacy=durable.open_empirical_closure(root_path,expected_root=pub.receipt.root_identity)
                self.assertEqual(legacy.exact_ref,cold._closure.exact_ref)
                self.assertEqual(canonical_json(legacy.manifest),canonical_json(cold._closure.manifest))
            finally:
                plain_path.unlink()
                packed_path.write_bytes(packed)
            for bad in (packed[:-1],packed+b"trailing", (2**32).to_bytes(8,"big")+packed[8:]):
                try:
                    packed_path.write_bytes(bad)
                    with self.assertRaises(durable.DurableEmpiricalClosureError):
                        durable.open_empirical_closure(root_path,expected_root=pub.receipt.root_identity)
                finally:
                    packed_path.write_bytes(packed)
            read=cold.read_s04(query.ref,conditioner_index=0)
            self.assertEqual(read.first_consumer.execution.facts[0].raw_denominator_support,1)
            self.assertEqual(read.first_consumer.ff01.semantic_projection()["raw_fully_resolved_joint_n"],1)
            result,=cold._closure.discovery_results
            self.assertEqual(result.candidate_count,result.covered_candidate_count)
            self.assertEqual(result.candidate_count,1)
            with self.assertRaises(ValueError):
                open_country_product(pub.receipt.root_path,expected_root=pub.receipt.root_identity,
                    expected_release_ref=direct.release_ref,country_receipt=replace(receipt,sha256="0"*64),
                    workload=workload,resolver=resolver,host=host,purpose=purpose)
            # A resolver returning the same dataclass instance is not proof
            # its issuing material is unchanged. Country scope pins it by
            # detached value and rejects in-place mutation at the reader.
            old=record.source_permission_ref
            try:
                object.__setattr__(record,"source_permission_ref",
                                   _ref("TEST_ONLY_SOURCE_PERMISSION","changed-in-place"))
                with self.assertRaises(ValueError):
                    cold.read_s04(query.ref)
            finally:
                object.__setattr__(record,"source_permission_ref",old)
            # Bulk serving must not leak a successful prefix on mid-batch revocation.
            from unittest.mock import patch
            original_read=cold._read_s04_retained
            def revoke(*args,**kwargs):
                value=original_read(*args,**kwargs)
                resolver._record=replace(record,currentness="REVOKED")
                return value
            with patch.object(cold,"_read_s04_retained",side_effect=revoke) as read_one:
                with self.assertRaises(ValueError):
                    cold.read_s04_many(((query.ref,0),(unary.ref,None)))
                self.assertEqual(read_one.call_count,1)
            with self.assertRaises(ValueError):
                cold.read_s04(query.ref)


    def test_lifetime_routing_columns_preserve_exact_bytes_and_refuse_bad_geometry(self):
        from rawlsing_next.pre553_source_backed_c11_facade import (
            _RoutingColumnBuilder,_routing_column_value,_PackedRoutingFacts,
            SourceBackedC11FacadeError)
        from rawlsing_next.pre553_empirical_objects import canonical_json
        # All physical encodings are lossless for arbitrary canonical byte
        # values, including controls and noncanonical reference-like strings.
        cases=[
            ([b'"constant"']*1000,b"C"),
            ([b'"a"']*500+[b'"b"']*500,b"R"),
            ([b'"a"',b'"b"']*500,b"B"),
            ([canonical_json(str(i)).encode() for i in range(300)]*5,b"S"),
            ([canonical_json({"content_hash":hashlib.sha256(str(i).encode()).hexdigest(),
              "kind":"REPLAY_ROOT","object_id":"urn:test:common-prefix:"+str(i)}).encode()
              for i in range(5000)],b"H"),
            ([b'{"content_hash":"'+b'f'*64+b'","object_id":"arbitrary"}',
              b'{"content_hash":"'+b'F'*64+b'","object_id":"arbitrary"}'],None),
        ]
        for values,layout in cases:
            col=_RoutingColumnBuilder()
            for value in values:col.add(value)
            lane=col.finish()
            if layout is not None:self.assertTrue(lane[3].startswith(layout),lane[3:4])
            self.assertEqual([_routing_column_value(lane,i) for i in range(len(values))],values)
        # Validate actual sealed geometry before a prepared digest can rely
        # on it; malformed tags/runs/codes cannot be hashed through one path
        # and randomly accessed through another.
        from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
        fixture=_fixture("lifetime-routing-columns")
        packed=_PackedRoutingFacts(iter(fixture["projection"].routing))
        original=packed.immutable_storage()
        rows=list(packed.canonical_rows())
        self.assertEqual(rows,[canonical_json(x.as_dict()).encode()
                              for x in fixture["projection"].routing])
        runs,ends=original
        keys,cols,digests=runs[0]
        column=cols[0]
        for invalid in ((column[0],column[1],b"",b"R"),
                        (column[0],column[1],b"",b"UNKNOWN")):
            try:
                object.__setattr__(packed,"_storage",(((keys,(invalid,*cols[1:]),digests),*runs[1:]),ends))
                with self.assertRaises(SourceBackedC11FacadeError):packed.immutable_storage()
            finally:object.__setattr__(packed,"_storage",original)

    def test_compact_storage_scale_sourcefree(self):
        """Mechanical storage witness only; not original survey or native I03 timing."""
        import numpy as np
        import time
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"scale.sav"
            n=4000
            rng=np.random.default_rng(404)
            frame=pd.DataFrame({f"q{i}":rng.integers(0,5,n) for i in range(64)})
            frame.insert(0,"country",np.tile([1,2],n//2))
            pyreadstat.write_sav(frame,str(src))
            with decode_sav(src) as inc:
                key=next(inc.iter_native_column("country")).raw_value
                start=time.monotonic()
                receipt=build_country(inc,country_variable="country",country_value=key,
                    output=p/"one.sqlite",require_current=lambda:None)
                elapsed=time.monotonic()-start
                self.assertEqual(receipt.country_rows,n//2)
            cells=receipt.country_rows*65
            with CountryReader(p/"one.sqlite",receipt,require_current=lambda:None) as reader:
                self.assertEqual(len(tuple(reader.row_ordinals())),n//2)
                self.assertEqual(reader.db.execute("SELECT count(*) FROM lanes").fetchone()[0],130)
            # A deliberately generous bound for this low-cardinality synthetic
            # shape; no blanket claim for text/high-cardinality original data.
            self.assertLess(receipt.bytes,8*cells)
            print("COUNTRY_NUMERIC_SCALE_FIXTURE",cells,"country_db_bytes",receipt.bytes,
                  "original_full_wave_sav_bytes",src.stat().st_size,"build_seconds",round(elapsed,4))


    def test_bounded_group_scan_matches_sequential_and_operator_resume(self):
        from unittest.mock import patch
        from rawlsing_next.pre553_country_numeric_carrier import (
            build_country_set,country_workspace_status,CountryReceipt)
        from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
        from dataclasses import asdict
        import json
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"three.sav";one=p/"one";many=p/"many"
            one.mkdir();many.mkdir()
            pyreadstat.write_sav(pd.DataFrame({"country":[1,2,3,1,2,3,None],
                  "q":[0,1,2,3,4,5,6],"text":["a","b","c","a","c","b","held"]}),str(src))
            with decode_sav(src) as inc:
                serial=list(build_country_set(inc,country_variable="country",root=one,
                    require_current=lambda:True,max_open_countries=1,block_rows=2))
                progress=[]
                calls=[]
                original=PhysicalSourceIncidence.iter_countries_cells
                def counted(self,*args,**kwargs):
                    calls.append(1)
                    yield from original(self,*args,**kwargs)
                with patch.object(PhysicalSourceIncidence,"iter_countries_cells",counted):
                    grouped=list(build_country_set(inc,country_variable="country",root=many,
                        require_current=lambda:True,max_open_countries=4,block_rows=2,
                        on_progress=progress.append))
                self.assertEqual(len(calls),1)
                self.assertEqual(progress[0]["held_rows"],1)
                self.assertEqual(sum(x["phase"]=="SOURCE_SCAN" for x in progress),1)
                self.assertEqual([r for _,r in serial],[r for _,r in grouped])
                # Receipt custody belongs to the operator, not local hash inference.
                receipts=tuple(CountryReceipt(**json.loads(json.dumps(asdict(r)))) for _,r in grouped)
                status=country_workspace_status(many,retained_receipts=receipts)
                self.assertEqual(len(status["pinned_present"]),3)
                self.assertEqual(status["unreceipted_final"],[])
                self.assertEqual(len(country_workspace_status(many)["unreceipted_final"]),3)
                self.assertEqual(list(build_country_set(inc,country_variable="country",root=many,
                    require_current=lambda:True,retained_receipts=receipts)),grouped)
                with self.assertRaises(CountryCarrierError):
                    list(build_country_set(inc,country_variable="country",root=many,
                        require_current=lambda:True))
                self.assertEqual(country_workspace_status(many,retained_receipts=receipts)["uncommitted_stage"],[])
                self.assertEqual([r for _,r in grouped],list(receipts))
