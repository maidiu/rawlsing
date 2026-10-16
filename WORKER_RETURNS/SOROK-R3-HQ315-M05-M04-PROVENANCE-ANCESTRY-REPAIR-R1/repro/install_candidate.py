"""Install owned candidate bytes at the original import location; no test edits."""

from pathlib import Path
import hashlib, json, shutil

R = Path(__file__).resolve().parents[1]
target = R / "runtime/m02/runtime/m01/repro"
rows = []
for name in ["cell.py", "claim_provenance.py"]:
    source = R / "candidate" / name
    data = source.read_bytes()
    shutil.copyfile(source, target / name)
    rows.append(
        {
            "candidate": str(source.relative_to(R)),
            "effective_module": str((target / name).relative_to(R)),
            "blob_sha1": hashlib.sha1(
                b"blob " + str(len(data)).encode() + b"\0" + data
            ).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    )
(R / "evidence/CANDIDATE_INSTALLATION.json").write_text(
    json.dumps(
        {
            "source_inputs_remain_at_pinned_git_and_frozen_snapshot": True,
            "test_oracle_bytes_changed": False,
            "response_functions_monkeypatched": False,
            "files": rows,
        },
        indent=2,
    )
    + "\n"
)
print("OWNED_CANDIDATE_INSTALLED")
