from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

ROOT=Path('/mnt/data/rawlsing_v17_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v17_20260731')
SEC=ROOT/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5'
NEXT='P2_GLOBAL_NEXT_FIXED_3000_PAIR_TRANCHE_FROM_8847_REMAINING_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION'

def setup(doc,title,subtitle):
    sec=doc.sections[0]
    sec.top_margin=Inches(.55); sec.bottom_margin=Inches(.55); sec.left_margin=Inches(.68); sec.right_margin=Inches(.68)
    styles=doc.styles
    styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(9.5)
    styles['Title'].font.name='Aptos Display'; styles['Title'].font.size=Pt(20)
    styles['Heading 1'].font.name='Aptos Display'; styles['Heading 1'].font.size=Pt(14)
    styles['Heading 2'].font.name='Aptos Display'; styles['Heading 2'].font.size=Pt(11.5)
    p=doc.add_paragraph(style='Title'); p.paragraph_format.space_after=Pt(3); p.add_run(title)
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(8); r=p.add_run(subtitle); r.italic=True
    foot=sec.footer.paragraphs[0]; foot.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rr=foot.add_run('Rawlsing cumulative authority handoff — 2026-07-31'); rr.font.size=Pt(8)

def bullet(doc,text):
    p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(1); p.add_run(text)

def keyline(doc,label,value):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(2); r=p.add_run(label+': '); r.bold=True; p.add_run(value)

# Master
D=Document(); setup(D,'Rawlsing J-Family Authority Strategy — Master Handoff v17','Governing cumulative restart state after global P2 fixed 3,000-pair tranche 5')
D.add_heading('Current state',1)
keyline(D,'Phase','P2 global cross-source semantic reconciliation — OPEN')
keyline(D,'Completed pass','P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5_COMPLETE')
keyline(D,'Queue movement','11,847 pending → 3,000 adjudicated → 8,847 pending')
keyline(D,'Cumulative semantic-priority adjudication','9,984 of 18,831 pairs')
keyline(D,'Canonical J-family authority','Not authored')
keyline(D,'Respondent or production execution','None')

D.add_heading('What tranche 5 completed',1)
for x in [
 'Froze exactly 3,000 candidate rows: 893 MEDIA_NEWS_SOURCE, 601 MEDIA_INTERNET, 554 CIVIC_DISCUSS_POLITICS, 527 CIVIC_INTEREST_POLITICS, and 425 highest-priority CIVIC_DEMONSTRATION rows.',
 'Classified 379 source-local lineages from exact source-native question, response, and structure evidence.',
 'Issued 3,000 pair rulings and 6,000 side-level evidence records.',
 'Reviewed all 72 proposition-equivalence acceptances against their exact two-sided item and response evidence.',
 'Preserved medium, target, operator, timeframe, participation mode, and access/use distinctions that the inherited semantic neighborhoods blur.',
 'Passed 25 adversarial tests and a six-artifact hash-exact deterministic rebuild.'
]: bullet(D,x)

D.add_heading('Authority return',1)
for x in [
 '72 typed reworded proposition-equivalence relations.',
 '312 coordinate-only relations: 287 domain-coordinate and 25 same-construct/target with different operator or incomplete proposition evidence.',
 '2,554 explicit negative-authority relations.',
 '27 shared other-domain relations redirected for adjudication in their proper domain.',
 '35 unresolved relations, all caused by two under-specified source-native lineages.'
]: bullet(D,x)

D.add_heading('Critical distinctions preserved',1)
for x in [
 'Political-news use by television, radio, newspaper, mixed media, and unspecified media remains target-bounded.',
 'Partisan television-bias judgments remain distinct from frequency of watching news.',
 'Home broadband, generic home internet, mobile internet access, mobile internet use, and general internet frequency remain separate.',
 'Access availability remains distinct from frequency of access or use.',
 'Ordinary-week, last-week, daily, and unspecified-period news-use operators remain separate.',
 'Political discussion and persuasion retain the named social target: friends, colleagues, family, or unspecified others.',
 'Campaign-rally participation retains last-election, ever, and unspecified-period scope.',
 'Retrospective protest participation remains distinct from willingness, likelihood, and mixed past-or-willingness dispositions.'
]: bullet(D,x)

D.add_heading('Exact continuation',1)
keyline(D,'Resume token',NEXT)
for x in [
 'Use section 38’s 8,847-row remaining queue as the sole governing pending surface.',
 'Select exactly 3,000 rows under FIXED_3000_TRANCHE_PROTOCOL.md.',
 'Apply the embedded acceptance standard inside the tranche; do not create a separate automatic review loop.',
 'Package the full cumulative handoff before starting another work unit.'
]: bullet(D,x)

D.add_heading('Hard boundaries',1)
D.add_paragraph('Global P2 remains open. No canonical J-family membership, response-value harmonization, respondent join, registry installation, database write, or V550/V551/V552 production execution occurred. The component-aware V551J strata/horizon bridge v3.1 remains validated against recovered runtime evidence and uninstalled in Matthew’s current live repository. Asian Barometer W6 remains excluded.')
D.save(ROOT/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v17_20260731.docx')

# Tranche report
R=Document(); setup(R,'P2 Media/Civic Adjudication — Fixed 3,000 Tranche 5','Acceptance-complete authority return and exact continuation')
R.sections[0].top_margin=Inches(.42); R.sections[0].bottom_margin=Inches(.42)
R.styles['Normal'].font.size=Pt(8.7); R.styles['Title'].font.size=Pt(18); R.styles['Heading 1'].font.size=Pt(12.5)
R.add_heading('Fixed work-unit return',1)
for label,value in [
 ('Incoming queue','11,847'),('Selected and adjudicated','3,000 exactly'),('Remaining queue','8,847'),('Lineages classified','379'),('Pair rulings','3,000'),('Evidence records','6,000'),('Adversarial tests','25 passed'),('Deterministic rebuild','PASS — six tracked artifacts hash-identical')
]: keyline(R,label,value)

R.add_heading('Selection contract',1)
R.add_paragraph('The tranche consumes every remaining candidate in MEDIA_NEWS_SOURCE, MEDIA_INTERNET, CIVIC_DISCUSS_POLITICS, and CIVIC_INTEREST_POLITICS, then takes the highest-priority deterministic 425-row slice of CIVIC_DEMONSTRATION. Selected and remaining IDs form an exact disjoint partition of the incoming queue.')

R.add_heading('Authority partition',1)
for x in [
 '72 reworded proposition equivalences.',
 '287 domain-coordinate-only relations.',
 '25 same-construct/target coordinate-only relations with a different operator or incomplete proposition evidence.',
 '2,554 explicit negative-authority relations.',
 '27 redirects to another substantive domain.',
 '35 unresolved relations.'
]: bullet(R,x)

R.add_heading('Acceptance review',1)
R.add_paragraph('Proposition authority requires exact identity of governed relation axis, target or scope, and operator, with HIGH-confidence source-local classifications on both sides. All 72 acceptances were re-exposed with exact question text, response evidence, and portability ceiling. The review found no remaining proposition-level reversal after the pre-release corrections.')
R.add_paragraph('The unresolved surface is bounded to two prompts whose child action or participation target cannot be recovered from the delivered source-native record. No unresolved or MEDIUM-confidence lineage exports proposition authority.')

R.add_heading('Material false-equivalence controls',1)
for x in [
 'News medium and political-news medium are not interchangeable.',
 'Media bias judgments are not media-use frequency.',
 'Broadband, home internet, mobile access, mobile use, and general internet use are not one proposition.',
 'Timeframes and frequency operators remain explicit.',
 'Discussion and persuasion retain their social target.',
 'Campaign and protest items retain temporal scope and participation mode.',
 'Exact normalized text cannot override a material relation-axis difference.'
]: bullet(R,x)

R.add_heading('Authority boundary and continuation',1)
R.add_paragraph('These are pair-relation rulings only. They create no J-family membership, value portability, respondent identity, or production permission.')
keyline(R,'Next pass',NEXT)
R.save(SEC/'Rawlsing_P2_Global_Media_Civic_Fixed_3000_Tranche5_Report_20260731.docx')
