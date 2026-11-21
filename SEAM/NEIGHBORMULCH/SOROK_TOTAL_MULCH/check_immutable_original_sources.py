#!/usr/bin/env python3
"""Source-based SOROK TOTAL bank verification from FIVE immutable public blobs.

Does not use a repository-wide code scan, another feature owner, credentials,
private data, or model judgments. Public HTTP is needed (GitHub Actions).
A green court proves only original-source extraction/identity, not scientific
validity, code parity of later PRs, or protected adoption.
"""
import hashlib
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
bank = json.loads((ROOT / "01_MACHINE_SOURCE_UNION_757_ROWS.json").read_text())
raw = {}

for source in bank["source_files"]:
    url = (
        "https://raw.githubusercontent.com/maidiu/rawlsing/"
        + source["commit_or_ref"] + "/" + source["path"]
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "neighbormulch-total-source-court"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read()
    actual_sha = hashlib.sha1(
        ("blob " + str(len(content)) + "\x00").encode() + content
    ).hexdigest()
    assert actual_sha == source["blob_sha"], (
        source["key"], "ORIGINAL_GIT_BLOB_CHANGED", actual_sha
    )
    raw[source["key"]] = content.decode("utf-8")
    print("ORIGINAL_BLOB_PASS", source["key"], actual_sha, len(content), flush=True)

o = json.loads(raw["oindex"])["rows"]
expected_o = bank["original_function_and_source_registry"]
assert len(o) == len(expected_o) == 144
for orig, saved in zip(o, expected_o):
    assert orig["id"] == saved["id"]
    assert orig["title"] == saved["title"]
    assert orig["status"] == saved["original_status"]
    assert orig["owner"] == saved["owner"]
    assert (orig.get("first_consumer_required") or orig.get("first_consumer")) == saved["first_consumer_required"]
print("ORIGINAL_OINDEX_144_EXACT_ROW_FIELDS_PASS", flush=True)

h = []
for line in raw["ideation"].splitlines():
    if not line.startswith("| **H"):
        continue
    m = re.match(
        r"^\|\s*\*\*(H\d{3})\*\*\s*[—–-]\s*(.*?)\s*\|\s*\x60([^\x60]+)\x60\s*\|",
        line,
    )
    assert m, ("UNPARSED_H_IDENTITY", line[:160])
    h.append((m.group(1), m.group(2), m.group(3)))
assert len(h) == 190
for orig, saved in zip(h, bank["original_ideation_H001_H190"]):
    assert orig == (saved["id"], saved["claim"], saved["original_disposition"])
print("ORIGINAL_H190_CLAIMS_AND_GRADES_PASS", flush=True)

q = []
for line in raw["questions"].splitlines():
    if not line.startswith("| [Q-"):
        continue
    m = re.match(
        r"^\|\s*\[(Q-[^\]]+)\]\([^)]+\)\s*\|\s*(S\d+)\s*\|\s*\x60([^\x60]+)\x60\s*\|\s*\x60([^\x60]+)\x60\s*\|\s*(.+?)\s*\|\s*$",
        line,
    )
    assert m, ("UNPARSED_Q_IDENTITY", line[:160])
    q.append(tuple(m.groups()))
assert len(q) == 123
for original, saved in zip(q, bank["original_product_questions_Q"]):
    assert original == (
        saved["id"], saved["workstream"], saved["original_closure"],
        saved["original_blocking_stage"], saved["original_question"],
    )
print("ORIGINAL_Q123_QUESTIONS_AND_CLOSURES_PASS", flush=True)

sources = [json.loads(line) for line in raw["sorokuda"].splitlines() if line.strip()]
assert len(sources) == 300
for original, saved in zip(sources, bank["sorokuda_source_and_alternative_versions"]):
    for k in ("id", "kind", "source_cut", "path", "blob", "url", "functional_cluster", "summary", "evidence"):
        assert original.get(k) == saved.get(k), ("SOROKUDA_ROW_CHANGED", saved["id"], k)
print("ORIGINAL_SOROKUDA_300_EXACT_SOURCE_FIELDS_PASS", flush=True)

workstreams = []
for line in raw["workstreams"].splitlines():
    m = re.match(r"^##\s*(S\d+)\s*[—-]\s*(.*)$", line)
    if m:
        workstreams.append((m.group(1), m.group(2)))
assert len(workstreams) == 17
for src, saved in zip(workstreams, bank["original_workstreams_S0_S16"]):
    assert src == (saved["id"], saved["original_title"])
print("ORIGINAL_S0_S16_HEADING_IDENTITIES_PASS", flush=True)
print("IMMUTABLE_GITHUB_757_SOURCE_ROWS_VERIFIED_FROM_ORIGINAL_BLOBS")
print("GRADE: DOCUMENTARY SOURCE INTEGRITY ONLY; NO NATIVE SCIENCE/ACTOR/ALPHA/PROTECTED RECEIVING")
