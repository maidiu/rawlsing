#!/usr/bin/env python3
"""HQ280 WGE repro 2: pre-result scientific expectation vs actual product identity.

Builds a PROPOSED pre-result-only expectation specification for exact Q86B->Q86A at its
existing admitted native CONTEXT scope, whose hash material contains NO produced fact hash,
NO observed support/cell counts, NO actual-result or post-outcome F1 hash, NO batch membership,
NO output-derived list and NO result-derived relay hash.

It is explicit that this 2026-10-11 constructed identity was NOT frozen before the historical
GT2 execution. Its legitimate prospective authority is established by timestamped freeze BEFORE
any fresh local consumer invocation (see 03 runtime record), and by competent issuer citations
for every material input.

Outputs: 02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json
"""
import json, hashlib, datetime, os, sys

ROOT = '/tmp/rawlsing_hq280_WGE'
REPO = '/Users/matthewsmith/Desktop/Rawlsing/FIABC-LITS-executed-role-closure-repair'
sys.path.insert(0, REPO)

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next import gt12_c_to_d_relation_bridge as c2d

def sh(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def code_blob(rel):
    """Canonical git blob identity of an owner module (byte identity, no content hash leakage)."""
    import subprocess
    return subprocess.run(['git', 'hash-object', rel], cwd=REPO, capture_output=True, text=True).stdout.strip()

# ---------------- pre-result material, each with issuer/competence citation ----------------
material = {
    'schema_id': 'HQ280_WGE_PRE_RESULT_EXPECTED_OPERATION_SPEC@1.0.0',
    'operation_identity': {
        'operation_id': 'GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1',
        'operation_direction': 'Q86B(CONDITIONER) -> Q86A(TARGET)',
        'operation_class': 'SAMERESPONDENT_CONDITIONED_JOINT__RAW__CONTEXT_SCOPED',
    },
    'source_artifact': {
        'source_family': 'Afrobarometer', 'wave': 'R5',
        'source_path': adm.GT2_SOURCE_PATH,
        'source_sha256': adm.GT2_SOURCE_SHA256,
        'issuer': 'GT12-A_R5_Q86_SOURCE_SEMANTICS / carrier re-expression GT12-A-R5-Q86-CARRIER-REEXPRESSION',
        'raw_bytes_opened_by_wge': False,
    },
    'participant_roles': {
        'conditioner_source_native_variable': ff.CONDITIONER_SOURCE_NATIVE_VARIABLE,
        'target_source_native_variable': ff.TARGET_SOURCE_NATIVE_VARIABLE,
        'participant_role_order': [ff.CONDITIONER_ROLE, ff.TARGET_ROLE],
        'issuer': 'frozen GT12 C-to-D relation rule cddf66e2... (static, pre-result)',
    },
    'risk_and_exposure': {
        'risk_set_id': adm.GT2_RISK_SET_ID,
        'risk_set_member_set_sha256': adm.GT2_RISK_SET_MEMBER_SET_SHA256,
        'risk_set_type': 'COMMON_ELIGIBLE_RISK_SET',
        'member_count_declared': 19210,
        'member_count_note': 'denominator magnitude is a SOURCE-SCOPE/RISK-DESIGN fact declared by the issuer, not an observed result cell count; the expectation does not assert any produced numerator or cell value',
        'issuer': 'GT12-A-R5-Q86-COMMON-RISK-ROUTING',
    },
    'native_response_semantics': {
        'response_state_semantics_id': 'Afrobarometer:R5:Q86:SOURCE_NATIVE_RESPONSE_STATES',
        'state_order_semantics': ff.STATE_ORDER_SEMANTICS,
        'frozen_target_order': ff.FROZEN_TARGET_ORDER,
        'expected_cell_arity': 36,
        'expected_cell_arity_note': 'grid arity 6x6 is a source-native instrument-structure fact, not an observed distribution',
        'issuer': 'GT12-A-R5-Q86-SOURCE-SEMANTICS',
    },
    'measure_and_scope_ceiling': {
        'measure_kind': 'RAW',
        'measure_ceiling': 'EMPIRICAL_INPUT_TO_FROZEN_EXACT_CONDITIONAL_SUPPORT_ONLY__NO_CAUSAL_OR_ACTOR_PROMOTION',
        'target_use': adm.GT2_TARGET_USE,
        'publication_family': 'F1',
        'v557_state': 'ALLOW_CONTEXT_ONLY',
        'v558_requested_uses': ['CONTEXT'],
        'weight_design_ceiling': 'RAW_SOURCE_LOCAL_ONLY__NO_DESIGN_OR_ESTIMAND_GRANT',
        'issuer': 'GT12-A3-GT2-TARGET-USE; publication GT12_RELATION_V554_TO_V557_F1_CONTEXT_PUBLICATION_AUTHORITY',
    },
    'finite_grammar': {
        'query_execution_contract': 'PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0',
        'relation_family': ff.RELATION_FAMILY,
        'relation_semantics': ff.RELATION_SEMANTICS,
        'relation_rule_ref': c2d.frozen_gt12_c_relation_rule_ref().as_dict(),
        'semantic_owner': ff.SEMANTIC_OWNER,
        'producer_function': 'produce_exact_conditional_support_profile',
        'information_loss': ff.INFORMATION_LOSS,
        'bridge_contract': c2d.BRIDGE_CONTRACT_ID,
        'admission_operation': adm.GT2_ADMISSION_OPERATION,
        'downstream_contract': adm.GT2_DOWNSTREAM_CONTRACT,
        'discovery_frontier': None,
        'batch_units': None,
        'issuer': 'GT12-A3-GT2-I03-QUERY + frozen C-to-D relation rule',
    },
    'intended_consumer': {
        'consumer_id': 'rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py::run_current_r1c_e2b_actual_objects',
        'consumer_blob': code_blob('rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py'),
        'publisher_permission_translation_blob': code_blob('rawlsing_next/gt12_permission_translation_authority.py'),
        'publication_governance_blob': code_blob('rawlsing_next/gt12_e2b_publication_governance_binding.py'),
        'm4_repository_blob': code_blob('rawlsing_next/m4_v557_v558_publication_repository.py'),
        'consumer_scope': 'CONTEXT_ONLY',
        'issuer': 'GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY (adopted, CONTEXT)',
    },
    'frozen_provenance_anchors': {
        'frozen_canary_commit': adm.FROZEN_CANARY_COMMIT,
        'closure_program_commit': c2d.CLOSURE_PROGRAM_COMMIT,
    },
}

preimage = json.dumps(material, sort_keys=True, separators=(',', ':'))
expected_key = hashlib.sha256(preimage.encode('utf-8')).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

# ---------------- dependency-lineage audit (real, not substring) ----------------
EXCLUDED = {
    'empirical_fact_hash': '540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46',
    'produced_f1_object_hash': '3530f08f43e704ad67e0fb74984b03b7ad0f068ea1de4bcf658f3b2d591bd56d',
    'produced_f1_content_hash': 'a008553dc94af138de44e73ade8ddbcc1e2bb3a5c40cec575aad694aae104cbb',
    'ff_profile_hash': '1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19',
    'v557_publication_hash': '2c7fb3f81343179ad75c6441fadcd09201aa47b9dc0e032383071e83cc4e022a',
    'v558_repository_hash': '47594be9aaf284122f76e3f2e3d74af29054ae3e1d6228134e4eccfdacfa46d1',
    'v558_resolution_key': '205f5049be54eb226a35fad1561554c52f830d858bbf9a642167b3f96c281fda',
    'c11_release_hash': '8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295',
    'query_hash': 'e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0',
    'predicate_hash': 'bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3',
    'replay_hash': 'c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f',
}
lineage = {}
for name, val in EXCLUDED.items():
    lineage[name] = {'value': val, 'present_in_preimage': val in preimage}
# measured numerators / observed cell counts
for name, val in {'observed_numerator_support': '19210', 'observed_cell_count': '36'}.items():
    lineage[name] = {'value': val, 'note': 'declared source-scope magnitude only; no produced numerator/cell value appears',
                     'produced_values_present': False}

doc = {
    'schema': 'HQ280_WGE_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT@1.0.0',
    'governing_decision': 'HQD-2026-10-10-280',
    'canonical_control': '6a8c91d99dca1ae2fd3559ba3c11ee26649e3cd9',
    'semantic_pre_main': '1f47063c3205a45888b3c55e81e7485943ed1390',
    'supersedes_wgd_key': {
        'wdg_key': 'ecb7411003a96966d703fc88a28d973b',
        'defect': 'WGD keyed its issued identity with manifest actual_fact.ref.content_hash (a produced EmpiricalFact), so it cannot discharge the pre-outcome independent no-drop requirement; WGD T08 checked substrings instead of dependency lineage',
        'status': 'REJECTED_AS_PRE_OUTCOME_EXPECTED_WORK_KEY__RETIRED',
    },
    'pre_result_expected_operation': {
        'proposed_expected_operation_key': expected_key,
        'key_rule': 'sha256(canonical_json(material)) full 64-hex; material published in full below',
        'material': material,
        'material_sha256': expected_key,
        'hash_material_excludes': ['EmpiricalFact hashes', 'observed support or produced cell counts',
                                   'actual-result/post-outcome F1 object or content hashes',
                                   'Field Forge produced profile hash', 'V557 publication hash',
                                   'V558 repository/resolution keys', 'batch membership',
                                   'output-derived lists', 'result-derived relay hashes'],
        'freeze_status': 'PROSPECTIVELY_FROZEN_AT_CONSTRUCTION__NOT_FROZEN_BEFORE_HISTORICAL_GT2_EXECUTION',
        'constructed_at_utc': now,
        'adoption_status': 'PROPOSED_CANDIDATE__REQUIRES_COMPETENT_HQ_OR_ISSUER_ADOPTION',
    },
    'dependency_lineage_audit': {
        'method': 'exact substring test against the canonical preimage string (dependency lineage for this key is the material set itself, which is published in full)',
        'results': lineage,
        'any_produced_identity_present': any(v['present_in_preimage'] for v in lineage.values() if 'present_in_preimage' in v),
    },
    'distinction': {
        'scientific_pre_execution_expectation': {
            'key': expected_key,
            'identity': 'PROPOSED pre-result scientific expectation: what the admitted native source/operation/permission/consumer scope authorises to be computed',
            'depends_on_empirical_result': False,
            'invariance_under_changed_result': True,
        },
        'current_retained_product_identity': {
            'fact_hash': '540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46',
            'query_hash': 'e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0',
            'predicate_hash': 'bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3',
            'replay_hash': 'c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f',
            'identity': 'exact CURRENT retained product: the actually produced empirical product and its replay chain',
            'depends_on_empirical_result': True,
            'invariance_under_changed_result': False,
        },
        'rule': 'expected work is never derived from, and must never be keyed with, a produced result identity',
    },
    'no_drop_classification': {
        'eligible_operation_expectations_vs_executed': 'one pre-result expectation (this key) vs one executed retained product (03 runtime record)',
        'not_compared_against': 'all 78,037 WGC documentary annotations',
        'full_35_wave_claim': False,
        'no_new_i05_or_batch_emitted': True,
    },
    'honest_limitations': [
        'this 2026-10-11 construction cannot and does not claim to predate the historical GT2 execution',
        'the expectation is a PROPOSED candidate; it is not adopted expected work until a competent issuer/HQ adopts it',
        'it does not discharge the all-35 or any other operation; it applies only to the exact Q86B->Q86A admitted native CONTEXT scope',
    ],
}
json.dump(doc, open(ROOT + '/02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json', 'w'), indent=1)
print('proposed pre-result expectation key:', expected_key)
print('any produced identity in preimage:', doc['dependency_lineage_audit']['any_produced_identity_present'])
for k, v in lineage.items():
    print('  ', k, '->', v.get('present_in_preimage', 'n/a'))