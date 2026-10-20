"""06B documentary references + 08 authoritative CLOSED_35 roster."""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

DOC_PATTERNS = [
    ("LiTS", re.compile(r"\bLiTS\b|\bLITS1?\b", re.I)),
    ("q301", re.compile(r"\bq301\b", re.I)),
    ("ONE_CANARY", re.compile(r"ONE[_ -]?CANARY|one-canary", re.I)),
    ("universal", re.compile(r"universal", re.I)),
    ("CLOSED_35", re.compile(r"CLOSED[_ -]?35|closed35|all35|35[- ]wave", re.I)),
    ("canary", re.compile(r"canary", re.I)),
    ("N11_1890", re.compile(r"1890|1,890", re.I)),
]
ROSTER = "data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv"
F_GATES = "F1 source-native read; F2 empirical identity; F3 finite operation/workload; F4 learned/empirical composition; F5 structural/FF relation; F6 partial-bound transport; F7 observed temporal pair; F8 selected-world consumer"


def doc_scan():
    rows = []
    tree = C.ls_tree()
    blobs = C.blob_reader if hasattr(C, "blob_reader") else None
    import subprocess
    md = [r for r in tree if r["path"].endswith(".md")]
    sizes = C.blob_sizes([r["blob"] for r in md])
    payload = "".join(r["blob"] + "\n" for r in md).encode()
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=str(C.ROOT),
                          input=payload, capture_output=True, check=True)
    data, pos, raw = {}, 0, proc.stdout
    while pos < len(raw):
        end = raw.index(b"\n", pos)
        header = raw[pos:end].decode().split()
        pos = end + 1
        if len(header) != 3:
            continue
        sha, _, size = header
        data[sha] = raw[pos:pos + int(size)]
        pos += int(size) + 1
    for row in md:
        blob = data.get(row["blob"])
        if blob is None:
            continue
        text = blob.decode("utf-8", "replace")
        counts = {name: len(regex.findall(text)) for name, regex in DOC_PATTERNS}
        total = sum(counts.values())
        if not total:
            continue
        rows.append((row["path"], row["blob"], sizes.get(row["blob"], -1),
                     counts["LiTS"], counts["q301"], counts["ONE_CANARY"],
                     counts["universal"], counts["CLOSED_35"], counts["canary"],
                     counts["N11_1890"], total,
                     "DOCUMENTARY_MENTION_NOT_CODE_LEAKAGE"))
    rows.sort(key=lambda r: (-r[-2], r[0]))
    digest = C.write_tsv(
        C.OUT / "06B_DOCUMENT_REFERENCE_COUNTS.tsv",
        ("path", "blob", "size", "lits", "q301", "one_canary", "universal",
         "closed35", "canary", "n11_1890", "total", "classification"),
        rows)
    return rows, digest


def roster():
    path = C.ROOT / ROSTER
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        all_rows = list(reader)
    active = [r for r in all_rows
              if (r.get("authority_status") or "").strip() != "EXCLUDED_INACTIVE_WAVE"]
    pairs = {}
    for row in active:
        key = (row["source_family"].strip(), row["canonical_wave"].strip())
        pairs.setdefault(key, []).append(row)
    ordered = sorted(pairs)
    assert len(ordered) == 35, (len(ordered), ordered)
    assert ("Asian Barometer", "W6") not in ordered
    # source-family literal presence in sealed production code (bounded index)
    prod_text = {}
    for row in C.ls_tree():
        p = row["path"]
        if not p.startswith("rawlsing_next/") or not p.endswith(".py"):
            continue
        data = C.read_blob(row["blob"]).decode("utf-8", "replace")
        prod_text[p] = data
    rows = []
    for source, wave in ordered:
        members = pairs[(source, wave)]
        countries = sorted({m.get("country_code_scope", "") for m in members if m.get("country_code_scope")})
        statuses = sorted({m.get("authority_status", "") for m in members})
        reviews = sorted({m.get("review_status", "") for m in members})
        directional = sum(1 for m in members if (m.get("relation_use_status") or "") == "GOVERNED_DIRECTIONAL")
        adapter_hits = [p for p, text in prod_text.items() if source.lower() in text.lower()]
        rows.append((source, wave, ",".join(countries) or "UNKNOWN",
                     "UNKNOWN_IN_AUTHORITY_ROW",
                     statuses[0] if len(statuses) == 1 else "|".join(statuses),
                     reviews[0] if len(reviews) == 1 else "|".join(reviews),
                     f"{len(members)} authority rows; directional={directional}; question/var fields present",
                     "UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN",
                     "NOT_ISSUED / NULL",
                     ("EXPLICIT_LOCAL_ADAPTER_PRESENT:" + ";".join(adapter_hits[:3])) if adapter_hits
                     else "NO_GENERIC_PLANNER_EDGE_FOUND_IN_BOUNDED_SEALED_SCAN",
                     F_GATES,
                     "F1 source-native generic read not proved; F2-F4 require source-indexed operation/workload; "
                     "F5 only retained context for some sources; F6 target/transport unissued; "
                     "F7 observed comparable pair unissued; F8 TEST_ONLY consumer only",
                     "NONE_FOUND_IN_SEALED_INDEX"))
    header = ("source_family", "canonical_wave", "country_scope", "format",
              "authority_status", "review_status", "semantics_routing_role_weight_evidence",
              "source_permission_runtime", "known_original_U_E_pre_scope",
              "generic_workload_planner_status", "expected_F1_F8_responsibilities",
              "precise_blocked_reason", "historical_sourcepositive_receipts")
    digest = C.write_tsv(C.OUT / "08_CLOSED35_UNIVERSAL_EXECUTION_COVERAGE.tsv",
                         header, rows)
    return rows, digest, dict(total_authority_rows=len(all_rows),
                              active_rows=sum(len(v) for v in pairs.values()),
                              unique_waves=len(ordered),
                              excluded_rows=len(all_rows) - sum(len(v) for v in pairs.values()))


def main():
    docs, docs_hash = doc_scan()
    rows, roster_hash, meta = roster()
    C.write_json(C.EVID / "docs_and_roster_receipt.json",
                 dict(schema="R53_U53F_DOCS_AND_ROSTER_RECEIPT@1",
                      document_rows=len(docs), document_tsv_sha256=docs_hash,
                      roster_rows=len(rows), roster_tsv_sha256=roster_hash,
                      roster_meta=meta,
                      note="35 identities exactly; F6/F7 cross-family pairs and F8 service are not single-wave fields; "
                           "N11 1,890 cells are accounting, not query count; no source right inferred."))
    print(json.dumps(dict(documents=len(docs), roster=len(rows), meta=meta,
                          roster_sha=roster_hash), indent=1))


if __name__ == "__main__":
    main()
