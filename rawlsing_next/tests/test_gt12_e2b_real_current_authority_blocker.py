from __future__ import annotations

import inspect

from rawlsing_next import gt12_d_to_m4_typed_bridge as d_to_m4
from rawlsing_next.gt12_e2b_publication_governance_binding import (
    load_current_gt12_e2b_publication_governance_binding,
)
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_AUTHORITY_REF,
    ADOPTED_PRODUCER_ALLOWED_USES,
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
)
from rawlsing_next.tests import gt12_e2b_actual_object_consumer_harness as harness


def _required_parameter(fn, name: str) -> None:
    param = inspect.signature(fn).parameters[name]
    assert param.default is inspect.Parameter.empty


def test_real_current_e2b_publication_authority_seam_is_now_fixed_and_caller_nonselectable():
    assert ADOPTED_AUTHORITY_REF.authority_hash == (
        "d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c"
    )
    assert ADOPTED_PRODUCER_ALLOWED_USES == ("CONTEXT",)
    assert ADOPTED_V557_ALLOWED_USES == ("CONTEXT",)
    assert ADOPTED_V558_REQUESTED_USES == ("CONTEXT",)

    current = load_current_gt12_e2b_publication_governance_binding()
    assert current.bundle_content_hash == (
        "f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14"
    )
    assert tuple(
        inspect.signature(harness.run_current_r1c_e2b_actual_objects).parameters
    ) == ("query", "fact")
    for name in (
        "governed_use_id",
        "v554_rule_ref",
        "publication_authority",
        "v557_authority_ref",
    ):
        assert name not in inspect.signature(
            harness.run_current_r1c_e2b_actual_objects
        ).parameters

    # Generic lower-level bridge APIs remain explicit/parameterized; only the
    # real current E2B entry is fixed to the adopted current provider.
    for name in ("governed_use_id", "v554_rule_ref", "publication_authority"):
        _required_parameter(d_to_m4.evaluate_typed_d_to_e_at_v554, name)
    _required_parameter(
        d_to_m4.publish_and_resolve_relation_v554_at_current_m4,
        "v557_authority_ref",
    )
