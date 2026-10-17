"""Fresh interpreter attempts a foreign source-view against a real signed checkpoint."""
import copy,json,sys
from pathlib import Path
from dataclasses import replace
from phase_b_support_v1 import w,plan,profile_calls
folder=Path(sys.argv[1]);owner=w.FixtureOwner(folder/'owner')
releases=w.build_all_releases(fixture_owner=owner);p=plan(releases=releases)
checkpoint=w.ColdCheckpoint.from_json((folder/'checkpoint.json').read_text(),fixture_owner=owner)
mapping=dict(p.releases);mapping['REL-A-W1']=replace(mapping['REL-A-W1'],source_artifact_ref=mapping['REL-A-W2'].source_artifact_ref)
bad=replace(p,releases=mapping);before=copy.deepcopy(owner._issued());custody=bad.fact_custody.snapshot();calls=[];error=None
sys.setprofile(profile_calls(calls))
try:w.restore_from_checkpoint(checkpoint,bad)
except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
finally:sys.setprofile(None)
record=dict(pid=w.os.getpid(),same_original_manifest=checkpoint.manifest_hash==p.manifest.manifest_hash,
            manifest_units=len(p.manifest.units),checkpoint_original_receipts=len(checkpoint.prior_receipts),
            error=error,new_I03_calls=sum(c['name']=='execute_empirical_query' for c in calls),
            owner_journal_unchanged=owner._issued()==before,custody_unchanged=bad.fact_custody.snapshot()==custody,
            restored_receipts=len(bad.prior_receipts),candidate_sha256=w.hashlib.sha256(Path(w.__file__).read_bytes()).hexdigest())
(folder/'result.json').write_text(json.dumps(record,indent=2)+'\n')
assert error and error['type']=='IdentityError' and record['new_I03_calls']==0
assert record['same_original_manifest'] and record['manifest_units']==3
assert record['owner_journal_unchanged'] and record['custody_unchanged'] and record['restored_receipts']==0
