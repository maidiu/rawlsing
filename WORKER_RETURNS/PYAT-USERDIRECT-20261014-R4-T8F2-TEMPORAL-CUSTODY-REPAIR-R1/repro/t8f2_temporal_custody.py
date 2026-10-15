"""PYAT R4 T8F2 -- Immutable wave-fact custody and rederiving historical consumer.

Repairs all ten T8I REDs against T8F:
  R1 variance-only change collides identity / overwrites old fact
  R2 (same root cause class: claim fields outside digest)
  R3 forged WaveFactRef.year accepted
  R4 (strict ref schema; frozen dataclass + explicit check)
  R5 mutable list alias corrupts registered fact
  R6 self-resigned forged delta accepted
  R7 self-resigned forged variance delta accepted
  R8 coherent source rewrite without verified refs accepted
  R9 forged historical publication accepted
  R10 rewritten eligible risk accepted
  + native category-0 omission refused

Design: content_hash covers ALL scientifically relevant WaveFact fields;
registry normalizes to immutable tuples at registration, refuses overwrite
of a ref_id by different content, and binds ref.year/source/version;
consume_registered() dereferences two independently stored immutable refs
from a caller-supplied trusted registry and recomputes every primitive
(5-category + 4-special arithmetic, asked/eligible risk, satisfied shares,
delta, independent variance) plus authoritative publication clock, asof,
revocation and category-0 presence. Never trusts a caller digest alone.
Test-only trusted registry authority; never real EE12.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import date
from fractions import Fraction as F
from typing import Optional

GRADE = "SOURCEFREE_STANDALONE_ONLY"
SPECIAL = ("DK", "REFUSED", "MISSING", "NOT_ASKED")
REGISTRY_AUTHORITY = "TEST_ONLY_TRUSTED_REGISTRY@1"

AUTHORITATIVE_PUBLICATIONS = {
    2012: "2015-07-16",
    2022: "2024-10-01",
}


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


def _freeze_seq(value):
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_seq(v) for v in value)
    if isinstance(value, dict):
        return {k: _freeze_seq(v) for k, v in value.items()}
    return value


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

    def __post_init__(self):
        object.__setattr__(self, "category_weights", _freeze_seq(self.category_weights))
        object.__setattr__(self, "special_weights", _freeze_seq(self.special_weights))
        object.__setattr__(self, "native_category_codes", _freeze_seq(self.native_category_codes))

    def content_hash(self) -> str:
        return digest({
            "year": self.year,
            "field_start": self.field_start,
            "field_end": self.field_end,
            "publication": self.publication,
            "question": self.question,
            "version": self.version,
            "refusal_code": self.refusal_code,
            "category_weights": self.category_weights,
            "special_weights": self.special_weights,
            "eligible_weight": self.eligible_weight,
            "asked_weight": self.asked_weight,
            "native_category_codes": self.native_category_codes,
            "national_weight": self.national_weight,
            "country_selector": self.country_selector,
            "population": self.population,
            "variance": self.variance,
            "variance_method": self.variance_method,
            "sample_identity": self.sample_identity,
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
            isinstance(self.category_weights, tuple) and len(self.category_weights) == 5
            and all(isinstance(x, F) and x >= 0 for x in self.category_weights),
            "NATIVE_FIVE_CATEGORY_REQUIRED",
        )
        require(tuple(self.native_category_codes) == (0, 1, 2, 3, 4), "NATIVE_CATEGORY_ZERO_MISSING")
        require(
            isinstance(self.special_weights, tuple) and len(self.special_weights) == 4
            and all(isinstance(x, F) and x >= 0 for x in self.special_weights),
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
    ref_id: str
    content_hash: str
    year: int
    source: str = ""
    version: str = ""


def _check_ref_schema(ref: WaveFactRef) -> None:
    require(isinstance(ref, WaveFactRef), "REF_SCHEMA_VIOLATION")
    require(isinstance(ref.ref_id, str) and ref.ref_id, "REF_SCHEMA_VIOLATION")
    require(isinstance(ref.content_hash, str) and len(ref.content_hash) == 64, "REF_SCHEMA_VIOLATION")
    require(ref.year in (2012, 2022), "REF_SCHEMA_VIOLATION")


class WaveFactRegistry:
    """Collision-safe immutable registry with revocation."""

    def __init__(self, authority: str = REGISTRY_AUTHORITY):
        self._authority = authority
        self._facts: dict[str, WaveFact] = {}
        self._hashes: dict[str, str] = {}
        self._revoked: set[str] = set()

    @property
    def authority(self) -> str:
        return self._authority

    def register(self, fact: WaveFact) -> WaveFactRef:
        fact.validate()
        h = fact.content_hash()
        ref_id = f"WFACT-{fact.year}-{h[:12]}"
        if ref_id in self._facts and self._hashes[ref_id] != h:
            raise Refusal("FACT_IDENTITY_COLLISION")
        if ref_id not in self._facts:
            self._facts[ref_id] = fact
            self._hashes[ref_id] = h
        return WaveFactRef(ref_id=ref_id, content_hash=h, year=fact.year,
                           source="GHA_TEST_ONLY", version=fact.version)

    def retrieve(self, ref: WaveFactRef) -> WaveFact:
        _check_ref_schema(ref)
        require(ref.ref_id in self._facts, "UNKNOWN_FACT_REF")
        stored = self._facts[ref.ref_id]
        require(stored.content_hash() == ref.content_hash, "FACT_HASH_MISMATCH")
        require(self._hashes[ref.ref_id] == ref.content_hash, "REGISTRY_HASH_DRIFT")
        require(stored.year == ref.year, "FACT_YEAR_MISMATCH")
        require(ref.ref_id not in self._revoked, "FACT_REVOKED")
        return stored

    def revalidate(self, ref: WaveFactRef) -> bool:
        fact = self.retrieve(ref)
        fact.validate()
        return fact.content_hash() == ref.content_hash

    def revoke(self, ref: WaveFactRef) -> None:
        _check_ref_schema(ref)
        require(ref.ref_id in self._facts, "UNKNOWN_FACT_REF")
        self._revoked.add(ref.ref_id)


def _fact_dict(w: WaveFact):
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


def compare_registered(registry: WaveFactRegistry, ref_a: WaveFactRef, ref_b: WaveFactRef,
                       *, ee12="TEST_DOUBLE_ONLY", asof="2025-01-01", historical_year=2022):
    require(ee12 == "TEST_DOUBLE_ONLY", "UNISSUED_EE12")
    a = registry.retrieve(ref_a)
    b = registry.retrieve(ref_b)
    require((a.year, b.year) == (2012, 2022), "TEMPORAL_INVERSION")
    require(a.population == b.population, "POPULATION_MISMATCH")
    require(historical_year in (2012, 2017, 2022), "HISTORICAL_TIME_UNAUTHORIZED")
    try:
        asof_date = date.fromisoformat(asof)
    except (ValueError, TypeError):
        raise Refusal("INVALID_ASOF_DATE")
    require(asof_date >= date.fromisoformat(b.publication), "HISTORICAL_ASOF_BEFORE_RELEASE")
    p, q = _fact_dict(a), _fact_dict(b)
    out = {
        "grade": GRADE,
        "issued_EE12": False,
        "measured_original_data": False,
        "fixture_authorization": "TEST_DOUBLE_ONLY_NOT_ISSUED",
        "registry_authority": registry.authority,
        "wave_refs": {"earlier": vars(ref_a), "later": vars(ref_b)},
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


def consume_registered(registry: WaveFactRegistry, product, *,
                       asof="2025-01-01", claim_same_person=False,
                       selected_context="HISTORICAL_ATTITUDE_ONLY"):
    require(not claim_same_person, "FALSE_SAME_PERSON_INFERENCE")
    require(selected_context == "HISTORICAL_ATTITUDE_ONLY", "N8S_OR_CAUSAL_LAUNDERING")
    require(product.get("grade") == GRADE and product.get("issued_EE12") is False, "UNAUTHORIZED_EVIDENCE_GRADE")
    require(product.get("registry_authority") == registry.authority, "UNVERIFIED_SOURCE_VALUE_OR_REF")
    refs = product.get("wave_refs") or {}
    require("earlier" in refs and "later" in refs, "UNVERIFIED_SOURCE_VALUE_OR_REF")
    ref_a = WaveFactRef(**{k: refs["earlier"][k] for k in ("ref_id", "content_hash", "year") if k in refs["earlier"]})
    ref_b = WaveFactRef(**{k: refs["later"][k] for k in ("ref_id", "content_hash", "year") if k in refs["later"]})
    a = registry.retrieve(ref_a)
    b = registry.retrieve(ref_b)
    recomputed = dict(product)
    stored_digest = recomputed.pop("product_digest", None)
    recomputed["product_digest"] = None
    require(stored_digest == digest(recomputed), "PRODUCT_DIGEST_MISMATCH")
    require(asof == product["query_asof"], "MIXED_ASOF_POLICY")
    try:
        asof_date = date.fromisoformat(asof)
    except (ValueError, TypeError):
        raise Refusal("INVALID_ASOF_DATE")
    for side, fact in (("earlier", a), ("later", b)):
        node = product[side]
        cats = node.get("categories", {})
        require(sorted(cats.keys()) == ["0", "1", "2", "3", "4"], "NATIVE_CATEGORY_ZERO_MISSING")
        require(node.get("refusal_native_code") == fact.refusal_code, "REFUSAL_CODE_MISMATCH")
        require(node.get("publication") == fact.publication, "SOURCE_PUBLICATION_CLOCK_MISMATCH")
        require(node.get("question") == fact.question and node.get("version") == fact.version,
                "QUESTION_RELEASE_OR_CLOCK_MISMATCH")
        for code, weight in zip(["0", "1", "2", "3", "4"], fact.category_weights):
            require(cats.get(code) == weight, "NATIVE_CATEGORY_VALUE_MISMATCH")
        for name, weight in zip(SPECIAL, fact.special_weights):
            require(node.get("specials", {}).get(name) == weight, "NATIVE_SPECIAL_VALUE_MISMATCH")
        require(node.get("eligible_weight") == fact.eligible_weight, "ELIGIBLE_RISK_DENOMINATOR_MISMATCH")
        require(node.get("asked_weight") == fact.asked_weight, "ASKED_DENOMINATOR_MISMATCH")
        den = sum(fact.category_weights)
        require(node.get("valid_weight") == den, "VALID_WEIGHT_MISMATCH")
        expected_share = (fact.category_weights[3] + fact.category_weights[4]) / den
        require(node.get("satisfied_share") == expected_share, f"SATISFIED_SHARE_ARITHMETIC_MISMATCH_{side.upper()}")
        require(node.get("variance") == fact.variance, "VARIANCE_VALUE_MISMATCH")
    p_share = (a.category_weights[3] + a.category_weights[4]) / sum(a.category_weights)
    q_share = (b.category_weights[3] + b.category_weights[4]) / sum(b.category_weights)
    require(product["delta_later_minus_earlier"] == q_share - p_share, "TEMPORAL_DELTA_ARITHMETIC_MISMATCH")
    require(product["variance_delta_independent"] == a.variance + b.variance, "VARIANCE_DELTA_ARITHMETIC_MISMATCH")
    require(product["later"]["publication"] == AUTHORITATIVE_PUBLICATIONS[b.year],
            "SOURCE_PUBLICATION_CLOCK_MISMATCH")
    require(product["earlier"]["publication"] == AUTHORITATIVE_PUBLICATIONS[a.year],
            "SOURCE_PUBLICATION_CLOCK_MISMATCH")
    require(asof_date >= date.fromisoformat(b.publication), "HISTORICAL_ASOF_BEFORE_RELEASE")
    reads = {
        "earlier": product["earlier"],
        "later": product["later"],
        "delta": product["delta_later_minus_earlier"],
        "variance_delta": product["variance_delta_independent"],
    }
    return {
        "consumer": "T8F2_REGISTERED_HISTORICAL_VALUES_READER__NOT_REAL_N9",
        "grade": GRADE,
        "query_asof": asof,
        "historical_requested": product["historical_requested"],
        "historical_intervening": product["historical_intervening"],
        "values_read": reads,
        "values_read_digest": digest(reads),
        "selected_numeric_temporal_value": reads["delta"],
        "registry_authority": registry.authority,
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
