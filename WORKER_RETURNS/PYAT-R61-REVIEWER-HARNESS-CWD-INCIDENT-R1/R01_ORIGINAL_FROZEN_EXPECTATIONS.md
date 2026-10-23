# R61-R01V R5 independent expectations — frozen before candidate code/author conclusions

Status: reviewer-owned oracle frozen and committed before reading R5 candidate
code, R5 author test bodies, or the R5 author return. Sourcefree TEST_ONLY.
Reviewer session is distinct from author `ses_e98c905cbffekusoHURfKyEUKG`.
Same opencode-go/deepseek-v4.1-flash account; role/session/worktree separation
only, not institutional independence and not proven OS isolation.

## Exact target, startup and write scope (verified before freeze)

- Commission: `9307abc2a9a4177fc8964496334e74694f8ba711`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R01V/revisions/r5/00_COMMISSION.md`.
- Exact candidate/startup: `4b5fd7a240a6e2d007ba1df2424780e6b5612ea9`
  (author branch `agent/opencode-pyat-r61-generic-grammar-r1`).
- Exact candidate code commit: `c9cd59536e9323e6f48f1818bd41204cc6ae6095`.
- Reviewer branch `agent/opencode-pyat-r61-r01v-r5-independent-review-r1`.
  The commissioned worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`
  was outside this session's permitted filesystem scope; the reviewer therefore
  reused the same repository checkout in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-flight-director` detached
  at the exact candidate/startup commit, and writes only the assigned return
  root. This environment deviation is disclosed; it is not candidate code
  inspection and does not change the oracle. Reviewer pushes non-force to the
  assigned branch and directly verifies the final pushed SHA.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r5/`; probes,
  mutant copies, JUnit and witness remain below that root; `.r61`, pycache and
  all candidate/native/HQ/old-return paths stay untouched. No candidate repair,
  self-adoption, worker wake, R03 start, source/science/CI/prod/N11/N12/Sorok/
  J52/W52 activity. Python `/usr/local/bin/python3`; existing checkout, no new
  repository copy.
- Governing inputs read before this freeze: R61L E1-E6
  `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`; R61M user S1/S2 approval
  `37dba2837c94ddb71287ffbc18260d051fc9765a`; R5 author commission
  `df2fdd12a55e1c153e2b60377c903a764ff59f26`; frozen R5 amendment
  `63fe9ebf110e76326a07b9d0badf0ab7b208af6f`; R4 independent review
  `634ee0dac4ef87347d6f334f6c8c1abc97b24d01` (return, defects, probes,
  oracle); frozen R4 profile `f3601f418d79c83d467ce8dd0ed1c0113c31d7e8`.
- Expected code allowlist: `rawlsing_next/universal_grammar/types.py`,
  `enumerate.py`, `native_map.py`, `rawlsing_next/tests/test_universal_grammar.py`;
  four code blobs to be identified exactly in the return manifest. Candidate
  report root `WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r5/`;
  its manifest must exclude itself and its hashes must be independently
  reproduced, not trusted. Author replay is supporting evidence only.

## Settled contract extracted before code inspection

The settled product intent is finite adaptive social-world/minority/
counterpattern discovery with source-root-relative and immediate-parent-
relative views preserved separately (R61M S1/S2), implemented as finite
versioned adaptive issue transactions over the existing source/risk-bound
predicate and receipt/replay handoff (R61L E1-E6). It is not exhaustive
subdivision, not an unbounded Cartesian materialization, not original-source
science, and not an R03 wake. R3 A1-A3 and the inherited engine remain.

The R5 amendment fixes one generation convention: `RecurrenceParent.generation`
is the generation that **produced** the parent (root=0; a generation-1 child
means producer generation 1). Issue for G=1 requires exactly one root parent at
generation 0; G>1 requires non-root parents whose producer generation is G-1;
mixed/root/duplicate/skipped labels and G>D refuse. Issue, activation,
execution and persistence must consume the same versioned convention; no silent
relabel.

The trusted seam is a declared host/coordinator catalog supplied as a
`RecurrenceParentResolver`, created by `load_recurrence_parent_resolver` from
the existing recursive-handoff loader (or a validated in-process tuple of
`RecursiveBranchHandoff`). It is trusted configuration, never a catalog
generated from the untrusted parent it purports to authenticate. The module may
claim consistency under that resolver plus existing owner authority/replay and
must not claim a protected issuer, signing service, global durable uniqueness,
fork prevention, or R09 isolation.

## Independent oracle (reviewer-owned; not read from candidate output)

1. **Receipt-bound parent binding (issue AND execution).** Every
   `PARENT_RECEIPT_BOUND` parent must be resolved from the configured trusted
   resolver and must match: canonical parent id recomputation, exact
   `handoff`/`replay_binding_ref`, `parent.predicate == handoff.winning_predicate`,
   `receipt_ref == handoff.receipt_ref`, source-release/edition set equality with
   the handoff and the actual execution releases, relevant generation/ancestry,
   and existing owner authority/replay membership. Missing, severed, fabricated,
   stale, cross-source, wrong-edition, wrong-replay, wrong-authority,
   wrong-predicate and wrong-ancestry binding must typed-refuse at the SAME
   next-generation I05 consumer before issue and again before execution as
   applicable. Equality of two caller-fabricated descriptors is not
   authoritative. Immutable/self-consistent forged descriptors must be tested
   against the SAME configured resolver. Exploratory parents stay explicitly
   receipt-free, source/risk-valid, and never become fabricated winner receipts.
   Root parents stay root predicates only and cannot carry a winner receipt.
2. **Generation continuity.** Independently test issue, activation, execution
   and persisted restore at generations 0/1/2/3, including duplicate/mixed
   parents, root relabelled as G>1, skipped/relabelled generation, stale
   predecessor, and altered plan after creation. A root-only G=2 call and a
   G=N+1 call whose parent was not produced at N must refuse. An altered plan
   after creation must not bypass actual execution. Full ancestry/source/root/
   policy must remain bound.
3. **Predecessor issue-chain accounting.** The expected operation set must be
   independently constructed before execution and compared by content and
   multiplicity, not count alone. A plan must bind its actual predecessor
   plan identity/count, policy hash, root, generation, exact expected operation
   ids and state. A caller copy/replace/recompute of the dataclass must not
   undercount prior issued work or counterfeit a valid chain. Generation 1 has
   no predecessor; later plans require the matching immediate predecessor
   chain/root/policy. Per-generation and total caps are checked before
   unbounded materialization. Exhaustion returns explicit `STOPPED_BUDGET` /
   unissued/PENDING entries with reasons and performs no native execution; no
   false native success, no bare crash, no fabricated empty success. Cold
   restore retains the same chain and exact issued operations. Service-wide
   durable uniqueness/fork prevention is R04/R09 and NOT_REACHED here; the
   actual trust seam must be named, not merely a caller integer renamed.
4. **Comparators and discovery.** `ROOT_RELATIVE` and
   `IMMEDIATE_PARENT_RELATIVE` are separately identified, actually executed
   requests with correct independent root/parent baselines and values,
   including a case where the child is above its parent but below its root (and
   the reverse where supported). Distinct predicates/refs alone do not prove
   value arithmetic. Independently construct a changed-data neutral-aggregate
   hidden minority/counterpattern and show a valid nonwinning exploratory
   parent is issued/activated/executed through the public actual interface, not
   only an author fixture. Changed caps/data/inventory/branching must change
   the mechanism accordingly; arbitrary renaming alone is insufficient.
   Exploration is activation/bookkeeping, never a finding; no mandatory
   complement and no invented scientific threshold.
5. **Preservation and wiring.** R3 A1 conditioned JOINT/CO_TRAVEL, A2 canonical
   IDs, A3 unknown/unsupported/valid-empty/PENDING, and J/K/D separation with
   explicit ancestor-conditioning counts must still pass. Retained controls may
   require mechanical versioned fixture/API adaptation only; no importerror may
   be counted as product failure and no archived test may be edited. Review the
   exact public R03-facing interface wiring and any unwired/unsupported new A4
   edge. The legacy unconfigured-A4 gap label remains distinguishable.
6. **Same-consumer fault/restoration/cold proof.** On the SAME public consumer:
   baseline passes, a meaningful parent/receipt/source/plan/policy mutation
   refuses or changes the result as required, restoration passes, and a fresh
   process replays the persisted chain. Predicates must affect real facts, not
   labels. Signature/import/setup crashes, skips or helper-only assertions do
   not count as typed refusals or positive capability.
7. **Honesty and verdict rule.** Record actual commands, exits, skips,
   environment, imports, trust assumptions, incomplete arithmetic/minority/
   identity obligations and all NOT_REACHED boundaries honestly. Candidate
   passes alone are not acceptance. `ACCEPT_SCOPED_LOCAL` only if A4 is
   genuinely qualified at the exact generic consumer under the declared trusted
   catalog/TEST_ONLY profile; otherwise `REVISE` with the minimal reproducible
   missing function. No original/world/full-machine/science or R03
   qualification follows. Reviewer does not repair or adopt.

## Planned independent evidence

- Reviewer-owned EXPECTATIONS (this file) committed before code inspection.
- Independent replay of author tests (JUnit/log) and R3 A1-A3 controls with
  reviewer-owned JUnit; author pass alone is not acceptance.
- Own positive chain probe at D=3 through the public interface with independent
  expected operation/root/ancestry/comparator computation, real I05 execution
  and persisted cold restore.
- Own hostile probes: forged/severed/missing/stale/cross-source/wrong-edition/
  wrong-replay/wrong-authority/wrong-predicate parent binding; root-relabel/
  skipped/mixed/duplicate generation; predecessor undercount/copy-replace/
  altered prior plan/policy/root; cap exhaustion and no-native-call witness;
  same-consumer mutation -> refusal/assertion fail -> restore -> pass.
- Own changed-data hidden minority/counterpattern and nonwinning exploration;
  opposite-direction root/parent value arithmetic; changed inventory/labels/
  caps/domains.
- Exact blob/source/report hashes, manifest self-exclusion, path scope, actual
  imports and direct remote readback of reviewer and candidate branches.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/` + JUnit/results, `proof_witness.json`, `manifest.json`
with explicit self-exclusion, `RESUME.md`. Max 45 minutes total, bank coherent
evidence by 35, stop at the decisive bounded verdict. No candidate edit, no
self-adoption, no R03 wake.
