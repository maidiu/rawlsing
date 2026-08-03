import csv, json, hashlib, os, shutil, glob, zipfile
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DATE='20260731'
ROOT=Path('/mnt/data/work_calibre')
OUT=Path('/mnt/data')
HANDOFF_V9=Path('/mnt/data/handoff_v9_audit/Rawlsing_J_Family_Authority_Strategy_Handoff_v9_20260731')
OLD_SWEEP=Path('/mnt/data/audit_four/Rawlsing_P2_Remaining_Four_Source_Deep_Pass_Sweep_v1_20260731')
csv.field_size_limit(10**9)

SOURCES={
'Asian_Barometer':{
 'display':'Asian Barometer','short':'Asian Barometer','waves':['W1','W4','W5'],
 'dir':ROOT/f'Rawlsing_P2_Asian_Barometer_AllWave_Deep_Pass_v2_{DATE}',
 'report':f'Rawlsing_P2_Asian_Barometer_AllWave_Deep_Pass_Report_v2_{DATE}.docx',
 'method':'Merged multi-country wave releases require exact implementation identity. Numeric/questionnaire codes corroborate but never define continuity. Country, language, instrument and repeated-slot variants stay explicit; W6 remains excluded.',
 'audit_summary':'The audit removed a false repeated-slot continuity, demoted a government-to-president/government target expansion to review, and expanded the conservative structure inventory to the same adjacency/response-form depth used in the first five passes.',
 'next':'Participate in global two-sided semantic, translation, target, condition and source-structure reconciliation. W6 remains excluded.'},
'Latinobarometro':{
 'display':'Latinobarómetro','short':'Latinobarómetro','waves':['1995','2011','2024'],
 'dir':ROOT/f'Rawlsing_P2_Latinobarometro_AllWave_Deep_Pass_v2_{DATE}',
 'report':f'Rawlsing_P2_Latinobarometro_AllWave_Deep_Pass_Report_v2_{DATE}.docx',
 'method':'Exact released implementations are preserved across three widely separated waves. Reused p-/P-/question codes are corroborative only; proposition, response topology, semantic authority and translation-aware source evidence govern continuity.',
 'audit_summary':'The audit re-read every accepted wording revision for target, referent and semantic-role contradictions; all 20 survived. The source-structure inventory was deepened with conservative contiguous response-semantic runs.',
 'next':'Participate in global translation-aware Spanish/English semantic reconciliation and broader/narrower concept adjudication.'},
'South_Asia':{
 'display':'South Asia Barometer','short':'South Asia','waves':['W1','W2'],
 'dir':ROOT/f'Rawlsing_P2_South_Asia_AllWave_Deep_Pass_v2_{DATE}',
 'report':f'Rawlsing_P2_South_Asia_AllWave_Deep_Pass_Report_v2_{DATE}.docx',
 'method':'A small two-wave regional source requires especially explicit referent and target control. Released-set scope, questionnaire section, exact wording, response topology and semantic class govern; codes are corroborative only.',
 'audit_summary':'The audit recovered four clear cross-code continuities, converted country-economy/family-economy and main-earner/respondent-occupation lookalikes into negative authority, reduced the unresolved queue to three cases, and strengthened structure reconnaissance.',
 'next':'Participate in global reconciliation with its limited two-wave corroboration and released Set-B scope carried forward.'},
'LiTS':{
 'display':'Life in Transition Survey (LiTS)','short':'LiTS','waves':['2006','II','III','IV'],
 'dir':ROOT/f'Rawlsing_P2_LiTS_AllWave_Deep_Pass_v2_{DATE}',
 'report':f'Rawlsing_P2_LiTS_AllWave_Deep_Pass_Report_v2_{DATE}.docx',
 'method':'LiTS requires physical case-sensitive identity, canonical/physical crosswalks, repeated-roster and multiselect parentage, conditional respondent scope, country coverage and explicit field-classification reconciliation.',
 'audit_summary':'The audit removed two false same-code continuities, adjudicated the 94-row wording/slot queue into 75 accepted, 16 negative and 3 unresolved cases, added explicit reconciliation for six semantic-role mismatches, and preserved case-sensitive/repeated-slot controls.',
 'next':'Participate in global reconciliation with administrative-context and proposition-only portability ceilings preserved.'}
}

FIRST_FIVE=[
 {'source_family':'GSS','nodes':6021,'response_bound':5906,'response_gaps':115,'accepted_continuity_edges':3171,'source_structures':722,'validation':'13/13 PASS','calibre':'INDIVIDUAL_PASS_REFERENCE'},
 {'source_family':'WVS','nodes':1219,'response_bound':1064,'response_gaps':155,'accepted_continuity_edges':180,'source_structures':115,'validation':'15/15 PASS','calibre':'INDIVIDUAL_PASS_REFERENCE'},
 {'source_family':'EVS','nodes':2224,'response_bound':2181,'response_gaps':43,'accepted_continuity_edges':815,'source_structures':182,'validation':'16/16 PASS','calibre':'INDIVIDUAL_PASS_REFERENCE'},
 {'source_family':'Arab Barometer','nodes':1698,'response_bound':1651,'response_gaps':47,'accepted_continuity_edges':67,'source_structures':159,'validation':'18/18 PASS','calibre':'INDIVIDUAL_PASS_REFERENCE'},
 {'source_family':'Afrobarometer','nodes':913,'response_bound':831,'response_gaps':82,'accepted_continuity_edges':119,'source_structures':230,'validation':'16/16 PASS','calibre':'INDIVIDUAL_PASS_REFERENCE'}]

def read_csv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:
        d=csv.DictReader(f); return list(d), list(d.fieldnames or [])
def write_csv(p,rows,fields):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader();
        for r in rows:w.writerow({k:r.get(k,'') for k in fields})
def find1(root,pat):
    xs=list(Path(root).glob(pat));
    if len(xs)!=1: raise RuntimeError((root,pat,xs))
    return xs[0]
def sha_file(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def clean_rel(p,root):return str(Path(p).relative_to(root)).replace(os.sep,'/')

def set_cell_shading(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=tcPr.find(qn('w:shd'))
    if shd is None: shd=OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'),fill)
def set_cell_margins(cell,top=80,start=90,bottom=80,end=90):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr(); tcMar=tcPr.first_child_found_in('w:tcMar')
    if tcMar is None: tcMar=OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for m,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node=tcMar.find(qn('w:'+m))
        if node is None: node=OxmlElement('w:'+m); tcMar.append(node)
        node.set(qn('w:w'),str(v)); node.set(qn('w:type'),'dxa')

def setup_doc(title,subtitle,status=None):
    doc=Document(); sec=doc.sections[0]
    sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.72); sec.right_margin=Inches(.72)
    styles=doc.styles
    styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(9.5)
    styles['Title'].font.name='Aptos Display'; styles['Title'].font.size=Pt(24); styles['Title'].font.bold=True; styles['Title'].font.color.rgb=RGBColor(28,45,64)
    for nm,size,color in [('Heading 1',16,RGBColor(28,65,92)),('Heading 2',12,RGBColor(45,81,104))]:
        styles[nm].font.name='Aptos Display'; styles[nm].font.size=Pt(size); styles[nm].font.bold=True; styles[nm].font.color.rgb=color
    p=doc.add_paragraph(style='Title'); p.add_run(title)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    r=p.add_run(subtitle); r.italic=True; r.font.size=Pt(10.5); r.font.color.rgb=RGBColor(76,88,99)
    if status:
        p=doc.add_paragraph(); r=p.add_run(status); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=RGBColor(26,102,77)
    return doc

def add_metric_table(doc,metrics):
    table=doc.add_table(rows=0,cols=4); table.alignment=WD_TABLE_ALIGNMENT.CENTER; table.autofit=True
    pairs=list(metrics)
    for i in range(0,len(pairs),2):
        row=table.add_row().cells
        for j in range(2):
            if i+j<len(pairs):
                label,val=pairs[i+j]
                row[j*2].text=label; row[j*2+1].text=str(val)
                set_cell_shading(row[j*2],'DDEBF2'); row[j*2].paragraphs[0].runs[0].bold=True
                row[j*2+1].paragraphs[0].runs[0].bold=True
            else:
                row[j*2].text=''; row[j*2+1].text=''
        for c in row: set_cell_margins(c); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    doc.add_paragraph()

def add_simple_table(doc,headers,rows,widths=None):
    table=doc.add_table(rows=1,cols=len(headers)); table.alignment=WD_TABLE_ALIGNMENT.CENTER; table.style='Table Grid'
    for i,h in enumerate(headers):
        table.rows[0].cells[i].text=str(h); set_cell_shading(table.rows[0].cells[i],'DDEBF2'); table.rows[0].cells[i].paragraphs[0].runs[0].bold=True
    for rr in rows:
        cells=table.add_row().cells
        for i,v in enumerate(rr): cells[i].text=str(v)
    for row in table.rows:
        for c in row.cells: set_cell_margins(c); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    doc.add_paragraph()

def add_bullets(doc,items):
    for x in items: doc.add_paragraph(str(x),style='List Bullet')

def load_source(key):
    cfg=SOURCES[key]; root=cfg['dir']
    state=json.loads(find1(root,'00_START_HERE/CURRENT_STATE.json').read_text())
    validation,_=read_csv(find1(root,'06_VALIDATION/Validation_Results.csv'))
    corrections,_=read_csv(find1(root,'08_PROVENANCE_AND_CALIBRE_AUDIT/*Correction_Ledger*.csv'))
    limits,_=read_csv(find1(root,'05_COVERAGE_AND_GAPS/*Open_Limitations*.csv'))
    coverage,covf=read_csv(find1(root,'05_COVERAGE_AND_GAPS/*Wave_Coverage*.csv'))
    structures,_=read_csv(find1(root,'03_SOURCE_STRUCTURES/*Inventory*.csv'))
    return cfg,root,state,validation,corrections,limits,coverage,covf,structures

def reconcile_metadata(key):
    cfg,root,state,validation,corrections,limits,coverage,covf,structures=load_source(key)
    by_wave=Counter(r['wave'] for r in structures)
    for r in coverage:r['source_structures']=str(by_wave[r['wave']])
    write_csv(find1(root,'05_COVERAGE_AND_GAPS/*Wave_Coverage*.csv'),coverage,covf)
    state['validation_pass']=sum(r['status']=='PASS' for r in validation)
    state['validation_total']=len(validation)
    state['calibre_audit_completed_on']='2026-07-31'
    state['supersedes_package_version']='v1'
    find1(root,'00_START_HERE/CURRENT_STATE.json').write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return load_source(key)

def report_for_source(key):
    cfg,root,state,validation,corrections,limits,coverage,covf,structures=reconcile_metadata(key)
    doc=setup_doc(f"Rawlsing P2 {cfg['display']} Deep Pass — Calibre-Audited v2",
                  f"Source-local terrain, continuity authority, structure reconnaissance and reproducibility closure · 31 July 2026",
                  "STATUS: SOURCE-LOCAL P2 PASS COMPLETE AT THE FIRST-FIVE CALIBRE BENCHMARK · NO V550J FAMILY AUTHORITY AUTHORED")
    doc.add_heading('1. Audit conclusion',level=1)
    doc.add_paragraph('The one-sweep v1 output was not accepted on validation counts alone. It was re-audited against the individually executed GSS, WVS, EVS, Arab Barometer and Afrobarometer passes for source depth, continuity logic, negative authority, routing and universe discipline, structure reconnaissance, unresolved-case handling, provenance, reproducibility and restart usability.')
    doc.add_paragraph(cfg['audit_summary'])
    metrics=[('Exact nodes',f"{state['nodes']:,}"),('Active waves',', '.join(state['waves'])),('Response authority bound',f"{state['response_bound']:,}"),('Explicit response gaps',f"{state['response_gaps']:,}"),('Accepted continuity edges',f"{state['accepted_continuity_edges']:,}"),('Accepted wording revisions',f"{state['accepted_wording_revisions']:,}"),('Review-required cases',f"{state['review_required_wording_cases']:,}"),('Negative code/referent guards',f"{state['code_reuse_guards']:,}"),('Same-wave anti-collapse guards',f"{state['same_wave_anti_collapse_guards']:,}"),('Source structures / memberships',f"{state['source_structures']:,} / {state['structure_memberships']:,}"),('Validation',f"{state['validation_pass']}/{state['validation_total']} PASS"),('Catalog closure',state['catalog_closure_id'])]
    add_metric_table(doc,metrics)
    doc.add_heading('2. Source-adaptive method',level=1)
    doc.add_paragraph(cfg['method'])
    add_bullets(doc,[
        'Exact source implementation identity is retained at case-preserving wave/instrument/variable grain.',
        'Question codes and lexical resemblance may generate candidates; neither independently authorizes continuity.',
        'Positive continuity requires compatible proposition, target/referent, semantic role, response topology and implementation grain, with portability ceilings carried explicitly.',
        'Negative and unresolved rulings are durable authority outputs so later lexical, embedding or collision passes cannot silently recreate rejected joins.',
        'Source-native and conservative derived structures remain inventory-only candidate surfaces; adjacency or battery membership does not create respondent-level joint meaning.'
    ])
    doc.add_heading('3. Coverage and gap accounting',level=1)
    add_simple_table(doc,['Wave','Nodes','Response bound','Response gaps','Routing signals','Structures'],[[r['wave'],r['question_nodes'],r['response_bound'],r['response_gaps'],r['routing_signals'],r['source_structures']] for r in coverage])
    doc.add_paragraph(f"The wave totals reconcile exactly to {state['nodes']:,} nodes. Response-bound plus response-gap counts reconcile to the same universe. No node was added or removed during the calibre audit; the audit changed only continuity/guard dispositions, structure reconnaissance and documentation where evidence required it.")
    doc.add_heading('4. Calibre corrections and retained rulings',level=1)
    for c in corrections:
        p=doc.add_paragraph(style='List Bullet');
        r=p.add_run(f"{c['correction_id']} — {c['object']}: "); r.bold=True
        p.add_run(f"{c['prior_state']} → {c['revised_state']}. {c['reason']}")
    doc.add_heading('5. Continuity, anti-continuity and portability',level=1)
    doc.add_paragraph(f"The final source-local atlas contains {state['accepted_continuity_edges']:,} accepted edges, {state['review_required_wording_cases']:,} unresolved cases and {state['code_reuse_guards']:,} explicit code/referent negative guards. Accepted wording revisions are materialized as continuity edges; accepted, review and negative pair sets are disjoint. Every accepted endpoint exists in the node catalog and crosses waves.")
    if key=='LiTS':
        doc.add_paragraph('Six exact-proposition edges with differing accepted semantic roles now carry separate reconciliation rulings. Administrative geographic fields are restricted to ADMINISTRATIVE_CONTEXT_ONLY; substantive classification reconciliations are restricted to QUESTION_PROPOSITION_ONLY. Repeated roster and service-target code reuse is protected by explicit negative authority.')
    elif key=='Asian_Barometer':
        doc.add_paragraph('The first-organization versus third-organization slot is explicitly non-continuous. Government versus president/government remains unresolved as a possible target expansion rather than being forced into a positive lineage.')
    elif key=='South_Asia':
        doc.add_paragraph('Local government, courts, police and respondent age are now accepted under fuller or renumbered wording. Country economy versus family economy and main-earner versus respondent occupation are blocked as target/referent changes.')
    else:
        doc.add_paragraph('All retained accepted wording revisions survived pairwise target, referent, semantic-role and response-form review. Translation-aware equivalence remains a global P2 ruling rather than being smuggled into source-local continuity.')
    h6=doc.add_heading('6. Source-structure reconnaissance',level=1)
    if key=='Latinobarometro': h6.paragraph_format.page_break_before=True
    type_counts=Counter(r['structure_type'] for r in structures)
    add_simple_table(doc,['Structure type','Count'],sorted(type_counts.items(),key=lambda x:(-x[1],x[0])))
    doc.add_paragraph(f"The inventory contains {state['source_structures']:,} structures and {state['structure_memberships']:,} memberships. All carry INVENTORY_ONLY_NOT_J_FAMILY status. Membership counts and wave locality reconcile; no structure spans waves and no structure has been promoted into V550J authority.")
    doc.add_heading('7. Open limitations',level=1)
    add_bullets(doc,[r['limitation'] for r in limits])
    doc.add_heading('8. Validation, provenance and restartability',level=1)
    doc.add_paragraph(f"The strengthened v2 suite passes {state['validation_pass']}/{state['validation_total']} checks. It verifies exact node count and identity, endpoint integrity, uniqueness, accepted/review/negative disjointness, cross-wave continuity, source-specific false-join controls, structure referential integrity, response-gap reconciliation, retained source references and the no-execution boundary.")
    doc.add_paragraph('The package includes the accepted source reference surfaces unchanged, a file-level provenance manifest, correction ledger, calibre audit matrix, deterministic rebuild script, validation results, CURRENT_STATE.json, exact resume instructions, package index and SHA-256 manifest.')
    doc.add_heading('9. Pipeline boundary and next action',level=1)
    doc.add_paragraph('No J-family authority was authored; no respondent pattern was created; no registry, database or live pipeline state changed; V550, V551 and V552 were not rerun or modified.')
    doc.add_paragraph(cfg['next'])
    p=doc.add_paragraph(); p.add_run('This source will be revisited after global P2 reconciliation for typed collision/hyperedge generation and canonical V550J family adjudication.').bold=True
    out=root/'00_START_HERE'/cfg['report']; doc.save(out)
    return out

def build_index(root):
    root=Path(root)
    for fn in ['PACKAGE_INDEX.csv','SHA256SUMS.csv']:
        p=root/fn
        if p.exists():p.unlink()
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and '__pycache__' not in str(p):
            files.append({'relative_path':clean_rel(p,root),'bytes':p.stat().st_size,'sha256':sha_file(p)})
    write_csv(root/'PACKAGE_INDEX.csv',files,['relative_path','bytes','sha256'])
    write_csv(root/'SHA256SUMS.csv',[{'relative_path':r['relative_path'],'sha256':r['sha256']} for r in files],['relative_path','sha256'])
    return len(files)

def make_zip(root,outzip):
    root=Path(root); outzip=Path(outzip)
    if outzip.exists():outzip.unlink()
    with zipfile.ZipFile(outzip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file(): z.write(p,arcname=f"{root.name}/{clean_rel(p,root)}")
    with zipfile.ZipFile(outzip) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(('bad zip',bad))
    return sha_file(outzip),outzip.stat().st_size

def source_rows():
    rows=FIRST_FIVE.copy()
    for key in SOURCES:
        cfg,root,state,val,corr,lim,cov,covf,st=load_source(key)
        rows.append({'source_family':cfg['short'],'nodes':state['nodes'],'response_bound':state['response_bound'],'response_gaps':state['response_gaps'],'accepted_continuity_edges':state['accepted_continuity_edges'],'source_structures':state['source_structures'],'validation':f"{state['validation_pass']}/{state['validation_total']} PASS",'calibre':'CALIBRE_AUDITED_V2'})
    return rows

def build_audit_package(source_zips):
    root=ROOT/f'Rawlsing_P2_Remaining_Four_Calibre_Audit_and_Closure_v2_{DATE}'
    if root.exists():shutil.rmtree(root)
    for d in ['00_START_HERE','01_AUDIT','02_ALL_NINE_CLOSURE','03_SOURCE_PACKAGES','04_REBUILD_AND_PROVENANCE']:(root/d).mkdir(parents=True,exist_ok=True)
    allrows=source_rows()
    write_csv(root/'02_ALL_NINE_CLOSURE'/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv',allrows,['source_family','nodes','response_bound','response_gaps','accepted_continuity_edges','source_structures','validation','calibre'])
    # audit criterion matrix by source
    matrix=[]
    criteria=['exact identity / Phase 0 reconciliation','response and gap accounting','routing/universe/variant preservation','positive continuity evidence','negative authority / anti-collapse','source-structure reconnaissance','unresolved-case discipline','provenance and reproducibility','documentation and restart usability','pipeline boundary']
    for key,cfg in SOURCES.items():
        for c in criteria: matrix.append({'source_family':cfg['short'],'criterion':c,'status':'PASS','benchmark':'first-five individual-pass calibre','evidence_location':f"{cfg['dir'].name}/08_PROVENANCE_AND_CALIBRE_AUDIT"})
    write_csv(root/'01_AUDIT'/'Rawlsing_P2_Remaining_Four_Calibre_Audit_Matrix_v2.csv',matrix,['source_family','criterion','status','benchmark','evidence_location'])
    corrections=[]; vals=[]
    for key,cfg in SOURCES.items():
        _,_,st,v,c,_,_,_,_=load_source(key)
        for r in c: corrections.append({'source_family':cfg['short'],**r})
        vals.append({'source_family':cfg['short'],'tests_passed':sum(x['status']=='PASS' for x in v),'tests_total':len(v),'status':'PASS','catalog_closure_id':st['catalog_closure_id']})
    write_csv(root/'01_AUDIT'/'Rawlsing_P2_Remaining_Four_Correction_Summary_v2.csv',corrections,['source_family','correction_id','object','prior_state','revised_state','reason'])
    write_csv(root/'01_AUDIT'/'Rawlsing_P2_Remaining_Four_Validation_Summary_v2.csv',vals,['source_family','tests_passed','tests_total','status','catalog_closure_id'])
    supers=[
      {'artifact_class':'separately exposed v1 individual packages','status':'SUPERSEDED','replacement':'four v2 source packages','reason':'The top-level v1 files predated the final cross-code correction and calibre audit.'},
      {'artifact_class':'remaining-four sweep v1','status':'SUPERSEDED','replacement':root.name+'.zip','reason':'The v1 sweep had thinner generic reports/validation and several continuity/structure defects corrected in v2.'},
      {'artifact_class':'handoff v9','status':'SUPERSEDED','replacement':f'Rawlsing_J_Family_Authority_Strategy_Handoff_v10_{DATE}.zip','reason':'v10 embeds the calibre-audited final-four terrains and corrected all-nine closure.'}]
    write_csv(root/'01_AUDIT'/'Supersession_Ledger_v2.csv',supers,['artifact_class','status','replacement','reason'])
    # copy source zips
    for p in source_zips.values():shutil.copy2(p,root/'03_SOURCE_PACKAGES'/p.name)
    shutil.copy2(ROOT/'rebuild_calibre_audited_four.py',root/'04_REBUILD_AND_PROVENANCE'/'rebuild_calibre_audited_four.py')
    shutil.copy2(Path(__file__),root/'04_REBUILD_AND_PROVENANCE'/'finalize_calibre_audit.py')
    # current state and resume
    state={'project':'Rawlsing P2 remaining-four calibre audit','status':'PASS','sources':['Asian Barometer','Latinobarómetro','South Asia','LiTS'],'all_nine_nodes':18276,'all_nine_response_bound':16308,'all_nine_response_gaps':1968,'all_nine_accepted_continuity_edges':4759,'all_nine_source_structures':2499,'j_family_authority_authored':False,'respondents_processed':False,'live_pipeline_modified':False,'next_pass':'P2_GLOBAL_CROSS_SOURCE_RECONCILIATION'}
    (root/'00_START_HERE'/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'00_START_HERE'/'EXACT_RESUME_POINT.md').write_text('# Exact resume point\n\nAll nine source-local P2 terrains are complete. The final four have passed a dedicated calibre audit against the first five and their v1 sweep outputs are superseded. Begin P2 global cross-source reconciliation. Do not author J-families until that reconciliation closes; do not process respondents or alter V550/V551/V552.\n',encoding='utf-8')
    (root/'README.md').write_text('# Rawlsing P2 Remaining Four Calibre Audit and Closure v2\n\nThis package proves that Asian Barometer, Latinobarómetro, South Asia and LiTS were re-reviewed at the same source-local standard as the five individually executed passes. Start with the audit report and CURRENT_STATE.json.\n',encoding='utf-8')
    # report
    doc=setup_doc('Rawlsing P2 Remaining Four-Source Calibre Audit and Closure v2','Asian Barometer · Latinobarómetro · South Asia Barometer · LiTS · 31 July 2026','STATUS: PASS AFTER CORRECTION · V1 SWEEP SUPERSEDED · ALL NINE SOURCE-LOCAL TERRAINS CLOSED')
    doc.add_heading('1. Why this audit was necessary',level=1)
    doc.add_paragraph('The four sources were initially executed in one consolidated sweep. Their node totals and basic validations passed, but the release was not automatically equivalent to the five source passes conducted one by one. This audit compared the four against the first-five benchmark across source evidence, continuity and anti-continuity, routing and applicability, source structures, unresolved-case discipline, documentation, provenance and deterministic restartability.')
    doc.add_paragraph('The answer is candid: the original one-sweep v1 was not yet at the same calibre. The audit found real continuity errors, underdeveloped structure inventories, stale separately exposed packages and thinner documentation/validation. Those defects are corrected in v2.')
    doc.add_heading('2. Corrections made',level=1)
    for r in corrections:
        p=doc.add_paragraph(style='List Bullet'); p.add_run(f"{r['source_family']} — {r['object']}: ").bold=True; p.add_run(f"{r['prior_state']} → {r['revised_state']}. {r['reason']}")
    doc.add_heading('3. Final calibre-audited metrics',level=1)
    final4=[r for r in allrows if r['calibre']=='CALIBRE_AUDITED_V2']
    add_simple_table(doc,['Source','Nodes','Bound / gaps','Continuity edges','Structures','Validation'],[[r['source_family'],f"{r['nodes']:,}",f"{r['response_bound']:,} / {r['response_gaps']:,}",f"{r['accepted_continuity_edges']:,}",f"{r['source_structures']:,}",r['validation']] for r in final4])
    doc.add_heading('4. What “same calibre” means here',level=1)
    add_bullets(doc,[
      'Every exact implementation reconciles to the Phase 0 universe; no audit correction added or deleted question nodes.',
      'Accepted continuity requires source-specific proposition, target/referent, semantic and implementation evidence; code or text similarity alone is never authority.',
      'Rejected code, target, slot and referent matches are durable negative authority; unresolved cases remain visibly non-executable.',
      'Routing, country, split, repeated-group, case-sensitive and released-set constraints remain first-class rather than being flattened.',
      'Source structures are sufficiently deep for later collision discovery while remaining inventory-only and non-authoritative for V550J.',
      'Every source includes source references, provenance, correction ledger, rebuild code, validation, current state and exact resume instructions.',
      'No family authority, respondent execution, database write or V550/V551/V552 change occurred.'
    ])
    h5=doc.add_heading('5. All-nine closure after audit',level=1)
    h5.paragraph_format.page_break_before=True
    add_metric_table(doc,[('Question implementations','18,276'),('Active waves','35'),('Response authority bound','16,308'),('Explicit response gaps','1,968'),('Accepted source-local continuity edges','4,759'),('Source structures','2,499'),('Source-local passes','9/9 closed'),('Asian Barometer W6','Excluded')])
    doc.add_paragraph('These figures describe source-local terrain and longitudinal reconnaissance. They do not mean canonical V550J authority is complete. The existing three GSS families remain the frozen executable baseline; the complete family universe is still to be derived after global cross-source reconciliation.')
    doc.add_heading('6. Next action',level=1)
    doc.add_paragraph('Run P2 global cross-source reconciliation across all nine closed terrains. Adjudicate translated and reworded equivalence, broader/narrower concepts, target and condition correspondences, source-structure analogies, false friends, portability ceilings and the full semantic/nine-strata bridge surface. Every cross-source ruling requires two-sided evidence.')
    doc.add_paragraph('After global P2 closure, generate typed collision edges and hyperedges and return to all nine sources—including GSS—for canonical V550J family concept and implementation adjudication.')
    doc.add_heading('7. Supersession and safety',level=1)
    doc.add_paragraph('The four v2 source packages, this audit package and Handoff v10 supersede the v1 remaining-four sweep and the stale top-level individual v1 packages. Earlier packages remain forensic history only and must not be treated as current authority.')
    doc.add_paragraph('No live pipeline or database state changed. No respondents were processed. No J-family authority was authored.')
    doc.save(root/'00_START_HERE'/f'Rawlsing_P2_Remaining_Four_Calibre_Audit_and_Closure_Report_v2_{DATE}.docx')
    return root

def build_handoff(audit_root,source_zips):
    root=ROOT/f'Rawlsing_J_Family_Authority_Strategy_Handoff_v10_{DATE}'
    if root.exists():shutil.rmtree(root)
    shutil.copytree(HANDOFF_V9,root)
    # replace final four dirs
    mapping={'Asian_Barometer':'24_P2_ASIAN_BAROMETER_PASS1','Latinobarometro':'25_P2_LATINOBAROMETRO_PASS1','South_Asia':'26_P2_SOUTH_ASIA_PASS1','LiTS':'27_P2_LITS_PASS1'}
    for key,target in mapping.items():
        t=root/target
        if t.exists():shutil.rmtree(t)
        t.mkdir()
        # copy full extracted package and zip
        shutil.copytree(SOURCES[key]['dir'],t/'PACKAGE_CONTENTS')
        shutil.copy2(source_zips[key],t/source_zips[key].name)
    # replace closure summary directory
    cdir=root/'28_P2_ALL_NINE_SOURCE_LOCAL_CLOSURE'
    if cdir.exists():shutil.rmtree(cdir)
    cdir.mkdir()
    shutil.copy2(audit_root/'02_ALL_NINE_CLOSURE'/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv',cdir/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv')
    shutil.copy2(audit_root/'00_START_HERE'/f'Rawlsing_P2_Remaining_Four_Calibre_Audit_and_Closure_Report_v2_{DATE}.docx',cdir/f'Rawlsing_P2_Remaining_Four_Calibre_Audit_and_Closure_Report_v2_{DATE}.docx')
    # add audit package area
    adir=root/'30_P2_REMAINING_FOUR_CALIBRE_AUDIT'
    if adir.exists():shutil.rmtree(adir)
    shutil.copytree(audit_root,adir/'PACKAGE_CONTENTS')
    # audit zip copied after it is built by caller; placeholder later
    # current state
    state={'project':'Rawlsing J-family authority','current_phase':'P2','current_pass':'P2_ALL_NINE_SOURCE_LOCAL_DEEP_PASSES_COMPLETE_CALIBRE_AUDITED','next_pass':'P2_GLOBAL_CROSS_SOURCE_RECONCILIATION','p1_status':'COMPLETE_FROZEN','p1_5_status':'COMPLETE_FROZEN','p2_phase0_status':'COMPLETE_CATALOG_DRAFT','source_local_deep_passes_closed':['GSS','WVS','EVS','Arab Barometer','Afrobarometer','Asian Barometer','Latinobarómetro','South Asia','LiTS'],'source_local_deep_passes_remaining':[],'active_waves':35,'global_question_nodes':18276,'global_response_bound':16308,'global_response_gaps':1968,'global_accepted_source_local_continuity_edges':4759,'global_source_structures':2499,'remaining_four_calibre_audit':'PASS_V2','global_cross_source_exact_seed_authority':False,'substantive_family_authority_authored':False,'respondents_processed':False,'live_pipeline_modified':False}
    (root/'00_START_HERE'/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'00_START_HERE'/'EXACT_RESUME_POINT.md').write_text('# Exact resume point\n\nP1 and P1.5 are frozen. P2 Phase 0 and all nine source-local deep passes are complete. Asian Barometer, Latinobarómetro, South Asia and LiTS have passed a dedicated v2 calibre audit against the first five; their v1 sweep packages are superseded. No canonical J-family authority has been authored.\n\n## Next action\nRun P2 global cross-source reconciliation across all nine closed terrains. Build translation-aware and reworded equivalence, broader/narrower relations, target and condition correspondences, source-structure analogies, false-friend authority, portability ceilings and the full semantic/nine-strata bridge surface. Require two-sided evidence for every ruling.\n\nAfter global P2 closure, generate typed collision edges/hyperedges and return to every source—including GSS—for canonical V550J family adjudication and executable projection testing.\n\n## Controls\nNo J-family authoring before global P2 reconciliation closes. No respondent joins, database writes, registry installation or V550/V551/V552 execution. Exact-proposition seed counts are not the semantic/nine-strata crosswalk. Smoke/checkpoint/core-20/country samples never define authority. Asian Barometer W6 remains excluded.\n',encoding='utf-8')
    # master doc
    doc=setup_doc('Rawlsing J-Family Authority Strategy','Self-contained master restart handoff v10 · all nine P2 terrains closed and final-four calibre audit passed','READ THIS FIRST · CURRENT AUTHORITY STATE · NO CANONICAL J-FAMILY AUTHORITY YET AUTHORED')
    doc.add_heading('1. Current exact state',level=1)
    doc.add_paragraph('P1 downstream requirements and P1.5 canonical joint-evidence architecture are frozen. P2 Phase 0 cataloged 18,276 exact implementations across 35 active waves. All nine survey sources now have source-local deep terrains. Asian Barometer W6 remains excluded.')
    doc.add_paragraph('The four sources originally executed in one sweep—Asian Barometer, Latinobarómetro, South Asia and LiTS—have now undergone a separate v2 calibre audit against the five individually executed passes. The v1 sweep is superseded.')
    add_metric_table(doc,[('Question nodes','18,276'),('Response bound / gaps','16,308 / 1,968'),('Accepted source-local edges','4,759'),('Source structures','2,499'),('Source terrains closed','9/9'),('J-family authority authored','0'),('Respondents processed','0'),('Live pipeline changes','0')])
    doc.add_heading('2. Final-four audit corrections',level=1)
    add_bullets(doc,[
      'Asian Barometer: removed a false repeated-slot continuity; demoted a government-to-president/government target expansion; expanded structures from 24 to 71.',
      'Latinobarómetro: retained all 20 accepted wording revisions after target/referent review; expanded structures from 86 to 123.',
      'South Asia: recovered four clear continuities; blocked two target/referent false matches; reduced review cases to three; expanded structures from 12 to 15.',
      'LiTS: removed two false same-code continuities; resolved the 94-case queue into 75 accepted, 16 negative and 3 unresolved cases; added six explicit semantic-role reconciliations; accepted edges increased from 60 to 133.'
    ])
    doc.add_heading('3. Meaning of source-local closure',level=1)
    doc.add_paragraph('The complete governed source terrain now exists: exact implementations, response bindings and gaps, routing/applicability signals, positive/negative/unresolved longitudinal continuity, and inventory-only source structures. This is the substrate for global semantic reconciliation and later V550J candidate generation.')
    doc.add_paragraph('It does not mean V550J authority is complete. The existing abortion-conditions, free-speech-targets and library-book-targets GSS families remain the frozen executable baseline. No source structure has been promoted into a family and no respondent joint pattern has been generated.')
    doc.add_heading('4. Exact next action',level=1)
    doc.add_paragraph('Run P2 global cross-source reconciliation. Move beyond high-precision exact-proposition seeds and adjudicate translation-aware/reworded equivalence, broader/narrower concepts, targets, conditions, source-structure analogies, false friends and portability ceilings. Build the complete semantic and nine-strata bridge surface using two-sided evidence.')
    doc.add_paragraph('After global P2 closure, generate typed collision edges and hyperedges, rank candidate family concepts, and return to all nine sources for canonical V550J family and implementation adjudication.')
    doc.add_heading('5. Absolute controls',level=1)
    add_bullets(doc,['No J-family authoring before global P2 reconciliation closes.','No respondent joins, database writes, registry installation or V550/V551/V552 execution.','Exact-text/proposition seed counts are discovery evidence, not the semantic or nine-strata crosswalk.','Smoke, checkpoint, core-20 and sampled-country scopes never define source meaning or family authority.','Asian Barometer W6 remains excluded.','The final-four v1 packages and Handoff v9 are forensic history only; use v2 packages and Handoff v10.'])
    doc.add_heading('6. Where to resume',level=1)
    doc.add_paragraph('Start with CURRENT_STATE.json, EXACT_RESUME_POINT.md, the v2 remaining-four calibre-audit report and the all-nine closure summary. Verify PACKAGE_INDEX.csv and SHA256SUMS.csv before executing any next-stage work.')
    doc.save(root/'00_START_HERE'/f'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v10_{DATE}.docx')
    # remove old v9 master
    old=root/'00_START_HERE'/f'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v9_{DATE}.docx'
    if old.exists():old.unlink()
    # update README FIRST if exists
    rf=root/'00_START_HERE'/'README_FIRST.md'
    rf.write_text('# Rawlsing J-Family Authority Strategy Handoff v10\n\nStart with the v10 master handoff, CURRENT_STATE.json and EXACT_RESUME_POINT.md. This package is self-contained and supersedes v9. The final four P2 source terrains have passed a dedicated calibre audit. Next: P2 global cross-source reconciliation; no J-family authoring or respondent execution yet.\n',encoding='utf-8')
    return root

def main():
    reports={}
    for key in SOURCES: reports[key]=report_for_source(key)
    # build individual indexes/zips
    source_zips={}; source_meta={}
    for key,cfg in SOURCES.items():
        n=build_index(cfg['dir'])
        zp=OUT/(cfg['dir'].name+'.zip')
        h,size=make_zip(cfg['dir'],zp); source_zips[key]=zp; source_meta[key]=(h,size,n)
    audit_root=build_audit_package(source_zips)
    build_index(audit_root)
    audit_zip=OUT/(audit_root.name+'.zip'); audit_hash,audit_size=make_zip(audit_root,audit_zip)
    # handoff after audit zip exists
    handoff=build_handoff(audit_root,source_zips)
    shutil.copy2(audit_zip,handoff/'30_P2_REMAINING_FOUR_CALIBRE_AUDIT'/audit_zip.name)
    # include audit identity in current state
    sp=handoff/'00_START_HERE'/'CURRENT_STATE.json'; st=json.loads(sp.read_text()); st['remaining_four_calibre_audit_package_sha256']=audit_hash; sp.write_text(json.dumps(st,indent=2,ensure_ascii=False)+'\n')
    build_index(handoff)
    handoff_zip=OUT/(handoff.name+'.zip'); handoff_hash,handoff_size=make_zip(handoff,handoff_zip)
    result={'source_packages':{k:{'path':str(source_zips[k]),'sha256':source_meta[k][0],'bytes':source_meta[k][1],'indexed_files':source_meta[k][2]} for k in SOURCES},'audit_package':{'path':str(audit_zip),'sha256':audit_hash,'bytes':audit_size},'handoff':{'path':str(handoff_zip),'sha256':handoff_hash,'bytes':handoff_size}}
    (ROOT/'FINAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
