"""Read-only S48 root plus S49 independent-B actor producer."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S48_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "s36": "8da78d8031a06a4bd7e1297fd713e573299c0860",
    "s37": "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9",
    "s39": "e41513fa65601a37e7b3b430d26c626ae0217d90",
    "s40": "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
    "s41": "c72a10d284f8869b990db3e6849ed174a51bd784",
    "s42": "2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91",
    "s43": "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
    "s44": "923278fbe6b030e2ffdd10fe42d7a18266344611",
    "s45": "f26a138e20d53c809d611cf8d834ec647b0804bf",
    "s46": "f0ef39b92ce2e4add5c0a699389e12f1d7ae434e",
    "s47": "765a441f87292aa4c17794745b65cb54e6aaa83f",
    "s48": "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S48_RETURN)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s48.bootstrap import install as s48_install

    s48_install()
    import s48  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s48.bootstrap import roots as s48_roots

    value = s48_roots()
    value["s48_return"] = str(S48_RETURN)
    value["s49_return"] = str(RETURN)
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S48_RETURN", "install", "roots"]
