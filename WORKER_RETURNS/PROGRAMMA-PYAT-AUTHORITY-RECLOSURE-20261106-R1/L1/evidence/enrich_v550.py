#!/usr/bin/env python3
"""Add scoped, source-inspected V550 authority attribution to exact AST sites.

Never infer accepted status from an IO label; unknown paths remain explicit.
"""
import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "generated"
DST = ROOT.parent / "WORKER_RETURNS" / "PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1" / "L1"
DST.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC / "01_SCANNED_FILES.tsv", DST / "01_SCANNED_FILES.tsv")
with (SRC / "02_LEGACY_CALLSITES.csv").open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

FQ = "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
FQ_SHA = "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"
BINDING = "data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv"
BINDING_SHA = "89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb"
SCALE = "data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv"
SCALE_SHA = "d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8"

def bind(row, path, sha, grain, role, effect, negative, downstream, candidate, *, sha_basis=""):
    row.update(
        source_authority_path=path,
        source_file_byte_sha256=sha + (" [MANIFEST_ASSERTED_NOT_RECOMPUTED]" if sha_basis else ""),
        grain=grain,
        authority_role=role,
        semantic_transformation=effect,
        typed_negative_semantics=negative,
        later_actual_reader=downstream,
        current_pre553_successor=candidate + " [CANDIDATE_ONLY]",
        current_first_consumer="UNBOUND / HOLD; pre553_empirical_query.py:685 exists but no verified asset-to-runtime binding",
        accepted_status="HISTORICAL_ASSET_ONLY; CURRENT_ISSUER_ACCEPTANCE_UNPROVEN",
    )

for r in rows:
    mod = r["historical_module"].rsplit("/", 1)[-1]
    symbol = r["symbol"]
    expr = r["call_expression"]
    leaf = expr.split("(", 1)[0].rsplit(".", 1)[-1]
    kind = r["call_kind"]
    if kind == "SELECTION":
        r["authority_role"] = "RUNTIME_SELECTOR_NOT_AUTHORITY_ISSUANCE"
        r["source_authority_path"] = expr
        r["typed_negative_semantics"] = "SELECTION_ONLY; NEEDS_CALLER_BRANCH_PROOF"
        r["current_pre553_successor"] = "UNBOUND / HOLD" if mod.startswith("ddm_v550") else "NOT_APPLICABLE_NONAUTHORITY_SELECTOR"
        r["current_first_consumer"] = "UNBOUND / HOLD"
    elif kind == "PERSISTENCE_OR_MUTATION":
        r["authority_role"] = "DERIVED_OUTPUT_NOT_AN_AUTHORITY_SOURCE"
        r["source_authority_path"] = "NOT_AN_INPUT"
        r["typed_negative_semantics"] = "PERSISTED_DATA_DOES_NOT_PROVE_ISSUED_AUTHORITY"
        r["current_pre553_successor"] = "UNBOUND / HOLD"
        r["current_first_consumer"] = "UNBOUND / HOLD"
    if mod == "ddm_v550_question_relation_authority.py" and symbol.split(".")[-1] in {
        "_build_index", "load_question_relation_authority",
        "resolve_question_relation_authority", "apply_question_relation_authority",
        "active_closed_35_waves", "validate_active_universe", "derive_legacy_latinobarometro_1995_residual"
    }:
        if "derive_legacy" in symbol:
            bind(r,"data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv",
                 "UNVERIFIED_GIT_BLOB_ONLY","700-row QRA calibration + 20 Latinobarometro residual","CLAIM_CONDITIONAL_LEGACY_QRA",
                 "derive 20 permitted residual identities","bad QRA hash/version/row count or overlap => reject",
                 "ddm_v550_question_relation_authority.py:500","pre553_empirical_authority.py:162")
        else:
            bind(r,FQ,FQ_SHA,"source/wave/country/question or var","MANDATORY_GOVERNED_RELATION",
                 "overwrite structural coordinates/polarity/eligibility by exact relation status",
                 "MISSING_AMBIGUOUS_EXCLUDED_W6_BLOCK; possible QUC-certified no-match preserve at :748-765",
                 "ddm_v550_bridge.py:1008 -> compile_v551_relation_evidence_atoms.py:160",
                 "pre553_empirical_authority.py:162",sha_basis="manifest")
    elif mod == "ddm_v550_response_semantics_authority.py" and symbol.split(".")[-1] in {
        "load_v551_registry_key_set", "load_response_semantics_contract_bindings",
        "bind_governed_response_semantics_contracts", "assert_v551_applicable_contract_compatibility"
    }:
        is_scale = "load_v551_registry_key_set" in symbol
        bind(r,SCALE if is_scale else BINDING,SCALE_SHA if is_scale else BINDING_SHA,
             "source/wave/var response contract; 145 certified hashes" if is_scale else "236 active source/wave/var bindings",
             "MANDATORY_RESPONSE_CONTRACT_IF_APPLICABLE",
             "validate manifest SHA, active count, certification; inherit exact scale key",
             "bad SHA/status/duplicate/missing/conflict -> error or REVIEW_REQUIRED",
             "ddm_v550_response_options.py:532 -> shard:1306/1368",
             "pre553_empirical_authority.py:162")
    elif mod == "ddm_v550_family_overlay.py" and ("load_family_overlay" in symbol or "load_family_overlay" in expr or "load_overlay_manifest" in symbol):
        bind(r,"DDM_AUTHORITY_ROOT/reports or caller_search_roots/<family><wave>_<type>*.csv",
             "UNAVAILABLE_DYNAMIC_OVERLAY","family/wave/var_name","CLAIM_CONDITIONAL_OVERLAY",
             "prefer canonical source/wave stem; rejects cross-family columns",
             "UNSUPPORTED_FAMILY/INVALID_SCHEMA/MISSING_REQUIRED/MISSING_OPTIONAL",
             "ddm_v550_question_use.py:2297-2333 and ddm_v550_bridge.py:1357",
             "pre553_empirical_authority.py:162")
    elif mod == "ddm_v550_question_use.py":
        if "load_family_overlay" in expr:
            bind(r,"--first-pass|semantic|position-conditioning|directionality-authority-dir/<family><wave>*.csv",
                 "UNAVAILABLE_DYNAMIC_OVERLAY","family/wave/var","CLAIM_CONDITIONAL_QUESTION_USE",
                 "first-pass, semantic, position-conditioning, directionality overlay joins and flags",
                 "missing optional -> None; ambiguous exact fallback -> RuntimeError; downstream gate depends on role",
                 "build_determinicity_wave_shard_v550.py:1567",
                 "pre553_empirical_authority.py:162")
        elif "_cached_override_frame" in expr or "load_question_use_overrides" in expr:
            bind(r,"data/ddm_build_copy/manifests/question_use_overrides.csv",
                 "29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479",
                 "source/wave/var/question","CLAIM_CONDITIONAL_OVERRIDE",
                 "manual role/use override with ambiguity guard","missing/read error -> empty, high-risk uses separately gated",
                 "build_determinicity_wave_shard_v550.py:1567",
                 "pre553_empirical_authority.py:162")
        elif "_cached_itinerary_frame" in expr or "load_question_wave_itinerary" in expr:
            bind(r,"data/ddm_build_copy/manifests/question_wave_itinerary.csv",
                 "866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3",
                 "source/wave/question","CLAIM_CONDITIONAL_ITINERARY",
                 "document use/source history per wave","missing/read error -> empty",
                 "build_determinicity_wave_shard_v550.py:1567",
                 "pre553_empirical_authority.py:162")
    elif mod == "ddm_v550_source_structure.py" and "load_question_structure_register" in symbol:
        bind(r,"DDM_QUESTION_STRUCTURE_REGISTER > data/ddm_build_copy/manifests/question_structure_register.csv",
             "UNAVAILABLE_REPO_CSV_ABSENT","source/wave/question/var","CLAIM_CONDITIONAL_STRUCTURE",
             "match typed split child, admin, open text, response structure",
             "missing CSV => empty frame, not a positive structure match",
             "build_determinicity_wave_shard_v550.py:1307/1558",
             "pre553_source_native_preimage_adapter.py:524")
    elif mod == "ddm_v550_shared_cache.py" and symbol.split(".")[-1] in {"cached_query_frame","load_cached_frame","write_cached_frame"}:
        bind(r,"data/ddm_repository_copy/v550/shared_cache/<kind>/<query_signature>/data.parquet",
             "UNAVAILABLE_DERIVED_CACHE","mapping query payload","OPTIONAL_DERIVED_CACHE",
             "query-signature reuse, no underlying DB revision in key","missing/metadata mismatch -> rerun; changed DB with same query key untested",
             "build_determinicity_repository_v550.py:307-410 -> shard:1255",
             "pre553_parquet_carrier.py")
    elif mod == "ddm_v550_bridge.py" and "apply_question_relation_authority" in expr:
        bind(r,FQ,FQ_SHA,"bridge row source/wave/country/var","MANDATORY_GOVERNED_BRIDGE_RELATION",
             "apply QRA coordinate/eligibility overwrite to V551 bridge row",
             "missing ambiguous block except certified QUC no-match exception",
             "compile_v551_relation_evidence_atoms.py:160-185",
             "pre553_empirical_authority.py:162",sha_basis="manifest")
    elif mod == "build_determinicity_wave_shard_v550.py" and "_build_authority_receipt" in symbol:
        bind(r,"four optional overlay types + QRA + response map",
             "NO_RECEIPT_EMITTED_PROVEN","source/wave","UNREACHABLE_DEFINED_PROVENANCE_HELPER",
             "would record file SHA/row count but no invocation anywhere in 177 scanned files",
             "NO_CALLSITE; cannot assert runtime receipt",
             "NONE_PROVED","pre553_empirical_authority.py:162")
    elif mod == "build_determinicity_wave_shard_v550.py" and ("build_response_authority_match_audit" in expr or "assert_response_authority_match_gate" in expr):
        bind(r,"--response-option-map or live codebooks","UNVERIFIED_RUNTIME_INPUT","source/wave/var/response option",
             "MANDATORY_SCOPED_RESPONSE_GATE","compare selected question map to response semantics; reject empty",
             "unmatched/empty response options -> V550_RESPONSE_SEMANTICS_EMPTY or match gate failure",
             "ddm_v550_bridge.py:1008 -> V551 atoms",
             "pre553_source_backed_c11_facade.py:502")
    elif mod == "build_determinicity_repository_v550.py" and ("pd.read_sql_query" in expr or "cached_query_frame" in expr):
        bind(r,"Postgres public.question_structural_mapping / respondent-long authority view",
             "NATIVE_DB_NOT_AVAILABLE","source/wave/country/var/respondent","MANDATORY_NATIVE_MAPPING_OR_RESPONSE",
             "select/alias/normalize native DB rows","missing source or DB error; query-key cache may remain stale",
             "build_determinicity_wave_shard_v550.py:1255-1380",
             "pre553_c11_ingest.py")

with (DST / "02_LEGACY_CALLSITES.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"enriched legacy site rows: {len(rows)}")
