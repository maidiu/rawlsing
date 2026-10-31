"""Required full-history refusal properties: preserve their actual REDs."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f1c as F


@pytest.mark.parametrize("changed_input", ["A", "B", "shared_witness"])
def test_changed_live_prior_is_refused(tmp_path, changed_input):
    life, frozen, expected = F.freeze()
    if changed_input in {"A", "B"}:
        ledger = life.a_ledger if changed_input == "A" else life.b_ledger
        event = next(e for e in ledger.events if e.kind == "RELATION_VIEW")
        event.payload["perceived_state"] = "F1CI3_POST_FREEZE_DRIFT"
        assert ledger.verify()[0] is False
    else:
        life.witness["status"] = "F1CI3_POST_FREEZE_NOT_WITNESSED"
    # The accepted frozen bytes are unchanged. A consumer must refuse the
    # independently changed live prehistory instead of proving a different one.
    assert F.digest(frozen) == expected
    with pytest.raises(F.Hold):
        F.same_receiver_assertion(tmp_path, life, frozen, expected)
