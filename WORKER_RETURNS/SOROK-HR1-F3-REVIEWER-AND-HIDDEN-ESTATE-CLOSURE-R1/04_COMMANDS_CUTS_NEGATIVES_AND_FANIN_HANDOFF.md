# Commands, cuts, negatives and PRE-MAIN handoff

## 1. Host, permissions and custody

- Host: macOS local, `/Users/matthewsmith/Desktop/Rawlsing` object store; isolated return worktree at `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hr1-f3-estate`.
- Editor/model: OpenCode / DeepSeek V4.1-Flash. No model/harness switch.
- Writes: only this `WORKER_RETURNS/SOROK-HR1-F3-REVIEWER-AND-HIDDEN-ESTATE-CLOSURE-R1/` directory on branch `agent/sorok-hr1-three-reviews-hidden-estate-source-close-20261029-r1`.
- Read-only refs: RC1 `337896aa…`, HR1 `40df1e61…`, PRE-MAIN `299f41e9…`, startup `3fd8dcb3…`, prompt head `1cc63e34…`.
- No PRE-MAIN, PR #514/#516, RC1/HR1, author or reviewer branch was modified. No merge, rebase, reset or force-push. No original survey/respondent/secret source was opened or executed.
- No test was executed by this worker. All test results below are the original reviewers’ retained evidence, cited by exact path/blob. This is a source comparison, not a re-execution.

## 2. Git commands used (representative)

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing ls-remote origin
git -C /Users/matthewsmith/Desktop/Rawlsing fetch origin <exact-branch-ref>
git -C /Users/matthewsmith/Desktop/Rawlsing cat-file -t <sha>
git -C /Users/matthewsmith/Desktop/Rawlsing show -s --format='%H %T %P %ci %s' <sha>
git -C /Users/matthewsmith/Desktop/Rawlsing show <sha>:<path>
git -C /Users/matthewsmith/Desktop/Rawlsing ls-tree -r --long <sha>
git -C /Users/matthewsmith/Desktop/Rawlsing diff-tree --no-commit-id --name-status -r <sha>^ <sha>
git -C /Users/matthewsmith/Desktop/Rawlsing diff <sha>^ <sha> -- <path>
git -C /Users/matthewsmith/Desktop/Rawlsing grep -n -F <symbol> <sha> -- '*.py'
git -C /Users/matthewsmith/Desktop/Rawlsing merge-base --is-ancestor <sha> 299f41e97a43c67be9cc76a79fa49b48f4e12e54
git -C /Users/matthewsmith/Desktop/Rawlsing rev-parse <sha>:<path>
git -C /Users/matthewsmith/Desktop/Rawlsing worktree add -b <return-branch> <return-worktree> 1cc63e34ea2ebdf9391198b439c06c3e80e3668a
```

No branch-code execution, no `git checkout` of an original author/reviewer branch, no `git reset`, no `git update-ref`, no push until the return commit.

## 3. Exact cuts and source hashes

### G17I

- Reviewer: `156b84cc8481b65c4196b42574010eb7920d6f44`.
- Reviewer doc: `WORKER_RETURNS/SOROK-20261019-G17I-MATERIAL-HISTORY-INDEPENDENT-R1/00_RETURN.md`, blob `01f2db8920b441ba1456fc269537072e0b5a19d7`, SHA-256 `b208dc74c0f108b487998f01340d1128cbed86e86f61402cea79270a7a7a3471`.
- Author: `90d0eb7925de54635559a879ee76fc1b97b9ff61` (`agent/rabochii-sorok-20261019-g17-material-history-and-independent-lives-r1`).
- Source: `candidate/lab_sgi1/continuation.py` `c9318dcf33d041a673cfae15aff8fc51712f53e7`; `c9_handoff_consumer.py` `47e59c12b79c04b05c18e73ad76078a29d0d7b3c`; `candidate/lab_sgi1/pipeline.py` `fc954993ef966d20d1915546e04a122daa93538f`. Reviewer `target_candidate/` copies match the first two blobs.
- Reviewer test: `tests/test_g17i_independent.py` `83f17006b22271f17c87f4563608de08395d7a1c`.
- Evidence: `evidence/g17i_independent.xml` `0dec3fafc23d9c19d1575ae960472ffdb5f82060`.
- Actual recorded result: 14 cases, 11 PASS / 3 RED / 0 ERROR / 0 SKIP. Literal REDs: forged material cash (100058), nested future-child `COMMITTED`, C9 forged material `ACCEPTED` (100055).
- NOT_RUN by this worker: all 14.

### OC5E

- Reviewer: `67a4f1561cdad40192f00797d66b24fc4cd91589`.
- Reviewer doc: `WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/00_RETURN.md`, blob `9897d7bbbfaf8f6b0e05ab9d93c3eb9eff3b01ed`, SHA-256 `552fca27553af2121c11c43aa7c1f0abd65343d61fd225a2c31920a30c9c5b2a`.
- Author: `0caaec590f6a8bf6744f22dc9c948c5fe233bc94` (`agent/rabochii-sorok-r3-hq310-oc4-custody-ten-red-repair-r1`).
- Source: `repro/custody_protocol.py` `af2b7e943018077cb36808b5af1cd67704624bec`; author test `repro/test_oc4_repair_controls.py` `c139a877aa4586ec5ab729d333c40037840721d4`.
- Reviewer test: `tests/test_oc5e_native_hostiles.py` `9837579ebb5b2fbf3a41c967e584a166786e46b9`.
- Evidence: `observations/oc5e_native_hostiles.xml` `33efbc315cc424c377441b0f1f79ee31a5a185bc`.
- Actual recorded result: hostile court 159 cases, 110 PASS / 49 RED / 0 ERROR / 0 SKIP; full 349 cases, 283 PASS / 66 RED. The original ten historical REDs are preserved; all seven OC5 predictions are confirmed natively.
- Reviewer invocation pattern: the retained runner executes `python -m pytest -q <files> --tb=line` in the staged `source/` directory with the pinned module; exact per-file command and environment are in `repro/run_court.py` and the observations logs. NOT_RUN by this worker.

### M04

- Reviewer: `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`.
- Reviewer doc: `WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/00_RETURN.md`, blob `5840b2f3f551903d61ce00654b8b964c0ea3a545`, SHA-256 `da0386ebb565477f3ff304f732e866eeddb3466794930250d068d176e6b900b2`.
- Author: `e1f7a74e51201b9614bcc578348b4e9db7be7bd3` (`agent/rabochii-sorok-r3-hq313-m03-claim-selector-provenance-repair-r1`).
- Source: `candidate/cell.py` `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58`; `candidate/claim_provenance.py` `2434bda6f4b00e6ea5881291f5422227e8045e74`. Reviewer copies are byte-identical.
- Reviewer test: `review/test_falsifiers.py` `8add06c66b347e324443c1263771755f6898c7e2`.
- Evidence: `evidence/fresh/junit.xml` `2f54f3e3bc1a750fe87d9e697e324ffe019ae59e`; `evidence/fresh/command.json` `8f199a6fc2e6d3ed0b74104e7bd2fafd9d62b8a5`.
- Actual recorded result: fresh 51 cases, 41 PASS / 10 FAIL; unchanged published 587/587 PASS; separate historical CAN3 9 FAIL.
- Exact recorded command (from `command.json`): `/usr/local/bin/python3 -m pytest [RETURN]/review/test_falsifiers.py -vv --tb=short --import-mode=importlib -p no:cacheprovider --rootdir=[RETURN] --confcutdir=[RETURN] --basetemp=[RETURN]/runtime/tmp/m04 --junitxml=[RETURN]/evidence/fresh/junit.xml`. NOT_RUN by this worker.

## 4. Negatives preserved

- G17I: the author’s narrow 13-case material court passes, but it does not cover the three alternate-interface failures. M2/MP and C9 E1/RULE_A/T/E2 are not promoted.
- OC5E: the ten historical REDs are not implementation defects and are not erased; the 49 new REDs are not negated by the 110 controls. C07 is not reached.
- M04: the 587-case published denominator is not replaced by the fresh 51; the nine historical CAN3 FAILs remain separate. The three ledger/selector repairs are not a general provenance proof.
- Outside estate: a no-tip-hit branch is not ancestry-clear; 359 of 377 were not deep-read; 2,366 unselected rows remain. A branch-local test is not a first product consumer.
- WSC002D and GT12-D branch blobs differ from current PRE-MAIN blobs; no equivalence is assumed.
- C12/R95/HQ284/HQ292/W11 are candidate-only and have no PRE-MAIN first consumer.

## 5. PRE-MAIN fan-in handoff

1. Incumbent Sorok/PRE-MAIN HQ intakes this return as a source-grade reconciliation, not an adoption.
2. Route G17I, OC5E and M04 to their original component owners for repair. Preserve the three literal G17I REDs, the 49 OC5E REDs, the 10 M04 fresh REDs and the nine historical M04 REDs.
3. Route C12/BP4, R95/P41/R05/R06, HQ284/PRE-V3, W11/Field Forge and WSC drift to their owners before any code adoption.
4. Commission a separate source-qualified reviewer after this immutable return. The reviewer must not be this worker.
5. Update owner progress MD/JSON via the existing CAS-authorized path only where an owner has accepted a finding. Do not log this return as adopted, scientifically accepted or native.

## 6. Final remote SHA

The ordinary push creates the immutable return commit. Its 40-hex SHA is reported in the final response after direct `ls-remote` verification; a commit cannot contain its own final SHA. No self-acceptance, no force-push, no PRE-MAIN mutation.
