# 06 — Git/grep/AST reproducer and precise regression tripwire

**Script status: NOT_RUN.** This Browser/GitHub connection could fetch exact branch trees and chosen source blobs but did not expose an authenticated read-only git mirror or S2 runner. The current literal registry (01) covers **only 37 chosen blobs across 4 selected tree/ref indices (35 PRE-MAIN, 2 P1) and 2,466 literal hits**; other paths not content-scanned are not negative results. A remote GitHub code index is not an exhaustive tracked-file census.

## 1. Operator prerequisites

Use an authorized read-only local clone with all refs, objects, and any governed LFS access; keep census outputs outside protected PRE-MAIN. Do not pull private respondent data into the report. Verify:

    git remote -v
    git status --porcelain=v1
    git rev-parse integration/pre-main-reconciliation-r1
    git cat-file -t 773bb412a820949f13a7178b6671327cd56a3bf1
    git for-each-ref --format='%(refname) %(objectname)' refs/heads refs/remotes refs/tags
    git ls-tree -rz --full-tree 773bb412a820949f13a7178b6671327cd56a3bf1
    git grep -n -I -i -E 'Q86A|Q86B|Q86|Q69B|GT1|GT2|GT12|GT34|Afrobarometer|FIRST_GENUINE_CANARY' 773bb412a820949f13a7178b6671327cd56a3bf1 -- .
    git log --all -S'CONDITIONER_SOURCE_NATIVE_VARIABLE' --format='%H %P %ad %s' --date=iso -- rawlsing_next/field_forge_conditional_support.py
    git log --all -G'Q86A|Q86B|Q69B' --format='%H %P %ad %s' --date=iso -- rawlsing_next

Capture command exit status, timestamp, exact SHA, scope, non-UTF8/binary exclusions, LFS pointers and byte counts. The historical git log/blame is mandatory to distinguish deliberate frozen preservation from reintroduction or missed scope. The listed commands were **NOT_RUN** here.

## 2. Machine-readable full-ref raw census — reference Python script

Save the following to a temporary script outside protected source, for example q86_census.py. It reads git blobs and produces raw one-hit-per-offset JSONL plus separate blob/provenance and failures. It is **unexecuted reference code**, not a verified test result. Unlike GitHub indexed code search, it reads each distinct blob encountered on refs, preserving all locations. Note that all reachable *historical commits* beyond live ref trees require a separate git rev-list --all pass.

    #!/usr/bin/env python3
    import argparse, ast, collections, json, re, subprocess
    from pathlib import Path

    TOKENS = re.compile(
        rb"Q86A|Q86B|Q86|Q69B|GT12|GT34|GT1|GT2|Afrobarometer|"
        rb"FIRST_GENUINE_CANARY|CONDITIONER_SOURCE_NATIVE_VARIABLE|"
        rb"TARGET_SOURCE_NATIVE_VARIABLE|CANARY", re.I)
    LFS = b"version https://git-lfs.github.com/spec/v1"

    def run(*args):
        p = subprocess.run(["git", *args], capture_output=True, check=True)
        return p.stdout

    def line(f, value):
        f.write(json.dumps(value, sort_keys=True, ensure_ascii=False) + "\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    a = parser.parse_args()
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)

    ref_lines = run("for-each-ref", "--format=%(refname)\t%(objectname)",
                    "refs/heads", "refs/remotes", "refs/tags").decode().splitlines()
    refs = dict(x.split("\t", 1) for x in ref_lines)
    refs["ANCHOR:PRE_MAIN"] = "773bb412a820949f13a7178b6671327cd56a3bf1"
    provenances = collections.defaultdict(list)
    failures = []
    for ref, commit in refs.items():
        try:
            tree = run("ls-tree", "-r", "-z", "--full-tree", commit)
        except subprocess.CalledProcessError as err:
            failures.append({"ref": ref, "commit": commit,
                             "reason": "TREE_UNREADABLE", "exit_code": err.returncode})
            continue
        for record in tree.split(b"\0"):
            if not record:
                continue
            meta, rawpath = record.split(b"\t", 1)
            mode, typ, sha = meta.decode("ascii").split(" ")
            path = rawpath.decode("utf-8", "surrogateescape")
            if typ == "blob":
                provenances[sha].append({"ref": ref, "commit": commit,
                                         "path": path, "mode": mode})
            else:
                failures.append({"ref": ref, "path": path, "type": typ,
                                 "reason": "NON_BLOB_GITLINK_OR_TREE"})

    count = 0
    with (out / "raw_hits.jsonl").open("w") as hits, \
         (out / "blob_manifest.jsonl").open("w") as manifest, \
         (out / "python_imports.jsonl").open("w") as imports:
        for blob, locs in sorted(provenances.items()):
            try:
                payload = run("cat-file", "blob", blob)
            except subprocess.CalledProcessError:
                failures.append({"blob": blob, "locations": locs,
                                 "reason": "BLOB_OBJECT_UNAVAILABLE"})
                continue
            if payload.startswith(LFS):
                failures.append({"blob": blob, "locations": locs,
                                 "reason": "LFS_POINTER_NOT_MATERIALIZED"})
                continue
            if b"\0" in payload:
                failures.append({"blob": blob, "locations": locs,
                                 "reason": "BINARY_NUL"})
                continue
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError:
                failures.append({"blob": blob, "locations": locs,
                                 "reason": "NON_UTF8_TEXT_OR_BINARY"})
                continue
            line(manifest, {"blob": blob, "bytes": len(payload),
                            "locations": locs, "read_grade": "LOCAL_EXACT_BLOB"})
            for m in TOKENS.finditer(payload):
                offset = m.start()
                ln = payload.count(b"\n", 0, offset) + 1
                before = payload.rfind(b"\n", 0, offset)
                end = payload.find(b"\n", offset)
                if end < 0:
                    end = len(payload)
                line(hits, {
                    "finding_id": "Q86-" + blob[:12] + "-" + format(offset, "x"),
                    "blob": blob, "offset_byte": offset, "line": ln,
                    "column_byte_1_based": offset - before,
                    "needle": m.group().decode("ascii", errors="replace"),
                    "surrounding_line": payload[before+1:end].decode("utf-8")[:600],
                    "locations": locs, "match_kind": "LITERAL",
                    "semantic_class": "UNTRIAGED",
                    "first_consumer": "UNKNOWN_PENDING_SEMANTIC_GRAPH"})
                count += 1
            if any(x["path"].endswith(".py") for x in locs):
                try:
                    tree = ast.parse(text)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            targets = [alias.name for alias in node.names]
                        elif isinstance(node, ast.ImportFrom):
                            targets = [node.module or ""]
                        else:
                            continue
                        line(imports, {"blob": blob, "locations": locs,
                                       "line": node.lineno, "imports": targets})
                except (SyntaxError, ValueError) as err:
                    failures.append({"blob": blob, "locations": locs,
                                     "reason": "AST_ERROR", "detail": str(err)[:180]})

    with (out / "coverage.json").open("w") as f:
        json.dump({"heads_and_refs": refs,
                   "unique_blob_identities": len(provenances),
                   "raw_occurrences": count, "failures": failures},
                  f, indent=2, sort_keys=True)
    print(json.dumps({"refs": len(refs), "unique_blobs": len(provenances),
                      "raw_hits": count, "skipped": len(failures)}))

Usage:

    python3 q86_census.py --output /tmp/q86-full-tracked-census
    git rev-list --all > /tmp/q86-historical-commit-list.txt

**Important limitations:** This enumerates **current available ref trees**, not every historical commit in the second command; git rev-list requires a separate explicit historical per-commit manifest and first-introduction traceback. It cannot prove runtime reachability, dynamic imports, generated code, provider/external repositories or owner-science issuance. Where original respondent bytes are restricted, record immutable identifiers and controlled read grades, not actual bytes in these reports. Review script semantics and test it on a tiny known toy repo before running the real estate.

## 3. AST semantic-dependency pass

Join python_imports.jsonl with the exact per-tree path/blob map to derive import/reexport edges and inspect aliases. Follow nonliteral dependencies (source identity/frozen risk-set hashes, authority selection dictionaries, injected refs, JSON config and fixture calls) through:

    Definer -> import/reexport -> validator/constructor -> receiver -> FIRST NON-TEST product consumer.

Independently examine imports and runtime call sites outside rawlsing_next, including source-transport, repository loader, SQL, workflow scripts, tests and archived material. Manual scrutiny is required for dynamically selected registries, generated copies, deserialization and call-site flags. Confirm where an accepted generic successor supplants a narrow canary; do not merely count tokens. Compare all-branch historical fixed constants with frozen-source hashes before issuing any removal instruction.

## 4. Minimal anti-canary-to-general CI tripwire — proposed, NOT_RUN

**Frozen-scoped allowlist, not a universal deletion list**:

- field_forge_conditional_support.py
- wave1_ff_prev3_relation_admission.py
- gt12_c_to_d_relation_bridge.py
- gt12_d_to_m4_typed_bridge.py
- gt12_permission_translation_authority.py
- gt12_e2b_publication_governance_binding.py
- wave1_gt12_i03_positive_facts.py
- wave1_gt12_a2_real_gt1.py
- wave1_r5_q86_c11_projection.py
- wave2_r5_q69b_conditioner_projection.py
- gt34_q2_q69b_q86a_same_source_materialization.py
- f07_second_canary_prev3_admission.py
- **rawlsing_next/tests/** is only allowed *as test/fixture*, never allowlisted as generic production.

Any other production file adding Q86A/Q86B/frozen risk identity or a direct import of those canary modules raises a scoped review; a deliberately bound context-only adapter may request an explicit exception with source, grant, first reader and negative protections. Do not globally ban ordinary Q86 evidence, delete canary data, or deny unrelated source-native terms. The test must additionally look for indirect taint into currentness selection even without literal Q86.

**Regression contracts:**

1. Legally configured *different* pair cannot be silently stamped Q86B/Q86A at the purportedly generic producer; frozen bridge must reject non-Q86.
2. Generic selected-world reader must select source evidence by explicit authority/currentness/permission, not because Q86 happens to be present.
3. With Q86 transport unavailable, unrelated native/sourcefree processing at its authorized scope must proceed; Q86 itself returns typed negative, not a fabricated fallback.
4. CONTEXT permission cannot become REVIEW/ACTIVE_CAUSAL/actor use.
5. Existing Q86 historical replay fixtures remain reproducible under their exact source IDs.
6. First real consumer of the GF1 generic pair candidate must be independently replayed before accepting or replacing a producer.

**Acceptance blocker:** Until the full-ref text census, AST/manual dependency trace, skipped-file accounting and at least two independent cold-reviewed exact chains are executed, **INCOMPLETE_CENSUS** is mandatory.