"""Restore the parent metadata omitted when staging only the old GF1 court."""
import hashlib
import subprocess
from pathlib import Path

ORIGINAL = '9f4a23cef1482e0a81afb1e7a65df90879931465'
RETURN = 'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
REQUIRED_PARENT_FILES = (
    '01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json',
    'pinned_refs/PV3N_01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json',
)


def stage_gf1i_parent_metadata(repo: Path, destination: Path) -> list[dict]:
    rows = []
    for relative in REQUIRED_PARENT_FILES:
        source = RETURN + '/' + relative
        data = subprocess.check_output(['git', 'show', ORIGINAL + ':' + source], cwd=repo)
        target = destination / relative
        existed = target.is_file()
        if existed:
            if target.read_bytes() != data:
                raise ValueError('STAGED_PARENT_METADATA_DRIFT:' + str(target))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        actual = subprocess.check_output(['git', 'rev-parse', ORIGINAL + ':' + source], cwd=repo, text=True).strip()
        assert digest == actual
        rows.append(dict(commit=ORIGINAL, source_path=source, destination=str(target),
                         already_present=existed, git_blob_sha1=digest,
                         sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
    return rows
