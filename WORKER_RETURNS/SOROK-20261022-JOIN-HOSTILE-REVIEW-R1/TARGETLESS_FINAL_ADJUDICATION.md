# JOIN-V adjudication — targetless repair 75a134e

**STATUS:** `TARGETLESS_FINAL_REVISE__75a134e__BRANCH_LINEAGE_RECEIPT_AND_PARENT_SWITCH_NOT_BOUND__AWAIT_NEXT_REPAIR_SHA`
**REVIEWED SHA:** `75a134ed733acaed2c62ea3421b54fcb09c5442f`
**PREVIOUS:** `cc0ff7d0305340b806ba94b020017c3d8d0585dc` (REVISE)
**BRANCH:** `codex/sorok-join-v-20261022`
**WRITE SCOPE:** own return only. No candidate/J/E edit.

## Verdict

The three requested repairs are **partially successful**:

1. Coordinated `session.json` + `refusal.json` source tampering against C12 `GM01_REFUSAL`/C8 is now rejected with `J_PROVENANCE_MISMATCH`. **PASS.**
2. Root metadata-only branch substitution is rejected, but a forked session can be switched back to its parent `first_session` by metadata alone and opens successfully. **PARTIAL/FAIL.**
3. `fork_alt` genuinely switches to `alt`, cold-reopens `alt`, and the parent branch remains uncorrupted, but the recorded fork receipt has `fork_clock=null` and `root_hash=null`. **PARTIAL/FAIL.**

The joined path and all 26 preserved reviewer tests (10 positive + 7 hostile + 9 repaired) pass. The authored 16-test suite and inherited J/E/R30A suites pass; the source manifest is 444/444; frozen hashes are unchanged. The new targeted tests expose three exact counterexamples.

**Final-cut engineering verdict: REVISE.** One coherent lineage repair remains: complete the fork receipt from the actual created branch, and reject any metadata branch selection, including the parent `first_session`, when recorded lineage points elsewhere. Apply the same guard to both targetless and joined paths.

## Independent count

| Suite | Result |
|---|---|
| Preserved reviewer positives | **10/10 passed** |
| Preserved reviewer hostiles | **7/7 passed** |
| Existing repaired-cut tests | **9/9 passed** |
| **Author-reported 26/26 reviewer executions** | **independently reproduced: 26/26 passed** |
| Targeted c367 tests | 5/6; E-first-refusal expectation superseded by legitimate J closure |
| New targetless-final tests | **1/4 passed; 3 failed** |
| JOIN-E own suite | **16/16 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified** |

Frozen test hashes all match `FROZEN_ORACLES.json`; no frozen test was edited.

## Exact failing reproducers

### F1. Incomplete fork receipt

After `RefusalSession.fork_alt("alt")`, the created branch row has `fork_clock=10` and a real `root_hash`, but the session lineage receipt records `null` for both:

```json
{"parent_branch": "first_session", "new_branch": "alt",
 "fork_clock": null, "root_hash": null}
```

The code reads `fork.get("fork_clock")`/`fork.get("root_hash")` from the outer fork result; the actual values are under `fork["branch"]`. The same construction exists in `JoinedSession.fork_alt`. This means lineage is not a receipt of the actual fork clock/root.

New test: `test_refusal_fork_receipt_and_parent_integrity`.

### F2. Parent metadata switch accepted

Start a targetless session, call lawful `fork_alt("alt")`, close, then edit only `session.json`:

```json
{"branch_id": "first_session"}
```

leaving `branch_lineage.current_branch = "alt"`. `RefusalSession.open()` accepts the session with branch `first_session`, `verify=true`, and the contradictory lineage still present. The same attack opens a joined session:

```json
{"case": "refusal_parent_metadata_switch", "opened": true,
 "branch_id": "first_session", "verify": true,
 "branch_lineage": {"current_branch": "alt", ...}}
```

Both `_guard_branch`/parent checks only validate non-parent branches and never reject `branch == first_session` when recorded lineage points to another branch.

New tests: `test_refusal_parent_metadata_switch_refused`, `test_joined_parent_metadata_switch_refused`.

### F3. Parent not corrupted (positive)

The separate positive `test_refusal_fork_parent_not_corrupted_positive` passes: a lawful fork leaves the parent branch episodes/counts unchanged, alt speech does not mutate the parent, and cold reopen of alt leaves the parent unchanged. The fork itself is real; only receipt/guard completeness fails.

## Claim coverage

| Claim | Status |
|---|---|
| Coordinated targetless meta/sidecar source tamper vs C12/C8 | **PASS** (`J_PROVENANCE_MISMATCH`) |
| Root metadata branch substitution | **PASS** (rejected) |
| Parent metadata branch substitution | **FAIL** (accepted for targetless and joined) |
| Targetless `fork_alt` switches branch | **PASS** |
| Targetless `fork_alt` cold-reopens alt | **PASS** |
| Targetless fork parent not corrupted | **PASS** |
| Fork receipt has actual fork clock/root | **FAIL** (`null`/`null`) |
| Nonmutating targetless cold reopen | **PASS** |
| No fabricated target/native grant | **PASS** (`target_id=""`, targetless, native grants false; inherited `c9.grant_id` remains a documented C9 field) |
| Actual B refusal source to E consumer | **PASS_SCOPED_RECEIVING_EDGE**; zero tools, no inspection, `GM01_REFUSAL`, `HELP_REFUSE`; no refusal=>help-accept |
| Bounded receiving-edge fault/restore | **PASS_SCOPED**; not original upstream pre-C8 severance |
| Joined encounter/fork/attention/privacy/contact/cold | **PASS** |
| E-first J closure adaptation | **PASS**; old c367 refusal expectation is historical |
| Native/science | **HOLD** |

## Source and test hashes

- Candidate: `75a134ed733acaed2c62ea3421b54fcb09c5442f`.
- `joined/refusal.py`: `17e33bc0e5e37de92b8b9b56e190d7ee97235ff7c188c7923bd2b3868a5a5273`.
- `joined/session.py`: `d7dbabf4f7be3516540f8c1035d4136f2efe61f1f0150b53565fb73aa3c9872f`.
- `joined/imports.py`: `2b49f6ebbbff2d5ca008d350306da229a4798f0f7c075312519d4209c6957cfd`.
- `joined/provenance.py`: `3618beca7997c5674ce6b7490ab600a891fbadbc38e49e4644928d6712c65c1b`.
- `tests/test_join.py`: `26d7c69494037994c3ae5118a8cc91a251707b2ed4b93d9b5e5c0f596977f4bf`.
- `tests/test_join.py.proof.json`: `332f1c23d14e0511b181bf9529f9f630ba7e17b87fcae281478a69be170fe282`.
- New targetless-final test: `tests/test_join_v_targetless_final.py` hash `f5411af4191188f0391dda2019225ab2856c798b2b5d101f2f66f4308473da66`.
- Repaired-cut test hash (unchanged): `8a7ce8e61253ce6adb9286a4fb44f8ff26a7c851a28738fbacbe06df309f1028`.
- Targeted c367 hash (unchanged): `6e2f87d773090235a4a5f3567430737f30f16698397c852f799585ff73280de1`.
- Frozen test hashes: unchanged/verified; `SOURCE_MANIFEST.json` `444/444`; no vendor edits.

## Exact commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<75a134e worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py tests/test_join_v_hostile.py tests/test_join_v_repaired_cut.py -p no:cacheprovider
26 passed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
5 passed, 1 failed (historical E-first-refusal expectation; J closure adaptation)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_targetless_final.py -p no:cacheprovider --tb=short
1 passed, 3 failed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_targetless_final.py
candidate own 16/16; inherited 8/8, 15/15, 10/10; manifest 444/444
```

Evidence: `evidence/targetless_final/results.json`, `evidence/targetless_final/source.json`, and `evidence/targetless_final/*.xml`.

## Courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE` | Coordinated source tamper and nonmutating/no-target behavior pass; parent metadata branch substitution remains accepted in both paths and the fork receipt clock/root are null. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | B-source remains bounded receiving-edge; no original pre-C8 severance, acquired practice, psychology, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native CAN/ADP/C8/C12/Pyat/C11/C5, protected keys, external provider or human A5. |

## Next coherent repair

1. In both `RefusalSession.fork_alt` and `JoinedSession.fork_alt`, read `fork_clock`/`root_hash` from `fork["branch"]` (or the created branch row) and record the actual values.
2. In `RefusalSession.open` and the joined branch guard, reject any `branch_lineage` whose `current_branch` differs from `meta["branch_id"]`, including a switch back to `first_session`; require the created branch parent/receipt to match.
3. Preserve the passing parent-noncorruption, cold nonmutation, source/C12 provenance, no-target/no-grant and 26/26 positive/hostile/repaired behavior.
4. Re-run frozen tests, targeted c367 tests, repaired-cut tests and targetless-final tests on the next exact SHA; keep the E-first expectation historical.

No polling; same lane.
