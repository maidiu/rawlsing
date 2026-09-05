"""Single bounded insertion seam for the real current GT2 constructor payload.

Worker B intentionally leaves this symbol empty.  Fan-in may replace only the RHS
of ``CURRENT_GT2_PAYLOAD`` with one immutable ``RepoNativeSealPayload(...)`` built
from Worker A's actual ordinary current ``EmpiricalQuerySpec`` + ``EmpiricalFact``.
No source rows, Library paths, caller-selected authorities, or identity overrides
belong here.
"""
from __future__ import annotations

from typing import Final

from rawlsing_next.pre553_repo_native_seal import RepoNativeSealPayload

CURRENT_GT2_PAYLOAD: Final[RepoNativeSealPayload | None] = None

__all__ = ["CURRENT_GT2_PAYLOAD"]
