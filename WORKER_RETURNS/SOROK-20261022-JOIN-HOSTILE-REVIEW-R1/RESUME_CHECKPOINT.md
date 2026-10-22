# JOIN-V resume checkpoint — repaired cut cc0ff7d

**STATUS:** `REPAIRED_CUT_REVISE__cc0ff7d__TARGETLESS_REFUSAL_PERSISTENCE_LINEAGE_AND_FORK_NOT_BOUND__AWAIT_NEXT_REPAIR_SHA`
**BRANCH:** `codex/sorok-join-v-20261022`
**REPAIRED CUT:** `cc0ff7d0305340b806ba94b020017c3d8d0585dc` (read-only detached worktree)
**PRIOR CUTS:** c367777 (targetless A/B; superseded), 13dfd6bad (preliminary)
**CONTINUATION:** `0445059a81d0882bc6d1488150697d00f044bd39:.../continuations/04_JOIN_V_REPAIRED_EXACT_CUT.md`
**WRITE SCOPE:** own return only; no candidate/J/E edit.

## Results against cc0ff7d

| Suite | Result |
|---|---|
| Frozen independent positives | 10/10 passed |
| Frozen independent hostiles | 7/7 passed |
| Targeted c367 tests | 5/6; one superseded E-first-refusal expectation |
| New repaired-cut tests | 6/9; 3 failed |
| JOIN-E own suite | 15/15 passed |
| Inherited J / E / R30A | 8/8, 15/15, 10/10 passed |
| Source manifest | 444/444 verified |

Frozen test hashes were checked first and match `FROZEN_ORACLES.json`; no frozen test was edited. `REPAIRED_CUT_ADJUDICATION.md` has full detail; `evidence/repaired_cut/` has JUnit/JSON.

## Repaired / preserved

- All prior joined-path root/source/C12/branch/typed-root findings pass.
- Joined positive encounter, lawful fork, attention, privacy, contact, B ignorance and cold reopen pass.
- E-first import now adapts to the J-first closure; the old targeted test expecting an E-first refusal is historical/superseded, not a candidate defect.
- Actual B refusal source gives zero tools, no performed inspection, `GM01_REFUSAL`, `target_id=""`, and E `HELP_REFUSE`; share source gives `HELP_ACCEPT`; no refusal=>help-accept claim.
- Bounded receiving-edge fault/restore: force tool 1 under `REFUSE_TOOL` flips E to `HELP_ACCEPT`; fresh refusal restores `HELP_REFUSE`. This is not end-to-end B pre-C8 severance.

## Still failing / new counterexamples

1. Coordinated `session.json` + `refusal.json` source tampering opens with `verify=true` while C12 `GM01_REFUSAL` retains the original source.
2. Metadata-only branch `branch_id="root"` opens with `verify=true`.
3. `RefusalSession.fork_alt()` returns OK but leaves `branch_id=first_session`, no lineage; cold reopen ignores `alt`.
4. `c9.grant_id=TEST_ONLY_BP2_TARGET_GRANT` remains in the targetless receipt; it is inherited, not a newly fabricated native grant, but should be documented by the owner contract.

## Next safe move

Await the next repair SHA; run the unchanged frozen tests, targeted c367 and repaired-cut tests, then `tools/collect_repaired_cut.py`. The remaining repair should:

1. make `joined/refusal.py` read-only and C12/C8-provenance-bound, with no meta/sidecar-only source acceptance;
2. enforce canonical targetless root and sealed branch/fork lineage; reject metadata-only branch selection;
3. implement a real targetless fork or a typed `FORK_UNSUPPORTED` refusal; never return success on a no-op;
4. preserve no-tool/no-target and no refusal=>help-accept; document the inherited C9 grant field.

## Flight / model

One accountable reviewer on this branch; local OpenCode, user-selected harness; no subagents, provider calls, native operations or model swaps. Remote head is reported after the ordinary non-force push and `git ls-remote` readback.
