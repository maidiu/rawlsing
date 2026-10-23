# R61-R01V R5 defects and limits — REVISE

Verdict: **REVISE**. The R5 candidate preserves the R3 A1–A3 controls and real
D=3 native execution, and it repairs the R4 issue-time bargraph: severed,
missing, wrong-predicate, wrong-source and unbound integer attacks now raise
typed refusals. However, the published claim that receipt binding is checked
"again before execution" is false, ancestry and producer generation are not
bound to an independent artifact, and a caller can replace the predecessor plan
object with a self-consistent undercount. A4 therefore remains unqualified at
the exact generic consumer grain. Candidate files were not edited.

Repro commands (all under the reviewer return root):

```sh
/usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r5/independent_probes/test_r01v_r5_reviewer.py \
  -q -o addopts=''
/usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r5/independent_probes/defect_demonstration.py
```

The first command exits 1 with exactly the seven expected-refusal failures
below; the second records the candidate's accepted behavior in
`evidence/defect_demonstrations.json`.

## D1 — Execution does not revalidate the embedded parent binding (blocking)

**Contract:** commission item 1 ("before issue and again before execution");
amendment "before issue and again before execution ... predicate, receipt ref,
handoff ref, canonical parent id, source releases".

**Observed:** `execute_recurrence_generation`
(`rawlsing_next/universal_grammar/native_map.py:1450`) checks only that a
receipt-bound parent has a non-`None` handoff, that
`parent.source_release_refs` equals the execution releases, and that
`replay_recursive_branch_membership` accepts the embedded handoff. It never
checks `handoff.ref == parent.replay_binding_ref`,
`handoff.receipt_ref == parent.receipt_ref`,
`handoff.winning_predicate == parent.predicate`, or the canonical parent id. It
also has no resolver argument, so it cannot re-resolve the binding.

**Repro (H3):** build a valid generation-2 plan, replace only its parent's
`handoff` with a different valid handoff from the same source (same releases),
keep the original receipt/replay refs and predicate. Execution accepts the
altered plan and the anti-join is `no_drop_ok: true`
(`evidence/defect_demonstrations.json`, `H3_execution_binding`). The returned
generation then binds a plan whose declared receipt/replay refs do not match
the handoff that was replayed. This is not a typed refusal and it is not the
declared binding check.

**Required:** re-resolve/validate the receipt-bound parent at execution against
the trusted resolver, or carry an unforgeable validated binding token; require
handoff/predicate/receipt/replay/canonical-id equality before the I05 call.

## D2 — Receipt-bound ancestry is not bound to the parent identity (blocking)

**Contract:** commission item 2 ("Full ancestry/source/root/policy must remain
bound"); item 3 binds the ancestor-conditioned plan/chain.

**Observed:** `_validate_parent_resolution`
(`native_map.py:1069`) recomputes `parent_id` from
`(kind, predicate, generation, (receipt_ref, handoff_ref))` only.
`ancestry_conditions` and `ancestry_predicates` are neither in the parent id nor
compared with the handoff. Replacing them leaves `parent_id` unchanged.

**Repro (H1):** take a canonical generation-1 receipt-bound parent with one
ancestry condition, replace
`ancestry_conditions=()`/`ancestry_predicates=()`, and issue generation 2. The
issue is accepted, the root-relative rule loses its ancestor condition, and
execution returns `no_drop_ok: true`
(`evidence/defect_demonstrations.json`, `H1_ancestry_strip`). This changes the
actual conditioned contrast and lets a caller silently rewrite lineage.

**Required:** bind the exact ancestry material (condition keys/values and
predicate refs) into the canonical parent identity and validate it against the
persisted handoff/receipt chain; reject any difference.

## D3 — A receipt-bound parent can be relabelled to skip a generation (blocking)

**Contract:** commission item 2 ("G>1 actual parent from G-1 ... skipped/
relabelled/stale generation ... must not bypass"; "an actual generation N
receipt/activation is necessary for N+1").

**Observed:** generation continuity is checked only against the caller-written
`parent.generation` field. The canonical id folds that same field into the
hash, so changing both the field and the recomputed id is self-consistent. The
recursive handoff contains no independent producer-generation anchor that the
validator compares.

**Repro (H2):** take a generation-1 receipt-bound parent and a genuine
generation-2 predecessor plan; relabel the parent `generation=2` and recompute
`parent_id` with the candidate's own `_parent_id`. Issuing generation 3 is
accepted and executes with `no_drop_ok: true`
(`evidence/defect_demonstrations.json`, `H2_generation_relabel`). The real
handoff was produced by generation 1, so an entire generation is skipped.

**Required:** make producer generation an independently authenticated property
(for example, bind it into the handoff/branch ancestry and compare, or maintain
a trusted coordinator chain record keyed by handoff ref), not a caller field
that the id recomputation merely echoes.

## D4 — Replacing the predecessor plan undercounts issued work (blocking)

**Contract:** commission item 3 ("A caller copy/replace/recompute of the
dataclass must not undercount prior issued work or counterfeit a valid chain";
"derive or validate count against retained predecessor records").

**Observed:** `build_recurrence_issue_plan` validates only that
`previous_plan.cumulative_issued_count == previous_plan.predecessor_issued_count
+ len(previous_plan.expected_operations)`. All three terms belong to the
caller-supplied plan object, so a `dataclasses.replace` that removes issued
operations and lowers the cumulative count passes.

**Repro (H4):** with `total_issued_cap=5`, a real generation-1 plan issues 4
operations. Replace it with the first 2 operations and
`cumulative_issued_count=2`. The honest generation-2 plan issues 1 operation;
the forged predecessor is accepted and generation 2 issues 3 operations with
`predecessor_issued_count=2`
(`evidence/defect_demonstrations.json`, `H4_predecessor_undercount`). This is
exactly the undercount the commission prohibits.

**Required:** bind the predecessor to retained issuance/execution records or a
trusted append-only ledger (exact predecessor plan ref plus count derived from
records outside the mutable plan object), and cross-check the predecessor's
expected operations against its bound grammar/actual receipts. Internal
self-consistency of the replaced object is insufficient.

## D5 — The root parent is not bound to the declared source root (blocking)

**Contract:** commission item 2 ("Full ancestry/source/root/policy must remain
bound"); amendment "Root parents are source-root predicates only".

**Observed:** generation 1 accepts any `PARENT_ROOT` generation-0 parent even
when its predicate is not `root_predicate`. The grammar then uses one predicate
as the root atom and a different predicate as the parent atom.

**Repro (H6):** build generation 1 with `root_predicate` = the source root but
`root_parent.predicate` = a response-condition predicate. Issue and execution
succeed with `no_drop_ok: true`
(`evidence/defect_demonstrations.json`, `H6_root_parent_mismatch`). The
root-relative view is anchored to the declared root while the parent-relative
view is anchored to an unrelated root predicate.

**Required:** require the root parent predicate ref and source releases to
equal the declared root identity, and include that equality in the plan
validation.

## D6 — Zero per-generation cap is not represented as stopped budget (secondary)

`per_generation_issued_cap=0` is accepted by `RecurrencePolicy` but
`build_recurrence_issue_plan` reaches the empty-rule path and raises
`RECURRENCE_GENERATION_ISSUED_NO_OPERATIONS` instead of returning a
`STOPPED_BUDGET` plan with explicit unissued entries (H5). The typed refusal is
not a bare crash, but it is not the commissioned honest budget state. Handle a
zero per-generation cap like the zero remaining-total case.

## D7 — Activation does not enforce the actual next-generation label (secondary)

`activate_next_generation` checks only `next_generation > D`; it accepts
`next_generation=1` for a generation-1 result, returns
`activation.generation=1`, labels the children with producer generation 1, and
those children are still usable to issue generation 2 (H7). The producer label
is correct, so this is not itself a generation skip, but the activation label
is not the enforced next generation as the contract requires. Require
`next_generation == generation.plan.generation + 1` before becoming inactive.

## Positive findings retained (not acceptance)

- Author suite replayed independently: 26 passed, 0 failed/error/skip.
- R3 A1–A3 controls replayed independently: 10 passed.
- Reviewer changed-data D=3 positive: 2 passed (main + fresh-process cold
  restore). Independent operation-set content/multiplicity and typed-state
  arithmetic matched; a neutral 50%/50% exploratory parent contained 75%/25%
  opposite-direction q2 subgroups; both root- and parent-relative baselines
  were distinct and executed.
- Issue-time refusal repairs for the R4 B1/B5 family (severed receipt, missing
  handoff, wrong source release, unbound `total_issued_before`, root as G2) do
  pass under the new API.
- The author manifest's 7 report hashes and four code blobs were independently
  reproduced; manifest self-exclusion is explicit.

## Minimal missing function / owning seam

`rawlsing_next/universal_grammar/native_map.py`:

1. At execution, re-resolve the parent binding against a declared trusted
   resolver and require handoff/receipt/replay/predicate/canonical-id equality;
   do not trust the embedded `plan.parents` object.
2. Bind exact ancestry material and producer generation into the canonical
   parent identity/authenticated handoff chain, and reject stripped/relabelled
   ancestry or generation.
3. Bind predecessor plan ref/count to retained issuance or executed-receipt
   records outside the plan object, so `replace` cannot undercount.
4. Bind the root parent predicate/source releases to the declared root.
5. Return `STOPPED_BUDGET` for a zero per-generation cap.
6. Enforce `next_generation == generation.plan.generation + 1`.

## Preserved limitations

Reference caps/rows are TEST_ONLY synthetic engineering, not source science.
The trust seam remains a declared trusted coordinator resolver, not a protected
issuer, signing service, global durable uniqueness, or R09 isolation.
R04/R09 service-level fork prevention is NOT_REACHED. No R03 wake, R03
qualification, self-adoption, original 35/1890, global F6/F7/F8, N11/N12,
Sorok, production/CI or J52/W52 claim follows.
