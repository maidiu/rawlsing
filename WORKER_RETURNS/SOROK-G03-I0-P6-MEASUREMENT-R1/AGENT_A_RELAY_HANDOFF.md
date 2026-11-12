# G03-I0 — AGENT A ADVERSARIAL RELAY, B→A constructive return

Commission [#949](https://github.com/maidiu/rawlsing/issues/949), including its R3C G1–G5 amended receiving contract. Original unabridged Agent A and B personae: `SOROK_PRODUCT_CONTROL_ROOM/ADVERSARIAL_IMPLEMENTATION_20261112_R1/01_USER_ORIGINAL_DUEL_PERSONAS_UNABRIDGED.md` at PR #938 frozen `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.

## 1. Source custody, exact cut and branch

**B frozen full parent:** `aa157f23cf7d6284c982595295301036145b7cdf` ([PR #956](https://github.com/maidiu/rawlsing/pull/956)). **A original frozen parent:** `b4f26fec056f5cb481a0b4e417e7a29bae833546` ([PR #953](https://github.com/maidiu/rawlsing/pull/953)). **Relay branch:** `agent/sorok-g03-i0-a-relay-typed-sqlite-20261112-r1`, uniquely created from B exact SHA, no B/A upstream writer branch touched. Selected source correction cut `2b1a115168be94479e3e12334fc9d23f3d0163b6`, final immutable HEAD to be verified separately after documentary commits. Changes remain additive new relay tests and workflow plus small edits to B's `measure.py` and `read_receipts.py`; none to P3/P4/P5/P6 or actor/world owners. No Mac/OpenCode host-level writer lease was inspectable; isolated GitHub branch custody is **not** a claim of global mutex ownership.

## 2. Accepted opponent victories

B correctly demonstrated: A's equal-size state oracle was not integrity evidence; A's external index excluded manifest; actual refused P6 can physically rewrite a SQLite database without changing its logical table content; A's cold-reopened aggregate must derive from actual observed clock; untracked sources cannot silently pass a clean source claim. B preserved real original P6 subprocesses, positive/negative/cold receipt first consumer, correct Linux wait4 direct-child CPU/RSS scope, UNOBSERVED provider/cost, and failure denominator. B's exact final Actions [#43278614274](https://github.com/maidiu/rawlsing/actions/runs/43278614274) succeeded: 23 hostile tests, 5 real P6 attempts, raw artifact #13972011801. **All preserved**, not replaced.

## 3. Independently established SEV-1 defect — noninjective SQLite logical witness

B's `sqlite_logical_digest` converted BLOB via `v.hex()` into an untagged Python string. In actual SQLite `p3_records.payload_json TEXT NOT NULL`, storage class BLOB bytes `0x4142` becomes string `"4142"`; subsequent committed UPDATE to TEXT `"4142"` changes the stored value, but B's normalized logical digest is identical. This is an exact logical-change false negative. Verified using a copy of the **real P6-generated** `state/actual-p2/p3_psyche.sqlite3` extracted from B's successful sourcefree artifact #13972011801, in a separate local temporary directory. A's local independent differential against B algorithm showed unchanged B hash `95382cbbabd8aa3e4352d308b4fd4c3b352c21e12aa5de7c0232d604c140d865` versus distinct typed hashes `234b19f9cf9e2282d743cd2ce5d7aafed542aaf225a759c50107ee487d49d828` and `1a4764c2a5569bc55394aca1e19219ab39641bf16777f3956ed705df03c8ddd3` after committed/checkpointed updates.

A second, related finding: the original P6-generated P3 SQLite database is in WAL journal mode. B's `mode=ro&immutable=1` **does not see committed uncheckpointed WAL row updates**. Direct read-only `mode=ro` saw changed BLOB/TEXT content while `immutable=1` returned the pre-WAL main-file version. B already bounded the witness to closed/checkpointed SQLite. The source-compatible repair must refuse nonempty pending WAL rather than silently call stale rows logical truth. This is not a new SQLite implementation or a universal transaction claim.

## 4. Construction and hostile test

**Reader and writer V3:** `SCHEMA=G03_I0_REAL_P6_V3`, `STATE_LOGICAL_SCHEME=G03_SQLITE_TYPED_ROWS_AND_OTHER_CONTENT_V2`. Both independent code paths normalize SQLite primitives as tagged `["NULL"]`, `["INTEGER", string]`, `["REAL", float.hex()]`, `["TEXT", value]`, `["BLOB", bytes.hex()]`. This removes the demonstrable BLOB/TEXT alias without modifying database data or P6. Both refuse a nonempty `p3_psyche.sqlite3-wal` during logical snapshot; writer reports `UNOBSERVED/sqlite_uncheckpointed_wal` and denies false positive while reader emits `SQLITE_UNCHECKPOINTED_WAL`. B's V2 evidence remains frozen and readable with B's V2 reader; no retroactive regrading.

New `test_agent_a_relay.py` provides three independently source-relevant cases: direct SQLite BLOB→TEXT collision; same collision against **original P6's actual generated P3 database** (not mocked owner), with explicit SQLite checkpointing; and a committed uncheckpointed WAL which must be refused rather than reported unchanged. Existing 23 A/B cases retained. New relay-only workflow executes these, original B/A tests and the exact P6 five-child/reader with raw artifact upload, when GitHub Actions runners are operational.

**Material execution boundary:** the container had no internet/git clone access, so this session did not execute the final modified `measure.py` + `read_receipts.py` against a full local repo. The actual stored SQLite bytes were independently available from B's downloaded genuine GitHub Actions archive and were mutated/tested using Python sqlite3; that *differential* is executed evidence but **not final-head CI**. GitHub Actions relay jobs starting [#43286729711](https://github.com/maidiu/rawlsing/actions/runs/43286729711) and subsequent runs across SOROK and independent PYAT workflows all failed in 2–3 seconds **before runner allocation** (empty steps, `runner_id=0`). Manual retry also failed before any executed command. These are runner-infrastructure failures, not tested RED or GREEN judgments on the patch. Do not upgrade to `S2` acceptance until a clean host reruns source-exact tests plus actual P6 and an independent G5 reviewer does their court.

## 5. Refuted, incomplete and new attack surfaces

- **No refutation of B's original A defects.** They were genuine and preserved.
- **Incomplete B victory:** SQLite row hash was stronger than bytes, but untyped conversion was still noninjective. Type changes were invisibly normalized.
- **New material false claim:** `immutable=1` is not an all-journal live SQLite logical snapshot. The existing boundary was checkpointed/closed; the repair now enforces that boundary.
- **Remaining valid B limits:** physical SQLite page churn is not identical to semantic actor development; zero provider configuration does not imply authenticated zero usage; no process-tree resource tracer, real billed token costs, cold kernel cache, G02 cohort, native psychogenesis, human validation or protected merge.
- **Further independent attacks:** coordinated forged index and manifest when external digest isn't separately trusted; source-external Python dependencies; inode/snapshot races; transient peak state bytes; SQLite sidecar manipulations after the measured close; live WAL concurrency beyond this intentionally fail-closed witness; false cold cache conclusions.

## 6. Required replay/receipt status under #949 R3C

G1 source contract, seven mandatory case IDs and base are reconstructed, and no owner change occurred. B exact final `aa157f23...` passed its own G1–G4 evidence; the new A V3 code requires its **own** real runtime verification. The local P6-derived SQL differential establishes this *specific* defect and algorithmic correction, not full G2–G4. **G5 = NOT_RUN**, no self-acceptance. Current integration `UNMERGED`, scientific and actor authority HELD, full G03 `NOT_EVALUATED_G02_MISSING`.

The correct open disposition while GitHub Actions runners refuse to allocate is `HOLD_EXTERNAL` for final V3 executable verification, rather than `READY_FOR_RECEIVING` or `ACCEPT_SCOPED`. Once a real host returns, execute exactly one rerun at the frozen HEAD and one independent nonauthor G5 pass; no new dueling bureaucracy.

## 7. Rejected alternatives

- Do not preserve BLOB/TEXT type erasure merely because no native psychological writer should generate malformed JSON; the receipt witness must distinguish real SQL storage transitions.
- Do not use `PRAGMA wal_checkpoint` in the measurement reader as a hidden state-writing repair. Refuse uncheckpointed evidence at this bounded cut.
- Do not replace B's path-sensitive physical/logical state distinction with raw file hashes or byte-size equality.
- Do not invent completed CI/CPU/RSS receipts for this modified source or present B's older passing run as V3 proof.
- Do not broaden to G02 root population, new scientific authorities, source families or protected integration.

## 8. Agent B's next legitimate challenge

Attempt a physical, checkpointed SQLite state transition whose semantic rows differ but the V3 typed hash stays unchanged; show a real P6 regression under the patched reader; or establish that V3 WAL fail-closed makes the existing five-step sourcefree P6 impossible at a clean runner. Those would warrant an actual code repair. A generic uncheckpointed WAL or BLOB/TEXT collision no longer deserves an authoritative `UNCHANGED` result.

**Author A relay: code committed; local real P6-DB differential executed; final-head sourcefree S2 execution HELD_EXTERNAL pending runner. G5 NOT_RUN. G03_FULL NOT_EVALUATED_G02_MISSING.**
