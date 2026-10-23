# R61-R01V R4 defects and preserved limitations

Verdict: **REVISE**. R3 A1–A3 remain PASS. R4 positive chain is real but A4 is
not qualified because the recurrence consumer does not authenticate the
receipt-bound parent or the generation relation. Candidate files were not
edited; probes are disposable below this reviewer root.

## D1 — Receipt-bound parent binding is not consumed or validated (blocking)

**Contract:** commission item 2; R4 profile E1/E2 ("exact canonical persisted
parent", "receipt-bound parents must resolve through the existing recursive
handoff"). **Observed:** `execute_recurrence_generation`
(`rawlsing_next/universal_grammar/native_map.py`) validates only
`discovery_authority.candidate_grammar_ref`. It never compares
`RecurrenceParent.receipt_ref`, `replay_binding_ref`, `handoff`,
`source_release_refs`, or `parent.predicate` to the persisted handoff.
`build_recurrence_issue_plan` likewise only materializes the caller-supplied
parent.

**Repro (probes, B1/B5):**

```sh
/usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r4/probes/test_r01v_r4_reviewer.py \
  -q -o addopts=''
```

- B1: take a valid `activate_next_generation` receipt-bound parent and replace
  `receipt_ref`/`replay_binding_ref` with bogus refs, `handoff=None`. The
  candidate generates an identical grammar and identical expected operation
  IDs; the real I05 next-generation execution passes `no_drop_ok`.
- B5: construct `PARENT_RECEIPT_BOUND` with `receipt_ref=None`,
  `replay_binding_ref=None`, `handoff=None` and a caller-chosen predicate.
  Generation 2 executes and passes the anti-join.

**Required:** typed refusal for a missing/forged/stale receipt or replay binding,
exact predicate/parent-id/handoff equality, and source-release equality with the
execution releases. The parent source release currently has no effect on
execution.

## D2 — Generation continuity is not enforced (blocking)

**Contract:** commission item 2 ("Repeated root calls with new generation labels
are not recurrence"); profile D semantics. **Observed:** the planner accepts any
`parent.generation` for any `1 <= generation <= D`.

**Repro (probe B2):** build a `generation=2` plan with the sole parent
`PARENT_ROOT, generation=0`; generation 2 executes natively and the anti-join
passes.

**Required:** require `generation == max(parent.generation) + 1` (root only at
generation 1), or bind an authenticated lineage contract that makes relabelling
impossible.

## D3 — Cumulative budget is a caller-declared input, not an enforced ledger (secondary)

**Observed:** `total_issued_before` is an unchecked integer argument used only
to reduce the per-generation cap; it is absent from
`RecurrenceIssuePlan.material()`. An understated value issues more operations
(probe B3). Exhaustion raises `RECURRENCE_GENERATION_ISSUED_NO_OPERATIONS`
rather than returning explicit unissued/PENDING records (probe B7). The author
return and matrix say "cumulative ... cap", which overstates enforcement.

**Required:** either bind/exact-check an append-only cumulative issued ledger, or
declare `total_issued_before` as a trusted caller scheduling input and stop
claiming enforcement; report budget exhaustion as explicit pending/unissued.

## D4 — Wrong source/edition/replay negatives are not independently mutated by the author

The author matrix marks this `PARTIAL` and the proof witness says it is "guarded
by existing owner closure and not separately mutated". D1 shows the new
interface itself ignores the parent's exact source/replay refs; existing I05
closure does not repair that because the recurrence consumer supplies the
grammar without a parent-binding check. This is part of D1, not a separate
scientific claim.

## Positive findings retained

- R3 A1 conditioned JOINT/CO_TRAVEL, A2 canonical operation ID and A3
  empty/unsupported/pending controls: 10/10 prior reviewer probes pass on this
  candidate.
- Author R4 suite: 24/24 pass, including actual three-generation I05 execution,
  per-generation exact anti-join, cold persisted-handoff subprocess, protected
  nonwinning exploration, neutral-aggregate hidden differentiation, D/K/cap
  typed checks, and renamed/transformed profile execution.
- Comparator structure: probe B6 confirms root-relative and parent-relative
  generation-2 jobs use distinct baseline predicate hashes and distinct expected
  condition sets; both execute. Value-level opposite-direction arithmetic is a
  remaining independent falsifier, not a claimed pass.
- Profile refusals: missing/malformed J/K/D, unknown counting convention,
  non-TEST_ONLY grade, missing comparator, and negative caps raise typed
  `ValueError`s (probe B4).
- Per-generation cap leaves explicit `unissued` records with reasons (author
  suite/probe inspection).

## Preserved limitations

Reference caps (J=2,K=3,D=3; 4 per generation/12 total; transformed D=2 etc.)
are TEST_ONLY demonstration parameters, not source/science defaults. No R03,
U43/Batch, R04 custody, R05 grades, original 35/1890, global F6/F7/F8, N11/N12,
Sorok, production/CI or J52/W52 activity. The legacy unconfigured-A4 gap label
is not globally deleted by this candidate.
