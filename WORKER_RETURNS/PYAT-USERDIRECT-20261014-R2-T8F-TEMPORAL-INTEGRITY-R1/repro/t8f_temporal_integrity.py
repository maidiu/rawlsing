"""PYAT R2 T8F -- Content-verified native temporal product and historical values reader.

Repairs three T8R integrity REDs:
  1. Tampered delta accepted under stale product digest
  2. Tampered native category data accepted under stale digest
  3. Malformed as-of date raising bare ValueError instead of typed refusal

Immutable, content-addressed five-category native wave-fact registry.
Revalidates primitive data, receipt identity, comparison arithmetic,
source scope and historical publication availability.

Source-free. No original Afrobarometer/EE12/N8E issuer, no V3.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import date
from fractions import Fraction as F
from typing import Optional

GRADE = "SOURCEFREE_STANDALONE_ONLY"
SPECIAL = ("DK", "REFUSED", "MISSING", "NOT_ASKED")


class Refusal(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def require(ok, code):
    if not ok:
        raise Refusal(code)


def canonical(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: canonical(v) for k, v in sorted(x.items())}
    if isinstance(x, (list, tuple)):
        return [canonical(v) for v in x]
    return x


def digest(x):
    return hashlib.sha256(
        json.dumps(canonical(x), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class WaveFact:
    year: int
    field_start: str
    field_end: str
    publication: str
    question: str
    version: str
    refusal_code: int
    category_weights: tuple
    special_weights: tuple
    eligible_weight: F
    asked_weight: F
    native_category_codes: tuple = (0, 1, 2, 3, 4)
    national_weight: str = "WITHINWT_TEST_ONLY"
    country_selector: str = "GHA_NATIONAL_CITIZEN_18_PLUS_TEST_ONLY"
    population: str = "GHA_CITIZEN_18_PLUS_TEST_ONLY"
    variance: Optional[F] = F(1, 2500)
    variance_method: str = "HYPOTHETICAL_DESIGN_TEST_ONLY"
    sample_identity: str = "INDEPENDENT_CROSS_SECTION_TEST_ONLY"

    def content_hash(self) -> str:
        return digest({
            "year": self.year, "field_start": self.field_start, "field_end": self.field_end,
            "publication": self.publication, "question": self.question, "version": self.version,
            "refusal_code": self.refusal_code, "category_weights": self.category_weights,
            "special_weights": self.special_weights, "eligible_weight": self.eligible_weight,
            "asked_weight": self.asked_weight,
        })

    def validate(self):
        require(self.year in (2012, 2022), "UNOBSERVED_ANCHOR")
        expected = (
            ("Q43", "GHA_R5_2012_INSTRUMENT_TEST", 998, "2012-05-08", "2012-05-27", "2015-07-16")
            if self.year == 2012
            else ("Q31", "GHA_R9_2022_INSTRUMENT_TEST", 8, "2022-04-04", "2022-04-20", "2024-10-01")
        )
        require(
            (self.question, self.version, self.refusal_code, self.field_start, self.field_end, self.publication) == expected,
            "QUESTION_RELEASE_OR_CLOCK_MISMATCH",
        )
        require(
            len(self.category_weights) == 5 and all(isinstance(x, F) and x >= 0 for x in self.category_weights),
            "NATIVE_FIVE_CATEGORY_REQUIRED",
        )
        require(self.native_category_codes == (0, 1, 2, 3, 4), "NATIVE_CATEGORY_ZERO_MISSING")
        require(
            len(self.special_weights) == 4 and all(isinstance(x, F) and x >= 0 for x in self.special_weights),
            "NATIVE_SPECIALS_REQUIRED",
        )
        require(self.eligible_weight == self.asked_weight + self.special_weights[3], "ELIGIBLE_RISK_DENOMINATOR_MISMATCH")
        require(self.asked_weight == sum(self.category_weights) + sum(self.special_weights[:3]), "ASKED_DENOMINATOR_MISMATCH")
        require(self.national_weight == "WITHINWT_TEST_ONLY", "WRONG_WEIGHT_BASIS")
        require(self.country_selector == "GHA_NATIONAL_CITIZEN_18_PLUS_TEST_ONLY", "WRONG_NATIONAL_SELECTOR")
        require(self.population == "GHA_CITIZEN_18_PLUS_TEST_ONLY", "POPULATION_MISMATCH")
        require(self.sample_identity == "INDEPENDENT_CROSS_SECTION_TEST_ONLY", "FALSE_SAME_PERSON_OR_CIRCULAR_ESTIMATOR")
        require(
            self.variance is not None and isinstance(self.variance, F) and self.variance >= 0
            and self.variance_method == "HYPOTHETICAL_DESIGN_TEST_ONLY",
            "DESIGN_UNQUANTIFIED",
        )
        require(sum(self.category_weights) > 0, "ZERO_VALID_SUPPORT")
        return self


@dataclass(frozen=True)
class WaveFactRef:
    """Immutable, content-addressed reference to a wave fact."""
    ref_id: str
    content_hash: str
    year: int


class WaveFactRegistry:
    """Immutable, defensive-copy, content-addressed wave-fact registry."""

    def __init__(self):
        self._facts: dict[str, WaveFact] = {}
        self._hashes: dict[str, str] = {}

    def register(self, fact: WaveFact) -> WaveFactRef:
        fact.validate()
        h = fact.content_hash()
        ref_id = f"WFACT-{fact.year}-{h[:12]}"
        self._facts[ref_id] = fact
        self._hashes[ref_id] = h
        return WaveFactRef(ref_id=ref_id, content_hash=h, year=fact.year)

    def retrieve(self, ref: WaveFactRef) -> WaveFact:
        require(ref.ref_id in self._facts, "UNKNOWN_FACT_REF")
        stored = self._facts[ref.ref_id]
        require(stored.content_hash() == ref.content_hash, "FACT_HASH_MISMATCH")
        require(self._hashes[ref.ref_id] == ref.content_hash, "REGISTRY_HASH_DRIFT")
        return stored

    def revalidate(self, ref: WaveFactRef) -> bool:
        fact = self.retrieve(ref)
        fact.validate()
        return fact.content_hash() == ref.content_hash


def compare(a: WaveFact, b: WaveFact, *, ee12="TEST_DOUBLE_ONLY", asof="2025-01-01", historical_year=2022):
    require(ee12 == "TEST_DOUBLE_ONLY", "UNISSUED_EE12")
    a.validate()
    b.validate()
    require((a.year, b.year) == (2012, 2022), "TEMPORAL_INVERSION")
    require(a.population == b.population, "POPULATION_MISMATCH")
    require(historical_year in (2012, 2017, 2022), "HISTORICAL_TIME_UNAUTHORIZED")
    try:
        asof_date = date.fromisoformat(asof)
    except (ValueError, TypeError):
        raise Refusal("INVALID_ASOF_DATE")
    require(asof_date >= date.fromisoformat(b.publication), "HISTORICAL_ASOF_BEFORE_RELEASE")

    def fact_dict(w):
        den = sum(w.category_weights)
        return {
            "year": w.year,
            "field": [w.field_start, w.field_end],
            "publication": w.publication,
            "question": w.question,
            "version": w.version,
            "categories": dict(zip(["0", "1", "2", "3", "4"], w.category_weights)),
            "specials": dict(zip(SPECIAL, w.special_weights)),
            "refusal_native_code": w.refusal_code,
            "eligible_weight": w.eligible_weight,
            "asked_weight": w.asked_weight,
            "valid_weight": den,
            "satisfied_share": (w.category_weights[3] + w.category_weights[4]) / den,
            "variance": w.variance,
            "variance_method": w.variance_method,
            "population": w.population,
            "weight_basis": w.national_weight,
        }

    p, q = fact_dict(a), fact_dict(b)
    out = {
        "grade": GRADE,
        "issued_EE12": False,
        "measured_original_data": False,
        "fixture_authorization": "TEST_DOUBLE_ONLY_NOT_ISSUED",
        "time_order": [2012, 2022],
        "query_asof": asof,
        "historical_requested": historical_year,
        "historical_intervening": "UNKNOWN_UNOBSERVED_GAP" if historical_year == 2017 else "NATIVE_ANCHOR_ONLY",
        "earlier": p,
        "later": q,
        "delta_later_minus_earlier": q["satisfied_share"] - p["satisfied_share"],
        "variance_delta_independent": p["variance"] + q["variance"],
        "design_uncertainty": "HYPOTHETICAL_DESIGN_TEST_ONLY__NOT_ACTUAL_SURVEY_SE",
        "N8S": "NOT_APPLICABLE_SUBJECTIVE_REPORTS",
        "product_digest": None,
    }
    out["product_digest"] = digest(out)
    return out


def consume(product, *, asof="2025-01-01", claim_same_person=False, selected_context="HISTORICAL_ATTITUDE_ONLY"):
    require(not claim_same_person, "FALSE_SAME_PERSON_INFERENCE")
    require(selected_context == "HISTORICAL_ATTITUDE_ONLY", "N8S_OR_CAUSAL_LAUNDERING")
    require(product["grade"] == GRADE and product["issued_EE12"] is False, "UNAUTHORIZED_EVIDENCE_GRADE")

    recomputed = dict(product)
    stored_digest = recomputed.pop("product_digest", None)
    recomputed["product_digest"] = None
    actual_digest = digest(recomputed)
    require(stored_digest == actual_digest, "PRODUCT_DIGEST_MISMATCH")

    require(asof == product["query_asof"], "MIXED_ASOF_POLICY")
    try:
        asof_date = date.fromisoformat(asof)
    except (ValueError, TypeError):
        raise Refusal("INVALID_ASOF_DATE")
    require(asof_date >= date.fromisoformat(product["later"]["publication"]), "HISTORICAL_ASOF_BEFORE_RELEASE")

    for side in ("earlier", "later"):
        cats = product[side]["categories"]
        expected_share = (cats.get("3", F(0)) + cats.get("4", F(0))) / sum(cats.values())
        require(
            product[side]["satisfied_share"] == expected_share,
            f"SATISFIED_SHARE_ARITHMETIC_MISMATCH_{side.upper()}",
        )

    reads = {
        "earlier": product["earlier"],
        "later": product["later"],
        "delta": product["delta_later_minus_earlier"],
        "variance_delta": product["variance_delta_independent"],
    }
    return {
        "consumer": "STANDALONE_HISTORICAL_ASOF_TEST_READER__NOT_REAL_N9",
        "grade": GRADE,
        "query_asof": asof,
        "historical_requested": product["historical_requested"],
        "historical_intervening": product["historical_intervening"],
        "values_read": reads,
        "values_read_digest": digest(reads),
        "selected_numeric_temporal_value": reads["delta"],
    }


def fixtures():
    a = WaveFact(
        2012, "2012-05-08", "2012-05-27", "2015-07-16", "Q43", "GHA_R5_2012_INSTRUMENT_TEST", 998,
        tuple(F(x) for x in (10, 20, 25, 30, 15)), tuple(F(x) for x in (3, 2, 1, 4)), F(110), F(106),
    )
    b = WaveFact(
        2022, "2022-04-04", "2022-04-20", "2024-10-01", "Q31", "GHA_R9_2022_INSTRUMENT_TEST", 8,
        tuple(F(x) for x in (8, 15, 30, 35, 22)), tuple(F(x) for x in (2, 3, 1, 4)), F(120), F(116),
    )
    return a, b
