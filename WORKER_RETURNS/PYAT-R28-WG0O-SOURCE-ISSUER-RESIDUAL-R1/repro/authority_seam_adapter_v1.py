"""WG0O independent authority-seam attack transport (PHASE A frozen).

Constructs the preregistered attacks against the REAL rel.authorities / rel.qauth
issuance surface and the REAL owner interfaces (FixtureOwner.revoke/_sign/verify/
assert_native_sources). Reviewer-side construction only: no author source is
edited and no inherited expectation is rewritten.

PHASE A: this adapter and 01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json are frozen
and pushed BEFORE any candidate execution.
PHASE B: execute against the independently staged WG0P6 candidate.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from dataclasses import replace

R = pathlib.Path(__file__).resolve().parents[1]
# The candidate transport is resolved from sys.path so the candidate's own
# identity bootstrap (bootstrap_p6/sitecustomize) wires and verifies it first.
import phase_b_support_v1 as S  # noqa: E402
from phase_b_support_v1 import plan, execute, profile_calls, dump  # noqa: E402

w = S.w
OP = "OP-WG0P-ORD-01-MARGINAL"
REL1 = "REL-A-W1"
REL2 = "REL-A-W2"

TYPED_TOKENS = ("HELD", "INADMISSIBLE", "REVOKED", "STALE", "REFUSED",
                "UNAVAILABLE", "HOLD", "SUPERSEDED", "MISSING_REQUIRED_AUTHORITY",
                "NOT_EXPRESSIBLE")
LAW_FAMILIES = ("IdentityError", "FrontierError", "RevocationError", "ColdRestartError",
                "NativeDataError", "BatchIntegrityError", "Pre553IntegrityError",
                "Pre553AuthorityError", "Pre553AuthorityConflict",
                "Pre553SemanticCollapseError")


def _typed_refusal(exc_name, reason):
    if exc_name is None:
        return None
    blob = f"{exc_name} {reason or ''}".upper()
    for tok in TYPED_TOKENS:
        if tok in blob:
            return tok
    if exc_name in LAW_FAMILIES:
        return "REFUSED"
    return None


def _rebody(orig, **over):
    """Rebuild one AuthoritySnapshot body; identity triple preserved unless overridden."""
    names = ("authority_id", "authority_version", "authority_content_hash", "authority_kind",
             "decision_state", "governed_operations", "governed_object_families",
             "scope_envelope", "effective_time_or_interval", "parent_authority_refs",
             "negative_limit_refs", "supersession_refs",
             "interpretation_semantics_fingerprint", "replay_protocol_ref")
    kw = {n: over.pop(n, getattr(orig, n)) for n in names}
    typed = over.pop("typed_state", orig.typed_state)
    root = over.pop("producer_replay_locator_or_reference_root",
                    orig.producer_replay_locator_or_reference_root)
    if over:
        raise RuntimeError("unknown rebody fields " + repr(sorted(over)))
    return w.AuthoritySnapshot(typed_state=typed, authority_snapshot_refs=(),
                               dependency_refs=(),
                               producer_replay_locator_or_reference_root=root, **kw)


def _mutate_release(p, rel_key, **fields):
    rels = dict(p.releases)
    rels[rel_key] = replace(rels[rel_key], **fields)
    return replace(p, releases=rels)


def _supported_facts(effects):
    supported = 0
    for entries in (effects or {}).values():
        for e in entries:
            for c in e.get("cells", []):
                if c.get("state") in ("OBSERVED_POSITIVE", "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"):
                    supported += 1
    return supported


class AuthoritySeamCourt:
    def __init__(self):
        self.physical = S.verified_modules()
        self.out = (R / "observations/authority_seam_runs") / os.environ.get("WG0O_RUN", "phase_a_frozen")
        self.out.mkdir(parents=True, exist_ok=True)

    def execute_case(self, group: str, case: str) -> dict:
        p = plan()
        rel1 = p.releases[REL1]
        rel2 = p.releases[REL2]
        p2 = p
        stimulus = {}
        direct = None  # optional direct owner-surface probe (no plan execution)

        # ---- A: real rel.authorities / rel.qauth substitution -------------
        if group == "authority_issuer_substitution":
            if case == "A1_wrong_issuer_qauth_substitution":
                p2 = _mutate_release(p, REL1, qauth=rel2.qauth)
                stimulus = {"swap": "qauth", "from": REL2, "to": REL1,
                            "foreign_authority_id": rel2.qauth.authority_id}
            elif case == "A2_stale_issuer_epoch_same_identity":
                stale = _rebody(rel1.qauth, effective_time_or_interval="2019-01-01",
                                supersession_refs=("urn:wg0p4:test:supersession:SUCCESSOR-AUTH-2",))
                p2 = _mutate_release(p, REL1, qauth=stale)
                stimulus = {"identity_triple_preserved": True,
                            "effective_time_or_interval": "2019-01-01",
                            "supersession_refs": ["urn:wg0p4:test:supersession:SUCCESSOR-AUTH-2"]}
            elif case == "A3_same_hash_foreign_signed_body":
                foreign = _rebody(
                    rel1.qauth,
                    interpretation_semantics_fingerprint="f" * 64,
                    producer_replay_locator_or_reference_root=w.base._ref(
                        "REPLAY_ROOT", "authority-FOREIGN-SIGNED-BODY"),
                    parent_authority_refs=("urn:wg0p4:test:foreign-issuer-parent",))
                assert foreign.authority_ref == rel1.qauth.authority_ref
                p2 = _mutate_release(p, REL1, qauth=foreign)
                stimulus = {"identity_triple_preserved": True,
                            "foreign_body": ["interpretation_semantics_fingerprint",
                                             "producer_replay_locator_or_reference_root",
                                             "parent_authority_refs"]}
            elif case == "A4_foreign_governed_operations_same_hash":
                foreign = _rebody(
                    rel1.qauth,
                    governed_operations=("WG0P3-OP-FOREIGN-ONLY",),
                    interpretation_semantics_fingerprint="e" * 64)
                p2 = _mutate_release(p, REL1, qauth=foreign)
                stimulus = {"identity_triple_preserved": True,
                            "governed_operations": ["WG0P3-OP-FOREIGN-ONLY"]}
            elif case == "A5_foreign_authority_inside_authorities_tuple":
                p2 = _mutate_release(p, REL1,
                                     authorities=(rel2.authorities[0],) + rel1.authorities[1:])
                stimulus = {"swap": "authorities[0]", "from": REL2, "to": REL1,
                            "foreign_authority_id": rel2.authorities[0].authority_id}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- B: forged signature / captured callback ---------------------
        elif group == "signature_and_callback":
            if case in ("B1_self_rehashed_checkpoint_foreign_signature",
                        "B2_foreign_signature_proper_tag"):
                runner, receipts, effects = execute(p)
                cp = w.create_checkpoint(p, receipts)
                d = json.loads(cp.to_json())
                if case.startswith("B1"):
                    d["source_editions"]["REL-A-W1"] = "FORGED-EDITION-AFTER-BIND"
                    d["signature"] = cp.signature  # old signature over mutated payload
                    stimulus = {"forge": "self_rehashed_payload_with_old_signature",
                                "tag_fields_proper": True}
                else:
                    d["signature"] = "f" * 64
                    stimulus = {"forge": "foreign_signature_over_unmodified_payload",
                                "tag_fields_proper": True}
                d.pop("checkpoint_hash", None)
                sig = d.pop("signature")
                forged = w.ColdCheckpoint(**d, signature=sig)
                direct = ("restore_from_checkpoint", forged)
            elif case == "B3_captured_executor_callback_fabricates_fact":
                forged_ref = w.ref({"kind": "WG0P4_NATIVE_ITEM",
                                    "object_id": "urn:wg0p4:test:forged-fact",
                                    "content_hash": "0" * 64})
                spec = p.op_specs[OP]

                def captured_callback(unit):
                    p.fact_custody.store(forged_ref.key, {"forged": True, "op_id": OP})
                    return w.ExecutionOutcome(
                        result_refs=(forged_ref,),
                        provenance_refs=(spec.query.ref, spec.predicate.ref))

                direct = ("run_plan_with_captured_callback", captured_callback)
                stimulus = {"capture": "executor_callback",
                            "fabricated_fact_ref": forged_ref.as_dict(),
                            "native_call_made_by_callback": False}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- C: revocation / missing issuer / cross-universe alias -------
        elif group == "revocation_and_alias":
            if case == "C1_source_artifact_revocation_not_release_tag":
                direct = ("owner_revoke_source_artifact", rel1.source_artifact_ref.object_id)
                stimulus = {"revoke_target": "source_artifact object_id",
                            "distinct_from_release_tag": True,
                            "object_id": rel1.source_artifact_ref.object_id}
            elif case == "C2_missing_independent_issuer":
                flavor = os.environ.get("WG0O_MISSING_ISSUER_FLAVOR", "qauth_none")
                if flavor == "qauth_none":
                    p2 = _mutate_release(p, REL1, qauth=None)
                else:
                    p2 = _mutate_release(p, REL1, authorities=())
                stimulus = {"missing_issuer_flavor": flavor}
            elif case == "C3_alias_pointer_across_genuine_source_universes":
                p2 = _mutate_release(p, REL2, universe_ref=rel1.universe_ref)
                stimulus = {"alias": "universe_ref", "from": REL1, "to": REL2,
                            "both_universes_genuine": True,
                            "aliased_universe": rel1.universe_ref.object_id}
            else:
                raise RuntimeError("unknown case " + case)

        # ---- D: honest positives ----------------------------------------
        elif group == "positive_owner":
            if case == "P1_unmodified_owner_serves":
                p2 = p
                stimulus = {"control": "pristine_unmodified"}
            elif case == "P2_own_authority_identity_rebind_serves":
                rebuilt = w.base._query_authority(f"wg0p3-{REL1}")
                assert rebuilt.authority_ref == rel1.qauth.authority_ref
                p2 = _mutate_release(p, REL1, qauth=rebuilt)
                stimulus = {"control": "own_authority_identity_rebind",
                            "authority_id": rebuilt.authority_id}
            elif case == "P3_replay_identical_consumer":
                p2 = p
                stimulus = {"control": "pristine_replay"}
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
        baseline = None
        extra = {}
        if group == "positive_owner" and case == "P3_replay_identical_consumer":
            try:
                _, r1, e1 = execute(p2)
                receipts, effects = r1, e1
                baseline = e1
                _, r2, e2 = execute(p2)
                stimulus["second_run_equal_consumer"] = (e2 == e1)
                stimulus["second_run_equal_receipts"] = (r2 == r1)
            except Exception as e:  # noqa: BLE001
                exception, reason = type(e).__name__, str(e)
        elif direct is not None:
            action, arg = direct
            sys.setprofile(profile_calls(calls))
            try:
                if action == "restore_from_checkpoint":
                    w.restore_from_checkpoint(arg, p)
                elif action == "run_plan_with_captured_callback":
                    w.run_plan(p, arg)
                elif action == "owner_revoke_source_artifact":
                    p.fixture_owner.revoke(arg)
                else:
                    raise RuntimeError("unknown direct action " + action)
            except Exception as e:  # noqa: BLE001
                exception, reason = type(e).__name__, str(e)
            finally:
                sys.setprofile(None)
            extra["direct_owner_surface"] = action
        else:
            sys.setprofile(profile_calls(calls))
            try:
                w.make_executor(p2)(p2.units_by_op[OP])
                _, receipts, effects = execute(p2)
            except Exception as e:  # noqa: BLE001
                exception, reason = type(e).__name__, str(e)
            finally:
                sys.setprofile(None)

        typed = _typed_refusal(exception, reason)
        supported = _supported_facts(effects)
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
            "baseline_consumer": baseline,
            "new_I03_calls": sum(
                c["name"] == "execute_empirical_query"
                and str(c["file"]).endswith("pre553_empirical_query.py")
                for c in calls),
            "calls": calls,
            "stimulus": S.w._plain(stimulus) if hasattr(S.w, "_plain") else stimulus,
            "physical_modules": self.physical,
            "candidate_module": getattr(S.w, "__file__", None),
            "actual_process_argv": [sys.executable, *sys.argv],
            "raw_path": str(path),
            **extra,
        }
        dump(path, result)
        return result
