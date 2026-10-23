# R61 R01 R6 retained campaign owner — API and record contract

Status: frozen before R6 code. Implements R61V sections A–F inside the existing
four R01 paths. TEST_ONLY, synthetic, sourcefree. No R03 wake.

## Facade

`RetainedRecurrenceCampaign` is the one accepted recurrence owner.

- `create_campaign(*, policy, root_predicate, source_release_refs, target_label,
  query_object, condition_catalog, repository, authority_registry,
  authority_factory, owner_refs=()) -> RetainedRecurrenceCampaign`
  Trusted coordinator setup. Freezes policy/root/query/releases and the native
  authority factory. Subject input cannot select callbacks or root.
- `campaign.issue(*, parent_lineage_refs, condition_refs, requested_generation=None,
  predecessor_issuance_ref=None) -> str`
  Resolves parents only from retained lineage records; derives producer
  generation; checks bounds before materialization; commits issuance atomically
  before execution. Multiple batches at a generation are allowed and counted.
  `STOPPED_BUDGET` issuance carries exact unissued reasons and no expected work.
- `campaign.execute(issuance_ref) -> str`
  Resolves the retained issuance and lineage again, validates grammar/root/
  policy/source/ancestry/handoff/predecessor chain, invokes the pinned existing
  native I05+handoff path, reconciles exact receipts/handoffs and only then
  commits execution. Retry of a completed issuance returns the retained
  execution ref without a second native call.
- `campaign.activate(execution_ref, *, requested_next_generation=None) -> str`
  Derives next generation from the retained producing execution; requested
  label is an assertion. Commits retained lineage records and activation queue.
- `campaign.inspect() -> dict`
  Deep detached material only; mutation cannot change retained authority.
- `campaign.snapshot() -> dict`
  Canonical full history plus checkpoint identity. Does not self-admit.
- `RetainedRecurrenceCampaign.restore(*, snapshot, expected_checkpoint_ref,
  repository, authority_registry, authority_factory, condition_catalog) -> ...`
  Requires the separately pinned checkpoint ref supplied by the coordinator.
  Validates closure/counts/lineage/handoffs before accepting. Rewritten bytes
  with internally recomputed hashes fail against the unchanged pin.

Legacy `build_recurrence_issue_plan`, `execute_recurrence_generation` and
`activate_next_generation` remain explicit unqualified utility helpers for the
existing R4/R5 tests and native proof adapters. They are not the accepted
campaign path and cannot register campaign history. R03 must consume the
campaign facade.

## Retained records

- `CampaignRootRecord`: campaign ref/schema, policy, root predicate/ref,
  releases, target/query ref, native configuration ref, owner refs.
- `CampaignIssuanceRecord`: issuance ref, monotone issue sequence, actual
  discovery generation, parent lineage refs, predecessor issuance ref,
  predecessor count, exact plan/grammar/expected operations, cumulative count,
  unissued reasons, state.
- `CampaignExecutionRecord`: execution ref, issuance ref, native grammar ref,
  receipt/handoff refs and retained native result, exact no-drop reconciliation.
- `CampaignLineageRecord`: lineage ref, campaign/root/policy/source binding,
  predicate, producer generation, producing issuance/execution/operation,
  immediate prior lineage ref, ordered ancestry conditions/predicate refs,
  receipt/replay/handoff or explicit exploratory construction, activation
  reason/state.
- `CampaignActivationRecord`: activation ref, execution ref, derived next
  generation, active lineage refs, waiting/stopped/ledger partitions.

Identity-bearing maps are deep-detached at create/issue/execute/activate and
inspect. No public method registers a caller plan, parent, execution, receipt,
generation or counter record.

## Trust / lifecycle

Trusted coordinator host: retained Python object state is authority. No claim to
resist private-state reflection, monkeypatching, same-UID host access, ptrace or
global service compromise; no signing service/protected issuer/R09 capture.
Run-local `RLock` serializes mutations; retry/completed-issue behavior is
idempotent; no distributed anti-fork claim. R04/R09 durable custody and
fork prevention remain NOT_REACHED.

Generation convention is inherited: producer generation, root=0. Issue sequence
is separate from generation. Counts derive from retained issuance records and
exact operation multiplicity, not caller integers. Root/parent comparators both
count. No new numeric or scientific defaults.
