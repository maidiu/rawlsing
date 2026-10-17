"""T9S capability probes for the two unavailable-capability falsifiers.

These are signature-only probes: they call the pinned candidate API if it has a
representation for the capability, and raise a typed ``CapabilityUnavailable``
when it does not.  No external filtering, permission decision or output rewrite
is supplied; the missing capability stays a RED, never a green.
"""
from __future__ import annotations

import inspect


class CapabilityUnavailable(AssertionError):
    """A frozen capability has no candidate API representation."""


def archival_known_at_evaluate(T, case, method, clock_year, known_at_year):
    """A retrospective read bounded to what was known by ``known_at_year``.

    D04: a 2030-published observation must not be knowable at a 2020 archive
    bound.  Accept any candidate parameter that names an archival known-at upper
    bound; otherwise the capability is unavailable.
    """
    sig = inspect.signature(T.evaluate)
    for name in ("archival_known_at_upper_year", "archival_known_at_year",
                 "known_at_year", "archive_known_at_year"):
        if name in sig.parameters:
            return T.evaluate(case, method, clock_year=clock_year,
                              retrospective=True, **{name: known_at_year})
    raise CapabilityUnavailable(
        "D04: evaluate has no archival known-at upper year; a 2020 snapshot "
        "cannot be represented without forbidden reviewer filtering")


def granted_source_read(T, case, method, clock_year, *, grant_edition=None,
                        grant_current=True, grant_owner=None):
    """A read carrying an explicit source-edition / currentness / owner grant.

    D16/D17/D17_WRONG_OWNER: a grant for a different edition, an expired grant,
    or a wrong owner must refuse; a clock flag must not resurrect it.  If the
    candidate exposes no grant-pair representation, the capability is unavailable.
    """
    sig = inspect.signature(T.read_selected_world)
    candidates = (
        ("source_grant", dict(source_grant=dict(
            edition=grant_edition, current=grant_current, owner=grant_owner))),
        ("source_edition_grant", dict(source_edition_grant=dict(
            edition=grant_edition, current=grant_current, owner=grant_owner))),
        ("grant", dict(grant=dict(edition=grant_edition, current=grant_current,
                                  owner=grant_owner))),
    )
    for name, payload in candidates:
        if name in sig.parameters:
            return T.read_selected_world(
                T.StructuralWorld("W_SYNTH", ("ROUTE_PARTICIPATION",), (),
                                  "SYNTH_INSTITUTION"),
                case, method, clock_year, **payload)
    raise CapabilityUnavailable(
        "D16/D17/D17_WRONG_OWNER: source-edition/currentness/owner grant pair "
        "has no candidate API representation; refusing to invent a permission gate")
