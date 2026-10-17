"""PYAT R18 T9B — inherited temporal engine and historically situated world consumer.

GRAIN: SOURCEFREE_SYNTHETIC. NOT a real EE12/EE14 source. NOT observed temporal
calibration. NOT V3. NOT a person.

The temporal primitives are INHERITED VERBATIM from the pinned V553 native module
(blob 5304b70f9f): `_interp`, `_pressure_band`, `_bounded_score` and the
three-state temporal key machine. This module adds only the consumer that reads a
historically situated world at an explicit clock.

Known-at discipline
-------------------
A source wave is admissible at a query clock ONLY if it was PUBLISHED at or before
that clock. A wave observed earlier but published later is future information and
is refused, never interpolated and never back-filled.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_NATIVE = Path(__file__).resolve().parent / "native"
if str(_NATIVE) not in sys.path:
    sys.path.insert(0, str(_NATIVE))

from data.ddm_build_copy import ddm_v553_temporal_pressure as V553  # noqa: E402

# ---- inherited verbatim, by identity ----
_interp = V553._interp
_pressure_band = V553._pressure_band
_bounded_score = V553._bounded_score

AUTHORIZED_SPARSE_TEMPORAL_KEY = V553.AUTHORIZED_SPARSE_TEMPORAL_KEY
PROBE_ONLY_TEMPORAL_KEY = V553.PROBE_ONLY_TEMPORAL_KEY
BLOCKED_TEMPORAL_KEY = V553.BLOCKED_TEMPORAL_KEY
ALLOWED_MULTI_WAVE_GRAINS = V553.ALLOWED_MULTI_WAVE_GRAINS

GRAIN = "structural_channel_exact"

METHOD_M0_HOLD = "M0_PIECEWISE_HOLD"
METHOD_M1_INTERP = "M1_LINEAR_INTERPOLATION"
METHOD_M2_BACKOFF = "M2_UNCERTAINTY_AWARE_BACKOFF"

T8F3_ASSIGNMENT = "8079f69778eb4a2e6f30b246e3ec445dc161ae15"


# ---------------------------------------------------------------------------
# Source-native wave records. Each carries observation year AND publication year.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Wave:
    wave_id: str
    source_family: str
    country: str
    instrument: str
    edition: str
    cohort: str
    observation_year: int
    published_year: int
    value: float
    revoked: bool = False
    archived_nonrenewed: bool = False

    def known_at(self, clock_year: int) -> bool:
        """A wave is knowable at a clock only if it was PUBLISHED by then."""
        return self.published_year <= clock_year and not self.revoked


@dataclass(frozen=True)
class TemporalCase:
    case_id: str
    country: str
    waves: tuple
    ruptures: tuple = ()
    target_year: int = 0
    instrument: str = "SYNTH_INSTRUMENT"
    cohort: str = "COHORT_ALL"
    harmonize_countries: bool = False


@dataclass
class TemporalValue:
    method: str
    value: float | None
    band: str | None
    uncertainty: str
    temporal_key: str
    basis_wave_ids: tuple
    detail: str = ""
    refused_code: str | None = None

    def as_dict(self) -> dict:
        return dict(method=self.method, value=self.value, band=self.band,
                    uncertainty=self.uncertainty, temporal_key=self.temporal_key,
                    basis_wave_ids=list(self.basis_wave_ids), detail=self.detail,
                    refused_code=self.refused_code)


def _admissible(waves: tuple, clock_year: int, *, instrument: str, cohort: str,
                country: str, retrospective: bool = False) -> tuple:
    """Admissibility depends on WHICH CLOCK QUESTION is being asked.

    AS_OF (retrospective=False) - "what was KNOWABLE in clock_year?"
      only waves PUBLISHED by clock_year. Note this makes two-sided interpolation
      structurally impossible: a right-hand anchor observed later is published
      later by construction.
    RETROSPECTIVE (retrospective=True) - "what does today's complete archive say
      happened at clock_year?" Valid-at (observation_year) governs, and any wave
      published after the clock is carried as a publication-lag flag so the value
      can never be presented as knowable at that time.
    """
    if retrospective:
        # archival read: the whole valid series is available, including waves
        # observed AFTER the clock; each such wave carries a publication-lag flag.
        ok = [w for w in waves
              if w.country == country and w.instrument == instrument
              and w.cohort == cohort
              and not w.revoked and not w.archived_nonrenewed]
    else:
        ok = [w for w in waves
              if w.country == country and w.instrument == instrument
              and w.cohort == cohort and not w.archived_nonrenewed
              and w.observation_year <= clock_year and w.known_at(clock_year)]
    return tuple(sorted(ok, key=lambda w: w.observation_year))


# ---------------------------------------------------------------------------
# The three inherited/candidate methods.
# ---------------------------------------------------------------------------

def _lag_caveat(tv, pub_lag):
    if not pub_lag or tv.value is None:
        return tv
    tv.uncertainty = tv.uncertainty + "|PUBLICATION_LAG:" + "+".join(pub_lag)
    tv.detail = tv.detail + "; wave(s) published AFTER the query clock"
    return tv


def harmonization_check(case: TemporalCase) -> tuple:
    """Refuse an explicit cross-geography/cross-cohort harmonization request.

    Silently narrowing to one country would hide a real incomparability, so an
    explicit multi-geography request is REFUSED instead.
    """
    countries = sorted({w.country for w in case.waves})
    if len(countries) > 1 and case.harmonize_countries:
        return (False, "NON_HARMONIZABLE_GEOMETRY",
                f"countries {countries} are not harmonizable under this contract")
    return (True, None, "")


def evaluate(case: TemporalCase, method: str, clock_year: int | None = None,
             retrospective: bool = False) -> TemporalValue:
    ok, code, why = harmonization_check(case)
    if not ok:
        return TemporalValue(method, None, None, "NON_HARMONIZABLE", BLOCKED_TEMPORAL_KEY, (),
                            why, refused_code=code)
    clock = case.target_year if clock_year is None else clock_year
    waves = _admissible(case.waves, clock, instrument=case.instrument,
                        cohort=case.cohort, country=case.country,
                        retrospective=retrospective)
    pub_lag = tuple(w.wave_id for w in waves if w.published_year > clock)

    if not waves:
        return TemporalValue(method, None, None, "NO_SUPPORT", BLOCKED_TEMPORAL_KEY, (),
                            "no source wave is admissible at this clock",
                            refused_code="NO_TEMPORAL_SUPPORT")

    # A registered rupture/cohort shift means the bracket straddles two different
    # populations. Interpolating ACROSS it would fabricate a smooth measurement of a
    # discontinuity, so the whole straddling bracket is refused.
    ruptured_bracket = any(waves[0].observation_year <= r <= waves[-1].observation_year
                           for r in case.ruptures)
    post_rupture_only = bool(case.ruptures) and waves[0].observation_year > max(case.ruptures)

    if method == METHOD_M0_HOLD:
        prior = [w for w in waves if w.observation_year <= clock]
        if not prior:
            return TemporalValue(method, None, None, "BEFORE_FIRST_OBSERVATION",
                                 PROBE_ONLY_TEMPORAL_KEY, (),
                                 "query precedes every known-at wave",
                                 refused_code="NO_PRIOR_KNOWN_AT_WAVE")
        latest = prior[-1]
        return _lag_caveat(TemporalValue(method, _bounded_score(latest.value), _pressure_band(latest.value),
                             "HELD_NO_INTERPOLATION", AUTHORIZED_SPARSE_TEMPORAL_KEY,
                             (latest.wave_id,), "nearest prior admissible anchor"), pub_lag)

    if method == METHOD_M1_INTERP:
        if ruptured_bracket and not post_rupture_only:
            return TemporalValue(method, None, None, "RUPTURE_WINDOW_NO_SMOOTH_INTERPOLATION",
                                 BLOCKED_TEMPORAL_KEY, tuple(w.wave_id for w in waves),
                                 "bracket straddles a registered rupture/cohort shift; "
                                 "interpolation would fabricate a smooth measurement",
                                 refused_code="RUPTURE_BRACKET_REFUSED")
        left = [w for w in waves if w.observation_year <= clock]
        right = [w for w in waves if w.observation_year > clock]
        if not left:
            return TemporalValue(method, None, None, "BEFORE_FIRST_OBSERVATION",
                                 PROBE_ONLY_TEMPORAL_KEY, (),
                                 "no left anchor", refused_code="NO_LEFT_ANCHOR")
        if not right:
            lo = left[-1]
            return _lag_caveat(TemporalValue(method, _bounded_score(lo.value), _pressure_band(lo.value),
                                 "TERMINAL_NO_RIGHT_ANCHOR", AUTHORIZED_SPARSE_TEMPORAL_KEY,
                                 (lo.wave_id,), "no later anchor; hold last known-at value"), pub_lag)
        lo, hi = left[-1], right[0]
        span = hi.observation_year - lo.observation_year
        frac = (clock - lo.observation_year) / span if span else 0.0
        val = _bounded_score(_interp(lo.value, hi.value, frac))
        return _lag_caveat(TemporalValue(method, val, _pressure_band(val),
                             "INTERPOLATED_NOT_OBSERVED", PROBE_ONLY_TEMPORAL_KEY,
                             (lo.wave_id, hi.wave_id),
                             "linear interpolation inside an authorized gap; not a measurement"), pub_lag)

    if method == METHOD_M2_BACKOFF:
        prior = [w for w in waves if w.observation_year <= clock]
        if not prior:
            return TemporalValue(method, None, None, "NO_SUPPORT", BLOCKED_TEMPORAL_KEY, (),
                                 "no known-at support", refused_code="NO_TEMPORAL_SUPPORT")
        latest = prior[-1]
        later = [w for w in waves if w.observation_year > clock]
        gap = (later[0].observation_year - latest.observation_year) if later else None
        unc = ("BACKOFF_SINGLE_ANCHOR" if gap is None
               else ("BACKOFF_SHORT_GAP" if gap <= 2 else "BACKOFF_WIDE_GAP_UNCERTAIN"))
        return _lag_caveat(TemporalValue(method, _bounded_score(latest.value), _pressure_band(latest.value),
                             unc, AUTHORIZED_SPARSE_TEMPORAL_KEY, (latest.wave_id,),
                             "uncertainty-aware nearest-anchor backoff"), pub_lag)

    raise ValueError("unknown temporal method " + method)


# ---------------------------------------------------------------------------
# Historically situated selected-world consumer.
# Structural/access world is held CONSTANT; only the temporal channel moves.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StructuralWorld:
    world_id: str
    structural_routes: tuple          # constant across both historical clocks
    access_grants: tuple             # constant across both historical clocks
    institution: str


@dataclass
class OpportunitySet:
    query_clock: int
    temporal_method: str
    opportunity_ids: tuple
    pressure_band: str | None
    temporal_key: str
    uncertainty: str
    basis_wave_ids: tuple
    provenance: dict
    refused_code: str | None = None

    def as_dict(self) -> dict:
        return dict(query_clock=self.query_clock, temporal_method=self.temporal_method,
                    opportunity_ids=list(self.opportunity_ids),
                    pressure_band=self.pressure_band, temporal_key=self.temporal_key,
                    uncertainty=self.uncertainty, basis_wave_ids=list(self.basis_wave_ids),
                    provenance=self.provenance, refused_code=self.refused_code)


# Band -> which lawful structural routes are actually OPEN at that historical clock.
_BAND_ROUTES = {
    "high": ("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION"),
    "medium": ("ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
    "low": ("ROUTE_DEFERRED_REVIEW",),
    "none": ("ROUTE_BLOCKED_NO_SUPPORT",),
}


def read_selected_world(structural: StructuralWorld, case: TemporalCase,
                        method: str, clock_year: int, retrospective: bool = False) -> OpportunitySet:
    """Read a permission-valid historical opportunity set for ONE young person.

    The structural and access world is held fixed. Only the temporal channel,
    evaluated at the historical clock, selects which routes are open.
    """
    tv = evaluate(case, method, clock_year=clock_year, retrospective=retrospective)
    routes = structural.structural_routes
    if tv.refused_code is not None or tv.value is None:
        opened = ("ROUTE_BLOCKED_NO_SUPPORT",)
    else:
        allowed = _BAND_ROUTES.get(tv.band or "none", ("ROUTE_BLOCKED_NO_SUPPORT",))
        opened = tuple(r for r in routes if r in allowed)
    return OpportunitySet(
        query_clock=clock_year, temporal_method=method,
        opportunity_ids=opened, pressure_band=tv.band, temporal_key=tv.temporal_key,
        uncertainty=tv.uncertainty, basis_wave_ids=tv.basis_wave_ids,
        refused_code=tv.refused_code,
        provenance=dict(
            world_id=structural.world_id, institution=structural.institution,
            access_grants=list(structural.access_grants),
            grain=GRAIN, source_family=case.waves[0].source_family if case.waves else "",
            instrument=case.instrument, cohort=case.cohort, country=case.country,
            edition=case.waves[0].edition if case.waves else "",
            query_clock=clock_year,
            clock_question="RETROSPECTIVE_ARCHIVAL" if retrospective else "AS_OF_KNOWABLE",
            publication_lag_wave_ids=list(pub_lag_of(tv)),
            synthetic=True, observed_temporal_calibration=False,
            t8f3_assignment_preserved=T8F3_ASSIGNMENT,
        ),
    )


def pub_lag_of(tv):
    """Wave ids flagged as published after the query clock, if any."""
    if tv.value is None or "|PUBLICATION_LAG:" not in tv.uncertainty:
        return ()
    return tuple(tv.uncertainty.split("|PUBLICATION_LAG:")[1].split("+"))


def structurally_identical(a: OpportunitySet, b: OpportunitySet) -> bool:
    """Structural/access world must be provably unchanged between two clocks."""
    return (a.provenance["world_id"] == b.provenance["world_id"]
            and a.provenance["access_grants"] == b.provenance["access_grants"]
            and a.provenance["institution"] == b.provenance["institution"]
            and a.provenance["grain"] == b.provenance["grain"])


def materially_different(a: OpportunitySet, b: OpportunitySet) -> bool:
    return a.opportunity_ids != b.opportunity_ids