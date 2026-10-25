"""Source-owner boundary for S48 prospective other-actor operations.

No independently owned/current B source or performer is present in the accepted
same-root S42/S47 consumer. S48 must not author a B refusal body or infer one
from actor material state; this module therefore exposes no positive candidate
and returns an explicit source-owner hold until an actual owner-issued source
exists.
"""
from __future__ import annotations

from .errors import S48Refusal

MISSING_FUNCTION = "S48_MISSING_INDEPENDENT_CURRENT_B_SOURCE_PERFORMER"
SOURCE_OWNER_HOLD = "S48_SOURCE_OWNER_HOLD_NO_CURRENT_OWNER_ADMISSION"


def candidate_specs(session=None) -> list[dict]:
    return []


def eligible_candidate_ids(session=None) -> list[str]:
    return []


def issue_current_source(session, candidate_id: str):
    raise S48Refusal(SOURCE_OWNER_HOLD, MISSING_FUNCTION)


__all__ = [
    "MISSING_FUNCTION", "SOURCE_OWNER_HOLD", "candidate_specs",
    "eligible_candidate_ids", "issue_current_source",
]
