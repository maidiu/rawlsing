"""Read-only S40/S39/S37 roots plus the S41 continuation adapter."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S40_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1"
S39_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-S39-GENERATED-RESPONSE-R1"
S37_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1"
CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "s36": "8da78d8031a06a4bd7e1297fd713e573299c0860",
    "s37": "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9",
    "s39": "e41513fa65601a37e7b3b430d26c626ae0217d90",
    "s40": "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S40_RETURN), str(S39_RETURN), str(S37_RETURN)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s40.bootstrap import install as s40_install

    s40_install()
    import s40  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s40.bootstrap import roots as s40_roots

    value = s40_roots()
    value["s40_return"] = str(S40_RETURN)
    value["s41_return"] = str(RETURN)
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S37_RETURN", "S39_RETURN", "S40_RETURN", "install", "roots"]
