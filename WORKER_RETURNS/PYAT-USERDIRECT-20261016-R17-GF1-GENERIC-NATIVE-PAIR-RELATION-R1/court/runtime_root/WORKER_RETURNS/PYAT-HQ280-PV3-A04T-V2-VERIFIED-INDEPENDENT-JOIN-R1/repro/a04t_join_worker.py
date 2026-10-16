#!/usr/bin/env python3
"""A04T join worker: real owner chain, then an independent verifier subprocess.

Phases (argv[2] is the run root, argv[3] the phase):
  produce  - run the REAL source-free C11 -> Route B/I03/I05 -> Batch chain
             through the A04S v2 candidate and write the produced manifest,
             typed outcomes and purported consumer receipts as PLAIN DATA.
  verify   - install a candidate-import blocker, prove it is active, then run
             the stdlib-only independent verifier over the separately authored
             frozen payload plus the produced data.  Writes the verdict.

The produce phase may import the whole repository.  The verify phase must
never import the v2 candidate (or its test module): the blocker raises
ImportError on any such attempt, and the worker records that the block held.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

BLOCKED_MODULES = frozenset({
    "rawlsing_next.pre553_original_workload_contract_v2_candidate",
    "rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate",
})


class _CandidateImportBlocker:
    def find_spec(self, name, path=None, target=None):
        if name in BLOCKED_MODULES or any(
                name.startswith(b + ".") for b in BLOCKED_MODULES):
            raise ImportError(
                f"blocked for verifier independence: {name}")
        return None


def _ref_dict(ref) -> dict:
    return {"kind": ref.kind, "object_id": ref.object_id,
            "content_hash": ref.content_hash}


def _do_produce(root: Path, raw_payload: dict) -> dict:
    import rawlsing_next.pre553_original_workload_contract_v2_candidate as v2
    import rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate as T

    scope = T._v2_scope()
    declarations = []
    for raw in raw_payload["declarations"]:
        kwargs = dict(
            source=raw["source"], wave=raw["wave"], item=raw["item"],
            form=raw["form"], slot=raw["slot"],
            semantic_op_class=raw["semantic_op_class"],
            semantic_roles=tuple(raw["semantic_roles"]),
            target=raw["target"],
            condition_order=tuple(raw.get("condition_order", [])),
            measure_kind=raw.get("measure_kind", "RAW"),
            source_identity=raw["source_identity"],
            authority_ref=raw["authority_ref"],
            risk_identity=raw["risk_identity"],
            topology_identity=raw["topology_identity"],
            required_consumer=raw["required_consumer"],
            state=raw.get("state", "RUNNABLE"),
            hold_reason=raw.get("hold_reason"),
            multiplicity=raw.get("multiplicity", 1),
        )
        disp = v2.SEMANTIC_TO_DISPATCH[kwargs["semantic_op_class"]]
        if kwargs["state"] == "RUNNABLE":
            if disp == "I03_UNARY_OR_JOINT_QUERY":
                query = scope["queries"][raw["query_slot"]]
                kwargs["query_ref"] = query.ref
                # The conditioned query carries its own exact predicate.
                if raw.get("predicate_slot") == "query":
                    kwargs["predicate_ref"] = query.dependency_refs[0]
                else:
                    kwargs["predicate_ref"] = scope["all_p"].ref
            else:
                kwargs["discovery_authority_ref"] = scope["discovery_ref"]
        declarations.append(v2.V2ExpectedWorkDeclaration(**kwargs))

    executed = v2.v2_execute_through_a04(
        declarations=declarations,
        projection_fields=scope["projection_fields"],
        runtime_catalog=scope["catalog"],
        source=scope["stream"])
    prod = executed.a04_executed.production_result

    by_query = {}
    for item in prod.i03_results:
        by_query[item.query_ref.key] = item
    units = []
    for b in executed.dispatch_bindings:
        if b.dispatch_class == "I03_UNARY_OR_JOINT_QUERY":
            item = by_query.get(b.dispatch_job_ref.key)
            facts = item.facts if item is not None else ()
            units.append({
                "job_kind": "QUERY",
                "job_ref": b.dispatch_job_ref.as_dict(),
                "claimed_expected_work_key": b.expected_work_key,
                "declared_source_identity": b.declared_source_identity,
                "declared_condition_order": list(b.declared_condition_order),
                "predicate_ref": (b.dispatch_predicate_ref.as_dict()
                                  if b.dispatch_predicate_ref else None),
                "release_refs": [prod.c11_release.release_ref.as_dict()],
                "attempt_index": 1,
                "state": "COMPLETED",
                "result_typed_states": [f.typed_state for f in facts],
                "denominators": [f.raw_denominator_support for f in facts],
                "null_sources": [None for _ in facts],
                "reported_success": all(
                    f.typed_state in ("SUPPORTED", "OBSERVED_ZERO", "VALID_EMPTY")
                    for f in facts) if facts else False,
            })
        else:
            units.append({
                "job_kind": "DISCOVERY",
                "job_ref": b.dispatch_job_ref.as_dict(),
                "claimed_expected_work_key": b.expected_work_key,
                "declared_source_identity": b.declared_source_identity,
                "declared_condition_order": list(b.declared_condition_order),
                "predicate_ref": None,
                "release_refs": [prod.c11_release.release_ref.as_dict()],
                "attempt_index": 1,
                "state": "COMPLETED",
                "result_typed_states": [r.typed_state
                                        for r in prod.i05_result.receipts],
                "denominators": [None for _ in prod.i05_result.receipts],
                "null_sources": [None for _ in prod.i05_result.receipts],
                "reported_success": all(
                    r.typed_state in ("DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY")
                    for r in prod.i05_result.receipts
                ) if prod.i05_result.receipts else False,
            })
    consumers = T.v2_consumers_for(declarations, executed)
    # Translate the A04 binder's held-frontier rows (A04 keys) back to v2
    # keys.  This translation lives on the PRODUCER side (which may import
    # both); the verifier independently recomputes v2 keys from the raw
    # payload and compares — never trusts these strings.
    import rawlsing_next.pre553_original_workload_binder_candidate as a04b
    v2key_of_a04key: dict[str, str] = {}
    for d in declarations:
        if d.is_runnable:
            continue
        # Held declarations carry no owner refs; their condition_order passes
        # through untranslated on both sides, so recompute identically.
        a04key = a04b.expected_work_key(
            item_key=a04b.documentary_item_key(
                source=d.source, wave=d.wave, item=d.item, form=d.form,
                slot=d.slot, version=d.schema_version),
            operation_key_value=a04b.operation_key(
                op_class=d.dispatch_class,
                roles=d.semantic_roles, target=d.target,
                condition_order=tuple(d.condition_order),
                measure_kind=d.measure_kind, version=d.schema_version),
            source_identity=d.source_identity, authority_ref=d.authority_ref,
            risk_identity=d.risk_identity, topology_identity=d.topology_identity,
            consumer=d.required_consumer, version=d.schema_version)
        v2key_of_a04key[a04key] = d.expected_work_key
    produced = {
        "executed_source_sha": prod.source_identity.get("source_sha256", ""),
        "executed_release_ref": prod.c11_release.release_ref.as_dict(),
        "units": units,
        "held_export": [
            {"expected_work_key": v2key_of_a04key.get(
                row["expected_work_key"], row["expected_work_key"]),
             "item": row["item"], "state": row["state"]}
            for row in executed.a04_executed.bound.held_frontier],
        "consumer_receipts": [
            {"expected_work_key": c["expected_work_key"],
             "consumer": c["consumer"]} for c in consumers],
    }
    (root / "produced.json").write_text(json.dumps(produced, indent=1,
                                                  sort_keys=True))
    return {"units": len(units),
            "dependency_root": prod.replay_receipt["dependency_root"]}


def _do_verify(root: Path) -> dict:
    sys.meta_path.insert(0, _CandidateImportBlocker())
    blocked_holds = False
    try:
        import rawlsing_next.pre553_original_workload_contract_v2_candidate  # noqa: F401
    except ImportError:
        blocked_holds = True
    import rawlsing_next.pre553_original_workload_v2_verifier_candidate as V
    payload = json.loads((root / "payload.json").read_text())
    produced = json.loads((root / "produced.json").read_text())
    frozen = V.freeze_payload(payload)
    verdict = V.verify(frozen, produced)
    custodian = payload.get("custodian")
    cust = V.custodian_check(frozen, custodian)
    actual = V.actual_consumer_court(verdict)
    migration = V.audit_a05_migration(frozen["records"])
    out = {
        "candidate_import_blocked": blocked_holds,
        "verifier_contract": V.VERIFIER_CONTRACT_ID,
        "ok": verdict.ok,
        "failure_codes": verdict.failure_codes(),
        "holds": verdict.hold_codes(),
        "expected_keys": verdict.expected_keys,
        "job_keys": verdict.job_keys,
        "omitted": verdict.omitted,
        "extra": verdict.extra,
        "visible_non_runnable": verdict.visible_non_runnable,
        "result_classes": verdict.result_classes,
        "unsatisfied_consumers": verdict.unsatisfied_consumers,
        "frontier_digest": verdict.frontier_digest,
        "custodian": cust,
        "actual_consumer_court": actual,
        "migration": migration,
    }
    (root / "verdict.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    return out


def main() -> int:
    root = Path(sys.argv[1])
    phase = sys.argv[2]
    root.mkdir(parents=True, exist_ok=True)
    if phase == "produce":
        raw_payload = json.loads((root / "payload.json").read_text())
        summary = _do_produce(root, raw_payload)
        print(json.dumps({"phase": "produce", **summary}, sort_keys=True))
        return 0
    if phase == "verify":
        out = _do_verify(root)
        print(json.dumps({"phase": "verify", "ok": out["ok"],
                          "failure_codes": out["failure_codes"],
                          "candidate_import_blocked":
                              out["candidate_import_blocked"]},
                         sort_keys=True))
        return 0
    print(json.dumps({"error": f"unknown phase {phase!r}"}))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
