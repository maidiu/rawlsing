from __future__ import annotations

import csv
import hashlib
import os
import zipfile
from pathlib import Path


ROOT_NAME = "Rawlsing_J_Family_Authority_Strategy_Handoff_v29_20260801"
TARGETS = [
    f"{ROOT_NAME}/35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/generated_question_semantic_hierarchy/crosssurvey__Latinobarómetro_1995_BR_question_semantic_hierarchy.csv",
    f"{ROOT_NAME}/35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/runtime_reproducibility_inputs/v551_atoms/crosssurvey/Latinobarómetro_1995_BR/relation_evidence_atoms.csv",
]
MOJIBAKE = "Latinobar├│metro"


def test_v29_zip_unicode_paths_and_manifest_reconcile():
    zip_path = Path(os.environ["RAWLSING_V29_ZIP"])
    build_root = Path(os.environ["RAWLSING_V29_BUILD_ROOT"])
    manifest = list(csv.DictReader((build_root / "PACKAGE_INDEX.csv").open(encoding="utf-8")))
    with zipfile.ZipFile(zip_path) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        names = {info.filename for info in infos}
        by_name = {info.filename: info for info in infos}

    assert not any(MOJIBAKE in name for name in names)
    for target in TARGETS:
        assert target in names
        assert by_name[target].flag_bits & 0x800

    manifest_set = {f"{ROOT_NAME}/{row['relative_path']}" for row in manifest}
    zip_payload_set = names - {f"{ROOT_NAME}/PACKAGE_INDEX.csv", f"{ROOT_NAME}/SHA256SUMS.csv"}
    assert manifest_set == zip_payload_set

    for row in manifest:
        path = build_root / row["relative_path"]
        assert path.stat().st_size == int(row["bytes"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
