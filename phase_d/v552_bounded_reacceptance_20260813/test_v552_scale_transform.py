import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE" / "runtime_reproducibility_code"))

from data.ddm_build_copy.ddm_v552_structural import (  # noqa: E402
    _source_response_intensity,
    resolve_v552_distribution_intensity_representation,
    resolve_v552_signed_component,
)


def _row(*, code, direction, supplied, rank, scale_direction="descending", reversal="none"):
    return {
        "response_direction": direction,
        "response_intensity": supplied,
        "ordinal_rank": rank,
        "scale_min": 1,
        "scale_max": 4,
        "scale_direction": scale_direction,
        "relation_projection_polarity": reversal,
        "response_topology": "scalar",
    }


def test_supplied_coordinate_precedes_ordinal_fallback_and_preserves_zero():
    positive = _row(code=1, direction="positive", supplied=1.0, rank=1)
    negative_zero = _row(code=4, direction="negative", supplied=0.0, rank=4)
    assert _source_response_intensity(positive) == (1.0, "response_intensity")
    assert _source_response_intensity(negative_zero) == (0.0, "response_intensity")
    group = __import__("pandas").DataFrame([positive, negative_zero])
    rep = resolve_v552_distribution_intensity_representation(group)
    assert rep.representation_class == "NORMALIZED_AXIS_COORDINATE_0_1"
    assert resolve_v552_signed_component(positive, rep).canonical_signed_component == 1.0
    assert resolve_v552_signed_component(negative_zero, rep).canonical_signed_component == -1.0


def test_ordinal_fallback_applies_descending_scale_once():
    positive = _row(code=1, direction="positive", supplied=None, rank=1)
    negative = _row(code=4, direction="negative", supplied=None, rank=4)
    assert _source_response_intensity(positive)[0] == 1.0
    assert _source_response_intensity(negative)[0] == 0.0


def test_projection_reversal_does_not_change_source_scale_coordinate():
    row = _row(code=1, direction="positive", supplied=1.0, rank=1, reversal="reverse_driver")
    assert _source_response_intensity(row) == (1.0, "response_intensity")
