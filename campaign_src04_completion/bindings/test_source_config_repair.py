import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config, validate_source_config


def _config():
    return json.loads((ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.json").read_text())


def test_old_config_preserved():
    d = json.loads((ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json").read_text())
    assert canonical_config_hash(d) == "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"


def test_repaired_config_is_schema_valid_and_keeps_178_3():
    cfg = _config()
    validate_source_config(cfg)
    assert len(cfg["response_slots"]) == 178
    assert len(cfg["coordinate_slots"]) == 3
    assert len(cfg["physical_slots"]) == 181
    assert len(cfg["items"]) == 181


def test_scale_fields_have_exact_2_through_9():
    cfg = _config()
    for field in [f"q{n}" for n in range(235, 245)]:
        slot = next(s for s in cfg["response_slots"] if s["slot"]["name"] == field)
        values = {v["raw_value"] for v in slot["values"] if v.get("raw_value") is not None}
        assert set(range(1, 11)).issubset(values), field


def test_income_decile_fields_have_1_through_10():
    cfg = _config()
    for field in ("q715incomedeciles", "q716incomedeciles"):
        slot = next(s for s in cfg["response_slots"] if s["slot"]["name"] == field)
        values = {v["raw_value"] for v in slot["values"] if v.get("raw_value") is not None}
        assert set(range(1, 11)).issubset(values), field


def test_q701_has_system_missing_coordinate_rule():
    cfg = _config()
    slot = next(s for s in cfg["coordinate_slots"] if s["slot"]["name"] == "q701")
    assert slot["copy_observed_raw"] is True
    assert any(v.get("raw_value") is None and v.get("missing_state") == "SYSTEM_MISSING"
               and v.get("coordinate_state") == "MISSING" for v in slot["values"])


def test_unresolved_fields_have_exact_residuals():
    cfg = _config()
    residuals = {r["residual_id"]: r for r in cfg["residuals"]}
    for field in ("q217", "q715withoutmorocco", "q716withoutmorocco"):
        key = f"SRC04-FIELD-REPAIR-{field}"
        assert key in residuals
        assert residuals[key]["field"]
        assert residuals[key]["reason"]
        assert residuals[key]["dependent_operation"]
        assert residuals[key]["unaffected_scope"]


def test_ledger_covers_all_181_slots_and_preserves_old_hash():
    ledger = json.loads((ROOT / "campaign_src04_completion/bindings/FIELD_REPAIR_LEDGER.json").read_text())
    assert ledger["old_config_canonical_sha256"] == "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
    assert ledger["counts"]["physical_slots"] == 181
    assert len(ledger["entries"]) == 181
    assert {e["ordinal"] for e in ledger["entries"]} == set(range(1, 182))
    assert ledger["counts"]["repaired_fields"] == 13
    assert ledger["counts"]["unresolved_fields"] == 3


def test_field_evidence_covers_16_fields_and_declares_labels():
    ev = json.loads((ROOT / "campaign_src04_completion/bindings/FIELD_REPAIR_EVIDENCE.json").read_text())
    assert len(ev["entries"]) == 16
    codes = {e["field"]: e["codebook"]["response_options_all"] for e in ev["entries"]}
    assert "2 = 2" in codes["q235"] and "9 = 9" in codes["q244"]
    assert "1 = 1 first decile" in codes["q715incomedeciles"]
    unresolved = {e["field"] for e in ev["entries"] if e["unresolved"]}
    assert unresolved == {"q217", "q715withoutmorocco", "q716withoutmorocco"}
