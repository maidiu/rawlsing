"""T9S capability probes — Phase B signature-only binding to the T9D API.

Phase A shipped the pure-probe version (raised ``CapabilityUnavailable`` on the
T9C adapter, which lacked ``archival_known_at_upper_year`` and ``SourceGrant``).
Phase B adds the disclosed signature-only binding to the pinned T9D public API:
it performs actual candidate calls and supplies no external filter, no injected
permission decision and no output rewrite.

The two unavailable-capability probes now bind to:
  * ``evaluate(..., archival_known_at_upper_year=...)``  (F5 / D04)
  * ``read_selected_world(..., source_grant=SourceGrant(...), require_source_grant=True)``
    (F6 / D16 / D17 / D17_WRONG_OWNER)

A probe still raises ``CapabilityUnavailable`` if the candidate API has no
representation for the capability — a RED, never a green.
"""
from __future__ import annotations

import inspect


class CapabilityUnavailable(AssertionError):
    """A frozen capability has no candidate API representation."""


def _sig(params, *names):
    return next((n for n in names if n in params), None)


def archival_known_at_evaluate(T, case, method, clock_year, known_at_year):
    sig = inspect.signature(T.evaluate)
    name = _sig(sig.parameters, "archival_known_at_upper_year",
                "archival_known_at_year", "known_at_year", "archive_known_at_year")
    if name is None:
        raise CapabilityUnavailable(
            "D04: evaluate has no archival known-at upper year; a dated archive "
            "snapshot bound cannot be represented without forbidden filtering")
    return T.evaluate(case, method, clock_year=clock_year, retrospective=True,
                      **{name: known_at_year})


def granted_source_read(T, case, method, clock_year, *, grant_edition=None,
                        grant_current=True, grant_owner=None,
                        grant_source_family="ACTUAL_SOURCE"):
    sig = inspect.signature(T.read_selected_world)
    param = _sig(sig.parameters, "source_grant", "source_edition_grant", "grant")
    if param is None or not hasattr(T, "SourceGrant"):
        raise CapabilityUnavailable(
            "D16/D17/D17_WRONG_OWNER: source-edition/currentness/owner grant pair "
            "has no candidate API representation; refusing to invent a permission gate")
    grant = T.SourceGrant(
        grant_source_family=grant_source_family,
        grant_edition=grant_edition,
        grant_current=grant_current,
        grant_source_owner=grant_owner or "")
    world = T.StructuralWorld("W_SYNTH", ("ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
                              (), "SYNTH_INSTITUTION")
    return T.read_selected_world(world, case, method, clock_year,
                                 source_grant=grant, require_source_grant=True)
