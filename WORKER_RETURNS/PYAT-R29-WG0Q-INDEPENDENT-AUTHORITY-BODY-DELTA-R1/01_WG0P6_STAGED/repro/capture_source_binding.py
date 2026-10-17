"""Export actual owner-qualified bindings and digest records; never owner keys."""
import hashlib,json
from pathlib import Path
from phase_b_support_v1 import plan,w
R=Path(__file__).resolve().parents[1]
p=plan();journal=p.fixture_owner._issued();source=json.loads(p.source_material)
rows=[]
for tag,release in p.releases.items():
 native=p.repository.resolve_release_exact(release.release_ref)
 snapshots=[ref.as_dict() for ref in native.replay_manifest.closure_refs if ref.kind=='SOURCE_SNAPSHOT']
 rows.append(dict(tag=tag,release_ref=release.release_ref.as_dict(),source_edition=release.source_edition,
                  view_source_snapshot=release.source_artifact_ref.as_dict(),
                  sealed_native_source_artifact=native.source_artifact_ref.as_dict(),
                  sealed_native_replay_snapshots=snapshots,
                  registered_material_digest=journal['native_sources'][release.release_ref.key],
                  actual_material_digest=w.digest(source[tag]),binding=source[tag]['source_view_binding']))
 assert rows[-1]['registered_material_digest']==rows[-1]['actual_material_digest']
 assert snapshots==[release.source_artifact_ref.as_dict()]
contract_hash=hashlib.sha256(p.contract).hexdigest()
registered=journal['plans'][contract_hash]
assert registered['source_material']==hashlib.sha256(p.source_material).hexdigest()
record=dict(schema='WG0P6_SOURCE_VIEW_TO_OWNER_QUALIFIED_C11_ARTIFACT@1',
            version=w.VERSION,sourcefree_only=True,source_bindings=rows,
            registered_plan_record=registered,contract_sha256=contract_hash,
            plan_source_material_sha256=hashlib.sha256(p.source_material).hexdigest(),
            manifest_hash=p.manifest.manifest_hash,manifest_units=len(p.manifest.units),
            original_frontier_counts=p.expected_frontier_counts,
            immutable_bound_descriptor_fields=list(json.loads(p.contract)['bindings'][next(iter(p.units_by_op))]['descriptor']),
            guarantee='Exact C11 replay-closure snapshot ref plus artifact hash, then TEST_ONLY owner material and compiled-plan registration; rechecked at compile/I03/consumer/restore boundaries.',
            trust_boundary='Trusted local fixture owner/code/key only; no original-source or external distributed issuer rights',
            candidate_code_sha256=hashlib.sha256(Path(w.__file__).read_bytes()).hexdigest())
(R/'01_SOURCE_SNAPSHOT_BINDING.json').write_text(json.dumps(record,indent=2)+'\n')
print('ACTUAL_SOURCE_BINDINGS_EXPORTED',len(rows))
