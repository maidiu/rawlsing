"""Explicit TEST_ONLY help-language evidence added to the S44 root bundle."""
from __future__ import annotations

from typing import Any

from .bootstrap import install

install()

from s44.bundle import default_bundle  # noqa: E402

from .language import NATIVE, PAIRS, UNITS  # noqa: E402


def root_bundle(seed: str = "01" * 32) -> dict:
    bundle = default_bundle(root_seed=seed)
    evidence = list(bundle.get("language_evidence") or [])
    for template_id, pair in PAIRS.items():
        unit = UNITS[template_id]
        evidence.append({
            "evidence_id": "TEST_ONLY_S45_HELP_" + template_id.upper(),
            "intent": unit["intent"],
            "text": pair["native_text"],
            "concept_id": unit["concept_id"],
            "milieu_id": unit["milieu_id"],
            "sense_id": unit["sense_id"],
            "relation_label": "AFFIRMED",
            "atoms": list(unit["atoms"]),
            "language_tag": NATIVE,
            "speaker_actor": "B",
            "counterexample_event_ids": [],
        })
    bundle["language_evidence"] = evidence
    bundle.pop("bundle_hash", None)
    from s44.bundle import normalize_bundle
    return normalize_bundle(bundle)


__all__ = ["root_bundle"]
