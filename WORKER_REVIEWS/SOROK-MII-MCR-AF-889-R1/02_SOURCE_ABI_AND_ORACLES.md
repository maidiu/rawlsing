# Source ABI, oracles and independent novel challenge — R5

All reads at frozen cuts: author `0178df262ac04d6fef074a56f6b8448c4d7fdcf9` (file blob
`ecba2a9e199bd018099adc2093f83ef7c8c2c517`), protected `4f3413fc5c37b589be3412f826bf8f68ee617d4a`,
review base `ed839963ff18c4ad4d297a056cb2825976e71986`, original #792 `094937d3187ed3c2e215fe2c1f7c1c84f50d9006`.

## Frozen registries

| Registry | Commit | Blob | Pin |
|---|---|---|---|
| Seven reviewer obligations (`mcr_frozen_review_ids.tsv`) | `e37322219c54df2cd0084162bb0b68d016794a6b` | `23c55f74b227a5d843e8489f65dcb45302813762` | PASS |
| Original MII 54 identities (`mcr_frozen_identities.tsv`) | `8382651eabc5a7fa6ca0fed3447fa6308b3324fc` | `a4aa2fafbb19263e3a89de703c8525a765417e95` | PASS |
| Frozen 63 E1–E10 outcomes (`mcr_full_e1_e10_acceptance.json`) | `62cd9aae4a12f6cef9ef4c7bc34326c3d3c306ff` | `2ff94ac73fbd22344acfe2890a9163b8b492348d` | PASS |

Seven obligations enumerated and structure-verified by `mcr_reviewer_inventory.py verify` (7/7, 54-mission exact,
00E byte-exact, 54 issued commands, 53/54 refusal, 63 discriminators, forged-63 refusal).

## Canonical checker

Protected `CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py` blob
`6e16878e60e8e89bf8ab8001144ed84ad257f5fc` (hash-object verified at `4f3413fc`; the obsolete `e11a7b9b…` in the
review tree was not substituted). `--source-check` PASS zero errors on the review prompt (contract
`c95f0a6504ad5203c89b1a5358f6994744a85276baea2d793ef81bf4b595989b`, 7 obligations) and the author prompt
(contract `43dd64d0197960d907c1991bf92ef2a47deb7cdd773878d545187ee73bb2df64`, 54 obligations).

## Real first-consumer witness

`mcr_independent_consumer_trace.py` with `MCR_QUALIFIED_RUNTIME_ROOT` = a separate git worktree at
`4f3413fc…` and `MCR_QUALIFIED_RUNTIME_SHA` authenticated:

- `--counterfeit-attack` → `PASS_COUNTERFEIT_ADAPTER_REJECTED` (no genuine P6 frame; self-reported digest not
  accepted).
- `--baseline` → `PASS_ACTUAL_P6_CODE_OBJECT_AND_SOURCE_DENIAL_RESTORE_WITNESSED`; 24 observed owner frames;
  public digest `bf5a1b5f0e24c88db8f931478e4e9c6ae9d9629f6c1beffcf08341caae0ccde0`; upstream
  `house.OBJECTS["bench"]["glance"]` mutation → typed refusal; exact restore → equal public view; world ledger
  byte-invariant.

Mechanism: reviewer-side `sys.setprofile` matches CPython code objects from live imports; adapter-claimed
`p6_observed_return_sha256` must equal the independently observed `run_p6.experience` return; profiler
disablement is detected.

## Full-E gate

`mcr_full_e1_e10_gate.py --preflight` → `PASS_FULL_MISSION_63_DISCRIMINATORS_PRESERVED` (93=63 claims, 10
packages, actual MII `NOT_RUN`, acceptance `PENDING`). `--forged-attack` →
`PASS_FORGED_63_OF_63_AUTHOR_RECEIPTS_REJECTED` (fails on missing separately-run P6 observer).
`assess_receipts` demands per outcome: `SOURCEFREE_S2`, a real `run_p6.experience` return in
`independent_actual_source_witness`, `qualified_source_denial`, `exact_source_restore`, a 64-hex first-reader
digest equal to the regenerated observer artifact, and `reviewer_command_origin: INDEPENDENT_NONAUTHOR_SOURCE`.

## Terminal no-drop

`mcr_contract_reduction_attack.py --self-test` → `PASS_REJECTED_53_FORGED_PROOFS` (verifier `RED_INCOMPLETE`;
missing `MII-T05`; frozen-universe and no-drop mismatch). `mcr_terminal_receiving.py` readback: candidate-edited
proof executables refused; 54 exact issued commands; 63 conservation per E package; distinct output/evidence
paths; runner + witness + full gate + frozen verify-return before readiness; `--preflight`
`PASS_ISSUED_54_SOURCE_PROOF_COMMANDS_ONLY` (`actual_MII_not_run: true`).

## Independent novel challenge N2 — decoy call + unconnected invented metrics (executed, PASS 6/6)

**Case selected.** A genuine observed `run_p6.experience` return (56 profiler frames) has its authentic digest
attached to invented unrelated metrics — E9 latency/cold-start, E3 exposure-ledger writes, E8 replay failures —
and an unrelated "MII-P03 unusual target recognition" claim. Separately, a decoy real `look(bench)` call is used
to claim the sandal identity. Nonredundant: the author's attacks cover a fully counterfeit adapter (no call) and
all-forged receipt sets; neither covers the mixed laundering case where a real call authenticates unconnected
invented data — the exact "decoy P6 call plus invented unrelated metrics" the launch requires.

**Result.** `genuine_p6_return_observed` PASS; `invented_metrics_have_no_observed_producer` PASS (no profiled
frame produces latency/exposure/replay data); `unrelated_scenario_claim_not_in_real_return` PASS
(`recognized_identity=None`); `laundered_receipt_must_be_rejected` PASS; decoy `look(bench)` yields `{}`
recognition and cannot certify the sandal identity (both PASS). Conclusion: a real call is necessary but never
sufficient; unconnected metrics must be rejected even when the carrier digest is genuine.

## Conservation

54 original identities set-matched against original #792; 00E appendix byte-exact (68,221 source characters);
63 E outcomes supplement rather than replace the 54; no new MII-only psychology engine, world author, extra
narrator LLM gate, implicit consent, or serial MIII prerequisite introduced.
