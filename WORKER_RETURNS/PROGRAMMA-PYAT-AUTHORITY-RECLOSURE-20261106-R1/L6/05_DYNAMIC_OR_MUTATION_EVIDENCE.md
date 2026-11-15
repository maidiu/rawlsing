# L6 — static and dynamic evidence receipt; reproducible anti-omission boundary

## Exact environment and runtime limit

**S1 performed:** private GitHub connector read-only `git tree`, frozen `git blob` contents, issue #722, controlling #716 and PR #724 preparatory documents. Frozen code commit `9ba4764bef551b1ce498e5772d60b73d69337d4b`. Current protected branch at commencement `fce43498e16e4709f3c9801e8717f0fdae18126a`; branch must be rechecked at receiving.

**S2 NOT_RUN:** scratch `/workspace/scratch/ed986114a029` was not a Git checkout (`git status` returned `not a git repository`). No original respondent or local authority estate was mounted, `gh` not installed, and GitHub connector cannot itself execute source-native local tests. GitHub file reads are *not* a local S2 entitlement. No source bytes, respondent IDs or original codebook bytes copied into the return.

The 69 files listed in `01_SCANNED_FILES.tsv` were fetched fully as UTF-8 and examined; the 262 site lines in `02_LEGACY_CALLSITES.csv` were located using the exact deterministic S1 source-string scan below. The 30 `03` rows are **manually scope-labeled code tracing** from those files and are not automatically derived from the grep pattern.

## Reproduce the scanned universe and candidate-site counts

Checkout only the frozen ref under an authorized read-only worktree, then from repo root:

```bash
git rev-parse HEAD
git ls-tree -r --name-only 9ba4764bef551b1ce498e5772d60b73d69337d4b data/ddm_build_copy rawlsing_next
git cat-file -p 9ba4764bef551b1ce498e5772d60b73d69337d4b:data/ddm_build_copy/ddm_v550_question_relation_authority.py
rg -n 'read_csv|read_parquet|read_sql_query|json\.loads?|yaml\.safe_load|read_text\(|read_bytes\(|open\(|os\.getenv|os\.environ|add_argument' data/ddm_build_copy
```

For identical 262 candidate-site line counts, reproduce the exact JS scan against **only** the 30 `data/ddm_build_copy/` paths in `01_SCANNED_FILES.tsv` (other files are intentionally outside that denominator). This scan is lexical; it does **not** resolve dynamic imports, multiline arguments, quoted filenames, SQL execution, path joins or transitive helper ownership:

```javascript
const fs = require("node:fs");
const rows = fs.readFileSync("WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/L6/01_SCANNED_FILES.tsv","utf8")
  .trimEnd().split("\n").slice(1).map(x => x.split("\t"));
const paths = rows.map(x=>x[0]).filter(x=>x.startsWith("data/ddm_build_copy/"));
const regexes = [
  ["FILE_READ", /\b(?:pd\.read_csv|pd\.read_parquet|pd\.read_sql_query|pd\.read_json|pandas\.read_csv|yaml\.safe_load|json\.load[s]?)\s*\(|(?:\.read_text|\.read_bytes|\.open)\s*\(|\bopen\s*\(/],
  ["ENV_SELECTION", /\b(?:os\.getenv|os\.environ\.get|os\.environ\[)\s*/],
  ["CLI_SELECTION", /parser\.add_argument\s*\(|\bp\.add_argument\s*\(/],
  ["DB_QUERY", /\b(?:read_sql_query|execute|cursor\.execute)\s*\(/]
];
let rowsFound=[], byFile={};
for (const path of paths) {
  let count=0;
  fs.readFileSync(path,"utf8").split("\n").forEach((line,idx)=>{
    const t=line.trim();
    if (t.startsWith("#") || t.startsWith("import ") || t.startsWith("from ")
        || t.startsWith("def ") || t.startsWith('"""') || t.startsWith("'") || !t) return;
    for (const [kind,re] of regexes) {
      if (re.test(t)) {rowsFound.push({path,line:idx+1,kind,text:t.slice(0,160)});count++;break;}
    }
  });
  byFile[path]=count;
}
console.log(rowsFound.length,rowsFound.reduce((a,r)=>(a[r.kind]=(a[r.kind]||0)+1,a),{}));
console.log(byFile);
```

**Observed scan counters:** 262 line sites = 95 FILE_READ, 12 ENV_SELECTION, 155 CLI_SELECTION, 0 separately classified DB_QUERY (the SQL-read match is categorized under FILE_READ first). Some lines are legitimate control/input definitions, not authority reads. They must **never** be promoted to evidence of 262 distinct original semantically authoritative lookups.

**Enumerated but unvisited top-level blob denominators:** `data/ddm_build_copy` 178 (unread 148); `rawlsing_next` 153 (unread 125); `rawlsing_next/tests` 227 (unread 216). This is a sampled L6 source audit, not an exhaustive transitive closed call graph. Nested runtime/tests fixtures and other repository directories are outside these denominators.

## Static controls actually observed

1. `ddm_v550_question_relation_authority.py:298–307`: explicit path / environment / configured root / default priority, not latest. `:564–567` caches index by path + stat mtime + size; issuer lifecycle not thereby guaranteed.
2. `ddm_v550_response_semantics_authority.py:128–170,174–255`: two frozen CSV/manifest SHA gates, 145 certified registry keys and 236 binding records in legacy loader. Actual files not mounted to compute SHA.
3. `build_v550j_prepared_substrate.py:298–371`: cache manifest signature compares available hashes; typed `prepared_or_forensic_fallback` at `:373–405` can make an empty forensic artifact. L3 must verify whether omission of optional caller-supplied expected hash has any unsafe "match"; no positive native claim here.
4. `pre553_carrier_execution.py:317–350`: runtime catalog materializes **caller-supplied mappings**, not a hardcoded original authority path. `pre553_empirical_authority.py:234–249` resolves local or explicitly runtime-bound exact snapshot.
5. `pre553_source_native_preimage_adapter.py:421–473,524–553`: generated `R56-TEST-ONLY-AUTH-*` ALLOW authority consumed by synthetic preimage. This directly falsifies treating all C11 paths as original source authority integration.
6. `pre553_issued_workload.py:219–261,301–355`: native issued workloads are externally admitted and rechecked before/during query and Batch. No fake accepted issuer is created by scheduling.
7. `pre553_source_backed_c11_facade.py:616–686`: in-memory exact source/projection cache; `_pre553_c11_execution_view.py:160–325`: optional private event-body Parquet accelerator keyed by sealed I02 selector material; `pre553_parquet_carrier.py:249–356` and `pre553_duckdb_direct.py:14–67`: persisted canonical C11 data. These are distinct caches and cannot be assumed semantic authority sources.
8. `pre553_structural_admission.py:529–632` and `m1_admitted_field_forge_relation_v554_ingress.py:281–355`: structural and FF ingress require separate exact positive permission and preserve typed negatives; no old V552J source equivalence validated.

## Authorized next-run matrix (S2 only with rights)

For each SEM-01..12 from `04_NEGATIVES_AND_UNAVAILABLE.md`:

- Obtain a **legitimate issuer-controlled** baseline original source and immutable authority release. Record source file-byte SHA-256; authority file-byte SHA-256, row/revision, source/wave/option/operation and currentness; declared expected digest.
- Snapshot and freeze a legitimate alternate release for **meaning mutation**; do not forge an ALLOW record by altering a test fixture.
- Run cold source decode → accepted authority loader → C11 projection → I03/I05/Batch and optional FF with recording of exact first consumer, status and artifact digest.
- Change *only* source authority (same physical data) and assert typed effect/refusal. Then sever the real authority loader while leaving a preexisting test catalog to catch accidental fallback. Repeat for stale cache, reversed joint role, unknown routing, signed response revoked, and optional weighted/FF absence.
- Restore exact source+issuer release and assert output/receipts equal original hash. Every result must carry command, host/right proof, actual source/authority SHA and positive/negative expected/actual, not only a test name.

**No such executions occurred in this L6 session.** Existing pytest file contents were observed only. Independent L7 must run or independently verify actual S2 receipts before declaring closure.
