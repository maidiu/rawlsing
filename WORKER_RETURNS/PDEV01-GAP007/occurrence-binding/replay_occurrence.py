"""Sourcefree P1 CONDITIONAL/JOINT operand-binding attempt at GAP007 d3d6.

TEST_ONLY. Reuses the accepted GAP007 frozen source, C11 projection/catalog,
P1 plan and the existing R03 OccurrenceKey construction. It never invents a
source item, occurrence, policy, risk set or direction.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPAIR = ROOT.parent / "repair"
REPLAY = REPAIR / "replay_repair.py"
sys.path.insert(0, str(ROOT.parents[2]))
SPEC = importlib.util.spec_from_file_location("gap007.repair", REPLAY)
repair = importlib.util.module_from_spec(SPEC)
sys.modules["gap007.repair"] = repair
SPEC.loader.exec_module(repair)

from rawlsing_next.universal_grammar.types import OccurrenceKey  # noqa: E402

P1_KINDS = ("CONDITIONAL", "JOINT")
OWNER = "P1 source-grant/ItemRegistry owner named by SourceGrant.item_registry_ref; R03 policy owner is downstream"
FIRST_MISSING = (
    "governed P1 SourceItem -> C11/R03 occurrence binding record "
    "(item_id/option_id/form_id/repeat_id), addressed by SourceGrant.item_registry_ref"
)


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_hash(value) -> str:
    return _sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def _build_c11():
    source = repair.verify_frozen_source()
    incidence = repair.decode_sav(source)
    codes = [f"Q{i:02d}{side}" for i in range(35) for side in ("A", "B")]
    package = repair.package(
        source, incidence.row_count,
        tuple(repair.NativeSourceRule("impl." + code, code) for code in codes),
        coordinate="FORM",
    )
    bundle = repair.materialize_native_preimages(package=package, incidence=incidence)
    repository, release = repair.build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection
    )
    return source, incidence, bundle, repository, release


def _c11_index(bundle):
    code_by_question = {
        ref.key: code for code, ref in bundle.question_refs.items()
    }
    domain = {}
    occurrences = {}
    for slot in bundle.projection.response_slots:
        code = code_by_question.get(slot.question_binding.native_question_ref.key)
        if code is None:
            continue
        values = {
            str(rule.canonical_value)
            for rule in slot.values
            if rule.response_state == "SUBSTANTIVE_RESPONSE"
            and rule.canonical_value is not None
        }
        domain[code] = sorted(values)
        rules = []
        for rule in slot.values:
            for occurrence in rule.occurrences:
                rules.append({
                    "key": occurrence.key,
                    "fields": dict(occurrence.multiplicity_order_rank_fields),
                    "topology_ref": occurrence.topology_ref.as_dict(),
                })
        occurrences[code] = rules
    return {
        "code_by_question": code_by_question,
        "domain": domain,
        "occurrences": occurrences,
    }


def _find_item_registry_content(uri: str) -> dict:
    proc = subprocess.run(
        ["git", "grep", "-n", "-F", uri, "--", "."],
        cwd=str(ROOT.parents[2]), check=False, capture_output=True, text=True,
    )
    return {
        "uri": uri,
        "git_grep_returncode": proc.returncode,
        "matches": [line for line in proc.stdout.splitlines() if line][:20],
        "content_present_outside_p1_constructor": bool(proc.stdout.strip()),
    }


def main() -> int:
    source, incidence, bundle, repository, release = _build_c11()
    input_value = repair.tests._input()
    plan = repair.p1.construct_original35_epre(input_value)
    item_by_ref = {
        item.item_ref.key: item
        for wave in input_value.waves for item in wave.items
        if item.item_ref is not None
    }
    wave_by_atlas = {wave.identity.atlas_id: wave for wave in input_value.waves}
    index = _c11_index(bundle)
    registry_refs = {
        wave.source_grant.item_registry_ref.object_id
        for wave in input_value.waves
        if wave.source_grant is not None
        and wave.source_grant.item_registry_ref is not None
    }
    registry_checks = {uri: _find_item_registry_content(uri) for uri in sorted(registry_refs)}
    p1_item_refs_in_c11 = set()
    for item_ref in item_by_ref:
        # C11 question/admin records do not carry the P1 SourceItem ExactRef.
        if item_ref in bundle.question_refs or any(
                item_ref == admin.implementation_id for admin in bundle.administered):
            p1_item_refs_in_c11.add(item_ref)

    rows = []
    first = None
    for operation in plan.operations:
        if operation.operation_kind not in P1_KINDS:
            continue
        item = item_by_ref[operation.item_ref.key]
        target_code = item.source_variable_code
        operand_ref = operation.conditioner_ref or operation.joint_item_ref
        operand_item = item_by_ref[operand_ref.key]
        operand_code = operand_item.source_variable_code
        condition_value = operation.conditioner_value or operation.joint_value
        c11_target = bundle.question_refs.get(target_code)
        c11_operand = bundle.question_refs.get(operand_code)
        target_domain = index["domain"].get(target_code, [])
        operand_domain = index["domain"].get(operand_code, [])
        target_key = OccurrenceKey(item_id=target_code)
        operand_key = OccurrenceKey(item_id=operand_code)
        wave = wave_by_atlas[operation.wave_atlas_id]
        registry_ref = (
            wave.source_grant.item_registry_ref.object_id
            if wave.source_grant and wave.source_grant.item_registry_ref else None)
        if c11_target is None:
            reason = "P1_TARGET_CODE_HAS_NO_C11_QUESTION"
        elif c11_operand is None:
            reason = "P1_CONDITIONER_CODE_HAS_NO_C11_QUESTION"
        else:
            reason = "P1_SOURCEITEM_TO_C11_R03_OCCURRENCE_BINDING_ABSENT"
        row = {
            "operation_ref": operation.operation_ref.as_dict(),
            "batch_job_ref": operation.batch_job_ref.as_dict() if operation.batch_job_ref else None,
            "wave_atlas_id": operation.wave_atlas_id,
            "operation_kind": operation.operation_kind,
            "item_ref": operation.item_ref.as_dict(),
            "target_code": target_code,
            "target_value": operation.target_value,
            "conditioner_or_joint_ref": operand_ref.as_dict(),
            "conditioner_or_joint_code": operand_code,
            "conditioner_or_joint_value": condition_value,
            "target_p1_sourceitem_exact_in_c11": operation.item_ref.key in p1_item_refs_in_c11,
            "conditioner_p1_sourceitem_exact_in_c11": operand_ref.key in p1_item_refs_in_c11,
            "c11_question_ref": c11_target.as_dict() if c11_target else None,
            "c11_conditioner_question_ref": c11_operand.as_dict() if c11_operand else None,
            "c11_target_domain": target_domain,
            "c11_conditioner_domain": operand_domain,
            "c11_target_occurrence_rules": index["occurrences"].get(target_code, []),
            "c11_conditioner_occurrence_rules": index["occurrences"].get(operand_code, []),
            "r03_candidate_target_key": target_key.material(),
            "r03_candidate_conditioner_key": operand_key.material(),
            "r03_candidate_is_exact": False,
            "source_grant_item_registry_ref": registry_ref,
            "source_grant_item_registry_content_present": bool(
                registry_ref and registry_checks[registry_ref]["content_present_outside_p1_constructor"]),
            "source_grant_source_sha256": wave.identity.source_sha256,
            "c11_source_sha256": bundle.source_sha256,
            "status": "TYPED_REFUSAL",
            "reason": reason,
        }
        if first is None:
            first = row
        rows.append(row)

    counts = {kind: sum(1 for row in rows if row["operation_kind"] == kind) for kind in P1_KINDS}
    reason_counts = {}
    for row in rows:
        reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0) + 1
    value_counts = {}
    for row in rows:
        value_counts[row["conditioner_or_joint_value"]] = value_counts.get(
            row["conditioner_or_joint_value"], 0) + 1
    status_counts = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    operation_refs = [row["operation_ref"]["content_hash"] for row in rows]
    first_missing = {
        "artifact": FIRST_MISSING,
        "owner": OWNER,
        "first_operation_ref": first["operation_ref"] if first else None,
        "first_p1_item_registry_ref": first["source_grant_item_registry_ref"] if first else None,
        "first_p1_item_registry_content_present": first["source_grant_item_registry_content_present"] if first else None,
        "first_p1_target_sourceitem": first["item_ref"] if first else None,
        "first_p1_conditioner_sourceitem": first["conditioner_or_joint_ref"] if first else None,
        "first_c11_target_question_ref": first["c11_question_ref"] if first else None,
        "first_c11_conditioner_question_ref": first["c11_conditioner_question_ref"] if first else None,
        "first_r03_candidate_target_key": first["r03_candidate_target_key"] if first else None,
        "first_r03_candidate_conditioner_key": first["r03_candidate_conditioner_key"] if first else None,
        "why_not_accepted": (
            "P1 SourceItem refs and source_variable_code strings are not C11 "
            "item identities; no ItemRegistry content binds them. Code equality "
            "is a name match, not an exact occurrence mapping."
        ),
        "downstream_missing": (
            "Even after item/occurrence identity: exact R03 GrammarPolicy, "
            "authorized direction grants, risk_set_refs/denominator, form_scope/"
            "scope/administration and current joint/marginal query refs."
        ),
        "owner_of_downstream": "R03 policy/risk-set/direction owner; C11 projection owner for native query objects",
    }
    # Exercise the existing governed C11 catalog for the first sample's exact
    # code/value operands. This proves the catalog is available; it does not
    # create a P1 item/occurrence binding or a conditional/joint query.
    catalog_probe = {"attempted": False}
    try:
        target_catalog, target_request = repair.build_projection_catalog(
            bundle=bundle,
            operation=repair.OperationFixture(
                fixture_id="GAP007-OCCURRENCE-TARGET-PROBE",
                target_variable_code=first["target_code"],
                response_value=first["target_value"],
            ),
            as_of=repair.AS_OF,
        )
        condition_catalog, condition_request = repair.build_projection_catalog(
            bundle=bundle,
            operation=repair.OperationFixture(
                fixture_id="GAP007-OCCURRENCE-CONDITION-PROBE",
                target_variable_code=first["conditioner_or_joint_code"],
                response_value="1",
            ),
            as_of=repair.AS_OF,
        )
        catalog_probe = {
            "attempted": True,
            "target_query_ref": target_request.query_ref.as_dict(),
            "target_predicate_ref": target_request.predicate_ref.as_dict(),
            "condition_query_ref": condition_request.query_ref.as_dict(),
            "condition_predicate_ref": condition_request.predicate_ref.as_dict(),
            "catalog_query_count": len(target_catalog.queries) + len(condition_catalog.queries),
            "catalog_only_not_execution": True,
        }
    except Exception as exc:
        catalog_probe = {
            "attempted": True,
            "refused": type(exc).__name__,
            "detail": str(exc),
        }

    output = {
        "schema": "PDEV01_GAP007_OCCURRENCE_BINDING_ATTEMPT@1.0.0",
        "candidate_commit": "d3d6e48791623478fd1d838c7e95a72b77b5cd74",
        "review_commit": "3aa57b99a2cbef3ab9f55acc92b73670757a3028",
        "mode": "TEST_ONLY_SOURCEFREE_OPERAND_RESOLUTION",
        "source": {
            "source_sha256": bundle.source_sha256,
            "rows": incidence.row_count,
            "columns": len(incidence.variables),
            "release_ref": release.release_ref.as_dict(),
        },
        "p1_plan": {
            "plan_ref": plan.plan_ref,
            "operation_count": len(plan.operations),
            "conditional_count": counts["CONDITIONAL"],
            "joint_count": counts["JOINT"],
            "conditional_joint_accounted": len(rows),
            "operation_refs_unique": len(set(operation_refs)) == len(operation_refs) == len(rows),
            "source_qualification": plan.source_qualification,
        },
        "resolution": {
            "status": "HOLD_FIRST_EXACT_INPUT_MISSING",
            "first_missing": first_missing,
            "p1_sourceitem_refs_exact_in_c11": len(p1_item_refs_in_c11),
            "p1_code_matches_in_c11": sum(
                1 for row in rows
                if row["c11_question_ref"] is not None
                and row["c11_conditioner_question_ref"] is not None),
            "r03_candidate_keys_are_name_only": True,
            "r03_candidate_policy_exact": False,
            "end_to_end_replay_attempted": False,
            "executed_operations": 0,
            "unsupported_entries": len(rows),
            "reason_counts": reason_counts,
            "condition_value_counts": value_counts,
            "status_counts": status_counts,
            "target_value_available_in_c11": sum(
                1 for row in rows if row["target_value"] in row["c11_target_domain"]),
            "condition_value_available_in_c11": sum(
                1 for row in rows if row["conditioner_or_joint_value"] in row["c11_conditioner_domain"]),
            "c11_source_identity_equal_to_p1_wave": sum(
                1 for row in rows if row["source_grant_source_sha256"] == row["c11_source_sha256"]),
            "catalog_probe": catalog_probe,
        },
        "additional_gates": {
            "source_identity": {
                "p1_wave_source_sha_equal_c11": 0,
                "classification": "TEST_ONLY_SOURCE_IDENTITY_SUBSTITUTION_PRESENT_IN_EXISTING_GAP007_DISTRIBUTION_BINDING; not reopened as an exact production identity",
                "owner": "P1 source-grant owner (SourceGrant.source_sha256)",
            },
            "item_occurrence": {
                "p1_sourceitem_exact_in_c11": 0,
                "code_only_matches": 420,
                "accepted": False,
                "reason": "matching source_variable_code is a name match, not an ExactRef/occurrence identity",
            },
            "r03_policy_direction_risk": {
                "exact_policy_present": False,
                "authorized_direction_present": False,
                "risk_set_or_denominator_present": False,
                "reason": "P1 carries refs/operation classes, not an issued R03 GrammarPolicy or risk-set handoff",
            },
        },
        "registry_checks": registry_checks,
        "accounting": rows,
        "scope": {
            "test_only": True,
            "sourcefree": True,
            "original_data": False,
            "production_edit": False,
            "new_science": False,
            "policy_manufactured": False,
            "occurrence_mapping_manufactured": False,
            "merge": False,
            "ci": False,
        },
    }
    (ROOT / "01_ACCOUNTING.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": output["resolution"]["status"],
        "plan_ref": plan.plan_ref,
        "source": output["source"],
        "counts": output["p1_plan"],
        "first_missing": first_missing,
        "reason_counts": reason_counts,
        "value_counts": value_counts,
        "operation_refs_unique": output["p1_plan"]["operation_refs_unique"],
        "executed": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
