# PYAT R3 · Pair 2 · S2-B — unified Agent A reciprocal adversarial return

**Disposition:** \`REVISE_EXACT_DEFECT__BOUNDED_DERIVED_I02_IMPROVED__FULL_S2B_NOT_COMPLETE__G5_NOT_RUN\`.

**Correct commission:** #919 / S2-B / original P2-02, controlled by #909 R3/R3C/R3S, PROGRAMMA PYAT and adopted PRE-MAIN MCR-lite. S1-C/P1-04 is **not** this artifact's commission. User has disclosed that B could not read the original commission before A's return; this limits any claim to B's procedural research independence, not the reproduccible substance of its four original engineering faults. A/B are not G5.

## 1. Exact unified artifact / source grounding

- **Original A:** PR [#952](https://github.com/maidiu/rawlsing/pull/952) @ \`d5d6577b557fa8ced2dbb42d190ab254ab983b19\`; 84/84 author PASS at tested cut \`2d217c63653f98a56ac23182f766a059460e8d68\`.
- **Adversarial B:** PR [#954](https://github.com/maidiu/rawlsing/pull/954) @ frozen \`f5ee89b8e700ac14cf266c2e3eae4c25f021c349\`, [88/88 actual PASS](https://github.com/maidiu/rawlsing/actions/runs/43278005794). Its exact-type, post-check assignment seal, closed typed refusal, and genuine native I03 fixes are retained.
- **Parallel reciprocal A attack:** PR [#957](https://github.com/maidiu/rawlsing/pull/957) @ frozen report-bearing \`fdb1e913fd7c1fbc6c4806967101a7eee6d6cf2b\`. This introduced correctly main-qualified cert tables, SELECT-only session, immutable SQL handles, adversarial TEMP/collation tests, and atomic no-clobber publication. **The PR #957 branch itself is untouched.**
- **Combined merge:** \`b5eb4c03c00ff7063838d633ef9d8a6bf7e86fda\` has *two actual parents*: our independent B-descendant R2 \`cc5936c74730ddec4834693491af8cffecf4ebdd\` and the frozen #957 head \`fdb1e913fd7c1fbc6c4806967101a7eee6d6cf2b\`. Merged source/test tree retains the strongest parts of both rather than publishing rival end products.
- **Unified branch:** \`agent/pyat-pair2-s2b-a-counter-20261112-r2\`; draft PR [#961](https://github.com/maidiu/rawlsing/pull/961), stacked on B's frozen exact HEAD. **Frozen source/test cut for this report:** \`6d5a8b7b6ea0b4035cefab62925705a30269c758\`.
- **Protected PRE-MAIN:** \`6a5c12f04323d74001f9632063ec907f4fc4468e\` reverified unchanged. No protected merge, W03/W04 branch edit, source-native/original35 use, P01–P20/T01–T18 issuance, S3, current source permission or G5.
- **S2-A source input:** [#944](https://github.com/maidiu/rawlsing/pull/944) \`d3814d08dbe03b8464ac6fff4164765179869213\` remains open, unmerged, G5 pending. Do not imply acceptance.

**Executable files:** \`rawlsing_next/_pre553_external_i02_certificate.py\`, unchanged inherited \`rawlsing_next/_pre553_query_predicate.py\`, \`rawlsing_next/tests/test_pre553_external_i02_certificate.py\`, independent SQLite repro \`rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py\`, and \`.github/workflows/pyat-pair2-s2b-external-i02.yml\`. Historical #957 report and receipt are also preserved at their own exact cut.

## 2. What B got right, exactly

B identified four actual trust-boundary failures in original A:

1. An arbitrary protocol carrying real-looking roots and respondent census could install counterfeit EMPTY postings into **real native I03**.
2. An overrideable \`VerifiedExternalI02\` subclass could impersonate an authenticated selector.
3. A post-install closed SQLite reader yielded uncontrolled \`sqlite3.ProgrammingError\`.
4. A verified concrete instance could have its \`db\` connection replaced post-hash, changing actual I03 results under the held roots.

B's hostile [RED 84/3](https://github.com/maidiu/rawlsing/actions/runs/43276452169), [RED 87/1](https://github.com/maidiu/rawlsing/actions/runs/43277256665) and final [GREEN 88/88](https://github.com/maidiu/rawlsing/actions/runs/43278005794) substantiate its *frozen* repairs. No regression to the original unguarded installation is introduced here.

B also correctly recognized the derived/full-I02 distinction. A complete sourcefree legacy \`C11LogicalRelease\` and \`ReplayManifest.closure_refs\` are still materialized *before* this new disk-sorted certificate. This is a **material still-open S2-B contract defect**, not a permission gate that licenses premature completion.

## 3. New attacks, repaired code and actual evidence

### NEW-A-01: mutable read-only SQL connection

B protected assignments to the verifier but exposed \`db\` as a raw \`sqlite3.Connection\`. Local Python/SQLite reproduction proved a caller could \`ROLLBACK\` its authenticated read transaction, then an ordinary SQLite writer could change selector rows; the same connection sees the modified data without any root check. A second attack used \`PRAGMA query_only=OFF\` + a TEMP \`selectors\` table, making an unqualified main count change from 2 to zero under unchanged saved bytes. A third showed that replacing the SQLite \`BINARY\` collation made \`main\`-qualified equality select 2 events instead of 1. These are substantive API integrity defects, not Python object-model theatrics.

**Consolidated repair:** PR #957's \`main.\` table qualification and SELECT-only \`_VerifiedSelectOnlyDatabase\` + wrapped cursor, strengthened by ordinary \`__delattr__\`/assignment protection, immutable facade/cursor state, \`in_transaction\` checks and closed-state typed refusal. Only SELECT reaches the verified connection, no PRAGMA/ROLLBACK/COLLATION/TEMP/session mutation, and no raw \`Cursor.connection\` escapes through the public result. The concrete native I03 first-consumer code remains unchanged. Ordinary private Python introspection and hostile native extension/OS modification are **not** claimed to be isolated.

### NEW-A-02: delete B's authentication seal

B guarded \`__setattr__\` after \`_sealed=True\` but did not implement \`__delattr__\`. Standalone Python reproduction: \`del object._sealed\` succeeds and the same assignment guard then admits \`db\` replacement. Our exact native-I03 test now attacks that path; the combined source denies ordinary deletion and refuses the swapped DB.

### NEW-A-03: G4 publication collision

Original/baseline A/B code used \`target.exists()\` before a later \`os.replace(stage,target)\`, allowing another writer's certificate created between operations to be silently overwritten. Local OS reproduction confirms \`os.replace\` clobbers, while \`os.link(stage,target,follow_symlinks=False)\` raises \`FileExistsError\` and preserves the rival. The consolidated builder atomically claims only a previously absent name and fsyncs the published directory. A crash between link and stage-unlink leaves a complete final plus orphan stage, never a partially written committed file. Both PR #957's and this branch's hostile collision tests are preserved.

### NEW-A-04: wrong physical certificate after a path swap

**This is not the same as B's post-check connection assignment attack.** The original cold verifier physically hashed \`path\` and then separately opened \`sqlite3.connect(path)\`. A writer swapping in another valid SQLite file between those operations—same logical table rows but different *physical* bytes—could evade the physical-root promise. Standalone Linux reproduction: the second file changed only SQLite \`PRAGMA user_version\`; its logical rows remained identical, while its SHA256 differed. Old pathname open read the substituted \`user_version=19\` under the original digest; an already-open \`/proc/self/fd/N\` descriptor continued reading original \`user_version=0\` and matching the original SHA256 after rename.

**Repair:** cold verifier now opens \`O_RDONLY|O_NOFOLLOW\` descriptor, uses its \`/proc/self/fd/N\` URI to open SQLite from the *same inode*, begins a read transaction/integrity verification, then streams SHA256 from that held descriptor. Only after that does it validate identities, closure, full logical root and publish the restricted reader. No compulsory secondary full-file temp copy or heap-wide list. This support is explicitly Linux-/proc-dependent; an unsupported platform gets typed refusal rather than insecure fallback. A deterministic actual native-I03 test monkeypatches the SQLite connect boundary to swap in a logically identical/different-physical file; asserts the reader still opens original pinned inode and returns the oracle.

### NEW-A-05: streamed cursor close and invalid SQL

PR #957's \`_rows\` protects each row in a streaming query. This combined version adds explicit cursor/view open-transaction checks at public fetch points. Invalid public SQL (including semicolon-separated statements and invalid SELECT) is rejected as \`ExternalI02IntegrityError\`; a closed verifier must not leak SQLite runtime errors. A direct test checks lifecycle, SQL and pointer leakage.

## 4. Test inventory and execution boundaries

At B's frozen HEAD the target S2-B test module had **14** \`test_*\` functions and the full selected workflow returned **88 PASS**. The unified module has **25** \`test_*\` functions: **11 additional** adversarial cases from the two A corrections (six from #957, five ours).

**Exact required runs once an executor can actually schedule:**

\`\`\`bash
git checkout 6d5a8b7b6ea0b4035cefab62925705a30269c758
python rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py
python -m pip install pytest pyarrow pandas pyreadstat
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py::test_s2b_material_sourcefree_resource_probe
\`\`\`

**Evidence honestly graded:**

- B's original 88-case suite and 2048-respondent resource probe are genuinely green **only at B's frozen commit**, not necessarily the new code.
- On this turn, local Python 3 SQLite/OS primitives were actually executed for rollback, TEMP shadow 2→0, BINARY equality 1→2, seal deletion, os.replace overwrite vs os.link no-clobber, and a same-logical/different-physical SQLite pathname swap against descriptor-pinned open. The reproduced mechanism is established; *native I03 green at this new merged commit is not yet established*.
- [Latest merged native CI run #43284811631](https://github.com/maidiu/rawlsing/actions/runs/43284811631) and adjacent run fail **before allocation** (\`runner_id=0\`, zero job steps). The same absence appears across parallel PYAT Actions runs. This is neither a pytest RED nor a source GREEN; full native tests and memory measurements **NOT_RUN at current HEAD**. Re-running the failed job once previously produced the same pre-run issue.
- No source-direct I02 100k/6GiB gate, process-tree aggregated RSS, peak scratch, real CURRENT source issuer, S2-C Parquet saved bodies, original35 or independent G5 were run or issued. Old B 2048 timings are historical parent evidence only.

## 5. G1–G5 receipt

| Gate | Exact current grade | Unresolved original requirement |
|---|---|---|
| G1 | **PARTIAL** | M01–M18 and complete sourcefree corpus/selector keyspace are inherited from truly legacy sealed I02, not independently source-direct bounded construction; no P01–P20/T01–T18/current issuer |
| G2 | **PARTIAL, new tests NOT_RUN** | Existing B native I03 changed/restored result proven at B SHA; new combined pinned-physical/SQL facade I03 comparators need running; no all-direct I02 pipeline |
| G3 | **PARTIAL, new tests NOT_RUN** | Local SQLite/OS counterexamples real, 11 exact native adversarial tests added; no new full regression proof; hostile filesystem/process attack limits persist |
| G4 | **PARTIAL** | Atomic no-clobber and same-inode root code, sourcefree disk selector; no new process-tree peak, scratch, large-scale or upstream bounded full I02 proof |
| G5 | **NOT_RUN** | Nonauthor reviewer **other than A/B** may receive only after G1–G4 are executable and substantively demonstrated |

**Provisional full-packet disposition:** \`REVISE_EXACT_DEFECT\`. No G5 claim, no protected integration, and no S3.

## 6. Strongest next adversarial challenge

1. Run the **25 S2-B cases + inherited exact I02/I03 suite** on a real executor and repair any actual failures, preserving the B 88 baseline. The GitHub no-run jobs are not evidence.
2. Especially attack the **descriptor-pinned physical SHA root** across writer races, SQLite rollback journals and platform behavior. Linux /proc binding is now explicitly a capability condition; do not quietly claim portable validation. Detect actual same-logical/different-physical counterfeit, not only changed semantic values.
3. Replace full legacy \`C11LogicalRelease\` + \`ReplayManifest.closure_refs\` prerequisite with source-direct, genuinely bounded external-memory M01–M18 validation, conserving all native alias, occurrence, respondent, source/universe, coordinate/weight/routing, authority and replay negatives. This is still the **largest material unfinished S2-B defect**.
4. Keep real native first-consumer effects: query fact/replay, changed/restored physical and semantic roots, typed refusal, and zero vs unknown. S2-C separate cold physical event bodies, original35 science/rights and competent independent expected-root issuer must remain explicitly external.
5. Independently measure retained bytes, scratch, process-tree peak RSS, cold read, crash/orphan, and v1 migration. Prevent full canonical materialization; do not extrapolate from a 2,048-row pilot or a tiny model.

**Rejected approaches:** reopen path after hash and call it physical-root proof; merely make Python verifier immutable while exposing raw SQLite session; merely prefix \`main\` while permitting caller collation mutation; overwrite final path on publication; patch native scientific evaluator to match a deficient selector; manufacture a new source grant or a new MCR council.

**End condition remains finite:** Repair actual reproduced material failures, run the original G1–G4 court, return for one nonauthor G5 when genuinely justified. No endless theoretical hardening in place of source-direct functional completion.
