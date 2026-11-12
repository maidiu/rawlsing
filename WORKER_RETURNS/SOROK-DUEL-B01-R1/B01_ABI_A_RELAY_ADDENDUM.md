# B01 ABI — Agent A relay addendum

**Base:** B's `B01_ABI_B_REVISION.md` remains the B01 ABI. This addendum records only the A relay additive changes at `6deb7b71d0f8d761ae7734868c693dcb5dd253d8`.

## 1. Fork provenance at the actual P6 consumer

`read_household` and `parent_choice_input` now return:

```text
provenance = {
  stored_branch: <document branch>,
  current_branch: <session branch>,
  inherited: <bool>,
  scope: "P6_MATERIAL_FACT_ONLY",
  fork_state: "CURRENT_BRANCH" | "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
}
```

`parent_choice_input.source` also carries `stored_branch`, `inherited` and `fork_state`.
The stored document is not rebound; the read reports the current branch. This is
material-only scope, never a full P3 composite identity. The same-branch
`P2Owner.material_fact` shape remains B's shape (no `state_scope`); ancestor
reads keep B's `state_scope=C12_FORK_WITHOUT_S46_INTERVAL_STATE`.

## 2. Shared-prefix verification

`branch_is_ancestor` now calls `_copied_prefix_equal` for every parent edge:

```text
episode      (seq, hash)
world_event  (seq, hash)
checkpoint   (seq, hash)
perception   (seq, event_id, actor_id)
```

It compares the child's actual copied prefix rows to the parent rows with
`clock <= fork_clock`. Mutable `branch.root_counts` is no longer the prefix
authority; emptying it cannot disable the comparison. A copied-row hash
mismatch refuses the ancestor fact even when `root_counts={}`.

## 3. Unchanged boundaries

- Same-branch B01 household/read behavior is unchanged.
- No rebinding, no write on read, no new owner/scheduler/ledger.
- `first_consumer=NONE_VERIFIED` and `parent_decision=NOT_EVALUATED` remain.
- Prior P3 code-pin roots are incompatible with this cut; fresh final-code
  fixture roots are required and tested. P3 migration is not in this lease.
- Ancestor provenance relabel between verified ancestors remains an attack
  surface; no checkpoint-history binding is added here.
