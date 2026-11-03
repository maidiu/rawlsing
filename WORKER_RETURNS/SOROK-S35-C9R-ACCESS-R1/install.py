"""Read-only import roots for the S35 actor-access bridge.

Only WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1 is writable. The staged R31J cut
provides the exact pinned C9R consumer and BP1/BP2/BP4 closures; the M35 return
provides firstclass.py. No external checkout is read.
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent
REPO = RETURN.parents[1]
R31J = (
    REPO
    / ".s35-sources"
    / "WORKER_RETURNS"
    / "SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1"
)
M35_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1"
BP2_VENDOR = R31J / "candidate" / "vendor" / "bp2" / "vendor"
BP2_JOINED = M35_RETURN / "candidate" / "vendor" / "bp2"
C9R = BP2_VENDOR / "c9r"
NATIVE = BP2_VENDOR / "native"
BP1 = BP2_VENDOR / "bp1"
G18 = BP2_VENDOR / "g18"
BP3 = BP2_VENDOR / "bp3"
BP4 = R31J / "candidate" / "vendor" / "bp4"
R31J_CANDIDATE = R31J / "candidate"
GENERATIVE = R31J / "r29m" / "source"

CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "r31j": "64fec28c374d8f77fb0b412d0c934d798ede03e8",
    "c9r": "6fa2939972ce5a2c0cc4f2b033946b276f1c2934",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
}

EXPECTED_SHA256 = {
    "m35_firstclass": "acfdc42daec3e701e017664caef370780db47c72ed1bc85fcc26999f8a38a3db",
    "c9r_response_rules": "aa8d978f43bd14a11430371e68e2ce4e2ebf1adb385ee52230a4c23a16c49dfc",
    "c9r_target_rules": "e5d38865d2a4d50a904a387b2a8770bda55567dcef670e97c0dd696c8f7475a5",
    "c9r_pipeline": "b5da655ca03cdc9dc6dad11b88dfadd22101836cffc7993f530e6148ded0695c",
    "c9r_conditioning": "edc3a5690c4ed281a41b877119af63397b6348c54a407276eee020005b849887",
    "c9r_native_guard": "12b2c49f664662cbfe993fc4817751ed9edfff3ce89c44cac489a00cb5e42177",
}

_PATHS = (
    RETURN,
    M35_RETURN,
    BP2_JOINED,
    R31J_CANDIDATE,
    R31J,
    GENERATIVE,
    C9R,
    NATIVE,
    BP4,
    BP1,
    G18,
    BP3,
)

_FORGET_PREFIXES = (
    "bp1",
    "bp2_joined",
    "bp2p4",
    "bp3",
    "bp4",
    "candidate",
    "c8_exclusive_writer",
    "c8_readonly_consumer",
    "c8o_trusted_outbox",
    "c9_event_ingress",
    "generative_resource",
    "historical_actor_producer",
    "lab_sgi1",
    "outbox_prototype",
    "r29m",
    "r29p",
    "r31j",
    "rawlsing_next",
)

_INSTALLED = False
_ORIGINS: dict[str, str] = {}


class S35DependencyMissing(ImportError):
    def __init__(self, name: str, path: Path) -> None:
        super().__init__(f"S35_DEPENDENCY_MISSING:{name}:{path}")
        self.name = name
        self.path = path


def _require(name: str, path: Path) -> None:
    if not path.exists():
        raise S35DependencyMissing(name, path)


def _forget() -> None:
    for name in list(sys.modules):
        if any(
            name == prefix or name.startswith(prefix + ".")
            for prefix in _FORGET_PREFIXES
        ):
            sys.modules.pop(name, None)


def _insert_front(path: Path) -> None:
    text = str(path)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for name, path in (
        ("R31J_STAGED_CUT", R31J),
        ("M35_RETURN", M35_RETURN),
        ("M35_BP2_VENDOR", BP2_VENDOR),
        ("C9R_PINNED", C9R),
        ("C9R_NATIVE_GUARD", NATIVE),
        ("BP4", BP4),
        ("BP1", BP1),
        ("M35_FIRSTCLASS", M35_RETURN / "firstclass.py"),
    ):
        _require(name, path)
    pinned_paths = {
        "m35_firstclass": M35_RETURN / "firstclass.py",
        "c9r_response_rules": C9R / "candidate" / "response_rules.py",
        "c9r_target_rules": C9R / "candidate" / "target_rules.py",
        "c9r_pipeline": C9R / "candidate" / "pipeline.py",
        "c9r_conditioning": C9R / "candidate" / "conditioning.py",
        "c9r_native_guard": NATIVE / "rawlsing_next" / "v3_psepf_zero_positive_guard.py",
    }
    for name, path in pinned_paths.items():
        if _sha256(path) != EXPECTED_SHA256[name]:
            raise ImportError("S35_PINNED_BLOB_DRIFT:" + name + ":" + str(path))
    os.environ["M35_BP2_VENDOR"] = str(BP2_VENDOR)
    _forget()
    for path in reversed(_PATHS):
        _insert_front(path)

    import bp2_joined

    bp2_path = Path(bp2_joined.__file__).resolve()
    if not bp2_path.is_relative_to(BP2_JOINED):
        raise ImportError("S35_M35_BP2_NOT_LOADED:" + str(bp2_path))

    import candidate

    candidate_path = Path(candidate.__file__).resolve()
    if not candidate_path.is_relative_to(C9R):
        raise ImportError("S35_PINNED_C9R_NOT_LOADED:" + str(candidate_path))

    import firstclass

    firstclass_path = Path(firstclass.__file__).resolve()
    if firstclass_path != (M35_RETURN / "firstclass.py").resolve():
        raise ImportError("S35_M35_FIRSTCLASS_NOT_LOADED:" + str(firstclass_path))

    import candidate.pipeline as pipeline
    from bridge import access as access_bridge

    if not getattr(pipeline, "_s35_selector_installed", False):
        pipeline._s35_original_evaluate_response = pipeline.evaluate_response
        pipeline._s35_selector_installed = True
        pipeline.evaluate_response = access_bridge.pipeline_selector

    for name in (
        "bp2_joined",
        "candidate",
        "candidate.pipeline",
        "firstclass",
        "bp4.store",
    ):
        module = sys.modules.get(name)
        if module is not None:
            _ORIGINS[name] = str(Path(getattr(module, "__file__", "")).resolve())
    _INSTALLED = True


def origins() -> dict:
    install()
    return dict(_ORIGINS)


def source_manifest() -> dict:
    install()
    pinned = {
        "m35_firstclass": M35_RETURN / "firstclass.py",
        "c9r_response_rules": C9R / "candidate" / "response_rules.py",
        "c9r_target_rules": C9R / "candidate" / "target_rules.py",
        "c9r_pipeline": C9R / "candidate" / "pipeline.py",
        "c9r_conditioning": C9R / "candidate" / "conditioning.py",
        "c9r_native_guard": NATIVE / "rawlsing_next" / "v3_psepf_zero_positive_guard.py",
    }
    return {
        "cuts": dict(CUTS),
        "paths": {
            "return": str(RETURN),
            "repo": str(REPO),
            "r31j_staged_cut": str(R31J),
            "m35_return": str(M35_RETURN),
            "m35_bp2_vendor": str(BP2_VENDOR),
            "c9r": str(C9R),
            "bp4": str(BP4),
        },
        "pinned": {
            name: {"path": str(path), "sha256": _sha256(path)}
            for name, path in pinned.items()
        },
        "origins": origins(),
    }


__all__ = [
    "BP1",
    "BP2_JOINED",
    "BP2_VENDOR",
    "BP3",
    "BP4",
    "C9R",
    "CUTS",
    "G18",
    "M35_RETURN",
    "NATIVE",
    "R31J",
    "REPO",
    "RETURN",
    "S35DependencyMissing",
    "install",
    "origins",
    "source_manifest",
]
