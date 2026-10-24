"""Read-only S37 roots plus the S39 generated-response adapter."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S37_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1"
CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "s36": "8da78d8031a06a4bd7e1297fd713e573299c0860",
    "s37": "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9",
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
    "s38_court": "2d34e1310e51a5a4ff248baa4eb7f9e938d6880e",
    "s38_hq_decision": "8f037c2f553a902df41b9db3333f41cda26a830e",
    "s39_commission": "a91ece256d0367633e546dc7a7fb1806c3ec9c58",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S37_RETURN)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s37.bootstrap import install as s37_install

    s37_install()
    import s37  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s37.bootstrap import roots as s37_roots

    value = s37_roots()
    value["s37_return"] = str(S37_RETURN)
    value["s39_return"] = str(RETURN)
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S37_RETURN", "install", "roots"]
