# R01 final independent receiving — L01 sourcefree R08/R118/P41 consumer

**Verdict: `ACCEPT_SCOPED_SOURCEFREE`.**

This is one independent, sourcefree local S2 receiving operation. It does not
confer original survey/source-scientific, R09 host, N11/N12, Sorok actor,
protected CAS or production authority. It is not an L01 author, R01 repair
implementer, original scientific issuer, protected CAS merger or own-review
return.

## Exact reviewed identity

- Repository: `maidiu/rawlsing` (private).
- PR: #702.
- Repaired head: `0252e028e65dabb080d9aa485a151d5b77d32ffc`.
- Repaired tree: `245ff7941ab0d485c7ab346c0ef374a7d7924699`.
- Protected base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.
- Pre-repair head: `33af55415ef43f96457a017a24bdceab13fa6068`.
- `refs/pull/702/head` read directly at receipt time:
  `0252e028e65dabb080d9aa485a151d5b77d32ffc`; the head did not move during
  this review. The base commit resolved to
  `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.
- Clean reviewer worktree:
  `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-receive-702`,
  detached at the repaired head. `git status --porcelain` was empty before and
  after the proof gate.
- Repair delta `33af554..0252e02`: exactly three added files, 48 insertions:
  `rawlsing_next/tests/test_l01_evidence_world_consumer.py.proof.json`,
  `rawlsing_next/tests/test_universal_evidence_binding.py.proof.json`,
  `rawlsing_next/tests/test_world_conditioned_progressive_service.py.proof.json`.
  No implementation or test body changed in the repair commit.
- Full candidate delta `8ffec40..0252e02`: 59 files, 11285 insertions,
  76 deletions.
- `WORKER_RETURNS/PROGRAMMA-PYAT-L01-SOURCEFREE-CONSUMER-20261105-R1/SHA256SUMS.json`:
  all 55 committed source/test/receipt entries matched `sha256` exactly. The
  three added proof files are not in that pre-repair manifest, as expected.

## Runner provenance

- Execution: OpenCode local S2, model `opencode-go/deepseek-v4.1-flash`.
- Host: `oldMac.lan`, macOS 13.7.8, x86_64, git 2.39.1.
- Ambient interpreter: Python 3.11.3, pytest 9.1.1.
- Cold replay venv: pytest 9.0.2, pandas 2.3.1, numpy 2.3.2, pyreadstat 1.3.2,
  narwhals 2.28.0 (exact `logs/cold-dependency-lock.txt`).
- R61/decoder replay venv/userbase: pytest 9.2.0, pyarrow 26.0.1, duckdb 2.0.0,
  pyreadstat 1.3.2, pandas 3.0.6. This mirrors the R61 workflow's unpinned
  `pytest pandas pyreadstat pyarrow duckdb` install.
- `python` is not installed on this host; every command used `python3` (the
  same Python 3.11.3 interpreter). This is the only substitution from the
  literal launch command.

## Mandatory returns and access limit

Read directly:

- L01 `00_RETURN.md`, `INDEPENDENT_R01_REVIEW_REQUEST.md`, `RESUME.md`,
  `LEAD_QUALIFICATION.json`, `SHA256SUMS.json`, `R53-current-positive-hostile-matrix.jsonl`,
  `cold_replay.py`, cold receipts/logs and first-consumer trace.
- R53 P53T `00_RETURN_AND_ASTRA_READ_FIRST.md` and
  `02_NATIVE_SOURCEFREE_REPRODUCTION_MATRIX.tsv` from
  `agent/rabochii-pyat-r53-p53t-native-sourcefree-defect-reproduction-r1`.
- R116 `00_REVIEW.md` and R118 `00_REVIEW.md` from their exact reviewer
  branches.
- `CROSS_HQ_CONTROL_ROOM/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md`,
  the gate, and the court workflows at the reviewed head.

The two PR-comment bodies (issuecomment-6675558777 and issuecomment-6676835047)
were **not** independently readable. The available fine-grained credential
returned `403 Resource not accessible by personal access token` for
`/repos/maidiu/rawlsing/pulls/702`, `/issues/702/comments`, and
`/actions/runs/...`; the commit-comments endpoint returned an empty list. This
review therefore uses the launch's quoted mandatory requirements, the in-repo
L01 request/return, the R53/R116/R118 returns above, and independently executed
behavior. The exact CI run logs/comment bodies remain an access residual, not a
sourcefree code/proof defect. The underlying CI commands were reproduced
locally against the exact head and matched the reported outcomes.

## Executed commands and results

All commands ran from the clean reviewer worktree at the exact head unless a
path is shown.

| Command | Result | Evidence |
|---|---|---|
| `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed --base 8ffec40a6924848a49f95950aa9ce28c27ee3ec1 --head 0252e028e65dabb080d9aa485a151d5b77d32ffc --root .` | PASS; 4 witness contracts; every baseline PASS and every target assertion RED | `evidence/proof-gate.log` |
| `python3 -B -m pytest -q ... test_l01_evidence_world_consumer.py test_universal_evidence_binding.py test_l01_reviewed_progressive_world.py test_world_conditioned_progressive_service.py test_universal_world_binding.py` | 170 passed, 1 environment-only failure (`pyreadstat` absent in ambient interpreter); failed node rerun with pyreadstat 1.3.2/narwhals 2.28.0: 1 passed. Behavior total: 171/171 | `evidence/reviewer-sourcefree.log`, `reviewer-sourcefree-junit.xml`, `reviewer-sourcefree-rerun.log`, `reviewer-sourcefree-junit-rerun.xml` |
| `python3 WORKER_RETURNS/PROGRAMMA-PYAT-L01-SOURCEFREE-CONSUMER-20261105-R1/cold_replay.py` from a second disposable worktree at the head | PASS; 167 passed, 4 deselected; one-commit clean checkout, no remotes, historical P41/J42/R118 objects absent, fresh pinned venv, byte-identical trace | `evidence/cold-replay.stdout.json`, `evidence/cold-logs/` |
| `python3 -B -m rawlsing_next.tests.l01_sourcefree_replay` | PASS; `output_hash` `760e934258844704ba0fb27e15f270ef880de1cd0c6fd7a3bfc45d6c004a705b`; equals author `first-consumer-trace.json` exactly | `evidence/reviewer-first-consumer-trace.json` |
| `python3 CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py` | PASS canonical tree | `evidence/canonical-verify.log` |
| R61 workflow test commands (grammar, workload, source projection, byte custody; decoder/metadata) | 105 passed; 37 passed, 1 documented skip | `evidence/r61-*.log`, `r61-*.xml` |
| R61 witnesses for grammar, workload, source projection | PASS 3/3, target assertion RED | `evidence/r61-*-witness.log/json` |
| `python3 -m unittest discover -s CROSS_HQ_CONTROL_ROOM -p test_proof_integrity_gate_r1.py -v` | 9 tests OK | `evidence/proof-gate-selftest.log` |
| Governed court `.rabochii/court_spec.json` | **144 passed / 3 failed**, inherited FIABC blob-anchor conflicts; not made green | `evidence/governed-court.log`, `governed-court-receipt.json` |
| Focused negative matrix (17 nodes) | 17 passed | `evidence/reviewer-negative-matrix.log`, `.xml` |
| Cached wrong-condition probe | distinct K; wrong condition UNKNOWN `NO_EXACT_PRODUCER_BINDING`; no consumer values; reader refused | `evidence/cached-wrong-condition-probe.json` |
| R08 canonical-reorder probe (requested X,O; canonical leaves O,X) | current code SUPPORTED/denominator 4/selected view; old positional `zip` control dies `result is not exact support: UNKNOWN` | `evidence/r08-reorder-probe2.json`, `evidence/r08-old-zip-control.log` |

## Per-witness proof-integrity results

Gate state: `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`,
`witness_contracts_run: 4`. Re-run of each mutant independently confirmed the
exact failing assertion and source restoration.

| Claim | Positive node | Fault path | Baseline | Mutant RED |
|---|---|---|---|---|
| `L01_SIGNED_R08_CELLS_REACH_NATIVE_NONPARENT_SOURCE_BALANCE` | `test_l01_evidence_world_consumer.py::test_signed_r08_evidence_reaches_actual_nonparent_numbers_and_world_routes` | `pre553_universal_world_binding.py` signed-cell copy | PASS | `test_l01_evidence_world_consumer.py:40` `assert numbers['source_balance_count'] == 4` -> `assert 0 == 4` |
| `R08_SIGNED_CONSUMER_DENOMINATOR_REACHES_E04_STEP` | `test_universal_evidence_binding.py::test_positive_actual_producer_consumer_values_read` | `pre553_universal_evidence_binding.py` `e04_step` denominator projection | PASS | `test_universal_evidence_binding.py:497` `assert step["denominator"] == 60` -> `assert 61 == 60` |
| `ACTUAL_P41_DISTINCT_MODELED_TEMPORAL_PAIR_IS_CONSUMED` (retained) | `test_universal_world_binding.py::test_r06r2_actual_r05_learned_to_p41_world_with_synthetic_pair` | `pre553_universal_world_binding.py` `temporal_changed` | PASS | `test_universal_world_binding.py:665` `assert view.temporal_changed is True` -> `assert False is True` |
| `R118_PREFIX_EMPIRICAL_STEP_REACHES_NATIVE_NONPARENT` | `test_world_conditioned_progressive_service.py::test_native_nonparent_consumer_runs_per_prefix_with_both_inputs` | `pre553_world_conditioned_progressive_service.py` `"steps": [step]` -> `[]` | PASS | `test_world_conditioned_progressive_service.py:31` `assert material["source_balance_reads"]` -> `assert []` |

The three new contracts are claim-specific implementation faults, not test,
import or setup mutations. The retained P41 fault corrupts a derived recorded
value that is set only after distinct clocks and distinct actual temporal
payloads are checked (`pre553_universal_world_binding.py:881-896`). A stronger
independent mutation that refuses to construct the T1 snapshot made the same
named test fail earlier at line 664 with `R05_CLAIMED_RECEIPT_MISSING`, showing
the test is also sensitive to actual snapshot non-consumption
(`evidence/p41-nonconsumption-probe.json`).

Source hashes were identical before and after the gate:
`evidence/pre-gate-source-sha256.txt` equals
`evidence/post-gate-source-sha256.txt`.

## Actual first-consumer measurements

The actual path is
`progressive_world_view` (`pre553_universal_world_binding.py:1337`) ->
`consume_world_conditioned_prefixes` (`:1374`) ->
`_pinned_nonparent_consume` ->
`rawlsing_next.sourcefree_world.nonparent.consume`
(`pre553_world_conditioned_progressive_service.py:105-160`;
`sourcefree_world/nonparent.py:6-24`).

T0 and T1 each select two prefixes. For every prefix:

- native state `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED`;
- denominator `4`;
- complete cells `{0: 0, 1: 4}`; the zero is an observed zero inside a
  supported binary cell set, not `ZERO_SUPPORT`;
- numerical source balance `4` (`cells['1'] - cells['0']`);
- `values_read` contains both `structural` and `empirical` channels;
- `route_probability` is `None` with
  `route_probability_reason=NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`;
- `n10w.world_conditioned_prefixes` length 2; `n10e_steps` length 2; each
  prefix carries its actual `n10e_consumer_hash` and native receipt.

T0 routes: `training=ELIGIBLE`, `exit_constraint=WITHIN_MODELED_BUDGET`,
`civil=ELIGIBLE`. T1 routes: `training=BLOCKED_BY_MODELED_RULE`,
`exit_constraint=RESOURCE_CONSTRAINED`, `civil=ELIGIBLE`. The empirical steps
are identical between T0 and T1; the world snapshots and routes differ.
`evidence/reviewer-first-consumer-trace.json` is byte-identical in meaning and
`output_hash` to the author's `first-consumer-trace.json`; the cold replay's
trace is byte-identical.

## R08 exact-coordinate multi-leaf check

The committed L01 fixture happens to have canonical leaf order equal to the
requested binding order, so it does not by itself exercise the repair. An
independent reordered probe used requested order `[X=1, O=AB]` while the
canonical AND leaf order was `[O, X]`:

- `pre553_universal_evidence_binding.py:877-899` associated `X` leaf to `X`
  binding and `O` leaf to `O` binding by exact coordinate;
- `mismatch_reason` returned `None`; the resolver returned `SUPPORTED` with
  denominator 4; the selected world view served both prefixes with cells
  `{0: 0, 1: 4}`;
- the old positional `zip` control (temporarily restored) failed with
  `EvidenceAssociationError: result is not exact support: UNKNOWN`;
- the single-conditioner prefix remained `SUPPORTED` denominator 4, conserving
  the accepted single-conditioner contract.

Evidence: `evidence/r08-reorder-probe2.json`,
`evidence/r08-old-zip-control.log`, `evidence/probes/r08_reorder_probe2.py`.

Residual: this reordered edge has no committed regression fixture or dedicated
proof.json in the candidate. The external executable control above proves the
repair at this review; a durable fixture is recommended in the author's next
ordinary pass. It is not a functional blocker at this scoped acceptance.

## Original-vs-current negative matrix

The historical R53 P53T RED evidence is preserved unchanged; it is not
repinned, merged or waived.

| Historical negative | Original R53 observed RED | Current executable negative | Current observed |
|---|---|---|---|
| D11 wrong conditioner item (`Y|C=1` receiving `Y|A=1`) | J42 adapter returned A evidence/denominator and P41/E04 served success for the C request | `test_actual_request_mutation_refuses_and_restores[condition_item]`; `test_wrong_claimed_prefix_condition_cannot_consume_signed_other_value`; cached wrong-condition probe | REFUSED; wrong condition `UNKNOWN`/`NO_EXACT_PRODUCER_BINDING`; reader association refused |
| D11 wrong conditioner value (`Y|A=0` receiving A=1) | same J42 depth reuse | `...[condition_value]`; `test_condition_a0_result_cannot_resolve_a1_request`; cached A0/A1 probe | keys distinct; wrong request `UNKNOWN`; reader refused |
| D12 ZERO_SUPPORT false positive | J42 aggregate productive; E04 success | `test_status_mutation_never_produces_supported_world[ZERO_SUPPORT]`; `test_actual_zero_support_does_not_become_positive_and_breaks_consumer`; P41 guard `EXACT_SUPPORTED_NONEMPTY_RISK_REQUIRED` | REFUSED; zero support not positive |
| D13 ROUTING_UNKNOWN exact label | P41 unknown evidence overstatement | `test_current_p41_receipt_owner_closes_historical_r53_failures[ROUTING_UNKNOWN]`; `P41Service.progressive` state guard | `P41ServiceError`; no exact-support claim |
| D14 missing structural state | J42 defaulted supported; E04 success | `test_actual_missing_structural_authority_is_not_supported`; selected-world `read` returns unavailable | REFUSED |
| R116 mixed-model prefixes | mixed model accepted and served | `test_r117_mixed_prefix_model_identity_refuses`; model identity in `_progressive_prefix_identity` | REFUSED `PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` |
| R118 consistent alternate model | scoped acceptance | `test_r117_consistent_alternate_model_remains_valid` | selected view; step hashes equal alternate rule hash |
| Revocation / restore | historical unavailable behavior | `test_r110_empirical_revocation_is_typed_unavailable_and_restores`; `test_revoked_empirical_and_world_dependencies_are_nonproductive_and_restore` | typed unavailable/partial, then selected view restored |
| Permission, clock, source, edition, risk, model, producer identity | R53/identity defects | `test_actual_request_mutation_refuses_and_restores[...]`; R08 identity-axis tests | REFUSED and restored |

The historical `Y|C=1` / `Y|A=1` labels are represented in the current fixture
by exact conditioner coordinate/value mutations (`X/O`, `A0/A1`). The checked
invariant is label-agnostic exact coordinate, typed value and occurrence
identity, not a copied label.

## Cold-install proof

`evidence/cold-logs/cold-replay-receipt.json`:

- `state: PASS`
- historical commit absence all true: P41 `f27d110...`, J42
  `f53cb0d...`, R118 `849a76d...`
- `remote_count: 0`
- `checkout_commit_count: 1`
- `clean_checkout: true`
- `trace_byte_identical: true`
- `output_hash: 760e934258844704ba0fb27e15f270ef880de1cd0c6fd7a3bfc45d6c004a705b`
- `fresh_venv: true`; `source_files: 374`
- cold tests: `167 passed, 4 deselected`; the four excluded nodes are the
  archival J42 and context-authority oracles, not runtime dependencies.

Independent readback of the disposable checkout: `git rev-list --count HEAD` =
1, `git remote` empty, `git status --porcelain` empty, all three historical
`git cat-file -e` absent, and `pip freeze` matched the dependency lock. The
checkout was removed after verification; the logs above are preserved. The warm
171-node suite includes those four archival tests and passed with the local
historical objects, separate from the cold sourcefree run.

## CI reconciliation and inherited RED

Reported at the repaired head: proof-integrity gate PASS 4/4; canonical-tree
integrity run #42161998797 PASS; R61 sourcefree workload run #42161998905 PASS;
governed court run #42161998791 144 PASS / 3 FAIL. The overall governed CI is
not green.

The exact CI API objects were blocked by the local credential
(`403`/`404`), so the run logs themselves were not fetched. At the exact head,
the underlying commands reproduce the reported outcomes:

- proof gate: PASS 4/4 (`evidence/proof-gate.log`), checker self-test 9 OK;
- canonical tree: PASS (`evidence/canonical-verify.log`);
- R61 workload: 105 passed; 37 passed + 1 documented skip; three witnesses PASS;
- governed court: 144 passed / 3 failed, with the inherited FIABC historical
  blob-anchor conflicts:
  `test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope`,
  `test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state`,
  `test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law`.

Those three failures are preserved as a separate FIABC owner/authority problem.
No historical LiTS/T5 evidence was repinned, no failure was waived, and this
receiving did not expand into FIABC repair.

## Residual holds

1. The two PR comment bodies and exact Actions run logs were not readable with
   the available credential. Acceptance relies on the launch-quoted mandatory
   requirements, the in-repo L01 request/return, the R53/R116/R118 returns and
   independently executed behavior. This is a process/access residual.
2. The R08 canonical-reorder edge is independently proven here but lacks a
   committed durable regression fixture/proof contract. Recommended follow-up:
   add a reordered multi-conditioner fixture to the L01/R08 suite in the next
   ordinary author pass. Non-blocking at this scoped acceptance.
3. The retained P41 witness's selected fault is a recorded-flag corruption; the
   stronger independent non-consumption mutation also fails the named test, so
   the underlying consumption edge is exercised. Non-blocking.
4. Scope: sourcefree TEST_ONLY software behavior. No original35/source science,
   original survey data, R09/protected CI/production, N11/N12, Sorok actor,
   J52/W52, protected CAS or original scientific authority is conferred.
5. Inherited governed-court 144/3 remains RED and separate.

## Evidence index

All paths are relative to this return directory:

- `evidence/proof-gate.log`
- `evidence/pre-gate-source-sha256.txt`, `evidence/post-gate-source-sha256.txt`
- `evidence/proof-gate-selftest.log`
- `evidence/reviewer-sourcefree.log`, `evidence/reviewer-sourcefree-junit.xml`
- `evidence/reviewer-sourcefree-rerun.log`, `evidence/reviewer-sourcefree-junit-rerun.xml`
- `evidence/reviewer-first-consumer-trace.json`
- `evidence/cold-replay.stdout.json`, `evidence/cold-logs/`
- `evidence/mutant-probes.json`, `evidence/p41-nonconsumption-probe.json`
- `evidence/reviewer-negative-matrix.log`, `evidence/reviewer-negative-matrix-junit.xml`
- `evidence/cached-wrong-condition-probe.json`
- `evidence/r08-reorder-probe2.json`, `evidence/r08-old-zip-control.log`
- `evidence/r61-sourcefree.log`, `evidence/r61-sourcefree-junit.xml`
- `evidence/r61-decoder.log`, `evidence/r61-decoder-junit.xml`
- `evidence/r61-*-witness.log/json`
- `evidence/governed-court.log`, `evidence/governed-court-receipt.json`
- `evidence/canonical-verify.log`
- `evidence/prior/R53_00_RETURN.md`, `evidence/prior/R53_matrix.tsv`
- `evidence/prior/R116_00_REVIEW.md`, `evidence/prior/R118_00_REVIEW.md`
- `evidence/junit-summary.json`, `evidence/manifest.json`, `SHA256SUMS.txt`
- `evidence/commands.txt`, `evidence/ci-access-limitation.txt`

**Verdict: `ACCEPT_SCOPED_SOURCEFREE`.**
