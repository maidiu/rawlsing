"""Local source-free actor-history variants for R29P fault controls."""
from __future__ import annotations

from dataclasses import replace

import historical_actor_producer as H

A_GENESIS_ALTERED = "R29P_A_GENESIS_ALTERED"


def install() -> None:
    """Register the bounded A-genesis variant without patching any builder."""
    if A_GENESIS_ALTERED not in H.VARIANTS:
        H.VARIANTS[A_GENESIS_ALTERED] = replace(
            H.VARIANTS["A_REPAIR_LONG"],
            variant=A_GENESIS_ALTERED,
            a_seed="R29P_A_ALTERED_SEED",
            a_birth=17,
        )
