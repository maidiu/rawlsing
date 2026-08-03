from pathlib import Path
import json, hashlib, datetime, shutil
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
S41=ROOT/'41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8'
S42=ROOT/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE'
START=ROOT/'00_START_HERE'
closure=json.loads((S42/'GLOBAL_P2_CLOSURE_RETURN.json').read_text())
final_ret=json.loads((S41/'FINAL_2847_TRANCHE_RETURN.json').read_text())
rul=pd.read_csv(S41/'Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).isoformat(timespec='seconds')

BLUE='17365D'; LIGHT='D9EAF7'; PALE='EEF4F8'; DARK='1F1F1F'; GREEN='E2F0D9'; ORANGE='FCE4D6'

def shade(cell,fill):
 tcPr=cell._tc.get_or_add_tcPr(); shd=tcPr.find(qn('w:shd'))
 if shd is None: shd=OxmlElement('w:shd'); tcPr.append(shd)
 shd.set(qn('w:fill'),fill)

def margins(doc):
 for sec in doc.sections:
  sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.72); sec.right_margin=Inches(.72)

def style_doc(doc):
 margins(doc)
 styles=doc.styles
 styles['Normal'].font.name='Arial'; styles['Normal'].font.size=Pt(9.5)
 styles['Title'].font.name='Arial'; styles['Title'].font.size=Pt(24); styles['Title'].font.bold=True; styles['Title'].font.color.rgb=RGBColor.from_string(BLUE)
 for name,size in [('Heading 1',16),('Heading 2',12),('Heading 3',10.5)]:
  st=styles[name]; st.font.name='Arial'; st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor.from_string(BLUE)
  st.paragraph_format.space_before=Pt(8); st.paragraph_format.space_after=Pt(3)

def set_cell_text(cell,text,bold=False,color=None,size=8.5):
 cell.text=''
 p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0)
 r=p.add_run(str(text)); r.bold=bold; r.font.name='Arial'; r.font.size=Pt(size)
 if color: r.font.color.rgb=RGBColor.from_string(color)
 cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER


def mark_header(row):
 trPr=row._tr.get_or_add_trPr(); e=trPr.find(qn('w:tblHeader'))
 if e is None:
  e=OxmlElement('w:tblHeader'); e.set(qn('w:val'),'true'); trPr.append(e)

def prevent_row_split(row):
 trPr=row._tr.get_or_add_trPr(); e=trPr.find(qn('w:cantSplit'))
 if e is None:
  e=OxmlElement('w:cantSplit'); trPr.append(e)

def table(doc,headers,rows,widths=None):
 t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'
 for i,h in enumerate(headers):
  set_cell_text(t.rows[0].cells[i],h,True,'FFFFFF',8); shade(t.rows[0].cells[i],BLUE)
 mark_header(t.rows[0]); prevent_row_split(t.rows[0])
 for ri,row in enumerate(rows):
  newrow=t.add_row(); prevent_row_split(newrow); cells=newrow.cells
  for i,v in enumerate(row):
   set_cell_text(cells[i],v,False,None,8)
   if ri%2: shade(cells[i],PALE)
 if widths:
  for row in t.rows:
   for i,w in enumerate(widths): row.cells[i].width=Inches(w)
 return t

def p(doc,text='',bold=False,italic=False):
 para=doc.add_paragraph(); para.paragraph_format.space_after=Pt(3)
 run=para.add_run(text); run.bold=bold; run.italic=italic; run.font.name='Arial'; run.font.size=Pt(9.5)
 return para

def bullets(doc,items):
 for x in items:
  para=doc.add_paragraph(style='List Bullet'); para.paragraph_format.space_after=Pt(1.5); para.paragraph_format.left_indent=Inches(.22)
  r=para.add_run(x); r.font.name='Arial'; r.font.size=Pt(9.2)

def title(doc,title,subtitle):
 q=doc.add_paragraph(); q.alignment=WD_ALIGN_PARAGRAPH.CENTER
 r=q.add_run(title); r.bold=True; r.font.name='Arial'; r.font.size=Pt(23); r.font.color.rgb=RGBColor.from_string(BLUE)
 q2=doc.add_paragraph(); q2.alignment=WD_ALIGN_PARAGRAPH.CENTER
 r=q2.add_run(subtitle); r.font.name='Arial'; r.font.size=Pt(10); r.font.color.rgb=RGBColor.from_string('555555')

def banner(doc,text,fill=GREEN):
 t=doc.add_table(rows=1,cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'; shade(t.cell(0,0),fill); set_cell_text(t.cell(0,0),text,True,BLUE,10); mark_header(t.rows[0]); prevent_row_split(t.rows[0])

def footer(doc,label):
 for sec in doc.sections:
  f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER
  r=f.add_run(label); r.font.name='Arial'; r.font.size=Pt(7.5); r.font.color.rgb=RGBColor.from_string('666666')

# Final tranche markdown
counts=rul.relation_type.value_counts().to_dict()
accept=rul[rul.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE']
ceil=accept.portability_ceiling.value_counts().to_dict()
md41=f'''# P2 Global Final 2,847-Pair Tranche 8

## Result

- Incoming queue: 2,847
- Adjudicated: 2,847
- Remaining queue: 0
- Lineages classified: {final_ret['lineages_classified']}
- Two-sided evidence records: {final_ret['evidence_rows']}
- Proposition relations: {counts.get('REWORDED_PROPOSITION_EQUIVALENCE',0)}
- Coordinate relations: {counts.get('DOMAIN_COORDINATE_ONLY',0)+counts.get('CONSTRUCT_TARGET_COORDINATE_ONLY',0)}
- Negative authority: {counts.get('NEGATIVE_AUTHORITY',0)}
- Redirected: {counts.get('OTHER_DOMAIN_REVIEW_REQUIRED',0)}
- Unresolved: {counts.get('UNRESOLVED',0)}

## Acceptance corrections

The initial proposition-positive surface was reduced after exact two-sided review. Corrections blocked specific prayer from collapsing into generic prayer, parents’ attendance from collapsing into respondent attendance, past petition signing from collapsing into willingness scales, unrelated social-media purpose/causality/use items from collapsing, child-value ranking from collapsing into mention/importance, democratic from non-democratic system support, contextualized happiness from unprompted happiness, binary neighbor exclusion from like/dislike ratings, and foreign-workers-only targets from combined immigrant/foreign-worker targets.

Final proposition authority is split by portability ceiling: {ceil.get('QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY',0)} question-plus-response-topology relations and {ceil.get('QUESTION_PROPOSITION_ONLY',0)} question-only relations.

The {counts.get('UNRESOLVED',0)} unresolved pairs are closed fail-closed authority rows. They all touch source-local child prompts whose target is absent; they are not pending queue rows and export no positive authority.
'''
(S41/'P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8_REPORT.md').write_text(md41)

# Closure markdown
c=closure['semantic_priority_authority_class_counts']; e=closure['exact_foundation_authority_class_counts']
md42=f'''# Global P2 Cross-Tranche Closure

Global P2 is closed as relation, negative, unresolved, structure, and semantic-reference authority.

## Closure surface

- 18,276 exact implementations
- 13,526 source-local continuity lineages
- 18,831 / 18,831 semantic-priority pairs adjudicated
- 0 semantic-priority pairs pending
- 641 proposition-relation authorities
- 1,024 coordinate or bounded-relation authorities
- 14,857 explicit negative authorities
- 1,958 redirected other-domain authorities
- 351 formally unresolved fail-closed authorities
- all 36 unordered source pairs represented

## Exact foundation

- 751 exact-foundation pairs
- 270 accepted
- 78 rejected
- 403 formally unresolved

## Structure and reference authority

- 19 structure analogies adjudicated: 13 full, 5 partial, 1 rejected
- 119 member-level rulings: 80 accepted correspondences, 39 source-local boundary/extension rows
- 30 semantic-reference overlays: 29 corrected/new coordinates and 1 source-local coordinate with unresolved parent

## Boundary

Closure does not create canonical J-family membership, value portability, respondent joins, or a database/registry installation. The component-aware strata/horizon bridge remains uninstalled because no user-designated current live repository or git worktree exists in the active runtime. Historical snapshots are evidence, not installation targets.

## Next phase

P3_TYPED_COLLISION_HYPEREDGE_CANDIDATE_FAMILY_RANKING_AND_CANONICAL_V550J_ADJUDICATION
'''
(S42/'P2_GLOBAL_CROSS_TRANCHE_CLOSURE_REPORT.md').write_text(md42)

# Final tranche DOCX
doc=Document(); style_doc(doc); footer(doc,'Rawlsing P2 final semantic tranche • v20 • 2026-07-31')
title(doc,'Rawlsing P2: Final 2,847-Pair Tranche','Tranche 8 • semantic-priority queue closure • 31 July 2026')
banner(doc,'QUEUE CLOSED: 2,847 → 0')
doc.add_heading('Authority return',level=1)
table(doc,['Authority result','Pairs'],[
 ['Question proposition equivalence',counts.get('REWORDED_PROPOSITION_EQUIVALENCE',0)],
 ['Domain-coordinate only',counts.get('DOMAIN_COORDINATE_ONLY',0)],
 ['Construct-target coordinate only',counts.get('CONSTRUCT_TARGET_COORDINATE_ONLY',0)],
 ['Explicit negative authority',counts.get('NEGATIVE_AUTHORITY',0)],
 ['Redirected to proper domain',counts.get('OTHER_DOMAIN_REVIEW_REQUIRED',0)],
 ['Unresolved, fail-closed',counts.get('UNRESOLVED',0)],
 ['Total',len(rul)]],widths=[4.8,1.1])
p(doc,f"The tranche classified {final_ret['lineages_classified']} source-local lineages and produced {final_ret['evidence_rows']} explicit side-level evidence records. The selected IDs equal the entire incoming queue exactly; no pair was omitted or added.")
doc.add_heading('Embedded acceptance review',level=1)
bullets(doc,[
 'Specific Fajr and istikharah practices were separated from generic prayer frequency.',
 'Respondent religious-service attendance was separated from mother and father attendance.',
 'Past petition signing was separated from mixed past/might/would-never disposition scales.',
 'Social-media use, purpose, causal attribution, frequency, and trust were separated.',
 'Child-quality desirability ranking was separated from importance or mention batteries.',
 'Support for democratic systems was separated from support for non-democratic systems.',
 'Binary neighbor exclusion was separated from like/dislike closeness ratings and narrower foreign-worker targets from combined immigrant/foreign-worker targets.',
 'Contextualized happiness following an environment prompt was kept below full proposition identity.'
])
p(doc,f"Final proposition authorities: {len(accept)}. Of these, {ceil.get('QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY',0)} carry question-plus-response-topology portability and {ceil.get('QUESTION_PROPOSITION_ONLY',0)} carry question-only portability.")
doc.add_heading('Unresolved boundary',level=1)
p(doc,f"All {counts.get('UNRESOLVED',0)} unresolved rows touch source-local child prompts whose specific target is absent. They are closed as fail-closed authority, carry NO_AUTHORITY ceilings, and do not remain in the pending queue.")
doc.add_heading('Verification',level=1)
bullets(doc,['7 tranche-specific adversarial tests passed.','Seven governing artifacts reproduced with identical hashes across a deterministic rebuild.','No J-family authority, value harmonization, respondent join, registry write, or production execution occurred.'])
doc.save(S41/'Rawlsing_P2_Global_Final_2847_Tranche8_Report_20260731.docx')

# Closure DOCX
doc=Document(); style_doc(doc); footer(doc,'Rawlsing global P2 closure • v20 • 2026-07-31')
title(doc,'Rawlsing Global P2 Closure','Cross-tranche authority reconciliation • 31 July 2026')
banner(doc,'GLOBAL P2 CLOSED',GREEN)
doc.add_heading('Complete authority surface',level=1)
table(doc,['Surface','Closed result'],[
 ['Exact implementations','18,276'],['Source-local lineages','13,526'],['Semantic-priority pairs','18,831 adjudicated / 0 pending'],['Source-pair coverage','36 / 36 unordered pairs'],['Exact-foundation pairs','751 classified'],['Structure analogies','19 adjudicated'],['Structure-member rulings','119'],['Semantic-reference overlays','30 resolved']],widths=[3.2,2.7])
doc.add_heading('Semantic-priority partition',level=1)
table(doc,['Authority class','Rows'],[
 ['Proposition relation',c['PROPOSITION_RELATION_AUTHORITY']],['Coordinate or bounded relation',c['COORDINATE_OR_BOUNDED_RELATION_AUTHORITY']],['Explicit negative',c['NEGATIVE_AUTHORITY']],['Redirected other domain',c['REDIRECTED_OTHER_DOMAIN_AUTHORITY']],['Unresolved, fail-closed',c['UNRESOLVED_FAIL_CLOSED_AUTHORITY']],['Total','18,831']],widths=[4.2,1.2])
doc.add_heading('Exact foundation and structures',level=1)
p(doc,'Exact foundation: 270 accepted, 78 rejected, and 403 formally unresolved. Structure authority: 13 full analogies, 5 partial analogies with source-specific extensions, and 1 rejected shared-label analogy. Member authority: 80 accepted correspondences and 39 source-local boundary rows.')
doc.add_heading('Meaning of closure',level=1)
bullets(doc,[
 'Every semantic-priority candidate now has proposition, coordinate, negative, redirect, or unresolved authority.',
 'Unresolved rows are governed fail-closed outcomes; they are not omitted or waiting in a queue.',
 'No canonical J-family membership, value harmonization, respondent linkage, or registry installation follows automatically.',
 'The component-aware strata/horizon bridge remains uninstalled because no user-designated current live repository exists in the active runtime.'
])
doc.add_heading('Next phase',level=1)
p(doc,'P3 — typed collision/hyperedge construction, candidate-family ranking, and canonical V550J adjudication',bold=True)
p(doc,'Begin by constructing typed positive, negative, nested-target, broader/narrower, and unresolved collision edges and hyperedges from the closed P2 authority surface. Rank candidate families, then adjudicate canonical V550J membership across all nine sources, including GSS. Preserve the P2 portability ceilings and unresolved boundaries.')
doc.save(S42/'Rawlsing_P2_Global_Cross_Tranche_Closure_Report_20260731.docx')

# Master restart DOCX
doc=Document(); style_doc(doc); footer(doc,'Rawlsing J-family authority strategy • master handoff v20 • 2026-07-31')
title(doc,'Rawlsing J-Family Authority Strategy','Master handoff v20 • Global P2 closed • 31 July 2026')
banner(doc,'START HERE: P2 IS CLOSED; RESUME AT P3')
doc.add_heading('Exact current state',level=1)
p(doc,'All nine source-local terrains are closed and reconcile exactly to the 18,276-node Phase 0 universe. Global P2 cross-source reconciliation is now closed across exact proposition authority, reworded and translated relation authority, negative and unresolved authority, member-level structure analogies, semantic-reference repairs, and the complete 18,831-row semantic-priority queue.')
table(doc,['Governing surface','Current state'],[
 ['Implementations / lineages','18,276 / 13,526'],['Semantic-priority queue','18,831 adjudicated / 0 pending'],['Semantic authority','641 proposition; 1,024 coordinate; 14,857 negative; 1,958 redirected; 351 unresolved'],['Exact foundation','270 accepted; 78 rejected; 403 unresolved'],['Structures','19 analogies; 119 member rulings'],['Semantic repairs','30 overlays'],['Canonical J families','Not yet authored'],['Live bridge','Validated on recovered evidence; not installed in a current live repository']],widths=[2.6,4.1])
doc.add_heading('Authority boundary',level=1)
bullets(doc,[
 'P2 closure authorizes relation-level comparison only at each row’s recorded portability ceiling.',
 'Negative and unresolved rows are first-class authority. They may not be converted into family membership by similarity scoring.',
 'No response-value portability, respondent joins, database writes, registry installation, or V550/V551/V552 production execution has occurred.',
 'Asian Barometer W6 remains excluded. GSS remains inside the coming canonical adjudication rather than functioning as an unquestioned template.'
])
doc.add_heading('Exact continuation',level=1)
p(doc,'P3 — typed collision/hyperedge construction, candidate-family ranking, and canonical V550J adjudication',bold=True)
bullets(doc,[
 'Build typed pair edges and multi-source hyperedges from the closed P2 proposition, coordinate, nested-target, negative, and unresolved authority surfaces.',
 'Rank candidate J families without flattening broader/narrower, relation-axis, target, operator, timeframe, or source-specific boundary differences.',
 'Adjudicate canonical V550J memberships across all nine sources, including GSS, with two-sided evidence and explicit exclusions.',
 'Carry the component-aware strata/horizon bridge into the user-designated current live repository only when that repository is supplied; rerun fail-closed integration tests before production execution.'
])
doc.add_page_break()
doc.add_heading('What to read first',level=1)
table(doc,['Order','File or section','Purpose'],[
 ['1','00_START_HERE/CURRENT_STATE.json','Machine-readable governing state'],['2','42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE/','Closure registry, validation, report, and runtime boundary'],['3','41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8/','Final queue tranche and evidence'],['4','32–40','Full global P2 construction and every prior task return'],['5','24–31 and earlier','All nine source-local authority terrains and independent integrity audit']],widths=[.45,3.6,2.8])
doc.add_heading('Verification and reproducibility',level=1)
p(doc,'The v20 release must be accepted only after the cumulative verifier passes against the assembled tree and again against a fresh extraction of the final outer ZIP; all delivered files must match byte-for-byte, recursive archives must remain intact, generated test caches must be absent, and all governing DOCX files must pass rendered visual and accessibility review.')
doc.add_heading('Milestone map',level=1)
table(doc,['Sections','Milestone'],[
 ['00–31','Source recovery, all-nine source-local authority, and independent package audit'],
 ['32','Unified node/lineage registry, exact foundation, semantic queue, structure queue'],
 ['33–35','Relation-axis adjudication, evidence correction, and component-aware bridge'],
 ['36','Trust neighborhoods: 3,863 pairs'],
 ['37','Democracy/electoral fixed tranche: 3,000 pairs'],
 ['38','Media/civic fixed tranche: 3,000 pairs'],
 ['39','Material-economy fixed tranche: 3,000 pairs'],
 ['40','Social-order fixed tranche: 3,000 pairs'],
 ['41','Final fixed tranche: 2,847 pairs; queue closed'],
 ['42','Cross-tranche global P2 closure and exact next-phase boundary']],widths=[1.25,5.5])
doc.add_heading('Permanent handoff protocol',level=1)
p(doc,'Every response containing new Rawlsing work must place the fully updated cumulative handoff link first. The handoff must contain the complete prior project state, every task return, and the new work so another agent can resume without re-education.')
doc.save(START/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v20_20260731.docx')

# Machine-readable controls
current={
 'handoff_version':'v20','date':'2026-07-31','global_p2_closed':True,
 'phase0_implementations':18276,'source_local_lineages':13526,
 'semantic_priority_queue_total':18831,'semantic_priority_pairs_adjudicated_cumulative':18831,'semantic_priority_pairs_remaining':0,
 'semantic_priority_authority_class_counts':closure['semantic_priority_authority_class_counts'],
 'exact_foundation_pairs':751,'exact_foundation_authority_class_counts':closure['exact_foundation_authority_class_counts'],
 'structure_analogy_rulings':19,'structure_member_rulings':119,'semantic_reference_overlays':30,
 'canonical_j_family_authority_authored':False,'live_component_bridge_installed':False,
 'live_bridge_blocker':closure['live_component_bridge_blocker'],'asian_barometer_w6_excluded':True,
 'next_pass':closure['next_pass'],'authority_boundary':closure['authority_boundary'],
 'governing_sections':['41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8','42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE']}
(START/'CURRENT_STATE.json').write_text(json.dumps(current,indent=2,sort_keys=True)+'\n')

scope={
 'scope_lock_version':'v20','global_p2_closed':True,
 'allowed_next_work':['typed collision edges','typed hyperedges','candidate-family ranking','canonical V550J family adjudication across all nine sources','live component bridge installation only in user-designated current repository'],
 'prohibited_until_canonical_authority_closes':['respondent joins','raw-value harmonization','database writes','registry installation','V550/V551/V552 production execution'],
 'nonnegotiable_controls':['preserve negative and unresolved authority','respect portability ceilings','two-sided evidence for membership and exclusion','Asian Barometer W6 excluded','GSS is a source, not a universal template'],
 'next_pass':closure['next_pass']}
(START/'SCOPE_LOCK.json').write_text(json.dumps(scope,indent=2,sort_keys=True)+'\n')

nexttxt='''Open 00_START_HERE/CURRENT_STATE.json, SCOPE_LOCK.json, and the v20 master handoff. Global P2 is closed: 18,831/18,831 semantic-priority pairs are governed, the exact foundation and structures are closed, and no canonical J-family authority has yet been authored. Resume at P3_TYPED_COLLISION_HYPEREDGE_CANDIDATE_FAMILY_RANKING_AND_CANONICAL_V550J_ADJUDICATION. Preserve all P2 portability ceilings, negative authority, unresolved boundaries, source-specific extensions, and Asian Barometer W6 exclusion. Do not join respondents, harmonize values, write registries/databases, or execute production V550/V551/V552 until canonical authority closes. Install the component-aware strata/horizon bridge only in a user-designated current live repository and rerun fail-closed integration tests.\n'''
(START/'NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text(nexttxt)

readme=f'''# Rawlsing J-Family Authority Strategy Handoff v20

**Global P2 is closed. Resume at P3 typed collision/hyperedge construction, candidate-family ranking, and canonical V550J adjudication.**

## Governing state

- 18,276 exact implementations
- 13,526 source-local lineages
- 18,831 / 18,831 semantic-priority pairs adjudicated
- 0 pending semantic-priority pairs
- 751 exact-foundation pairs governed
- 19 structure analogies and 119 member-level rulings governed
- 30 semantic-reference overlays governed
- Canonical J-family authority: not yet authored
- Live component bridge: validated against recovered evidence, not installed in a current live repository

Read `CURRENT_STATE.json`, `SCOPE_LOCK.json`, the v20 master DOCX, then section 42.
'''
(START/'README_FIRST.md').write_text(readme)
(ROOT/'README_FIRST.md').write_text(readme)
(ROOT/'MASTER_HANDOFF.md').write_text(md42+'\n\n'+nexttxt)
print(json.dumps({'documents_created':3,'controls_updated':7,'timestamp':now},indent=2))
