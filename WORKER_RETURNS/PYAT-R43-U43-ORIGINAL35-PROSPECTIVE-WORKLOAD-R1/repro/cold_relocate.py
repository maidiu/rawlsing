"""Stage a fresh sourcefree closure with no .git and no warm owner/checkpoint."""
from pathlib import Path
import hashlib,json,shutil,sys

R=Path(__file__).resolve().parents[1];WT=R.parents[1]
sys.path.insert(0,str(R/"repro"))
from prepare_replay import repair


def main():
    dest=WT/"LOCAL_COURTS/u43-cold"
    if dest.exists():raise ValueError("REFUSE_OVERWRITE_COLD_EVIDENCE")
    relative=R.relative_to(WT)
    shutil.copytree(WT/"rawlsing_next",dest/"rawlsing_next",ignore=shutil.ignore_patterns("__pycache__",".pytest_cache"))
    shutil.copytree(WT/"CROSS_HQ_CONTROL_ROOM",dest/"CROSS_HQ_CONTROL_ROOM",ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(R,dest/relative,ignore=shutil.ignore_patterns("__pycache__",".pytest_cache"))
    baseline=WT/"LOCAL_COURTS/u43-baseline"
    review=dest/"LOCAL_COURTS/u43-repaired"
    def ignore(directory,names):
        return [n for n in names if n in {"__pycache__",".pytest_cache","runtime","controls_v1_final"}]
    shutil.copytree(baseline,review,ignore=ignore)
    path=review/"runtime_phase_b/candidate/repro/wg0p4_workload.py"
    path.write_text(repair(path.read_text()))
    cutpath=review/"observations/phase_b/candidate_read_cut.json"
    cut=json.loads(cutpath.read_text())
    for row in cut["source_rows"]:
        data=(review/row["staged_path"]).read_bytes()
        if row["staged_path"].endswith("/repro/wg0p4_workload.py"):
            row["sha256"]=hashlib.sha256(data).hexdigest()
        elif hashlib.sha256(data).hexdigest()!=row["sha256"]:
            raise ValueError("COLD_INHERITED_PREIMAGE_CHANGED:"+row["staged_path"])
    cutpath.write_text(json.dumps(cut,indent=2)+"\n")
    expected={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in [
        "source_wave_item_operation_frontier.jsonl.gz","original35_wave_execution_manifest.json",
        "original35_issuer_decision_packets.json","currently_permitted_native_manifests.json",
        "evidence/native_sourcefree_execution.json"]}
    (dest/relative/"evidence/cold_expected.json").write_text(json.dumps(expected,indent=2)+"\n")
    assert not (dest/".git").exists()
    print(json.dumps(dict(cold_root=str(dest),git_present=False,expected=expected),sort_keys=True))


if __name__=="__main__":main()
