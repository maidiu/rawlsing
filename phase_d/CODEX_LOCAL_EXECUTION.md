# Codex local execution — Phase D M6

This GitHub change is an **additive sidecar** for the existing V550→V552J local architecture. Do not replace or rewrite the local runtime with the transfer repository.

## Install into the real local Rawlsing checkout

The GitHub transfer repository has curated source but not the full local history. On the real local checkout, fetch this PR branch and cherry-pick **only the Phase-D commits after the transfer base**. Do not merge the transfer repository history.

```bash
cd /path/to/real/local/rawlsing
# add the transfer remote once if needed
git remote add phase-d-transfer git@github.com:maidiu/rawlsing.git || true
git fetch phase-d-transfer agent/phase-d-m6-positioned-evidence
git cherry-pick $(git rev-list --reverse a819fb35337ea28c4a83352d0040030b3da83a7a..phase-d-transfer/agent/phase-d-m6-positioned-evidence)
```

Preflight must pass before any empirical run:

```bash
git cat-file -e acbba91de28b9cee20af05e81e4d8bfdaa876298^{commit}
git merge-base --is-ancestor acbba91de28b9cee20af05e81e4d8bfdaa876298 HEAD
```

The checked-in V550J implementation already exposes `--v550j-substrate-mode prepared_required` and `--forbid-database-access`. Preserve those semantics. Association mode for this canary is **DIAGNOSTIC**, never production-active.

## Execute

1. Run the existing bounded nine-family / 20-variable smoke using the current local runner and local database. The required data path is:

   `one V550 governed union extraction → shared respondent substrate → V550 base + V550J prepared_required with database reopening forbidden → V551 + V551J`

2. Point the Phase-D aggregator at the completed smoke output root:

```bash
python3 phase_d/code/run_m6_nine_family_canary.py \
  --repo-root "$PWD" \
  --smoke-root /absolute/path/to/completed/nine_family_smoke \
  --output-dir /absolute/path/to/phase_d_m6_return
```

3. The aggregator materializes the frozen Job3 topology into the return automatically. Validate:

```bash
python3 phase_d/validation/validate_phase_d_canary_return.py /absolute/path/to/phase_d_m6_return
```

If the validator reports missing archetype coverage, preserve the block; do not synthesize or infer an empirical relation. No respondent-level Parquet, IDs, database URL, or secrets belong in the return or on GitHub.

## What this changes

- Adds frozen Job3-R3 semantic topology/blockers as **read-only sidecar authority**.
- Adds E04 association policy and positioned-evidence schema.
- Adds a fail-closed compiler that only attaches empirical evidence to a semantic relation when exact implementation IDs co-occur in one empirical artifact row.
- Preserves empirical-only co-travel when semantic authority is absent or blocked.
- Adds the nine-family M6 return aggregator and validator.

It does **not** alter V550, V550J, V551, V551J, V552, V552J, registries, or respondent data.
