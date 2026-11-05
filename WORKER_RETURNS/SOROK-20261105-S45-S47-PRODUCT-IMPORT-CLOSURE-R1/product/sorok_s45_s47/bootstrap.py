"""Install the pinned local import closure for the S45-S47 product spine."""

from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PRODUCT = PACKAGE.parent
RETURN_ROOT = PRODUCT.parent
VENDOR = PRODUCT / "vendor"
WORKER_RETURNS = VENDOR / "WORKER_RETURNS"

S36_RETURN = WORKER_RETURNS / "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
S37_RETURN = WORKER_RETURNS / "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1"
S39_RETURN = WORKER_RETURNS / "SOROK-20261024-S39-GENERATED-RESPONSE-R1"
S40_RETURN = WORKER_RETURNS / "SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1"
S41_RETURN = WORKER_RETURNS / "SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1"
S42_RETURN = WORKER_RETURNS / "SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1"
S43_RETURN = WORKER_RETURNS / "SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1"
S44_RETURN = WORKER_RETURNS / "SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1"
S45_RETURN = WORKER_RETURNS / "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1"
S46_RETURN = WORKER_RETURNS / "SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1"
S47_RETURN = WORKER_RETURNS / "SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1"
JOIN_E_RETURN = WORKER_RETURNS / "SOROK-20261022-SAME-PERSON-JOIN-R1"
LANGUAGE_RETURN = VENDOR / "LANGUAGE_MEDIATION_R1"

_INSTALLED = False


def _insert_front(path: Path) -> None:
    text = str(path)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)


def install() -> dict:
    global _INSTALLED
    if _INSTALLED:
        return roots()
    bp2_vendor = JOIN_E_RETURN / "vendor" / "j" / "candidate" / "vendor" / "bp2" / "vendor"
    for label, path in {
        "S37_M35_RETURN": S37_RETURN / "vendor" / "m35",
        "S37_JOIN_E_RETURN": JOIN_E_RETURN,
        "S37_LANGUAGE_RETURN": LANGUAGE_RETURN,
        "S37_S36_RETURN": S36_RETURN,
        "M35_JOIN_E_RETURN": JOIN_E_RETURN,
        "M35_BP2_VENDOR": bp2_vendor,
    }.items():
        os.environ[label] = str(path)

    _insert_front(VENDOR)
    for path in (S47_RETURN, S46_RETURN, S45_RETURN, S44_RETURN, S43_RETURN,
                 S42_RETURN, S41_RETURN, S40_RETURN, S39_RETURN,
                 S37_RETURN, S36_RETURN, LANGUAGE_RETURN, JOIN_E_RETURN):
        _insert_front(path)
    _insert_front(VENDOR)

    import rawlsing_next.m1_temporal_v554_admission_dedup  # noqa: F401
    import rawlsing_next.m2_v555_atomic_route  # noqa: F401
    import rawlsing_next.m3_v556_higher_order_structural  # noqa: F401
    import rawlsing_next.m4_v557_v558_publication_repository  # noqa: F401
    import rawlsing_next.m5_runtime_rsc_peer_prior  # noqa: F401
    import rawlsing_next.m6_actor_safe_expression  # noqa: F401
    _insert_front(bp2_vendor / "native")
    import rawlsing_next.v3_psepf_zero_positive_guard  # noqa: F401

    from s47.bootstrap import install as s47_install

    s47_install()
    import s47  # noqa: F401

    _insert_front(VENDOR)
    _INSTALLED = True
    return roots()


def roots() -> dict:
    return {
        "package": str(PACKAGE),
        "product": str(PRODUCT),
        "return_root": str(RETURN_ROOT),
        "vendor": str(VENDOR),
        "worker_returns": str(WORKER_RETURNS),
        "s36": str(S36_RETURN),
        "s37": str(S37_RETURN),
        "s39": str(S39_RETURN),
        "s40": str(S40_RETURN),
        "s41": str(S41_RETURN),
        "s42": str(S42_RETURN),
        "s43": str(S43_RETURN),
        "s44": str(S44_RETURN),
        "s45": str(S45_RETURN),
        "s46": str(S46_RETURN),
        "s47": str(S47_RETURN),
        "join_e": str(JOIN_E_RETURN),
        "language": str(LANGUAGE_RETURN),
        "live": str(VENDOR / "rawlsing_next"),
    }
