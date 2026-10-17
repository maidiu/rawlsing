from __future__ import annotations

from dataclasses import fields
import inspect

import rawlsing_next.gt34_u2_v3p1_authenticated_subject_materializer as u2


def test_shadow_receipt_surface_cannot_carry_production_identity_or_schema() -> None:
    shadow_fields = {field.name for field in fields(u2._ShadowReceipt)}
    assert "materializer_id" not in shadow_fields
    assert "materializer_version" not in shadow_fields

    source = "\n".join(
        [
            inspect.getsource(u2._ShadowReceipt),
            inspect.getsource(u2._materialize_noncurrent_shadow_fixture),
        ]
    )
    assert "NONCURRENT_SYNTHETIC_SHADOW_RECEIPT@1.0.0" in source
    assert u2.MATERIALIZER_ID not in source
    assert u2.MATERIALIZER_VERSION not in source
    assert u2.RECEIPT_SCHEMA not in source
