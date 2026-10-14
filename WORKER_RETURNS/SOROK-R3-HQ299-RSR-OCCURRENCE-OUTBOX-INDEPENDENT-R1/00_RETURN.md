# SOROK HQ299 RSR — independent occurrence/outbox source-free court

**Terminal decision:** `INDEPENDENT_F2_REPRODUCTION_COMPLETE__SCOPED_TEST_REPRODUCTION_ACCEPT__STRONGER_OUTBOX_AND_PERCEPTION_ACCEPTANCE_HOLD__12_EXECUTED_REDS__NO_ADOPTION`

**Role:** independent commissioned I2 reviewer, **not** the SR prototype implementer, Sorok HQ, ADP019/CAN022/CAN025 issuer, renderer, V3 executor or accepting authority.

**Repository:** `maidiu/rawlsing` (private).  
**Exact user-sealed startup:** `8cebf47b1706fc2f86d055632a43cc8cfdc3b601`.  
**Assigned branch:** `agent/reviewer-sorok-r3-hq299-rsr-occurrence-outbox-independent-r1`.  
**Commission:** `WORKER_COMMISSIONS/SOROK-R3-HQ299-RSR-OCCURRENCE-OUTBOX-INDEPENDENT-R1/00_COMMISSION.md`, directly fetched in full at that exact startup (Git blob `8e328d6bcd92d92e89c202477e1ccbc1829cda47`).  
**Initial remote ref:** GitHub `refs/heads/` confirmed **exactly** the sealed startup before reviewer writes. HQ299 parent `5c59fb409d5f08312c19b936738eb4410dbd4f26` is not substituted for the worker startup.

## 1. Sources and proof hierarchy

Read Sorok `00_READ_ME_FIRST`, `00B`, `00C` (including mandatory §5A Browser-native S1 suitability) and `00D`, plus `SOROK_PRODUCT_CONTROL_ROOM/HQ299_SIX_RETURN_INTAKE_AND_INDEPENDENT_COURT_ORDER_R1.md` at HQ299 parent `5c59fb…`. Wrote only in this worker return. No general Sorok/full-project regrok or change to HQ controls.

Candidate:
- Initial SR/semantic S01–S28 frozen independent spec `WORKER_RETURNS/SOROK-R3-POSTASTRA-SR-BINDING-OCCURRENCE-SURFACE-R1/03_CRASH_RETRY_GHOST_EVENT_FALSIFIERS.json`, `99f2e7128a8417dfeaa39468c45ba65f6958c061`, exact Git blob **`782ba75ee94f24908100b1f3464e7035497d546c`**. Copied unchanged here as `FROZEN_S01_S28_ORACLES.json`.
- HQ298 SR `8da45605c267ea60b664d00fc8444d8c9b007628` `00_RETURN.md`, `01_EVIDENCE.json`, `02_MANIFEST.json`, `outbox_prototype.py`, `test_sr_28_falsifier_court.py`, `03_BROWSER_EXECUTED_F2_SUPPLEMENT.md`, `04_BROWSER_28_CASE_SHA_INDEX.md`, `05_BROWSER_ENVIRONMENT_PASSPORT_SUMMARY.json`. Original source/test files are copied byte-for-byte in this return; direct remote and locally calculated native Git blob SHA-1 equality is verified.
- Original HQ298 standalone prototype's 28-test pass is a **narrow literal test outcome**, whereas a distinct HQ298 supplemental Browser prototype author-reported 31/31 and 28/28 from a separate archive. That supplement was **inspected** but its binary tar/second source implementation was **not reexecuted** by this reviewer; do not conflate it with our independently executed SR original/cold court.
- Triggered accepted-owner read: `ADP-019 / V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0` blob `5c38772ea193e5a3f20da23c16df086a153ab2f2`, `CAN-022 / V2_RENDER_ADMISSION_PROMPT_CONTRACT@1.0.0` blob `5b85c67f74112c19fa72acf2cd4de226f73ecf47`, `CAN-025 / V2_TO_V3_EXTERNAL_EVENT_PACKAGING_CONTRACT@1.0.0` blob `7bf380f5e6cef1f7a0d28d5ecc1ae65e5fde9ebb`, and `CAN-015 / V2_PHENOMENOLOGICAL_PROJECTION_RULE@1.0.0` blob `cd976fb9b3b84b09068a57607adea09a33abf4ad`, all fetched at HQ299 base. These are governing **authority documents**, not loaded executable owner modules.

## 2. Verified S1 runtime and exact execution

A **new**, independently verified Python/shell runtime was available, not merely a Browser tab or GitHub connector. `python --version` = **Python 3.13.5**; `python -m pytest --version` = **pytest 9.0.2**; `git --version` = 2.47.3; Node v22.16.0; Linux filesystem writable; `subprocess` and `os._exit(79)` verified by the cold tests. No full private checkout. Anonymous GitHub raw URL acquisition DNS failed; the exact two small source-free files were staged from authenticated GitHub connector content, then verified with native `SHA1(b"blob " + length + b"\\0" + bytes)` Git hashing. `outbox_prototype.__file__` imported from the explicit staged module. Sanitary marker environment ID `RSR299-S1-1d4bb671a107`, epoch `RSR299-COLD-352d6842b968`; marker digest in `environment_passport_delta.json`. Do not infer next conversation's runtime remains alive.

**Actual commands/exit codes (real independent run):**

| Test | Command | Executed result |
|---|---|---|
| First discriminating S27 | `python -m pytest -q test_sr_28_falsifier_court.py::test_s27_material_move_needs_world_owner --junitxml=first_s27.xml` | **1 passed, exit 0** |
| Original frozen authored suite | `python -m pytest -q test_sr_28_falsifier_court.py --junitxml=original_28_junit.xml` | **28 passed, exit 0** |
| New independent boundaries | `python -m pytest test_rsr_independent.py -q --junitxml=independent_raw_junit.xml` | **5 passed, 12 FAILED, exit 1** |
| Independent cold subprocess replay | `python -m pytest -q test_rsr_cold_replay.py --junitxml=cold_junit.xml` | **2 passed, exit 0** |

The independent suite's 12 failures are retained as **actual** failures. No `xfail`, `skip` or changed original acceptance oracle was used to turn them green. Complete case-by-case executed statuses and raw JUnit/stdout SHA256 hashes are in `01_EXECUTED_REVIEW_MATRIX.json`; exact executable sources and reproduction commands in `03_REPRODUCE_AND_JUNIT_CUSTODY.md`. Original full raw JUnit/stdout is preserved as a user-available compressed conversation attachment, integrity hash in `03`, not falsely represented as GitHub-uploaded raw XML.

## 3. Independent scientific adjudication: 28 literal PASS ≠ 28 frozen-law PASS

Five particularly discriminating cases:

1. **S27 contradicts its frozen oracle.** Frozen S27 stimulus is `world_authority=MISSING`, expecting `HOLD_MISSING_MATERIALIZATION_OWNER`, `mug_remains_counter`, `no_emitted_move`. The copied original S27 test places string `world_owner="NADIA"` in payload, accepts it without competent world authority, changes mug position `table -> hand`, and **asserts that world change as PASS**. This is a *direct original-test-to-frozen-oracle mismatch*, not a hypothetical future concern.
2. **S28 tests rollback by explicitly restoring a pre-admission snapshot**, instead of checking the oracle's missing causal time `DEFER_MISSING_CAUSAL_TIME`. Sourcefree `OccurrenceLedger.admit` can admit a candidate with `causal_time=None`, confirmed by one of the independent REDs. A test that manufactures its own rollback is not proof of crash-safe causal-time refusal.
3. **S17 is in-memory only**, with no actual external crash, durable event+outbox transaction or recovery. The independently executed `os._exit(79)` replay shows that manual atomic JSON persistence by *our harness* permits one-entry restore, but a crash after unpersisted in-memory `admit` loses the event. This distinguishes `recoverable saved fixture` from `ADP019 atomicity`.
4. **S19 appends actor memory to `world_state`** merely after admitted utterance, without testing ADP016 event/perception/encoding effect authority. S04 checks the self-equality of one event hash rather than contrasting user-specific rendered allowlists; neither is independent full membrane evidence.
5. **S23 accepts an empty payload as an admitted occurrence**, but frozen S23 compares `VALID_EMPTY` and `UNAUTHORIZED` and requires that missing authority not silently become a no-op. The test does not exercise that discrimination.

Other S08–S14 and S20–S26 cases often verify locally constructed booleans/collections rather than invoking a real rejected semantic producer; they can be kept as narrow scaffolding but cannot be reported as exact owner/refusal proof.

## 4. Twelve actual independent REDs

The independent strict tests prove that this **standalone candidate** has these unclosed behaviors:
- `UserProjection.perceive` can record actual perceived status with **no** delivery and **no** user opportunity;
- `UserProjection.offer` can offer unknown, unadmitted occurrence IDs;
- `Outbox.emit` can queue unknown occurrence IDs;
- snapshot/restore both fails to revert uncommitted opportunities in the same instance **and** fails to preserve committed opportunity on a fresh one;
- aliasing of input payload, mutable event view and shallow snapshot can change a supposedly committed event **after** content hash is fixed;
- same candidate ID+payload but different `source_refs` is treated as identical admission, obscuring source/authority changes;
- an untyped utterance proposal with side-car `objective_employment_transition="quit"` is admitted as an event, despite no world-owner rule, even while the isolated `world_state` remains unchanged;
- missing causal time and empty source/authority references do not block admission.

These are 12 independently executed failures, not proof that the accepted ADP019/CAN022/CAN025 implementations have these bugs. Our positive controls also show **5 precise bounded invariants**, including original candidate replay idempotence, false `"I quit."` testimony not directly changing the synthetic employment state, ACK not automatically marking perceived, and actor-specific offer possibility. The fact that `Outbox.ack` does not itself call `UserProjection.perceive` is good but does not prevent a client from directly calling that unguarded method.

**Known scientific ceiling:** Without an accepted issuer/transaction/cross-client context, one cannot simply strengthen an isolated class by assumption. No physical event was simulated as accepted world truth; no first-person epistemic permission or user phenomenology was measured.

## 5. Cold replay and exactly-once distinctions

Two real fresh-process tests:
- After `rsr_cold_replay.py` manually serializes one admitted occurrence plus emitted intent to JSON using `os.replace`, it forcibly exits 79. Another process reloads and re-admits the same candidate with stable `OCC-0001`/ledger count=1, delivers as `DELIVERED_UNACKED`, and subsequent new process ACKs while `has_perceived(user-A)` stays false. `COLD_HARNESS_PERSISTED_REPLAY=PASS`.
- A second case persists only an empty baseline, admits a new occurrence **in memory**, exits 79 before a harness save, then reloads baseline. Event count and outbox are zero. `IN_MEMORY_ADMIT_DURABLE_AFTER_CRASH=FALSE`.

Neither case proves a production event/cursor/outbox atomic commit, fsync, cross-worker serializability, provider callback, per-client delivery ID semantics, or physical exactly-once delivery. A stable event ID supports **deduplication of effects under a correct owner**, not exactly-once network transport or evidence that any particular human perceived an artifact. ACK is not perception. An opportunity is not perception. The exact actual user experience is unmeasured.

## 6. Recommendation and independent owner actions

**Recommendation:** `ACCEPT_SCOPED_REPRODUCTION_OF_ORIGINAL_SR_F2_TESTS`; `HOLD_ACCEPTANCE_OF_FULL_ADP019_OCCURRENCE_OUTBOX_USER_MEMBRANE`; `DO_NOT_SELF_ADOPT`.

The owner-specific action register `02_OWNER_ACTION_AND_REVIEW_REGISTER.md` distinguishes the specific blockers and the smallest bounded next work:
1. An accepted ADP019+CAN025 implementation owner must bind the complete exact immutable envelope (proposal ID+payload+authority/release/candidate/artifact/causal-time/participant/parent refs) to an atomic admission receipt and event/outbox intent, with stable cursor/event identity and persisted crash boundaries. No candidate payload string is authority.
2. The objective world/material effect owner must approve real object existence and a valid movement/causal rule separately. No material mutation from utterance/renderer testimony; false speech acts are true utterances only.
3. The client/outbox owner must support per-viewer/per-delivery stable IDs and ACK/retry, reliable opportunity tracking/restore, explicit knowledge/perception authorizations and lost-ACK duplicate demonstration. Transport exactly-once is not assumed.
4. A distinct independent oracle custodian/owner reviewer must adjudicate S27/S28/S19/S23 mismatches **without editing the frozen S01–S28 specification to match candidate outputs**. Future independent execution should include actual owner-code imports and external state/cursor checks at its granted grain.

No competent accepted-authority conflict requiring an I3/architecture reopen was found. The blocker is stronger implementational coupling and evidence-grade adequacy. No full V3, source, actor, renderer or N11/N12 has been executed or approved here.

## 7. Environment, costs, changes and return constraints

- **Actual model/renderer API calls:** 0; **original survey/source accesses:** 0; **V3 actor execution:** 0; **physical world changes:** 0; **canonical/shared HQ mutation:** 0; **new accepted ADP/CAN semantics:** 0.
- **Provider/model:** GPT-6, High requested; actual user effort/usage/cost/window not inspectable. Python subprocess tests do not use paid LLM calls. Additional observed incremental cash/credits: UNKNOWN, not asserted zero billing.
- **Execution material:** all six pinned/executed Python+oracle files, human review and machine-readable failure ledger, immutable run/JUnit hashes and relative reproduction steps are committed in this return directory. The precise temporary runtime marker is not itself a distributed persistent fixture. No credentials, complete user account path, private respondents or binary source files committed.
- **Independent reviewer:** independent of SR author; **not** automatically an ADP019/CAN022/CAN025 owner issuer or accepting HQ. A later separate competent implementation/review decision is still required.

**Final remote GitHub HEAD:** must be read directly after this report's commit, and exact changed-path compare vs sealed `8cebf47b…` included in final chat return; never embed a guessed self-referential future SHA in this file.

**Terminal:** `HQ299_RSR_ORIGINAL_28_EXECUTED_PASS__INDEPENDENT_12_EXECUTED_REDS__TWO_REAL_COLD_SUBPROCESS_REPLAYS__SOURCEFREE_F2_ONLY__SEMANTIC_AND_TRANSACTION_ACCEPTANCE_HOLD__NO_ADOPTION_OR_WAKE`.
