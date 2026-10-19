"""WG0RI independent helpers: exact payload, shard, manifest, O07 boundary.

The author's recovery/reader modules are the object under test; every expected
byte, ordinal, hash and count here is independently decoded and asserted.
"""
from __future__ import annotations

import base64
import collections
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parent
AUTHOR = R / "stage/WORKER_RETURNS/PYAT-R37-WG0R-CURRENT35-FRONTIER-SUCCESSION-R1"
PACK_SHA = "64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98"
P2_SHA = "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"
ORIGINAL_GIT_COMMIT = "b44596d880425f6984f208bfa14daee2f15d3f90"
ORIGINAL_GIT_BLOB = "c93945d158198871f5cc6692a6bed25aeef44028"
SHARD_GIT_BLOB = "3a9b5bde2fc479c6fc10280561fe715686e39dd4"
ORIGINAL_CSV_SHA = "c1d5a9a9b2905f7ed783a21f43eeef91bc173d6e5e077751a67f7025408ee7ad"
ORIGINAL_BYTES = 24972
ORIGINAL_DECODED_BYTES = 18387
ORIGINAL_DECODED_SHA = "3bee6f0ec5cae74c112f2896b517b23ab7e880c9400bf019d1df6d0b3157edee"
ORIGINAL_RESERVED = 2114
SHARD_SHA = "e9fff20e06fabbd90fff6552f73811e93caeb8c0d998cb96add5d472d8892a67"
SHARD_ROWS = 1000
MANIFEST_PART000_SHA = "e2f5f13ade6187412dbe11a3c98b0e8a97ef967f45d8b583d157da5eaf12f140"
CLASS_ORDER = ["SEM", "TOP", "POS", "END", "CTX", "SCX", "ADM", "REJ", "CPC", "BLK"]
EXPECTED_CLASS_COUNTS = {"SEM": 4681, "TOP": 3667, "POS": 2904, "END": 2113,
                         "CTX": 1675, "SCX": 1506, "ADM": 1026, "REJ": 454,
                         "CPC": 183, "BLK": 67}
EXPECTED_HARD_FAIL = 10418
EXPECTED_ROUTE = 4447
EXPECTED_P10_UNITS = 65354
EXPECTED_P10_HELDS = 76
PRIOR_WG0I = "44eac9021db23267448a6fc151e6bbe8374a868f"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def original_path() -> Path:
    return next((AUTHOR / "sources/repair_original_git").rglob(
        "CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv"))


def shard_path() -> Path:
    return next((AUTHOR / "sources/repair_original_git").rglob("part-000.csv"))


def manifest_path() -> Path:
    return next((AUTHOR / "sources/repair_original_manifest").rglob(
        "CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv"))


def repaired_path() -> Path:
    return AUTHOR / "sources/recovered_disposition/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv"


def p2_path() -> Path:
    return AUTHOR / "sources/local_archive/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv"


def o07_path() -> Path:
    return AUTHOR / "sources/recovered_disposition/o07_recall_projection.csv"


def custody_path() -> Path:
    return AUTHOR / "evidence/disposition_recovery_input_custody.json"


def pack(path: Path) -> tuple[dict, bytes, dict]:
    rows = list(csv.DictReader(Path(path).open()))
    assert len(rows) == 1, len(rows)
    row = rows[0]
    raw = base64.b64decode("".join(row["payload_b64_" + str(i)] for i in range(4)),
                           validate=True)
    codes = dict(x.split("=") for x in row["use_code_map"].split(";"))
    return row, raw, codes


def bit_counts(payload: bytes, codes: dict) -> dict:
    classes = collections.Counter(codes[str(b & 15)] for b in payload)
    return {"classes": dict(classes),
            "hard_fail": sum(bool(b & 16) for b in payload),
            "route": sum(bool(b & 32) for b in payload),
            "reserved": sum(bool(b & 192) for b in payload),
            "use_out_of_range": sum(str(b & 15) not in codes for b in payload)}


def shard_rows() -> list[dict]:
    return list(csv.DictReader(shard_path().open()))


def shard_mismatches(payload: bytes, codes: dict) -> tuple[int, int]:
    reverse = {v: int(k) for k, v in codes.items()}
    bad = 0
    for row in shard_rows():
        byte = reverse[row["use"]] + 16 * (row["hard_fail"] == "Y") + \
            32 * (row["route_predicate_required"] == "Y")
        if payload[int(row["p2_row_ordinal"])] != byte:
            bad += 1
    return len(shard_rows()), bad


def manifest_rows() -> list[dict]:
    return list(csv.DictReader(manifest_path().open()))


def p2_rows() -> list[dict]:
    data = p2_path().read_bytes()
    assert sha(data) == P2_SHA
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def original_decode() -> tuple[dict, bytes, dict]:
    return pack(original_path())


def author_modules():
    if str(AUTHOR) not in sys.path:
        sys.path.insert(0, str(AUTHOR))
    import account_current35  # noqa: F401
    import recover_disposition_payload  # noqa: F401
    return account_current35, recover_disposition_payload


def junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    return {k: sum(int(s.attrib.get(k, 0)) for s in suites)
            for k in ("tests", "failures", "errors", "skipped")}


def make_pack_variant(tmp: Path, mutation: str, *, row: dict | None = None,
                      codes: dict | None = None, payload: bytes | None = None) -> Path:
    """Write a one-row P2_ORDINAL_BYTEPACK CSV with one controlled mutation."""
    base = dict(row or next(csv.DictReader(repaired_path().open())))
    codes = dict(codes or dict(x.split("=") for x in base["use_code_map"].split(";")))
    payload = payload if payload is not None else base64.b64decode(
        "".join(base["payload_b64_" + str(i)] for i in range(4)), validate=True)

    def set_payload(raw: bytes):
        b64 = base64.b64encode(raw).decode()
        n = len(b64)
        cuts = [0, n // 4, n // 2, (3 * n) // 4, n]
        chunks = [b64[cuts[i]:cuts[i + 1]] for i in range(4)]
        assert "".join(chunks) == b64
        for i in range(4):
            base["payload_b64_" + str(i)] = chunks[i]

    if mutation == "payload_byte":
        raw = bytearray(payload)
        raw[0] ^= 0x01
        set_payload(bytes(raw))
    elif mutation == "header_sha":
        base["payload_sha256"] = "0" * 64
    elif mutation == "p2_sha":
        base["p2_sha256"] = "0" * 64
    elif mutation == "code_map":
        base["use_code_map"] = base["use_code_map"].replace("0=SEM", "0=ADM")
    elif mutation == "byte_length":
        base["payload_bytes"] = str(len(payload) - 1)
    elif mutation == "reserved_bit":
        raw = bytearray(payload)
        raw[0] |= 0x40
        set_payload(bytes(raw))
    elif mutation == "use_code_15":
        raw = bytearray(payload)
        raw[0] = (raw[0] & 0xF0) | 0x0F
        set_payload(bytes(raw))
    elif mutation == "reserved_bit_rehashed":
        raw = bytearray(payload)
        raw[0] |= 0x40
        set_payload(bytes(raw))
        base["payload_sha256"] = sha(bytes(raw))
    elif mutation == "use_code_15_rehashed":
        raw = bytearray(payload)
        raw[0] = (raw[0] & 0xF0) | 0x0F
        set_payload(bytes(raw))
        base["payload_sha256"] = sha(bytes(raw))
    elif mutation == "truncate":
        set_payload(payload[:-1])
    elif mutation == "duplicate_chunk":
        base["payload_b64_1"] = base["payload_b64_0"]
    elif mutation == "bad_base64":
        base["payload_b64_0"] = "!!!" + base["payload_b64_0"][3:]
    elif mutation == "duplicate_row":
        pass
    else:
        raise ValueError(mutation)
    path = tmp / ("hostile_" + mutation + ".csv")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, list(base), lineterminator="\n")
        writer.writeheader()
        writer.writerow(base)
        if mutation == "duplicate_row":
            writer.writerow(base)
    return path


def o07_rows() -> list[dict]:
    return list(csv.DictReader(o07_path().open()))


def o07_counts() -> dict:
    return dict(collections.Counter(
        r["current_o07_measurement_use_class_DIAGNOSTIC_ONLY"] for r in o07_rows()))


def make_recovery_copy(tmp: Path) -> Path:
    """Copy the minimal recovery closure so mutations cannot touch author bytes."""
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "sources").mkdir(parents=True)
    (tmp / "evidence").mkdir()
    for name in ("recover_disposition_payload.py", "account_current35.py"):
        shutil.copy2(AUTHOR / name, tmp / name)
    shutil.copytree(AUTHOR / "sources/recovered_disposition",
                    tmp / "sources/recovered_disposition")
    shutil.copytree(AUTHOR / "sources/local_archive", tmp / "sources/local_archive")
    shutil.copy2(custody_path(), tmp / "evidence/disposition_recovery_input_custody.json")
    return tmp


def run_recovery(root: Path) -> dict:
    code = (
        "import json,hashlib,sys; sys.path.insert(0, %r);"
        "import recover_disposition_payload as r;"
        "d=r.recover();"
        "print(json.dumps({'ok':True,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}))"
        % str(root)
    )
    proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=root,
                          text=True, capture_output=True)
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    try:
        payload = json.loads(line) if line else {}
    except json.JSONDecodeError:
        payload = {}
    return {"exit": proc.returncode, "payload": payload,
            "stderr": proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""}
