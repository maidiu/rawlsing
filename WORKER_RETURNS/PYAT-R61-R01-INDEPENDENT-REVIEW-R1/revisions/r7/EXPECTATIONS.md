# R61-R01V R7 independent expectations — frozen before R7 code/author inspection

Status: reviewer-owned successor oracle frozen and committed before reading R7
candidate code, R7 author test bodies, R7 author return, or any R7 API/record
contract. Sourcefree TEST_ONLY. Reviewer is the existing distinct session
`ses_e96304356ffeC8HSvwFluWOjG1`, never author
`ses_e98c905cbffekusoHURfKyEUKG`. Same opencode-go/deepseek-v4.1-flash
MAX/Global account; role/session/worktree separation only, not institutional
independence and not proven OS isolation.

## Exact target, startup and write scope (verified before freeze)

- Commission: `fbb162a0717bb067b7f2e244d738c33cd13f49af`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R01V/revisions/r7/00_COMMISSION.md`.
- Exact candidate/startup: `9c0f81ecb76ffe35d0190e31492ea1e9b568f01b`.
- Exact candidate code: `0271a7e37a3ccccce5ff69db99f56f7745a62875`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r7-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, same top level,
  expected branch, no tracked changes.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r7/`.
  Probes, versioned adapters, snapshots, JUnit and witness remain below that
  root. Candidate, native owners, HQ/director checkout, old R5/R6 oracles,
  other nodes, original data, CI/prod/N11/N12/Sorok/J52/W52 stay untouched.
- Governing inputs read before this freeze: full R61AF
  `e349da0d886d8e365648afccf40a2e6b8e105ff7`
  (`R61AF_R01_RESTORE_AND_CONTEXT_ADJUDICATION.md`,
  `R61AF_DECISIONS_AND_ROUTING.json`,
  `R61AF_DECISION_INPUT_IDENTITIES.json`); full R61V
  `8c03f95ca77a4c874449fff67a4032f83d9d0a02`; R61L E1-E6
  `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`; R61M S1/S2 approval
  `37dba2837c94ddb71287ffbc18260d051fc9765a`; prior exact independent review
  `568ff717662ac1ee63d29bad3080deaf10bd17f9`. R61AF reclassifies the prior D3
  forged-snapshot-plus-forged-pin case as host-trust replacement, not an
  in-scope refusal requirement; that correction is incorporated below.
- Four code paths remain the expected R01 allowlist:
  `rawlsing_next/universal_grammar/types.py`,
  `rawlsing_next/universal_grammar/enumerate.py`,
  `rawlsing_next/universal_grammar/native_map.py`,
  `rawlsing_next/tests/test_universal_grammar.py`.
  Author report root `WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r7/`;
  its manifest must self-exclude and its 8 report hashes plus 4 code blobs must
  be independently reproduced, not trusted. Author 31 passes are supporting
  evidence only.

## Settled corrected contract extracted before code inspection

R61V remains the architecture. R61AF does not reopen architecture, product
intent or science; it corrects the fixed-pin interpretation and requires one
cohesive whole-function state-transition/serialization repair.

### A. Trust, creation and freeze
- One trusted local campaign owner retains issuance, actual native execution,
  parent lineage and activation history. Retained records, not caller plans,
  parents, counters, views, handoffs, resolvers or snapshot bytes, establish
  history.
- Create resolves every release/root/query/catalog predicate in the actual
  configured repository and validates existing native source/universe/risk/
  authority closure and target/query compatibility. Nonexistent but
  well-formed release refs refuse before any native call. Duplicate typed
  catalog keys (including conflicting duplicate predicates) refuse rather than
  overwrite.
- Freeze pins semantic native configuration and canonical object
  identities/materials. Trusted host callables remain host configuration; no
  process-specific id()/hash is portable authority. Cold context is
  re-provisioned by the trusted host and checked against the declared semantic
  owner/version/source/query inventory. Dishonest host code is outside the
  claim.
- A different caller-created campaign may exist but cannot certify or mutate
  the original campaign's history. Same-UID/root/private-state/monkeypatch
  attacks are outside the declared local grade.

### B. Chronological issue and discovery generation
- Issue sequence/head is chronological and independent of discovery
  generation. Root 0 may issue multiple separate generation-1 batches under
  the existing finite policy. Later generations may also have multiple
  explicit batches.
- Every committed issuance, including stopped/no-work, advances the
  chronological predecessor/head. Stopped records add zero work. Cumulative
  workload counts derive only from exact issued-operation material and
  retained records; failed/unrun work cannot erase or refund counters.
- Parent-generation compatibility is independently checked from actual parent
  lineage, not inferred from the previous issuance's generation. Mixed/stale/
  skipped/relabelled parent labels refuse.
- Bounds are checked before large materialization. Zero per-generation or zero
  total cap returns explicit stopped/no-work with honest unissued reasons, no
  native call and unchanged workload count.

### C. Execute and full parent binding
- Execute resolves source/root/query/native authority and every retained
  parent identity again at the actual invocation. It compares full
  ancestry/predicate/receipt/handoff/replay/source/campaign/policy relation,
  not four selected fields.
- Every receipt-bound parent must match canonical parent identity,
  handoff/replay refs, winning predicate, receipt ref, source/release/edition,
  full ordered ancestry and admissible authority. Missing, severed, fabricated,
  stale, cross-source, wrong-edition, wrong-replay, wrong-authority,
  wrong-predicate or wrong-ancestry binding is a typed refusal at issue AND
  execution as applicable.
- No missing native material may silently drop through a filtering
  comprehension. A public plan/parent/view, if accepted for compatibility,
  must equal retained canonical material in every identity-bearing field;
  rehashed/recomputed views cannot register authority.
- Actual receipts and typed states, not handoff-only winners, back execution
  and activation. Handoffs alone omit unsuccessful operations and are
  insufficient.

### D. Completed-prefix activation and restore
- Retain a canonical activation preimage for every completed execution:
  issued plan/expected-operation material; exact native receipt material and
  typed states indexed by actual operation/rule; corresponding canonical
  handoffs; source/query/authority/replay identities; exact no-drop
  reconciliation. This is existing execution output, not caller evidence.
- Restore verifies complete referential closure against the separately trusted
  original pin and actual supplied native context, reconstructs the activation
  input using existing native object representations (or an equivalent
  record-backed view), and invokes the SAME activation policy/helper used live.
  Live and cold activation consume one checked record projection; no second
  independent activation algorithm.
- Snapshot after completed execution but before activation -> fresh-process
  restore -> real activation -> N+1 must pass WITHOUT rerunning or recounting
  the original execution and without a new budget charge. Repeated activation
  returns the original retained activation.
- Existing already-activated snapshot -> activate returns its existing result
  before demanding an unnecessary raw native_result.
- Inflight/ambiguous execution remains typed HOLD; it cannot be turned into a
  completed or safely unexecuted record. R04/R09 global crash/durability
  guarantees remain separate.

### E. Fixed original-pin restore semantics (R61AF correction)
- `expected_checkpoint_ref` stays outside subject payload selection. The
  trusted coordinator captures/retains the original pin independently of the
  snapshot. Configure the coordinator once, save the pin separately, and submit
  altered/rehashed snapshots through that SAME configured ingress.
- Missing pin refuses. A substituted/mutated/rehashed snapshot with the fixed
  original pin refuses. A genuine snapshot restores.
- Changing the trusted coordinator or supplying both a forged snapshot and a
  forged pin is host-trust replacement, outside the in-scope refusal gate; it
  may be documented only as a host-trust demonstration, not used to claim a
  product bypass and not used to demand a new pin registry/signing service.
- Restore also checks supplied query ref/content, complete typed condition
  inventory, policy/root/releases and stable native context against frozen
  context before accepting records; checks ordered chronological history,
  counters, exact expected sets/multiplicity, execution and activation closure.
- Legacy handoff bundles without campaign history cannot be relabelled as
  arbitrary generations; typed missing-lineage refusal is required.

### F. Same configured coordinator fault/restoration
- SAME original configured campaign: baseline passes; meaningful
  source/receipt/parent/history/plan/policy mutation refuses or fails the
  required assertion; restored genuine state passes.
- No duplicate native calls on retry; no new budget charge for restored
  already-completed work; no public view/record injection; no all-refuse
  pseudo-success.
- Preserve ordinary A1-A3 lowering and native paths, changed-data D3,
  root/parent numerical comparisons, neutral-aggregate hidden 75/25
  minority/counterpattern, nonwinning exploration, J/K/D separation and every
  receipt typed state. Exploration remains distinct from a supported finding.

## Independent oracle and planned falsifiers

### 1. Positive changed-data D=3 and arithmetic
Use 16 changed rows with q1/q2/q3/out: root 8/16 = 50%; q1=0 4/8 = 50%
(neutral); q1=1 4/8 = 50%; inside q1=0 the q2 subgroups are 3/4 and 1/4
(75%/25% opposite); preserve the same construction at q1=1. Independently
freeze expected operation tuples (producer lineage ref, comparator, ordered
condition keys/values, target/query, baseline ref) and multiplicity BEFORE
execution; both root and parent comparator jobs count. Independently
recompute typed states from raw rows for every operation. Require genuine D3
native execution, nonwinning exploratory lineage, distinct root/parent
baselines and the hidden 75/25 opposition. No selected fixture is a universal
policy claim; change data/inventory/caps in at least one extension.

### 2. Full F1-F6 matrix
- F1: positive changed-data/native D3, real root/parent values, hidden
  minority, nonwinning exploration; A1-A3 preserved.
- F2: every R5 H1-H7 and R6 successor attack through the SAME configured
  owner, including strip/reorder/substitute ancestry, recomputed parent
  hash/generation, handoff swap, dropped/undercounted predecessor jobs,
  root/policy/release mismatch, activation-label change and zero caps. Both
  issue and execution must refuse wrong claims; native call counters prove
  refusal before the wrong native invocation. Restored genuine views pass.
- F3: deep-mutated views, rehashed self-consistent plan/counter/parent/snapshot
  objects, public record registration/import, arbitrary callables/results,
  copied handoffs across different producing issues/campaigns, and legacy
  no-owner recurrence helpers. No authority appears without a matching
  retained record or checked native transition; legacy helpers are explicitly
  unqualified/typed-refuse and cannot feed the accepted path.
- F4: exact operation sets/multiplicity/counts across >=2 generation-1 batches
  and later generation batches; every committed issuance advances chronology;
  stopped/no-work records add zero work but stay in history; failed/unrun work
  cannot disappear/refund; retry and run-local concurrency at the exact claimed
  scope.
- F5: fixed original-pin restore as above; pre- and post-activation
  fresh-process proofs; mutated/rehashed snapshot with fixed pin refuses;
  missing/wrong pin/source/root/policy/query/catalog typed-limits; genuine
  snapshot restores; no duplicate original execution or budget charge.
- F6: same configured consumer baseline -> meaningful source/receipt/parent/
  plan/history mutation refusal/failure -> restoration -> fresh-process N+1;
  actual native imports/blobs, commands/exits/skips/counts/runtime/memory,
  JUnit and all NOT_REACHED obligations. No import/signature/setup crash is
  counted as a typed product refusal.

### 3. Create / execute / restore context substitutions
- Create with a nonexistent well-formed release, a root predicate outside the
  release/source/authority closure, a query incompatible with the target/root,
  or duplicate/conflicting condition catalog entries must refuse before any
  native call.
- Execute must re-resolve the retained release/root/query/authority and full
  parent lineage; missing native material must not be filtered away.
- Restore with wrong query content/ref, incomplete/duplicate condition
  inventory, wrong policy/root/releases or wrong native context must refuse
  typed before accepting records. Altered full history with recomputed internal
  hashes and fixed original pin must refuse.

### 4. Chronology/no-work/activation
- Two generation-1 batches with independently computed exact counts; both
  counted, predecessor chain chronological, no one-batch restriction.
- Later-generation multiple batches; cumulative counts exact; parent
  generation compatibility independent.
- Zero per-generation and zero total caps; stopped/no-work records advance
  chronology, no native call, no refund.
- Stopped issuance followed by another committed issuance; predecessor head is
  the stopped record, count unchanged.
- Completed-prefix pre-activation restore -> activation -> N+1 without
  re-executing/recounting; post-activation restore -> existing activation
  before raw native result; retry idempotent; concurrent execute one native
  call.
- Inflight/ambiguous state remains typed HOLD; do not fabricate completed or
  unexecuted records.

### 5. Receipt states and exploration
- Every actual receipt state used by the mechanism must be retained and
  propagated, including valid-empty/no-result/unsupported distinctions; do not
  invent supported receipts or use handoff-only winners. Exploratory children
  remain receipt-free/explicitly tagged and never become fabricated winner
  receipts.
- Preserve nonwinning exploration and S1/S2 root/parent comparison identities;
  changed caps/data/inventory/branching must change the mechanism
  accordingly; renaming alone is insufficient.

### 6. Honesty and verdict
Record actual commands, exits, skips, imports, environment, counts, runtime,
memory, trust assumptions, all partial/unverified obligations and every
NOT_REACHED boundary. Author passes alone are not acceptance.

`ACCEPT_SCOPED_LOCAL` only if the whole generic recurrence facade genuinely
satisfies R61V and corrected R61AF under the declared local trusted
coordinator/TEST_ONLY profile, including F1-F6, fixed-pin restore, complete
chronology, complete parent binding, full receipt-backed cold activation and
the same-consumer fault/restoration proof. Otherwise `REVISE` with the exact
minimal reproducible missing function. R03 remains NOT_STARTED. No
original/world/full-machine/science qualification follows. Reviewer does not
repair or adopt.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` with explicit self-exclusion, `RESUME.md`. Max 45 minutes/bank
35; stop after decisive bounded review. No candidate edit, no self-adoption,
no R03 wake, no new court, no review-of-reviewer. R08/R61Q is a separate lane
and is not inspected, repaired or certified here.
