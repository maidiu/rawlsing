from __future__ import annotations

import copy
import pytest

from rawlsing_next.fiabc_derivative_parentage import (
    mint_derivative_parentage_receipt,
    mint_parentage_bundle,
    mint_source_verification_receipt,
)
from rawlsing_next.fiabc_live_accounting_binding import (
    LiveAccountingError,
    PARENTAGE_SCHEMA,
    require_derivative_parentage,
)
from rawlsing_next.fiabc_live_r35_guard import (
    CURRENT_EDGE_CLASSES,
    CURRENT_SOURCE_SHA,
    LIVE_GUARD_PASS,
    LiveR35GuardError,
    verify_live_two_source_physical_guard,
)
from rawlsing_next.fiabc_whole_source_physical_equivalence import (
    COMPATIBILITY_PHYSICAL_ONLY,
    build_candidate_realization,
    build_canonical_expectation,
    canonical_digest,
    required_dimensions,
)

def _reader(source):
    return {
        "decoder_implementation":"synthetic",
        "decoder_version":"1",
        "decoder_mode":"DTA_COMPAT" if source=="LITS_I" else "SAV_NATIVE_GOVERNED",
        "config":{"apply_value_formats":False,"user_missing":True},
        "compatibility_mode":"COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY" if source=="LITS_I" else "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE",
        "compatibility_semantic_scope":COMPATIBILITY_PHYSICAL_ONLY if source=="LITS_I" else "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM",
        "semantic_authority":False,
    }

def _source(source):
    return {
        "family":"LiTS" if source=="LITS_I" else "WVS",
        "wave_or_release":"I" if source=="LITS_I" else "7",
        "canonical_filename":"LiTS_I.dta" if source=="LITS_I" else "WVS Wave 7.sav",
        "sha256":CURRENT_SOURCE_SHA[source],
        "format":"dta" if source=="LITS_I" else "sav",
    }

def _metadata(source):
    material={"source":source,"raw_layout":{"witness":"kept"},"normalized":{"witness":"kept"}}
    return {
        "contract":"PRE553_PHYSICAL_METADATA@1.0.0",
        "receipt_identity":"a"*64,
        "source_sha256":CURRENT_SOURCE_SHA[source],
        "physical_metadata_digest":canonical_digest(material),
        "verification_state":"VERIFIED",
        "semantic_authority":False,
    }

def _evidence(source):
    out={}
    for name in required_dimensions(CURRENT_EDGE_CLASSES[source]):
        if name=="physical_metadata":
            continue
        out[name]={"source":source,"dimension":name,"witness":"preserved"}
    return out

def _expectation(source):
    return build_canonical_expectation(
        scope_id=f"{source}::WHOLE_SOURCE",
        source_identity=_source(source),
        reader_configuration=_reader(source),
        applicable_edge_classes=CURRENT_EDGE_CLASSES[source],
        evidence_material=_evidence(source),
        physical_metadata_binding=_metadata(source),
    )

def _document():
    sources={}
    for source in ("LITS_I","WVS7"):
        exp=_expectation(source)
        realizations={}
        for candidate in ("A","B","C"):
            realizations[candidate]=build_candidate_realization(
                candidate=candidate,
                expectation=exp,
                source_identity=_source(source),
                reader_configuration=_reader(source),
                applicable_edge_classes=CURRENT_EDGE_CLASSES[source],
                evidence_material=_evidence(source),
                physical_metadata_binding=_metadata(source),
                semantic_observation_digest="b"*64,
            )
        sources[source]={"expectation":exp,"realizations":realizations}
    return {"schema":"FIABC_T6_LIVE_R35_PHYSICAL_GUARD_INPUT@1.0.0","sources":sources}

def test_current_edge_classes_are_exact_s35_declarations():
    assert CURRENT_EDGE_CLASSES["LITS_I"]==("EC01","EC02","EC05","EC06","EC09","EC12")
    assert CURRENT_EDGE_CLASSES["WVS7"]==("EC01","EC05","EC07","EC09","EC10","EC12","EC13")

def test_two_source_physical_guard_pass_is_not_semantic_or_certification_pass():
    receipt=verify_live_two_source_physical_guard(_document())
    assert receipt["status"]==LIVE_GUARD_PASS
    assert receipt["physical_equivalence_upgrades_semantic_failure"] is False
    assert receipt["semantic_pass_manufactures_physical_pass"] is False
    assert receipt["whole_source_certification_claimed"] is False
    assert len(receipt["receipt_identity"])==64

def test_same_semantic_digest_cannot_hide_physical_witness_drift():
    doc=_document()
    doc["sources"]["LITS_I"]["realizations"]["C"]["evidence_digests"]["typed_missingness"]="0"*64
    with pytest.raises(LiveR35GuardError):
        verify_live_two_source_physical_guard(doc)

def test_missing_candidate_c_physical_receipt_fails_closed():
    doc=_document()
    del doc["sources"]["WVS7"]["realizations"]["C"]
    with pytest.raises(LiveR35GuardError):
        verify_live_two_source_physical_guard(doc)

def test_t4_parentage_adapter_refuses_old_mini_contract_without_exact_r35_binding(tmp_path):
    p=tmp_path/"old.json"
    p.write_text('{"schema":"FIABC_T4_DERIVATIVE_PARENTAGE@1.0.0"}',encoding="utf-8")
    with pytest.raises(LiveAccountingError):
        require_derivative_parentage(
            p,derivative_identity="d"*64,canonical_source_sha256="e"*64
        )

def test_t4_parentage_adapter_consumes_generic_r35_bundle(tmp_path):
    source_sha="e"*64
    producer={"identity":"builder","code_blob":"blob","version":"1"}
    reader={"reader":"synthetic","version":"1"}
    scope={"scope":"current"}
    current={"runtime":"current"}
    ownership={"candidate":"A","root":"r"}
    source=mint_source_verification_receipt(
        source_id="S",canonical_source_sha256=source_sha,observed_source_sha256=source_sha,
        producer=producer,operation="VERIFY",reader_config=reader,
        scope_determinants=scope,currentness_determinants=current,ownership=ownership,
    )
    derivative_id="d"*64
    derivative=mint_derivative_parentage_receipt(
        source_receipt=source,derivative_class="TEST",derivative_identity=derivative_id,
        derivative_hash=derivative_id,derivative_metadata={"m":1},producer=producer,
        derivation_operation="BUILD",reader_config=reader,scope_determinants=scope,
        currentness_determinants=current,ownership=ownership,
    )
    bundle=mint_parentage_bundle(source_receipt=source,derivative_receipt=derivative)
    assert bundle["schema"]==PARENTAGE_SCHEMA
    p=tmp_path/"bundle.json"
    import json
    p.write_text(json.dumps(bundle),encoding="utf-8")
    out=require_derivative_parentage(
        p,derivative_identity=derivative_id,canonical_source_sha256=source_sha,
        expected_binding={
            "expected_source_id":"S",
            "expected_derivative_class":"TEST",
            "expected_derivative_identity":derivative_id,
            "expected_derivative_receipt_identity":derivative["receipt_identity"],
            "expected_derivative_hash":derivative_id,
            "expected_derivative_metadata":{"m":1},
            "expected_producer":producer,
            "expected_derivation_operation":"BUILD",
            "expected_reader_config":reader,
            "expected_scope_determinants":scope,
            "expected_currentness_determinants":current,
            "expected_ownership":ownership,
            "expected_source_receipt_identity":source["receipt_identity"],
            "expected_source_operation":"VERIFY",
            "expected_source_producer":producer,
            "expected_source_reader_config":reader,
            "expected_source_scope_determinants":scope,
            "expected_source_currentness_determinants":current,
            "expected_source_ownership":ownership,
        },
    )
    assert out.canonical_source_sha256==source_sha
