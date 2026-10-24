# R91 R05V R7 independent review — return

Verdict: **REVISE.** R7 closes the R6 executor-only original and learned-
association checks for ordinary admitted slots, and moves actual joint/changed-
evidence execution through the trusted coordinator with restore (author 40/40,
prior probes 22/22, provider 43/43, C1 13/13). One admission-boundary gap remains:
the coordinator verifies only the base refs/route/model of a request slot against
its admitted slot, then builds the retained original/slot records from the
**request** slot's learned/topology/currentness/E41 fields. A request can keep the
admitted id/base fields while substituting M1/M2/B5 (and similar actual fields);
the admitted native inputs still execute, but the trusted original now records
the request-supplied association, so an alternate productive learned object is
served as exact.

## Custody

- Stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-r7-consumer-review-r1`; startup/HEAD
  `65f7acf226b7b21a1a8f3be23f14a93b3f3cfbcc`; clean at gate.
- R05V R7 commission `2844a2c9...`; High decision `c618dc28...`; R7 contract
  `ce225f20773e7151f25faa3679131d0c5de14d65`; R7 code
  `6fa02ff850bec0c17db9b0a4fc4b1483dd8a97d9`; module blob `a1421201...`, test
  blob `b0114a82...`.
- Frozen EXPECTATIONS `7ea6e9ad1e1cbef0ed051c7a2f35ee37bde62b4a`, before R7 code.
- R4/R5/R6 code and prior reviews preserved; accepted R08/provider/evaluator
  bodies unchanged; R7 manifest 7/7 matched; only authorized two code/test paths
  plus author r7 return changed.

## What R7 establishes

- Author 40/40; exact prior R1/R2/R3/R5/R6 probes 22/22; provider 43/43; C1
  13/13.
- Executor-only/prebuilt fallback no longer retains a trusted original; the R6
  unadmitted-executor probe passes (trusted consumer refuses).
- Per-slot learned M1/M2/B5 comparison exists for the request slot, and the R6
  alternate-learned probe passes against the request-recorded original.
- Actual AT10 joint arity-2 executes through an admitted coordinator/trusted
  reader; actual changed evidence executes through an admitted slot/trusted
  reader, refuses and restores; discovery/recursive/E41 coordinator positives
  and typed/Z16 custody remain.
- Manifest/code scope and accepted owners are correct.

## Remaining defect

### R7-P1 — Request slot actual associations can rewrite the admitted original

`TrustedNativeGraphCoordinator.execute` compares admitted vs request only:
producer/consumer query, predicate, model hash, route, source universe and
release. It does not compare the request slot's `m1_disposition`, `m2_release`,
`b5_selection`, `require_current_selection`, `target_arity`,
`joint_order_semantics`, discovery result/receipt/frontier, recursive handoff/
lineage/root-parent, condition witness, E41 input or actual repository/query/
authority/consumer/model objects. It uses the admitted native inputs to execute
but builds `slot_records` from the **request** slot, including
`m1_disposition_ref`, `m2_release_ref`, `b5_selection_ref`,
`require_current_selection`, `target_arity` and `joint_order_semantics`. The
consumer then compares the submitted learned object to those request-derived
records.

Dynamic probe
`probes/test_r05v_r7_request_association_gap.py::test_request_slot_cannot_rewrite_admitted_learned_association`:
capture the actual AT10 discovery coordinator call; build a request slot with the
same admitted id/base fields but alternate M1/M2/B5 (`049214...` vs
`83220c...`); `coordinator.execute` accepts, the admitted discovery actually runs,
and the trusted consumer with the alternate learned object returns
`LEARNED_CONSUMER_EXACT_SUPPORTED`. The trusted original is not fixed to the
admitted learned association.

Exact missing function: require every request slot's actual association to equal
its independently admitted slot (all M1/M2/B5/currentness/topology/discovery/
recursive/E41/input fields), or build the retained original and slot records
solely from admitted slots and ignore/reject request-supplied actual values. The
request may select admitted slot ids/metadata but cannot rewrite learned/M1/M2/
B5/currentness/route inputs.

## Limits

Full live J42/P41/E04 remains NOT_REACHED; R04 independent. No original source/
science, F6/F7/FieldForge, CI/prod, N11/N12, Sorok, J52/W52 or adoption. Local
trusted-coordinator assumption; no OS/R09 protection. No candidate edit,
self-adoption or author wake.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_r7_observations.json`,
`probes/test_r05v_r7_request_association_gap.py`, prior probe copies,
`junit/*.xml`, `logs/stdout.jsonl`.
