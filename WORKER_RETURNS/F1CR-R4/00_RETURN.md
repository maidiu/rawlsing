# SOROK R4 F1CR — live A/B history binding and targetless receiver

**Verdict:** `ENGINEERING_ACCEPT_SCOPED__LIVE_A_B_SHARED_BINDING_REPAIRED__TARGETLESS_CONTINUATION_HOLD__NO_ADOPTION`.

The three F1CI3 live-history mutations are now refused before C8 with distinct A, B and shared codes. All 13 original F1C outcomes, the same `r31j.assertion.p01`, physical tool transfer, B’s one-hour opportunity cost, omission and source-severance behavior are preserved. The existing JOIN targetless REFUSE carrier remains a read-only owner input; F1C REFUSE/SILENCE continuation and C10 semantics remain HOLD.

## Identity and custody

- Repository: `maidiu/rawlsing` (private).
- Return branch: `agent/sorok-r4-f1c-live-history-targetless-coverage-repair-20261030`.
- Source base: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.
- F1C author: `bcea367e7dc0f2e069de71b0fe5e481de094dad5`.
- F1CI3 reviewer: `0a884fd5af7ebb97f4cc0ef8c1251386641732f0`.
- F1C program blob `104f5bd7826c8676192eac96753d980e35d8a80a`, SHA-256 `7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b`.
- R31J: `64fec28c374d8f77fb0b412d0c934d798ede03e8`; JOIN-E: `7bf2da302996491ddf34b9a039fea47ac982d135`; QF2: `a93db6bce4832270cf29727233dbfbc5f0312395`.
- PRE-MAIN: `299f41e97a43c67be9cc76a79fa49b48f4e12e54` (read only, not modified).
- Host: `oldMac` (local `scutil` verification); harness OpenCode; agent `opencode`; model `opencode-go/deepseek-v4.1-flash`; MAX requested, actual effort `UNVERIFIED`; session UI title/ID/URL not exposed.
- Worktrees: return `.../opencode/f1cr-return`; replay Git worktree `.../opencode/f1cr-base` detached at `299f41e9…`.
- No PRE-MAIN, PR #514/#516/#519/#521, original author/reviewer tree or other worker was mutated. No original source/native corpus was executed.

## FINDING — repair and replay

The minimal repair adds a live projection binding in the F1C executable:

```python
live = live_prior(life)          # full A/B ledgers+snapshots; shared material+witness+objective
require(digest(live["A"]) == digest(frozen["prior"]["A"]), "LIVE_A_HISTORY_CHANGED")
require(digest(live["B"]) == digest(frozen["prior"]["B"]), "LIVE_B_HISTORY_CHANGED")
require(digest(live["shared"]) == digest(frozen["prior"]["shared"]), "LIVE_SHARED_HISTORY_CHANGED")
```

The check runs before `intervene`, `Receiver`, C8 or C9. The accepted frozen bytes, original `p01`, all 13 original input scenarios and all prior test/evidence files are unchanged. Patched program SHA-256 `18c96f97eca5480893c0f38a06f21c0d985fe0c6c997e63e0898001157351dfb`; patched Git blob `bf7e625e1f208908e583ea72ebb73992ad7d19ae`.

| Court | Before repair | After repair |
|---|---:|---:|
| F1C original 13 scenarios | **13/13 expected outcomes** | **13/13 same outcomes** |
| F1CI3 live A `RELATION_VIEW` mutation | FAIL `DID NOT RAISE` | **PASS: `LIVE_A_HISTORY_CHANGED`** |
| F1CI3 live B `RELATION_VIEW` mutation | FAIL `DID NOT RAISE` | **PASS: `LIVE_B_HISTORY_CHANGED`** |
| F1CI3 shared witness mutation | FAIL `DID NOT RAISE` | **PASS: `LIVE_SHARED_HISTORY_CHANGED`** |
| JOIN targetless REFUSE regression | 1/1 pass (read-only) | **1/1 pass (unchanged)** |

The 13 outcomes preserve SHARE `p01=True`, UNOBSERVED_SHARE `True`, B_SOURCE_RESTORED `True`, B_SOURCE_SEVERED `False` with the transfer/B-cost retained, E2_OMITTED `False`, and REFUSE/SILENCE/UNOBSERVED_REFUSE exact `C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL`. Resource/encumbrance/duplicate/native smuggling and RETROACTIVE_A retain their exact holds.

### Physical invariants preserved

- SHARE/B_SOURCE_SEVERED/B_SOURCE_RESTORED terminal tool ledger **A=0, B=0, spent=1**; material **A=3, B=0, spent=1**.
- E2_OMITTED terminal tool ledger **A=1, B=0, spent=0**; material **A=4, B=0, spent=0**.
- B free hours retain **12→11** and the finishing commitment; the source-severed case keeps the physical transfer but `B_source_admitted=False`.
- Two patched runs in separate processes match all 13 `p01`/hold/terminal/access fields. The original C12 episode verifier remains RED; the F2 add-on remains an add-on with its raw-SQLite/anchor HOLD.

## INTERPRETATION

The original adapter authenticated the detached frozen value and snapshots but did not prove that the live A/B ledgers and shared witness consumed by `build_world_occurrence` still equal that frozen source. The new digest binding closes that exact gap. It does not change biographies, manufacture B, issue Rule A/T or turn targetless NO_PROPOSAL into evaluated psychological nochange.

The existing JOIN `joined/refusal.py` at `7bf2da30…` (blob `9a8726fe26486a2beb2af8216910737bf1fc323a`) supplies a derived targetless REFUSE C12 carrier and its original regression passes 1/1. It is **not** an F1C adapter: its `RefusalSession.start` hardcodes the original R31J evaluated input and does not accept F1C frozen roots or a SILENCE packet. F1C REFUSE/SILENCE targetless continuation and original C10 semantics remain owner HOLD.

## ACTION / ACCOUNTABLE OWNER

**HQ ACTION:** Send this repaired F1C cut and the three mutation witnesses to the original F1C adapter owner and C8/R31J source owner for replay/acceptance. Send the targetless REFUSE/SILENCE/C10 contract to the original JOIN/BP2P4/C9/C10/C12 owners. Do not merge or adopt.

**OWNER:** Original F1C adapter owner; R31J/C8 source owner; JOIN/BP2P4/C9/C10/C12 owners; incumbent Sorok HQ; a distinct post-return reviewer. No self-adoption.

## Three courts

- **ENGINEERING:** `ACCEPT_SCOPED` — 3/3 live-history mutations now refuse with distinct codes before C8; 13/13 originals, physical/source-severance/omission and 1/1 JOIN targetless regression preserved.
- **SCIENCE:** `HOLD_ORIGINAL_B_AGENCY_G1_G2_RULE_A_T_AND_ACQUIRED_PRACTICE`. The test-only material/consumer results do not prove independent B, native practice, actor-specific motive or evaluated nochange.
- **AUTHORITY:** `HOLD_ORIGINAL_ISSUANCE_AND_CANONICAL_CAS__NO_ADOPTION`. No original B/world/ADP/Pyat/CAN/SCI05/C11/C12 grant is issued.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** 13 original scenarios, three mutation witnesses before/after, distinct live-refusal codes, physical/B-cost/omission/source-severance preservation, 1/1 JOIN targetless regression, source pins, session locator.
- **REMAINING:** owner replay/acceptance of the repaired F1C cut; owner decision on REFUSE/SILENCE/C10 targetless continuation; native B/world/ADP/CAN/Pyat/SCI05 grants; separate review. QF2 remains `STOP_QF2_ORIGINAL_OWNER_GRANTS_AND_RELEVANT_ACCEPTED_REVIEWS_ABSENT__NOT_MERGED`.
- **CRITICAL BLOCKERS:** no owner-issued F1C targetless adapter or C10 semantics; JOIN carrier uses a different actor/source cut; no native B or science authority; C12 raw/anchor limits remain.
- **LARGEST PRODUCTIVE MOVE:** original F1C owner applies the live binding at `bcea367e…` and replays; original C9/C10/C12 owners decide whether to adapt `joined/refusal.py`, not a new engine.
- **FLIGHT:** one sourcefree local Git/Python worker; no PRE-MAIN/PR/original tree mutation; no model/harness switch.
- **DELTA:** the three accepted live-history mutations are closed at the exact pre-C8 boundary while the targetless continuation remains explicitly unissued.

## First actual consumer

`f1c.same_receiver_assertion` → `R31JProduct` / unchanged `r31j.assertion.p01` for SHARE and the 13 sourcefree scenarios. The existing targetless REFUSE consumer is `joined.refusal.RefusalProduct`/`RefusalSession` (read-only, 1/1 regression); it is not linked to F1C. No production or native first consumer.

## Final remote SHA

The ordinary push binds this return. Its exact 40-hex SHA is verified by direct `ls-remote` and reported in the final response; it is not embedded self-referentially. No force-push, no PRE-MAIN mutation, no self-review.
