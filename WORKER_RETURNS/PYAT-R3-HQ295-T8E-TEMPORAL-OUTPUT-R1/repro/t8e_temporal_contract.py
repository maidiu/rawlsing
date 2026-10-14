#!/usr/bin/env python3
"""T8E independent SOURCE-FREE executable contract specification.

Stdlib only. Imports NO Rawlsing owner. Never reads SAV/DTA. Never issues EE12,
constructs an N8E product, or calls an N9 implementation. Its positive output
is a fixture-only arithmetic/retention demonstration, NOT observed history.
Run: python3 -m unittest -v WORKER_RETURNS/.../repro/test_t8e_temporal_contract.py
Or: python3 WORKER_RETURNS/.../repro/t8e_temporal_contract.py
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
import json
import unittest

CONTRACT = "PYAT_HQ295_T8E_SOURCEFREE_ONLY@1"
CANDIDATE_PAIR_GRAPH_SHA = "8870545724d2b3353e4cb4125bc06c041d463954"
CANDIDATE_COUNT = 63
EXPECTED_GHANA_VALID = ("0", "1", "2", "3", "4")

def exact_fraction(text: str) -> Fraction:
    return Fraction(text)

def seal(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass(frozen=True)
class NativeFixture:
    source_id: str
    year: int
    item: str
    source_sha256: str
    population: str
    response_map: tuple[tuple[str, str], ...]
    valid_codes: tuple[str, ...]
    missing_codes: tuple[str, ...]
    cell_mass: tuple[tuple[str, str], ...]
    asked_risk_ref: str
    respondent_frame: str
    design_ref: str
    status: str = "SOURCEFREE_FIXTURE_ONLY"

    def validated(self):
        assert self.status == "SOURCEFREE_FIXTURE_ONLY"
        assert self.source_id and self.item and self.asked_risk_ref and self.design_ref
        assert len(self.source_sha256) == 64 and all(c in "0123456789abcdef" for c in self.source_sha256)
        codes = [code for code, _ in self.response_map]
        assert len(codes) == len(set(codes))
        assert set(self.valid_codes).isdisjoint(self.missing_codes)
        assert set(self.valid_codes) | set(self.missing_codes) == set(codes)
        masses = dict(self.cell_mass)
        assert len(masses) == len(self.cell_mass) and set(masses) == set(codes)
        assert all(exact_fraction(m) >= 0 for m in masses.values())
        assert sum((exact_fraction(v) for v in masses.values()), Fraction()) == Fraction(1)
        assert sum((exact_fraction(masses[c]) for c in self.valid_codes), Fraction()) > 0
        return self

def ghana_a():
    return NativeFixture(
        "SRC02", 2012, "GHA Q43",
        "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
        "Ghana adult citizen national intended frame",
        (("0","respondent says Ghana is not a democracy"), ("1","not at all satisfied"),
         ("2","not very satisfied"), ("3","fairly satisfied"), ("4","very satisfied"),
         ("9","do not know"), ("998","refused")),
        EXPECTED_GHANA_VALID, ("9","998"),
        (("0","1/10"),("1","1/10"),("2","1/5"),("3","3/10"),
         ("4","1/5"),("9","1/20"),("998","1/20")),
        "TEST_RISK_2012", "TEST_INDEPENDENT_FRAME_2012", "TEST_UNISSUED_DESIGN_2012"
    )

def ghana_b():
    return NativeFixture(
        "SRC03", 2022, "GHA Q31",
        "3afcecd08d2f4b531a926d455a943084d9f71c1276b4f79475cb455243d3c7b651",
        "Ghana adult citizen national intended frame",
        (("0","respondent says Ghana is not a democracy"), ("1","not at all satisfied"),
         ("2","not very satisfied"), ("3","fairly satisfied"), ("4","very satisfied"),
         ("9","do not know"), ("8","refused")),
        EXPECTED_GHANA_VALID, ("9","8"),
        (("0","1/5"),("1","1/10"),("2","1/10"),("3","1/4"),
         ("4","1/4"),("9","1/20"),("8","1/20")),
        "TEST_RISK_2022", "TEST_INDEPENDENT_FRAME_2022", "TEST_UNISSUED_DESIGN_2022"
    )

def scientific_gate(a: NativeFixture, b: NativeFixture,
                    *, issued_source_facts: bool, issued_ee12: bool,
                    issued_measurement_invariance: bool,
                    issued_design_uncertainty: bool) -> str:
    """No boolean here is authority; flags encode prerequisite status in a TEST."""
    a.validated()
    b.validated()
    if a.source_id == b.source_id or a.year >= b.year:
        return "HOLD_DISTINCT_ORDERED_WAVE_IDENTITIES"
    if not issued_source_facts:
        return "HOLD_TWO_SEPARATELY_ISSUED_WAVE_FACTS"
    if a.population != b.population:
        return "HOLD_COMMON_POPULATION_ESTIMAND"
    if not issued_measurement_invariance:
        return "HOLD_NATIVE_MEASUREMENT_INVARIANCE"
    if not issued_design_uncertainty:
        return "HOLD_DESIGN_AND_UNCERTAINTY"
    if not issued_ee12:
        return "HOLD_SEPARATELY_COMPETENT_EE12"
    # No 'MEASURED' positive is obtainable from this fixture gate.
    return "HOLD_REAL_OWNER_AND_ISSUER_VERIFICATION__SOURCEFREE_ONLY"

def fixture_only_comparison(a: NativeFixture, b: NativeFixture, *, token: str):
    """Only demonstrative finite exact arithmetic; no original empirical claim."""
    if token != "T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY":
        raise PermissionError("test-only comparison; no source or EE12 warrant")
    a.validated()
    b.validated()
    if a.source_id == b.source_id or a.year >= b.year or a.population != b.population:
        raise ValueError("distinct chronologically ordered waves and exact common named population required")
    if a.valid_codes != b.valid_codes:
        raise ValueError("native substantive topology not equivalently declared")
    sa, sb = dict(a.cell_mass), dict(b.cell_mass)
    den_a = sum((exact_fraction(sa[c]) for c in a.valid_codes), Fraction())
    den_b = sum((exact_fraction(sb[c]) for c in b.valid_codes), Fraction())
    # This denominator is an explicitly declared TEST semantic, not a real estimand grant.
    mass_diff = {c: str(exact_fraction(sb[c]) / den_b - exact_fraction(sa[c]) / den_a)
                 for c in a.valid_codes}
    payload = {
        "contract": CONTRACT,
        "claim_grade": "SOURCEFREE_FIXTURE_DEMONSTRATION_NOT_MEASURED",
        "a": {"source_id":a.source_id,"year":a.year,"item":a.item,"sha":a.source_sha256},
        "b": {"source_id":b.source_id,"year":b.year,"item":b.item,"sha":b.source_sha256},
        "valid_codes": list(a.valid_codes),
        "missing_A": {c: sa[c] for c in a.missing_codes},
        "missing_B": {c: sb[c] for c in b.missing_codes},
        "category_delta_fixture": mass_diff,
        "respondent_join": False,
        "design_variance": None,
        "ee12_ref": None,
        "actual_n8e_product_ref": None,
        "actual_n9_read_ref": None,
        "n9_values_read_receipt": None,
        "consumer_state": "HOLD_N9_REAL_OWNER_NOT_PROVED",
        "observed_intermediate_years": [],
        "temporal_candidate_graph_size_preserved": CANDIDATE_COUNT,
        "temporal_candidate_graph_blob": CANDIDATE_PAIR_GRAPH_SHA
    }
    return dict(payload, fixture_hash=seal(payload))

def historical_read_request(year: int, a: NativeFixture, b: NativeFixture,
                            *, qualified_model_use: bool = False):
    """Specification only: no N9 reader exists in this module."""
    if year in (a.year,b.year):
        return "HOLD_N9_DEREFERENCE_AND_CURRENTNESS"
    if a.year < year < b.year:
        return "HOLD_MODELED_PRIOR_ISSUER_AND_N9" if qualified_model_use else "UNKNOWN_UNOBSERVED_GAP"
    return "UNKNOWN_OUTSIDE_WAVE_HORIZON"

class T8ESourceFreeCourt(unittest.TestCase):
    def setUp(self):
        self.a, self.b = ghana_a(), ghana_b()

    def test_native_semantics_separately_retained(self):
        self.a.validated(); self.b.validated()
        self.assertIn("0",self.a.valid_codes)
        self.assertIn("0",self.b.valid_codes)
        self.assertEqual(self.a.missing_codes,("9","998"))
        self.assertEqual(self.b.missing_codes,("9","8"))
        self.assertNotIn("0",self.a.missing_codes)

    def test_full_native_distribution_and_no_selected_binary(self):
        out=fixture_only_comparison(self.a,self.b,token="T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY")
        self.assertEqual(set(out["category_delta_fixture"]),set(EXPECTED_GHANA_VALID))
        self.assertEqual(out["category_delta_fixture"]["0"],"1/9")
        self.assertEqual(out["missing_A"]["998"],"1/20")
        self.assertEqual(out["missing_B"]["8"],"1/20")

    def test_replay_and_two_input_perturbation(self):
        before=fixture_only_comparison(self.a,self.b,token="T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY")
        same=fixture_only_comparison(self.a,self.b,token="T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY")
        self.assertEqual(before["fixture_hash"],same["fixture_hash"])
        m=list(self.b.cell_mass)
        m[0]=("0","1/4"); m[3]=("3","1/5") # net mass zero; still full distribution
        altered=fixture_only_comparison(self.a,replace(self.b,cell_mass=tuple(m)),
            token="T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY")
        self.assertNotEqual(before["fixture_hash"],altered["fixture_hash"])
        self.assertNotEqual(before["category_delta_fixture"]["0"],altered["category_delta_fixture"]["0"])

    def test_unissued_science_is_hold_not_null(self):
        state=scientific_gate(self.a,self.b,issued_source_facts=False,issued_ee12=False,
            issued_measurement_invariance=False,issued_design_uncertainty=False)
        self.assertEqual(state,"HOLD_TWO_SEPARATELY_ISSUED_WAVE_FACTS")

    def test_missing_design_and_relation(self):
        self.assertEqual(scientific_gate(self.a,self.b,issued_source_facts=True,issued_ee12=True,
            issued_measurement_invariance=True,issued_design_uncertainty=False),"HOLD_DESIGN_AND_UNCERTAINTY")
        self.assertEqual(scientific_gate(self.a,self.b,issued_source_facts=True,issued_ee12=False,
            issued_measurement_invariance=True,issued_design_uncertainty=True),"HOLD_SEPARATELY_COMPETENT_EE12")

    def test_flags_never_mint_real_positive(self):
        state=scientific_gate(self.a,self.b,issued_source_facts=True,issued_ee12=True,
            issued_measurement_invariance=True,issued_design_uncertainty=True)
        self.assertIn("SOURCEFREE_ONLY",state)

    def test_population_and_wave_order_guard(self):
        self.assertEqual(scientific_gate(self.b,self.a,issued_source_facts=True,issued_ee12=True,
            issued_measurement_invariance=True,issued_design_uncertainty=True),"HOLD_DISTINCT_ORDERED_WAVE_IDENTITIES")
        self.assertEqual(scientific_gate(self.a,replace(self.b,population="different frame"),
            issued_source_facts=True,issued_ee12=True,issued_measurement_invariance=True,
            issued_design_uncertainty=True),"HOLD_COMMON_POPULATION_ESTIMAND")

    def test_permission_not_string(self):
        with self.assertRaises(PermissionError):
            fixture_only_comparison(self.a,self.b,token="ISSUED_EE12")

    def test_nonresponse_and_category_loss_hostiles(self):
        with self.assertRaises(AssertionError):
            replace(self.a,valid_codes=("1","2","3","4")).validated()
        with self.assertRaises(AssertionError):
            replace(self.a,cell_mass=tuple(x for x in self.a.cell_mass if x[0]!="998")).validated()

    def test_year_2017_is_never_measured(self):
        self.assertEqual(historical_read_request(2017,self.a,self.b),"UNKNOWN_UNOBSERVED_GAP")
        self.assertEqual(historical_read_request(2017,self.a,self.b,qualified_model_use=True),
                         "HOLD_MODELED_PRIOR_ISSUER_AND_N9")
        self.assertEqual(historical_read_request(2012,self.a,self.b),
                         "HOLD_N9_DEREFERENCE_AND_CURRENTNESS")

    def test_no_actual_world_or_actor_positive(self):
        out=fixture_only_comparison(self.a,self.b,token="T8E_SOURCEFREE_FIXTURE_NOT_AN_AUTHORITY")
        self.assertIsNone(out["actual_n8e_product_ref"])
        self.assertIsNone(out["actual_n9_read_ref"])
        self.assertIsNone(out["n9_values_read_receipt"])
        self.assertEqual(out["claim_grade"],"SOURCEFREE_FIXTURE_DEMONSTRATION_NOT_MEASURED")
        self.assertFalse(out["respondent_join"])
        self.assertEqual(out["temporal_candidate_graph_size_preserved"],63)

if __name__=="__main__":
    unittest.main(verbosity=2)
