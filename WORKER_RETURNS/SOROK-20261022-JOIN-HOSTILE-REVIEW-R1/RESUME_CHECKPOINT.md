# JOIN-V resume checkpoint

**STATUS:** `PRELIMINARY_REVISE__ROOT_LINEAGE_AND_SOURCE_BINDING_NOT_PROVEN__AWAIT_JOIN_E_EXACT_SHA`
**BRANCH:** `codex/sorok-join-v-20261022`
**CANDIDATE:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**STARTUP:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**AUTHORITY:** independent accession `3de081023406a52ec23e1ae43ade77aea485a3f8`; HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`.
**WRITE SCOPE:** own return only; no candidate/J/E edit.

## Current state

- Candidate author suite: 2/2 PASS.
- Independent positives: 10/10 PASS.
- Independent hostile: 7/7 RED on the frozen candidate.
- Inherited: R31J 8/8, R31E 15/15, R30A 10/10 PASS in separate processes.
- Source manifest: 444/444 vendored files match recorded Git blobs.
- Frozen candidate/test hashes: `FROZEN_ORACLES.json`.
- Evidence: `evidence/test_results.json`, `evidence/positive.xml`, `evidence/hostile.xml`, `evidence/import_audit.json`.

## Findings

1. `open()` trusts `session.json` `product_root`/`branch_id`; a foreign product root, a plain R29P root, or a forked branch opens with `verify=true`. The R29P path accepts help with empty J source and mutates the donor `bp2_join.json` with `r31j_*` keys.
2. `R31JProduct.reopen()` loads `r31j_source` from mutable `bp2_join.json`; tampering operation/quantity/actor is accepted with `verify=true` while the C12 `GM01_SOURCE` episode disagrees.
3. Missing/orphan/moved roots raise raw `FileNotFoundError`, raw `RuntimeError: R31J_PREC9_REFUSED...`, or raw `ValueError: R31J_TIME_COORDINATE_HOLD`, not typed session refusals.
4. The author's two-test oracle checks only `b_performed`, which is true for B's `REFUSE_TOOL` too; it does not establish `SHARE_TOOL`/quantity/feasibility, source-to-episode equality, root/branch identity, or sidecar tamper.
5. The untampered positive path is real: E2/omit, B refusal/share, source-to-episode, repeated reopen without duplicate GM01/checkpoints, cold child reopen, attention invariance, private/B ignorance, contact/no-contact, and normal/E-first import order all pass.
6. Cross-root builds are not canonical: same B/E1/C8 source hashes but different C9 target/consumed hashes and possibly different template variants; in-place reopen preserves the root.

## Next safe move

1. When HQ/human supplies the exact JOIN-E return SHA, set `SOROK_JOIN_CANDIDATE_ROOT` to an immutable checkout/worktree of that cut.
2. Run the frozen `tests/test_join_v_positive.py` and `tests/test_join_v_hostile.py` without editing the frozen test files; verify `FROZEN_ORACLES.json` hashes first.
3. Record the exact JOIN-E SHA, command results, source hashes and final engineering/science/authority courts in an update to `00_RETURN.md`.
4. Final verdict only after the exact JOIN-E cut is tested. Do not poll, spawn another worker, edit the candidate, or self-adopt.

## Commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_results.py
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/freeze.py
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/import_audit.py
```

## Flight / model

One accountable reviewer on this branch; local OpenCode, user-selected harness; no subagents, provider calls, native operations or model swaps. Usage/cost unknown. Final remote head is reported after the ordinary non-force push and `git ls-remote` readback.
