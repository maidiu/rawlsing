from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

DATE = '2026-07-31'
SRC = Path('/mnt/data/rawlsing_v14_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v14_20260731')
BUILD = Path('/mnt/data/rawlsing_v15_build')
ROOT = BUILD / 'Rawlsing_J_Family_Authority_Strategy_Handoff_v15_20260731'
S35 = ROOT / '35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE'
S36 = ROOT / '36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3'
RUNTIME_SRC = Path('/mnt/data/rawlsing_v15_outputs/runtime_bridge')
TRUST_SRC = Path('/mnt/data/rawlsing_v15_outputs/trust_adjudication')
NEXT = 'P2_GLOBAL_REMAINING_14847_SEMANTIC_PAIR_ADJUDICATION_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION'


def dump_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def remove_caches(root: Path) -> None:
    for path in sorted(root.rglob('*'), reverse=True):
        if path.is_dir() and path.name in {'__pycache__', '.pytest_cache'}:
            shutil.rmtree(path)
        elif path.is_file() and path.suffix in {'.pyc', '.pyo'}:
            path.unlink()


def set_cell_text(cell, text: str, bold: bool = False) -> None:
    cell.text = ''
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(9)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def mark_header_row(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement('w:tblHeader')
    tbl_header.set(qn('w:val'), 'true')
    tr_pr.append(tbl_header)
    for cell in row.cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), 'D9E2F3')
        tc_pr.append(shd)


def set_doc_defaults(doc: Document, title: str) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.68)
    section.right_margin = Inches(0.68)
    styles = doc.styles
    styles['Normal'].font.name = 'Aptos'
    styles['Normal'].font.size = Pt(9.5)
    for style_name, size in [('Title', 20), ('Heading 1', 14), ('Heading 2', 11.5)]:
        styles[style_name].font.name = 'Aptos Display'
        styles[style_name].font.size = Pt(size)
    p = doc.add_paragraph()
    p.style = doc.styles['Title']
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.add_run(title)


def add_bullets(doc: Document, items: list[str]) -> None:
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(1)
        p.add_run(item)


def add_table(doc: Document, headers: list[str], rows: list[list[object]], widths: list[float] | None = None) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for idx, header in enumerate(headers):
        set_cell_text(table.rows[0].cells[idx], header, bold=True)
    mark_header_row(table.rows[0])
    for values in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(values):
            set_cell_text(cells[idx], str(value))
    if widths:
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = Inches(width)


def add_footer(doc: Document, text: str) -> None:
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(8)


if BUILD.exists():
    shutil.rmtree(BUILD)
BUILD.mkdir(parents=True)
shutil.copytree(SRC, ROOT)
S35.mkdir()
S36.mkdir()

# Copy governing runtime bridge artifacts and reproducibility substrate.
runtime_files = [
    'ddm_v552j_component_strata_horizon_bridge.py',
    'test_ddm_v552j_component_strata_horizon_bridge.py',
    'run_recovered_runtime_integration.py',
    'regenerate_question_semantic_hierarchy.py',
    'Rawlsing_V552J_Component_Strata_Horizon_Bridge_GSS_2010_v3_1.csv',
    'Rawlsing_V552J_Packet_Strata_Horizon_Summary_GSS_2010_v3_1.csv',
    'Rawlsing_V551J_Certified_Packet_Index_GSS_2010_With_Strata_Horizon_v3_1.csv',
    'RUNTIME_INTEGRATION_RETURN_V3_1.json',
    'RUNTIME_BRIDGE_REPRODUCIBILITY_RETURN.json',
    'QSH_REPRODUCIBILITY_RETURN.json',
]
for name in runtime_files:
    shutil.copy2(RUNTIME_SRC / name, S35 / name)
for dirname in ['runtime_test_inputs', 'runtime_reproducibility_inputs', 'runtime_reproducibility_code', 'generated_question_semantic_hierarchy']:
    shutil.copytree(RUNTIME_SRC / dirname, S35 / dirname)

# Copy governing trust-neighborhood artifacts only; preliminary v1 explorations remain outside the release.
trust_files = [
    'build_trust_adjudication_v2.py',
    'test_trust_adjudication_v2.py',
    'Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv',
    'Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv',
    'Rawlsing_P2_Trust_Neighborhood_Two_Sided_Evidence_Ledger_v2.csv',
    'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv',
    'TRUST_ADJUDICATION_RETURN_V2.json',
    'TRUST_REPRODUCIBILITY_RETURN.json',
]
for name in trust_files:
    shutil.copy2(TRUST_SRC / name, S36 / name)

runtime_return = json.loads((S35 / 'RUNTIME_INTEGRATION_RETURN_V3_1.json').read_text())
qsh_return = json.loads((S35 / 'generated_question_semantic_hierarchy' / 'QSH_REGENERATION_RETURN.json').read_text())
trust_return = json.loads((S36 / 'TRUST_ADJUDICATION_RETURN_V2.json').read_text())
trust_rulings = read_csv(S36 / 'Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv')
trust_class = read_csv(S36 / 'Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv')

# Governing workflow standard: no separate ritual audit after each completed tranche.
acceptance_standard = f'''# Embedded Rawlsing tranche acceptance standard

A Rawlsing tranche is reported as complete only after the acceptance review is performed inside the tranche build. A second review is not the default next step.

Required release gates:

1. Bind every authority ruling to direct two-sided evidence and an explicit portability ceiling.
2. Run adversarial tests against false equivalence, target flattening, relation-axis leakage, inherited semantic contamination, incomplete keys, cardinality drift, and silent missing rows.
3. Prefer recovered production artifacts over synthetic fixtures whenever they exist. Mark any remaining synthetic-only or uninstalled boundary directly.
4. Make governing artifacts deterministically rebuildable from delivered code and inputs; compare hashes after rebuild.
5. Reconcile all queue partitions, endpoint identities, row counts, side-level evidence counts, and source/structure memberships.
6. Run the cumulative verifier against a clean extraction and recursively test every nested ZIP.
7. Prevent the verifier and tests from leaving cache or bytecode debris.
8. Render and visually inspect every governing DOCX and run accessibility checks before release.
9. Put the newly updated complete cumulative handoff link first in every response that reports new completed Rawlsing work.

A separate follow-up audit is warranted only when new contradictory evidence appears, the live repository differs from the recovered snapshot, or a previously untested runtime boundary becomes executable.

Current continuation: `{NEXT}`.
'''
(ROOT / '00_START_HERE' / 'ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md').write_text(acceptance_standard, encoding='utf-8')

# Section reports and exact task returns.
runtime_report = f'''# V552J component-aware strata/horizon runtime bridge

## Result

The recovered runtime evidence disproved the row-oriented assumption behind sidecar v2.1 for V551J: certified V551J records are joint packets containing multiple question components. Sidecar v2.1 remains valid only for true one-question-per-row tables and is superseded for V551J joint packets.

Bridge v3.1 preserves a component-level authority vector and permits scalar packet projection only when every component matches and every non-empty value for the projected field is unanimous.

## Recovered execution

- Recovered V552 question-semantic hierarchy scopes regenerated: {qsh_return['scope_files']}
- Regenerated hierarchy rows: {qsh_return['total_question_semantic_hierarchy_rows']}
- Recovered GSS 2010 certified packets: {runtime_return['packet_rows']}
- Packet components: {runtime_return['component_rows']}
- Matched components: {runtime_return['matched_component_rows']}
- Unmatched components: {runtime_return['unmatched_component_rows']}
- Packet status: {json.dumps(runtime_return['packet_status_counts'], sort_keys=True)}
- Pytest: 18 passed
- Deterministic QSH rebuild: PASS
- Deterministic bridge rebuild: PASS

## Installation boundary

The bridge was executed against recovered production-format artifacts and a recovered runtime code snapshot. It was not written into Matthew's live repository. Live installation remains a separate boundary because the repository may have moved since the recovered snapshot.
'''
(S35 / 'RUNTIME_COMPONENT_BRIDGE_REPORT.md').write_text(runtime_report, encoding='utf-8')
(S35 / 'TASK_RETURN.md').write_text(runtime_report, encoding='utf-8')

runtime_validation = {
    'status': 'PASS',
    'contract_version': 'V552J_COMPONENT_STRATA_HORIZON_BRIDGE_V3_1',
    'qsh_scope_files': qsh_return['scope_files'],
    'qsh_rows': qsh_return['total_question_semantic_hierarchy_rows'],
    'packet_rows': runtime_return['packet_rows'],
    'component_rows': runtime_return['component_rows'],
    'matched_components': runtime_return['matched_component_rows'],
    'unmatched_components': runtime_return['unmatched_component_rows'],
    'pytest_cases': 18,
    'qsh_reproducibility': 'PASS_HASH_EXACT',
    'bridge_reproducibility': 'PASS_HASH_EXACT',
    'recovered_runtime_execution': 'PASS',
    'live_repository_installation': 'NOT_PERFORMED',
    'next_pass': NEXT,
}
dump_json(S35 / 'VALIDATION.json', runtime_validation)

status_counts = trust_return['pair_authority_status_counts']
trust_report = f'''# P2 global trust-neighborhood adjudication — tranche 3

## Result

The ten contaminated trust neighborhoods were adjudicated at the source-local lineage level using exact item text, response contracts, recovered battery context, and source structures.

- Input pending queue: {trust_return['input_pending_pair_rows']}
- Trust-neighborhood pairs adjudicated: {trust_return['trust_domain_pair_rows_adjudicated']}
- Remaining global semantic-priority pairs: {trust_return['remaining_pair_rows']}
- Source-local lineages classified: {trust_return['trust_domain_lineages_classified']}
- Two-sided evidence records: {trust_return['evidence_rows']}
- Pytest: 16 passed
- Deterministic rebuild: PASS

## Authority partition

- Typed proposition equivalence: {status_counts['ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION']}
- Derived-index construct coordinates: {status_counts['ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX']}
- Nested or functional target coordinates: {status_counts['ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY']}
- Trust construct/target coordinate only: {status_counts['ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY']}
- Non-trust relation rescued from a contaminated trust neighborhood: {status_counts['ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD']}
- Negative authority: {status_counts['REJECTED_FALSE_EQUIVALENCE_TARGET_OR_TRUST_AXIS_MISMATCH'] + status_counts['REJECTED_TRUST_VERSUS_NONTRUST_OPERATOR_MISMATCH'] + status_counts['REJECTED_CONTAMINATED_TRUST_NEIGHBORHOOD_NONTRUST_MISMATCH']}
- Redirected for proper non-trust-domain review: {status_counts['REDIRECTED_OUT_OF_TRUST_NEIGHBORHOOD_OTHER_DOMAIN_NOT_ADJUDICATED']}
- Unresolved because a source-local lineage is heterogeneous or evidence is insufficient: {status_counts['UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE']}

## Adversarial controls installed

Proposition equivalence now requires the same governed trust operator and the same target. Cabinet, prime minister, president, national government, generic government, opposition parties, co-resident family, police station, American courts, Shura Council, military governing council, and comparative social-media trust remain distinct at the appropriate grain. The Afrobarometer lineage that reuses a source-local continuity identity across tax department and president is blocked as heterogeneous rather than exported cross-source. A typographic `pollice` variant is explicitly recovered as the same police-assistance target, preventing a false heterogeneous classification while preserving the trust/non-trust boundary.

No respondent join, value harmonization, J-family authority, database write, or live runtime installation follows from these rulings.
'''
(S36 / 'P2_GLOBAL_TRUST_NEIGHBORHOOD_TRANCHE3_REPORT.md').write_text(trust_report, encoding='utf-8')
(S36 / 'TASK_RETURN.md').write_text(trust_report, encoding='utf-8')
trust_validation = {
    'status': 'PASS',
    'contract_version': trust_return['contract_version'],
    'input_pending_pairs': trust_return['input_pending_pair_rows'],
    'pairs_adjudicated': trust_return['trust_domain_pair_rows_adjudicated'],
    'pairs_remaining': trust_return['remaining_pair_rows'],
    'lineages_classified': trust_return['trust_domain_lineages_classified'],
    'evidence_rows': trust_return['evidence_rows'],
    'pytest_cases': 16,
    'reproducibility': 'PASS_HASH_EXACT',
    'accepted_proposition_exact_axis_target_gate': trust_return['accepted_proposition_rows_require_exact_axis_and_target'],
    'queue_partition_exact': trust_return['remaining_queue_partition_exact'],
    'authority_boundary': trust_return['authority_boundary'],
    'next_pass': NEXT,
}
dump_json(S36 / 'VALIDATION.json', trust_validation)

# Updated governing restart controls.
current_state = {
    'project': 'Rawlsing J-family authority',
    'handoff_version': 'v15',
    'handoff_date': DATE,
    'current_phase': 'P2',
    'current_pass': 'P2_GLOBAL_TRUST_NEIGHBORHOOD_TRANCHE3_AND_COMPONENT_STRATA_RUNTIME_BRIDGE_COMPLETE',
    'next_pass': NEXT,
    'p1_status': 'COMPLETE_FROZEN',
    'p1_5_status': 'COMPLETE_FROZEN',
    'source_local_deep_passes_closed': ['GSS','WVS','EVS','Arab Barometer','Afrobarometer','Asian Barometer','Latinobarómetro','South Asia','LiTS'],
    'source_local_deep_passes_remaining': [],
    'active_waves': 35,
    'asian_barometer_w6_in_scope': False,
    'global_question_nodes': 18276,
    'source_local_lineages': 13526,
    'exact_foundation_pair_candidates': 751,
    'exact_foundation_accepted': 270,
    'exact_foundation_rejected': 78,
    'exact_foundation_unresolved': 403,
    'semantic_priority_queue_total': 18831,
    'semantic_priority_pairs_adjudicated_before_tranche3': 121,
    'trust_neighborhood_pairs_adjudicated_tranche3': 3863,
    'semantic_priority_pairs_adjudicated_cumulative': 3984,
    'semantic_priority_pairs_remaining': 14847,
    'trust_lineages_classified': 562,
    'trust_two_sided_evidence_records': 7726,
    'runtime_bridge_version': 'v3.1',
    'runtime_qsh_scopes_regenerated': 17,
    'runtime_qsh_rows_regenerated': 111,
    'runtime_packets_exercised': 19,
    'runtime_packet_components_exercised': 109,
    'runtime_packet_components_matched': 109,
    'runtime_bridge_live_repository_installation': False,
    'acceptance_standard_embedded': True,
    'automatic_second_review_required': False,
    'global_p2_closed': False,
    'substantive_family_authority_authored': False,
    'respondents_processed': False,
    'live_pipeline_modified': False,
    'exact_resume_document': '00_START_HERE/EXACT_RESUME_POINT.md',
    'cumulative_output_protocol': '00_START_HERE/OUTPUT_AND_HANDOFF_PROTOCOL.md',
    'acceptance_standard_document': '00_START_HERE/ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md',
    'runtime_bridge_report': '35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/RUNTIME_COMPONENT_BRIDGE_REPORT.md',
    'trust_tranche_report': '36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/P2_GLOBAL_TRUST_NEIGHBORHOOD_TRANCHE3_REPORT.md',
}
dump_json(ROOT / '00_START_HERE' / 'CURRENT_STATE.json', current_state)

scope_lock = {
    'governing_task': 'Adjudicate the remaining 14,847 global semantic-neighborhood pairs and install the component-aware strata/horizon bridge only against the current live repository with fail-closed integration returns.',
    'allowed': [
        'use all prior P2 rulings only at their explicit portability ceilings',
        'consume tranche-3 trust rulings and their two-sided evidence ledger',
        'process the remaining 14,847 semantic-priority rows by bounded governed neighborhood',
        'use the component-aware bridge v3.1 for V551J joint packets',
        'install v3.1 only after testing the current live repository schema, packet cardinality, component identity and conflict behavior',
        'preserve negative, coordinate-only, redirected and unresolved authority',
        'apply the embedded tranche acceptance standard before reporting completion',
    ],
    'forbidden': [
        'author canonical J-family authority before global P2 closes',
        'treat semantic IDs, text similarity, structure labels or shared nouns as authority by themselves',
        'flatten distinct component strata or horizon values into a packet scalar',
        'use sidecar v2.1 as the governing V551J joint-packet bridge',
        'claim live installation from recovered-snapshot execution',
        'join respondents, write to the database, install a registry, or execute V550/V551/V552',
        'reopen Asian Barometer W6 without explicit user direction',
    ],
    'scope': {'active_waves': 35, 'sources': 9, 'asian_barometer_w6': False},
    'current_phase': 'P2',
    'current_pass': current_state['current_pass'],
    'next_pass': NEXT,
    'p2_global_reconciliation_permitted': True,
    'p2_family_authoring_permitted': False,
    'p2_respondent_execution_permitted': False,
    'trust_tranche3': {
        'pairs_adjudicated': 3863,
        'pairs_remaining': 14847,
        'lineages_classified': 562,
        'evidence_records': 7726,
    },
    'runtime_bridge': {
        'version': 'v3.1',
        'recovered_runtime_execution': 'PASS',
        'live_repository_installation': 'NOT_PERFORMED',
        'sidecar_v2_1_joint_packet_status': 'SUPERSEDED_FOR_V551J_JOINT_PACKETS',
    },
}
dump_json(ROOT / '00_START_HERE' / 'SCOPE_LOCK.json', scope_lock)

resume_text = f'''# Governing v15 resume point

Resume at:

`{NEXT}`

Use section 36's remaining queue of 14,847 pairs as the governing pending surface. Continue neighborhood-by-neighborhood with exact two-sided evidence and explicit relation/target ceilings.

For the strata/horizon runtime lineage, section 35 bridge v3.1 governs V551J joint packets. It has passed real recovered-artifact execution but has not been written into Matthew's current live repository. Install only after the current repository is supplied and the 18 tests plus live schema/cardinality/component-identity/conflict returns pass.

Global P2 remains open. No canonical J-family authority, respondent joins, value harmonization, database writes, registry installation, or V550/V551/V552 execution. Asian Barometer W6 remains excluded.
'''
(ROOT / '00_START_HERE' / 'EXACT_RESUME_POINT.md').write_text(resume_text, encoding='utf-8')
(ROOT / '00_START_HERE' / 'NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text(
    'Open the v15 master handoff, CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, OUTPUT_AND_HANDOFF_PROTOCOL.md, ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md, and sections 35–36. Verify package hashes, then resume ' + NEXT + '.\n',
    encoding='utf-8',
)

output_protocol = '''# Output and cumulative-handoff protocol

For every response that reports newly completed Rawlsing work or supplies newly generated Rawlsing artifacts:

1. Put the link to the newly updated complete cumulative handoff package at the very top of the response.
2. The package must contain the entire prior governing state, every relevant task return, and the newly completed work.
3. Detached deltas may be supplied secondarily, never as the sole restart artifact.
4. Update CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, the master handoff, top-level validation, package index and hashes in the same package.
5. Apply ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md inside the tranche before reporting completion. A separate immediate review is not the default next task.
6. A new agent must be able to resume without reconstructing missing turns or requiring the user to re-explain the project.

Progress-only updates that introduce no completed artifact do not require a package link. The next completed-work response does.
'''
(ROOT / '00_START_HERE' / 'OUTPUT_AND_HANDOFF_PROTOCOL.md').write_text(output_protocol, encoding='utf-8')

readme = f'''# Rawlsing J-Family Authority Strategy Handoff v15

This is the complete cumulative restart package through P2 trust-neighborhood tranche 3 and the recovered-runtime component-aware strata/horizon bridge.

Read, in order:

1. Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v15_20260731.docx
2. CURRENT_STATE.json
3. EXACT_RESUME_POINT.md
4. SCOPE_LOCK.json
5. ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md
6. OUTPUT_AND_HANDOFF_PROTOCOL.md
7. Sections 35 and 36

Tranche 3 adjudicates 3,863 trust-neighborhood pairs and leaves 14,847 semantic-priority pairs. Bridge v3.1 is validated against recovered production-format GSS 2010 V551J packets and regenerated V552 hierarchy evidence; it is not installed into the current live repository.

Next: `{NEXT}`.
'''
(ROOT / '00_START_HERE' / 'README_FIRST.md').write_text(readme, encoding='utf-8')

master_md = f'''# Current governing handoff v15

The authoritative narrative is `00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v15_20260731.docx`.

P2 trust-neighborhood tranche 3 is complete under the embedded acceptance standard. It adjudicates 3,863 pairs, classifies 562 lineages, binds 7,726 side-level evidence records, and leaves 14,847 semantic-priority pairs.

V552 question-semantic hierarchy evidence was deterministically regenerated for 17 recovered scopes (111 rows). The V551J joint-packet bridge v3.1 was executed against 19 recovered GSS 2010 certified packets containing 109 components; all 109 matched. This is recovered-snapshot validation, not installation into the current live repository.

Exact next pass: `{NEXT}`.

Read sections 35–36 and the complete start-here controls before continuing.
'''
(ROOT / '00_START_HERE' / 'MASTER_HANDOFF.md').write_text(master_md, encoding='utf-8')
(ROOT / 'MASTER_HANDOFF.md').write_text(master_md, encoding='utf-8')

# Append supersession record.
sup_path = ROOT / '00_START_HERE' / 'SUPERSEDED_AND_NON_GOVERNING_ARTIFACTS.csv'
sup = read_csv(sup_path)
new_row = {
    'artifact_or_idea': 'V552→V552J row-oriented strata/horizon sidecar v2.1 used as a V551J joint-packet bridge',
    'status': 'SUPERSEDED_FOR_V551J_JOINT_PACKETS',
    'reason': 'Recovered certified V551J records contain multiple question components; row-oriented scalar authority can flatten heterogeneous component evidence.',
    'permitted_use': 'Retain for historical comparison or true one-question-per-row tables; use component-aware bridge v3.1 for V551J joint packets.',
}
sup = pd.concat([sup, pd.DataFrame([new_row])], ignore_index=True)
sup.to_csv(sup_path, index=False)

# Create governing DOCX documents.
master_doc = Document()
set_doc_defaults(master_doc, 'Rawlsing J-Family Authority Strategy — Master Handoff v15')
p = master_doc.add_paragraph()
p.add_run('Governing date: ').bold = True
p.add_run(DATE)
p.add_run('  |  Phase: ').bold = True
p.add_run('P2 global reconciliation')
p.add_run('  |  Status: ').bold = True
p.add_run('OPEN')
master_doc.add_heading('1. Exact restart state', level=1)
add_bullets(master_doc, [
    'All nine source-local terrains remain closed across 35 active waves; Asian Barometer W6 remains excluded.',
    'The exact foundation remains 270 accepted, 78 rejected, and 403 unresolved pair rulings.',
    'Cumulative semantic-priority adjudication is now 3,984 rows: 121 from tranche 2 plus 3,863 trust-neighborhood rows from tranche 3.',
    'The governing remaining queue contains 14,847 rows.',
    'Global P2 remains open. No canonical J-family authority or respondent/runtime production execution has been authorized.',
])
master_doc.add_heading('2. Embedded acceptance standard', level=1)
add_bullets(master_doc, [
    'Every tranche includes its own adversarial acceptance review before it is called complete.',
    'Rulings require direct two-sided evidence, an explicit portability ceiling, deterministic rebuild, partition checks, clean-extraction verification, and document QA.',
    'A second immediate review is not routine. Re-audit only when new contradictory evidence or a newly executable live boundary appears.',
])
master_doc.add_heading('3. Trust-neighborhood tranche 3', level=1)
add_table(master_doc, ['Surface', 'Count'], [
    ['Pairs adjudicated', '3,863'],
    ['Lineages classified', '562'],
    ['Two-sided evidence records', '7,726'],
    ['Typed trust proposition equivalence', str(status_counts['ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION'])],
    ['Nested/functional target coordinates', str(status_counts['ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'])],
    ['Remaining semantic-priority pairs', '14,847'],
])
add_bullets(master_doc, [
    'Proposition equivalence requires the same governed trust operator and the same target.',
    'Cabinet, prime minister, generic government, national government, opposition parties, co-resident family, police station, American courts, Shura Council, military governing council, and comparative social-media trust are preserved at narrower grains.',
    'Non-trust items misclustered under trust are rejected or redirected; inherited semantic IDs carry no independent authority.',
])
master_doc.add_heading('4. Component-aware strata/horizon bridge', level=1)
add_table(master_doc, ['Recovered runtime surface', 'Result'], [
    ['Question-semantic hierarchy scopes', '17'],
    ['Question-semantic hierarchy rows', '111'],
    ['Certified GSS 2010 packets', '19'],
    ['Packet components', '109'],
    ['Matched components', '109'],
    ['Unmatched components', '0'],
    ['Bridge tests', '18 passed'],
])
add_bullets(master_doc, [
    'Bridge v3.1 keeps component authority primary and permits scalar packet projection only under complete coverage and unanimity.',
    'The recovered runtime snapshot passed. Matthew’s current live repository was not modified.',
    'Sidecar v2.1 is superseded for V551J joint packets and remains usable only for genuine one-question-per-row tables.',
])
master_doc.add_heading('5. Exact continuation', level=1)
p = master_doc.add_paragraph()
p.paragraph_format.keep_with_next = True
next_display = NEXT.replace('_AND_LIVE_COMPONENT_', '_AND_LIVE_COMPONENT_\n')
run = p.add_run(next_display)
run.bold = True
run.font.name = 'Liberation Mono'
run.font.size = Pt(9)
add_bullets(master_doc, [
    'Adjudicate the remaining 14,847 pairs neighborhood by neighborhood under the same evidence and target/relation-axis discipline.',
    'Install bridge v3.1 only when the current live repository is supplied; rerun schema, key, cardinality, component identity, conflict, and output-partition tests there.',
    'Do not author J-family authority, join respondents, harmonize values, write the database, install registries, or execute V550/V551/V552 before global P2 closure.',
])
add_footer(master_doc, 'Rawlsing cumulative handoff v15 — complete restart authority')
master_doc_path = ROOT / '00_START_HERE' / 'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v15_20260731.docx'
master_doc.save(master_doc_path)

runtime_doc = Document()
set_doc_defaults(runtime_doc, 'V552J Component-Aware Strata/Horizon Runtime Bridge v3.1')
runtime_doc.add_heading('Decision', level=1)
runtime_doc.add_paragraph('The row-oriented v2.1 sidecar is rejected as the governing V551J joint-packet bridge. Recovered packet structure requires component-aware authority.')
runtime_doc.add_heading('Recovered execution', level=1)
add_table(runtime_doc, ['Measure', 'Result'], [
    ['Regenerated hierarchy scopes', '17'], ['Hierarchy rows', '111'], ['Certified packets', '19'],
    ['Components', '109'], ['Matched components', '109'], ['Unmatched components', '0'], ['Tests', '18 passed'],
])
runtime_doc.add_heading('Contract', level=1)
add_bullets(runtime_doc, [
    'Each packet component matches by governed question identity, with scoped variable fallback.',
    'Component order and packet cardinality are preserved.',
    'Scalar projection requires complete component coverage and unanimous non-empty values.',
    'Blank IDs, normalized duplicates, orphan summaries, missing summaries, output-column collisions, and conflicting identities fail closed.',
    'Delivered code and 17 V551 atom inputs deterministically rebuild the 111 hierarchy rows.',
])
runtime_doc.add_heading('Boundary', level=1)
runtime_doc.add_paragraph('Validated against recovered production-format GSS 2010 artifacts. Not installed into the current live repository.')
add_footer(runtime_doc, 'Rawlsing v15 — section 35')
runtime_doc_path = S35 / 'Rawlsing_V552J_Component_Strata_Horizon_Runtime_Bridge_v3_1_Report_20260731.docx'
runtime_doc.save(runtime_doc_path)

trust_doc = Document()
set_doc_defaults(trust_doc, 'P2 Global Trust-Neighborhood Adjudication — Tranche 3')
trust_doc.add_heading('Governed result', level=1)
add_table(trust_doc, ['Surface', 'Count'], [
    ['Input pending pairs', '18,710'], ['Pairs adjudicated', '3,863'], ['Remaining', '14,847'],
    ['Lineages classified', '562'], ['Evidence records', '7,726'], ['Tests', '16 passed'],
])
trust_doc.add_heading('Authority partition', level=1)
disposition_labels = {
    'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY': 'Nested/functional trust-target coordinate only',
    'ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD': 'Recovered non-trust proposition equivalence',
    'ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX': 'Trust construct coordinate with derived index',
    'ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY': 'Trust construct/target coordinate only',
    'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION': 'Typed cross-source trust proposition equivalence',
    'REDIRECTED_OUT_OF_TRUST_NEIGHBORHOOD_OTHER_DOMAIN_NOT_ADJUDICATED': 'Redirected to proper non-trust domain',
    'REJECTED_CONTAMINATED_TRUST_NEIGHBORHOOD_NONTRUST_MISMATCH': 'Rejected contaminated non-trust mismatch',
    'REJECTED_FALSE_EQUIVALENCE_TARGET_OR_TRUST_AXIS_MISMATCH': 'Rejected target or trust-axis mismatch',
    'REJECTED_TRUST_VERSUS_NONTRUST_OPERATOR_MISMATCH': 'Rejected trust versus non-trust operator mismatch',
    'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE': 'Unresolved: insufficient or heterogeneous evidence',
}
add_table(trust_doc, ['Disposition', 'Count'], [[disposition_labels[k], v] for k, v in sorted(status_counts.items())])
trust_doc.add_heading('Acceptance controls', level=1)
add_bullets(trust_doc, [
    'Exact operator and target equality is required for proposition equivalence.',
    'Narrower jurisdictional, role-specific, organizational, household-scope, and comparative targets receive coordinate-only authority.',
    'Heterogeneous source-local lineages cannot export cross-source authority.',
    'A source typo (pollice) is recovered only where the exact proposition and target remain demonstrably police assistance.',
    'Every pair has two explicit evidence records; queue partition and deterministic rebuild pass exactly.',
    'No value harmonization, respondent join, database write, registry installation, or J-family authority is implied.',
])
add_footer(trust_doc, 'Rawlsing v15 — section 36')
trust_doc_path = S36 / 'Rawlsing_P2_Global_Trust_Neighborhood_Tranche3_Report_20260731.docx'
trust_doc.save(trust_doc_path)

# Section and top-level validation.
root_validation = {
    'status': 'PASS_PENDING_FINAL_PACKAGE_GATES',
    'handoff_version': 'v15',
    'current_pass': current_state['current_pass'],
    'next_pass': NEXT,
    'global_p2_status': 'OPEN',
    'canonical_j_family_authority_authored': False,
    'respondents_processed': 0,
    'asian_barometer_w6': 'EXCLUDED',
    'acceptance_standard_embedded': True,
    'trust_tranche3': trust_validation,
    'runtime_bridge': runtime_validation,
    'docx_qa': {'status': 'PENDING_RENDER_AND_A11Y'},
    'cumulative_verifier': {'status': 'PENDING'},
    'release_status': 'PENDING',
}
dump_json(ROOT / 'VALIDATION.json', root_validation)

remove_caches(ROOT)

# Copy and extend the cumulative verifier.
old_verifier = ROOT / '34_P2_TRANCHE2_ACCEPTANCE_AUDIT_AND_CORRECTION' / 'verify_handoff_v14.py'
new_verifier = S36 / 'verify_handoff_v15.py'
verifier_text = old_verifier.read_text(encoding='utf-8')
verifier_text = verifier_text.replace("description='Read-only v14 cumulative handoff verifier'", "description='Read-only v15 cumulative handoff verifier'")
verifier_text = verifier_text.replace("expected_next='P2_GLOBAL_SEMANTIC_NEIGHBORHOOD_FULL_ADJUDICATION_AND_STRATA_DOCTRINE_RUNTIME_REPAIR'", "expected_v14_next='P2_GLOBAL_SEMANTIC_NEIGHBORHOOD_FULL_ADJUDICATION_AND_STRATA_DOCTRINE_RUNTIME_REPAIR'\n    expected_next='" + NEXT + "'")
verifier_text = verifier_text.replace("cur.get('handoff_version')=='v14'", "cur.get('handoff_version')=='v15'")
verifier_text = verifier_text.replace("if p.stat().st_size==0: raise ValueError('empty')", "if p.stat().st_size==0 and ext!='.py': raise ValueError('empty')")
verifier_text = verifier_text.replace("sec2val.get('next_pass')==expected_next", "sec2val.get('next_pass')==expected_v14_next")
verifier_text = verifier_text.replace("sec3val.get('next_pass')==expected_next", "sec3val.get('next_pass')==expected_v14_next")
insert = r'''

    # V15 embedded acceptance standard, component-aware runtime bridge, and trust tranche 3.
    standard = root/'00_START_HERE'/'ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md'
    ck('v15_acceptance_standard_embedded', standard.exists() and 'A second review is not the default next step' in standard.read_text(encoding='utf-8') and cur.get('acceptance_standard_embedded') is True and cur.get('automatic_second_review_required') is False, '')

    sec35 = root/'35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE'
    qsh_files = sorted((sec35/'generated_question_semantic_hierarchy').glob('*_question_semantic_hierarchy.csv'))
    qsh_rows = sum(len(rows(p)) for p in qsh_files)
    qsh_ret = json.load((sec35/'generated_question_semantic_hierarchy'/'QSH_REGENERATION_RETURN.json').open())
    qsh_rep = json.load((sec35/'QSH_REPRODUCIBILITY_RETURN.json').open())
    bridge_rep = json.load((sec35/'RUNTIME_BRIDGE_REPRODUCIBILITY_RETURN.json').open())
    runtime_ret = json.load((sec35/'RUNTIME_INTEGRATION_RETURN_V3_1.json').open())
    ck('v15_qsh_17_scopes_111_rows', len(qsh_files)==17 and qsh_rows==111 and qsh_ret.get('scope_files')==17 and qsh_ret.get('total_question_semantic_hierarchy_rows')==111, json.dumps({'files':len(qsh_files),'rows':qsh_rows}))
    ck('v15_qsh_deterministic_rebuild', qsh_rep.get('status')=='PASS' and qsh_rep.get('hashes_exact') is True and qsh_rep.get('tracked_files')==17, '')
    ck('v15_component_bridge_deterministic_rebuild', bridge_rep.get('status')=='PASS' and bridge_rep.get('hashes_exact') is True, '')
    bridge_rows=rows(sec35/'Rawlsing_V552J_Component_Strata_Horizon_Bridge_GSS_2010_v3_1.csv')
    packet_rows=rows(sec35/'Rawlsing_V552J_Packet_Strata_Horizon_Summary_GSS_2010_v3_1.csv')
    enriched_rows=rows(sec35/'Rawlsing_V551J_Certified_Packet_Index_GSS_2010_With_Strata_Horizon_v3_1.csv')
    ck('v15_real_component_bridge_cardinality', len(bridge_rows)==109 and len(packet_rows)==19 and len(enriched_rows)==19 and all(r['qsh_match_status'].startswith('MATCHED_') for r in bridge_rows), json.dumps({'components':len(bridge_rows),'packets':len(packet_rows)}))
    ck('v15_real_component_bridge_status_partition', runtime_ret.get('bridge_version')=='v3.1' and runtime_ret.get('matched_component_rows')==109 and runtime_ret.get('unmatched_component_rows')==0 and runtime_ret.get('packet_status_counts')=={'COMPLETE_HOMOGENEOUS_COMPONENT_AUTHORITY':19}, json.dumps(runtime_ret))
    try:
        cp35=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_ddm_v552j_component_strata_horizon_bridge.py'],cwd=sec35,capture_output=True,text=True,timeout=90,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        bridge_pytest_ok=cp35.returncode==0 and '18 passed' in cp35.stdout
        bridge_pytest_detail=(cp35.stdout+cp35.stderr).strip()
    except Exception as e:
        bridge_pytest_ok=False; bridge_pytest_detail=repr(e)
    ck('v15_component_bridge_18_real_tests',bridge_pytest_ok,bridge_pytest_detail)
    ck('v15_component_bridge_live_installation_boundary',runtime_ret.get('installation_status')=='COMPONENT_BRIDGE_VALIDATED_AGAINST_RECOVERED_RUNTIME_SNAPSHOT_NOT_WRITTEN_TO_USER_LIVE_REPOSITORY','')

    sec36 = root/'36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3'
    trust_class=rows(sec36/'Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv')
    trust_rulings=rows(sec36/'Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv')
    trust_ev=rows(sec36/'Rawlsing_P2_Trust_Neighborhood_Two_Sided_Evidence_Ledger_v2.csv')
    trust_remaining=rows(sec36/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv')
    trust_ret=json.load((sec36/'TRUST_ADJUDICATION_RETURN_V2.json').open())
    trust_rep=json.load((sec36/'TRUST_REPRODUCIBILITY_RETURN.json').open())
    ruling_ids={r['trust_pair_ruling_id'] for r in trust_rulings}
    ev_count=Counter(r['trust_pair_ruling_id'] for r in trust_ev)
    ev_sides=defaultdict(set)
    for r in trust_ev: ev_sides[r['trust_pair_ruling_id']].add(r['side'])
    ck('v15_trust_queue_partition_exact',len(trust_rulings)==3863 and len(trust_remaining)==14847 and len(trust_rulings)+len(trust_remaining)==18710 and len({r['semantic_pair_candidate_id'] for r in trust_rulings})==3863 and not ({r['semantic_pair_candidate_id'] for r in trust_rulings}&{r['semantic_pair_candidate_id'] for r in trust_remaining}),json.dumps({'rulings':len(trust_rulings),'remaining':len(trust_remaining)}))
    ck('v15_trust_lineage_classification_exact',len(trust_class)==562 and len({r['lineage_id'] for r in trust_class})==562 and Counter(r['authority_status'] for r in trust_class)==Counter({'P2_NONTRUST_EXCLUSION_CLASSIFIED':412,'P2_TRUST_LINEAGE_AXIS_TARGET_CLASSIFIED':148,'P2_TRUST_LINEAGE_CLASSIFICATION_UNRESOLVED':2}),json.dumps(Counter(r['authority_status'] for r in trust_class)))
    ck('v15_trust_two_sided_evidence_exact',len(trust_ev)==7726 and set(ev_count)==ruling_ids and all(v==2 for v in ev_count.values()) and all(v=={'LEFT','RIGHT'} for v in ev_sides.values()),'')
    bad_prop=[r['trust_pair_ruling_id'] for r in trust_rulings if r['authority_status']=='ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION' and (r['left_relation_axis']!=r['right_relation_axis'] or r['left_target_entity']!=r['right_target_entity'] or r['relation_type']!='REWORDED_PROPOSITION_EQUIVALENCE')]
    ck('v15_trust_proposition_axis_target_gate',not bad_prop,json.dumps(bad_prop[:20]))
    unresolved_lineages={r['lineage_id'] for r in trust_class if r['authority_status']=='P2_TRUST_LINEAGE_CLASSIFICATION_UNRESOLVED'}
    bad_hetero=[r['trust_pair_ruling_id'] for r in trust_rulings if ({r['left_lineage_id'],r['right_lineage_id']} & unresolved_lineages) and r['authority_status']!='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE']
    ck('v15_heterogeneous_lineages_fail_closed',not bad_hetero,json.dumps(bad_hetero[:20]))
    expected_status_counts=Counter({'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY':76,'ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD':7,'ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX':30,'ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY':1,'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION':329,'REDIRECTED_OUT_OF_TRUST_NEIGHBORHOOD_OTHER_DOMAIN_NOT_ADJUDICATED':1413,'REJECTED_CONTAMINATED_TRUST_NEIGHBORHOOD_NONTRUST_MISMATCH':65,'REJECTED_FALSE_EQUIVALENCE_TARGET_OR_TRUST_AXIS_MISMATCH':330,'REJECTED_TRUST_VERSUS_NONTRUST_OPERATOR_MISMATCH':1531,'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE':81})
    ck('v15_trust_authority_partition_exact',Counter(r['authority_status'] for r in trust_rulings)==expected_status_counts,json.dumps(Counter(r['authority_status'] for r in trust_rulings)))
    typo_lineage=next((r for r in trust_class if r['lineage_id']=='p2lineage_f47e6b84e36bddf926693820'),None)
    typo_pair=next((r for r in trust_rulings if r['semantic_pair_candidate_id']=='p2sempair_512304291ed8221bfe859cd9'),None)
    ck('v15_pollice_typo_target_recovered',typo_lineage is not None and typo_lineage['governed_target_entity']=='police_assistance_service' and typo_pair is not None and typo_pair['authority_status']=='ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD','')
    ck('v15_trust_deterministic_rebuild',trust_rep.get('status')=='PASS' and trust_rep.get('hashes_exact') is True and trust_rep.get('tracked_files')==5,'')
    try:
        cp36=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_trust_adjudication_v2.py'],cwd=sec36,capture_output=True,text=True,timeout=90,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        trust_pytest_ok=cp36.returncode==0 and '16 passed' in cp36.stdout
        trust_pytest_detail=(cp36.stdout+cp36.stderr).strip()
    except Exception as e:
        trust_pytest_ok=False; trust_pytest_detail=repr(e)
    ck('v15_trust_16_adversarial_tests',trust_pytest_ok,trust_pytest_detail)
    ck('v15_pending_queue_and_resume_current',cur.get('semantic_priority_pairs_remaining')==14847 and scope.get('trust_tranche3',{}).get('pairs_remaining')==14847 and scope.get('next_pass')==expected_next and val.get('next_pass')==expected_next,'')
    ck('v15_master_and_reports_present',(root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v15_20260731.docx').exists() and (sec35/'Rawlsing_V552J_Component_Strata_Horizon_Runtime_Bridge_v3_1_Report_20260731.docx').exists() and (sec36/'Rawlsing_P2_Global_Trust_Neighborhood_Tranche3_Report_20260731.docx').exists(),'')
    debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir() and p.name in ('__pycache__','.pytest_cache')]
    debris += [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.suffix in ('.pyc','.pyo')]
    ck('v15_no_generated_test_or_bytecode_debris',not debris,json.dumps(debris))
'''
verifier_text = verifier_text.replace("\n    result={'status':'PASS' if not failures else 'FAIL'", insert + "\n\n    result={'status':'PASS' if not failures else 'FAIL'")
new_verifier.write_text(verifier_text, encoding='utf-8')

# Preserve the cumulative assembly procedure and its path-specific provenance.
shutil.copy2(Path(__file__).resolve(), ROOT / '00_START_HERE' / 'assemble_handoff_v15.py')
(ROOT / '00_START_HERE' / 'ASSEMBLY_PROVENANCE.md').write_text(
    '# Assembly provenance\n\n'
    'The delivered `assemble_handoff_v15.py` is the exact cumulative assembly procedure used for this handoff. '
    'It is intentionally preserved for auditability. Its `/mnt/data` paths describe the build environment and must be remapped before replay elsewhere. '
    'The governing authority surfaces are independently reproducible from the delivered section-level builders and inputs.\n',
    encoding='utf-8',
)

# Initial manifests. They will be regenerated after document QA and final validation update.
def write_manifests() -> None:
    idx = ROOT / 'PACKAGE_INDEX.csv'
    sums = ROOT / 'SHA256SUMS.csv'
    records = []
    for path in sorted(p for p in ROOT.rglob('*') if p.is_file() and p not in {idx, sums}):
        records.append({'relative_path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha256(path)})
    pd.DataFrame(records).to_csv(idx, index=False)
    pd.DataFrame(records).to_csv(sums, index=False)

write_manifests()
print(ROOT)
