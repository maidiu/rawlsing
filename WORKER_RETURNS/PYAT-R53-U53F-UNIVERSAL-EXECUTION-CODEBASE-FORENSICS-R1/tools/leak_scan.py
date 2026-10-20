"""06 — whole-census source-specificity and fixture-leak scan (static only)."""
from __future__ import annotations

import ast
import json
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

PATTERNS = [
    ("LITS_LITERAL", re.compile(r"\bLiTS\b|\bLITS1?\b|lits-i|lits1", re.I)),
    ("Q301_LITERAL", re.compile(r"\bq301[_\-.]?[27]\b|q301", re.I)),
    ("SYNTHETIC_SOURCE", re.compile(r"SYNTH[-_ ]?SRC|SYNTH_SRC|SYNTHETIC_SOURCE", re.I)),
    ("SOURCE_ROWS_COLUMNS", re.compile(r"SOURCE_ROWS|SOURCE_COLUMNS", re.I)),
    ("DIST_QUERY", re.compile(r"\bDIST\b")),
    ("KNOWN_ROUTE", re.compile(r"\bKNOWN\b")),
    ("FAMILY_HARDCODE", re.compile(
        r"Afrobarometer|Asian Barometer|Arab Barometer|Latinobarometro|Eurobarometer|"
        r"World Values Survey|\bWVS\b|\bGSS\b|\bLiTS\b", re.I)),
    ("FIXED_ARITY_TEXT", re.compile(r"single[_ -]?(target|item|wave|source)|one[_ -]?target|"
                                    r"first[_ -]?source|canary|universal", re.I)),
    ("SCIENTIFIC_NULL", re.compile(r"SCIENTIFIC_NULL|SOURCE_INTRINSIC|NOT_APPLICABLE", re.I)),
    ("RESPONDENT_ONE_ROW", re.compile(r"one[_ -]?respondent|single[_ -]?row|respondent.*==\s*1", re.I)),
]
IMPORT_TESTS = re.compile(r"rawlsing_next\.tests|^\s*from\s+tests\b|import\s+tests\b")


def classify(path, category, pattern, snippet):
    p = path.lower()
    if path.startswith("tests/") or "/tests/" in path or Path(path).name.startswith("test_"):
        return "TEST_FIXTURE_ALLOWED"
    if pattern == "TEST_IMPORT":
        return "GENERIC_RUNTIME_DEFECT"
    if pattern == "DIST_QUERY" and "/g50/" in p:
        return "UNTESTED_ASSUMPTION"
    if path.startswith("WORKER_RETURNS/"):
        if "r51_joined_source_producer" in p:
            return "GENERIC_RUNTIME_DEFECT"
        if any(k in p for k in ("/g50/", "canaries.py", "fixture.py")):
            return "TEST_FIXTURE_ALLOWED"
        if pattern in ("Q301_LITERAL", "LITS_LITERAL", "SYNTHETIC_SOURCE"):
            return "TEST_FIXTURE_ALLOWED"
        return "UNTESTED_ASSUMPTION"
    if path.startswith("rawlsing_next/"):
        explicit = any(k in p for k in (
            "fiabc_lits", "lits_", "as2a", "as2b", "wave2_r5", "q69b",
            "wvs7", "afro", "e04", "t35", "n9j"))
        generic_orchestration = any(k in p for k in (
            "candidate_c_production_binding", "darwin_stage_backend",
            "darwin_court_driver", "live_terminal_control", "succession_producer"))
        if generic_orchestration:
            return "GENERIC_RUNTIME_DEFECT"
        if "pre553_independent_parity_oracle" in p:
            return "SEMANTIC_AUTHORITY_DEPENDENCY"
        if explicit:
            return "PROPER_LOCAL_SOURCE_ADAPTER"
    if path.startswith("data/"):
        if pattern in ("FAMILY_HARDCODE", "LITS_LITERAL", "Q301_LITERAL") and any(
                k in p for k in ("adapter", "codebook", "ddm_v550", "lits", "source_rules",
                                 "question_relation", "authority")):
            return "PROPER_LOCAL_SOURCE_ADAPTER"
        return "UNTESTED_ASSUMPTION"
    if category in ("PRODUCTION_CODE", "OTHER_CODE"):
        if pattern in ("LITS_LITERAL", "Q301_LITERAL", "SYNTHETIC_SOURCE",
                       "SOURCE_ROWS_COLUMNS", "RESPONDENT_ONE_ROW"):
            return "GENERIC_RUNTIME_DEFECT"
        if pattern in ("DIST_QUERY", "KNOWN_ROUTE", "SCIENTIFIC_NULL"):
            return "UNTESTED_ASSUMPTION"
        if pattern == "FAMILY_HARDCODE":
            return "SEMANTIC_AUTHORITY_DEPENDENCY"
        return "UNTESTED_ASSUMPTION"
    return "DEAD_OR_INACCESSIBLE"


IMPACT = {
    "TEST_FIXTURE_ALLOWED": ("LOW", "fixture-scoped; cannot by itself prove universal runtime behavior"),
    "PROPER_LOCAL_SOURCE_ADAPTER": ("LOCAL", "legitimate local adapter/authority scope; not universal proof"),
    "GENERIC_RUNTIME_DEFECT": ("HIGH", "generic runtime carries a source-specific literal; consumer may silently serve only that source"),
    "UNTESTED_ASSUMPTION": ("MEDIUM", "generic path assumes a default/limited shape without an explicit source adapter"),
    "SEMANTIC_AUTHORITY_DEPENDENCY": ("MEDIUM", "family meaning depends on an external semantic authority"),
    "DEAD_OR_INACCESSIBLE": ("UNKNOWN", "path/ref not provably reachable"),
}
CONSEQUENCE = {
    "LITS_LITERAL": "universal planner may be bounded to the LiTS release; other 34 waves unproven",
    "Q301_LITERAL": "single proving item may substitute for all items/operations",
    "SYNTHETIC_SOURCE": "synthetic source identity may enter a production-looking path",
    "SOURCE_ROWS_COLUMNS": "source rows/columns may be assumed rather than read from the source",
    "DIST_QUERY": "a manually chosen DIST query may define the universal worklist",
    "KNOWN_ROUTE": "fabricated generic route/unit may bypass source-native meaning",
    "FAMILY_HARDCODE": "one survey family name may act as a universal gate or bypass",
    "FIXED_ARITY_TEXT": "single-target/canary wording may narrow universal scope",
    "SCIENTIFIC_NULL": "absence of implementation may be reported as scientific null/nonapplicability",
    "RESPONDENT_ONE_ROW": "one respondent/row may stand in for a population workload",
}


def scan_python(source: str, path: str, category: str):
    hits = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [dict(path=path, line=exc.lineno or 0, pattern="SYNTAX_ERROR",
                     snippet=str(exc), role="scan_limitation", classification="DEAD_OR_INACCESSIBLE")]
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            text = node.value
            for pattern, regex in PATTERNS:
                if regex.search(text):
                    line = getattr(node, "lineno", 0)
                    snippet = lines[line - 1].strip()[:200] if 0 < line <= len(lines) else text[:200]
                    hits.append(dict(path=path, line=line, pattern=pattern,
                                     snippet=snippet))
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            upper = node.slice.upper
            if isinstance(upper, ast.Constant) and isinstance(upper.value, int):
                line = getattr(node, "lineno", 0)
                snippet = lines[line - 1].strip()[:200] if 0 < line <= len(lines) else ""
                hits.append(dict(path=path, line=line, pattern="SLICE_LIMIT",
                                 snippet=snippet))
        if isinstance(node, ast.ImportFrom) and node.module and (
                "tests" in node.module.split(".") or node.module.startswith("rawlsing_next.tests")):
            if "/tests/" not in path and not Path(path).name.startswith("test_"):
                line = getattr(node, "lineno", 0)
                snippet = lines[line - 1].strip()[:200] if 0 < line <= len(lines) else ""
                hits.append(dict(path=path, line=line, pattern="TEST_IMPORT",
                                 snippet=snippet))
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq):
            if isinstance(node.comparators[0], ast.Constant) and node.comparators[0].value == 1:
                if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and \
                        node.left.func.id == "len":
                    line = getattr(node, "lineno", 0)
                    snippet = lines[line - 1].strip()[:200] if 0 < line <= len(lines) else ""
                    hits.append(dict(path=path, line=line, pattern="FIXED_ARITY_COMPARE",
                                     snippet=snippet))
    for hit in hits:
        classification = classify(path, category, hit["pattern"], hit["snippet"])
        severity, meaning = IMPACT[classification]
        hit.update(classification=classification, severity=severity,
                   impact=meaning,
                   consumer_consequence=CONSEQUENCE.get(hit["pattern"], meaning),
                   confidence=("HIGH" if classification in
                               ("GENERIC_RUNTIME_DEFECT", "PROPER_LOCAL_SOURCE_ADAPTER")
                               else "MEDIUM"))
    return hits


def collect_targets():
    sealed = {row["path"]: row for row in C.ls_tree()}
    targets = {}
    for path, row in sealed.items():
        if path.endswith(".py"):
            targets[(row["blob"], path, "")] = dict(
                blob=row["blob"], path=path, category=C.classify_path(path), refs=["SEALED"])
    # branch-only blobs from 03 shards
    import glob
    for shard in sorted((C.OUT).glob("03_MATERIAL_BRANCH_DIFF_FILE_BLOBS*.tsv")):
        for line in shard.read_text().splitlines()[1:]:
            fields = line.split("\t")
            if len(fields) < 12 or not fields[8].endswith(".py"):
                continue
            ref, _, _, _, _, _, _, _, path, blob, _, _ = fields[:12]
            key = (blob, path, ref)
            targets.setdefault(key, dict(blob=blob, path=path,
                                         category="BRANCH_ONLY_CODE", refs=[]))
            if ref not in targets[key]["refs"]:
                targets[key]["refs"].append(ref)
    return targets


def blob_reader(blobs):
    unique = sorted(set(blobs))
    payload = "".join(b + "\n" for b in unique).encode()
    import subprocess
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=str(C.ROOT),
                          input=payload, capture_output=True, check=True)
    data, index, pos = {}, 0, 0
    raw = proc.stdout
    while pos < len(raw):
        header_end = raw.index(b"\n", pos)
        header = raw[pos:header_end].decode().split()
        pos = header_end + 1
        if len(header) == 2:
            continue
        sha, kind, size = header
        chunk = raw[pos:pos + int(size)]
        pos += int(size) + 1
        data[sha] = chunk
    return data


def main():
    targets = collect_targets()
    blobs = blob_reader([key[0] for key in targets])
    rows = []
    syntax = 0
    scanned = 0
    category_counts = Counter()
    for key, meta in sorted(targets.items(), key=lambda kv: (kv[1]["path"], kv[0])):
        data = blobs.get(meta["blob"])
        if data is None:
            continue
        try:
            source = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        hits = scan_python(source, meta["path"], meta["category"])
        if any(h["pattern"] == "SYNTAX_ERROR" for h in hits):
            syntax += 1
        for hit in hits:
            rows.append((meta["path"], meta["blob"], meta["category"],
                         "|".join(meta["refs"])[:300], hit["line"], hit["pattern"],
                         hit["classification"], hit["severity"], hit["confidence"],
                         hit["snippet"], hit["consumer_consequence"], hit["impact"]))
            category_counts[hit["classification"]] += 1
    header = ("path", "blob", "tree_category", "refs", "line", "pattern",
              "candidate_classification", "severity", "confidence", "snippet",
              "consumer_consequence", "impact")
    C.write_tsv(C.OUT / "06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv",
                header, rows)
    receipt = dict(
        schema="R53_U53F_LEAK_SCAN_RECEIPT@1",
        scanned_python_blobs=scanned,
        syntax_errors=syntax,
        total_hits=len(rows),
        classification_counts=dict(sorted(category_counts.items())),
        targets=len(targets),
        scan_scope="all sealed-tree .py + branch-only .py blobs from the material-ref diff ledger",
        limitations=["Static AST/literal scan only; no repository test or production code was executed.",
                     "Dynamic reachability of a flagged edge is not asserted.",
                     "Documentation literals are handled in the timeline, not counted as code leakage."])
    C.write_json(C.EVID / "leak_scan_receipt.json", receipt)
    print(json.dumps(receipt, indent=1))


if __name__ == "__main__":
    main()
