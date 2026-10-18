# Sorok — two parallel bounded executable investigations (2026-10-18)

**Status:** LOCAL TESTED CANDIDATES ONLY. Not a new HQ decision, not adopted semantics, not formal fresh independent I2 review, not canonical V3 code, not published to private GitHub.

## Track A — M2 historical-source preimage repair

**Pin:** original M2 candidate `5c2fbe14ccfa5027becfabc682206a1e61aaf986`, first M3 P0 court `49dfcb30971310756a12f659961600d9f2eb4a11`. Original committed `kernel.py` SHA-256 `888d73fff63f70a22932f1001f5c9003104b0e5a9cdef84e93456151428676c8` was preserved in the included M2 source ZIP. New `m2_patch/kernel.py` is a separate versioned, unadopted candidate.

Fix: freeze exact **source-level readsets actually consumed** by each durable test-only interpretation, including cited utterance, speaker-action and listener-exposure receipts, prior practical history plus witness, chosen affect and public act plus witnesses. Verify old preimages *at every future continuation*. Leave unconsumed caregiver private history free to change. Preserve objective event hashes and clock gates.

**Actual frozen and prospective Python/pytest runs:**

- Original M1, unchanged on M1: 37 PASS.
- Original I2, unchanged on M1: 14 PASS / 9 RED.
- Original M2 suite, unchanged on repair: 41 PASS.
- M3 lawful scenarios, unchanged on repair: 32 PASS.
- Original M3 three source-preimage REDs, unchanged on repair: **3 PASS**.
- Newly written targeted source-preimage tests: 15 PASS.
- **91/91** directly relevant repaired-kernel prospective tests pass.
- Original M1 37 against repair: 18 PASS / 19 RED; I2 23 against repair: 13 PASS / 10 RED. These historical compatibility REDs remain intact and are *not* rewritten.

**Limitations:** hashes and synthetic fixture witnesses are not independent signed owner authority. A hostile editor replacing both lineage state and witness registry remains out of scope; the next layer requires authenticated custody, append-only database and accepted owner grants. A distinct reviewer must independently reproduce before integration.

## Track B — independently situated contingency → actor encounter → observable practice

Research-only, newly authored `causal_experiment/world_intersection.py` and 24 passing tests. Holds theft and biographies fixed while intervening on an employer-side workplace occurrence, which changes father's cash/time commitments, father action, and potentially child's *observed* subsequent activity. Includes a neighbor's independent project, record hashes, causal parents and temporal constraints. A simple practice-frequency rule is **explicitly uncalibrated and nonpsychological**: it is not a validated learning law or actual generated disposition. Unlike personality scripts, no `secure` or `insecure` child belief is emitted.

**Executed sourcefree results, baseline father cash buffer 125**:

| Employer event | Father's available minutes | Father's enacted response | Child day 4 action | Observed repair practice tally |
|---|---:|---|---|---:|
| Hours cut | 35 | Discuss nonpurchase options | Take bus | 1 |
| Raise + compulsory overtime | 3 | Defer conversation | Take bus | 1 |
| Routine | 35 | Offer joint repair | Participate in repair | 3 |

This is **not** a claim that a raise generally decreases caregiving, or that the simulated father's actions are empirically probable. The illustrative work/pay numbers and decision rules are authored assumptions for falsification and architectural evaluation. The two changed encounters that both lead to taking the bus are an intentionally retained **no-effect** comparison. Increasing the father's independently held cash reserve to 220 allows loss-of-hours to lead to a shared repair; retaining an independently practiced protected family-time boundary can permit shared repair after a raise/overtime too, with the overtime declined and the work tradeoff recorded.

**Remaining scientific task:** independently qualify laws/constraints explaining father conduct, child uptake, learning and durable dispositions, compare with real observations, and independently integrate qualified owner-permitted source custody. No production B3, CAN008/CAN011 or ADP rule adoption.

## Run

```bash
python -m pytest -q m2_patch/test_m2.py m2_patch/test_m3_independent.py m2_patch/test_m3_unresolved.py m2_patch/test_source_preimages.py
python -m pytest -q causal_experiment/test_world_intersection.py
python causal_experiment/world_intersection.py
```

For the strongest isolated import guarantee, run `m2_patch` and `causal_experiment` from their own directories. `evidence/` contains test stdout/JUnit files and structured receipts including all preserved historical failures.
