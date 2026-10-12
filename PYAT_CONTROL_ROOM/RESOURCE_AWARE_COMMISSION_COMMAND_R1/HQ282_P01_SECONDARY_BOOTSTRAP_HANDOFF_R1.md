# HQ282 P01 — secondary sparse worktree bootstrap handoff

**Status:** `BOOTSTRAP_REQUIRED__NO_LOCAL_P01_WORKTREE__P01_ENGINEER_NOT_LAUNCHABLE`

User confirmed that the P01 worktree does not exist on the secondary Mac. This is an infrastructure condition, not failure of any empirical or integration test. The existing P01 GitHub branch stays unchanged:
- Branch: `agent/rabochii-pyat-hq282-p01-v2-durable-consumer-integration-r1`
- Exact commission/startup: `712b818e6c0fa87412db7f4edaad1397b2e9f090`
- Local planned model AFTER bootstrap: SECONDARY Codex GPT-6.1 Sol **Medium**.
- PRIMARY Codex is protected for full-local-repository Astra; no Codex usage for ordinary Git setup.

## Authorized infrastructure action, not another P01 commission

On **SECONDARY** Mac, an operator or zero-Codex qualified local shell helper may create **one new isolated sparse worktree** for this already-issued P01 branch, using ONLY the existing shared canonical Rawlsing clone/object store ON SECONDARY. First observe actual canonical clone path and already-present worktrees. Do not guess the path from PRIMARY-Mac historical tests. Require explicit new nonexisting worktree target under the authorized secondary worktree root.

Before creating any path: verify secondary existing canonical clone, `origin` points to `maidiu/rawlsing`, exact current remote P01 branch tip matches `712b818e6c0fa87412db7f4edaad1397b2e9f090`, no already registered P01 worktree, no changed/dirty P01 local branch and no write collision. Missing actual canonical clone => `SECONDARY_CANONICAL_STORE_MISSING__SEPARATE_AUTHORIZATION_REQUIRED`; do NOT make a per-worker clone.

When all checks pass, use standard Git `worktree add --no-checkout` from the existing shared repository to attach P01's exact branch, then `sparse-checkout set --cone` to include `rawlsing_next`, P01 commission, and necessary resource-law paths. Local branch may be attached if already present **at the same exact tip and not checked out elsewhere**, otherwise create the local branch at the exact startup commit. Do not switch any existing checked-out worktree, merge/rebase V2/B01E branches, reset, prune, or recreate.

The separately pinned original source-free Git objects are:
- A04TU/V2: `d6e766cd6ba7dc46b19cc61123d968a274015ddd`
- B01E/B01D: `92cb25340c49fb51e2b8d6e00d5a4f471296fc8f`
- A05 independent oracle: `9491d0296c95ee2942fe80eadc6aa9f54b07c634`, path `WORKER_RETURNS/PYAT-HQ280-PV3-A05-INDEPENDENT-NODROP-ORACLE-R1/repro/a05_oracle.py`, expected Git blob `00a4cc84d321c3fbace0f4aa09be62dbb31994fc`. Only fetch exact missing objects. Verify the blob independently; do not copy PRIMARY-Mac local A04/A05 directories or their raw source data.

Original V2 tests have hard-coded PRIMARY A04/A05 worktree paths and can SKIP on SECONDARY. Treat absent external coverage as **HOLD**, not PASS; use a new portable exact-Git-blob court in P01's permitted candidate test terrain.

Bootstrap receipt must report actual secondary canonical clone/worktree paths, `git branch --show-current`, `git rev-parse HEAD`, `git status --short`, shared `git-common-dir`, sparse list, exact source object availability and local Python/pytest version (or typed environment HOLD). A newly constructed Python environment must not be called governed without its separate provenance. The setup is complete only after local receipt, not by publishing this note.

Do not spend Codex quota, Full reset credits, paid overflow, or launch Astra on worktree setup. P01 can be started afterwards on SECONDARY GPT-6.1 Sol **Medium**, with actual privacy/model/quota and reviewer preflight.

**Authority:** `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`, HQ281/282 RCM01 resource law, sealed P01 commission. No source-read, scientific adoption, actual REAL_EXECUTION grant, or immutable HQ_HANDOFF checkpoint modification.

**Terminal:** `HQ282_P01_SECONDARY_BOOTSTRAP_DOCUMENTED__LOCAL_RECEIPT_REQUIRED__NO_DUPLICATE_CLONE_OR_CODEX_BURN`
