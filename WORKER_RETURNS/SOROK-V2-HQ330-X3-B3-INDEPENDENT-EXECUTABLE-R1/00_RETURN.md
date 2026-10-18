# X3 independent executable court — B3_REVISE

**Verdict: `B3_REVISE` for exact B3 `47b46a85b9ebb633754866f1e6f1b12db3bd2012`.** The positive executions reproduce, including blinded F2 and actual cold SQLite. Independent hostile execution finds a public-entrypoint refusal/partial-write defect. This return does not issue `B3_EXECUTABLE_TEST_ONLY_ACCEPT_SCOPED`.

Sealed startup `50349f2e90f8e9d0379040fdb7d3186dfe3b6c02` and target tip were directly verified against origin. Assigned branch: `agent/reviewer-sorok-v2-hq330-x3-b3-independent-executable-r1`. One fresh reviewer performed this work, with no B3/M2 authorship, subagents, paid/model API calls, package installs, candidate repair or frozen-source edits. All published changes are confined to this X3 return.

## Executed results, kept at their own grades

| Court | Actual result |
|---|---|
| Exact B3 author suite | **71 PASS** |
| Frozen F2 through original B3 adapter | **42 PASS**, 20 eligible / 22 refusal or deferral |
| Independent blinded F2: remove expectations, replace case IDs before execution | **42 PASS**, same 20 / 22 split |
| Independent constant / cosmetic-label mutant contrasts | Both killed; real adapter passes all four contrasts |
| B2 inherited | **249 PASS**: B1 39, P1 74, historical D1 22, corrected D1 17, F1 reference 97 |
| B2 integration/accounting | **81 PASS** |
| Frozen R1 | **45 PASS** |
| Post-E2 repair controls / strict E2 | **5 PASS / 2 PASS** |
| Frozen full E2 / X2 | **42 PASS + 2 FAIL / 16 PASS + 1 FAIL**; assertions of repaired old bugs remain literal failures |
| M2 author suite | **41 PASS** |
| Frozen M1 / I2 against M2 | **18 PASS + 19 FAIL / 13 PASS + 10 FAIL** |
| M3 original source-preimage court on unchanged M2 | **3 FAIL**: all original strict REDs reproduced |
| Original native F1 | **17 RED**, exit 1, unchanged case IDs |
| Independent X3 final hostile suite | **20 PASS + 8 FAIL**, 28 executed, zero errors/skips/xfails |
| Positive and no-permission developmental loops | Both execute; both fresh-process reconstructions match exact receipts and complete SQL snapshots |

The eight X3 failed assertions are **not eight distinct vulnerabilities**. Five independently check manifestations/cold persistence of the partial-write defect. The other three expose narrower practice or helper-contract assumptions, discussed below. Earlier incremental X3 runs are preserved separately and are not additional independent test populations.

`suite_results.json` and raw JUnit/logs are authoritative. No pooled ALL_GREEN total is appropriate. Native F1 IDs remain F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21. Historical D1's green 22 is not corrected absence qualification. M1/I2 compatibility results do not override the M3 adjudication of obsolete time/access fixtures. M3's missing 32-case ZIP was not reconstructed or claimed executed.

## Blocking P1: refusal after already committed admission

At exact `integration.py:210–215`, B3 calls B2 admission and inserts `b3_source`/`b3_audit` **before** resolving `origin_event_id` at lines 220–223. A registered, otherwise valid frame with `origin_event_id='NEVER_ADMITTED_PARENT'` admits its loss first. Parent lookup then refuses, but no encompassing transaction exists. The refusal handler at lines 265–267 cannot undo B2's committed admission or autocommitted B3 rows; its own `stop()` assertion raises `REFUSAL_MUTATED_DATABASE` instead of returning the advertised unchanged refusal.

Independent SQL receipts `evidence/sql/missing_origin.json` and `cold_partial_missing_origin.json` show each of `occurrence`, `b2_event_identity`, `b2_ingress`, `b3_source`, and `b3_audit` moving **0 → 1**. Closing and reopening SQLite preserves these rows. No source-code patch, forged SQL, bypass method or owner permission was used. The extra origin field is also outside `FixtureAuthority.binding()`, so registration does not bind it.

A second public-entrypoint trigger sets the external loss time to **99** while the frame remains **as_of=7**. `qualify()` checks record clocks but not `event.time <= as_of`. B2 receives a context clock manufactured from the supplied event time in `custody.prepare()`. Later M2 validation refuses only after admission and source projections. Receipts `atomic_future_event.json` and `cold_partial_future_event.json` show **five** committed occurrence/identity/ingress/audit rows and one `b3_source` row surviving the exception and cold reopen. Thus no successful owner effect is manufactured in these attacks, but refused temporal/lineage processing pollutes durable admitted history.

Minimal repair direction, **not implemented by X3**: validate/bind origin lineage and event chronology before writes; ensure every later refusal obeys B3's stated snapshot invariant across all participating tables. B2 manages its own SQLite transactions, so simply adding a late BEGIN or rolling back only response/target writes is insufficient. Use a correctly composed transaction or complete preflight/staging design, and retain these literal RED tests as the regression court. If the intended contract instead permits admission followed by response refusal, expose that explicitly and reconcile it with `stop()`/`no_mutation`; the current implementation does neither.

## Practice result: real dependency, limited evidence semantics

The positive t2/t7 authored world runs do produce one persistent target record; no-permission runs produce none. Missing observer, wrong result, one check, future record, absent registered permission and stale permission controls all deny formation. Changing private affect does not select or change practice. At t9 the persisted exact practice hash supplies **an offered CHECK_LOCK option**; it does not enact a third check. The journal-only B2 inherited control preserves inspect-alone rather than its positive joint-check path.

Two strict X3 assertions fail at `target_owner.py:18–23`:

- Replacing pre-loss t2 with t6 gives two post-loss checks (t6/t7) and still commits. The owner checks that *some* check is after loss, not that one precedes it. This limits the commission's before/after-history contrast; CAN011 itself does not impose a universal pre-loss requirement.
- Two differently named records with otherwise identical t7 actor/object/observer/result fields also commit. The rule counts distinct IDs, with no independently bound physical action-occurrence identity or temporal separation. This demonstrates insufficient evidence to distinguish repeated activity from duplicate descriptions. Coarse same-time records could represent two actual actions, so this is an identity/formation-proof limitation, not proof that every same-time pair is fraudulent.

The engine genuinely depends on registered synthetic evidence, predicates and owner permission; it does not derive practice from demographic labels or F2 expected outputs. However `World.tick()` itself scripts the two completed checks and result labels, `FixtureAuthority` accepts a trusted author's registered bytes, and the target court recognizes those declared fields. There is no external physical observer authentication, empirical learning law, calibrated threshold, or independently generated human activity. Do not promote this dependency into witnessed real-world learning or semantic CAN011 adoption.

## Historical source guard and adversarial entrypoints

All three renewed-attestation analogues are refused through **cold reopened Integration.run** without changing tables: old speech, practical history and affect-source records cannot be rewritten even after fixture re-registration and refreshed hashes. Prior raw records are compared at `integration.py:199–201`; derived M2 preimages are then checked at 229–232. Removing prior speech/exposures through the integrated path also refuses without mutation. These are useful bounded protections.

The standalone `source_guard.check()` helper compares only keys present in the *new* scene. Removing prior sources passes it; its strict missing-readset X3 assertion is RED. That alone is **not a demonstrated bypass of Integration.run**, whose retained raw preimages reject the tested removal. It must not be advertised as a self-sufficient general durable source guard. Missing sources need explicit semantics if another adapter reuses it.

Direct frozen M2 `eligible()`/append continuation bypasses B3 entirely: the original three M3 tests still fail. Calling raw `scene_at()`, `response()`, `admit_projection()` or private `_run()` is not equivalent to the commissioned locked `run()` boundary. `admit_projection()` itself has neither registrar nor B3 lock; callers must not treat it as an independently safe issuer. `process_b3.py` creates a registrar and registers its input frame, so the test CLI is deliberately a trusted-fixture entrypoint, not an authenticated hostile-user perimeter.

An actual second SQLite connection, opened by an injected test scheduling hook **after source_guard returns and before B3 commits**, can replace a `b3_preimage` row. The current call still returns ELIGIBLE; cold reentry detects the mismatch and leaves the polluted snapshot intact. Receipts `privileged_guard_to_commit_race.json` and `privileged_guard_to_commit_cold_detection.json` document it. This requires a privileged writer that ignores B3's advisory lock; it is outside B3's disclosed trusted-store scope, not a new ordinary-caller bypass. B3 does not hold a database transaction from source checking through final commit. Mutating the Python registrar allowlist or loaded functions is similarly privileged fixture/runtime control, not a signed-owner proof. Re-registration alone cannot defeat the persisted-history comparisons tested here.

Honest B3 callers serialize with the advisory file lock. The unchanged B3 suite additionally runs real cold same-content/conflicting-content process races. Unchanged R1/E2 suites execute overlapping writers, stale readsets and SIGKILL/rollback boundaries; their SQL evidence is retained. The independent E3 report was read as prior accepted B2 scope, not substituted for executing these inherited courts. Its privileged-B1/SQL and O(total occurrences) scan limitations remain open.

## Independent F2 audit and scientific ceiling

`audit_f2.py` removes `expected`, replaces every case ID with an unseen ID, replaces analyst group metadata, and profiles the actual engine input and calls. The frozen reference runs **only after** each receipt returns. Every eligible case physically calls exact B2 `advance`, M2 `eligible` and B3 `response`; all 42 execute the adapter boundary. `evidence/f2_blinded/matrix.json` independently reconstructs the matrix, including refusal codes, engine-input keys and function counts. The oracle is never an engine input. Independent constant and cosmetic-label controls fail material-history/offer/hearing contrasts, while the actual results preserve label invariance.

Twenty eligible cases enumerate and respond; twenty-two refuse/defer. F2's conservative evidence contract neither demands 42 psychological effects nor detects all partial-write paths; passing it does not override X3's hostile REDs. Its exact-ledger case is seeded by an actual preliminary admission, explicitly a test-only reconstruction. No selected belief, selected affect, culprit fact, psychological repair or forced counterpart compliance is generated. The original t3 loss contains no t4/t5 speech; t6 PROCESS carries attributed alternatives. Later P's refusal comes from its scheduled own rehearsal history; the author suite also executes its free-history ALLOW contrast. These are deterministic synthetic counterpart processes, not autonomous persons or evidence of empirical psychology.

CAN008 R2's exact adopted candidate blob and adoption were read: immediate response/recruitment cannot seize target owners. CAN011's sparse/valid-empty law grants zero concrete practice labels or numeric rules by itself. ADP019 owns actual admission; ADP016 memory and ADP017 epistemic/claim access remain separate and ungranted. B3's M2 durable-lineage quarantine is appropriate and remains mandatory. No production actor, original35/source-wave use, semantic adoption, CURRENT/PREMAIN mutation or actor-memory entitlement is established.

## Exact custody, SQL and reproduction

`verified_sources.json` independently checks **216** entries: the materializer's 199 exact Git/archive entries plus all 17 B3 Python files. Each Git entry was compared byte-for-byte to `git show`, recomputed with Git's NUL-delimited blob SHA-1 and SHA-256, and checked against its object ID. F1 archive members were compared to the exact hash-verified Git archive. `loaded_modules.json` records all nine actual core imported files and hashes, not just intended pins. They resolve into the clean reviewer materialization. No candidate executable source byte changed.

| Source | Exact Git blob SHA-1 |
|---|---|
| B3 integration.py | `e2540491e31f79162b0be045bb35239f28ad8059` |
| B3 source_guard.py | `06fc933a2e9d2111515fabec28863e19c7aa4f75` |
| B3 target_owner.py | `30aa015143ecb01e0928032148d335aaf130360a` |
| Repaired B2 bridge.py | `ca27e715fca33da49b2d566cfe4bef521d5eb502` |
| Frozen M2 kernel.py | `5530bd1152161e084f734b5ba518668763192c6b` |
| Frozen F2 cases.json | `5917534001fc451831fe2ec92f7429899e96874e` |

F2 cases SHA-256: `827eada1eb73a131bfb1604f0977dcff08d173fb7eadb9a06d7894010f0e9351`. All remaining exact hashes are in the manifest.

Live and fresh-process positive SQLite snapshots both hash to `99eedde4545a657c51c3c1ae612895f3936001e802e105e237bf32bf6a2ddcfd`; no-permission snapshots both hash to `1344a727b9dbb7542c4937e97bc8cedeb12798a733775df81178ebb61c7d7982`. Both have 10 exact admitted occurrences, 2 B3 external source events and 6 responses; only the positive has one target transition. All four `PRAGMA integrity_check` results are `ok`. SQL files, complete snapshots, fresh subprocess receipts, write-statement traces and table counts are retained under `evidence/` and `sql_replay_audit.json`.

Run from this return directory, with the pinned objects in the existing shared object store:

```sh
python3 run_review.py --runtime /tmp/new-x3-court
python3 mutation_controls.py
```

`run_review.py` materializes unchanged code, executes the original driver, independent pytest and blinded F2, verifies Git/import bytes, then packages evidence. Expected hostile failures are retained as failures. The exact original `run_all.py` reaches and passes all execution/replay stages, then exits 1 in `finalize.py:73`, which hard-codes the **author** branch. X3 preserves that packaging failure and uses its own independent collector; it never spoofs the branch or edits the author finalizer. Its original artifact manifest is author provenance, not a checksum of a fresh run.

Bootstrap disclosure: the supplied clean app checkout initially pointed to unrelated `25830fe…`. The requested remote branch was fetched and checked out at the exact seal. An initial nested materialization location interacted with Git's cwd-relative tree paths and failed to find B2; staging was moved outside the checkout with explicit existing GIT_DIR, without changing the materializer. No clone was created. Incremental tests and their failure logs are preserved. Profiling overhead makes blinded F2 slower than ordinary execution; timings are not performance claims. Portable evidence sanitizes local paths/XML hostnames; source bytes, actual results and SQLite content remain unchanged.

Observed environment: Python 3.11.3, pytest 9.1.1, SQLite 3.40.1, Git 2.39.1, Node 18.14.2. `environment_passport_delta.json` records the new runtime epoch and portable source/coverage references. Requested GPT-6 Medium is user-specified; runtime model/effort and cash charges cannot be independently attested. No model/provider switch occurred. Remote return commit identity is verified and reported after publication, outside its own preimage. HQ owns intake and any subsequent acceptance/adoption.
