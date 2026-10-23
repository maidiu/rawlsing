# R61-R01V R6 independent expectations — frozen before R6 code/author-contract inspection

Status: reviewer-owned successor oracle frozen and committed before reading R6
candidate code, R6 author test bodies, R6 author return, or the R6
`API_AND_RECORD_CONTRACT.md`. Sourcefree TEST_ONLY. Reviewer session is the
existing distinct reviewer session `ses_e96304356ffeC8HSvwFluWOjG1`, never the
author session `ses_e98c905cbffekusoHURfKyEUKG`. Same
opencode-go/deepseek-v4.1-flash MAX/Global account; role/session/worktree
separation only, not institutional independence and not proven OS isolation.

## Exact target, startup and write scope (verified before freeze)

- Commission: `d737562873558ce01116f079815b00bdb06416fe`
  `WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R01V/revisions/r6/00_COMMISSION.md`.
- Exact candidate/startup: `fea3ca17d94183efbd526dc1687ae06b7bbbf0f7`.
- Exact candidate code commit: `3d60f9cb6f43830244fbd79699d1cf4041622d05`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r6-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, same top level,
  expected branch, no tracked changes.
- Reviewer writes only
  `WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r6/`.
  Probes, mutant copies, snapshots, JUnit and witness remain below that root.
  `.r61`, pycache, candidate, author returns, native owners, HQ, workflows,
  config and old R5 evidence remain untouched.
- Governing inputs read before this freeze: full R61V retained-owner contract
  `8c03f95ca77a4c874449fff67a4032f83d9d0a02`
  (`R61V_R01_RETAINED_CAMPAIGN_OWNER_DECISION.md` and `R61V_DECISIONS.json`);
  R61L E1-E6 `3cb1d659bc9efb10b307e66db5cf26af3256f1f5`; R61M S1/S2 approval
  `37dba2837c94ddb71287ffbc18260d051fc9765a`; prior R5 independent review
  `537bd3985d8a3825186e41cab9308d8150cac848` (return, defects, oracle and
  probes remain unchanged).
- Author R6 prescriptive contract `e2b87e6c33364e5361ed3c0b10ba5c13e34efbba`
  (`API_AND_RECORD_CONTRACT.md`) is NOT read before this freeze. Exact API
  names are therefore not used as oracle; the semantics below are fixed first.
- Expected code allowlist: `rawlsing_next/universal_grammar/types.py`,
  `enumerate.py`, `native_map.py`, `rawlsing_next/tests/test_universal_grammar.py`;
  four code blobs to be identified exactly and reproduced independently.
  Candidate report root `WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r6/`;
  its manifest must exclude itself and its seven report hashes plus four code
  blobs must be independently reproduced, not trusted.

## Settled contract extracted before code inspection

R61V replaces handoff-only/caller-dataclass self-consistency with one trusted,
local campaign owner. Its privately retained records, not caller-supplied plan,
parent, counter or snapshot objects, establish campaign history. Issue, execute,
activate and cold restore consume the same record authority. The existing C11/
I05/recursive-handoff native machinery is reused unchanged. No new empirical
engine, source adaptor, issuer service, protected runner, R03/R04 reversal or
scientific threshold is authorized. R03 remains NOT_STARTED.

The product meaning remains R61L E1-E6 plus R61M S1/S2: finite adaptive
social-world/minority/counterpattern discovery, separately identified
source-root-relative and immediate-parent-relative views where comparable,
finite versioned issue transactions, explicit issued-versus-potential
accounting, exploration distinct from evidence, and no exhaustive subdivision.
J/K/D and explicit ancestor-conditioning remain separate. Root is producer
generation 0; a child produced by discovery generation N feeds N+1.

A. Trust and ownership:
- Trusted coordinator creates a campaign before subject inputs and deeply
  snapshots identity-bearing policy, root, source/release/risk, inventory,
  native authority/executor configuration. Retaining mutable public dicts by
  reference is not a freeze.
- The campaign privately retains canonical records and exposes no
  subject-facing registration of arbitrary plan/execution/parent/counter/snapshot
  truth.
- Public dataclasses, recomputed hashes, freshly built resolvers, copied native
  handoffs and correct-looking plans are untrusted data until matched to this
  campaign's retained records.
- A different caller-created campaign may exist but cannot mutate or certify the
  original campaign's history. Same-UID/private-state/monkeypatch/ptrace/root,
  dishonest coordinator setup and global service compromise are excluded from
  the declared local trusted-runtime claim.

B. Required canonical records:
- Campaign root: campaign ref/schema, frozen policy material/hash and
  counting/budget unit, exact governed source/root predicate content/ref,
  releases, native scope/authority/consumer determinants, trusted native
  configuration identity; root parent generation 0 equals this root and has no
  winner receipt.
- Issuance: monotone issue sequence/ref, predecessor issuance ref, actual
  discovery generation, parent-lineage refs, full grammar and exact expected
  operation material/multiplicity, native query/condition/catalog/comparator
  refs, previous retained count and derived cumulative count, unissued/waiting/
  stopped reasons and state; committed before execution and not replaceable
  after observing results.
- Execution: issued-plan ref and exact input identities, actual unchanged
  native invocation/result/receipt set and typed states, no-drop/multiplicity
  reconciliation, canonical handoff refs/content and evaluator/replay context,
  completion/error/partial status; created only by the campaign's checked
  native path.
- Parent lineage: campaign/root/policy/source binding, producing issuance AND
  execution AND operation/receipt identity, actual producer generation,
  immediate prior parent-lineage ref, full ordered typed ancestor conditions/
  predicate refs, canonical child predicate/handoff binding or explicit
  exploratory construction, activation reason/state. Produced from retained
  execution and prior lineage, never caller fields.
- Activation/queue: exact execution and policy refs, derived next generation,
  chosen parent-lineage refs, separate exploratory/supported reasons and
  waiting/held/unsupported/stopped/budget partitions. Unrun work is never
  silently empty/inapplicable.
- A native handoff ref may repeat across campaign occurrences; it does not by
  itself determine generation. Lineage is indexed by producing execution/
  operation and prior lineage as well as handoff. A full content-derived parent
  ref binds full ancestry/generation and must be looked up in the independently
  retained record set; adding caller fields to a hash is insufficient.

C. Public operations and required validation:
1. Create: trusted frozen context; validate root/source/release/authority
   compatibility; register canonical root; arbitrary root descriptors are not
   interchangeable; host native callables/registry/catalog configured here;
   subjects cannot select callbacks or submit producer results as evidence.
2. Issue: finite batch from stored parent-lineage refs and governed proposed
   input refs; derive producer-generation continuity from retained records;
   mixed/stale/skipped/mismatched labels refuse; predecessor issued set/count
   derived from owner history, not `previous_plan`/`total_issued_before`
   caller fields; grammar/expected set/parent provenance/counts committed
   atomically before execution; bounds before large materialization; invalid
   proposal leaves no accepted record. Issue sequence and discovery generation
   are separate, and multiple explicit batches at one generation are permitted
   and all counted.
3. Execute: resolve retained issuance and parent lineage again, including full
   ancestry/root/policy/source and handoff/receipt/predicate/replay equality;
   validate native authority/membership; invoke pinned native path on canonical
   inputs; commit receipts/handoffs only after exact reconciliation. A public
   plan/parent view must equal retained material in every identity-bearing
   field; altered/rehashed views refuse even if internally self-consistent.
   Direct execution cannot bypass the owner by trusting an earlier planning
   check.
4. Activate: from retained execution ref, actual operation receipts and frozen
   policy; derive next generation/ancestry from actual producing records; a
   caller-supplied next generation is checked, never authority. Supported
   children use validated receipt/handoff; exploratory children use
   source/risk-admissible native construction tied to actual origin operation/
   prior lineage, explicit exploratory kind/reason, no invented winner receipt
   or evidence grade.
5. Inspect: immutable or detached views; caller mutation must not mutate
   retained authority; re-read/copy cannot register history; raw native handoff
   resolver alone cannot admit a campaign parent.
6. Snapshot/restore: preserve records/authority boundary; legacy A4 helpers
   without configured owner must typed-refuse or remain explicitly unqualified
   and cannot feed the accepted path; no accepting compatibility fallback;
   ordinary A1-A3 lowering preserved.

D. Counting, no-work and cold restore:
- Counts derive from exact issued operation identities/multiplicity at the
  frozen profile grain. Both comparator jobs count. Missing/failed/unexecuted
  jobs do not disappear or refund history.
- Total or per-generation cap zero returns explicit stopped-budget/no-work with
  honest unissued reasons, unchanged count, and no native call. It is never
  successful empty discovery.
- Snapshot includes versioned canonical campaign context, full issuance/
  execution/lineage/activation prefix, exact native handoff material or pinned
  bundle refs, and a checkpoint identity. Restore checks full referential
  closure, hashes, exact counts/operation sets, native handoff/source/root/
  policy consistency and expected terminal/inflight states.
- The coordinator supplies the expected checkpoint ref/hash separately from
  untrusted snapshot bytes, pinned when the original state was observed.
  Rewriting snapshot records and recomputing every internal hash must fail
  against that unchanged trusted pin. A self-hash or subject-chosen sidecar is
  not admission.
- Cold proof uses a fresh process, the separately pinned checkpoint identity
  and qualified native context, then actually runs N+1. Missing/wrong pin/
  source/root/policy returns a typed limit. A legacy handoff bundle without
  campaign history cannot be relabelled as an arbitrary generation; require a
  competent pinned full-lineage snapshot or typed missing-lineage refusal.
- Pins establish exact restored history only, not global latest-state knowledge,
  anti-rollback/fork protection, protected storage, crash-atomic joined
  execution or service-level durable uniqueness. R04/R09 retain those.
- Failed/unrun issued work cannot be refunded. Retry of one completed issue
  returns the retained result or typed already-completed state; no silent second
  issue/free budget. Run-local transition atomicity/concurrency must be
  implemented or concurrent mutation explicitly typed-refused; no global
  distributed claim.

E. Owners/dependency: only the four R01 paths may change. Reuse unchanged I05,
recursive handoff, canonical predicate persistence and membership replay. Do
not edit native owners or add a competing engine/service/world ontology. If a
specific unavoidable native-owner defect appears, return exact path/API/
amendment rather than editing it. R03 not started; R04/R09 future obligations
unchanged.

F. Finite qualification contract: reviewer freezes independent expected
history/operation identities before candidate inspection using actual native
outputs from the configured original campaign, not a catalog copied from an
adversarial plan. Required tests below.

## Independent oracle and planned falsifiers (reviewer-owned)

### 1. Positive continuity and arithmetic
- Reproduce the prior R5 independent changed-data D=3 fixture semantics:
  16 rows with q1/q2/q3/out; root 8/16 = 50%, q1=0 4/8 = 50% (neutral against
  root), q1=1 4/8 = 50%; inside q1=0 the q2 subgroups are 3/4 and 1/4 (75%/25%
  opposite directions); the neutral parent's aggregate equals root while its
  internal minority/counterpattern is hidden.
- Construct expected operation identities before execution as exact tuples
  (producer lineage ref, comparator, condition keys/values, target/query and
  baseline ref) with multiplicity, for every retained parent and condition;
  both root and parent comparator jobs count. Compare content and multiplicity,
  not count alone. Independently recompute typed states from raw changed rows.
- Require separately correct root-relative and parent-relative baselines/values,
  including one case above parent/below root and the reverse where supported.
- Require a genuine nonwinning exploratory parent to be issued, executed and
  activated through the public owner, with explicit exploratory kind and no
  fabricated winner receipt. Exploration is not a finding.
- Preserve changed inventory/labels/caps/branching; renaming alone is not
  evidence. Preserve R3 A1 conditioned JOINT/CO_TRAVEL, A2 canonical IDs, A3
  unknown/unsupported/valid-empty/PENDING, J/K/D separation and explicit
  ancestor-conditioning counts. Mechanical versioned fixture/API adaptation
  only; no archived test edit; no import/setup crash counted as product pass.

### 2. R5 H1-H7 successor attacks against the SAME retained owner
- H1 strip/reorder/substitute ancestry; H2 recompute parent hash/generation and
  relabel a real generation-1 handoff as generation 2; H3 swap a valid native
  handoff inside a plan/parent; H4 undercount/drop predecessor jobs; H5 zero
  per-generation/total caps; H6 change root parent/root mismatch; H7 alter
  activation next-generation labels.
- Also: missing/severed/fabricated/stale/cross-source/wrong-release/wrong-
  edition/wrong-authority/wrong-predicate/wrong-receipt/wrong-replay bindings;
  duplicate/mixed/skipped parents; plan altered after creation; caller
  copy/replace/recompute; restored genuine views.
- Every wrong claim must typed-refuse at issue AND at execution/activation as
  applicable before invoking the wrong native plan. A native call counter or
  equivalent witness must show refusal occurs before the bad invocation. A
  refusal after executing the wrong plan is a failure. Restored genuine views
  must pass afterwards on the same consumer.
- A root-only G=2 call, a G=N+1 call whose parent was not produced at N, and a
  parent handoff copied across different producing issues/campaigns must
  refuse. Native handoff ref repetition must not establish generation.

### 3. Owner-boundary and forged-record attacks
- Deep-mutate returned maps/lists/dataclasses; confirm retained authority is
  unchanged; re-read/copy cannot register history.
- Build self-consistent forged plan/counter/hash/parent/activation/execution
  objects and attempt public registration/import; no authority appears without
  an existing matching canonical owner record or actual checked native
  transition.
- Attempt arbitrary callables/results, subject-chosen record registration,
  fabricated parent-lineage/counts, and a second campaign claiming the first
  campaign's history. These must not certify the original campaign.
- Legacy no-owner R5-style recurrence helpers must typed-refuse or remain
  explicitly unqualified; no fallback into the accepted owner path. Ordinary
  A1-A3 lowering must still execute.

### 4. Issue/execution accounting
- Independently calculate exact issued sets/multiplicity/counts across multiple
  batches and generations where the policy permits; previous count and
  cumulative count must derive from retained issuance/execution records.
- No completed receipt or activated child may exist for missing/failed/unrun
  issued work. Missing/failed jobs stay in history. Budget exhaustion remains
  pending/stopped with no false native success and no refund.
- Zero per-generation and zero total caps return explicit stopped/no-work with
  unchanged count and no native call. Guard before unbounded materialization.
- Retry of one completed issue returns retained result or typed already-
  completed state; no silent second issue or budget refund. Run-local
  concurrency behavior must be atomic or typed-refused at the exact claimed
  scope; no distributed/exactly-once claim.

### 5. Snapshot/restore and cold proof
- Create a campaign, run generation 1 or more, snapshot, and independently pin
  the original checkpoint ref/hash outside the snapshot bytes.
- Fresh process: load snapshot with the separately pinned checkpoint identity
  and qualified native context; restore; actually execute N+1. Verify exact
  lineage, parent membership, receipts, counts, operation sets, hashes and
  anti-join.
- Mutate/rewrite snapshot history and recompute every internal hash while
  keeping the trusted pin fixed: restore must refuse. Missing/wrong pin,
  source, root, policy, release, handoff or campaign identity must typed-limit.
- A self-consistent forged checkpoint supplied as subject data cannot replace
  the original configuration. A legacy handoff bundle lacking campaign history
  cannot be relabelled as an arbitrary generation; it must typed-refuse or
  return the declared missing-lineage limit.
- Snapshot/restore claims must not exceed exact-history restoration; global
  anti-rollback/fork protection/durable uniqueness remain NOT_REACHED.

### 6. Same-consumer fault/restoration and honesty
- On the SAME public consumer: baseline passes; meaningful source/receipt/
  parent/plan/lineage/policy mutation refuses or changes the result as
  required; restoration passes; fresh-process owner-restore actually runs N+1.
- Record exact commands, exits, skips, imports, environment, counts, runtime,
  memory, trust assumptions, all partial/unverified arithmetic/minority/identity
  obligations and every NOT_REACHED boundary.
- Each native refusal must be a typed product refusal, not an import/signature/
  setup/helper crash. No all-refuse pseudo-success and no author-pass-only
  acceptance.

## Verdict rule

`ACCEPT_SCOPED_LOCAL` only if the R61V retained campaign owner (sections A-F)
is genuinely implemented and independently qualified at the exact generic
consumer under the declared trusted-catalog/TEST_ONLY profile, including F1-F6
and the H1-H7 successor attacks, without native-owner edits or scope expansion.
Otherwise `REVISE` with the exact minimal reproducible missing function. R03
remains NOT_STARTED. No original/world/full-machine/science qualification
follows. Reviewer does not repair or adopt.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/` + JUnit/results, `replay/`, `evidence/`,
`proof_witness.json`, `manifest.json` with explicit self-exclusion, `RESUME.md`.
Max 45 minutes/bank 35; stop after decisive bounded review. No candidate edit,
no self-adoption, no R03 wake. R08 is an independent author lane: this R01V
reviewer does not inspect, repair or certify R08/R61Q projection/export work.
