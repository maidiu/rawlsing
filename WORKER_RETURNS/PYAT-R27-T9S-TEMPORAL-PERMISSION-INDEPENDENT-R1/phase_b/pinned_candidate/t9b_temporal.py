"""PYAT R27 T9D — temporal authority and provenance repair of the T9C adapter.

GRAIN: SOURCEFREE_SYNTHETIC. NOT a real EE12/EE14 source. NOT observed temporal
calibration. NOT V3. NOT a person. NOT a longitudinal cohort estimand.

LINEAGE
-------
T9B (`PYAT-R18-T9B-TEMPORAL-HISTORY-CONSUMER-R1/t9b_temporal.py`, author commit
edf3494b1b11cb71a78540aba950aa15da900c8a) aliased the three native V553 temporal
key constants. T9I (a2a7bdeda76aa008b3d620b01af71f7fd6efaaae) returned
RED_SOURCEFREE_TEMPORAL_CLOCK_CUSTODY_AND_CONSUMER with ten failed assertions in
seven defect classes. T9C (9a33c2dcaa7ac0d50606416ab965488c9782934b, repair
d6e062684ca34b99ee9713c8c0affa0ed5c27f25) repaired all ten and returned 52 own
positives. Independent T9R (299dbf0d3a54fa76e36e524c553662f60090fe72) then
returned RED/HOLD with seven post-inspection counterexamples and four
unavailable precommitted capability gates.

This module is the T9D continuation repair. It keeps everything T9C fixed (R1..
R7), the V553 primitives INHERITED BY IDENTITY, the three methods and their
exact arithmetic, and the historically honest AS_OF versus RETROSPECTIVE
distinction. It repairs exactly the remaining independent failures and nothing
else:

  T9D-1  UNUSED FUTURE CONTEXT AUTHORITY UPGRADE. Product permission is now
         determined per the actually USED basis at the clock, not per all
         supplied archive context. A held estimate whose used basis sits before
         the query clock is typed `HELD_ESTIMATE_NOT_OBSERVATION_AT_CLOCK` and
         can never carry the anchor group's AUTHORIZED status into a product
         authorization ("a held 1995 estimate is not a 1995 observation"). An
         interpolated stand-in stays `INTERPOLATED_NOT_OBSERVED`. Only a product
         that IS the observation at the query clock may present itself as an
         authorized observation product. `evaluate` continues to publish the
         NATIVE ANCHOR-GROUP verdict verbatim in `native_authorization` and
         `temporal_key` (source-side temporal grant); the CONSUMER product key
         in `read_selected_world` is the gated product status. The two are
         deliberately distinct.

  T9D-2  EMPTY ACTOR GRANTS. Native temporal source-grant and actor opportunity
         entitlement are now separate typed concepts. No permission-valid route
         opens without an actual present current independently provided actor
         grant (`access_grants` non-empty). Missing grant => held, never an open
         route; typed `actor_opportunity_entitlement` records the gate.

  T9D-3  PUBLICATION-LAG / RUPTURE IDENTITY. Basis lag, archive context and
         rupture qualifiers are now TYPED fields (`publication_lag_wave_ids`,
         `archive_context_wave_ids`, `rupture_crossed_year`). `pub_lag_of`
         returns the typed basis-lag field and never parses a rupture caveat as
         a fake source-wave identity.

  T9D-4  DUPLICATE WAVE IDS. Duplicate `wave_id` in the supplied series is
         REFUSED BEFORE any source/country filtering with
         `DUPLICATE_WAVE_ID_REFUSED`, and basis provenance is additionally bound
         to the exact selected wave objects (`basis_source_refs`), so a
         last-wins dictionary can never rebind product identity to an excluded
         input.

  T9D-5  ARCHIVAL KNOWN-AT / SOURCE-CURRENTNESS CAPABILITIES. Typed
         `archival_known_at_upper_year` (dated archive snapshot bound) and
         typed `SourceGrant` (source-family / edition / owner / currentness)
         caller metadata are now expressible. The presence of metadata is never
         itself a grant: it is CHECKED. A missing, mismatched, wrong-owner or
         non-current issuer claim returns explicit UNAVAILABLE
         (`SOURCE_GRANT_*` refusals); a wave published after an archival
         known-at bound is not knowable in that snapshot and produces explicit
         no-support. The adapter never synthesizes a production original issuer
         or a faked clearance.

Nothing here is granted: no real EE12 source pair, no national inference, no
OC05, no N11, no N12, no V3, no adoption, no N8E/N8S/N9 execution, no actor
exposure or remembered-exposure evidence.
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_NATIVE = Path(__file__).resolve().parent / "native"
if str(_NATIVE) not in sys.path:
    sys.path.insert(0, str(_NATIVE))

from data.ddm_build_copy import ddm_v553_temporal_pressure as V553  # noqa: E402

# ---- inherited verbatim, by identity (NOT reimplemented, NOT modified) ----
_interp = V553._interp
_pressure_band = V553._pressure_band
_bounded_score = V553._bounded_score

AUTHORIZED_SPARSE_TEMPORAL_KEY = V553.AUTHORIZED_SPARSE_TEMPORAL_KEY
PROBE_ONLY_TEMPORAL_KEY = V553.PROBE_ONLY_TEMPORAL_KEY
BLOCKED_TEMPORAL_KEY = V553.BLOCKED_TEMPORAL_KEY
ALLOWED_MULTI_WAVE_GRAINS = V553.ALLOWED_MULTI_WAVE_GRAINS

# R1: the NATIVE authorization machine is called, not aliased.
_native_authorize_v553_multi_wave_key = V553._authorize_v553_multi_wave_key

GRAIN = "structural_channel_exact"

METHOD_M0_HOLD = "M0_PIECEWISE_HOLD"
METHOD_M1_INTERP = "M1_LINEAR_INTERPOLATION"
METHOD_M2_BACKOFF = "M2_UNCERTAINTY_AWARE_BACKOFF"

T8F3_ASSIGNMENT = "8079f69778eb4a2e6f30b246e3ec445dc161ae15"

REFUSED_MISSING = "MISSING_OBSERVATION_NOT_ZERO"
REFUSED_BASIS_SOURCE_CONFLICT = "BASIS_SOURCE_CONFLICT"

# ---- T9D typed refusals / statuses ----
REFUSED_DUPLICATE_WAVE_ID = "DUPLICATE_WAVE_ID_REFUSED"
REFUSED_SOURCE_GRANT_MISSING = "SOURCE_GRANT_UNAVAILABLE_MISSING_ISSUER"
REFUSED_SOURCE_GRANT_MISMATCH = "SOURCE_GRANT_UNAVAILABLE_SOURCE_OR_EDITION_MISMATCH"
REFUSED_SOURCE_GRANT_NOT_CURRENT = "SOURCE_GRANT_UNAVAILABLE_NOT_CURRENT"
REFUSED_SOURCE_GRANT_WRONG_OWNER = "SOURCE_GRANT_UNAVAILABLE_WRONG_SOURCE_OWNER"
REFUSED_ARCHIVAL_NOT_KNOWN_AT = "ARCHIVAL_KNOWN_AT_BOUND_EXCEEDED"

# Product observation status (T9D-1).
PRODUCT_OBSERVED_AT_CLOCK = "OBSERVED_AT_CLOCK"
PRODUCT_HELD_NOT_AT_CLOCK = "HELD_ESTIMATE_NOT_OBSERVATION_AT_CLOCK"
PRODUCT_INTERPOLATED = "INTERPOLATED_NOT_OBSERVED"
PRODUCT_REFUSED = "REFUSED_NO_PRODUCT"

# Actor opportunity entitlement (T9D-2).
ENTITLEMENT_GRANTED = "GRANTED_BY_PRESENT_CURRENT_ACCESS_GRANT"
ENTITLEMENT_WITHHELD = "WITHHELD_NO_CURRENT_ACCESS_GRANT"


# ---------------------------------------------------------------------------
# Source-native wave records. Each carries observation year AND publication year,
# plus the upstream native-support evidence the authorization machine consumes.
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
    # --- R1: upstream native-support evidence. These are the CALLER'S declarations,
    # forwarded verbatim to the native authorizer; they are not themselves grants.
    native_packet_ids: tuple = ("SYNTHETIC_PACKET_PROVENANCE",)
    canonical_semantic_signature: str = "synthetic_semantic_signature"
    structural_dimension_status: str = "resolved"
    probe_ready_input_count: int = 1
    comparable_key_grain: str = GRAIN
    fact_lane: str = "temporal_fact"
    # --- R2: explicit observation-support status. "OBSERVED" or "MISSING".
    support_status: str = "OBSERVED"

    def known_at(self, clock_year: int) -> bool:
        """A wave is knowable at a clock only if it was PUBLISHED by then."""
        return self.published_year <= clock_year and not self.revoked


@dataclass(frozen=True)
class SourceGrant:
    """T9D-5: typed caller-supplied source-qualified issuer evidence.

    This is TEST-ONLY caller metadata describing an asserted issuer grant for a
    source-family/edition. The adapter NEVER infers authority from its presence:
    the claim is only ever CHECKED against the waves actually used as product
    basis. Missing, mismatched, wrong-owner or non-current claims return
    explicit UNAVAILABLE; no production original issuer or clearance is ever
    synthesized.
    """
    grant_source_family: str
    grant_edition: str
    grant_current: bool
    grant_source_owner: str = ""


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
    # R1/R6: the native verdict that produced temporal_key, published verbatim.
    native_authorization: dict = field(default_factory=dict)
    # R1: True only when the value is a measurement/hypothesis about an anchor,
    # never an interpolated stand-in for an unobserved year.
    not_observed: bool = False
    # R6: set when a carry crosses a registered rupture.
    rupture_qualified: bool = False
    # --- T9D typed provenance identities (T9D-3 / T9D-4 / T9D-1) ---
    # R7/T9D-3: publication lag over the BASIS waves only, as a typed field.
    publication_lag_wave_ids: tuple = ()
    # R7/T9D-3: post-clock archive inventory explicitly NOT product basis.
    archive_context_wave_ids: tuple = ()
    # R6/T9D-3: the registered rupture actually crossed by the carry.
    rupture_crossed_year: int | None = None
    # R2/T9D-3: admissible waves excluded as typed UNKNOWN (never zeros).
    missing_excluded_wave_ids: tuple = ()
    # T9D-4: (source_family, edition) of the exact wave objects used as basis.
    basis_source_refs: tuple = ()
    # T9D-1: is this product the OBSERVATION at the query clock, or a held /
    # interpolated estimate for a year that was not observed?
    product_observation_status: str = PRODUCT_REFUSED

    def as_dict(self) -> dict:
        return dict(method=self.method, value=self.value, band=self.band,
                    uncertainty=self.uncertainty, temporal_key=self.temporal_key,
                    basis_wave_ids=list(self.basis_wave_ids), detail=self.detail,
                    refused_code=self.refused_code,
                    native_authorization=self.native_authorization,
                    not_observed=self.not_observed,
                    rupture_qualified=self.rupture_qualified,
                    publication_lag_wave_ids=list(self.publication_lag_wave_ids),
                    archive_context_wave_ids=list(self.archive_context_wave_ids),
                    rupture_crossed_year=self.rupture_crossed_year,
                    missing_excluded_wave_ids=list(self.missing_excluded_wave_ids),
                    basis_source_refs=[list(r) for r in self.basis_source_refs],
                    product_observation_status=self.product_observation_status)


# ---------------------------------------------------------------------------
# R2: upstream native support validation. Runs BEFORE any numeric use.
# ---------------------------------------------------------------------------

def _observation_support(w: "Wave") -> tuple:
    """Validate that a wave really carries an observation.

    Returns (ok, refused_code). A declared-or-observed MISSING, a non-numeric, a
    NaN or an infinite value is NOT an observation. It is a typed unknown.
    """
    if w.support_status == "MISSING":
        return (False, REFUSED_MISSING)
    value = w.value
    if value is None:
        return (False, REFUSED_MISSING)
    if isinstance(value, bool) or isinstance(value, (str, bytes)):
        return (False, REFUSED_MISSING)
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return (False, REFUSED_MISSING)
    if math.isnan(numeric) or math.isinf(numeric):
        return (False, REFUSED_MISSING)
    return (True, None)


# ---------------------------------------------------------------------------
# R1: native-derived authorization, via the ORIGINAL native function.
# ---------------------------------------------------------------------------

_NATIVE_GROUP_COLUMNS = (
    "wave_id",
    "structural_dimension_status",
    "probe_ready_input_count",
    "source_v552j_packet_ids_json",
    "structural_pressure_value",
    "comparable_key_grain",
    "fallback_permission_profile_key",
    "source_v552_structural_fact_lane",
    "canonical_semantic_signature",
)


def native_authorization(anchor_waves: tuple) -> dict:
    """Call the ORIGINAL `_authorize_v553_multi_wave_key` on the anchor waves.

    The adapter supplies the harmonized-key, packet-provenance, resolved-dimension
    and probe-readiness inputs the native function requires. It does not decide the
    status itself: AUTHORIZED still requires harmonizer authority AND at least two
    distinct eligible anchors, exactly as native defines it.
    """
    import pandas as pd  # local import keeps module import cheap

    rows = []
    for w in anchor_waves:
        rows.append({
            "wave_id": w.wave_id,
            "structural_dimension_status": w.structural_dimension_status,
            "probe_ready_input_count": w.probe_ready_input_count,
            "source_v552j_packet_ids_json": json.dumps(list(w.native_packet_ids)),
            "structural_pressure_value": float(w.value),
            "comparable_key_grain": w.comparable_key_grain,
            "fallback_permission_profile_key": "",
            "source_v552_structural_fact_lane": w.fact_lane,
            "canonical_semantic_signature": w.canonical_semantic_signature,
        })
    group = pd.DataFrame(rows, columns=list(_NATIVE_GROUP_COLUMNS))
    if rows:
        report = {
            "ready_for_v553": True,
            "comparison_authority_status": "multi_wave_authorized",
            "shared_semantic_columns": ["SYNTH_SEMANTIC_COLUMN"],
            "shared_directionality_columns": ["SYNTH_DIRECTIONALITY_COLUMN"],
            "shared_position_columns": ["SYNTH_POSITION_COLUMN"],
        }
    else:
        report = {}
    return _native_authorize_v553_multi_wave_key(report, group)


def _resolved_key(native: dict, *, not_observed: bool) -> str:
    """Native may only DOWNGRADE. An unobserved year is never an authorized grant.

    The native gap-segment index preserves `unknown_gap_preserved` with
    `interpolation_allowed=false` even when `allow_interpolation=True`, so a
    stand-in for an unobserved year stays exploratory regardless of anchor count.
    """
    native_key = native.get("multi_wave_authorization_status", BLOCKED_TEMPORAL_KEY)
    if not_observed and native_key == AUTHORIZED_SPARSE_TEMPORAL_KEY:
        return PROBE_ONLY_TEMPORAL_KEY
    return native_key


def _admissible(waves: tuple, clock_year: int, *, instrument: str, cohort: str,
                country: str, retrospective: bool = False,
                archival_known_at_upper_year: int | None = None) -> tuple:
    """Admissibility depends on WHICH CLOCK QUESTION is being asked.

    AS_OF (retrospective=False) - "what was KNOWABLE in clock_year?"
      only waves PUBLISHED by clock_year. Note this makes two-sided interpolation
      structurally impossible: a right-hand anchor observed later is published
      later by construction.

    RETROSPECTIVE (retrospective=True) - "what does today's complete archive say
      happened at clock_year?" Valid-at (observation_year) governs, and any wave
      published after the clock is carried as publication-lag metadata so the value
      can never be presented as knowable at that time. The supplied archive is a
      CALLER PRECONDITION, not an authenticated dated snapshot.

    T9D-5: when the caller supplies `archival_known_at_upper_year` (a typed dated
    archive snapshot bound), a wave published after that bound is NOT knowable in
    that snapshot. Target valid time and archival snapshot known-at time are
    separate clocks; unpublished-in-snapshot support is excluded rather than
    silently treated as snapshot knowledge.
    """
    def in_snapshot(w) -> bool:
        if archival_known_at_upper_year is None:
            return True
        return w.published_year <= archival_known_at_upper_year

    if retrospective:
        # archival read: the whole valid series is available, including waves
        # observed AFTER the clock, bounded by the snapshot when one is declared.
        ok = [w for w in waves
              if w.country == country and w.instrument == instrument
              and w.cohort == cohort
              and not w.revoked and not w.archived_nonrenewed
              and in_snapshot(w)]
    else:
        ok = [w for w in waves
              if w.country == country and w.instrument == instrument
              and w.cohort == cohort and not w.archived_nonrenewed
              and w.observation_year <= clock_year and w.known_at(clock_year)
              and in_snapshot(w)]
    return tuple(sorted(ok, key=lambda w: w.observation_year))


# ---------------------------------------------------------------------------
# The three inherited/candidate methods.
# ---------------------------------------------------------------------------

def _qualifiers(tv, pub_lag, basis_ids, *, rupture=None, missing_excluded=()):
    """Attach basis-only lag, rupture qualification and missing-support disclosure.

    R7: pub_lag is computed over the BASIS waves only.
    R6: a rupture qualifier is appended, and the caller downgrades the key.
    R2: excluded non-supporting waves are named so a missing value is never
        silently indistinguishable from an absent one.

    T9D-3: the lag, rupture and missing identities are ALSO stored as TYPED
    fields. The uncertainty string remains human-readable disclosure; it is
    never the source of a wave identity, so a pipe-suffixed rupture caveat can
    no longer be parsed as a fake source-wave ID.
    """
    tv.publication_lag_wave_ids = tuple(pub_lag)
    tv.missing_excluded_wave_ids = tuple(missing_excluded)
    if pub_lag and tv.value is not None:
        tv.uncertainty = tv.uncertainty + "|PUBLICATION_LAG:" + "+".join(pub_lag)
        tv.detail = tv.detail + "; wave(s) published AFTER the query clock"
    if rupture is not None:
        tv.rupture_qualified = True
        tv.rupture_crossed_year = int(rupture)
        tv.uncertainty = (tv.uncertainty
                          + "|POST_RUPTURE_CARRY_HYPOTHETICAL:R" + str(rupture)
                          + "|IDENTIFIED_SET_UNBOUNDED:STABILITY_NOT_ASSUMED")
        tv.detail = (tv.detail + "; typed bounded hypothetical carry across a registered"
                     " rupture; the post-break cohort estimand is NOT identified and no"
                     " stability is assumed")
    if missing_excluded:
        tv.uncertainty = (tv.uncertainty + "|MISSING_SUPPORT_EXCLUDED:"
                          + "+".join(str(i) for i in missing_excluded))
        tv.detail = (tv.detail + "; wave(s) carrying no observation were excluded as"
                     " typed UNKNOWN, never as an observed zero")
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


def _basis_lag(basis_ids: tuple, waves: tuple, clock: int) -> tuple:
    """R7: publication lag over the BASIS waves only."""
    ids = set(basis_ids)
    return tuple(w.wave_id for w in waves
                 if w.wave_id in ids and w.published_year > clock)


def _wave_identity_check(case: TemporalCase) -> tuple:
    """T9D-4: duplicate wave IDs are refused BEFORE any source filtering.

    A reused wave id lets a last-wins lookup rebind product provenance to an
    excluded input. The whole series is rejected before country/source filters
    run, so exclusion order can never decide product identity.
    """
    seen = set()
    dupes = []
    for w in case.waves:
        if w.wave_id in seen and w.wave_id not in dupes:
            dupes.append(w.wave_id)
        seen.add(w.wave_id)
    if dupes:
        return (False, tuple(dupes))
    return (True, ())


def _held_or_observed(tv, basis: tuple, clock: int) -> "TemporalValue":
    """T9D-1: classify the product against the actually used basis at the clock.

    A product may be the OBSERVATION at the query clock only when its used basis
    is a wave observed exactly AT the clock and the value is not an interpolated
    stand-in. Otherwise it is a held estimate for an unobserved year and is
    typed accordingly: "a held 1995 estimate is not a 1995 observation".
    """
    if tv.not_observed or len(basis) > 1:
        tv.product_observation_status = PRODUCT_INTERPOLATED
    elif basis and basis[0].observation_year == clock:
        tv.product_observation_status = PRODUCT_OBSERVED_AT_CLOCK
    else:
        tv.product_observation_status = PRODUCT_HELD_NOT_AT_CLOCK
    return tv


def evaluate(case: TemporalCase, method: str, clock_year: int | None = None,
             retrospective: bool = False,
             archival_known_at_upper_year: int | None = None) -> TemporalValue:
    ok, code, why = harmonization_check(case)
    if not ok:
        return TemporalValue(method, None, None, "NON_HARMONIZABLE", BLOCKED_TEMPORAL_KEY, (),
                             why, refused_code=code)
    # T9D-4: duplicate identity refusal runs BEFORE source/country filtering.
    unique, dupes = _wave_identity_check(case)
    if not unique:
        return TemporalValue(
            method, None, None, "DUPLICATE_WAVE_IDENTITY", BLOCKED_TEMPORAL_KEY, (),
            "duplicate wave_id(s) " + repr(list(dupes)) + " in the supplied series; "
            "product identity must be a unique qualified mapping and cannot be "
            "decided by exclusion order",
            refused_code=REFUSED_DUPLICATE_WAVE_ID,
            native_authorization=native_authorization(()),
            product_observation_status=PRODUCT_REFUSED)
    clock = case.target_year if clock_year is None else clock_year
    admissible = _admissible(case.waves, clock, instrument=case.instrument,
                             cohort=case.cohort, country=case.country,
                             retrospective=retrospective,
                             archival_known_at_upper_year=archival_known_at_upper_year)

    # R2: upstream native support validation BEFORE any numeric use.
    waves = tuple(w for w in admissible if _observation_support(w)[0])
    missing_excluded = tuple(w.wave_id for w in admissible
                             if not _observation_support(w)[0])

    if not admissible:
        detail = "no source wave is admissible at this clock"
        code = "NO_TEMPORAL_SUPPORT"
        if archival_known_at_upper_year is not None:
            detail = ("no source wave is knowable inside the declared archival "
                      "known-at bound " + str(archival_known_at_upper_year) +
                      "; target valid time and archival snapshot known-at time "
                      "are separate clocks and no snapshot knowledge is synthesized")
            code = REFUSED_ARCHIVAL_NOT_KNOWN_AT
        return TemporalValue(method, None, None, "NO_SUPPORT", BLOCKED_TEMPORAL_KEY, (),
                             detail, refused_code=code,
                             product_observation_status=PRODUCT_REFUSED)
    if not waves:
        # Every admissible wave exists but none carries an observation. This is a
        # typed UNKNOWN, explicitly NOT an observed zero.
        return TemporalValue(method, None, None, "UNKNOWN_NOT_OBSERVED",
                             BLOCKED_TEMPORAL_KEY, (),
                             "admissible wave(s) carry no observation; this is an "
                             "explicit unknown and not an observed zero",
                             refused_code=REFUSED_MISSING,
                             native_authorization=native_authorization(()),
                             missing_excluded_wave_ids=missing_excluded,
                             product_observation_status=PRODUCT_REFUSED)

    # A registered rupture/cohort shift means the bracket straddles two different
    # populations. Interpolating ACROSS it would fabricate a smooth measurement of a
    # discontinuity, so the whole straddling bracket is refused.
    ruptured_bracket = any(waves[0].observation_year <= r <= waves[-1].observation_year
                           for r in case.ruptures)
    post_rupture_only = bool(case.ruptures) and waves[0].observation_year > max(case.ruptures)

    def carry(tv, basis_waves):
        """Finish a carry/hold result: R1 native key, R6 rupture, R2/R7 qualifiers.

        The native call is made over the whole QUALIFIED ANCHOR GROUP at this clock,
        which is how V553 itself uses `_authorize_v553_multi_wave_key` (per key group,
        not per method). Per-result qualifiers below can only ever DOWNGRADE that key.
        The NATIVE verdict is the SOURCE-SIDE temporal grant; the CONSUMER product
        authorization is gated separately in `read_selected_world` per the actually
        used basis at the clock and the actor entitlement (T9D-1/T9D-2).
        """
        basis_ids = tuple(w.wave_id for w in basis_waves)
        # T9D-4: provenance identity comes from the exact selected wave objects.
        tv.basis_wave_ids = basis_ids
        tv.basis_source_refs = tuple((w.source_family, w.edition) for w in basis_waves)
        native = native_authorization(waves)
        crossed = None
        if case.ruptures:
            prior = max((w.observation_year for w in basis_waves), default=None)
            if prior is not None:
                later = [r for r in case.ruptures if prior < r <= clock]
                if later:
                    crossed = max(later)
        if crossed is not None:
            # R6: never claim the post-break cohort estimand.
            tv.temporal_key = PROBE_ONLY_TEMPORAL_KEY
            tv.native_authorization = native
        else:
            tv.temporal_key = _resolved_key(native, not_observed=tv.not_observed)
            tv.native_authorization = native
        _held_or_observed(tv, basis_waves, clock)
        # R7/T9D-3: typed archive context = admissible waves NOT used as basis and
        # published after the clock. AS_OF admissible sets contain none by
        # construction, so this is empty for AS_OF reads.
        tv.archive_context_wave_ids = tuple(
            w.wave_id for w in waves
            if w.wave_id not in set(basis_ids) and w.published_year > clock)
        return _qualifiers(tv, _basis_lag(basis_ids, waves, clock), basis_ids,
                           rupture=crossed, missing_excluded=missing_excluded)

    if method == METHOD_M0_HOLD:
        prior = [w for w in waves if w.observation_year <= clock]
        if not prior:
            return TemporalValue(method, None, None, "BEFORE_FIRST_OBSERVATION",
                                 PROBE_ONLY_TEMPORAL_KEY, (),
                                 "query precedes every known-at wave",
                                 refused_code="NO_PRIOR_KNOWN_AT_WAVE",
                                 native_authorization=native_authorization(()),
                                 product_observation_status=PRODUCT_REFUSED)
        latest = prior[-1]
        return carry(TemporalValue(method, _bounded_score(latest.value),
                                   _pressure_band(latest.value),
                                   "HELD_NO_INTERPOLATION", BLOCKED_TEMPORAL_KEY,
                                   (),
                                   "nearest prior admissible anchor"),
                     (latest,))

    if method == METHOD_M1_INTERP:
        if ruptured_bracket and not post_rupture_only:
            return TemporalValue(method, None, None, "RUPTURE_WINDOW_NO_SMOOTH_INTERPOLATION",
                                 BLOCKED_TEMPORAL_KEY, tuple(w.wave_id for w in waves),
                                 "bracket straddles a registered rupture/cohort shift; "
                                 "interpolation would fabricate a smooth measurement",
                                 refused_code="RUPTURE_BRACKET_REFUSED",
                                 native_authorization=native_authorization(waves),
                                 product_observation_status=PRODUCT_REFUSED)
        left = [w for w in waves if w.observation_year <= clock]
        right = [w for w in waves if w.observation_year > clock]
        if not left:
            return TemporalValue(method, None, None, "BEFORE_FIRST_OBSERVATION",
                                 PROBE_ONLY_TEMPORAL_KEY, (),
                                 "no left anchor", refused_code="NO_LEFT_ANCHOR",
                                 native_authorization=native_authorization(()),
                                 product_observation_status=PRODUCT_REFUSED)
        if not right:
            lo = left[-1]
            return carry(TemporalValue(method, _bounded_score(lo.value),
                                       _pressure_band(lo.value),
                                       "TERMINAL_NO_RIGHT_ANCHOR", BLOCKED_TEMPORAL_KEY,
                                       (),
                                       "no later anchor; hold last known-at value"),
                         (lo,))
        lo, hi = left[-1], right[0]
        span = hi.observation_year - lo.observation_year
        frac = (clock - lo.observation_year) / span if span else 0.0
        val = _bounded_score(_interp(lo.value, hi.value, frac))
        # R1: an interpolated year is never an observation; mark it so the native
        # AUTHORIZED anchor count cannot upgrade it to an authorized grant.
        return carry(TemporalValue(method, val, _pressure_band(val),
                                   "INTERPOLATED_NOT_OBSERVED", BLOCKED_TEMPORAL_KEY,
                                   (),
                                   "linear interpolation inside an authorized gap; not a measurement",
                                   not_observed=True),
                     (lo, hi))

    if method == METHOD_M2_BACKOFF:
        prior = [w for w in waves if w.observation_year <= clock]
        if not prior:
            return TemporalValue(method, None, None, "NO_SUPPORT", BLOCKED_TEMPORAL_KEY, (),
                                 "no known-at support", refused_code="NO_TEMPORAL_SUPPORT",
                                 native_authorization=native_authorization(()),
                                 product_observation_status=PRODUCT_REFUSED)
        latest = prior[-1]
        later = [w for w in waves if w.observation_year > clock]
        gap = (later[0].observation_year - latest.observation_year) if later else None
        unc = ("BACKOFF_SINGLE_ANCHOR" if gap is None
               else ("BACKOFF_SHORT_GAP" if gap <= 2 else "BACKOFF_WIDE_GAP_UNCERTAIN"))
        return carry(TemporalValue(method, _bounded_score(latest.value),
                                   _pressure_band(latest.value),
                                   unc, BLOCKED_TEMPORAL_KEY, (),
                                   "uncertainty-aware nearest-anchor backoff"),
                     (latest,))

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
    # R5: a PROBE_ONLY/exploratory read never opens a claimed lawful route.
    authorized_opportunity: bool = False
    exploratory_route_ids: tuple = ()
    # R7: post-clock archive inventory that was NOT used as product basis.
    archive_context_wave_ids: tuple = ()
    # T9D-2: actor opportunity entitlement, distinct from the native temporal
    # source-grant recorded in provenance.
    actor_opportunity_entitlement: str = ENTITLEMENT_WITHHELD
    # T9D-1: the product's observation status at the query clock.
    product_observation_status: str = PRODUCT_REFUSED

    def as_dict(self) -> dict:
        return dict(query_clock=self.query_clock, temporal_method=self.temporal_method,
                    opportunity_ids=list(self.opportunity_ids),
                    pressure_band=self.pressure_band, temporal_key=self.temporal_key,
                    uncertainty=self.uncertainty, basis_wave_ids=list(self.basis_wave_ids),
                    provenance=self.provenance, refused_code=self.refused_code,
                    authorized_opportunity=self.authorized_opportunity,
                    exploratory_route_ids=list(self.exploratory_route_ids),
                    archive_context_wave_ids=list(self.archive_context_wave_ids),
                    actor_opportunity_entitlement=self.actor_opportunity_entitlement,
                    product_observation_status=self.product_observation_status)


# Band -> which lawful structural routes are actually OPEN at that historical clock.
_BAND_ROUTES = {
    "high": ("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION"),
    "medium": ("ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
    "low": ("ROUTE_DEFERRED_REVIEW",),
    "none": ("ROUTE_BLOCKED_NO_SUPPORT",),
}


def pub_lag_of(tv):
    """R7/T9D-3: wave ids flagged as published after the query clock, BASIS ONLY.

    Identity comes from the TYPED `publication_lag_wave_ids` field, never from
    parsing the disclosure string, so a pipe-suffixed rupture qualifier can not
    be swallowed as a fake source-wave ID.
    """
    typed = getattr(tv, "publication_lag_wave_ids", None)
    if typed is not None:
        return tuple(typed)
    if tv.value is None or "|PUBLICATION_LAG:" not in tv.uncertainty:
        return ()
    tail = tv.uncertainty.split("|PUBLICATION_LAG:", 1)[1]
    segment = tail.split("|", 1)[0]
    return tuple(segment.split("+"))


def archive_context_of(case: TemporalCase, tv: TemporalValue, clock_year: int,
                       retrospective: bool) -> tuple:
    """R7: post-clock archive inventory that is explicitly NOT product basis.

    T9D-3: identity comes from the TYPED field captured at evaluation time (over
    the same admissible set the product actually saw, including any declared
    archival known-at bound). The legacy recomputation is a fallback only.
    """
    typed = getattr(tv, "archive_context_wave_ids", None)
    if typed is not None:
        return tuple(typed)
    if not retrospective:
        return ()
    admissible = _admissible(case.waves, clock_year, instrument=case.instrument,
                             cohort=case.cohort, country=case.country,
                             retrospective=True)
    basis = set(tv.basis_wave_ids)
    return tuple(w.wave_id for w in admissible
                 if w.wave_id not in basis and w.published_year > clock_year)


def basis_source_refs(case: TemporalCase, tv: TemporalValue) -> tuple:
    """R3/T9D-4: the exact (source_family, edition) of the waves actually used.

    The typed `basis_source_refs` captured from the exact selected wave objects
    is authoritative. The legacy ID lookup is retained only as a unique-qualified
    fallback and never lets a last-wins dictionary rebind identity to an excluded
    input.
    """
    typed = getattr(tv, "basis_source_refs", None)
    if typed:
        return tuple(typed)
    by_id = {}
    for w in case.waves:
        if w.wave_id not in by_id:
            by_id[w.wave_id] = w
    refs = tuple((by_id[i].source_family, by_id[i].edition)
                 for i in tv.basis_wave_ids if i in by_id)
    return refs


def check_source_grant(grant, refs: tuple) -> str | None:
    """T9D-5: CHECK a claimed source-qualified issuer grant against the basis.

    Returns None when the claim actually covers the used basis, otherwise one of
    the typed `SOURCE_GRANT_UNAVAILABLE_*` refusals. The presence of metadata is
    never itself a grant: owner, edition and currentness are all verified, and a
    missing issuer claim is UNAVAILABLE, never a synthesized clearance.
    """
    if grant is None:
        return REFUSED_SOURCE_GRANT_MISSING
    if not refs:
        return REFUSED_SOURCE_GRANT_MISMATCH
    families = {r[0] for r in refs}
    editions = {r[1] for r in refs}
    if getattr(grant, "grant_source_family", None) not in families:
        return REFUSED_SOURCE_GRANT_WRONG_OWNER
    owner = getattr(grant, "grant_source_owner", "") or ""
    if owner and owner not in families:
        return REFUSED_SOURCE_GRANT_WRONG_OWNER
    if getattr(grant, "grant_edition", None) not in editions:
        return REFUSED_SOURCE_GRANT_MISMATCH
    if not getattr(grant, "grant_current", False):
        return REFUSED_SOURCE_GRANT_NOT_CURRENT
    return None


def read_selected_world(structural: StructuralWorld, case: TemporalCase,
                        method: str, clock_year: int, retrospective: bool = False,
                        archival_known_at_upper_year: int | None = None,
                        source_grant: Any = None,
                        require_source_grant: bool = False) -> OpportunitySet:
    """Read a historical opportunity set for ONE young person.

    The structural and access world is held fixed. Only the temporal channel,
    evaluated at the historical clock, selects which routes are open.

    R5: only a natively AUTHORIZED observation may present an open, permission-valid
    route. A PROBE_ONLY result reports ROUTE_BLOCKED_NO_SUPPORT as its
    `opportunity_ids` and lists the band-implied routes separately as explicitly
    exploratory. This is a sourcefree consumer contract; it is not evidence that any
    real product was installed or issued.

    T9D-1: product authorization is determined per the actually USED basis at the
    clock. A held estimate or interpolated stand-in is never an authorized
    observation of the query year, even when the supplied archive context carries
    a natively multi-wave-authorized anchor group.

    T9D-2: the native temporal source-grant (provenance) and the ACTOR opportunity
    entitlement are distinct. No route opens without a present current
    independently provided actor grant in `structural.access_grants`.

    T9D-5: a claimed source-qualified issuer grant is CHECKED against the used
    basis; a missing/mismatched/non-current/wrong-owner claim returns explicit
    UNAVAILABLE rather than a synthesized clearance. Absence of any claim means no
    source-qualified authority is asserted (sourcefree synthetic grain).
    """
    tv = evaluate(case, method, clock_year=clock_year, retrospective=retrospective,
                  archival_known_at_upper_year=archival_known_at_upper_year)
    routes = structural.structural_routes

    # R3/T9D-4: bind provenance to the waves actually used, not to the first supplied wave.
    refs = basis_source_refs(case, tv)
    source_conflict = bool(refs) and len(set(refs)) > 1
    if source_conflict:
        tv = TemporalValue(method, None, None, "UNKNOWN_BASIS_SOURCE_CONFLICT",
                           BLOCKED_TEMPORAL_KEY, tv.basis_wave_ids,
                           "basis waves disagree on source_family/edition; refusing "
                           "to name a single supported source",
                           refused_code=REFUSED_BASIS_SOURCE_CONFLICT,
                           native_authorization=tv.native_authorization,
                           basis_source_refs=tv.basis_source_refs,
                           product_observation_status=PRODUCT_REFUSED)
    used = tuple(sorted({r[0] for r in refs}))
    used_editions = tuple(sorted({r[1] for r in refs}))

    # T9D-5: check a claimed source-qualified issuer grant against the used basis.
    grant_refusal = None
    if source_grant is not None:
        grant_refusal = check_source_grant(source_grant, refs)
    elif require_source_grant:
        grant_refusal = REFUSED_SOURCE_GRANT_MISSING
    if grant_refusal is not None and tv.refused_code is None:
        tv = TemporalValue(method, tv.value, tv.band, tv.uncertainty, tv.temporal_key,
                           tv.basis_wave_ids,
                           (tv.detail + "; source-qualified issuer claim is "
                            + grant_refusal + "; no production original issuer or "
                            "clearance is synthesized").strip("; "),
                           refused_code=grant_refusal,
                           native_authorization=tv.native_authorization,
                           not_observed=tv.not_observed,
                           rupture_qualified=tv.rupture_qualified,
                           publication_lag_wave_ids=tv.publication_lag_wave_ids,
                           archive_context_wave_ids=tv.archive_context_wave_ids,
                           rupture_crossed_year=tv.rupture_crossed_year,
                           missing_excluded_wave_ids=tv.missing_excluded_wave_ids,
                           basis_source_refs=tv.basis_source_refs,
                           product_observation_status=tv.product_observation_status)

    # T9D-1: the PRODUCT key is the gated status. Only an observation at the query
    # clock may carry the anchor group's AUTHORIZED status into a product.
    product_key = tv.temporal_key
    if (tv.refused_code is None and tv.value is not None
            and product_key == AUTHORIZED_SPARSE_TEMPORAL_KEY
            and tv.product_observation_status != PRODUCT_OBSERVED_AT_CLOCK):
        product_key = PROBE_ONLY_TEMPORAL_KEY

    # T9D-2: actor opportunity entitlement gate.
    entitlement = ENTITLEMENT_GRANTED if structural.access_grants else ENTITLEMENT_WITHHELD

    if tv.refused_code is not None or tv.value is None:
        opened = ("ROUTE_BLOCKED_NO_SUPPORT",)
        exploratory = ()
        authorized = False
        product_key = tv.temporal_key if tv.temporal_key else BLOCKED_TEMPORAL_KEY
    elif product_key == AUTHORIZED_SPARSE_TEMPORAL_KEY and entitlement == ENTITLEMENT_GRANTED:
        allowed = _BAND_ROUTES.get(tv.band or "none", ("ROUTE_BLOCKED_NO_SUPPORT",))
        opened = tuple(r for r in routes if r in allowed)
        exploratory = ()
        authorized = True
    else:
        # R5/T9D-1/T9D-2: exploratory / probe-only / held / unentitled.
        # Never a permission-valid open route.
        allowed = _BAND_ROUTES.get(tv.band or "none", ())
        exploratory = tuple(r for r in routes if r in allowed)
        opened = ("ROUTE_BLOCKED_NO_SUPPORT",)
        authorized = False

    return OpportunitySet(
        query_clock=clock_year, temporal_method=method,
        opportunity_ids=opened, pressure_band=tv.band, temporal_key=product_key,
        uncertainty=tv.uncertainty, basis_wave_ids=tv.basis_wave_ids,
        refused_code=tv.refused_code,
        authorized_opportunity=authorized,
        exploratory_route_ids=exploratory,
        archive_context_wave_ids=archive_context_of(case, tv, clock_year, retrospective),
        actor_opportunity_entitlement=entitlement,
        product_observation_status=tv.product_observation_status,
        provenance=dict(
            # R4: the COMPLETE structural/access world identity travels with the read,
            # so structural constancy can actually be certified.
            structural_world_fields=dict(
                world_id=structural.world_id,
                structural_routes=list(structural.structural_routes),
                access_grants=list(structural.access_grants),
                institution=structural.institution),
            world_id=structural.world_id, institution=structural.institution,
            access_grants=list(structural.access_grants),
            grain=GRAIN,
            # R3: bound to the basis waves actually used.
            source_family=used[0] if len(used) == 1 else (list(used) if used else ""),
            source_families=list(used),
            instrument=case.instrument, cohort=case.cohort, country=case.country,
            edition=used_editions[0] if len(used_editions) == 1 else (list(used_editions) if used_editions else ""),
            editions=list(used_editions),
            basis_source_refs=[list(r) for r in refs],
            query_clock=clock_year,
            clock_question="RETROSPECTIVE_ARCHIVAL" if retrospective else "AS_OF_KNOWABLE",
            # R7: basis lag only; unused post-clock waves live in
            # archive_context_wave_ids and are never presented as product basis.
            publication_lag_wave_ids=list(pub_lag_of(tv)),
            archive_context_wave_ids=list(
                archive_context_of(case, tv, clock_year, retrospective)),
            native_multi_wave_authorization_status=tv.native_authorization.get(
                "multi_wave_authorization_status"),
            native_multi_wave_authorization_reason=tv.native_authorization.get(
                "multi_wave_authorization_reason"),
            # T9D-1/T9D-2: typed product/entitlement distinctions, separate from
            # the native temporal source-grant above.
            product_observation_status=tv.product_observation_status,
            product_temporal_key=product_key,
            actor_opportunity_entitlement=entitlement,
            archival_known_at_upper_year=archival_known_at_upper_year,
            source_grant_claimed=source_grant is not None or require_source_grant,
            source_grant_status=grant_refusal if grant_refusal is not None else (
                "SOURCE_GRANT_VERIFIED" if source_grant is not None else "NO_SOURCE_QUALIFIED_CLAIM"),
            synthetic=True, observed_temporal_calibration=False,
            authorized_opportunity=authorized,
            t8f3_assignment_preserved=T8F3_ASSIGNMENT,
        ),
    )


def structurally_identical(a: OpportunitySet, b: OpportunitySet) -> bool:
    """R4: structural/access world must be provably UNCHANGED between two clocks.

    Compares the COMPLETE world identity including `structural_routes`, which the
    T9B certificate ignored. Removing a route from the supplied world at the same
    clock now makes this return False.
    """
    return (a.provenance.get("structural_world_fields")
            == b.provenance.get("structural_world_fields")
            and a.provenance["world_id"] == b.provenance["world_id"]
            and a.provenance["access_grants"] == b.provenance["access_grants"]
            and a.provenance["institution"] == b.provenance["institution"]
            and a.provenance["grain"] == b.provenance["grain"])


def materially_different(a: OpportunitySet, b: OpportunitySet) -> bool:
    return a.opportunity_ids != b.opportunity_ids
