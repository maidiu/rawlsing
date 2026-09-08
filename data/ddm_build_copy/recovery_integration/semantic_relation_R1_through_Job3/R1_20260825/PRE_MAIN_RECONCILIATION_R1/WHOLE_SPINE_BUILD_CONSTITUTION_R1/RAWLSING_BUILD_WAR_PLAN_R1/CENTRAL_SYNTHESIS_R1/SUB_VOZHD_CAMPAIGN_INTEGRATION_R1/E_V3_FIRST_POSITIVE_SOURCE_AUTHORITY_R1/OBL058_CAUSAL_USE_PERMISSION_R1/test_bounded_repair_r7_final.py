"""Final producer verification surface for OBL058 R7.

Two CPython-mechanics checks are replaced with deterministic forms. All other
R7 producer checks are inherited unchanged from the pre-freeze test surface.
"""
from __future__ import annotations

import causal_use_permission_candidate_r7 as candidate
from causal_use_permission_candidate_r7 import IssuedReceipt
from test_bounded_repair_r7 import OBL058BoundedRepairR7Court as _BaseCourt


class OBL058BoundedRepairR7Court(_BaseCourt):
    def test_r7_05_native_reservation_exposes_no_python_mutable_pin_handle(self):
        receipt = self.positive()
        self.assertFalse(hasattr(candidate._native, "pinned_receipts"))
        self.assertFalse(hasattr(candidate._native, "pin_head"))
        self.assertFalse(hasattr(candidate._native, "authority_key"))
        self.assertFalse(hasattr(receipt, "__dict__"))

    def test_r7_09_direct_constructor_and_object_new_are_unissued(self):
        self.assert_origin_rejected(IssuedReceipt())
        try:
            fabricated = object.__new__(IssuedReceipt)
        except TypeError:
            return
        self.assert_origin_rejected(fabricated)
