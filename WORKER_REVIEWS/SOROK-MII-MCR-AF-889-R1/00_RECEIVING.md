# MII #889 R5 — independent MCR-C contract-delta receiving (nonauthor review return)

**VERDICT: `ACCEPT_SCOPED_DOCUMENTARY`** — R5 delta repairs substantiated; seven obligations PASS at S1/S2
documentary grade. The MII engine itself remains `NOT_RUN`/INCOMPLETE; this is not an implementation acceptance.

FINDING. Author R5 HEAD `0178df262ac04d6fef074a56f6b8448c4d7fdcf9` (author file blob `ecba2a9e…`, 54
obligations, contract `43dd64d0…`) repairs both proof-boundary defects from the prior delta review and clears the
R3 DEFECT-01 stale MIII clause. Executed at the frozen review branch `ed839963…` against the protected cut
`4f3413fc5c37b589be3412f826bf8f68ee617d4a`:

- **DEFECT-01 fixed.** R5 line 208 records merged-via-#891 MIII status and the no-second-access-path rule; the
  former "remain DRAFT UNMERGED / not implicitly installed" clause is removed (R3→R5 grep diff).
- **63-outcome full-E coverage.** Frozen matrix `62cd9aae` blob `2ff94ac7…` conserves 63 discriminators across ten
  E packages; `--preflight` PASS (`actual_MII_implementation: NOT_RUN`), `--forged-attack` PASS (63/63 forged
  author receipts rejected).
- **Real first consumer.** `mcr_independent_consumer_trace.py` imports live owner code objects itself from a
  separately authenticated runtime checkout; `--counterfeit-attack` rejected; `--baseline` observed 24 genuine P6
  calls, mutated upstream `house.OBJECTS` → typed refusal, restored → identical public digest, byte-invariant
  world ledger.
- **53/54 + forged-63 refusal.** `mcr_contract_reduction_attack.py --self-test` → `PASS_REJECTED_53_FORGED_PROOFS`
  (MII-T05 missing detected); forged 63 refusal PASS; terminal receiving refuses candidate-edited proof
  executables and requires the full external suite.
- **Novel N2 challenge (reviewer-owned, corrected).** The mixed forged receipt — genuine observed P6 digest
  (`bf5a1b5f…`) carried by valid outcomes plus fabricated E3/E8/E9 measurements — was fed to the real receiving
  predicate `assess_receipts`, which returns RED with
  `MCR_MISSION_TEST_RETURNS_DIFFER_FROM_RECEIVER_OBSERVED_P6_MII-E03-APPEND_VERSION`; the all-genuine control is
  accepted. Verifier enforcement, not reviewer-side detection, is demonstrated (4/4). This resolves the
  `HOLD — N2_GATE_REJECTION_UNPROVEN` issue recorded on PR #893.
- **54 probes honest state.** Each per-ID runner command executes and returns
  `RED_INCOMPLETE / MCR_REAL_IMPLEMENTATION_ADAPTER_MISSING__NOT_RUN`; the MII implementation does not exist and
  no scenario is self-certified.

INTERPRETATION. The two repaired boundaries are correctly fail-closed: complete E1–E10 delivery is required
beyond the 54 probes, and genuine first-consumer execution must be independently observed. Prior accepted
unaffected facts (merged MIII correction, ABI/causal/viewer boundaries, 54 original identities, 68,221-character
00E appendix) are preserved. No native science, no protected merge, no MII engine PASS is claimed.

ACTION. None required before documentary receiving. The 54 probes and 63 outcomes remain INCOMPLETE until a real
implementation adapter and independent tests exist.

OWNER. Sorok HQ for scoped documentary receiving; future MII implementation author for execution; PREMAIN CAS
solely for eventual protected adoption.

## Per-obligation judgments

| Obligation | Judgment | Grade |
|---|---|---|
| MII-RV-MIII-SOURCE | PASS | S2 |
| MII-RV-CAUSAL-ACTION-ABI | PASS | S2 |
| MII-RV-VIEWER-SOURCE | PASS | S2 |
| MII-RV-EXECUTABLE-54 | PASS | S2 |
| MII-RV-RECEIPTS-54 | PASS | S2 |
| MII-RV-CURRENT-CONSUMERS | PASS | S2 |
| MII-RV-TERMINAL-NODROP | PASS | S2 |

## Runner facts vs NOT_RUN

RUN (local S2, this host): protected MCR-C checker blob `6e16878e…` hash-pinned; `--source-check` PASS zero
errors on the 7-obligation review prompt (contract `c95f0a65…`) and the 54-obligation author prompt (contract
`43dd64d0…`); reviewer inventory 7/7 enumerate + verify PASS (54 mission, 00E exact, registry structure, 54
issued commands, 53/54 refusal, 63 discriminators, forged-63 refusal, terminal seven-item preflight with
`independent_judgment: NOT_EXECUTED`); registries pinned (`e3732221` 7-ID blob `23c55f74…`, `8382651e` 54-ID blob
`a4aa2faf…`, `62cd9aae` 63-outcome blob `2ff94ac7…`); full-E gate preflight/forged-attack; contract-reduction
self-test; consumer-trace counterfeit/baseline; novel N2 probe; per-ID runner spot checks.

NOT_RUN: actual MII implementation and all 63 functional outcomes; S3 native science; human study; production
simulator; adaptive consent; protected merge.

## MII worker dispatch eligibility

**DOCUMENTARY-ACCEPTED for a qualified MII implementation worker** at the contract's own
`DELIVERED_PENDING_RECEIVING` ceiling. Any implementation return must clear the terminal receiving gates: 54
per-ID source-qualified runner proofs, 63 independent E-outcome receipts with real P6 returns and typed
source denial/restore, and the external nonauthor suite. No protected merge or native grant follows from this
acceptance.

## Execution passport

Reviewer host: OpenCode CLI, macOS local checkout, DeepSeek model — user-dispatched nonauthor of #889.
Review branch `review/sorok-mii-mcr-af-889-independent-r1` at `ed839963…`; author source frozen at `0178df26…`;
protected reference `4f3413fc…`; separately authenticated runtime worktree at `4f3413fc…`. No author, protected,
MIII, M-I, or PREMAIN file was edited (delta vs review base is `WORKER_REVIEWS/**` only).
MCR-C receiving gate receipt recorded in `05_MCR_C_RECEIVING_GATE_RECEIPT.json`.
