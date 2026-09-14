import hashlib
import inspect

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
import rawlsing_next.sdtf_r4_generic_batch_adapter as adapter_module
from rawlsing_next.sdtf_r4_generic_batch_adapter import (
    ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT,
    CANDIDATE_ROW_KIND,
    CURRENTNESS_EVIDENCE_MISMATCH,
    DETERMINANT_IDS,
    ELIGIBLE_FOR_SEPARATE_SELECTION,
    FIELD_PATHS,
    GENERIC_CONTRACT_REF,
    GenericR4BatchAdapterError,
    NOT_APPLICABLE,
    NOT_PROJECTABLE,
    PACKAGE_PARTITION,
    PREDECESSOR_CHAIN_INVALID,
    ROW_IDENTITY_CONFLICT,
    SATISFIED_CANDIDATE_ONLY,
    SATISFIED_CURRENT,
    adapt_generic_r4_batch,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> dict[str, str]:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}")).as_dict()


def _bound_authority(role: str, tag: str) -> dict:
    return {
        "role": role,
        "disposition": "BOUND",
        "scope_or_na_ref": _ref("AUTHORITY_SCOPE", tag),
        "authority_ref": {
            "authority_id": f"AUTH-{tag}",
            "authority_version": "1.0.0",
            "authority_content_hash": _h(f"AUTH:{tag}:1.0.0"),
        },
        "current_selection_evidence_refs": [
            _ref("AUTHORITY_CURRENT_SELECTION", tag)
        ],
    }


def _cell(
    determinant_id: str,
    resolved_value,
    *,
    state: str = SATISFIED_CURRENT,
    candidate_material_refs=(),
    blocker_refs=(),
    na_basis_ref=None,
):
    return {
        "determinant_id": determinant_id,
        "state": state,
        "resolved_value": resolved_value,
        "candidate_material_refs": list(candidate_material_refs),
        "blocker_refs": list(blocker_refs),
        "na_basis_ref": na_basis_ref,
        "basis_text": None,
    }


def _na_cell(ordinal: int, tag: str):
    return _cell(
        DETERMINANT_IDS[ordinal - 1],
        None,
        state=NOT_APPLICABLE,
        na_basis_ref=_ref("AUTHORITY_NOT_APPLICABLE", tag),
    )


def _valid_cells(tag: str):
    refs = {ordinal: _ref("R4_INPUT", f"{tag}-{ordinal}") for ordinal in range(5, 19)}
    values = [
        f"RULE-{tag}",
        "1.0.0",
        _h(f"rule-content:{tag}"),
        ["P1 MATERIAL_ACCESS_DEPENDENCY", "P5 COUNTERPART_CHANNEL_RELATION"],
        refs[5],
        [_ref("SOURCE", f"{tag}-source")],
        [_ref("CLAIM", f"{tag}-claim")],
        refs[8],
        refs[9],
        refs[10],
        refs[11],
        refs[12],
        refs[13],
        refs[14],
        refs[15],
        refs[16],
        refs[17],
        refs[18],
        _bound_authority("RULE_OWNER", f"{tag}-owner"),
        None,
        None,
        None,
        _bound_authority("CAUSAL_USE", f"{tag}-causal"),
        None,
        "NONNUMERIC",
        "CANDIDATE_NOT_CURRENT",
        [],
        [],
    ]
    cells = [_cell(DETERMINANT_IDS[index], value) for index, value in enumerate(values)]
    cells[19] = _na_cell(20, f"{tag}-measurement")
    cells[20] = _na_cell(21, f"{tag}-estimand")
    cells[21] = _na_cell(22, f"{tag}-identification")
    cells[23] = _na_cell(24, f"{tag}-calibration")
    return cells


def _row_hash_material(namespace, candidate_id, generation, predecessor, cells, provenance):
    governed_cells = []
    for cell in cells:
        governed_cells.append(
            {
                "determinant_id": cell["determinant_id"],
                "state": cell["state"],
                "resolved_value": cell["resolved_value"],
                "candidate_material_refs": cell["candidate_material_refs"],
                "blocker_refs": cell["blocker_refs"],
                "na_basis_ref": cell["na_basis_ref"],
            }
        )
    return {
        "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
        "key": {"candidate_namespace": namespace, "candidate_id": candidate_id},
        "row_generation": generation,
        "predecessor_row_ref": predecessor,
        "requirement_cells": governed_cells,
        "provenance_refs": provenance,
    }


def _row(
    tag: str,
    *,
    namespace: str = "fixture",
    candidate_id: str | None = None,
    generation: int = 0,
    predecessor=None,
    cells=None,
):
    candidate_id = candidate_id or tag
    cells = cells or _valid_cells(tag)
    provenance = [_ref("PROVENANCE", tag)]
    material = _row_hash_material(
        namespace, candidate_id, generation, predecessor, cells, provenance
    )
    row_ref = ExactRef(
        CANDIDATE_ROW_KIND,
        f"{namespace}:{candidate_id}:g{generation}",
        semantic_hash(material),
    )
    return {
        "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
        "key": {
            "candidate_namespace": namespace,
            "candidate_id": candidate_id,
        },
        "snapshot": {
            "row_generation": generation,
            "predecessor_row_ref": predecessor,
            "requirement_cells": cells,
            "provenance_refs": provenance,
        },
        "ref": row_ref.as_dict(),
    }


def _batch(rows, *, tag="batch", row_refs=None):
    row_refs = row_refs or [row["ref"] for row in rows]
    return {
        "contract_ref": GENERIC_CONTRACT_REF.as_dict(),
        "batch_namespace": "fixture-batches",
        "batch_id": tag,
        "candidate_rows": rows,
        "candidate_row_refs": row_refs,
        "batch_provenance_refs": [_ref("BATCH_PROVENANCE", tag)],
    }


def _receipt_by_id(result):
    return {receipt.candidate_row_ref.object_id: receipt for receipt in result.candidate_receipts}


def test_exact_contract_identity_and_frozen_28_to_six_partition():
    row = _row("contract")
    result = adapt_generic_r4_batch(_batch([row], tag="contract"))
    assert result.contract_ref == GENERIC_CONTRACT_REF
    assert len(DETERMINANT_IDS) == 28
    assert DETERMINANT_IDS == tuple(f"GBE-R4-{index:03d}" for index in range(1, 29))
    flattened = [ordinal for _, ordinals in PACKAGE_PARTITION for ordinal in ordinals]
    assert sorted(flattened) == list(range(1, 29))
    assert len(flattened) == len(set(flattened)) == 28
    assert len(PACKAGE_PARTITION) == 6


def test_wrong_or_mutable_contract_selector_is_rejected_at_batch_boundary():
    batch = _batch([_row("wrong-contract")], tag="wrong-contract")
    batch["contract_ref"] = "LATEST"
    with pytest.raises(GenericR4BatchAdapterError):
        adapt_generic_r4_batch(batch)

    batch = _batch([_row("wrong-contract-2")], tag="wrong-contract-2")
    bad = dict(GENERIC_CONTRACT_REF.as_dict())
    bad["content_hash"] = _h("not-the-contract")
    batch["contract_ref"] = bad
    with pytest.raises(GenericR4BatchAdapterError, match="exact frozen S03"):
        adapt_generic_r4_batch(batch)


def test_all_valid_multirow_projects_one_to_one_into_existing_r4_constructor():
    rows = [_row("alpha"), _row("beta")]
    result = adapt_generic_r4_batch(_batch(rows, tag="all-valid"))
    assert len(result.candidate_receipts) == 2
    for receipt in result.candidate_receipts:
        assert receipt.integrity_failures == ()
        assert receipt.runtime_projection_state == ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
        assert receipt.current_selection_state == ELIGIBLE_FOR_SEPARATE_SELECTION
        assert receipt.runtime_binding is not None
        assert receipt.runtime_binding.ref == receipt.runtime_binding_ref
        assert receipt.runtime_binding.rule_currentness.value == "CANDIDATE_NOT_CURRENT"
        assert len(receipt.determinant_states) == 28
        assert len(receipt.package_states) == 6


def test_one_invalid_row_is_quarantined_without_contaminating_later_valid_row():
    bad_cells = _valid_cells("bad")
    bad_cells[2]["resolved_value"] = "NOT-A-SHA256"
    bad = _row("bad", cells=bad_cells)
    good = _row("good")
    result = adapt_generic_r4_batch(_batch([bad, good], tag="isolation"))
    receipts = _receipt_by_id(result)
    bad_receipt = receipts[bad["ref"]["object_id"]]
    good_receipt = receipts[good["ref"]["object_id"]]
    assert bad_receipt.runtime_projection_state == NOT_PROJECTABLE
    assert bad_receipt.integrity_failures
    assert good_receipt.integrity_failures == ()
    assert good_receipt.runtime_projection_state == ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
    assert good_receipt.runtime_binding is not None


def test_deterministic_replay_and_reordering_preserve_batch_and_candidate_receipts():
    a, b = _row("replay-a"), _row("replay-b")
    forward = adapt_generic_r4_batch(_batch([a, b], tag="replay"))
    repeated = adapt_generic_r4_batch(_batch([a, b], tag="replay"))
    reverse = adapt_generic_r4_batch(
        _batch([b, a], tag="replay", row_refs=[b["ref"], a["ref"]])
    )
    assert forward.batch_ref == repeated.batch_ref == reverse.batch_ref
    assert forward.batch_receipt_ref == repeated.batch_receipt_ref == reverse.batch_receipt_ref
    assert [r.ref for r in forward.candidate_receipts] == [
        r.ref for r in reverse.candidate_receipts
    ]


def test_candidate_only_row_stays_governed_and_cannot_masquerade_as_current():
    cells = _valid_cells("candidate-only")
    cells[25] = _cell(
        DETERMINANT_IDS[25],
        "CURRENT_ACCEPTED",
        state=SATISFIED_CANDIDATE_ONLY,
        candidate_material_refs=[_ref("CANDIDATE_MATERIAL", "currentness")],
    )
    row = _row("candidate-only", cells=cells)
    result = adapt_generic_r4_batch(_batch([row], tag="candidate-only"))
    receipt = result.candidate_receipts[0]
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None
    assert receipt.runtime_binding_ref is None
    assert receipt.current_selection_state != "SELECTION_EVIDENCE_PRESENT"


def test_silent_not_applicable_on_required_determinant_is_rejected():
    cells = _valid_cells("silent-na")
    cells[0] = _cell(DETERMINANT_IDS[0], None, state=NOT_APPLICABLE)
    row = _row("silent-na", cells=cells)
    with pytest.raises(GenericR4BatchAdapterError, match="SILENT_NA_FORBIDDEN"):
        adapt_generic_r4_batch(_batch([row], tag="silent-na"))


def test_predecessor_chain_error_is_row_local_and_fails_closed():
    g1 = _row("g1", generation=1, predecessor=None)
    good = _row("lineage-good")
    result = adapt_generic_r4_batch(_batch([g1, good], tag="lineage"))
    receipts = _receipt_by_id(result)
    bad_receipt = receipts[g1["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID in bad_receipt.integrity_failures
    assert bad_receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipts[good["ref"]["object_id"]].runtime_binding is not None


def test_same_key_generation_different_hashes_are_both_quarantined_with_no_winner():
    first = _row("conflict", namespace="conflict", candidate_id="same")
    changed_cells = _valid_cells("conflict")
    changed_cells[0]["resolved_value"] = "RULE-conflict-changed"
    second = _row(
        "conflict",
        namespace="conflict",
        candidate_id="same",
        cells=changed_cells,
    )
    result = adapt_generic_r4_batch(_batch([first, second], tag="conflict"))
    assert len(result.candidate_receipts) == 2
    for receipt in result.candidate_receipts:
        assert ROW_IDENTITY_CONFLICT in receipt.integrity_failures
        assert receipt.runtime_binding is None
        assert receipt.runtime_projection_state == NOT_PROJECTABLE


def test_exact_duplicate_row_refs_deduplicate_idempotently():
    row = _row("duplicate")
    single = adapt_generic_r4_batch(_batch([row], tag="dedup"))
    duplicate = adapt_generic_r4_batch(
        _batch([row, row], tag="dedup", row_refs=[row["ref"], row["ref"]])
    )
    assert len(duplicate.candidate_receipts) == 1
    assert duplicate.batch_ref == single.batch_ref
    assert duplicate.batch_receipt_ref == single.batch_receipt_ref
    assert duplicate.candidate_receipts[0].ref == single.candidate_receipts[0].ref


def test_row_identity_hash_excludes_free_text_diagnostics_but_not_governed_fields():
    row = _row("basis")
    altered = _row("basis")
    altered["snapshot"]["requirement_cells"][0]["basis_text"] = "diagnostic wording changed"
    assert altered["ref"] == row["ref"]
    result = adapt_generic_r4_batch(_batch([altered], tag="basis"))
    assert result.candidate_receipts[0].runtime_binding is not None


def test_generic_implementation_contains_no_m10_specific_semantic_path_or_default():
    source = inspect.getsource(adapter_module)
    assert "M10" not in source
    assert "WRIGHT" not in source.upper()
    assert "CURRENT_ACCEPTED selection" not in source
    # The fixture namespace is opaque input and does not alter the generic mapping.
    row = _row("opaque", namespace="M10-fixture")
    receipt = adapt_generic_r4_batch(_batch([row], tag="opaque")).candidate_receipts[0]
    assert receipt.runtime_binding is not None


def test_adapter_does_not_invent_authority_ref_rule_body_or_currentness():
    row = _row("conservation")
    result = adapt_generic_r4_batch(_batch([row], tag="conservation"))
    binding = result.candidate_receipts[0].runtime_binding
    assert binding is not None
    cells = row["snapshot"]["requirement_cells"]
    assert binding.rule_identity.rule_id == cells[0]["resolved_value"]
    assert binding.rule_identity.rule_version == cells[1]["resolved_value"]
    assert binding.rule_identity.rule_content_hash == cells[2]["resolved_value"]
    assert binding.rule_owner.authority_ref.as_dict() == cells[18]["resolved_value"]["authority_ref"]
    assert binding.causal_use_authority.authority_ref.as_dict() == cells[22]["resolved_value"]["authority_ref"]
    assert binding.rule_currentness.value == cells[25]["resolved_value"] == "CANDIDATE_NOT_CURRENT"
    material = binding.as_material()
    assert "rule_body" not in material
    assert "actor_ref" not in material
    assert "entity_ref" not in material


def test_currentness_evidence_mismatch_is_rejected_by_existing_r4_path():
    cells = _valid_cells("currentness")
    cells[25]["resolved_value"] = "CURRENT_ACCEPTED"
    # Row 27 remains empty, so final R4 currentness law must fail closed.
    row = _row("currentness", cells=cells)
    result = adapt_generic_r4_batch(_batch([row], tag="currentness"))
    receipt = result.candidate_receipts[0]
    assert CURRENTNESS_EVIDENCE_MISMATCH in receipt.integrity_failures
    assert receipt.runtime_binding is None
