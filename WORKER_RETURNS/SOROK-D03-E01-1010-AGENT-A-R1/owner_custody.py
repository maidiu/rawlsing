"""Scoped P3 -> P2 event-write lease for the original DevelopmentOwner ABI.

The existing P3Owner.realize acquires P3Owner._root_lock before invoking
P2Owner.realize, which in turn locks recursion_owner.lock. This *adapter* uses
that SAME order and delegates actual world effects to P2Owner. It is not an
alternate owner, motive selector, source registry or event writer.

The check callback must fail closed on a P3 pending reservation, changed
P3 head/identity, changed selected source closure and mismatched source cut.
It is executed on BOTH sides of each P2 write while the P3 lock is held.
The original P2Owner still validates expected state under its own owner lock.

Limitation: processes that write directly to PsycheStore ignoring the P3Owner
root lock are outside this lease. No code-file lock and no cross-db atomicity
are implied. A direct P3 writer bypass cannot be called a held-safe proof.
"""
from __future__ import annotations

from typing import Any, Callable


class P3CoordinatedP2Owner:
    """Narrow original DevelopmentOwner forwarding adapter, no new owner state."""

    def __init__(self, p3_owner: Any, p2_owner: Any,
                 check: Callable[[], None]) -> None:
        if getattr(p3_owner, "base_owner", None) is not p2_owner:
            raise ValueError("E01_P3_P2_OWNER_BINDING")
        if not callable(getattr(p3_owner, "_root_lock", None)):
            raise ValueError("E01_P3_ROOT_LOCK_UNAVAILABLE")
        if not callable(check):
            raise TypeError("E01_CUSTODY_CHECK_REQUIRED")
        self._p3 = p3_owner
        self._p2 = p2_owner
        self._check = check

    def snapshot(self):
        return self._p2.snapshot()

    def validate_proposal(self, proposal):
        return self._p2.validate_proposal(proposal)

    def realize(self, operation_id, proposal, expected):
        # Original P3Owner.realize uses P3 -> P2 lock order. Do not reverse it.
        with self._p3._root_lock():
            self._check()
            if self._p2.snapshot() != expected:
                raise ValueError("E01_OWNER_MOVED_BEFORE_P2_REALIZE")
            result = self._p2.realize(operation_id, proposal, expected)
            self._check()
            return result


__all__ = ["P3CoordinatedP2Owner"]
