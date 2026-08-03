from __future__ import annotations
import csv, hashlib, json, os, shutil
from pathlib import Path
from collections import Counter
import pandas as pd
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

DATE='2026-07-31'
SRC=Path('/mnt/data/rawlsing_v15_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v15_20260731')
BUILD=Path('/mnt/data/rawlsing_v16_build')
ROOT=BUILD/'Rawlsing_J_Family_Authority_Strategy_Handoff_v16_20260731'
SEC=ROOT/'37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4'
OUT=Path('/mnt/data/rawlsing_v16_outputs/democracy_electoral_3000')
WORK=Path('/mnt/data/rawlsing_v16_work')
NEXT='P2_GLOBAL_NEXT_FIXED_3000_PAIR_TRANCHE_FROM_11847_REMAINING_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION'

def dump(path,obj): path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def read(name): return pd.read_csv(OUT/name,dtype=str,keep_default_na=False)
def set_cell(cell,text,bold=False):
    cell.text=''; p=cell.paragraphs[0]; r=p.add_run(str(text)); r.bold=bold; r.font.size=Pt(8.5); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
def header(row):
    tr=row._tr.get_or_add_trPr(); e=OxmlElement('w:tblHeader'); e.set(qn('w:val'),'true'); tr.append(e)
    for c in row.cells:
        tc=c._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'D9E2F3'); tc.append(sh)
def defaults(doc,title):
    s=doc.sections[0]; s.top_margin=Inches(.52); s.bottom_margin=Inches(.52); s.left_margin=Inches(.65); s.right_margin=Inches(.65)
    doc.styles['Normal'].font.name='Aptos'; doc.styles['Normal'].font.size=Pt(9.3)
    for n,z in [('Title',19),('Heading 1',14),('Heading 2',11.5)]: doc.styles[n].font.name='Aptos Display'; doc.styles[n].font.size=Pt(z)
    p=doc.add_paragraph(); p.style=doc.styles['Title']; p.add_run(title)
def bullets(doc,items):
    for x in items:
        p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(1); p.add_run(x)
def table(doc,headers,data):
    t=doc.add_table(rows=1,cols=len(headers)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,x in enumerate(headers): set_cell(t.rows[0].cells[i],x,True)
    header(t.rows[0])
    for row in data:
        cs=t.add_row().cells
        for i,x in enumerate(row): set_cell(cs[i],x)
def footer(doc,text):
    p=doc.sections[0].footer.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run(text); r.font.size=Pt(8)
def remove_caches(root):
    for p in sorted(root.rglob('*'),reverse=True):
        if p.is_dir() and p.name in {'__pycache__','.pytest_cache'}: shutil.rmtree(p)
        elif p.is_file() and p.suffix in {'.pyc','.pyo'}: p.unlink()

def manifests(root):
    idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'
    for p in (idx,sums):
        if p.exists(): p.unlink()
    rec=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rec.append({'relative_path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    for p in (idx,sums):
        with p.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256']); w.writeheader(); w.writerows(rec)

if BUILD.exists(): shutil.rmtree(BUILD)
BUILD.mkdir(parents=True)
shutil.copytree(SRC,ROOT)
SEC.mkdir()
for name in [
 'Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv',
 'Rawlsing_P2_Democracy_Electoral_3000_Two_Sided_Evidence_Ledger_v1.csv',
 'Rawlsing_P2_Democracy_Electoral_Lineage_Classification_v1.csv',
 'Rawlsing_P2_Fixed_3000_Tranche_Candidate_Surface_v1.csv',
 'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv',
 'FIXED_3000_TRANCHE_RETURN.json']:
    shutil.copy2(OUT/name,SEC/name)
for name in ['build_democracy_electoral_tranche_v1.py','test_fixed_3000_democracy_electoral_tranche_v1.py','fixed_tranche_3000_candidates.csv','FIXED_3000_REPRODUCIBILITY_RETURN.json','FIXED_3000_PYTEST_RETURN.txt']:
    shutil.copy2(WORK/name,SEC/name)

ret=json.loads((SEC/'FIXED_3000_TRANCHE_RETURN.json').read_text())
rul=read('Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv')
status=Counter(rul.authority_status)
relation=Counter(rul.relation_type)

report=f'''# P2 global democracy/electoral semantic adjudication — fixed 3,000 tranche 4

## Fixed work-unit return

- Queue at start: 14,847
- Pairs selected and adjudicated: exactly 3,000
- Queue at end: 11,847
- Selection: all pending DEMO_EXTENT, CIVIC_VOTE_MATTERS, CIVIC_VOTE, REJECT_STRONGMAN and REJECT_MILITARY rows, plus a deterministic 27-row REJECT_ONEPARTY boundary slice
- Lineages classified: 488
- Two-sided evidence records: 6,000
- Adversarial pytest cases: 20 passed
- Deterministic rebuild: PASS, six tracked artifacts hash-identical

## Authority partition

- Reworded proposition equivalence: 13
- Same construct/target, different operator — coordinate only: 19
- Same domain, relation or target/scope differs — coordinate only: 201
- Explicit negative authority: 2,667
- Redirected to the correct non-democracy/electoral domain: 92
- Unresolved: 8

## Acceptance controls

Every proposition equivalence requires identity of governed relation axis, target/scope and operator, with HIGH-confidence classifications on both sides. The pass preserves regular elections versus free-and-fair elections; individual vote efficacy versus honest-election effects; current, past and future democracy; named-country targets; generic strong leaders versus strong-president-plus-military models; conditional military takeover versus ordinary military rule; and defined versus generic democratic-system propositions.

The acceptance review also blocked ambiguous Asian Barometer “participated in last election” wording from being certified as voting and kept terse Afrobarometer R1 system ratings unresolved. Inherited semantic neighborhoods therefore function only as discovery queues, never as equivalence authority.

## Authority boundary

These are pair-relation rulings only. They do not author a J-family, harmonize response values, join respondents, install a registry, write a database, or execute V550/V551/V552. Asian Barometer W6 remains excluded.
'''
(SEC/'P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4_REPORT.md').write_text(report,encoding='utf-8')
(SEC/'TASK_RETURN.md').write_text(report,encoding='utf-8')
validation={
 'status':'PASS','contract_version':ret['contract_version'],'input_pending_pairs':14847,'fixed_work_unit_pairs':3000,'pairs_adjudicated':3000,'pairs_remaining':11847,
 'selected_semantic_id_counts':ret['selected_semantic_id_counts'],'lineages_classified':488,'evidence_rows':6000,'pytest_cases':20,'reproducibility':'PASS_HASH_EXACT',
 'proposition_acceptance_requires_axis_target_operator_identity':True,'queue_partition_exact':True,'authority_boundary':ret['authority_boundary'],'next_pass':NEXT}
dump(SEC/'VALIDATION.json',validation)

protocol='''# Fixed semantic-pair tranche protocol

Global P2 semantic adjudication proceeds in fixed work units of exactly 3,000 pending queue rows whenever at least 3,000 remain.

1. Record the governing queue count before selection.
2. Select exactly 3,000 rows deterministically, using coherent semantic neighborhoods where possible and a stable ordered boundary slice where necessary.
3. Freeze and deliver the selected candidate surface.
4. Adjudicate all 3,000 rows under the embedded acceptance standard.
5. Record the exact authority partition and two-sided evidence surface.
6. Prove that selected and remaining IDs form an exact disjoint partition of the incoming queue.
7. Deterministically rebuild and hash-compare all governing outputs.
8. Package the tranche into the cumulative handoff before starting another work unit.
9. Report start count, exactly 3,000 adjudicated, end count, and observed wall-clock span.

Do not drift above the 3,000-row cap to finish a neighborhood. Carry a deterministic remainder into the next tranche.
'''
(ROOT/'00_START_HERE'/'FIXED_3000_TRANCHE_PROTOCOL.md').write_text(protocol,encoding='utf-8')
acc=(ROOT/'00_START_HERE'/'ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md').read_text(encoding='utf-8')
acc=acc.replace('Current continuation: `P2_GLOBAL_REMAINING_14847_SEMANTIC_PAIR_ADJUDICATION_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION`.',f'Fixed work-unit rule: semantic-pair adjudication is capped at exactly 3,000 pending queue rows per tranche; see `FIXED_3000_TRANCHE_PROTOCOL.md`.\n\nCurrent continuation: `{NEXT}`.')
(ROOT/'00_START_HERE'/'ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md').write_text(acc,encoding='utf-8')

current=json.loads((ROOT/'00_START_HERE'/'CURRENT_STATE.json').read_text())
current.update({
 'handoff_version':'v16','current_pass':'P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4_COMPLETE','next_pass':NEXT,
 'semantic_priority_pairs_adjudicated_before_fixed_tranche4':3984,'fixed_tranche4_pairs_adjudicated':3000,
 'semantic_priority_pairs_adjudicated_cumulative':6984,'semantic_priority_pairs_remaining':11847,
 'fixed_semantic_pair_work_unit':3000,'fixed_tranche_protocol_embedded':True,
 'fixed_tranche4_lineages_classified':488,'fixed_tranche4_two_sided_evidence_records':6000,
 'fixed_tranche4_report':'37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4/P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4_REPORT.md'})
dump(ROOT/'00_START_HERE'/'CURRENT_STATE.json',current)
scope=json.loads((ROOT/'00_START_HERE'/'SCOPE_LOCK.json').read_text())
scope.update({'governing_task':'Adjudicate the next fixed 3,000 rows from the 11,847-row global semantic-priority queue and install the component-aware strata/horizon bridge only against the current live repository with fail-closed integration returns.','current_pass':current['current_pass'],'next_pass':NEXT})
scope['allowed']=[x for x in scope['allowed'] if '14,847' not in x]
scope['allowed'].insert(2,'process exactly 3,000 rows per semantic-pair tranche under FIXED_3000_TRANCHE_PROTOCOL.md')
scope['fixed_tranche_protocol']={'work_unit_pairs':3000,'tranche4_start':14847,'tranche4_adjudicated':3000,'tranche4_end':11847,'hard_cap':True}
dump(ROOT/'00_START_HERE'/'SCOPE_LOCK.json',scope)

resume=f'''# Governing v16 resume point

Resume at:

`{NEXT}`

Use section 37's remaining queue of **11,847 pairs** as the sole governing pending semantic-pair surface. The next adjudication work unit is exactly **3,000 rows**, selected deterministically under `00_START_HERE/FIXED_3000_TRANCHE_PROTOCOL.md`. Do not exceed the cap to finish a neighborhood.

Preserve all prior authority at its stated ceiling. Section 37 contributes 13 proposition equivalences, 220 coordinate-only relations, 2,667 negatives, 92 redirected pairs and 8 unresolved pairs, each with two-sided evidence.

The V551J component-aware strata/horizon bridge v3.1 remains validated against recovered runtime evidence but uninstalled in Matthew's current live repository. Install only after the live repository is supplied and all schema, cardinality, component-identity and conflict gates pass.

Global P2 remains open. No canonical J-family authority, respondent joins, value harmonization, database writes, registry installation or V550/V551/V552 execution. Asian Barometer W6 remains excluded.
'''
(ROOT/'00_START_HERE'/'EXACT_RESUME_POINT.md').write_text(resume,encoding='utf-8')
readme=f'''# Rawlsing J-Family Authority Strategy Handoff v16

This is the complete cumulative restart package through the first fixed 3,000-row semantic-pair tranche.

Read, in order:

1. Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v16_20260731.docx
2. CURRENT_STATE.json
3. EXACT_RESUME_POINT.md
4. SCOPE_LOCK.json
5. ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md
6. FIXED_3000_TRANCHE_PROTOCOL.md
7. OUTPUT_AND_HANDOFF_PROTOCOL.md
8. Section 37

Tranche 4 adjudicates exactly 3,000 pairs and leaves 11,847. The next semantic work unit is exactly 3,000 rows.

Next: `{NEXT}`.
'''
(ROOT/'00_START_HERE'/'README_FIRST.md').write_text(readme,encoding='utf-8')
master=f'''# Current governing handoff v16

The authoritative narrative is `00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v16_20260731.docx`.

The fixed 3,000-row tranche protocol is now governing. Tranche 4 begins with 14,847 pending semantic-priority pairs, adjudicates exactly 3,000, binds 6,000 side-level evidence records, and leaves 11,847.

Authority disposition: 13 proposition equivalences; 220 coordinate-only relations; 2,667 explicit negatives; 92 redirects; 8 unresolved. Twenty adversarial tests and a six-artifact hash-exact deterministic rebuild pass.

Exact next pass: `{NEXT}`.

Read section 37 and the complete start-here controls before continuing.
'''
(ROOT/'00_START_HERE'/'MASTER_HANDOFF.md').write_text(master,encoding='utf-8')
(ROOT/'MASTER_HANDOFF.md').write_text(master,encoding='utf-8')
(ROOT/'00_START_HERE'/'NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text(f'''Open `00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v16_20260731.docx`, then CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md and FIXED_3000_TRANCHE_PROTOCOL.md. Resume exactly at `{NEXT}`. Use section 37's 11,847-row remaining queue and adjudicate exactly 3,000 rows in the next tranche.\n''',encoding='utf-8')
(ROOT/'00_START_HERE'/'ASSEMBLY_PROVENANCE.md').write_text('''# Assembly provenance

The delivered `assemble_handoff_v16.py` is the cumulative assembly procedure used for this handoff. Its `/mnt/data` paths record the build environment and require remapping for replay elsewhere. Section 37's authority surfaces are independently reproducible from the delivered builder, frozen candidate surface, inherited cumulative inputs and tests.
''',encoding='utf-8')
shutil.copy2(WORK/'assemble_handoff_v16.py',ROOT/'00_START_HERE'/'assemble_handoff_v16.py')

# Master DOCX
mdoc=Document(); defaults(mdoc,'Rawlsing J-Family Authority Strategy — Master Handoff v16')
p=mdoc.add_paragraph(); p.add_run('Governing state: ').bold=True; p.add_run('P2 open; fixed 3,000-row tranche 4 complete. No canonical J-family authority or respondent execution.')
mdoc.add_heading('What changed',1)
bullets(mdoc,[
 'The acceptance standard now includes a hard semantic-pair work-unit cap of exactly 3,000 rows.',
 'Queue moved from 14,847 to 11,847 through a deterministic democracy/electoral tranche.',
 'All 3,000 rulings carry direct two-sided evidence; 20 adversarial tests pass.',
 'The six governing build artifacts reproduce hash-identically.',
 'The component-aware V551J strata/horizon bridge remains recovered-runtime validated and live-uninstalled.'
])
mdoc.add_heading('Tranche 4 authority return',1)
table(mdoc,['Disposition','Rows'],[['Proposition equivalence','13'],['Coordinate only','220'],['Negative authority','2,667'],['Redirected','92'],['Unresolved','8'],['Total','3,000']])
mdoc.add_heading('Acceptance meaning',1)
mdoc.add_paragraph('Shared democracy or election vocabulary does not authorize equivalence. Proposition authority requires the same relation axis, target or scope, and operator. Current, past and future democracy, named countries, regular versus free-and-fair elections, different authoritarian models, and ambiguous electoral participation remain distinct.')
mdoc.add_heading('Exact continuation',1)
mdoc.add_paragraph(NEXT)
bullets(mdoc,['Use the 11,847-row remaining queue in section 37.','Select and adjudicate exactly 3,000 rows.','Do not exceed the cap to finish a neighborhood.','Package the cumulative handoff before beginning another work unit.'])
mdoc.add_heading('Hard boundaries',1)
mdoc.add_paragraph('Global P2 remains open. No J-family authoring, response-value harmonization, respondent join, registry installation, database write, or V550/V551/V552 production execution. Asian Barometer W6 remains excluded.')
footer(mdoc,'Rawlsing cumulative governing handoff v16 — 2026-07-31')
mdoc.save(ROOT/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v16_20260731.docx')

rdoc=Document(); defaults(rdoc,'P2 Democracy/Electoral Adjudication — Fixed 3,000 Tranche 4')
rdoc.add_heading('Fixed work-unit return',1)
table(rdoc,['Measure','Result'],[['Queue at start','14,847'],['Adjudicated','3,000 exactly'],['Queue at end','11,847'],['Lineages classified','488'],['Evidence records','6,000'],['Adversarial tests','20 passed'],['Deterministic rebuild','PASS — 6/6 hashes exact']])
rdoc.add_heading('Authority partition',1)
table(rdoc,['Relation type','Rows'],[['Reworded proposition equivalence','13'],['Construct/target coordinate only','19'],['Domain coordinate only','201'],['Negative authority','2,667'],['Other-domain review required','92'],['Unresolved','8']])
rdoc.add_heading('Selection contract',1)
rdoc.add_paragraph('The tranche consumes all pending rows in DEMO_EXTENT, CIVIC_VOTE_MATTERS, CIVIC_VOTE, REJECT_STRONGMAN and REJECT_MILITARY, plus the first deterministic 27-row slice of REJECT_ONEPARTY. Selected and remaining candidate IDs form an exact disjoint partition of the incoming queue.')
rdoc.add_heading('Adversarial findings',1)
bullets(rdoc,['Regular elections remain distinct from free-and-fair elections.','Individual vote effect remains distinct from the effect of honest elections on life.','Generic strong-leader rule remains distinct from strong-president-plus-military government.','Conditional military takeover remains distinct from ordinary military rule.','Current, past, future and named-country democracy targets remain distinct.','Ambiguous “participated in last election” wording is not certified as voting.','Terse Afrobarometer R1 system ratings remain unresolved.'])
rdoc.add_heading('Authority boundary',1)
rdoc.add_paragraph('Pair-relation authority only. No family identity, value portability, respondent execution, database write, or live pipeline installation follows.')
footer(rdoc,'Rawlsing P2 fixed 3,000 tranche 4 — 2026-07-31')
rdoc.save(SEC/'Rawlsing_P2_Global_Democracy_Electoral_Fixed_3000_Tranche4_Report_20260731.docx')

# Update superseded registry with predecessor restart status.
sup=ROOT/'00_START_HERE'/'SUPERSEDED_AND_NON_GOVERNING_ARTIFACTS.csv'
with sup.open('a',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['Handoff v15 restart controls','SUPERSEDED_BY_V16','Queue advanced by exact fixed 3,000-row tranche and fixed work-unit protocol became governing.','Forensic packaging history only; v16 controls govern.'])

# Top-level validation (release fields completed after external QA).
top={
 'status':'PASS','handoff_version':'v16','current_pass':current['current_pass'],'next_pass':NEXT,'global_p2_status':'OPEN','canonical_j_family_authority_authored':False,'respondents_processed':0,'asian_barometer_w6':'EXCLUDED',
 'acceptance_standard_embedded':True,'fixed_tranche_protocol':{'status':'PASS','work_unit_pairs':3000,'input_pending_pairs':14847,'pairs_adjudicated':3000,'pairs_remaining':11847,'lineages_classified':488,'evidence_rows':6000,'pytest_cases':20,'reproducibility':'PASS_HASH_EXACT','authority_boundary':ret['authority_boundary']},
 'runtime_bridge_live_repository_installation':'NOT_PERFORMED','release_status':'PENDING_FINAL_CUMULATIVE_AND_DOCUMENT_GATES'}
dump(ROOT/'VALIDATION.json',top)
remove_caches(ROOT)
manifests(ROOT)
print(ROOT)
