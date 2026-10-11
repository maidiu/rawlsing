"""HQ280 C02 -- independent reproduction of the F8F K4/K5 B5 publication boundary.

This script does NOT assert a policy. It records the ACTUAL typed outcome of real
invocations of the ACCEPTED B5 owner (`rawlsing_next.pre553_learned_product_lifecycle`)
and the ACCEPTED M2 owner (`rawlsing_next.pre553_learned_product_release`) in this exact
worktree, so the C02 candidate is written against observed reality rather than against a
restatement of F8F's prose.

Probes (all are caller-side mutations of a subject the caller constructed itself):
  K4   forged replay_state on an otherwise well-formed subject
  K5a  honest replay_state + forged production-looking permission ceiling
  K5b  forged replay_state + forged permission ceiling
  K5c  forged replay_state + forged receipts + forged replay root
  K6   forged CURRENT selection over a subject published under a forged closure
  K7   forged subject built directly from caller dicts (no producer at all)

Every probe calls `stage_release` -> `register_product` -> `publish_product` ->
`selection_key` -> `select_current` on the real executor and prints the actual exception
type/message, or the actual published/selected ref.

Run:  python WORKER_RETURNS/PYAT-HQ280-PV3-C02-AUTHENTICATED-B5-BOUNDARY-R1/repro/
      repro_f8f_k4_k5_boundary.py
"""
from __future__ import annotations

import json
import platform
import sys
from dataclasses import replace

sys.path.insert(0, ".")

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
)


def ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:c02-probe:{kind.lower()}:{tag}:sha256:{digest}", digest)


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", "1.0.0", semantic_hash({"authority": tag}))


def honest_subject(tag: str = "c02") -> LearnedProductLifecycleSubject:
    determinants = (ref("DETERMINANT", f"{tag}-D"),)
    return LearnedProductLifecycleSubject(
        release_ref=ref("LearnedProductRelease", f"{tag}-release"),
        product_ref=ref("LearnedSemanticProduct", f"{tag}-product"),
        product_family_ref=ref("ProductFamily", "family-A"),
        producer_owner_ref=ref("ProducerOwner", f"{tag}-owner"),
        producer_contract_ref=ref("ProducerContract", f"{tag}-contract"),
        semantic_projection_hash=semantic_hash({"semantic": tag}),
        authority_snapshot_refs=(auth(f"{tag}-semantic"),),
        direct_dependency_refs=(),
        determinant_refs=determinants,
        determinant_set_hash=semantic_hash(
            [r.as_dict() for r in sorted(determinants, key=lambda x: x.key)]
        ),
        replay_root_ref=ref("ReplayRoot", f"{tag}-replay"),
        selection_scope_ref=ref("SelectionScope", "scope-A"),
        build_or_release_receipt_refs=(ref("BuildReceipt", f"{tag}-build"),),
        producer_permission_ceiling_ref=ref("PermissionCeiling", f"{tag}-ceiling"),
        replay_state="REPLAY_BLOCKED_MISSING_AUTHORITY",
    )


def forged_ceiling() -> ExactRef:
    digest = semantic_hash({"ceiling": "urn:reviewer:PRODUCTION_GRANT"})
    return ExactRef(
        "ProducerPermissionCeiling",
        f"urn:reviewer:PRODUCTION_GRANT:sha256:{digest}",
        digest,
    )


def attempt(label: str, subject: LearnedProductLifecycleSubject) -> dict:
    executor = LearnedProductLifecycleExecutor()
    out: dict = {"probe": label}
    try:
        executor.stage_release(subject)
        out["staged"] = True
    except Exception as exc:  # noqa: BLE001
        out["staged"] = False
        out["stage_exception"] = type(exc).__name__
        out["stage_message"] = str(exc)[:200]
        return out
    try:
        executor.register_product(
            subject.release_ref,
            event_authority_ref=ref("EventAuthority", label),
            event_rule_ref=ref("EventRule", "register"),
        )
        out["registered"] = True
    except Exception as exc:  # noqa: BLE001
        out["registered"] = False
        out["register_exception"] = type(exc).__name__
        out["register_message"] = str(exc)[:200]
        return out
    try:
        executor.publish_product(
            subject.release_ref,
            event_authority_ref=ref("EventAuthority", label),
            event_rule_ref=ref("EventRule", "publish"),
        )
        out["published"] = True
        out["publication_event_ref"] = executor.events[-1].ref.object_id
    except Exception as exc:  # noqa: BLE001
        out["published"] = False
        out["publish_exception"] = type(exc).__name__
        out["publish_message"] = str(exc)[:200]
        return out
    out["publication_payload_ceiling"] = (
        executor.events[-1].payload.get("producer_permission_ceiling", {}).get("object_id")
    )
    try:
        key = executor.selection_key(
            product_family_ref=subject.product_family_ref,
            selection_scope_ref=subject.selection_scope_ref,
            selection_purpose_ref=ref("SelectionPurpose", "serve"),
        )
        receipt = executor.select_current(
            key.ref,
            subject.release_ref,
            expected_previous_receipt_ref=None,
            event_authority_ref=ref("EventAuthority", label),
            event_rule_ref=ref("EventRule", "select"),
            selection_attestation_ref=ref("SelectionAttestation", label),
        )
        out["current_selected"] = True
        out["current_receipt_ref"] = receipt.ref.object_id
    except Exception as exc:  # noqa: BLE001
        out["current_selected"] = False
        out["select_exception"] = type(exc).__name__
        out["select_message"] = str(exc)[:200]
    return out


def main() -> None:
    honest = honest_subject()
    probes = [
        ("K4-forged-replay-state", replace(honest, replay_state="REPLAY_COMPLETE")),
        (
            "K5a-honest-replay-state-forged-production-ceiling",
            replace(honest, producer_permission_ceiling_ref=forged_ceiling()),
        ),
        (
            "K5b-forged-replay-state-forged-production-ceiling",
            replace(
                honest,
                replay_state="REPLAY_COMPLETE",
                producer_permission_ceiling_ref=forged_ceiling(),
            ),
        ),
        (
            "K5c-forged-replay-state-forged-receipts-and-replay-root",
            replace(
                honest,
                replay_state="REPLAY_COMPLETE",
                replay_root_ref=ref("ReplayRoot", "forged-root"),
                build_or_release_receipt_refs=(ref("BuildReceipt", "forged-receipt"),),
            ),
        ),
        (
            "K7-forged-subject-from-caller-dicts-no-producer",
            LearnedProductLifecycleSubject(
                **{
                    **{
                        k: v
                        for k, v in honest.as_dict().items()
                        if k not in ("replay_state", "rebuild_state", "materialization_class")
                    },
                    "replay_state": "REPLAY_COMPLETE",
                    "replay_root_ref": ref("ReplayRoot", "alien-root").as_dict(),
                }
            ),
        ),
    ]
    results = [attempt(label, subject) for label, subject in probes]
    report = {
        "worktree_head": __import__("subprocess").run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "b5_owner": "rawlsing_next.pre553_learned_product_lifecycle"
        ".LearnedProductLifecycleExecutor",
        "observed": results,
        "published_probes": [r["probe"] for r in results if r.get("published")],
        "current_selected_probes": [
            r["probe"] for r in results if r.get("current_selected")
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print(
        "\nC02 OBSERVED: %d/%d caller-constructed subjects reached PUBLISHED and %d/%d "
        "reached CURRENT_SELECTED."
        % (
            len(report["published_probes"]),
            len(results),
            len(report["current_selected_probes"]),
            len(results),
        )
    )


if __name__ == "__main__":
    main()