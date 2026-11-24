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
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"country.sqlite"
            rec=build_country(inc,country_variable="G",country_value="A",
                    output=path,require_current=lambda:None,block_rows=1)
            with CountryReader(path,rec,require_current=lambda:None) as reader:
                with self.assertRaises(CountryCarrierError):
                    reader.native_release(original)
                compact_repo,compact=reader.native_repository(subset,current_authorities=fx['authorities'])
                from rawlsing_next._pre553_c11_execution_view import _CompactPublicObjects
                self.assertIsInstance(compact.public_objects,_CompactPublicObjects)
                from rawlsing_next.pre553_country_numeric_carrier import _CountryEventBodies
                self.assertIsInstance(compact.public_objects.lane.bodies,_CountryEventBodies)
                self.assertEqual(compact.release_ref,direct.release_ref)
                self.assertEqual(compact.replay_manifest.ref,direct.replay_manifest.ref)
                self.assertEqual(tuple(x.ref for x in compact.public_objects),tuple(x.ref for x in direct.public_objects))
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
