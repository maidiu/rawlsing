"""Read-only S45 root plus the S46 interval-participation adapter."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S45_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1"
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
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
    "sdtf_r4": "79659b352035f095b325181d4f35c259da6b79d0",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S45_RETURN)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s45.bootstrap import install as s45_install

    s45_install()
    import s45  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s45.bootstrap import roots as s45_roots

    value = s45_roots()
    value["s45_return"] = str(S45_RETURN)
    value["s46_return"] = str(RETURN)
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S45_RETURN", "install", "roots"]
