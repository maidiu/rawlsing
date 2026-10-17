"""WG0Q independent authority-body / temporal / cold-replay attack transport.

Phase A frozen BEFORE any WG0P7 candidate is read.  The original WG0O 14
controls are preserved byte-identically in authority_seam_adapter_v1.py and its
oracle; this module adds a new finite matrix over the REAL AuthoritySnapshot
fields and the REAL FixtureOwner / ColdCheckpoint interfaces.

Reviewer-side construction only.  No author source or frozen expectation is
edited.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys
import tempfile
from dataclasses import replace

import authority_seam_adapter_v1 as A  # noqa: E402
from phase_b_support_v1 import w, plan, execute, profile_calls, dump  # noqa: E402
S = A.S

OP = A.OP
REL1 = A.REL1
REL2 = A.REL2
R = A.R
TYPED_TOKENS = A.TYPED_TOKENS
LAW_FAMILIES = A.LAW_FAMILIES


def _supported(effects):
    return A._supported_facts(effects)


def _plain(value):
    return w._plain(value)


def _effects_sha(effects):
    text = json.dumps(_plain(effects), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def _forge_checkpoint(cp, owner, **changes):
    """Structural forgery with a real owner signature over the altered payload.

    This models a checkpoint whose payload was altered before signing (e.g. by a
    compromised exporter).  The point is whether the plan/currentness binding
    notices the alteration, not whether HMAC can be forged without a key.
    """
    d = json.loads(cp.to_json())
    d.pop("checkpoint_hash", None)
    d.pop("signature", None)
    d.update(changes)
    payload = {k: v for k, v in d.items()
               if k not in ("signature", "checkpoint_hash")}
    d["signature"] = owner._sign(payload)
    fields = {k: v for k, v in d.items()
              if k not in ("signature", "checkpoint_hash")}
    return w.ColdCheckpoint(**fields, signature=d["signature"])


class AuthorityBodyCourt(A.AuthoritySeamCourt):
    def __init__(self):
        super().__init__()
        self.out = R / "observations/authority_body_runs" / os.environ.get(
            "WG0Q_RUN", "phase_a_wg0p6")
        self.out.mkdir(parents=True, exist_ok=True)

    def _finish(self, group, case, *, exception=None, reason=None, effects=None,
                calls=None, stimulus=None, extra=None, p=None):
        calls = calls or []
        effects = effects or {}
        typed = A._typed_refusal(exception, reason)
        supported = _supported(effects)
        path = self.out / (group + "__" + case + ".json")
        result = {
            "group": group,
            "case": case,
            "attempted": True,
            "exception_type": exception,
            "exception_reason": reason,
            "typed_refusal": typed,
            "served_positive": bool(effects),
            "supported_fact_cells_served": supported,
            "served_supported_original_fact": supported > 0,
            "consumer": effects,
            "effects_sha256": _effects_sha(effects) if effects else None,
            "new_I03_calls": sum(
                c["name"] == "execute_empirical_query"
                and str(c["file"]).endswith("pre553_empirical_query.py")
                for c in calls),
            "calls": calls,
            "stimulus": _plain(stimulus or {}),
            "physical_modules": self.physical,
            "candidate_module": getattr(w, "__file__", None),
            "raw_path": str(path),
            **(extra or {}),
        }
        dump(path, result)
        return result

    def execute_case(self, group, case):
        if group not in {"authority_body_integrity", "temporal_authority_status",
                         "source_item_swap", "owner_grant_and_cold",
                         "positive_current_body"}:
            return super().execute_case(group, case)

        p = None
        p2 = None
        direct = None
        stimulus = {}
        extra = {}
        construction_exception = None
        construction_reason = None

        try:
            p = plan()
            rel1 = p.releases[REL1]
            rel2 = p.releases[REL2]

            # ---------------- authority body integrity -------------------
            if group == "authority_body_integrity":
                if case == "B1_semantic_fingerprint_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    interpretation_semantics_fingerprint="f" * 64)
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "interpretation_semantics_fingerprint",
                                "identity_triple_preserved": True}
                elif case == "B2_parent_authority_refs_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    parent_authority_refs=("urn:wg0q:test:foreign-parent",))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "parent_authority_refs",
                                "identity_triple_preserved": True}
                elif case == "B3_replay_root_same_triple":
                    bad = A._rebody(
                        rel1.qauth,
                        producer_replay_locator_or_reference_root=w.base._ref(
                            "REPLAY_ROOT", "authority-FOREIGN-REPLAY-ROOT"))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "producer_replay_locator_or_reference_root",
                                "identity_triple_preserved": True}
                elif case == "B4_governed_family_removed":
                    bad = A._rebody(
                        rel1.qauth,
                        governed_object_families=("EmpiricalFact@1.0.0",
                                                   "EmpiricalPredicate@1.0.0"))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "governed_object_families",
                                "removed": "EmpiricalQuerySpec@1.0.0"}
                elif case == "B5_false_authority_kind":
                    bad = A._rebody(rel1.qauth, authority_kind="ROUTING_RISK_SET")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "authority_kind",
                                "claimed": "ROUTING_RISK_SET"}
                elif case == "B6_negative_limit_added":
                    bad = A._rebody(rel1.qauth,
                                    negative_limit_refs=("urn:wg0q:test:negative-limit",))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "negative_limit_refs"}
                elif case == "B7_deny_state_same_triple":
                    bad = A._rebody(rel1.qauth, typed_state="DENY",
                                    decision_state="DENY")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "decision_state", "state": "DENY"}
                elif case == "B8_false_content_hash_claim":
                    bad = A._rebody(rel1.qauth, authority_content_hash="f" * 64)
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "authority_content_hash",
                                "claimed_hash": "f" * 64}
                elif case == "B9_foreign_scope_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    scope_envelope={"source_universe_refs":
                                                    rel2.universe_ref.as_dict()})
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "scope_envelope",
                                "foreign_universe": rel2.universe_ref.object_id}
                elif case == "B10_no_permitted_operation":
                    bad = A._rebody(rel1.qauth, governed_operations=())
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "governed_operations", "value": []}
                elif case == "B11_foreign_operation_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    governed_operations=("WG0Q-OP-FOREIGN-ONLY",))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "governed_operations",
                                "value": ["WG0Q-OP-FOREIGN-ONLY"]}
                elif case == "B12_foreign_replay_protocol_ref":
                    bad = A._rebody(rel1.qauth,
                                    replay_protocol_ref=w.base._ref(
                                        "REPLAY_PROTOCOL", "FOREIGN-PROTOCOL"))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"altered": "replay_protocol_ref"}
                else:
                    raise RuntimeError("unknown case " + case)

            # ---------------- temporal status ----------------------------
            elif group == "temporal_authority_status":
                if case == "T1_expired_interval_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    effective_time_or_interval="2019-01-01/2020-01-01")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"effective_time_or_interval":
                                "2019-01-01/2020-01-01", "expected": "STALE"}
                elif case == "T2_unknown_epoch_none":
                    bad = A._rebody(rel1.qauth,
                                    effective_time_or_interval=None)
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"effective_time_or_interval": None}
                elif case == "T3_unknown_epoch_label":
                    bad = A._rebody(rel1.qauth,
                                    effective_time_or_interval="UNKNOWN")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"effective_time_or_interval": "UNKNOWN"}
                elif case == "T4_current_interval_unissued_body":
                    bad = A._rebody(
                        rel1.qauth,
                        effective_time_or_interval="2026-01-01/2026-12-31")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"effective_time_or_interval":
                                "2026-01-01/2026-12-31",
                                "unissued_body": True}
                elif case == "T5_supersession_only_same_triple":
                    bad = A._rebody(rel1.qauth,
                                    supersession_refs=("urn:wg0q:test:successor",))
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"supersession_refs": ["urn:wg0q:test:successor"]}
                elif case == "T6_stale_single_date":
                    bad = A._rebody(rel1.qauth,
                                    effective_time_or_interval="2019-01-01")
                    p2 = A._mutate_release(p, REL1, qauth=bad)
                    stimulus = {"effective_time_or_interval": "2019-01-01"}
                elif case == "T7_owner_known_before_explicit_interval":
                    parent = tempfile.mkdtemp(prefix="wg0q-owner-")
                    owner_dir = pathlib.Path(parent) / "owner"
                    owner = w.FixtureOwner.provision(owner_dir, w.COHORTS)
                    state = json.loads((owner_dir / "current.json").read_text())
                    state["known_at"] = "2019-01-01"
                    w.atomic_write(owner_dir / "current.json", w.canonical(state))
                    releases = w.build_all_releases(fixture_owner=owner)
                    releases[REL1] = replace(
                        releases[REL1],
                        qauth=A._rebody(releases[REL1].qauth,
                                        effective_time_or_interval="2026-01-01"))
                    p2 = plan(releases=releases)
                    stimulus = {"owner_known_at": "2019-01-01",
                                "authority_effective_time": "2026-01-01"}
                else:
                    raise RuntimeError("unknown case " + case)

            # ---------------- source / item swaps ------------------------
            elif group == "source_item_swap":
                if case == "S1_source_artifact_ref_swap":
                    p2 = A._mutate_release(p, REL1,
                                           source_artifact_ref=rel2.source_artifact_ref)
                    stimulus = {"swapped": "source_artifact_ref",
                                "from": REL2, "to": REL1}
                elif case == "S2_source_edition_swap":
                    p2 = A._mutate_release(p, REL1,
                                           source_edition=rel2.source_edition)
                    stimulus = {"swapped": "source_edition",
                                "from": REL2, "to": REL1}
                elif case == "S3_release_universe_swap":
                    p2 = A._mutate_release(p, REL1,
                                           release_ref=rel2.release_ref,
                                           universe_ref=rel2.universe_ref)
                    stimulus = {"swapped": "release_ref+universe_ref",
                                "from": REL2, "to": REL1}
                elif case == "S4_item_metadata_same_cardinality":
                    items = S.items()
                    # two ordinal items have the same domain cardinality; swap
                    # wave identities while keeping the domain shape.
                    a, b = items[0], items[1]
                    swapped = [replace(a, wave=b.wave), replace(b, wave=a.wave)]
                    try:
                        p2 = plan(its=swapped)
                    except Exception as exc:  # plan itself is the refusal point
                        construction_exception = type(exc).__name__
                        construction_reason = str(exc)
                        p2 = None
                    stimulus = {"swapped": "item wave identities",
                                "same_cardinality": True}
                elif case == "S5_qrefs_swap":
                    p2 = A._mutate_release(p, REL1, qrefs=rel2.qrefs)
                    stimulus = {"swapped": "qrefs", "from": REL2, "to": REL1}
                else:
                    raise RuntimeError("unknown case " + case)

            # ---------------- owner grant / cold replay -----------------
            elif group == "owner_grant_and_cold":
                if case == "R1_source_grant_withdrawn_after_plan":
                    p2 = p
                    p2.fixture_owner.revoke("REL-A-W1")
                    stimulus = {"revoked_release_tag": "REL-A-W1"}
                elif case == "R2_source_artifact_revocation_unknown":
                    p2 = None
                    direct = ("owner_revoke_source_artifact",
                              rel1.source_artifact_ref.object_id)
                    stimulus = {"revoke_target": "source_artifact object_id",
                                "expected": "UNKNOWN_RELEASE_NO_REVOCATION"}
                elif case in ("R3_cold_forged_source_edition",
                              "R4_cold_forged_replay_root"):
                    p2 = p
                    _, receipts, _ = execute(p)
                    cp = w.create_checkpoint(p, receipts)
                    if case == "R3_cold_forged_source_edition":
                        editions = dict(cp.source_editions)
                        editions["REL-A-W1"] = "FORGED-EDITION-AFTER-BIND"
                        forged = _forge_checkpoint(cp, p.fixture_owner,
                                                   source_editions=editions)
                        stimulus = {"altered": "source_editions",
                                    "value": editions["REL-A-W1"]}
                    else:
                        forged = _forge_checkpoint(cp, p.fixture_owner,
                                                   science_root="f" * 64)
                        stimulus = {"altered": "science_root",
                                    "value": "f" * 64}
                    direct = ("restore_from_checkpoint", forged)
                    extra["forged_checkpoint_payload"] = forged.payload()
                elif case == "R5_cross_plan_cold":
                    _, receipts, _ = execute(p)
                    cp = w.create_checkpoint(p, receipts)
                    p2 = plan()
                    direct = ("restore_from_checkpoint", cp)
                    stimulus = {"checkpoint_from": "plan-A",
                                "restored_into": "plan-B-distinct-owner"}
                elif case == "R6_valid_cold_restore":
                    _, receipts, _ = execute(p)
                    cp = w.create_checkpoint(p, receipts)
                    p2 = p
                    direct = ("restore_from_checkpoint", cp)
                    stimulus = {"control": "same-plan valid checkpoint"}
                else:
                    raise RuntimeError("unknown case " + case)

            # ---------------- honest positives ---------------------------
            elif group == "positive_current_body":
                if case == "P1_pristine_serves":
                    p2 = p
                    stimulus = {"control": "pristine"}
                elif case == "P2_owner_identity_rebind_serves":
                    rebuilt = w.base._query_authority(f"wg0p3-{REL1}")
                    assert rebuilt.authority_ref == rel1.qauth.authority_ref
                    p2 = A._mutate_release(p, REL1, qauth=rebuilt)
                    stimulus = {"control": "owner identity rebind"}
                elif case == "P3_replay_identical":
                    p2 = p
                    stimulus = {"control": "replay"}
                elif case == "P4_identical_body_rebind":
                    rebuilt = A._rebody(rel1.qauth)
                    assert rebuilt == rel1.qauth
                    p2 = A._mutate_release(p, REL1, qauth=rebuilt)
                    stimulus = {"control": "identical body rebound"}
                else:
                    raise RuntimeError("unknown case " + case)
            else:
                raise RuntimeError("unknown group " + group)
        except Exception as exc:  # noqa: BLE001
            construction_exception = type(exc).__name__
            construction_reason = str(exc)

        if construction_exception is not None:
            return self._finish(group, case, exception=construction_exception,
                                reason=construction_reason,
                                stimulus=stimulus, extra=extra, p=p)

        calls = []
        exception = None
        reason = None
        effects = {}
        baseline = None
        try:
            if group == "positive_current_body" and case == "P3_replay_identical":
                _, r1, e1 = execute(p2)
                effects = e1
                baseline = e1
                _, r2, e2 = execute(p2)
                extra["second_run_equal_consumer"] = (e2 == e1)
                extra["second_run_equal_receipts"] = (r2 == r1)
            elif direct is not None:
                action, arg = direct
                sys.setprofile(profile_calls(calls))
                try:
                    if action == "restore_from_checkpoint":
                        w.restore_from_checkpoint(arg, p2)
                        extra["restored"] = True
                    elif action == "owner_revoke_source_artifact":
                        p2 = plan()
                        p2.fixture_owner.revoke(arg)
                    else:
                        raise RuntimeError("unknown direct action " + action)
                except Exception as exc:  # noqa: BLE001
                    exception, reason = type(exc).__name__, str(exc)
                finally:
                    sys.setprofile(None)
                extra["direct_owner_surface"] = action
            elif group == "owner_grant_and_cold" and case == "R1_source_grant_withdrawn_after_plan":
                sys.setprofile(profile_calls(calls))
                try:
                    w.make_executor(p2)(p2.units_by_op[OP])
                    _, receipts, effects = execute(p2)
                except Exception as exc:  # noqa: BLE001
                    exception, reason = type(exc).__name__, str(exc)
                finally:
                    sys.setprofile(None)
            else:
                sys.setprofile(profile_calls(calls))
                try:
                    w.make_executor(p2)(p2.units_by_op[OP])
                    _, receipts, effects = execute(p2)
                except Exception as exc:  # noqa: BLE001
                    exception, reason = type(exc).__name__, str(exc)
                finally:
                    sys.setprofile(None)
        except Exception as exc:  # noqa: BLE001
            exception, reason = type(exc).__name__, str(exc)
        return self._finish(group, case, exception=exception, reason=reason,
                            effects=effects, calls=calls, stimulus=stimulus,
                            extra=extra, p=p2)
