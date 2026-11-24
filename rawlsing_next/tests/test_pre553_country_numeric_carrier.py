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
