"""Read-only S43 root plus the S44 sampled-root adapter."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S43_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1"
CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "s36": "8da78d8031a06a4bd7e1297fd713e573299c0860",
    "s37": "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9",
    "s39": "e41513fa65601a37e7b3b430d26c626ae0217d90",
    "s40": "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
    "s41": "c72a10d284f8869b990db3e6849ed174a51bd784",
    "s42": "2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91",
    "s43": "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S43_RETURN)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s43.bootstrap import install as s43_install

    s43_install()
    import s43  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s43.bootstrap import roots as s43_roots

    value = s43_roots()
    value["s43_return"] = str(S43_RETURN)
    value["s44_return"] = str(RETURN)
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S43_RETURN", "install", "roots"]
