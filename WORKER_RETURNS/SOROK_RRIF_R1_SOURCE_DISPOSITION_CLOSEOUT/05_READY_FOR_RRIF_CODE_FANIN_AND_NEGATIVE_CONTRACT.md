
# RRIF-R1 — one real sourcefree receiving tranche and non-negotiable negative contract for RRIF-R2

**This is the engineering Handoff; NOT delivered executable fan-in.** A sourcefree-compatible candidate route exists but mixes versioned writer/reader lineages. The RRIF-R2 engineer owns the actual S2 implementation/testing on the user-selected harness; RRIF-R1 is documentary S0–S1 only. Neither original actor science, C9/C12 production owner custody, Pyat source permission, nor human A5 is issued here.

## The one cut to attempt — sourcefree I1 person→B/C10→C9/C12→A-limited encounter

**Terminal first consumer**: read-only `cp_a5.encounter.EncounterReader.ask` and independent `c9c12_reader.read_composite` reporting A-known events / actor C9 snapshot and C12 continuity at a single accepted root/branch/epoch without changing the underlying sourcefree event records. The caller must distinguish `COMPOSITE_OK__EXTERNAL_ANCHOR_REQUIRED` from fully source-qualified native acceptance. If the two stores cannot be made compatible without changing historical behavior, return a named `C9C12_CUT_CONFLICT` with an exact fault receipt, *not* a fabricated green or a second invented actor.

### Exact source assets to reuse, not reproduce from narrative

| Layer | Exact source / blob | Actual implemented call | Important limitation |
|---|---|---|---|
| Base actor/material/C12 root | I1 `7d44e30064f8e873e1a3ff9cb05fe75456756b88`, `bp2p4/i1_product.py` → `GuardedJoinedProduct` | `other()`, `owner_material_readout()`, guarded same-root C12 reopen/fork | Sourcefree B at synthetic actor/event grain, no native owner; actual I1 54→56 B cash and 3→4 performed units |
| B/C10 targetless same root | B-F1CR-R2 `bf3273c294c704ad7c631559b9866d351bb4f103`; `candidate/targetless_i1_bridge.py`, blob `202478dc65a64c14aad20a305968984056732629` | `TargetlessGuardedJoinedProduct` inherits I1 and persists `targetless_c10.json`; `targetless_read()` with A public view | Requires R5 reconstructed F1CR, original patch absent; no C9 target, E2 or practice merely from B refusal |
| B/C10 producer | same BF source `candidate/targetless_c10_consumer.py`, blob `45997b198e6c0f65b54e523d9b1d6fda09e45ac2` | `BWorld`, `BAction`, `TargetlessC10Ledger`; actor-targetless states | Stock/replenishment and no forced NO_CHANGE exact negative contract |
| C9 actor schema/writer | C9C12-R2 `c78404724052496fdec8608c8b0e833c0f7c4ecc`; `candidate/c9_actor_r3.py`, blob `b9000cdb1a4e3e3be6de0dfb1690515f2984a122` | `C9_ACTOR_AUTHORITY_R3@1`, actor/epoch/head/version/outbox, optional mirror | **Not interchangeable** with BP2P4J `C9R CandidateStore`; supports `BP4_C12_STORE@1`, not @2 |
| Guarded BP4 C12 reader | same cut `candidate/c12_guard.py`, blob `8f629c29228cfc736c195db501dd100f2ac30f75` | `GuardedC12Store.verify_store`, append row/branch clock, immutably bound actor/body origin, external anchor payload | External owner anchor not issued; `check_anchor(None)` is `OWNER_ANCHOR_REQUIRED` |
| C9/C12 read composite | same cut `candidate/c9c12_reader.py`, blob `db38d05d5edab7ad72cc003807945e056f2b0779` | `read_actor_snapshot` + `guarded_c12_cold_read` → `read_composite` | Returns held outbox/mirror/anchor status, must not invent ACK or proof of E2 at C9 |
| A3/A5 bounded perception | CP-A5-R2 `913765328e4fab12b150ea01421ed6b445158184`; `candidate/cp_a5/encounter.py`, blob `8d388c2f10eec6b6d6ab0f3e5f1566b0053098e6` | `EncounterReader.ask` read-only from A's C12 perception rows; B private market remains `UNKNOWN` | Its own CP-A5 historical candidate contains C9 writer blob `b900...` but **does not prove the guarded C9C12 C12 cut or external anchor simultaneously** |
| Optional derived historical material check | V3CORE `b5cb3f917402b992d7cbe933af0b378d2b37cbfd`; `v3core_adapter.i1_consumer.project_actual_market_event` | Check I1 actual material event from same root changes bounded material index, read-only V3 compatibility | Secondary regression after core route; only 3/19 yearly steps admitted, 16 held; no native psychological defaults |

**Earlier chain**: `BP2P4J JoinedProduct` + `R31JProduct.material_inspect/record_omission` + `R31ESession.say/do_help/ask_contact/attend/wait` → `JoinedSession.start/open` under the historical `fac064c9c3370d598e9b7469af652ae3504bc4ba` fan-in source. This is historical sourcefree functional capital, **not an accepted C9 R3B writer by implication**. Preserve actual 1:1 source/method equivalence where it exists; do not reimplement everything.

## The two presently incompatible lineages — exact version and hash gates

1. **C9 actor writer vs BP2P4J C9R:** actual test-only C9-R3B patched writer is blob `b9000cdb...`. The B2P4J candidate-store transaction is not the same schema, mirror, epoch or outbox. `read_actor_snapshot` checks `actor_meta`, branch+epoch, actor head version and semantic hash, held/final receipt binding, and outbox state. Select an **exact** writer @1 and test via read-only snapshot at that cut. Without a verified translator, reject mixing.
2. **BP4 C12 old/new and JOIN-E digest:** original/older JOIN-E consumes C12 source reported as `7bf...`, whereas newer repaired C9 reader pins `68b...` in the 2026-10-31 original/Neo code report. The current guarded C12 blob `8f629c...` is another explicit candidate (BP4R-derived), **not automatically identical** to either. Pin the actual writer and verifier object/tree, content and branch semantics at the same cut; refuse @2 absent original owner migration. A string prefix or equal schema field count is not evidence of byte/behavior compatibility.
3. **C12 verifier historical defect:** BP2P4J delivered verifier was self-referential; the separate `bp2p4/c12_verify.py` is the independent content/episode checker. RRIF-R2 must use an independent preimage-based verifier before claiming a real cold-reader proof. Repair the self-reference defect as bounded code; compare to source-mutation witnesses and correct immutable receipts, not by weakening tests.
4. **Anchor and outbox are separate from local correctness:** `C12_ACTOR_MIRROR_R3@1` optional mirror, projection outbox with PENDING/missing/ACK and external owner anchor are **different** objects. The repaired R2 candidate is allowed to return `C9_OUTBOX_HELD`, `C9_MIRROR_HELD` or `OWNER_ANCHOR_REQUIRED`; a locally invented test key is not owner custody. `COMPOSITE_OK__EXTERNAL_ANCHOR_REQUIRED` is a **sourcefree engineering read**, not owner-accepted canonical CAS.

## RRIF-R2 finite implementation sequence

1. **Lock the input hashes** above, exact B-F1CR and CP files, I1 common base and C9C12 reader/writer/C12 schema; independently verify the reader's declared schema and that the same root/branch/epoch can be traced through the adapters. Do not run historical untrusted arbitrary Python outside a safe isolated sourcefree S2 tree.
2. **Write only a bounded compatibility consumer** joining existing sourcefree I1 identity→B targetless C10 receipt→actual C9-R3B snapshot/read-only guarded C12→CP A-perception answer. Retain no second permanent actor store. If C9 source ownership cannot be wired without migration, produce an explicit `C9_OWNER_WRITER_SCHEMA_HELD` receiver and prove all unaffected same-root I1/B/CP paths; do not forge an @1 or ACK.
3. **Positive semantic trace:** real bounded test-only performed work (not a declared story) changes B's material and/or capacity; same-root C12 event count/episode hash changes; later separate-process cold reopen sees it; user A can identify only observed workshop/tool action while unseen B market action returns `UNKNOWN`.
4. **Mutate/restore** actual source file/preimage or state row one at a time, re-open cold and compare exact error and hash. The failures below are necessary **engineering** tests; full native science and human alpha remain separate.
5. Return exact Git SHA, changed-path manifest, executed commands/JUnit and duplicate source hashes, first actual caller/fixture and negative matrix, rollback boundaries and original science/anchor holds. No self-merge or unsupported data grant. Original qualified Sorok sourcefree reviewer inspects the newly returned SHA; the existing R3-IR remains index-specific.

## Mutation and regression matrix — no green by broad exception

| ID | Mutated input or behavior | Required outcome / typed refusal |
|---|---|---|
| N01 | Change live B history or previously accepted B digest | `LIVE_B_HISTORY_CHANGED` / `B_HISTORY_CHANGED`; no green after hash self-recompute |
| N02 | Change A or shared original history | `LIVE_A_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED` or `SHARED_HISTORY_CHANGED` |
| N03 | Replace B source with same-shape row or remove independently performed evidence | Actual B source severance changes output/capability or explicit HELD; no code path just echoing B hash |
| N04 | B tool absent/encumbered, access cut or time not available | `B_HAS_NO_TRANSFERABLE_TOOL` / `B_TOOL_TRANSFER_RIGHT_DENIED`; no fabricated participation |
| N05 | Stock=0 with no prior source-approved replenishment | Typed material refusal and 0 consumption; no negative stock floor/clamp or free goods |
| N06 | B REFUSE without performed actor/source, or silence/no proposal | `REFUSE_REQUIRES_PERFORMER` or `HELD`; no C9 target/E2/practice/utterance invented |
| N07 | No Rule T evaluation receipt or malformed `TRUE_NO_CHANGE` | `HELD_MISSING_RULE` / `NO_CHANGE_RECEIPT`; not certified learned practice |
| N08 | Inject B unobserved market event into A memory | `UNOBSERVED_EVENT_IN_MEMORY`; public/encounter response remains `UNKNOWN` |
| N09 | C12 episode body origin changed without branch column; fork prefix wrong | Reject immutable origin/prefix/hash; no same-count substitution accepted |
| N10 | Writer accepts a perception clock 11 then an episode clock 10 | `NON_MONOTONIC_GLOBAL_CLOCK` (original BP4R failure must remain historical) |
| N11 | Change branch `actor_ids` or `created_clock` while chain same | Anchor payload changes; absent external anchor gives `OWNER_ANCHOR_REQUIRED`, never accepted |
| N12 | Forge C9 actor head version/semantic hash/branch epoch | `C9_*_MISMATCH` or precise typed refusal, no stale head replay |
| N13 | Substitute `BP4_C12_STORE@2` writer or BP2P4J CandidateStore for C9-R3B @1 | `C12_WRITER_SCHEMA_UNSUPPORTED` or explicit compatibility HOLD |
| N14 | Remove C9 outbox or change PENDING to fake ACK | `C9_OUTBOX_MISSING` or `C9_OUTBOX_HELD`; no inferred mirror receipt |
| N15 | Modify C9 mirror or actor-other's private state during A read | Typed mirror hold/actor-local epistemic refusal; no hidden revelation |
| N16 | Call cold reader twice or different process after valid fixture | Exact same root state/event hashes and no write, no new episode |
| N17 | Fork child with divergent branch then request parent/foreign actor rows | Reject actor/branch/clock mismatch; no fork inheritance leak |
| N18 | Mutate historic annual 19-step schedule or relabel Pyat N11 as V3 M25 year | Scheduler invariant failure; no age/Enneagram/identity seed |
| N19 | Use historical E2 offered help as performed learned practice | Later E2 cannot claim new operation; source severance changes result |
| N20 | Restore exact preimage after every fault | Same original receipt/hashes, ordinary positive unchanged; historical RED retained separately |

**No-permission fallback:** If a native science/actor grant is absent, the result may still be a real reviewed **sourcefree TEST_ONLY consumer** with ordinary B and A-specific epistemic behavior. If no safe current C9 writer/reader cut can be selected from actual S2 evidence, the engineering verdict stays **`PARTIAL_INTEGRATION_WITH_EXACT_COMPATIBILITY_HOLD`**, not an endless project-wide veto.

## Immediate ownership
- **RRIF-R2 sourcefree engineer:** build/test bounded compatibility adapter, independent verifier, hash & mutation receipts, exact SHA; *not science owner or own reviewer*.
- **Original C9/C12 owner:** version/epoch/mirror/anchor/ACK and actual current adopter; not replaced by a code writer's convenience choice.
- **Original F1CR author:** test-only replacement decision, not original source recovery.
- **Original V3/CAN008/CAN011/ADP/SCI05:** actor events/response/practice science; no default Enneagram or trial-hallucinated parent.
- **Pyat HQ:** external empirical/source/world authority and N11/N12; not an RRIF code worker.
- **Sorok HQ receiving owner:** independent reviewer/test receipts first, then qualified selective sourcefree fan-in. Do not wait on optional GitHub ruleset/protection administration for independently legitimate engineering work.
