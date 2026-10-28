"""Exact observed numeric-domain binding for SRC04 income fields.

The fixed original source has a finite observed income domain even though the
possible numeric domain is unbounded.  This builder accepts an already admitted
decoded transport, preserves each literal observed numeric value and physical
missing-state/declaration, and adds exact ResponseValueRules.  It never opens,
stats, hashes or decodes the original SAV itself.
"""
from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, PhysicalSourceIncidence  # noqa: E402
from rawlsing_next.pre553_source_backed_c11_facade import (  # noqa: E402
    ExactPhysicalCellStream,
    physical_value_binding_key,
)
from rawlsing_next.source_configuration.schema import (  # noqa: E402
    SourceConfig,
    canonical_config_hash,
    validate_source_config,
)

BASE_CONFIG = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json"
SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
TARGET_SLOTS = ("q715withoutmorocco", "q716withoutmorocco")
INCOME_DECILE_SLOTS = ("q715incomedeciles", "q716incomedeciles")


class NumericDomainBindingError(ValueError):
    pass


def _sha_material(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def base_config() -> dict[str, Any]:
    return json.loads(BASE_CONFIG.read_text(encoding="utf-8"))


def base_config_hash() -> str:
    return canonical_config_hash(base_config())


def _doc(config: SourceConfig | Mapping[str, Any]) -> dict[str, Any]:
    doc = config.document if isinstance(config, SourceConfig) else config
    if not isinstance(doc, Mapping):
        raise NumericDomainBindingError("config must be SourceConfig or mapping")
    return deepcopy(dict(doc))


def _literal_token(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise NumericDomainBindingError(f"income value must be literal numeric, got {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise NumericDomainBindingError("income value must be finite")
    if isinstance(value, Decimal) and not value.is_finite():
        raise NumericDomainBindingError("income value must be finite")
    return json.dumps(value, allow_nan=False) if not isinstance(value, Decimal) else str(value)


def _label_for(slot: Mapping[str, Any], value: Any) -> str | None:
    labels = slot.get("value_labels") or {}
    for key in (str(value), str(float(value)) if isinstance(value, (int, float)) else None):
        if key is not None and key in labels:
            return labels[key]
    return None


def _state_for_label(label: str | None) -> str:
    if not label:
        return "SUBSTANTIVE_RESPONSE"
    text = label.casefold()
    if "not asked" in text:
        return "NOT_ASKED"
    if "not applicable" in text:
        return "INAPPLICABLE"
    if any(x in text for x in ("don't know", "dont know", "can't choose", "not clear")):
        return "DK" if "refus" not in text and "decline" not in text else "REFUSAL"
    if any(x in text for x in ("refus", "decline", "no answer")):
        return "REFUSAL"
    if "not interested" in text:
        return "SOURCE_SPECIFIC_SPECIAL"
    if any(x in text for x in ("missing", "unknown", "unspecified", "not provided")):
        return "MISSING"
    return "SUBSTANTIVE_RESPONSE"


V1_CONFIG = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.json"


def write_v2_config() -> dict[str, Any]:
    """Create the versioned v2 config: preserved 13 repairs + corrected income special states."""
    cfg = json.loads(V1_CONFIG.read_text(encoding="utf-8"))
    cfg["config_id"] = cfg["config_id"] + "-NUMERIC-DOMAIN"
    cfg["config_revision"] = int(cfg["config_revision"]) + 1
    for r in cfg["residuals"]:
        if r["residual_id"] == "SRC04-FIELD-REPAIR-q217":
            r["status"] = "UNRESOLVED_EXACT_UNLABELED_CODES"
            r["reason"] = ("Campaign A records 38 observed q217 cells with no exact configured value rule. "
                           "The retained codebook and physical value labels declare only 1,2,3,4,5,6,10,97,98,99; "
                           "the exact unlabeled residual codes and their meanings remain unknown and no labels are guessed. "
                           "Admitted residual values/evidence are required.")
        elif r["residual_id"] == "SRC04-FIELD-REPAIR-q715withoutmorocco":
            r["status"] = "PENDING_OBSERVED_DOMAIN_QUALIFICATION"
            r["reason"] = ("The fixed original source has a finite observed individual-income domain, but no full-source "
                           "grant is available to read it. A runtime builder accepts an already admitted decoded transport "
                           "and adds exact literal observed numeric value rules, preserving physical missing-state/declaration "
                           "and source-country currency provenance without categorical invention or currency normalization. "
                           "This is a pending observed-domain qualification, not a proved universal engine deficiency.")
        elif r["residual_id"] == "SRC04-FIELD-REPAIR-q716withoutmorocco":
            r["status"] = "PENDING_OBSERVED_DOMAIN_QUALIFICATION"
            r["reason"] = ("The fixed original source has a finite observed family-income domain, but no full-source "
                           "grant is available to read it. A runtime builder accepts an already admitted decoded transport "
                           "and adds exact literal observed numeric value rules, preserving physical missing-state/declaration "
                           "and source-country currency provenance without categorical invention or currency normalization. "
                           "This is a pending observed-domain qualification, not a proved universal engine deficiency.")
    phys = {p["name"]: p for p in cfg["physical_slots"]}
    for field in TARGET_SLOTS:
        slot = next(s for s in cfg["response_slots"] if s["slot"]["name"] == field)
        for rule in slot["values"]:
            label = _label_for(phys[field], rule.get("raw_value"))
            state = _state_for_label(label)
            if state != "SUBSTANTIVE_RESPONSE":
                rule["response_state"] = state
                rule["canonical_value"] = None
                rule["transform_authority_ref"] = None
    cfg.setdefault("notes", []).append(
        "Numeric-domain transport support: q715withoutmorocco/q716withoutmorocco literal observed values are added "
        "at runtime from an admitted decoded transport; no values are pre-read or committed by this config. "
        "Stored special codes are mapped from their exact source labels, not treated as substantive incomes.")
    validate_source_config(cfg)
    BASE_CONFIG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return cfg


def apply_observed_domain(config: SourceConfig | Mapping[str, Any], cells: Any,
                          target_slots: tuple[str, ...] = TARGET_SLOTS) -> dict[str, Any]:
    """Apply exact observed numeric value rules to the two target income slots.

    Single pass over the supplied iterable; each cell is routed by its exact
    physical slot key.  This is safe for generator/iterator transports.
    """
    doc = _doc(config)
    phys = {p["name"]: p for p in doc["physical_slots"]}
    counts: dict[str, int] = {}
    targets = tuple(target_slots)
    states: dict[str, set[str]] = {slot: set() for slot in targets}
    prepared: dict[tuple[int, str], dict[str, Any]] = {}
    for slot_name in targets:
        slot = next((s for s in doc["response_slots"] if s["slot"]["name"] == slot_name), None)
        if slot is None:
            raise NumericDomainBindingError(f"target response slot absent: {slot_name}")
        existing = {physical_value_binding_key(v["raw_value"], PhysicalMissingState(v["missing_state"]),
                                               v.get("source_missing_declaration")):
                    v for v in slot["values"]}
        prepared[(slot["slot"]["ordinal"], slot_name)] = {
            "slot": slot,
            "existing": existing,
            "template": deepcopy(slot["values"][0]),
        }
    for cell in cells:
        key = (getattr(cell, "variable_ordinal", None), getattr(cell, "variable_name", None))
        target = prepared.get(key)
        if target is None:
            continue
        slot_name = key[1]
        slot = target["slot"]
        existing = target["existing"]
        state = getattr(cell, "missing_state", None)
        declaration = getattr(cell, "source_missing_declaration", None)
        raw = getattr(cell, "raw_value", None)
        states[slot_name].add(str(state))
        physical_key = physical_value_binding_key(raw, state, declaration)
        if physical_key in existing:
            continue
        if state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raise NumericDomainBindingError(
                f"unbound missing state for {slot_name}: {state!r} declaration={declaration!r}")
        label = _label_for(phys[slot_name], raw)
        semantic = _state_for_label(label)
        if semantic != "SUBSTANTIVE_RESPONSE":
            raise NumericDomainBindingError(
                f"special stored value for {slot_name} lacks an existing rule: {raw!r} label={label!r}")
        rule = deepcopy(target["template"])
        rule["raw_value"] = raw
        rule["missing_state"] = "OBSERVED_STORAGE_VALUE"
        rule["source_missing_declaration"] = declaration
        rule["response_state"] = "SUBSTANTIVE_RESPONSE"
        # Preserve the exact literal raw value; do not claim a canonical semantic mapping.
        rule["canonical_value"] = None
        rule["transform_authority_ref"] = None
        slot["values"].append(rule)
        existing[physical_key] = rule
        counts[slot_name] = counts.get(slot_name, 0) + 1
    return {"config": doc, "added_rule_counts": counts,
            "observed_missing_states": {k: sorted(v) for k, v in states.items()}}


def build_numeric_domain_runtime_config(
    config: SourceConfig | Mapping[str, Any],
    transport: ExactPhysicalCellStream | PhysicalSourceIncidence,
    *,
    expected_source_sha256: str | None = None,
    expected_config_canonical_sha256: str | None = None,
    batch_size: int = 10_000,
    target_slots: tuple[str, ...] = TARGET_SLOTS,
) -> dict[str, Any]:
    """Build a runtime config with exact literal observed income rules.

    The transport must already be admitted; this function performs no source I/O.
    """
    doc = _doc(config)
    expected_sha = expected_source_sha256 or SOURCE_SHA256
    expected_config = expected_config_canonical_sha256 or base_config_hash()
    if doc.get("identity", {}).get("source_id") != "SRC04":
        raise NumericDomainBindingError("only SRC04 is admitted to this builder")
    if doc.get("identity", {}).get("expected_source_sha256") != SOURCE_SHA256:
        raise NumericDomainBindingError("config original source identity is not exact SRC04")
    if canonical_config_hash(doc) != expected_config:
        raise NumericDomainBindingError("foreign/mutated config hash; refusing observed-domain binding")
    if not isinstance(transport, (ExactPhysicalCellStream, PhysicalSourceIncidence)):
        raise NumericDomainBindingError("an admitted ExactPhysicalCellStream/PhysicalSourceIncidence is required")
    if transport.source_sha256 != expected_sha:
        raise NumericDomainBindingError("transport source SHA is not the expected admitted source")
    binding_sha = doc.get("binding", {}).get("source_sha256")
    if transport.source_sha256 != binding_sha:
        raise NumericDomainBindingError("transport SHA differs from config binding")
    if transport.row_count != doc.get("binding", {}).get("row_count"):
        raise NumericDomainBindingError("transport row count differs from config binding")
    targets = tuple(target_slots)
    if not all(any(s["slot"]["name"] == slot for s in doc["response_slots"]) for slot in targets):
        raise NumericDomainBindingError("config lacks an exact target income response slot")
    cells = (transport.iter_cells() if isinstance(transport, ExactPhysicalCellStream)
             else transport.iter_cells(batch_size))
    applied = apply_observed_domain(doc, cells, target_slots=targets)
    out = applied["config"]
    out["config_id"] = f"{out['config_id']}-NUMERIC-DOMAIN-RUNTIME"
    out["config_revision"] = int(out["config_revision"]) + 1
    out.setdefault("notes", []).append(
        "NUMERIC_DOMAIN_RUNTIME: exact literal observed numeric values for "
        + ",".join(targets)
        + f"; source_sha256={transport.source_sha256}; transport_rows={transport.row_count}; "
        + f"base_config={expected_config}; source-country currency literals preserved without normalization.")
    validate_source_config(out)
    return {
        "config": out,
        "base_config_canonical_sha256": expected_config,
        "transport_source_sha256": transport.source_sha256,
        "transport_row_count": transport.row_count,
        "target_slots": list(targets),
        "added_rule_counts": applied["added_rule_counts"],
        "observed_missing_states": applied["observed_missing_states"],
        "runtime_config_canonical_sha256": canonical_config_hash(out),
    }


if __name__ == "__main__":
    if "--write-v2" in sys.argv:
        write_v2_config()
    print(json.dumps({"base_config": str(BASE_CONFIG.relative_to(ROOT)),
                      "base_config_canonical_sha256": base_config_hash(),
                      "source_sha256": SOURCE_SHA256,
                      "target_slots": list(TARGET_SLOTS)}, indent=2))
