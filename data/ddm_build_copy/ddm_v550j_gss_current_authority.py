"""Current GSS V550J bounded authority promotion validator (Authority 43 / B10).

This module does not discover survey meaning. It validates that the B10 current
authority surface is an exact bounded promotion of the already-adjudicated GSS
2010 Section85 control and that every broader draft member/scope remains typed
unresolved rather than being promoted by representation or analogy.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from data.ddm_build_copy.compile_v550j_joint_response_patterns import (
    _validate_bounded_authority_registry,
)
from data.ddm_build_copy.ddm_v550j_registry_contract import (
    registry_status_is_executable,
)

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "data/ddm_build_copy/authority/v550j_gss_current_authority_r1.yaml"
SOURCE = ROOT / "section85/authority/registry_gss.yaml"
DRAFT = ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml"
AUTHORITY_ROWS = ROOT / "section85/authority/bounded_joint_configuration_authority.csv"
ITEM_ROWS = ROOT / "section85/authority/bounded_joint_configuration_item_crosswalk.csv"
SCOPE_ROWS = ROOT / "section85/authority/bounded_nine_scope_manifest.csv"
FILTER = ROOT / "section85/inputs/gss_2010.json"
RESPONSE_BINDING = ROOT / "data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv"
B10 = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/RESIDUAL_ZERO_LOSS_EXECUTION_WAVE_R2/B10_V550J_GSS_HARDEN"
)
MEMBER_LEDGER = B10 / "GSS_DRAFT_MEMBER_RECONCILIATION.csv"
SCOPE_LEDGER = B10 / "GSS_WAVE_SCOPE_DISPOSITIONS.csv"
BLOCKER_LEDGER = B10 / "GSS_TYPED_BLOCKERS.csv"

AUTHORITY_ID = "V550J-GSS-CURRENT-AUTHORITY-2026-08-28-R1"
SOURCE_REGISTRY_HASH = "26cd8d5cad9cfa05ee70dc2f4f006e45030394aee79abc7c7f15c30332b7ca5a"
PROMOTION_HASH = "d7cef36fd22434d0a24321a4482dae548e04b3c08e057d500d27c7b40d826103"
RESPONSE_CONTRACT_HASH = "9573e1f8fb4e0b7126fa44c74892a2acb70db046e5d2e110079a30fe15730821"
APPROVED_FAMILY = "JCFG-GSS-ABORTION-CONDITIONS"
INHERITED_DRAFT_FAMILY = "gss_abortion_condition_family"
APPROVED_ORDER = ("abdefect", "abhlth", "abrape", "abany", "absingle", "abnomore")
APPROVED_ROLE_ORDER = (
    ("exception_case", "abdefect", "fetal_defect"),
    ("exception_case", "abhlth", "woman_health"),
    ("exception_case", "abrape", "rape"),
    ("elective_case", "abany", "any_reason"),
    ("social_condition", "absingle", "unmarried"),
    ("family_size_condition", "abnomore", "no_more_children"),
)
DRAFT_FAMILIES = (
    "gss_abortion_condition_family",
    "gss_civil_liberties_speak_family",
    "gss_civil_liberties_library_family",
)
DRAFT_WAVES = ("1972","1973","1982","1984","1993","2002","2004","2010","2014","2016","2024")


class GSSCurrentAuthorityError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise GSSCurrentAuthorityError(f"YAML mapping required: {path}")
    return payload


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _family_items(family: dict[str, Any]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    groups = family.get("item_role_groups") or {}
    if not isinstance(groups, dict):
        raise GSSCurrentAuthorityError("item_role_groups must be mapping")
    for role, items in groups.items():
        if not isinstance(items, list):
            raise GSSCurrentAuthorityError(f"role group is not list: {role}")
        for item in items:
            if not isinstance(item, dict) or not str(item.get("var_code", "")).strip():
                raise GSSCurrentAuthorityError(f"malformed member in {role}")
            out.append((str(role), str(item["var_code"]), str(item.get("condition_label", ""))))
    return out


def _family_by_id(registry: dict[str, Any], family_id: str) -> dict[str, Any]:
    found = [f for f in registry.get("families", []) if isinstance(f, dict) and f.get("family_id") == family_id]
    if len(found) != 1:
        raise GSSCurrentAuthorityError(f"expected one family {family_id}, found {len(found)}")
    return found[0]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GSSCurrentAuthorityError(message)


def validate_gss_current_authority() -> dict[str, Any]:
    current = _load_yaml(CURRENT)
    source = _load_yaml(SOURCE)
    draft = _load_yaml(DRAFT)

    _require(draft.get("source_family") == "GSS", "historical draft must be GSS")
    _require(str(draft.get("status", "")).lower() == "draft", "historical broad registry must remain draft/nonexecuting")
    draft_family_ids = tuple(f.get("family_id") for f in draft.get("families", []) if isinstance(f, dict))
    _require(draft_family_ids == DRAFT_FAMILIES, "unexpected GSS draft family set/order")
    draft_items: list[tuple[str, str, str, str]] = []
    for family in draft["families"]:
        waves = tuple(str(w) for w in family.get("eligible_waves", ()))
        _require(waves == DRAFT_WAVES, f"{family['family_id']}: draft wave set drift")
        for role, var_code, condition in _family_items(family):
            draft_items.append((family["family_id"], role, var_code, condition))
    _require(len(draft_items) == 25, f"expected 25 draft GSS members, got {len(draft_items)}")
    _require(len({(f, v) for f, _, v, _ in draft_items}) == 25, "duplicate draft GSS member identity")

    _require(current.get("source_family") == "GSS", "current registry source must be GSS")
    _require(current.get("status") == "governed", "current registry must use executable governed status")
    _require(registry_status_is_executable(current.get("status")), "current registry status is not runtime executable")
    _require(current.get("approval_state") == "APPROVED_CURRENT_EXECUTABLE_BOUNDED_GSS_CONTROL", "current approval state drift")
    _require(current.get("current_authority_id") == AUTHORITY_ID, "current authority id drift")
    _require(current.get("current_authority_content_hash") == PROMOTION_HASH, "promotion authority hash drift")
    basis = str(current.get("current_authority_hash_basis", ""))
    _require(hashlib.sha256(basis.encode()).hexdigest() == PROMOTION_HASH, "promotion authority hash basis mismatch")
    _require(current.get("source_registry_content_hash") == SOURCE_REGISTRY_HASH, "selected source registry hash drift")
    _require(source.get("registry_content_hash") == SOURCE_REGISTRY_HASH, "Section85 GSS source registry semantic hash drift")
    _require(current.get("production_completeness_claim") == "NO_PRODUCTION_COMPLETENESS_CLAIM", "production completeness overclaim")
    _require(current.get("response_portability_status") == "NOT_AUTHORIZED_BY_P3", "response portability overclaim")
    _require(current.get("promotion_scope_ceiling") == "ONLY_JCFG_GSS_ABORTION_CONDITIONS__GSS_2010_US__SIX_LISTED_MEMBERS", "promotion scope ceiling drift")
    _require(
        current.get("routing_authority_state") == "NO_SEPARATE_ROUTING_PREDICATE_AUTHORIZED__OBSERVED_RESPONSE_SCOPE_ONLY",
        "routing authority must remain observed-response scoped",
    )
    _require("not converted into routing-negative evidence" in str(current.get("routing_inference_ceiling", "")), "missing routing noninference ceiling")

    current_families = current.get("families", [])
    source_families = source.get("families", [])
    _require(len(current_families) == 1 == len(source_families), "current GSS authority must contain only selected control")
    _require(current_families[0] == source_families[0], "B10 must not mutate selected Section85 family semantics")
    runtime = _validate_bounded_authority_registry(current)
    _require(runtime == {"bounded_family_count": 1, "bounded_item_count": 6, "p3_bound_item_count": 0}, f"runtime authority validation drift: {runtime}")

    family = current_families[0]
    _require(family.get("family_id") == APPROVED_FAMILY, "wrong selected family")
    _require(family.get("joint_configuration_id") == APPROVED_FAMILY, "family/config identity mismatch")
    _require(tuple(str(w) for w in family.get("eligible_waves", ())) == ("2010",), "selected family must be 2010 only")
    _require(int(family.get("minimum_items_answered", 0)) == 3, "completion/minimum-items law drift")
    selected_items = tuple(_family_items(family))
    _require(selected_items == APPROVED_ROLE_ORDER, f"selected member role/order drift: {selected_items}")
    _require(tuple(x[1] for x in selected_items) == APPROVED_ORDER, "selected member order drift")
    meta = family.get("authority_metadata") or {}
    _require(meta.get("inherited_registry_family_id") == INHERITED_DRAFT_FAMILY, "draft-family lineage missing")
    _require(meta.get("joint_configuration_adjudication_id") == "V550JADJ-0005", "wrong GSS adjudication")
    _require(meta.get("joint_configuration_decision_status") == "ACCEPTED_EXISTING_GSS_EXECUTABLE_CONTROL", "GSS control decision not accepted")
    _require(meta.get("authority_basis_status") == "HUMAN_ADJUDICATED_FROM_EXACT_SOURCE_EVIDENCE", "human exact-evidence adjudication missing")
    forbidden = set(meta.get("forbidden_inferences") or ())
    _require(
        {"extension beyond listed variables", "cross-source portability", "automatic binding to a single P3 proposition family"} <= forbidden,
        "selected inference ceilings weakened",
    )

    draft_abort = _family_by_id(draft, INHERITED_DRAFT_FAMILY)
    draft_map = {(r, v): c for r, v, c in _family_items(draft_abort)}
    for role, var_code, condition in selected_items:
        _require(draft_map.get((role, var_code)) == condition, f"{var_code}: target condition drift from draft")
    _require("abpoor" not in APPROVED_ORDER, "abpoor may not be promoted")
    target_rules = family.get("target_resolution_rules") or []
    _require(len(target_rules) == 1, "selected target-resolution rule count drift")
    target = target_rules[0]
    _require(target.get("target_entity_id") == "abortion_permission", "target entity drift")
    _require(target.get("target_condition_label_from") == "condition_label", "condition must remain distinct target condition")
    _require(target.get("target_resolution_grain") == "condition_label", "target-condition grain drift")
    rules = family.get("response_role_rules") or []
    signed = {(str(r.get("response_value_normalized")), r.get("semantic_response_role"), r.get("response_direction")) for r in rules}
    _require(("1", "support", "positive") in signed and ("2", "oppose", "negative") in signed, "response semantic sign law drift")
    _require(all("2010" in {str(w) for w in r.get("validated_waves", ())} for r in rules), "2010 response semantics not validated")

    authority_rows = [r for r in _rows(AUTHORITY_ROWS) if r["source_family"] == "GSS"]
    _require(len(authority_rows) == 1, "expected one GSS bounded authority row")
    ar = authority_rows[0]
    _require(ar["joint_configuration_id"] == APPROVED_FAMILY and ar["wave"] == "2010" and ar["country_code"] == "US", "bounded GSS authority scope drift")
    _require(ar["joint_configuration_adjudication_id"] == "V550JADJ-0005", "bounded GSS adjudication row drift")
    _require(ar["item_count"] == "6" and ar["minimum_items_answered"] == "3", "bounded GSS cardinality/completion drift")

    item_rows = [r for r in _rows(ITEM_ROWS) if r["source_family"] == "GSS"]
    item_rows.sort(key=lambda r: int(r["item_order"]))
    _require(len(item_rows) == 6, "GSS bounded item crosswalk must be six rows")
    _require(tuple(r["var_code"] for r in item_rows) == APPROVED_ORDER, "GSS bounded item crosswalk order drift")
    for row in item_rows:
        _require(row["wave"] == "2010" and row["country_code"] == "US", f"{row['var_code']}: scope drift")
        _require(row["joint_configuration_id"] == APPROVED_FAMILY, f"{row['var_code']}: config drift")
        response = json.loads(row["response_semantics_summary"])
        _require(RESPONSE_CONTRACT_HASH in set(response.get("response_semantics_contract_hashes", [])), f"{row['var_code']}: response contract hash drift")

    scope_rows = [r for r in _rows(SCOPE_ROWS) if r["source_family"] == "GSS"]
    _require(len(scope_rows) == 1, "expected one exact GSS bounded scope")
    scope = scope_rows[0]
    _require((scope["wave"], scope["country_code"], scope["filter_file"]) == ("2010", "US", "gss_2010.json"), "GSS applicability scope drift")
    _require(scope["filter_sha256"] == "af054af053d083865331d6d0fac5382ca69adf9356a1d84e2b00d16feef9108b", "GSS filter hash drift")
    _require(scope["v550_response_semantics_audit_sha256"] == "6ccd7e438e73727f1edb59b09ab59bc50b86bc738656f71a00c60dac215e9c0c", "GSS V550 audit hash drift")
    filter_payload = json.loads(FILTER.read_text(encoding="utf-8"))
    filter_vars = {str(v).lower() for v in filter_payload.get("var_codes", ())}
    _require(set(APPROVED_ORDER) <= filter_vars, "GSS 2010 exact filter omits approved member")
    _require("abpoor" not in filter_vars, "GSS 2010 exact filter may not silently add abpoor")

    binding = [
        r for r in _rows(RESPONSE_BINDING)
        if r["source_family"] == "GSS" and r["canonical_wave"] == "2010" and r["var_code"] in APPROVED_ORDER
    ]
    _require(len(binding) == 6 and {r["var_code"] for r in binding} == set(APPROVED_ORDER), "active GSS 2010 response binding incomplete")
    _require(all(r["substantive_category_count"] == "2" for r in binding), "approved binary response category count drift")

    member_ledger = _rows(MEMBER_LEDGER)
    _require(len(member_ledger) == 25, "B10 member reconciliation must cover all 25 draft members")
    _require(
        {(r["draft_family_id"], r["var_code"]) for r in member_ledger}
        == {(f, v) for f, _, v, _ in draft_items},
        "B10 member reconciliation is not exact to draft universe",
    )
    approved_rows = [r for r in member_ledger if r["current_approval_state"].startswith("APPROVED_CURRENT_EXECUTABLE_MEMBER")]
    unresolved_rows = [r for r in member_ledger if r["current_approval_state"].startswith("STILL_UNRESOLVED")]
    _require(len(approved_rows) == 6 and len(unresolved_rows) == 19, "B10 member approval/unresolved partition drift")
    _require(tuple(r["var_code"] for r in approved_rows) == APPROVED_ORDER, "B10 approved member ledger order drift")

    scope_ledger = _rows(SCOPE_LEDGER)
    _require(len(scope_ledger) == 33, "B10 family-wave ledger must cover 3 x 11 draft scopes")
    approved_scopes = [r for r in scope_ledger if r["current_scope_state"].startswith("APPROVED_")]
    unresolved_scopes = [r for r in scope_ledger if r["current_scope_state"].startswith("STILL_UNRESOLVED")]
    _require(len(approved_scopes) == 1 and len(unresolved_scopes) == 32, "B10 scope approval/unresolved partition drift")
    _require(
        approved_scopes[0]["draft_family_id"] == INHERITED_DRAFT_FAMILY
        and approved_scopes[0]["wave"] == "2010"
        and approved_scopes[0]["approved_member_count"] == "6",
        "only abortion/2010 six-member scope may be approved",
    )

    blockers = {r["blocker_code"]: r for r in _rows(BLOCKER_LEDGER)}
    required_blockers = {
        "B10-GSS-BROAD-DRAFT-NOT-APPROVED",
        "B10-GSS-ABPOOR-NOT-IN-V550JADJ-0005",
        "B10-GSS-NON2010-SCOPE-NOT-PROMOTED",
        "B10-GSS-SPEAK-FAMILY-NO-CURRENT-JOINT-ADJUDICATION",
        "B10-GSS-LIBRARY-FAMILY-NO-CURRENT-JOINT-ADJUDICATION",
        "B10-GSS-LIVE-J-CHAIN-EXTERNAL-RUNTIME",
    }
    _require(required_blockers == set(blockers), "typed blocker ledger drift")

    return {
        "status": "APPROVED_CURRENT_EXECUTABLE_GSS_V550J_AUTHORITY__BOUNDED_2010_CONTROL__DRAFT_REMAINDER_TYPED_UNRESOLVED",
        "authority_id": AUTHORITY_ID,
        "authority_content_hash": PROMOTION_HASH,
        "current_registry_file_sha256": _sha256(CURRENT),
        "source_registry_content_hash": SOURCE_REGISTRY_HASH,
        "approved_family_count": 1,
        "approved_member_count": 6,
        "approved_family_wave_scope_count": 1,
        "draft_family_count": 3,
        "draft_member_count": 25,
        "typed_unresolved_member_count": 19,
        "draft_family_wave_scope_count": 33,
        "typed_unresolved_family_wave_scope_count": 32,
        "approved_scope": {"source_family": "GSS", "wave": "2010", "country_code": "US"},
        "approved_joint_configuration_id": APPROVED_FAMILY,
        "live_respondent_chain_status": "EXTERNAL_RUNTIME_BLOCKER__NOT_SUBSTITUTED_BY_CONTROLLED_TEST",
        "production_completeness_claim": "NO_PRODUCTION_COMPLETENESS_CLAIM",
        "product_wide_closure": False,
    }


__all__ = [
    "GSSCurrentAuthorityError",
    "validate_gss_current_authority",
    "CURRENT",
    "APPROVED_ORDER",
    "APPROVED_FAMILY",
]
