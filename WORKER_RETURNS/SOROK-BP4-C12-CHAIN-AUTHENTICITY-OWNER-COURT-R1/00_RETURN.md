# SOROK BP4/C12 — chain authenticity, completeness and writer/reader compatibility court — R1

## Identity, host and model

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-bp4-c12-chain-authenticity-writer-compatibility-r1` |
| Sealed startup | `342164a09e10aa70812299c12386ed0923308228` |
| Commission head before this return | `37b3e62a6b30da028531e2d94e6f33aabd1dd72a` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-bp4-c12-chain-auth-r1` |
| Host | macOS x86_64; Python 3.11.3; pytest 9.0.2; SQLite 3.40.1; stdlib only |
| Actual worker/model | OpenCode / `opencode-go/deepseek-v4.1-flash`; no harness or model switch |
| User-selected editor/model pair | No verified local Codex / GPT-6 High selection was supplied or proven. The running worker is the model above. Actual MAX/High effort is not independently verifiable from inside this session. |
| Write scope used | Only `WORKER_RETURNS/SOROK-BP4-C12-CHAIN-AUTHENTICITY-OWNER-COURT-R1/**`; candidate code was executed in throwaway checkouts and is carried as an exact patch in `03_...md` |
| Native authority | none; all C12/C9/BP4 results are TEST_ONLY sourcefree |

The four F2I artifacts, both F2 artifacts, BP2P4J `5b3e657…`, BP2P4JI `3212d716…`, JOIN-E `7bf2da3…`, C9-R3 `1e99681f…`, the C12 fork repair `68b05865…`, PRE-MAIN `299f41e9…` and HR1 `40df1e6…` were read from immutable Git objects. PRE-MAIN contains no `bp2p4/c12_verify.py`; no old JOIN-V acceptance was transferred.

## FINDING

1. **The F2 episode-preimage repair is real and independently reproduced.** A valid SAY row hashes the episode before appending `episode_id`. The original BP2P4J verifier excludes only `hash`, so it returns `episode:0:body_hash_mismatch` on an intact row. The F2 candidate blob `c1699c8da5e944ed079708e272c3af50d5a30a44` excludes `hash` and `episode_id` and returns green on the same row. BP4 `C12Store.verify` remains separately self-referential (`episode:0`, `world_event:0`, `world_event:1`, `checkpoint:0`, `checkpoint:1` on a valid store).
2. **The preimage fix does not close authenticity or completeness.** On the same chain assertion, an independently executed probe shows that raw SQLite deletion, a self-consistent injected world event and a fully rehashed episode body/id/hash are all accepted by content verification (`ok == true`). Only an out-of-band chain digest changes; there is no authenticated anchor.
3. **The fork/perception defect is reproduced and bounded.** The original BP4 fork clock excludes perception clocks; a perception-only suffix at clock 11 is not copied when the non-perception last clock is 10. The `68b05865…` candidate and this candidate bind all four tables, include perception clocks, use a `BP4_C12_FORK_ROOT@2` prefix with counts/row identities, and make the copy atomic. Legacy roots are held, not certified.
4. **Writer/reader versions are not checked by the original store or by F2/68b058.** A hypothetical `BP4_C12_STORE@2` database is read blindly. This candidate adds a reader guard that fails closed on unknown schema and on legacy/non-lawful episode ids.
5. **C9 and C12 are two separate stores with no cross-database ACID.** The C9-R3 outbox/watermark protocol is the only recovery contract: C9 commit and outbox are one SQLite transaction; C12 projection is idempotent; `CLEAN` requires exact mirror receipt plus `ACKED`; a crash leaves `PENDING`/`PROJECTED`/`SYNC_HELD`, never a silent clean state. The C9 `c12_fork_guard` remains conservatively `FORK_HELD` for a perception-only suffix and does not adopt the repaired store.
6. **No owner-issued anchor exists.** This worker did not invent a key, signer, issuer, secret or fixture oracle. `check_anchor` returns `OWNER_ANCHOR_REQUIRED`/`OWNER_TRUST_ROOT_ABSENT`/`ANCHOR_ROLLBACK_WINDOW_UNPROVEN` until an original owner or independent anchor custodian supplies a real trust root and monotonic anchor.

## INTERPRETATION

The F2 repair answers a **hash-preimage syntax** question: the verifier now reconstructs the bytes the writer actually hashed. It does not and cannot answer **who wrote the row** or **whether rows are missing**. Those are custody and completeness questions. Content hashing verifies the attacker's own preimage when an attacker can write SQLite directly; a self-consistent forgery is indistinguishable from a legitimate row without an external authenticated witness. The C12 fork repair answers a **prefix consistency** question, not a writer-authority question.

The correct engineering outcome is therefore split: a bounded sourcefree candidate can make content, episode-id derivation, schema version, fork prefix/perception clocks and fail-closed anchor refusal verifiable; the anchor itself must be owner-issued. That part remains HOLD, not PASS.

## HQ ACTION

1. Accept the F2 preimage candidate `c1699c8d…` as the minimum compatibility repair for the BP2P4J verifier, only at the exact base `5b3e657…`, subject to owner replay.
2. Route the new `C12_GUARD_READER@1` candidate (content + derived-id + schema + fork + anchor contract) to the original BP4/C12 owner and a distinct source-qualified reviewer. Do not adopt it on this return.
3. Require the original BP4/C12 owner to decide: (a) retain or repair upstream `C12Store.verify`; (b) accept `BP4_C12_FORK_ROOT@2` and perception-inclusive fork clocks; (c) approve or reject the `TEST_ONLY_BP4_EP_` sole derivation and legacy migration policy; (d) nominate the real anchor issuer/custodian and monotonic counter.
4. Require the C9 owner to decide whether `c12_fork_guard` may return `FORK_READY` for a perception-only suffix after the store repair, or must remain `FORK_HELD`. This return does not relax it.
5. Keep PRE-MAIN, PR #514/#516/#519 and all original branches unchanged. No production, native C12, C11, CAN/ADP, Pyat, Rule A/T or person claim is granted.

## OWNER

Original BP4/C12 store owner; original BP2P4J verifier owner; C9-R3 actor/mirror owner; original source/custody owner for any anchor; incumbent Sorok HQ for intake. The independent reviewer must be distinct from this worker and from the original authors.

## Three courts

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `PASS_SCOPED_CONTENT_SCHEMA_FORK__AUTHENTICITY_COMPLETENESS_HOLD__NO_NATIVE` | Valid SAY green; original BP4 RED reproduced; 11 guard tests and 48-test combined suite actually run; tamper/legacy/schema/fork/atomicity negatives pass; deletion/injection/rehash remain content-green and anchor-required |
| SCIENCE | `HOLD__TEST_ONLY_E2_ONLY__NO_NATIVE_PRACTICE_ACQUISITION` | No original developmental rule, person, practice acquisition or native source was issued. The finite sourcefree E2 consequence survives; nothing native is inferred. |
| AUTHORITY | `HOLD__NO_ADOPTION__ORIGINAL_OWNER_AND_INDEPENDENT_ANCHOR_REQUIRED` | No owner replay, signature, key, anchor, merge, production receiver or native grant. The author is not the reviewer. |

## Actually executed results

| Check | Result |
|---|---|
| Original BP2P4J suite at `5b3e657` | **32 passed, 1 skipped**; the skip is typed `BP2_ORIGIN_RUNTIME_ABSENT (local-only literal cross-check)`. F2's reported `33 passed` is not reproducible in this checkout; no assertion was waived. |
| Focused valid-SAY test against original verifier | **1 failed**, `episode:0:body_hash_mismatch`; exit 1 |
| F2 candidate overlay, full suite | **37 passed, 1 skipped** |
| F2 + guard candidate, full suite | **48 passed, 1 skipped** |
| Guard candidate alone | **11 passed** |
| Severance probe | **10/10 proved** (7 primary + 3 supplementary), same named assertion, baseline red=false / cut red=true / restore red=false |
| `68b05865…` fork-integrity suite | **8 passed** |
| C9-R3 suite at `1e99681f…` | **11 passed, 4 skipped** (`S36 source unavailable` once, `C12 source unavailable` three times). The C9 return's `15 passed` is not reproducible without the hard-coded external S36/C12 sources; these are typed HOLDs, not PASS. |
| Independent adversarial probes | valid SAY green/upstream red; raw deletion green; injected world event green; fully rehashed forgery green; legacy id refused; chain/anchor payload changed in every forgery case |

## First real consumer and native production

First real test consumer of the F2 repair remains the BP2P4J joined security/audit court (`tests/test_joined_security.py`) plus the new focused regression. First consumer of this candidate is the new `tests/test_c12_guard.py`; first C9/C12 consumer contract is the C9-R3 `c12_fork_guard` / mirror court. **No native production consumer, deployment, original owner receiver or source-native C12 issuer is proved.** The C9 C6 actual-C12 tests were NOT RUN because their hard-coded source paths were absent.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** independent F2 RED and GREEN; upstream disagreement; raw deletion, injection, full rehash, legacy id, perception tamper; schema-version fail-closed; fork perception suffix and atomic copy; legacy fork hold; cold reopen; 10/10 severance; exact blob custody; bounded candidate patch; exact owner HOLD contract for anchor and migration.
- **REMAINING:** original owner replay/adoption; owner-issued anchor and monotonic counter; upstream BP4 verifier disposition; legacy migration decision; C9 guard relaxation decision; fresh C9/C12 consumer run with real S36/C12 sources; independent review.
- **CRITICAL BLOCKERS:** raw SQLite deletion, self-consistent world-event injection and fully rehashed episode forgery are content-green; no authenticated anchor; C9 C6 tests skipped for missing sources; no native receiver.
- **LARGEST PRODUCTIVE MOVE:** original BP4/C12 owner replays candidate `c1699c8d…` + `C12_GUARD_READER@1` at `5b3e657…`, then decides the anchor issuer and fork/version policy.
- **FLIGHT:** sourcefree local Git/SQLite/Python only; no model/harness switch; no PRE-MAIN/PR mutation.
- **DELTA:** the preimage defect is no longer conflated with completeness; writer/reader version and fork-perception boundaries now have executable fail-closed tests and an exact owner contract.

## STOP / HOLD

`IMMEDIATE_OWNER_SCOPED_SOURCEFREE`; `ORIGINAL_ANCHOR_GRANT_HELD`. The candidate is not adopted. Missing source permission is reported as typed HOLD, not made-up PASS.

## Artifacts

- `00_RETURN.md` — this return.
- `01_C12_WRITER_VERIFIER_COMPATIBILITY_MATRIX.json` — version/fork/two-store/anchor matrix.
- `02_ANCHOR_COMPLETENESS_AND_FORGERY_FALSIFIERS.md` — exact attacks and residual boundary.
- `03_BOUNDED_SOURCEFREE_CODE_OR_EXACT_OWNER_HOLD.md` — exact patch and owner HOLD contract.
- `04_COMMANDS_BLOBS_AND_INDEPENDENT_REVIEW_HANDOFF.json` — commands, blobs, exits, NOT_RUN, handoff.

The final pushed branch SHA is reported externally after the ordinary push; a commit cannot contain its own final SHA. No self-adoption.
