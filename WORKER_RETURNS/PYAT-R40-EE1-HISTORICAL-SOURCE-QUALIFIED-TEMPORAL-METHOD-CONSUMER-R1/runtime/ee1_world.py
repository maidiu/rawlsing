"""Load the staged accepted T35 two-epoch world exactly."""
from __future__ import annotations

from pathlib import Path

import bootstrap  # staged
import two_epoch_world as W  # staged
import n8e_sourcefree_comparator as N8E  # staged

from ee1_paths import STAGED_WORLD


def assert_staged() -> None:
    for module in (bootstrap, W, N8E):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(STAGED_WORLD), f"non-staged import: {path}"


def serve_two_epochs():
    """Serve both accepted epochs through the actual consumer pipeline."""
    assert_staged()
    adapter1 = W.make_adapter()
    adapter2 = W.make_adapter()
    e1 = W.serve(adapter1, W.E1)
    e2 = W.serve(adapter2, W.E2)
    return e1, e2, (adapter1, adapter2)
