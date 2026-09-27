"""Finalize the bounded court from frozen and retained evidence; no source read."""
from pathlib import Path
import sys,json,hashlib,csv,gzip,datetime
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_empirical_objects import ExactRef,AuthorityRef
from rawlsing_next.pre553_component_authority_vector import build_component_authority_vector_receipt,reload_component_authority_vector_receipt
OUT=Path(__file__).resolve().parent;E=OUT/'evidence'
TOKEN='PYAT_HQ124_LIVE_J_PASS__MINIMAL_PAIR_EXECUTED_FAIL_CLOSED__NO_POSITIVE_J_OCCUPANCY_PROVED_ON_DECLARED_SCOPE__ARCHITECTURE_REMAINS_CLOSED'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
def tsv(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def md(name,text):(OUT/name).write_text(text.strip()+'\n')
F=E/'FROZEN_PREVALUE_SELECTION.json';assert sha(F)=='508838fc85e84d82b5a5a5f5f4799c214dee277fe69605bec79de13bc2437814'
frozen=json.loads(F.read_text());specs=frozen['specimens'];assert len(specs)==2
assert sha(E/'CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv')=='b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64'
assert sha(E/'J01B_D5_EXACT_CARRIERS.zip')=='0765b7981fd710b315f8a6439be5a4ca5520c1b5fbd7bc166d72401c72774097'
assert '89 passed' in (E/'BOUNDED_RUNTIME_TESTS.txt').read_text()
law=ROOT/'PYAT_CONTROL_ROOM/21_HQD122_J_ROLE_CERTIFICATION_SUCCESSION_ADOPTION.md'
lawhash=sha(law);assert lawhash=='8c8557c7d2b8c362f4c78c4bd4506251833a1f7529a22f8735756599712b9019'
lawref=ExactRef('PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0',str(law.relative_to(ROOT)),lawhash)
# The adoption law governs incomplete-vector preservation. It does not grant
# component value authority, and these diagnostic receipts are not J2I channels.
rule=AuthorityRef('HQD-2026-09-27-122','1.0.0',lawhash)
replay=ExactRef('HQ124_PREVALUE_SPECIMEN_SELECTION@1',str(F.relative_to(ROOT)),sha(F))
sources=[];selection=[];identity=[];roles=[];empirical=[];adjudication=[];composition=[];negative=[];gates=[]
for s in specs:
 source=s['source'];c=s['candidate_row'];cid=c['current_source_structure_id'];names=s['governed_native_component_order'];qids=s['governed_question_implementation_order']
 r=json.loads((E/(source+'_PHYSICAL_EXECUTION.json')).read_text());assert r['full_decodes']==1 and r['freeze_sha256']==sha(F)
 assert datetime.datetime.fromisoformat(frozen['frozen_at_utc']) < datetime.datetime.fromisoformat(r['value_access_started_at_utc'])
 local=OUT/r['retained_raw_intermediate']['path'];assert sha(local)==r['retained_raw_intermediate']['sha256']
 raw=gzip.decompress(local.read_bytes());assert hashlib.sha256(raw).hexdigest()==r['retained_raw_intermediate']['uncompressed_payload_sha256']
 cached=json.loads(raw);assert cached['columns']==r['specimen_columns_consumed'] and cached['row_count']==r['physical_shape'][0]
 assert [x['source_row_ordinal'] for x in cached['rows']]==list(range(1,cached['row_count']+1))
 subject=ExactRef('CURRENT_J_CANDIDATE',cid,c['global_identity_sha256'])
 vector=build_component_authority_vector_receipt(vector_subject_ref=subject,authority_dimension_contract_ref=lawref,vector_rule_authority_ref=rule,governed_component_ids=qids,component_bindings=(),producer_replay_locator_or_reference_root=replay)
 assert reload_component_authority_vector_receipt(vector.as_dict()).as_dict()==vector.as_dict()
 assert vector.projection_disposition=='VECTOR_INCOMPLETE_COVERAGE' and vector.missing_component_ids==tuple(qids) and vector.scalar_value_digest is None
 dump(E/(source+'_MISSING_ROLE_LOAD_CAV.json'),vector.as_dict())
 evidence='evidence/'+source+'_PHYSICAL_EXECUTION.json'
 gate={'source':source,'candidate_id':cid,'L1':'EXACT_CURRENT_IDENTITY_BOUND','L2':'UNRESOLVED_WHOLE_SPECIMEN_APPLICABILITY','L3':'UNRESOLVED_CURRENT_FAMILY_ROLE_OCCUPANCY_ALL_COMPONENTS','L4':vector.projection_disposition,'L5':'NOT_EXECUTED__L1_L4_PERMISSION_NOT_SATISFIED','L6':'NOT_EXECUTED__EXACT_PREREQUISITES_ABSENT','L7':'NOT_EXECUTED__NO_M1_DISPOSITION','CAV_ref':vector.ref.as_dict(),'named_j_family_item_role_vector':'NOT_CONSTRUCTED__NO_COMPETENT_COMPONENT_ROLE_VALUE_AUTHORITY','LearnedEmpiricalDisposition':'NONE','release_core':'NONE','B5_lifecycle':'NOT_BOUND__NO_CURRENT_LIFECYCLE_AUTHORITY','architecture_reopen':False};gates.append(gate)
 sources.append(dict(source=source,exact_source_path=r['source_path'],source_sha256=r['source_sha256'],physical_rows=r['physical_shape'][0],physical_variables=r['physical_shape'][1],full_decodes=1,metadata_only_inspections=2,selected_specimen_ids=cid,selection_freeze_commit='6744e3e0',selection_freeze_sha256=sha(F),frozen_at_utc=frozen['frozen_at_utc'],value_access_started_at_utc=r['value_access_started_at_utc'],specimen_columns_consumed='|'.join(r['specimen_columns_consumed']),full_decoder_columns='ALL_SOURCE_COLUMNS__ONLY_FROZEN_SPECIMEN_AND_COUNTRY_CONSUMED',retained_intermediate=r['retained_raw_intermediate']['path'],retained_intermediate_sha256=r['retained_raw_intermediate']['sha256'],source_rereads=0,retry=r['retry'],physical_execution_receipt=evidence))
 selection.append(dict(source=source,specimen_ordinal=1,current_j_candidate_id=cid,current_joint_contract=s['current_joint_contract_id'],succession_state=s['current_joint_succession_row']['succession_state'],native_component_order='|'.join(names),question_implementation_order='|'.join(qids),current_scope_metadata_rows_considered=s['candidate_scope_metadata_rows_considered'],selection_rule=s['selection_reason'],qualified_slot_intersection='|'.join(s['projection_intersection']),whole_grid_coverage=False,freeze_commit='6744e3e0',freeze_sha256=sha(F),respondent_values_before_freeze=0,second_specimen='NOT_SELECTED__FIRST_DISTINGUISHES_WHOLE_SCOPE_FROM_QUALIFIED_PATH',retained_selection='evidence/FROZEN_PREVALUE_SELECTION.json'))
 identity.append(dict(source=source,current_j_candidate_id=cid,J01A_identity='EXACT_CURRENT_BINDING',global_identity_sha256=c['global_identity_sha256'],J01B_current_contract='CURRENT_JOINT_AUTHORITY_CONTRACT@1',J01B_succession=s['current_joint_succession_row']['succession_state'],current_component_set_and_order='EXACT_NATIVE_ORDER_PRESERVED',physical_slots='ALL_EXACT_UNIQUE_IN_DECODED_SOURCE',source_local_row_basis='SHA256_PLUS_1_BASED_ORIGINAL_ROW_ORDINAL',physical_row_count=r['physical_shape'][0],coadministration='CURRENT_J01A_NATIVE_GROUPING_AND_EXACT_SAME_ROW_EXTRACTION__NO_COMPOSABILITY_CLAIM',same_lawful_respondent='QUALIFIED_SUBSCOPE_ONLY__WHOLE_J_SEMANTICS_UNRESOLVED',applicability='UNRESOLVED_FOR_WHOLE_CURRENT_J_SPECIMEN',qualified_subscope=('q301_2/q301_7; exact D03 extensional R2/R7/R27 roots only' if source=='LiTS_I' else 'Q291G5/Q291P5; 97220 respondents, 194440 routing facts; 15996 eligible respondents per question'),whole_specimen_denominator='NOT_AUTHORIZED__NO_EXTENSION_FROM_SUBSCOPE',typed_exclusions=('D03 roots retained without broadening' if source=='LiTS_I' else 'ELIGIBLE_APPLICABLE/NOT_ELIGIBLE exact per qualified question; no G1-G6 extension'),evidence=evidence))
 for ordinal,(name,qid) in enumerate(zip(names,qids),1):
  roles.append(dict(source=source,current_j_candidate_id=cid,ordinal=ordinal,native_component=name,current_question_implementation_id=qid,family_role_occupancy='UNRESOLVED',semantic_role_token='NONE',current_component_correspondence='EXACT_J01A_NATIVE_TO_CURRENT_QUESTION_BINDING',competent_current_role_authority='NOT_PRESENT_IN_SUPPLIED_CURRENT_AUTHORITY',current_role_mapping='NOT_PRESENT',value_authority_ref='NONE__NOT_FABRICATED',CAV_binding_state='MISSING_BINDING__UNRESOLVED_LIVE_LOAD',qualified_B_projection_coverage=('COVERED_SUBSCOPE_ONLY' if name in s['projection_intersection'] else 'OUTSIDE_QUALIFIED_PROJECTION_SCOPE'),authority_dimension='J_FAMILY_ITEM_ROLE',CAV_projection=vector.projection_disposition,scalarization='REFUSED__INCOMPLETE_COVERAGE',negative_limit_refs=str(law.relative_to(ROOT))+'#sha256='+lawhash+'|evidence/FROZEN_PREVALUE_SELECTION.json#sha256='+sha(F),replay_ref='evidence/'+source+'_MISSING_ROLE_LOAD_CAV.json'))
 empirical.append(dict(source=source,current_j_candidate_id=cid,source_decode='EXECUTED_ONCE_POST_FREEZE',physical_extraction='ALL_FROZEN_COMPONENTS_RETAINED',qualified_projection=('ADOPTED_D03_ROOTS_RELOADED__FULL_GRID_NOT_BOUND' if source=='LiTS_I' else 'CURRENT_MATERIALIZER_STRUCTURAL_INPUT_BOUND__TWO_QUESTION_SUBSCOPE'),L1_L4_permission='NOT_SATISFIED',M01='NOT_EXECUTED',I03_I05='NOT_EXECUTED',query_predicate_refs='NONE_FOR_WHOLE_SPECIMEN__NO_QUERY_FABRICATED',empirical_universe_riskset='QUALIFIED_SUBSCOPE_REFS_RETAINED__FULL_J_RISKSET_UNRESOLVED',empirical_fact_refs='NONE',discovery_evidence_refs='NONE',reason='Projection and role-load authority do not cover whole governed J specimen',evidence=evidence))
 adjudication.append(dict(source=source,current_j_candidate_id=cid,named_prerequisite='j_family_item_role_vector',prerequisite_state='NOT_CONSTRUCTED__COMPETENT_COMPONENT_ROLE_AUTHORITY_ABSENT',generic_missing_load_CAV_ref=vector.ref.key,J2I_validator='PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0',validator_invocation='NOT_EXECUTED__PREREQUISITES_ABSENT',six_state_ordered_contribution_determinant='NONE__NO_ACTUAL_VALIDATOR_RESULT',LearnedEmpiricalDisposition='NONE',source_free_runtime_tests='89_PASS__SEPARATE_FROM_LIVE_OCCUPANCY',typed_gate='NOT_EXECUTED__NO_RULE_SATISFIED_CLAIM'))
 composition.append(dict(source=source,current_j_candidate_id=cid,exact_M1_disposition='NONE',M2='NOT_EXECUTED__NO_M1',B5='NOT_BOUND__NO_CURRENT_LIFECYCLE_AUTHORITY',I4='NOT_EXECUTED__NO_M1_OR_RELEASE_CORE',dependency_determinant_replay_explanation_closure='NO_LEARNED_PRODUCT_TO_COMPOSE__INPUTS_AND_LIMITS_BANKED',publication='NONE',current_selection='NONE',Field_Forge='NO_MUTATION',relation_objects='NONE'))
 for stage,state,reason in [('L2','UNRESOLVED','Whole grid lacks qualified applicability/risk-set binding; same-row cells do not authorize denominator'),('L3','UNRESOLVED','No competent per-component role value-authority and mapping in supplied current authority'),('L4','VECTOR_INCOMPLETE_COVERAGE','Every role-load binding missing; diagnostic CAV reload verified; no scalarization'),('L5','NOT_EXECUTED','Conditional permission L1-L4 not satisfied'),('L6','NOT_EXECUTED','Named role channel and M01 fact prerequisites absent'),('L7','NOT_EXECUTED','No exact M1 disposition; B5 lifecycle authority absent')]:
  negative.append(dict(source=source,current_j_candidate_id=cid,stage=stage,typed_state=state,reason=reason,absence_is_not_denial=True,positive_occupancy_proved=False,architecture_reopen=False,evidence='evidence/LIVE_GATE_ADJUDICATION.json|evidence/'+source+'_MISSING_ROLE_LOAD_CAV.json'))
dump(E/'LIVE_GATE_ADJUDICATION.json',{'terminal':TOKEN,'declared_scope':'one LiTS I q301 grid + one WVS7 Q291G grid; no estate-wide verdict','source_gates':gates,'generic_CAV_status':'DIAGNOSTIC_MISSING_ROLE_LOAD_ONLY__NOT_NAMED_J2I_ROLE_CHANNEL','architectural_requirement_unrepresentable':False})
for name,rows in [('01_SOURCE_IDENTITY_AND_READ_DISCIPLINE.tsv',sources),('02_PREVALUE_SPECIMEN_SELECTION.tsv',selection),('03_LIVE_J_IDENTITY_AND_COADMINISTRATION.tsv',identity),('04_ROLE_OCCUPANCY_AND_COMPONENT_AUTHORITY.tsv',roles),('05_LIVE_EMPIRICAL_EXECUTION_LEDGER.tsv',empirical),('06_J2I_M1_ADJUDICATION_LEDGER.tsv',adjudication),('07_M2_B5_I4_LIVE_COMPOSITION_LEDGER.tsv',composition),('08_TYPED_NEGATIVE_AND_REFUSAL_LEDGER.tsv',negative)]:tsv(name,rows)
md('00_RETURN.md',f'''# HQ124 LiTS I + WVS7 — bounded typed-negative live court

Terminal: `{TOKEN}`.

Commission: `c44df7f99fcf86763431ea8c98f74c0245c94670`; branch `agent/rabochii-pyat-hq124-lits1-wvs7-live-j-authority-load-r1`.

Scope is exactly two frozen specimens: LiTS I `cssu.r2.lits.2006.c675f00abc752045b7af` (q301_1–q301_11) and WVS7 `cssu.r2.wvs.w7.d395c3494c5c7f5e301b` (Q291G1–Q291G6). One specimen per source; no second specimen, estate-wide respondent court, cross-source pooling or comparability claim. The 1,411-row carrier supplied current candidacy metadata only, filtered to these source scopes.

Both Library artifacts were downloaded after authenticated access and match canonical Git hashes: J01A CSV `b21a79947f19f4c520ea493480a38ef8b23cb6797444eeb913bc8575b6cafb64`; D5 ZIP `0765b7981fd710b315f8a6439be5a4ca5520c1b5fbd7bc166d72401c72774097`. D5 exact members and provenance are retained. The earlier access block is resolved; this terminal reflects live selected specimens.

Selection froze in commit `6744e3e0`, receipt SHA-256 `{sha(F)}`, before either respondent-value read. Selection used current identities and selected-B slot correspondence, with no outcome statistic or historical fallback. Each source was decoded once and had two metadata-only inspections (preparation and current decoder). WVS7's post-decode metadata serialization failure was recovered from retained incidence and preparation metadata, with zero source rereads. Its complete current-decoder metadata digest was not retained or claimed.

L1 succeeds: exact current identity, component set/order and J01B succession bind. LiTS I is EXACT_CURRENT_SUCCESSOR; WVS7 is CURRENT_SUCCESSOR_CHANGED_SCOPE with exact current identity. All selected native slots resolve uniquely in the physical source; retained cells preserve original source-local row ordinals. Native grouping and physical row evidence are separate from lawful whole-grid applicability.

L2 does not authorize full-grid execution. LiTS I's qualified selected-B authority covers q301_2/q301_7; adopted D03 R2/R7/R27 memberships are retained, without extension to the other nine components. WVS7's current materializer binds 97,220 respondents and 194,440 routing facts for Q291G5/Q291P5, with 15,996 eligible respondents per question. Only G5 overlaps the frozen G grid. This projection cannot authorize the other five G components or a whole-grid denominator. Physical missingness is not applicability.

L3 records UNRESOLVED family-role occupancy for all 17 components: their competent current role value-authority and exact mappings are absent from the supplied load. Labels, order, grouping, historical membership and values cannot supply them. L4 builds and reload-verifies one generic diagnostic ComponentAuthorityVectorReceipt per specimen: every role binding missing, VECTOR_INCOMPLETE_COVERAGE, scalar digest null. Exact HQD-122 adoption law governs incomplete-vector preservation; no component value-authority refs are fabricated. These receipts are not named J2I role-producer outputs.

L5–L7 are conditionally NOT_EXECUTED. L1–L4 do not permit whole-specimen M01/I03/I05; exact J2I/M1 prerequisites are absent; no LearnedEmpiricalDisposition exists for M2/I4. No six-state contribution determinant, lifecycle authorization, publication, current selection or Field Forge relation object is manufactured. The 89 bounded current source-free runtime tests pass separately and prove no live positive occupancy.

Architecture remains closed: identity/order, row/risk-set dependencies, unresolved roles, incomplete loads and withheld downstream execution have current representation and owners. No unrepresentable live semantic grain was exposed. This result covers these two specimens, not either entire source or the 1,411-candidate estate.

Owned changes are confined to this return directory. Outcome extracts remain local and ignored by Git, with exact path/hash receipts. Earlier preparation-only outputs are superseded. See 12_EVIDENCE_MAP.md for replay boundaries.
''')
md('09_ARCHITECTURE_REOPEN_OR_NO_REOPEN.md','''# No architecture reopen witness

`SOURCE_FREE_PRE553_ARCHITECTURE_COMPLETE_AT_AUDITED_GRAIN` remains the HQD-124 theorem. Neither specimen exposes a required semantic grain without a current owner or representation.

L1 identity/order is represented by J01A and current J01B. L2 row/risk-set/routing dependencies have exact source-specific representation on qualified subscopes; absent whole-grid applicability remains unresolved. L3 roles have adopted HQD-122 law and a current producer, but these components' competent value authority is absent from the supplied load. L4 incomplete coverage is represented by current CAV, with no scalarization. L5–L7 preserve missing prerequisites by withholding conditional execution.

No new semantic schema, core change or Field Forge mutation is proposed. The WVS7 serialization failure is a court-output issue recovered from retained bytes, not an unrepresentable semantic requirement. Generic diagnostic CAVs attest missing bindings; they are not named J2I role vectors. A missing positive load does not reopen architecture.
''')
md('10_FIELD_FORGE_HANDOFF_PACKET_IF_ANY.md','''# No Field Forge handoff product

Neither whole selected specimen produced an exact B learned product or LearnedEmpiricalDisposition. No Field Forge relation object or mutation was made. Retained inputs and gate limits are court evidence, not relation truth or a publishable handoff. B5 is not bound; no publication or current selection occurs.
''')
md('11_NEXT_SCOPE_RECOMMENDATION.md','''# Next scope recommendation

Keep architecture closed. A later positive-occupancy court needs competent current whole-specimen authority: exact component role/value mappings, source-specific coadministration/applicability and extensional risk-set coverage, and selected-B projection permission for every governed component.

For LiTS I this means the selected 11-component Q301 grid; for WVS7 the selected six-component Q291G grid. Do not substitute an unrecognized two-variable candidate because a B projection exists, default roles, or broaden denominators from physical nonmissingness. The first specimens already distinguish partial qualified-path capacity from missing whole-specimen occupancy; no second specimen is justified here.

Replay retained local incidence and committed WVS7 structural input. This result recommends no broader estate scan, added source, architecture reopening, new source read, Field Forge write or PRE-V3 target-use grant.
''')
md('12_EVIDENCE_MAP.md','''# Evidence and replay map

- FROZEN_PREVALUE_SELECTION.json: exact current specimen/succession rows, native/current order, binder hashes and pre-value selection law; freeze commit 6744e3e0.
- CURRENT_J_CANDIDATE_UNIVERSE_FROZEN.csv and J01B_D5_EXACT_CARRIERS.zip: exact Library artifacts matching Git pointers. D5 extracted members retain exact bytes; historical residual and match files are retained for archive integrity, not role/selection authority.
- AUTHORITY_RECOVERY_PROVENANCE.json, J01A/J01B pointers, D2 crosswalk and user Library-presence receipt: input provenance. Library IDs libfile_3f6b0d93bb74819195702d808e3093ec and libfile_64dd382a81148191a7645c98972802f4.
- LITS_I_METADATA.json and WVS7_METADATA.json: preparation metadata-only receipts. LiTS_I_CURRENT_DECODER_METADATA.json: retained current-decoder metadata. No complete WVS7 current-decoder metadata digest is claimed after serialization failure.
- LiTS_I_PHYSICAL_EXECUTION.json and WVS7_PHYSICAL_EXECUTION.json: source hashes/shapes, read times, consumed columns, physical counts and exact local intermediate hashes. Physical nonmissing counts are not semantic denominators.
- LiTS_I_QUALIFIED_D03_ROOTS.json: adopted exact extensional R2/R7/R27, restricted to q301_2/q301_7; no outcome-derived applicability.
- WVS7_CURRENT_STRUCTURAL_INPUT.json: current materializer's exact ordinal/name/missing declarations and typed retained B_COUNTRY values. Replay through materialize_from_structural_input without SAV access. Country routing inputs are committed; Q291 outcome values are local only.
- WVS7_CURRENT_PROJECTION_BINDING.json: current carrier-neutral projection binding; two response slots, nine authority snapshots, 97220 respondent/row bindings and 194440 routing facts. This is not a full G-grid projection or M01 fact.
- WVS7_POST_DECODE_RECOVERY.json: exact serialization failure and zero-source-reread recovery. The full source decode and selected incidence retention succeeded before failure.
- LiTS_I_MISSING_ROLE_LOAD_CAV.json and WVS7_MISSING_ROLE_LOAD_CAV.json: reload-verified generic diagnostic missing-load receipts; every governed role binding missing. They are not named J2I role channels and provide no component value authority.
- LIVE_GATE_ADJUDICATION.json: actual L1–L7 gates; no manufactured validator/M1/determinant/release outcome.
- BOUNDED_RUNTIME_TESTS.txt: 89 current source-free CAV/J-role/M1/M2 tests, independent of live occupancy. Test code unchanged.
- HQ123_08_SOURCE_FREE_VS_LIVE_OCCUPANCY_BOUNDARY.md and HQ123_09_EXACT_REMAINING_GAPS.tsv: exact adopted court at e7e6fdb25031b8d0ebc1bc8b357460814f385f01.
- EVIDENCE_SHA256.json: committed evidence byte sizes/hashes, excluding itself. Local raw hashes are in execution receipts.

execute_physical_court.py verifies/reuses existing receipts without source rereads and refuses automatic rereads after interruption. recover_wvs_from_retained.py uses exact local incidence plus retained metadata. finalize_return.py regenerates ledgers and verifies diagnostic CAVs without decoding sources. prepare_return.py is disabled to protect the frozen carrier.

Local outcome extracts: local_intermediates/LiTS_I_selected_physical_incidence.json.gz and local_intermediates/WVS7_selected_physical_incidence.json.gz. Each retains exact physical type/float64 hex and original row ordinal; Git ignores them. Full physical replay requires their exact bytes or separately justified original-source access. Single-read discipline is backed by retained markers/hashes/receipts and documented session execution, not a cryptographic proof of read count.
''')
dump(E/'EVIDENCE_SHA256.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(E.iterdir()) if p.is_file() and p.name!='EVIDENCE_SHA256.json'})
print(TOKEN);print('Verified two frozen specimens, one full decode each, 17 missing role loads, two exact diagnostic CAVs and 89 runtime tests.')
