"""Targetless C12 product shared by lawful SHARE_TOOL and REFUSE_TOOL.

The C12/world representation is derived from the actual M35 life and C8 source.
A's tool state comes from B's performed operation, never from an invented
psychology or a synthetic replacement ledger. The product is not a native C12.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

from joined.refusal import (  # noqa: E402
    _RefusalSeed,
    _sidecar_document,
    RefusalProduct,
    _read_c8_source,
)
from r26e.c12_integrity import QualifiedC12Store  # noqa: E402

GRADE = "TEST_ONLY_SOURCEFREE_TARGETLESS_C12_NOT_NATIVE"
EPISODE_KIND = "S36_TARGETLESS_RESPONSE"


class S37Seed(_RefusalSeed):
    """M35-life seed with A tool state derived from B's performed operation."""

    def __init__(self, life, source, c8_state_digest, e1_event_hash):
        super().__init__(life, source, c8_state_digest, e1_event_hash)
        share = source.get("b_operation") == "SHARE_TOOL"
        self.world.actor_state["A"]["tools_remaining"] = 1 if share else 0
        self.world.resources.setdefault("workshop", {})["tool_available"] = share


class S37TargetlessProduct(RefusalProduct):
    """Persistent C12/world representation with no C9 target."""

    def __init__(
        self,
        root,
        *,
        life,
        source: Mapping[str, Any],
        c8_binding: Mapping[str, Any],
        variant: str,
        s36_binding: Mapping[str, Any] | None = None,
        write_sidecar: bool = False,
        branch_id: str = "root",
        sidecar_document: Mapping[str, Any] | None = None,
    ) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.source = dict(source)
        self.c8_binding = dict(c8_binding)
        self.variant = variant
        self.s36_binding = dict(s36_binding or {})
        self.sidecar = (
            dict(sidecar_document)
            if sidecar_document is not None
            else _sidecar_document(self.source, self.c8_binding, variant)
        )
        self.sidecar["s36"] = self.s36_binding
        self.sidecar["source_operation"] = self.source.get("b_operation")
        self.sidecar["material_access"] = (
            "granted"
            if self.source.get("b_operation") == "SHARE_TOOL"
            else "denied"
        )
        self.sidecar_path = self.root / "targetless.json"
        if write_sidecar and not self.sidecar_path.exists():
            self.sidecar_path.write_text(
                json.dumps(self.sidecar, indent=2, sort_keys=True) + "\n",
                encoding="utf8",
            )
        self.seed = S37Seed(
            life,
            self.source,
            self.c8_binding["c8_state_digest"],
            self.c8_binding["e1_event_hash"],
        )
        self.store = QualifiedC12Store(self.root / "c12.sqlite")
        self.branch_id = branch_id
        self._ensure_root()

    def s36_episode(self) -> dict | None:
        rows = [
            row
            for row in self.store.episodes(self.branch_id)
            if row.get("kind") == EPISODE_KIND
        ]
        return rows[-1] if rows else None

    def s36_episode_body(self) -> dict | None:
        row = self.s36_episode()
        return dict(row.get("body") or {}) if row else None


def validate_s37_product(
    product: S37TargetlessProduct,
    meta: Mapping[str, Any],
    sidecar: Mapping[str, Any],
    branch_id: str,
) -> dict:
    """Compare the session, C12, C8 and S36 bindings without a copied summary."""
    checks: dict[str, bool] = {}
    observed: dict = {}
    try:
        source = dict(product.source)
        c8 = dict(meta.get("c8") or {})
        s36 = dict(meta.get("s36") or {})
        c8_source, c8_event = _read_c8_source(c8)
        seed = product.seed.public()
        custody = product.seed.custody()
        expected_map = {
            "TEST_ONLY_R31J_A": seed.get("actor_a"),
            "TEST_ONLY_R31J_B": seed.get("actor_b"),
        }
        payload = c8_event.get("payload") or {}
        actor = payload.get("actor") or {}
        other = payload.get("other_actor") or {}
        episode = product.s36_episode_body() or {}
        world = product._world(branch_id)
        share = source.get("b_operation") == "SHARE_TOOL"
        checks.update(
            {
                "source_matches_meta": source == dict(meta.get("source") or {}),
                "source_matches_c8": source == c8_source,
                "source_matches_sidecar": source == dict(sidecar.get("j_source") or {}),
                "source_operation_lawful": source.get("b_operation")
                in {"SHARE_TOOL", "REFUSE_TOOL"},
                "source_performed": source.get("b_performed") is True,
                "c8_matches_sidecar": c8 == dict(sidecar.get("c8") or {}),
                "s36_matches_sidecar": s36 == dict(sidecar.get("s36") or {}),
                "meta_case_matches_source": meta.get("case") == source.get("b_operation"),
                "source_actor_map": meta.get("source_actor_map") == expected_map,
                "c8_actor_is_seed_a": actor.get("actor_id") == seed.get("actor_a"),
                "c8_other_is_seed_b": other.get("actor_id") == seed.get("actor_b"),
                "source_b_is_seed_b": source.get("b_actor") == "TEST_ONLY_R31J_B",
                "source_b_to_is_seed_a": source.get("b_to_actor") == "TEST_ONLY_R31J_A",
                "meta_c8_matches_sidecar": meta.get("c8")
                == dict(sidecar.get("c8") or {}),
                "meta_e1_matches_sidecar": s36.get("e1_event_hash")
                == c8.get("e1_event_hash"),
                "c8_state_digest_matches_seed": custody.get("c8_state_digest")
                == c8.get("c8_state_digest"),
                "e1_hash_matches_seed": custody.get("e1_event_hash")
                == c8.get("e1_event_hash"),
                "c12_source_matches": episode.get("source") == source,
                "c12_c8_matches": episode.get("c8") == c8,
                "c12_s36_matches": episode.get("s36") == s36,
                "targetless_meta": meta.get("targetless") is True,
                "target_id_absent": meta.get("target_id") == ""
                and s36.get("target_id") == ""
                and (sidecar.get("target_id") == "")
                and episode.get("target_id", "") == "",
                "target_branch_no_change": s36.get("target_branch") == "NO_CHANGE",
                "target_reason_no_proposal": s36.get("target_reason")
                == "NO_PROPOSAL",
                "target_proposals_zero": s36.get("target_proposals") == 0,
                "tool_state_matches_source": world.actor_state["A"].get(
                    "tools_remaining"
                )
                == (1 if share else 0),
                "material_access_matches_source": s36.get("material_access")
                == ("granted" if share else "denied"),
                "native_grants_false": all(
                    value is False for value in custody["native_grants"].values()
                ),
                "no_native_sidecar": sidecar.get("native") is False,
                "root_actors_a_b": sorted(
                    product.store.branch("root").get("actor_ids", [])
                )
                == ["A", "B"],
                "branch_has_user": "U"
                in product.store.branch(branch_id).get("actor_ids", []),
                "c12_root_ok": bool(product.c12_verify("root").get("ok")),
                "c12_branch_ok": bool(product.c12_verify(branch_id).get("ok")),
            }
        )
        observed.update(
            {
                "source_operation": source.get("b_operation"),
                "source_b_event_hash": source.get("b_event_hash"),
                "c8_occurrence_id": c8.get("occurrence_id"),
                "c8_state_digest": c8.get("c8_state_digest"),
                "e1_event_hash": c8.get("e1_event_hash"),
                "response_ref": s36.get("response_ref"),
                "c9_receipt_hash": s36.get("c9_receipt_hash"),
                "target_branch": s36.get("target_branch"),
                "target_reason": s36.get("target_reason"),
                "tools_remaining": world.actor_state["A"].get("tools_remaining"),
                "source_actor_map": meta.get("source_actor_map"),
                "seed_actors": {
                    "a": seed.get("actor_a"),
                    "b": seed.get("actor_b"),
                },
            }
        )
    except Exception as exc:  # a missing binding is a failed check, not a pass
        checks["binding_readable"] = False
        observed["error"] = type(exc).__name__ + ":" + str(exc)
    checks.setdefault("binding_readable", True)
    return {"ok": all(checks.values()), "checks": checks, "observed": observed}


__all__ = [
    "EPISODE_KIND",
    "GRADE",
    "S37Seed",
    "S37TargetlessProduct",
    "validate_s37_product",
]
