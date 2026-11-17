#!/usr/bin/env python3
"""Generate exact SHA-256 inventory for the C review return."""
import hashlib, json, pathlib, subprocess

ROOT=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
CR=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW'
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def rec(p):
    q=pathlib.Path(p).resolve()
    try: label=str(q.relative_to(ROOT))
    except ValueError: label=str(q)
    return {'path':label,'bytes':q.stat().st_size,'sha256':sha(q)}

files={
 'target_commit': subprocess.run(['git','-C',str(ROOT),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
 'target_branch': subprocess.run(['git','-C',str(ROOT),'branch','--show-current'],capture_output=True,text=True).stdout.strip(),
 'original_zip': rec('/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'),
 'repaired_zip': rec(INT/'REPAIRED_PACKAGE.zip'),
 'candidate_manifest': rec(INT/'MANIFEST.json'),
 'source_authentication': rec(INT/'SOURCE_AUTHENTICATION.json'),
 'test_transcript': rec(INT/'TEST_TRANSCRIPT.json'),
 'inventory': rec(INT/'EVIDENCE/SOURCE_IDENTITY_INVENTORY.json'),
 'frame': rec(INT/'EVIDENCE/FRAME.json'),
 'decision': rec(INT/'EVIDENCE/DECISION.json'),
 'c_packet': rec(INT/'EVIDENCE/C.json'),
 'boundary_contracts_fixture': rec(INT/'EVIDENCE/BOUNDARY_CONTRACTS.json'),
 'release_register': rec(INT/'EVIDENCE/RELEASE_REGISTER.json'),
 'tools_r7_integrated': rec(INT/'PACKAGE/ANVIL_R7/tools/r7_integrated.py') if (INT/'PACKAGE/ANVIL_R7/tools/r7_integrated.py').exists() else rec(INT/'REPAIRED_PACKAGE/ANVIL_R7/tools/r7_integrated.py') if (INT/'REPAIRED_PACKAGE/ANVIL_R7/tools/r7_integrated.py').exists() else None,
 'built_manifest': rec(INT/'BUILT/MANIFEST.json'),
 'built_identity_dispositions': rec(INT/'BUILT/IDENTITY_DISPOSITIONS.tsv'),
 'built_boundary_map': rec(INT/'BUILT/BOUNDARY_CONTRACT_MAP.json'),
 'built_typed_graph': rec(INT/'BUILT/TYPED_GRAPH.json'),
 'built_evidence_index': rec(INT/'BUILT/EVIDENCE_INDEX.jsonl'),
 'built_builder_handoff': rec(INT/'BUILT/BUILDER_HANDOFF.json'),
 'package_tools': {n: rec(INT/'REPAIRED_PACKAGE/ANVIL_R7/tools'/n) for n in (
     'r7_integrated.py','r7_inventory.py','r7_build.py','r7_stage.py',
     'test_integrated_strict.py','test_r7_integrated.py') if (INT/'REPAIRED_PACKAGE/ANVIL_R7/tools'/n).exists()},
 'source_fixture_pin_manifest': rec(INT/'EVIDENCE/SOURCE_118/PIN_MANIFEST.json') if (INT/'EVIDENCE/SOURCE_118/PIN_MANIFEST.json').exists() else None,
 'review_verdict': rec(CR/'REVIEW_VERDICT.json') if (CR/'REVIEW_VERDICT.json').exists() else None,
 'grok_proof': rec(CR/'GROK_PROOF.md') if (CR/'GROK_PROOF.md').exists() else None,
 'readable_verdict': rec(CR/'VERDICT.md') if (CR/'VERDICT.md').exists() else None,
 'return': rec(CR/'RETURN.md') if (CR/'RETURN.md').exists() else None,
 'raw_commands': rec(CR/'RAW_COMMANDS.md') if (CR/'RAW_COMMANDS.md').exists() else None,
 'test_transcript': rec(CR/'TEST_TRANSCRIPT.json') if (CR/'TEST_TRANSCRIPT.json').exists() else None,
}
# source replay anchors
sr=json.load(open(CR/'WITNESS/W0_SOURCE_REPLAY/source_replay.json'))
files['source_replay']=rec(CR/'WITNESS/W0_SOURCE_REPLAY/source_replay.json')
files['source_files']=sr['git_files']
files['source_replay_counts']=sr['counts_actual']
files['source_replay_exact_rows_ok']=sr['exact_rows_ok']
# witness/log hashes
wlogs={}
for p in sorted((CR/'WITNESS').glob('W*/*.json')):
    wlogs[str(p.relative_to(CR))]=rec(p)
for p in sorted((CR/'LOGS').glob('*')):
    if p.name == 'make_exact_sha.log':
        continue
    wlogs[str(p.relative_to(CR))]=rec(p)
files['witness_and_logs']=wlogs
files['temp_readme']=rec(CR/'TEMP/README_REPRODUCE.md')
out=CR/'EXACT_SHA256.json'
out.write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'written':str(out),'target_commit':files['target_commit'],'repaired_zip':files['repaired_zip'],'source_exact_rows_ok':files['source_replay_exact_rows_ok'],'witness_logs':len(wlogs)},indent=2))
