# PYAT R38 WG0RI — INDEPENDENT EXACT CURRENT35 DISPOSITION REPAIR VERDICT

**Disposition: ACCEPT the exact disposition-carrier repair at its byte/ledger
grain. REVISE the manifest/O07 provenance disclosure and the short replay
command. HOLD the full original35 item/operation frontier.**

The original carrier RED is genuinely repaired: the exact frozen 18,276-byte
payload is recovered at the original SHA-256, and the original malformed Git
artifact is preserved and fails closed. No new disposition meaning is accepted;
O07 is diagnostic-only and the frozen-SHA gate is the sole acceptance gate.

## 1. Exact position

- Role: fresh independent I2 source-free custody reviewer, not WG0R/WG0I author,
  Pyat HQ, source-semantic issuer or original E_pre issuer.
- Branch: `agent/reviewer-pyat-r38-wg0ri-exact-disposition-repair-r1`
- Sealed base: `68873526efe5a39a0849aa401666ac997870f156`
- Author target: `86c13ea6cea813fa2f87dca92396646305e3742c`
- Prior independent WG0I: `44eac9021db23267448a6fc151e6bbe8374a868f`
- Phase A prefreeze commit: `4c1e5573f62bba7776a10030b73916eac7935985`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/wg0ri`

## 2. Was the original frozen payload exactly recovered? YES

| Check | Independent result |
|---|---|
| Recovered payload | **18,276 bytes**, SHA-256 `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98` |
| P2 identity master | **18,276** unique implementations, SHA-256 `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6` |
| Reserved bits | **0** violations; all use codes 0–9 legal |
| Class counts | SEM 4,681 · TOP 3,667 · POS 2,904 · END 2,113 · CTX 1,675 · SCX 1,506 · ADM 1,026 · REJ 454 · CPC 183 · BLK 67 (sum 18,276) |
| Flags | 10,418 hard-fail; 4,447 route-predicate-required |
| Format / code map | `P2_ORDINAL_BYTEPACK_V1`; `0=SEM;1=TOP;2=POS;3=END;4=CTX;5=SCX;6=ADM;7=REJ;8=CPC;9=BLK`; bits0-3 use / bit4 hard_fail / bit5 route / bits6-7 zero |
| Accounting reader | 18,276 rows / 35 waves / 9 families; no `DISPOSITION_CARRIER_REQUIRES_EXACT_REPUBLICATION`; 76 P10/G1A holds within 65,354 units; state `EXACT_PACK_VERIFIED` |

The recovered bytes match the frozen target exactly. The accounting reader binds
the payload to the exact P2 master, declared length, hash, format, code map and
packed-byte legality; it rejects corrupt copies closed.

## 3. Original malformed artifact preserved and fail-closed

The original Git publication `b44596d8…` (blob `c93945d1…`, 24,972 bytes, SHA-256
`c1d5a9a9…`) *claims* the 18,276-byte/`64a43ba2…` target but actually decodes to
**18,387 bytes / `3bee6f0e…` / 2,114 reserved-bit violations**. It remains
unmodified and the repaired reader rejects it. The repair is a separate active
versioned path; the historical RED is not silently overwritten or relabelled.

## 4. Evidence chain and surviving shard

- **Surviving shard:** exact original Git blob `3a9b5bde…` (11,944 bytes, SHA-256
  `e9fff20e…`), 1,000 rows, ordinals 0–999, **1,000/1,000 rows match** the
  recovered payload bytes; zero mismatches.
- **P2 first/last IDs** match the manifest’s 0/999 boundaries.
- **Manifest discrepancy (REVISE):** the retained 19-shard/18,276-row manifest
  lists part-000 SHA `e2f5f13ade61…`, which is not the Git survivor
  `e9fff20e…`. The survivor is byte-exact and row-correct; the manifest is a
  different serialization/full-shard set and must be typed as such — it is not
  the survivor’s byte manifest and cannot substitute for it.
- **Source projections:** S00 `d0fc960f…`, O06 `91379e9a…`, O07 `4b9b4a54…`,
  O08/O09 `2daebfe1…`, O04 `8da69f98…`; custody JSON binds projection/source
  hashes and archive/member origins. The external archive member bytes were not
  re-extracted in this return; the retained projections and their custody hashes
  are the verified inputs.

## 5. O07 recall projection boundary

O07 is a two-column diagnostic projection and never selects a use code. The
recovery selects use from S00 workstreams and the central O04/S2B ruling;
independently:

- changing a non-`UNRESOLVED` O07 value (`ADMIN → SEM`) leaves the recovered
  payload **exactly** at the frozen SHA;
- of 30 `UNRESOLVED` rows, changing the diagnostic to `ADMIN` changes the payload
  for **9** rows (held solely by O07) and leaves it exact for **21** (held for
  another retained reason); every changed payload is **rejected by the frozen
  payload SHA**, and no different payload is accepted.

Thus O07 may contribute a diagnostic held status for 9 rows, but cannot issue a
new disposition meaning or bypass the exact-payload acceptance gate. The S2B
feelevel special handling is backed by the retained central O04 ancestry and the
explicit feelevel ruling in `R10F_O03_O04_CENTRAL_INTEGRATION_REPORT.md`; the
2,113 accepted O04 endpoints equal the END count (2,113).

## 6. Independent execution

| Court | Actual result |
|---|---|
| Author full native 90-test court (with the four native test modules) | **90 passed / 0 failed / 0 error / 0 skip** |
| Author relocated cold court, `PYTHONHASHSEED` 0 | **90/0/0/0** |
| Author relocated cold court, `PYTHONHASHSEED` 1 | **90/0/0/0** |
| Independent R38 hostile court | **24 passed / 0 failed / 0 error / 0 skip** |
| Two fresh recovery processes / relocated copy | exact `64a43ba2…` in both |

The author’s short replay command (`pytest test_wg0r.py test_disposition_repair.py`)
yields 23 passing tests, not the reported 90; the 90-test court requires the four
`pre553_*` native test modules. This is a documentation/replay-command revision,
not a test failure.

## 7. Independent hostiles (all fail closed or detectably mismatch)

- Byte/hash corruption; header length/hash change; P2 substitution; code-map
  change; duplicate pack row; bad base64; duplicate/truncated payload — rejected.
- Ordinal duplication, omission and reordering — detected by the shard ordinal
  set, accounting ordinal sequence and frozen payload SHA.
- Reserved-bit violations and use-code 15 — rejected by the frozen payload SHA
  (the explicit reserved-bit guard is defence-in-depth).
- Dropped/silently converted holds — any changed held flag changes the payload
  hash and is rejected; 10,418 hard-fail flags and 76 P10 holds are preserved.
- Forged custody projection hash — `RECOVERY_INPUT_CUSTODY_MISMATCH`.
- Aggregate-count-only reconstruction — not the frozen bytes; truncated/false
  S00 identity inputs fail the full identity anti-join.
- Mismatched manifest — typed provenance discrepancy (above), not a payload pass.
- Two-process replay — identical exact payload; no non-deterministic acceptance.
- Historical malformed artifact — preserved and fails the repaired reader closed.

## 8. Scientific boundary preserved

This byte repair is **not** proof of complete original35 source-to-operation
execution. WG0I’s P2/O35E crosswalk remains open: 18,276 vs 18,259; 18,250
common non-None identities; 26 P2-only hashes (7 carrier + 19 measurement
candidates); 9 O35E blocked-identity rows; 17 net count delta; 76 P10/G1A holds.
The full original35 eligible item/operation frontier remains **HOLD**
(`PERMITTED = 0`; all 127,813 operation rows HOLD; 175 queue current refs null;
`all35_operation_execution = UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED`).
The exact source/operation authority issuer remains distinct; no source,
operation, issuer, actor/model or Field Forge right is issued by this repair or
this court.

## 9. Decision

| Grain | Decision |
|---|---|
| Exact 18,276-byte disposition payload recovery | **ACCEPT** — exact SHA, P2, class counts, zero reserved bits, 1,000/1,000 shard rows |
| Repaired ledger + downstream accounting reader | **ACCEPT** — 18,276/35/9, no null carrier rows, 10,418/4,447, 76 holds |
| Original malformed Git artifact preserved/fail-closed | **ACCEPT** — exact Git blob, unchanged, reader refuses |
| Manifest/survivor provenance and short replay command | **REVISE** — type the different serialization; list the four native modules |
| O07 diagnostic dependency | **DISCLOSE** — 9 held-status rows; no use-code issuance; frozen-SHA gate |
| Full original35 item/operation frontier | **HOLD** — WG0I crosswalk, 19 measurement candidates, 76 holds and all source/operation authority remain open |

## 10. Evidence index

- `00_PHASE_A_PREFREEZE.md` — pre-execution frozen expectations and chronology.
- `01_AUTHOR_COURT/` — 90-test native JUnit, two cold 90-test JUnits, independent
  24-test JUnit and the short-command 23-test record.
- `02_EXECUTION_AND_HOSTILE_RECEIPTS.json` — all counts, hashes, chain facts,
  O07 outcomes, manifest discrepancy and decision.
- `03_O07_BOUNDARY.json` — 30 `UNRESOLVED` mutation outcomes (9 changed/21 exact).
- `03_PROVENANCE_AND_CUSTODY.md` — chain, manifest/O07 limits and authority.
- `r38_court.py`, `test_r38_hostiles.py` — independent executable court.

Final remote reviewer SHA is supplied by direct remote readback in the final
reviewer response and bound by `PUBLICATION_RECEIPT.json`.

## 11. Non-grants

No original source U/E_pre, raw SAV/DTA/respondent read, signed issuer,
source-execution warrant, model/actor, Field Forge, N10W, Sorok, OC05, V3,
N11/N12, production owner commit or HQ adoption.
