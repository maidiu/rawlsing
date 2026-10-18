"""WG0N independent hostile source-view / release-identity attack transport.

Constructs the 17 preregistered attacks against the release-view / source-snapshot
/ issuer admission seam and reports the same result shape as the parent WG0M
descriptor court. Reviewer-side construction only: no author source is edited,
and this module never imports a candidate by itself -- the inherited
``phase_b_support_v1`` transport supplies the fixture and the physical module
verification.

PHASE A: this adapter is FROZEN BEFORE WG0P6 was read.
PHASE B: execute it against the independently staged WG0P6 candidate.
"""
from __future__ import annotations

import copy
import json
import os
import pathlib
import sys
from dataclasses import replace

R = pathlib.Path(__file__).resolve().parents[1]

# The reviewer transport is resolved from sys.path so that the candidate's own
# identity bootstrap (sitecustomize) can wire it first. Nothing here forces a
# specific source root: the physical owner verification is the bootstrap's job.
import phase_b_support_v1 as S  # noqa: E402
from phase_b_support_v1 import plan, execute, profile_calls, dump  # noqa: E402

OP = S.OP
REL1 = "REL-A-W1"
REL2 = "REL-A-W2"

# Refusal tokens the parent court already recognises as typed refusals.
TYPED_TOKENS = ("HELD", "INADMISSIBLE", "REVOKED", "STALE", "REFUSED", "UNAVAILABLE")


def _typed_refusal(exc_name, exc_reason):
    """Derive a typed refusal token from an exception, else None."""
    if exc_name is None:
        return None
    blob = f"{exc_name} {exc_reason or ''}".upper()
    for tok in TYPED_TOKENS:
        if tok in blob:
            return tok
    # An exception type that is one of the law's typed error families is itself
    # the typed refusal; an untyped KeyError/TypeError is NOT (it is a RED).
    if exc_name in ("IdentityError", "FrontierError", "RevocationError",
                    "ColdRestartError", "NativeDataError", "BatchIntegrityError"):
        return "REFUSED"
    return None


def _mutate_source_view(p, rel_key, **fields):
    rels = dict(p.releases)
    rel = rels[rel_key]
    rel = replace(rel, **fields)
    rels[rel_key] = rel
    return replace(p, releases=rels)


class HostileSourceViewCourt:
    """Independent construction of the preregistered hostile controls."""

    def __init__(self):
        self.physical = S.verified_modules()
        self.out = (R / "observations/hostile_runs") / os.environ.get("WG0N_RUN", "phase_a_frozen")
        self.out.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    def execute_case(self, group: str, case: str) -> dict:
        p = plan()
        unit = p.units_by_op[OP]
        rel1 = p.releases[REL1]
        rel2 = p.releases[REL2]
        stimulus = {}
        p2 = p

        # ---- A: release-source-view substitution -------------------------
        if group == "release_source_view_substitution":
            if case == "A1_genuine_foreign_pointer":
                p2 = _mutate_source_view(p, REL1, source_artifact_ref=rel2.source_artifact_ref)
                stimulus = {"swap": "source_artifact_ref", "from": REL2, "to": REL1}
            elif case == "A2_coherent_full_source_view":
                p2 = _mutate_source_view(p, REL1,
                                         source_artifact_ref=rel2.source_artifact_ref,
                                         source_edition=rel2.source_edition,
                                         universe_ref=rel2.universe_ref)
                stimulus = {"swap": "coherent_triple", "from": REL2, "to": REL1}
            elif case == "A3_pointer_and_edition_foreign_universe_own":
                p2 = _mutate_source_view(p, REL1,
                                         source_artifact_ref=rel2.source_artifact_ref,
                                         source_edition=rel2.source_edition)
                stimulus = {"swap": "partial_triple", "universe_ref": "kept_own"}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- B: reused source pointer -----------------------------------
        elif group == "reused_source_pointer":
            if case == "B1_one_pointer_two_releases":
                # Force both releases to claim the SAME snapshot pointer.
                p2 = _mutate_source_view(p, REL2, source_artifact_ref=rel1.source_artifact_ref)
                stimulus = {"alias": "one_source_artifact_ref_two_releases",
                            "shared_by": [REL1, REL2]}
            elif case == "B2_pointer_reused_across_universes":
                p2 = _mutate_source_view(p, REL2,
                                         source_artifact_ref=rel1.source_artifact_ref,
                                         universe_ref=rel1.universe_ref)
                stimulus = {"alias": "pointer_reused_across_universes"}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- C: source epoch / revocation -------------------------------
        elif group == "source_epoch_and_revocation":
            owner = p.fixture_owner
            if case == "C1_epoch_advance_after_binding":
                state = owner.state()
                state["epoch"] = "WG0N_EPOCH_ADVANCED_AFTER_BIND"
                S.w.atomic_write(owner.directory / "current.json", S.w.canonical(state))
                stimulus = {"epoch": "advanced_after_bind"}
            elif case == "C2_release_revocation_after_binding":
                owner.revoke(REL1)
                stimulus = {"revoked": REL1}
            elif case == "C3_source_artifact_revocation":
                # Revoke the SOURCE ARTIFACT registration, not the release owner.
                # If the owner surface cannot revoke an artifact, record the typed
                # unavailability instead of silently passing.
                try:
                    owner.revoke(rel1.source_artifact_ref.object_id)
                except AttributeError:
                    state = owner.state()
                    state.setdefault("revoked_objects", []).append(rel1.source_artifact_ref.object_id)
                    S.w.atomic_write(owner.directory / "current.json", S.w.canonical(state))
                stimulus = {"revoked_object": getattr(rel1.source_artifact_ref, "object_id", None)}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- D: altered snapshot ----------------------------------------
        elif group == "altered_snapshot":
            ref = rel1.source_artifact_ref
            if case == "D1_content_hash_mismatch_on_pointer":
                forged = replace(ref, content_hash="0" * 64)
                p2 = _mutate_source_view(p, REL1, source_artifact_ref=forged)
                stimulus = {"alter": "content_hash", "kept": "object_id"}
            elif case == "D2_rehashed_snapshot_registered_digest_unchanged":
                forged = replace(ref, content_hash="1" * 64)
                p2 = _mutate_source_view(p, REL1, source_artifact_ref=forged)
                stimulus = {"alter": "locally_rehashed", "registered_digest": "unchanged"}
            elif case == "D3_truncated_or_empty_snapshot":
                forged = replace(ref, content_hash="")
                p2 = _mutate_source_view(p, REL1, source_artifact_ref=forged)
                stimulus = {"alter": "empty_or_truncated_snapshot"}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- E: issuer mismatch -----------------------------------------
        elif group == "issuer_mismatch":
            if case == "E1_release_issuer_not_registrar":
                p2 = _mutate_source_view(p, REL1, issuer_id="ISSUER_NOT_THE_REGISTRAR")
                stimulus = {"issuer": "release_issuer_differs_from_registrar"}
            elif case == "E2_unregistered_issuer":
                p2 = _mutate_source_view(p, REL1, issuer_id="ISSUER_UNKNOWN_UNREGISTERED")
                stimulus = {"issuer": "outside_registered_set"}
            elif case == "E3_issuer_epoch_mismatch":
                p2 = _mutate_source_view(p, REL1, issuer_epoch="WG0N_OTHER_EPOCH")
                stimulus = {"issuer": "epoch_mismatch"}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- F: positive legitimate owner (must still serve) -------------
        elif group == "positive_legitimate_owner":
            if case == "F1_unmodified_legitimate_owner_serves":
                p2 = p
                stimulus = {"control": "pristine_unmodified"}
            elif case == "F2_replay_identical_receipts":
                p2 = p
                stimulus = {"control": "pristine_replay"}
            elif case == "F3_own_pointer_serves":
                # Explicitly re-bind REL-A-W1 to its OWN pointer: the control that
                # makes the substitution negatives meaningful.
                p2 = _mutate_source_view(p, REL1, source_artifact_ref=rel1.source_artifact_ref)
                stimulus = {"control": "own_pointer_rebound"}
            else:
                raise RuntimeError("unknown case " + case)
        else:
            raise RuntimeError("unknown group " + group)

        # ---- execute ------------------------------------------------------
        calls = []
        exception = None
        reason = None
        effects = {}
        receipts = []
        baseline_consumer = None
        if group == "positive_legitimate_owner" and case == "F2_replay_identical_receipts":
            # measure determinism: first run is the reference
            try:
                _, r1, e1 = execute(p2)
                receipts, effects = r1, e1
                baseline_consumer = e1
                _, r2, e2 = execute(p2)
                stimulus["second_run_equal_consumer"] = (e2 == e1)
                stimulus["second_run_equal_receipts"] = (r2 == r1)
                effects = e1
            except Exception as e:  # noqa: BLE001
                exception = type(e).__name__
                reason = str(e)
        else:
            sys.setprofile(profile_calls(calls))
            try:
                # Ordinary callback first: a native Batch must not swallow an
                # untyped exception and hide an admission defect.
                S.w.make_executor(p2)(unit)
                _, receipts, effects = execute(p2)
            except Exception as e:  # noqa: BLE001
                exception = type(e).__name__
                reason = str(e)
            finally:
                sys.setprofile(None)

        typed = _typed_refusal(exception, reason)
        served = bool(effects)
        path = self.out / (group + "__" + case + ".json")
        result = {
            "group": group,
            "case": case,
            "attempted": True,
            "exception_type": exception,
            "exception_reason": reason,
            "typed_refusal": typed,
            "served_positive": served,
            "consumer": effects,
            "baseline_consumer": baseline_consumer,
            "new_I03_calls": sum(
                c["name"] == "execute_empirical_query"
                and str(c["file"]).endswith("pre553_empirical_query.py")
                for c in calls
            ),
            "calls": calls,
            "stimulus": S.w._plain(stimulus) if hasattr(S.w, "_plain") else stimulus,
            "physical_modules": self.physical,
            "candidate_module": getattr(S.w, "__file__", None),
            "actual_process_argv": [sys.executable, *sys.argv],
            "raw_path": str(path),
        }
        dump(path, result)
        return result
