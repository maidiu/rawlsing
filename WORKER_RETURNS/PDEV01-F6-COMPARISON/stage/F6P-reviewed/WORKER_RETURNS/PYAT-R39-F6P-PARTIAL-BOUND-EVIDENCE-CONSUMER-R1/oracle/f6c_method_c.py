"""Comparison C: source-native NO-POOLING conservative bounds.

Independent method preparation by the R35 F6C worker. NOT an original-source
issuance, NOT a native producer, and NOT a claim about V550/J or any other
named lineage. It is declared as this worker's own method.

Design, in one line: never average or mix joints across independent surveys,
and never assert that one survey's stratum represents a target stratum unless
an explicit transport permission says so. Absent that permission the target is
reported as BOUNDS, which in the sourcefree worlds studied here is complete
ignorance. That is the honest answer, not a failure.

What C is for in this court. Neither A nor B emits a genuine partial
identification interval for a target marginal. B emits a covered
subprobability plus a scalar unknown mass; the two must be recombined by the
reader. C performs that recombination explicitly and additionally reuses the
native primitive ``complementary_binary_bounds`` so the partial identification
arithmetic is not invented here.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F

METHOD = "R35F6C_NO_POOLING_CONSERVATIVE_BOUNDS@1"
AUTHORITY = "INDEPENDENT_METHOD_PREPARATION_NOT_AN_ORIGINAL_SOURCE"


class BoundRefusal(Exception):
    pass


def _num(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise BoundRefusal("numeric inputs must be integers or rational strings")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise BoundRefusal("invalid rational") from exc


def _mapped_stratum_mass(source, z):
    """Recode one source-native stratum table into declared-label space.

    Returns {label_tuple: mass}. Also returns the set of native codes observed,
    so positivity can be checked rather than assumed.
    """
    axes = source["axes"]
    table = {}
    observed_native = set()
    for cell in source["strata"][z]["cells"]:
        cats = tuple(cell["categories"])
        observed_native.add(cats)
        key = tuple(a["category_map"][c] for a, c in zip(axes, cats))
        table[key] = table.get(key, F(0)) + _num(cell["mass"])
    return table, observed_native


def _check_positivity(source):
    """Refuse rather than manufacture an omitted category as an observed zero.

    Same invariant the corrected S03FO producer enforces; C enforces it
    independently instead of trusting a producer to have done so.
    """
    axes = source["axes"]
    for z, table in source["strata"].items():
        if table["table_status"] != "EXHAUSTIVE_DECLARED_JOINT_RISK_SET":
            raise BoundRefusal("POSITIVITY_NON_EXHAUSTIVE_TABLE_" + z)
        if sum(c["n"] for c in table["cells"]) + table["excluded_n"] != table["eligible_n"]:
            raise BoundRefusal("RISK_DENOMINATOR_NONCONSERVATION_" + z)
        domain = 1
        for a in axes:
            domain *= len(a["category_map"])
        seen = {tuple(c["categories"]) for c in table["cells"]}
        if len(seen) != domain:
            raise BoundRefusal(
                "POSITIVITY_INCOMPLETE_NATIVE_JOINT_DOMAIN_%s(%d/%d)" % (z, len(seen), domain))


def _check_distinct_respondents(sources):
    seen = {}
    for s in sources:
        key = (s["survey_lineage"], s["sample_id"])
        if key in seen:
            raise BoundRefusal("INDISTINCT_SAMPLE_UNRESOLVED:" + "|".join(sorted((seen[key], s["source_id"]))))
        seen[key] = s["source_id"]


def nopooling_bounds(target, sources, policy, *, transport_permission=None):
    """Return conservative bounds for a target marginal, with no pooling.

    ``transport_permission`` maps stratum -> set of source_ids whose stratum
    table is admitted to represent the TARGET stratum. Absent entirely, nothing
    is admitted and every target marginal is complete ignorance [0, 1].

    Returns a dict of exact rationals as strings. Never returns a predictive
    conditional, a route quantity, or a selection weight.
    """
    sources = deepcopy(sources)
    permission = {z: set(v) for z, v in (transport_permission or {}).items()}

    strata = {k: _num(v) for k, v in target["strata"].items()}
    if sum(strata.values()) != 1:
        raise BoundRefusal("TARGET_STRATUM_SHARES_MUST_SUM_TO_ONE")
    for k in ("target_id", "geography", "boundary_ref", "population", "unit", "strata_ref"):
        if not isinstance(target.get(k), str) or not target[k].strip():
            raise BoundRefusal("MISSING_TARGET_IDENTITY:" + k)

    for s in sources:
        _check_positivity(s)
    _check_distinct_respondents(sources)

    min_support = policy["minimum_raw_support"]
    axes_labels = [list(a["category_map"].values()) for a in sources[0]["axes"]]
    outcome_axis = next(i for i, a in enumerate(sources[0]["axes"])
                        if a["construct_ref"] == "employment_position")

    per_source, stratum_report, unknown_by_stratum = [], {}, {}
    for z, share in sorted(strata.items()):
        if not share:
            stratum_report[z] = {"target_share": str(share), "admissible": [],
                                 "admitted": [], "unknown_share": "0"}
            continue
        admissible, detail = [], []
        for s in sources:
            if z not in s["strata"]:
                continue
            counts = sum(c["n"] for c in s["strata"][z]["cells"])
            if counts < min_support:
                continue
            table, _ = _mapped_stratum_mass(s, z)
            if sum(table.values()) <= 0:
                continue
            admissible.append(s)
            detail.append({
                "source_id": s["source_id"],
                "raw_support": counts,
                "weighted_support": str(sum(table.values())),
                "scope": "SOURCE_NATIVE_ONLY_NO_TARGET_REPRESENTATION_CLAIMED",
                "stratum_marginal": {str(k[outcome_axis]): str(v / sum(table.values()))
                                     for k, v in sorted(table.items())},
            })
        # NO MIXING. Each admissible source is described on its own respondents.
        for d in detail:
            d["mixed_with_other_sources"] = False
            d["used_as_target_estimate"] = False
        per_source.extend(detail)

        admitted = [s["source_id"] for s in admissible if s["source_id"] in permission.get(z, set())]
        # A stratum is point-identified only when exactly ONE source is admitted
        # for it. Two admitted sources would require pooling, which C refuses.
        point = None
        if len(admitted) == 1:
            sid = admitted[0]
            src = next(s for s in sources if s["source_id"] == sid)
            table, _ = _mapped_stratum_mass(src, z)
            tot = sum(table.values())
            point = {}
            for lab in axes_labels[outcome_axis]:
                point[lab] = sum((v for k, v in table.items() if k[outcome_axis] == lab), F(0)) / tot
        unknown = share if point is None else F(0)
        unknown_by_stratum[z] = unknown
        stratum_report[z] = {"target_share": str(share),
                             "admissible": [s["source_id"] for s in admissible],
                             "admitted": admitted,
                             "point_identified": point is not None,
                             "unknown_share": str(unknown),
                             "pooling_applied": "NONE"}

    # Marginal bounds, computed for EVERY axis, carrying the unknown mass as
    # [0, unknown] rather than silently renormalizing it away.
    bounds_by_axis, point_contribution = {}, {}
    for ai in range(len(axes_labels)):
        axis_bounds = {}
        for lab in axes_labels[ai]:
            lo = F(0)
            for z, share in strata.items():
                if not share:
                    continue
                sr = stratum_report[z]
                if sr["point_identified"]:
                    s_obj = next(s for s in sources if s["source_id"] == sr["admitted"][0])
                    table, _ = _mapped_stratum_mass(s_obj, z)
                    tot = sum(table.values())
                    p = sum((v for k, v in table.items() if k[ai] == lab), F(0)) / tot
                    lo += share * p
            axis_bounds[lab] = {"lower": str(lo),
                                "upper": str(lo + sum(unknown_by_stratum.values()))}
        bounds_by_axis[axes_labels and sources[0]["axes"][ai]["construct_ref"]] = axis_bounds
        point_contribution[sources[0]["axes"][ai]["construct_ref"]] = axis_bounds
    outcome_bounds = bounds_by_axis["employment_position"]
    sec_bounds = bounds_by_axis["material_security"]

    # Native partial-identification primitive, reused rather than reinvented.
    cross_channel = None
    native = _load_native_primitive()
    if native is not None and "secure" in sec_bounds and "formal" in outcome_bounds:
        # Rational STRINGS, because the native primitive rejects floats and
        # Fractions by contract. Identical value, contract-legal type.
        cross_channel = native.complementary_binary_bounds(
            sec_bounds["secure"]["lower"], outcome_bounds["formal"]["lower"])

    out = {
        "method": METHOD,
        "authority": AUTHORITY,
        "world_scope": target,
        "pooling": "NONE",
        "positivity": "COMPLETE_NATIVE_JOINT_DOMAIN_REQUIRED_PER_STRATUM",
        "distinct_respondents": "LINEAGE_AND_SAMPLE_ID_MUST_BE_UNIQUE",
        "strata": stratum_report,
        "per_source_native_descriptives": per_source,
        "target_marginal_bounds_employment_position": outcome_bounds,
        "target_marginal_bounds_material_security": sec_bounds,
        "identified_point_component": point_contribution,
        "total_unknown_mass": str(sum(unknown_by_stratum.values())),
        "joint_status": ("NOT_IDENTIFIED_NO_POOLING_NO_TRANSPORT_PERMISSION"
                         if all(not v["point_identified"] for v in stratum_report.values())
                         else "PARTIAL_STRATUM_ADMITTED_NO_POOLING"),
        "unidentified_cross_channel": cross_channel,
        "refusals": [
            "NO_POINT_DISTRIBUTION_WITHOUT_SINGLE_SOURCE_TRANSPORT_PERMISSION",
            "NO_CROSS_SOURCE_POOLING",
            "NO_RESPONDENT_LEVEL_JOIN",
            "NO_ROUTE_ACTOR_OR_SELECTION_QUANTITY",
        ],
        "claims_not_made": [
            "these are not population point estimates",
            "26/31-style figures are not a generated person's life-route probability",
            "no target stratum is claimed to be represented by any survey",
        ],
    }
    return out


def condition_status(bundle, conditions, outcome):
    """C's own consumer: never returns a predictive probability."""
    return {
        "state": "UNAVAILABLE",
        "reason": "NO_POOLING_NO_TRANSPORT_PERMISSION",
        "bounds": bundle["target_marginal_bounds_employment_position"],
        "bounds_material_security": bundle["target_marginal_bounds_material_security"],
        "identified_point_component": bundle["identified_point_component"],
        "total_unknown_mass": bundle["total_unknown_mass"],
        "note": ("C reports bounds. It does not emit a predictive conditional, "
                 "because emitting one would require either pooling across "
                 "surveys or an admitted transport assumption."),
    }


_NATIVE = None


def _load_native_primitive():
    """Load the ORIGINAL native complementary_binary_bounds by absolute path.

    Deliberately loaded by file location, from the pinned corrected producer,
    so the partial-identification arithmetic is the original's and not this
    worker's invention.
    """
    global _NATIVE
    if _NATIVE is not None:
        return _NATIVE
    import importlib.util
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "staging" / "cand_A" / "rawlsing_next" / "pre553_heterogeneous_synthesis.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("r35f6c_native_primitive_A", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _NATIVE = mod
    return mod