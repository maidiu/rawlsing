from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
root=Path('/mnt/data/rawlsing_v17_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v17_20260731')
sec=root/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5'
nextp='P2_GLOBAL_NEXT_FIXED_3000_PAIR_TRANCHE_FROM_8847_REMAINING_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION'
d=Document(); s=d.sections[0]; s.top_margin=Inches(.38); s.bottom_margin=Inches(.38); s.left_margin=Inches(.62); s.right_margin=Inches(.62)
for name,size in [('Normal',8.6),('Title',17),('Heading 1',11.8)]: d.styles[name].font.name='Aptos' if name=='Normal' else 'Aptos Display'; d.styles[name].font.size=Pt(size)
p=d.add_paragraph(style='Title'); p.paragraph_format.space_after=Pt(1); p.add_run('P2 Media/Civic Adjudication — Fixed 3,000 Tranche 5')
p=d.add_paragraph(); p.paragraph_format.space_after=Pt(4); r=p.add_run('Acceptance-complete authority return'); r.italic=True

def h(t):
 p=d.add_heading(t,1); p.paragraph_format.space_before=Pt(5); p.paragraph_format.space_after=Pt(1)
def line(label,value):
 p=d.add_paragraph(); p.paragraph_format.space_after=Pt(0); r=p.add_run(label+': '); r.bold=True; p.add_run(value)
def bullet(t):
 p=d.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(0); p.add_run(t)

h('Fixed work-unit return')
line('Queue','11,847 incoming → 3,000 adjudicated exactly → 8,847 remaining')
line('Selection','893 news-source; 601 internet; 554 political-discussion; 527 political-interest; 425 demonstration candidates')
line('Evidence and tests','379 lineages; 3,000 rulings; 6,000 side records; 25 adversarial tests passed; six-artifact rebuild hash-exact')

h('Authority partition')
for t in ['72 reworded proposition equivalences.','312 coordinate-only relations.','2,554 explicit negative-authority relations.','27 redirects to their proper substantive domain.','35 unresolved relations, bounded to two under-specified source-native lineages.']: bullet(t)

h('Acceptance controls')
d.add_paragraph('Proposition authority requires exact identity of relation axis, target or scope, and operator, with HIGH-confidence evidence on both sides. Every one of the 72 acceptances was reviewed against exact question and response evidence. MEDIUM and unresolved lineages export no proposition authority.')
d.add_paragraph('The pass preserves news-medium specificity; media bias versus media use; broadband, home, mobile and general internet distinctions; access versus frequency or use; explicit news timeframes; social targets of discussion and persuasion; campaign-rally time scope; and protest participation versus willingness or mixed disposition.')

h('Selection and authority boundary')
d.add_paragraph('Selected and remaining IDs form an exact disjoint partition of the incoming queue. These are pair-relation rulings only: no J-family membership, value portability, respondent join, database write, registry installation, or production execution follows.')
line('Next pass',nextp)
foot=s.footer.paragraphs[0]; foot.alignment=WD_ALIGN_PARAGRAPH.CENTER; rr=foot.add_run('Rawlsing P2 fixed 3,000 tranche 5 — 2026-07-31'); rr.font.size=Pt(7.5)
d.save(sec/'Rawlsing_P2_Global_Media_Civic_Fixed_3000_Tranche5_Report_20260731.docx')
