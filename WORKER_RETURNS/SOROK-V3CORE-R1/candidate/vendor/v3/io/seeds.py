# v3/io/seeds.py — reproducible random initial state for smoke tests and scenarios.

from __future__ import annotations

import random

from v3.core.state import (
    BackboneState,
    Capacity,
    ReproductionConstraints,
)


def randomized_seed(seed: int, year: int = 2000, age: int = 25) -> BackboneState:
    """Return a BackboneState with randomized reproduction_constraints and capacity (0–100). Deterministic given seed."""
    rng = random.Random(seed)
    rc = ReproductionConstraints(
        dependents=rng.uniform(0, 80),
        housing_insecurity=rng.uniform(0, 70),
        legal_status=rng.uniform(20, 100),
        debt=rng.uniform(0, 60),
        job_insecurity=rng.uniform(0, 70),
        caregiving_load=rng.uniform(0, 80),
    )
    cap = Capacity(
        time=rng.uniform(20, 90),
        money=rng.uniform(20, 90),
        health=rng.uniform(30, 90),
        social_support=rng.uniform(20, 90),
        skill=rng.uniform(20, 80),
        mobility=rng.uniform(20, 80),
        risk_tolerance=rng.uniform(20, 80),
        legitimacy=rng.uniform(20, 80),
    )
    return BackboneState(year=year, age=age, reproduction_constraints=rc, capacity=cap)
