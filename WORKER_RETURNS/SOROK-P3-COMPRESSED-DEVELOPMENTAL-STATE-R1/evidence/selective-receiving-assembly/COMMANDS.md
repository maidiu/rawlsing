# Assembly commands — isolated candidate, no PR

All construction/verification was mechanical. No tests were rerun.

## Base and source verification

```bash
git ls-remote --heads origin \
  refs/heads/integration/pre-main-reconciliation-r1 \
  refs/heads/agent/sorok-p3-compressed-developmental-state-20261106-r1 \
  refs/heads/agent/sorok-p3-goal-audit-20261107-r1 \
  refs/heads/agent/sorok-p3-goal-residual-proof-20261107-r1
```

Observed protected base `c852d751…`; runtime `16275d03…`; audit `140b585f…`; residual `036787c1…`.

At the final remote check, `agent/sorok-p3-compressed-developmental-state-20261106-r1` had advanced to `fd51a5d871f00233cf5b32bc2e6082757526495b`, a descendant of `9abb3eee`/`16275d03`. Runtime/test hashes at that observed head are identical to `16275d03`; the candidate therefore uses the frozen `16275d03` bytes and records the source-ref movement as a HQ reconciliation dependency.

## Isolated branch construction

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-p3-receiving-prep-r1
git switch -c codex/sorok-p3-selective-receiving-20261107-r1 \
  c852d7516e23fcb6cf2215e9be7c5fa268503516

# The exact path lists were taken from the prepared package at 2a6573be.
git show 2a6573beedab020974bff2d789243b99aeb9f8ee:\
WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep/SELECTIVE_PATHS_16275.txt \
  > /tmp/p3_paths_16275.txt
git show 2a6573beedab020974bff2d789243b99aeb9f8ee:\
WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep/SELECTIVE_PATHS_140b.txt \
  > /tmp/p3_paths_140b.txt
git show 2a6573beedab020974bff2d789243b99aeb9f8ee:\
WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-prep/SELECTIVE_PATHS_0367.txt \
  > /tmp/p3_paths_0367.txt

# E1 B1 is outside the original sparse cone; add it before checkout.
git sparse-checkout add WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1

xargs git checkout 16275d03fc4724a694c48ed9d447c4eeadbe25f2 -- < /tmp/p3_paths_16275.txt
xargs git checkout 140b585f9b7321984725cf6f38ae95c2cb2bf89c -- < /tmp/p3_paths_140b.txt
xargs git checkout 036787c1f0c227cdc47828ba521a62b76c57a903 -- < /tmp/p3_paths_0367.txt

git checkout e85b6f6a733ef5bbd664679bdf9613c04003e3de -- \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/final-independent-review/focused-recheck-16275d03
git checkout 9abb3eee3d59c76ce20d5131d5b60151f7ca98ae -- \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/FOCUSED_RECHECK_DISPOSITION.json
```

## Exact-delta and blob verification

```bash
git diff --name-only c852d7516e23fcb6cf2215e9be7c5fa268503516 | sort \
  > /tmp/assembly_delta.txt
wc -l /tmp/assembly_delta.txt
grep -E 'SOROK_PRODUCT_CONTROL_ROOM|PROGRAMMA|\.DS_Store|__pycache__|\.pyc$' \
  /tmp/assembly_delta.txt || true

# Compare against the assembly allowlist.
diff -u \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/selective-receiving-assembly/PATH_ALLOWLIST.txt \
  /tmp/assembly_delta.txt
```

Observed: 186 paths; no coordination/PROGRAMMA/pyc/DS path.

Per-path source/blob integrity and runtime/test exactness are recorded in
`BLOB_CHECKS.json`. The focused-review manifest is separately verified for 14
listed files.

## No test repeats

No matrix, primary, cold, crash, resource, store, owner or residual test was
rerun during assembly. Published focused-review and author evidence are cited
unchanged.
