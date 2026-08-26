# Live reconciliation protocol

The packaged baseline is commit `5b500e160f964f4d47895080ee5673e91713223a`. Do not reset, overwrite, or force the user's current repository to that commit.

## 1. Inspect before applying

```bash
git status --short --branch
git rev-parse HEAD
git log --oneline --decorate --graph --all --date-order -50
git merge-base --is-ancestor 5b500e160f964f4d47895080ee5673e91713223a HEAD
```

Record the current authority release pointer and export the live P3C tables before mutation. Verify whether any post-R184 GSS work already exists.

## 2. Reconcile by deterministic identity

Use `component_id`, lineage IDs, pair keys, and deterministic adjudication IDs from this checkpoint. Do not allocate by row order. For each of the 148 resolved successor candidate adjudications:

- detect an already-applied equivalent decision;
- detect conflicts with newer family membership or stronger boundaries;
- allocate numeric family/revision/adjudication IDs only for genuinely new objects;
- preserve response variants and exclusions;
- reject any operation that would merge two distinct current canonical families.

## 3. Promote immutably

Create a new release whose parent is the actual current live release, not an assumed R185/R186/R187 chain. R184 must remain unchanged. Run all SQL closure, no-loss, mutation, provenance, deterministic-rebuild, and release-pointer gates.

## 4. Required post-apply proofs

- every one of the 148 successor adjudications has one live resolution or an explicit newer-state supersession;
- no open pair or lineage obligation remains;
- no component crosses two current canonical families;
- all 339 proposed new memberships are either installed or explicitly superseded/rejected by newer authority;
- the 13 R184 authority files remain hash-identical to `R184_IMMUTABILITY_MANIFEST.csv`;
- current Git work and commits newer than `5b500e1` remain preserved.
