# SOROK G03-I0 — Agent B FOLLOW-UPPER constructive return

**Original commission:** [#949](https://github.com/maidiu/rawlsing/issues/949), including its versioned I0-P01/P02, N01/N02/N03, R01, M01 and G1–G5 receiving amendment. **Original G03:** [#938](https://github.com/maidiu/rawlsing/pull/938) task G03, G02 population prerequisite. **Persona:** complete original SOROK four-role file at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`. This is a sourcefree S2 instrumentation correction, not the G03 cohort or native person/world science.

## 1. Exact artifact and isolation

- Repository: `maidiu/rawlsing`.
- **A frozen parent**: `b4f26fec056f5cb481a0b4e417e7a29bae833546` ([#953](https://github.com/maidiu/rawlsing/pull/953)); author branch never modified.
- **B writer branch**: `agent/sorok-g03-i0-b-follow-upper-20261112-r1`, created uniquely from A's exact parent. Use the exact current branch HEAD / receiving PR for the immutable final cut: the text of a commit cannot pin its own SHA.
- Original protected PRE-MAIN `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e` not touched; no live Codex fleet execution, local-worktree overwrite, protected merge, source science or actor grant. Branch-local GitHub writer isolation and separate GitHub Actions ephemeral checkouts observed; external Mac/OpenCode exclusive leases NOT_VERIFIED, and no claim that they are.

## 2. What A genuinely accomplished

A built a five-subprocess **actual P6** runner on sourcefree existing code, not a toy source substitute; separate cold Python process after `wait 1`, a deliberate `wait 0` refusal, persisted stdout/stderr/start/receipt files, source hashes, index and separate CLI reader. It correctly measured Linux direct-child wait4 CPU/RSS units, separated an expected refusal from unexpected reliability failures, and labeled provider calls/tokens/retries/billing and descendant-process resources UNOBSERVED. A's exact-head successful real-run receipt is [Actions #43272569345](https://github.com/maidiu/rawlsing/actions/runs/43272569345). All 18 A hostile tests were preserved.

## 3. Independently established defects

**RED-1 — state byte-count oracle not causal nonmutation proof.** Original reader compared only `state_bytes_before == state_bytes_after` on the expected refusal and never read final state contents. B built a same-size state rewrite adversary: A's parser accepted a physically changed state. [Frozen original-code red run #43274817492](https://github.com/maidiu/rawlsing/actions/runs/43274817492): 18 inherited tests pass; B state tamper test fails with `AssertionError: Reject not raised`.

**RED-2 — external index did not bind manifest.** Original `index.json` hashed only 20 per-attempt files, not `manifest.json`. Changing the source runner SHA-256 declaration in that manifest without changing the pinned index remained accepted. The same original-code red run shows B's second test fails with `AssertionError: Reject not raised`.

**RED-3 — actual refusal physically rewrites the P3 SQLite database.** B's first strict content-level gate revealed that the unmodified real `wait 0` changed `state/actual-p2/p3_psyche.sqlite3` without changing total state-root bytes. [Actual physical RED #43275935161](https://github.com/maidiu/rawlsing/actions/runs/43275935161). A's reported no-state-change assertion was not demonstrated at physical-byte grain.

**Crucial adversarial correction to B's own attack:** source P3 `PsycheStore._initialize` begins an immediate transaction and performs idempotent schema setup at each open. Read-only SQLite table/schema/user_version digests before and after the real refusal were **identical**, `17081c2346a32e8c704d289139bfda45465309128782032d578641400a93c9fb`, including `p3_meta`, `p3_operations`, `p3_records` and `sqlite_sequence` under that diagnostic's sourcefree snapshot method. [Genuine observation #43276552132](https://github.com/maidiu/rawlsing/actions/runs/43276552132). Physical-byte mutation is real; treating every SQLite page/header rewrite as an acquired psychological transition would itself be an invalid accusation.

**RED-5 — hard-coded cold success in the summary.** On B's hostile self-review the inherited reader still emitted `cold_reopened=1` even when a modified cold-view clock made `expected_scenario_pass=false`. B strengthened the existing cold-clock falsifier to require `cold_reopened=0`, observed the pre-repair RED at source cut `ed90a3a2f65cb9061d17df9c27e9aa140afa137b`, then made cold-reopened truth depend on the actual `wait`/+1 and fresh-view clock and exits. This is not a new requirement; it fixes a falsely reported existing first-consumer field.

**RED-4 — incomplete source preflight:** A invoked Git status with `--untracked-files=no`, allowing an untracked Python source candidate in the measured checkout despite a claimed immutable source tree. B's source check now rejects the candidate before P6 runs.

## 4. Construction: actual corrected source

Changed only the inherited four measurement/test files, additive B negative tests, the B-specific Actions workflow and this handoff/README. No P6/P3 or actor/world owner file modified.

- `measure.py`: records path-and-content state digest **and** a separately bounded SQLite logical-contents digest on every invocation; records genuine physical page churn without claiming actor change; refuses dirty/untracked source and output placed inside the repo; checks exact source HEAD/hashes again after actual run; external index also hashes manifest.
- `read_receipts.py`: independent digest implementation, actual source-clock-qualified cold-reopened derivation and genuine cold final-state recomputation; validates both state chains and different physical/logical refusal outcomes; detects a real SQLite row change rather than ignoring the entire database; checks immutable index against manifest and attempts; optional `--repo` source checkout recheck, `--index-sha256` external anchor.
- `test_measure.py`: 18 retained original hostile cases, now under explicit V2 sourcefree physical/logical state fixture without representing a real P6 execution; two added attempts against fake/missing logical-state witnesses.
- `test_agent_b.py`: independent same-size state tamper and manifest forgery red cases, plus real SQLite row-change adversary.
- `.github/workflows/sorok-g03-i0-follow-upper-20261112.yml`: isolated B branch, tests + untracked-source falsifier + **real unmodified P6** + separate source and externally anchored receipt-reader invocation + raw archive upload.

The V2 receipt format intentionally demands stronger evidence; old V1 artifacts remain exactly interpretable by A's frozen V1 reader, not silently regraded by B's successor schema.

## 5. Positive/falsifier/restoration and conservation

At [green execution #43277393973](https://github.com/maidiu/rawlsing/actions/runs/43277393973), **22 hostile tests PASS** and the untracked-source injection is refused at preflight; five real P6 subprocesses and a separate CLI reader succeed. The reader reports `attempts=5`, `success=4`, `expected_refusals=1`, `unexpected_failed_or_refused=0`, `cold_reopened=1`, `expected_scenario_pass=true`, `refused_state.physical_content_changed=true`, `refused_state.logical_content_changed=false`. This is honest: SQLite's physical bytes changed, the sourcefree logical row/schema state did not in this observed run. The raw artifact is available in that workflow's artifact list, and index SHA-256 printed in logs. The new independent SQL change test needs exact final-cut CI readback before terminal handoff.

Preservation: the 18 original tests remain and P6 itself runs through real `new/view/wait 1/cold view/wait 0`. No protected or other actor/world file edited. An external corrupted raw artifact with a forged matching index is still insufficient without separately trusted custody; the SHA-256 index is not a signature.

## 6. Refuted challenges and concessions

- **Refuted:** A never exercised real P6. Source CI proves the actual P6 subprocess path and clock 248→249 after `wait 1`; A's independent reader and failure accounting are substantial.
- **Refuted:** A invented zero provider cost. It correctly marked provider counters and billing UNOBSERVED; B retains that.
- **Refuted as overclaim:** physical SQLite changed, therefore Nadia's psyche changed. The observed read-only logical table comparison was invariant; B must not promote page churn into psychological change.
- **Conceded:** A's fixed five-command plan and independent receiver were worth preserving; no new life engine, new world owner or general billing inference was justified.

## 7. New surfaces and surviving holds

The logical SQLite witness is bounded to readable **closed, checkpointed database** table/schema content and a single known P3 sidecar; it is not a semantic theorem about arbitrary SQL engines, SQLite WAL concurrency or native psychological validity. File hashing is a sourcefree readback under an isolated runner, not an atomic distributed snapshot or globally authenticated signer. A single hosted Linux sample does not establish process-tree peak RSS, future all35/Pyat original science, tokens/cost, Mac performance, cold OS cache, five roots, statistical failure rates or production reliability. An external lease and separately qualified independent G5 nonauthor reviewer are not supplied by B.

**Engineering:** B author-candidate, actual sourcefree real first-consumer execution at exact green cuts; independent G5 NOT_RUN. **Scientific:** HELD. **Authority:** HELD. **Integration:** UNMERGED. **G03_FULL:** `NOT_EVALUATED_G02_MISSING`.

## 8. My own most serious remaining vulnerability

My normalized SQLite witness must not be used to excuse a future real row change, malformed database, uncheckpointed WAL, or a world-owner write outside this known sidecar. Agent A should attempt a real P6 invocation that changes SQLite logical rows without changing physical size, and determine whether a closed SQLite state snapshot truly catches it. A should also attack read-only state provenance when producer and receiver collude on an invented manifest/index and try a crash after `start.json` before `receipt.json`. Those attacks are material; mere increases in synthetic test count are not.

## 9. Direct challenge to A

Break the logical/physical distinction with a **real changed acquired-state record** accepted as harmless, or demonstrate a replay/root/branch breach under the actual P6 CLI that my content check misses. If you cannot, preserve this correction, independently verify the exact final SHA and move the bounded G03-I0 candidate to a third, genuinely nonauthor G5 receiver. Do not reopen G02/G03 as a reason to reject completed sourcefree instrumentation.
