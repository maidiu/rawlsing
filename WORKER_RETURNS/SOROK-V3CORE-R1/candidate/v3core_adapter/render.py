"""Render-only expression with an explicit backbone nonmutation court."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from v3.core.derived import DerivedIndices
from v3.core.invariants import backbone_hash
from v3.core.state import BackboneState
from v3.render.phenomenology import render_year

from .contracts import Status
from .derived_scope import PublishedDerived
from .provenance import digest

Renderer = Callable[[BackboneState, DerivedIndices | None, dict[str, Any]], None]


@dataclass(frozen=True)
class RenderOutcome:
    """Result of one render pass."""

    status: Status
    backbone_hash_before: str
    backbone_hash_after: str
    rendered_output_hash: str
    reason: str = ""


def render_readonly(
    state: BackboneState,
    published: PublishedDerived | None,
    *,
    renderer: Renderer | None = None,
    config: dict[str, Any] | None = None,
) -> RenderOutcome:
    """Render expression without permitting any backbone mutation.

    The actual historical renderer is the default. Any renderer that mutates a
    non-rendered backbone field is refused and its mutation is rolled back.
    """
    renderer = renderer or render_year
    before = backbone_hash(state)
    snapshot = deepcopy(state)
    try:
        renderer(state, None, dict(config or {}))
    except Exception as exc:
        state.__dict__.clear()
        state.__dict__.update(snapshot.__dict__)
        return RenderOutcome(
            status=Status.HELD_TRANSACTION_ABORTED,
            backbone_hash_before=before,
            backbone_hash_after=backbone_hash(state),
            rendered_output_hash="",
            reason=f"{type(exc).__name__}:{exc}",
        )
    after = backbone_hash(state)
    if after != before:
        state.__dict__.clear()
        state.__dict__.update(snapshot.__dict__)
        return RenderOutcome(
            status=Status.HELD_RENDERER_MUTATION,
            backbone_hash_before=before,
            backbone_hash_after=backbone_hash(state),
            rendered_output_hash="",
            reason="renderer_mutated_backbone",
        )
    if not isinstance(state.rendered_output, dict):
        state.rendered_output = {}
    state.rendered_output["material_scope"] = published.as_dict() if published else {"status": "HELD"}
    state.rendered_output["derived_publication_status"] = "SCOPED_MATERIAL_ONLY"
    return RenderOutcome(
        status=Status.DERIVED_EVALUATED_SCOPED,
        backbone_hash_before=before,
        backbone_hash_after=backbone_hash(state),
        rendered_output_hash=digest(state.rendered_output),
    )
