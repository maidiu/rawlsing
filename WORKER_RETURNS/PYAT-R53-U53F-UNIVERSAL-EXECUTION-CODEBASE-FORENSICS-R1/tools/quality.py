"""Independent pre/post-flight quality law checks a–i."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    checks = {}
    scope = json.loads((C.OUT / "01_REPOSITORY_SCOPE_AND_COMPLETENESS.json").read_text())
    census_rows = (C.OUT / "02_ALL_PINNED_TREE_FILES.tsv").read_text().splitlines()[1:]
    checks["a_tree_census_count"] = dict(
        tracked=scope["census"]["tracked_file_count"], tsv_rows=len(census_rows),
        pass_=(scope["census"]["tracked_file_count"] == len(census_rows) == 7615))
    refs = json.loads((C.EVID / "ref_inventory.json").read_text())
    shard_rows = 0
    for shard in C.OUT.glob("03_MATERIAL_BRANCH_DIFF_FILE_BLOBS*.tsv"):
        shard_rows += len(shard.read_text().splitlines()) - 1
    checks["b_refs_ledger"] = dict(
        observed_refs=scope["refs"]["counts"], material_refs=refs["material_refs"],
        diff_rows_inventory=refs["diff_rows"], diff_rows_tsv=shard_rows,
        pass_=(refs["diff_rows"] == shard_rows))
    records = [json.loads(line) for line in
               (C.OUT / "04_UNIVERSAL_PRODUCER_CONSUMER_GRAPH.jsonl").read_text().splitlines()
               if line.strip()]
    edges = [record for record in records if record.get("record_type") == "edge"]
    graph_receipt = json.loads((C.EVID / "graph_receipt.json").read_text())
    anchored = [e for e in edges if e.get("caller_blob") and (e.get("line") or e.get("doc_anchor"))]
    checks["c_graph_anchoring"] = dict(
        nodes=graph_receipt["nodes"], edges=graph_receipt["edges"],
        anchored=len(anchored), pass_=(len(anchored) == len(edges)))
    unresolved = (C.OUT / "05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv").read_text().splitlines()
    checks["d_bounded_unknowns"] = dict(
        unresolved_rows=len(unresolved) - 1,
        pass_=(len(unresolved) - 1 == graph_receipt["unresolved"]))
    scan = json.loads((C.EVID / "leak_scan_receipt.json").read_text())
    checks["e_scan_coverage"] = dict(
        scanned=scan["scanned_python_blobs"], targets=scan["targets"],
        pass_=(scan["scanned_python_blobs"] == scan["targets"]))
    roster = (C.OUT / "08_CLOSED35_UNIVERSAL_EXECUTION_COVERAGE.tsv").read_text().splitlines()
    roster_rows = [line.split("\t") for line in roster[1:]]
    checks["f_closed35_roster"] = dict(
        rows=len(roster_rows),
        unique=len({(r[0], r[1]) for r in roster_rows}),
        permission_columns_bounded=all("UNKNOWN" in r[7] or "NOT_GRANTED" in r[7]
                                       for r in roster_rows),
        u_epre_bounded=all("NOT_ISSUED" in r[8] or "NULL" in r[8] for r in roster_rows),
        pass_=(len(roster_rows) == 35 and len({(r[0], r[1]) for r in roster_rows}) == 35))
    tsv = (C.OUT / "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv").read_text().splitlines()
    canonical = ("rawlsing_next/pre553_source_backed_c11_facade.py",
                 "rawlsing_next/pre553_route_b_production.py",
                 "rawlsing_next/pre553_discovery_exact.py",
                 "rawlsing_next/pre553_batch_runner.py")
    canonical_hits = [line for line in tsv[1:] for p in canonical
                      if line.startswith(p + "\t") and ("\tLITS_LITERAL\t" in line or
                                                        "\tQ301_LITERAL\t" in line)]
    i51_hits = [line for line in tsv[1:] if "r51_joined_source_producer.py" in line
                and ("\tLITS_LITERAL\t" in line or "\tQ301_LITERAL\t" in line)]
    checks["g_negative_control"] = dict(
        canonical_literal_hits=len(canonical_hits), i51_literal_hits=len(i51_hits),
        pass_=(len(canonical_hits) == 0 and len(i51_hits) > 0))
    # h seeded fake fixture leak (temporary copy, never repository source)
    import leak_scan as L
    seeded_source = ('from rawlsing_next.tests.test_fixture import build_fact\n'
                     'FACT = "q301_2 LiTS fixture"\n')
    seeded_hits = L.scan_python(seeded_source, "seeded_fake_fixture_leak.py",
                                "PRODUCTION_CODE")
    seeded_detected = any(h["pattern"] in ("Q301_LITERAL", "LITS_LITERAL")
                          for h in seeded_hits)
    seeded_path = Path(tempfile.mkdtemp(prefix="r53-u53f-seeded-")) / "seeded_fake_fixture_leak.py"
    seeded_path.write_text(seeded_source)
    checks["h_seeded_leak"] = dict(
        detected=seeded_detected, hits=len(seeded_hits),
        temp_path_not_repository=str(seeded_path),
        pass_=seeded_detected)
    # i determinism: rerun deterministic producers and compare hashes
    targets = ["01_REPOSITORY_SCOPE_AND_COMPLETENESS.json",
               "02_ALL_PINNED_TREE_FILES.tsv", "04_UNIVERSAL_PRODUCER_CONSUMER_GRAPH.jsonl",
               "05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv",
               "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv",
               "06B_DOCUMENT_REFERENCE_COUNTS.tsv",
               "07_HISTORIC_REQUIREMENT_TO_ACCEPTANCE_PROPAGATION.tsv",
               "08_CLOSED35_UNIVERSAL_EXECUTION_COVERAGE.tsv"]
    before = {name: sha(C.OUT / name) for name in targets}
    for script in ("index_tree.py", "leak_scan.py", "docs_and_roster.py",
                   "timeline.py", "graph_build.py"):
        subprocess.run([sys.executable, str(C.TOOLS / script)], cwd=str(C.ROOT),
                       check=True, capture_output=True)
    after = {name: sha(C.OUT / name) for name in targets}
    checks["i_determinism"] = dict(
        before=before, after=after, pass_=(before == after))
    checks["all_pass"] = all(v["pass_"] for v in checks.values())
    schema = dict(schema="R53_U53F_QUALITY_CHECKS@1", checks=checks,
                  law="Checks a–i from the commission; mechanical, not scientific adoption.")
    C.write_json(C.OUT / "QUALITY_CHECKS.json", schema)
    print(json.dumps({k: v["pass_"] for k, v in checks.items()
                      if k not in ("all_pass",)}, indent=1))
    print("ALL:", checks["all_pass"])


if __name__ == "__main__":
    main()
