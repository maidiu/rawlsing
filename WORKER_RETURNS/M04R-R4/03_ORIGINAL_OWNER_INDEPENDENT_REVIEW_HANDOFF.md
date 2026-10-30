# M04R — original owner and independent reviewer handoff

Observed FINDING: the exact M04 helper still permits a direct unjournaled ADP017 terminal restore and a forged unjournaled pre-state; the M04R candidate refuses both under the same `read_owner` consumer while preserving 587/587, 51/51 and the nine historical failures. Causal INTERPRETATION: the missing link is journal coverage of the consumed restorative terminal, not a new native rule. Proposed HQ ACTION: original M03/M04 owners review the three-line behavioral change and the four new tests; a distinct source-qualified reviewer replays at the exact candidate SHA. Accountable OWNER: original M03/M04 author and CAN3/ADP017 owner; incumbent HQ appoints the reviewer. No adoption by this author.

## Exact candidate and apply

- Candidate helper: `WORKER_RETURNS/M04R-R4/candidate/claim_provenance.py`
  - Git blob `d9efd3f5ba0d06430ef99f114072ba91ef32f1fc`
  - SHA-256 `ef551f5ad0c927dffb37554d8aaf8c00a611877242b550fbc541ea5089151f4c`
  - Apply over the effective M03 module `runtime/m02/runtime/m01/repro/claim_provenance.py` after the M04 patch `5ba929f5…`.
- Candidate tests: `WORKER_RETURNS/M04R-R4/candidate/tests/test_m04r_journal_coverage.py`
  - Git blob `fa728cc89375e581c4c5ee326c940fa8562a58a1`
  - SHA-256 `0f1bb3978657f402f54623f548776612f6ca73768e5764317f0b0805317424bc`
- Original M04 patch: `5ba929f51870b111ca54ca87fdf97338e4295625`; original M03 helper `2434bda6…`; frozen reviewer test `8add06c6…`.

Replay:

```sh
cd <M04-reviewer-return>
python3 repro/stage_independent.py
python3 repro/install_candidate.py                 # original 2434 baseline: 41/10 RED
cp <candidate>/claim_provenance.py runtime/m02/runtime/m01/repro/claim_provenance.py
python3 review/run_fresh.py                        # 51/51 PASS
python3 repro/run.py after original_413             # 413 PASS
python3 repro/run.py after independent_100          # 100 PASS
python3 repro/run_author.py                         # 74 PASS
python3 repro/run_historical.py                     # nine failures, expected
M04R_RUNTIME=<...>/repro PYTHONPATH=<...>/repro python3 -m pytest \
  <candidate>/tests/test_m04r_journal_coverage.py -q  # 4 PASS
```

Then run `m04i2_unjournaled_probe.py` with `--variant direct` and `--variant forged`: both must return `read: REFUSED`, exit 0. Before the candidate, both return `read: ACCEPTED`, exit 2.

## What the reviewer must attack

1. Verify the candidate blob and test blob byte-for-byte; confirm the M04 patch and original M03 helper are unchanged.
2. Replay 41/10 baseline, 51/51 candidate, 587/587 inherited, nine historical failures, and both probes.
3. Verify the direct probe still grows the journal-2/transition-3 state before refusal and that `read_owner` returns `CLAIM_TRANSITION_UNJOURNALED` without mutating the post-call checkpoint.
4. Verify the forged-pre-state probe returns `CLAIM_TRANSITION_PRESTATE_ANCESTRY`.
5. Attack orphan journal entries, duplicate journal coverage, a forged journal entry payload, a direct unjournaled ADD after a revocation, and a direct unjournaled SUPERSEDE to an inaccessible state (the last is lawful native state change and must not be rejected).
6. Confirm the nine historical CAN3 failures remain separate and that no test was weakened to make the patch pass.

## Owner questions

- Is the consumed restorative terminal the correct journal-coverage unit, or must the owner require every selected-claim transition to be journaled? A blanket requirement was tested and broke lawful original native ADD/WITHDRAW tests; the final patch targets the exact terminal/forged route.
- Is `SUPERSEDE_EXACT_RECORD` the complete restorative operation set, or are there other owner-authorized operations that must be journaled when they restore accessible BELIEF?
- Should the journal entry also bind the full terminal transition/effect identity, not only pre/post state? The candidate preserves the existing M04 pre/post checks and adds terminal coverage; the owner may require a stronger identity check.
- Do the nine historical CAN3 failures remain outside this helper's authority? Yes in this return; owner must decide separately.

## Preserved authority and holds

No native CAN3/ADP016/ADP017/SCI05/Pyat rule, actor, world, practice or human A0–A5 authority is issued. No canonical C9/C12 compatibility is established. The nine historical CAN3 failures remain nine failures. No PRE-MAIN, PR #514/#516/#519/#521, original author/reviewer or other worker was modified. The author does not accept the candidate; a distinct I2 reviewer must replay at the exact SHA.

DONE: exact patch/test mapping, replay commands, probes, owner questions. REMAINING: owner replay, reviewer acceptance, CAN3 disposition. CRITICAL BLOCKERS: no owner CAS; native/C9 authority HOLD. LARGEST PRODUCTIVE MOVE: reviewer runs the four-command baseline/candidate/probe sequence against `d9efd3f5…`. FLIGHT: sourcefree local test harness only. DELTA: direct and forged unjournaled terminal routes are closed under the same read consumer with all prior positives preserved.
