# PYAT S2-B/P2-02 — Agent A reciprocal convergence and bounded-closure adversarial handoff

**Status:** \`REVISE_EXACT_DEFECT__A_B_A_CONVERGED__G1_G4_PARTIAL__G5_NOT_RUN__NEW_CI_RUNNER_UNAVAILABLE\`.

## 1. Exact descendant and governing provenance

- Controlling original task: [#919 S2-B/P2-02](https://github.com/maidiu/rawlsing/issues/919); reconciled [#909 R3/R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), [PYAT PROGRAMMA](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md), [adopted MCR-lite](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md).
- Original Agent A [PR #952](https://github.com/maidiu/rawlsing/pull/952) at \`d5d6577b557fa8ced2dbb42d190ab254ab983b19\`.
- Opponent Agent B [PR #954](https://github.com/maidiu/rawlsing/pull/954) at \`f5ee89b8e700ac14cf266c2e3eae4c25f021c349\`; [author CI #43278005794](https://github.com/maidiu/rawlsing/actions/runs/43278005794) genuinely **88/88 PASS** for that **parent commit only**.
- Converged stronger A reciprocal [PR #961](https://github.com/maidiu/rawlsing/pull/961) at immutable inherited **\`6d5a8b7b6ea0b4035cefab62925705a30269c758\`**. That previous same-lineage A return closed B's public SQL rollback, TEMP table shadowing, changed BINARY collation, deletion-of-seal and atomic no-clobber gaps, with local primitive reproductions and new native tests committed. Its current new-native CI still lacks an actual runner; do not attribute B's 88 PASS to #961.
- **This** converged R3: [draft PR #965](https://github.com/maidiu/rawlsing/pull/965), branch \`agent/pyat-pair2-s2b-a-closure-bounded-20261112-r3\`, based directly on #961's immutable HEAD above. Exact **code/test/workflow cut \`d3e3eed5fab51631eb796da4f20ce942ae8fd2ac\`**. This report and machine receipt follow that code cut only.
- My earlier independent [#964](https://github.com/maidiu/rawlsing/pull/964) was **closed as superseded**: its overlapping fixes are not an alternative implementation; its nonoverlapping closure-memory defect and tests are now carried by this descendant. No competing rewrites.
- Protected PRE-MAIN verified cut \`6a5c12f04323d74001f9632063ec907f4fc4468e\`, **unchanged**. S2-A #944 \`d3814d08dbe03b8464ac6fff4164765179869213\` remains G5 pending; never silently accept unmerged dependencies.

## 2. Mandatory full-file receiving against B

I independently inspected B's complete return, machine G1–G5 receipt, exact PR diff, and production/first-consumer implementation. B's four reproduced failures were genuine and are **retained**:

1. Fake certificate-shaped object with authentic roots/respondent census could install false empty native I03 selector.
2. Forged \`VerifiedExternalI02\` subclass could override authenticated selector retrieval.
3. Native I03 cursor after reader close raised uncontrolled \`sqlite3.ProgrammingError\`.
4. A real verified class's reassigned SQLite connection changed real native I03 facts under a held root; B's source seal fixed ordinary assignment.

The original A disk-backed *derived* complete corpus+selector root, real native I03 support/parity/change/restore, paired aliases, occurrence conservation, external logical and physical roots, and 88 B sourcefree tests were not discarded.

Independent subsequent same-lineage A #961 found a further valid incomplete victory in B: **an immutable Python attribute is not an immutable live SQLite session**. Raw \`db.execute("ROLLBACK")\`, TEMP table name shadow, custom BINARY collation and \`delattr(_sealed)\` provide ordinary API/state escapes. The #961 repairs are preserved in the ancestry, not duplicated in this change.

## 3. New material G4 defect neither B nor #961 closed

**G4-R3-01 — attacker-supplied giant missing-closure index triggers O(untrusted refs) Python materialization during refusal.**

Both \`_check_relations\` (builder) and \`_check_relations_readonly\` (fresh cold verifier) used:

\`\`\`python
extras = [x[0] for x in db.execute(
  "SELECT c.ref FROM main.closure c LEFT JOIN main.objects o ON c.ref=o.ref "
  "WHERE o.ref IS NULL ORDER BY c.ref"
)]
if len(extras) != 2 or source not in extras: ...
\`\`\`

An attacker can create many missing closure entries in an otherwise rejectable SQLite candidate. Instead of refusing in bounded extra Python memory, the checker first builds a list of all hostile references; this violates the bounded-resource and failure-behavior intent even though it eventually rejects.

**Causal repair:** Both owners now execute SQL \`COUNT(*)\` of unmatched entries and an independently queried source-exception membership \`EXISTS/SELECT 1\`, followed by the original missing-object anti-join. No malicious ref list is constructed. These queries retain the stronger #961 \`main.\` qualification; the exact \`2\` exceptional v1 closure refs and exact source identity remain required. The valid full-corpus M01–M18/replay/selector logic is unchanged.

**New executable test:** \`test_s2b_a3_giant_poisoned_closure_refusal_keeps_python_heap_bounded\` is parameterized over **building** and **cold_verification**. It seeds 60,000 forged closure refs and requires typed \`ExternalI02IntegrityError\` with Python tracing allocation peak below 1.5MB for each rejection path. The inherited native query tests remain in the workflow.

**Independent local SQLite primitive measurement**, Linux Python 3.13, 60,000 orphan closure entries, same original list/count query shapes, NOT the imported project implementation:

| Rejection method | Observed Python tracing peak |
| --- | ---: |
| Old \`[row[0] for row in ...]\` | **4,640,284 bytes** |
| New SQL \`SELECT COUNT(*)\` | **529 bytes** |

The local experiment reproduces why the new implementation is bounded, but **does not replace the new project's exact pytest execution**. SQLite internal native allocations, disk scratch and whole process-tree RSS are not captured by \`tracemalloc\`.

Reproduce independently:

\`\`\`bash
python - <<'PY'
import sqlite3,tracemalloc
db=sqlite3.connect(':memory:')
db.execute('CREATE TABLE closure(ref TEXT PRIMARY KEY)')
db.execute('CREATE TABLE objects(ref TEXT PRIMARY KEY)')
db.executemany('INSERT INTO closure VALUES (?)', ((f'x:{i:012d}',) for i in range(60000)))
db.commit()
base='FROM main.closure c LEFT JOIN main.objects o ON c.ref=o.ref WHERE o.ref IS NULL'
for label,sql in [('old','SELECT c.ref '+base+' ORDER BY c.ref'),('new','SELECT COUNT(*) '+base)]:
    tracemalloc.start()
    data=[row[0] for row in db.execute(sql)] if label=='old' else db.execute(sql).fetchone()[0]
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    print(label,'peak Python bytes',peak,'orphans',len(data) if isinstance(data,list) else data)
db.close()
PY
\`\`\`

## 4. Commands, CI evidence and exact proof bounds

\`\`\`bash
git checkout d3e3eed5fab51631eb796da4f20ce942ae8fd2ac
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

**GitHub Actions execution blocked upstream of Python:** [#965 run #43285547404](https://github.com/maidiu/rawlsing/actions/runs/43285547404) and [#43285505531](https://github.com/maidiu/rawlsing/actions/runs/43285505531) both returned \`failure\` after ~4s, but the REST job metadata records **runner_name empty, zero steps, no JUnit artifacts**. An explicit rerun of [#964 run #43284046209](https://github.com/maidiu/rawlsing/actions/runs/43284046209) also yielded zero steps, as did many unrelated repo workflows on Nov 12. These are **runner-not-assigned failures**, not source/test RED or GREEN. No new R3 code has a trustworthy CI PASS/FAIL; do not count queued/failed-to-start jobs as executed. B's earlier 88 PASS proves only B's prior SHA.

**Immutable committed changed files beyond #961:**
- \`rawlsing_next/_pre553_external_i02_certificate.py\` — two bounded closure mismatch checks.
- \`rawlsing_next/tests/test_pre553_external_i02_certificate.py\` — two new 60k-hostile closure memory cases.
- \`.github/workflows/pyat-pair2-s2b-external-i02.yml\` — run on isolated descendant branch.
- This return and machine receipt (documentary-only).

## 5. Required G1–G5 honest disposition

- **G1 PARTIAL:** Inherited v1 actual M01–M18 validation and protected derived identities preserved; full genuinely source-direct independent bounded validation does not yet exist. P01–P20/T01–T18 source equivalence and CURRENT permission are separate authority.
- **G2 PARTIAL:** B's 88 tested cases establish its native I03 positive and changed/restored/negative at B's SHA; #961 and this descendant add trust hardening but their new real-native tests are not yet executed. Do not claim universal cold sourcefree physical I03; S2-C owns that carrier.
- **G3 PARTIAL:** B four actual replayed failures repaired, #961 demonstrates local TEMP/collation/transaction primitives and committed hostile native tests, this branch carries them. New end-to-end execution blocked, not green.
- **G4 PARTIAL:** Derived disk sort and external logical+physical roots preserved; malformed-closure Python heap breach locally demonstrated and exact code patched. Still depends on legacy \`C11LogicalRelease\` and full \`ReplayManifest.closure_refs\` tuple upstream, cannot certify complete bounded I02. Peak scratch/process-tree, 100k/6GiB pipeline and R3 new resource tests NOT_RUN.
- **G5 NOT_RUN:** A and B cannot self-accept; independent nonauthor receiving only on genuinely completed and executable G1–G4 obligations.

**Disposition:** \`REVISE_EXACT_DEFECT\` for full S2-B. The bounded orphan-ref improvement and stronger inherited native certificate boundary are real engineering capital but do not satisfy the main source-direct full external-memory I02 certification obligation.

## 6. Strongest next independent attacks

1. **Run the actual sourcefree full court** at this frozen exact code cut on a functioning executor; repair any real failures rather than ratifying CI startup errors or making new formal gates.
2. Attack the new SQL \`COUNT/EXISTS\` with pathological SQLite collation/index records and verify closure exactness, duplicate rejection and retained M01–M18 original valid fixture unchanged.
3. Resolve the true **genuinely bounded source-direct I02** validator: M01–M18, original authority/replay, respondent/occurrence, all typed negatives, semantic alias cross-version joins and external root without compulsory materialized \`ReplayManifest.closure_refs\` or full canonical object graph.
4. Recheck new #961 SQL facade under native I03 and live original consumer, especially ordinary permitted API mutation and lifecycle. Private Python introspection and hostile filesystem remain explicit trust limits, not claims of tested exploits.
5. Measure process-tree RSS, SQLite temp/scratch and 100k sourcefree end-to-end, plus cold and changed/restored native fact and replay. No original35 rights or S2-C physical release can be invented by these sourcefree tests.

**Stop-and-advance discipline:** no additional A/B exchange for hypothetical out-of-scope threats. A proved existing-contract breach should be repaired; pass genuine frozen G1–G4 then request one independent G5, not a new committee. This report does **not** promote untested code to accepted scope.
