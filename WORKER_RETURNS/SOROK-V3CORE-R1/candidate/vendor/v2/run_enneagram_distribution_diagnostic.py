"""
Diagnostic: Run pipeline N times per country, collect Enneagram type distribution.

Purpose: Establish baseline before adding cultural-context layer.
- If any type is consistently rare across ALL countries → bug in wisdom base
- If Type 6 dominates everywhere (e.g. 40%+) → bug
- Empirical data informs floor/ceiling for cultural modifiers

Reference: ~189k test-takers show Type 9 (16.2%) and Type 6 (16.1%) most common;
Types 5 and 8 notably rarer. Self-selection bias in test-takers.
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))

from spec import IdentitySkeleton, simulate_life_course, CohortAdjusters
from data_access import get_world_slice, get_driver_vec, get_local_modifiers

# Diverse countries, N runs each
CONFIG = [
    ("US", "California", "Los Angeles", "city", 1990),
    ("GB", "England", "London", "city", 1988),
    ("DE", "Bavaria", "Munich", "city", 1992),
    ("VN", "Ho Chi Minh City", "Ho Chi Minh City", "megacity", 1980),
    ("JP", "Kanto", "Tokyo", "megacity", 1987),
    ("MX", "Mexico City", "Mexico City", "megacity", 1990),
    ("BR", "São Paulo", "São Paulo", "megacity", 1985),
    ("ZA", "Gauteng", "Johannesburg", "city", 1988),
    ("IN", "Maharashtra", "Mumbai", "megacity", 1990),
]
RUNS_PER_COUNTRY = 15  # 15 * 9 = 135 runs total


def run_one(country: str, region: str, locality: str, urbanicity: str, birth_year: int):
    identity = IdentitySkeleton(
        internal_id="diag",
        given_name="",
        gender="female",
        birth_year=birth_year,
        anchor_year=2025,
        age_at_anchor=2025 - birth_year,
        country_code=country,
        region=region,
        locality=locality,
        urbanicity=urbanicity,
        class_origin="middle",
        current_class="middle",
        ethnicity_label="",
        minority_status="",
        childhood_religion="",
        current_religion="",
        religiosity_level=50.0,
        primary_language="",
    )
    try:
        history = simulate_life_course(
            identity=identity,
            adjusters=CohortAdjusters(),
            constraints=None,
            get_world_slice=get_world_slice,
            get_driver_vec=get_driver_vec,
            get_local_modifiers=get_local_modifiers,
        )
        return history.enneagram_profile.primary_type if history.enneagram_profile else None
    except Exception:
        return None


def main():
    print("=" * 70)
    print("ENNEAGRAM TYPE DISTRIBUTION DIAGNOSTIC")
    print("=" * 70)
    print(f"Config: {len(CONFIG)} countries × {RUNS_PER_COUNTRY} runs = {len(CONFIG) * RUNS_PER_COUNTRY} total")
    print()

    # Per-country counts
    by_country = defaultdict(lambda: defaultdict(int))
    global_counts = defaultdict(int)

    for country, region, locality, urbanicity, birth_year in CONFIG:
        label = f"{country} {region}"
        for i in range(RUNS_PER_COUNTRY):
            t = run_one(country, region, locality, urbanicity, birth_year)
            if t is not None:
                by_country[label][t] += 1
                global_counts[t] += 1

    total = sum(global_counts.values())
    print("GLOBAL DISTRIBUTION (all runs)")
    print("-" * 40)
    for t in range(1, 10):
        n = global_counts[t]
        pct = 100 * n / total if total else 0
        bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
        print(f"  Type {t}: {n:3d} ({pct:5.1f}%) {bar}")
    print()

    print("PER-COUNTRY DISTRIBUTION")
    print("-" * 70)
    for label in sorted(by_country.keys()):
        counts = by_country[label]
        n_total = sum(counts.values())
        top = sorted(counts.items(), key=lambda x: -x[1])[:3]
        top_str = ", ".join(f"T{k}({100*v/n_total:.0f}%)" for k, v in top)
        print(f"  {label:25s} n={n_total:3d}  top: {top_str}")

    print()
    print("DIAGNOSTIC CHECKS")
    print("-" * 40)
    # Any type consistently rare everywhere?
    rare_everywhere = []
    for t in range(1, 10):
        pcts = [100 * by_country[lbl].get(t, 0) / max(1, sum(by_country[lbl].values())) for lbl in by_country]
        if all(p < 5 for p in pcts):
            rare_everywhere.append(t)
    if rare_everywhere:
        print(f"  ⚠ Types consistently rare (<5%) everywhere: {rare_everywhere}")
    else:
        print("  ✓ No type is consistently rare across all countries")

    # Any type dominating globally?
    max_pct = max(100 * v / total for v in global_counts.values()) if total else 0
    if max_pct > 40:
        print(f"  ⚠ One type dominates globally: {max_pct:.1f}%")
    else:
        print(f"  ✓ No single type dominates (>40%): max={max_pct:.1f}%")

    print()
    print("Reference: ~189k test-takers → Type 9 (16.2%), Type 6 (16.1%) most common; 5,8 rarer")
    print("=" * 70)


if __name__ == "__main__":
    main()
