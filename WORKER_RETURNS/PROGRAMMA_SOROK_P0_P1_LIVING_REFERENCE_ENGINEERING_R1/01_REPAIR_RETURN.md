# PROGRAMMA SOROK P0/P1 — coherent repair R1 return

**Job:** `programma-p0p1-repair1-d8e579b1a1a3`
**Repair branch:** `codex/programma-sorok-p0-p1-repair1-20261102`
**Reviewed baseline:** `54013d1907e5ea55b0d1f54ea9afe07ef6388b11`
**Original implementation:** `93945e4b4539fd5d5e39805d7d1f35d2325a2cbd`
**Original engineering baseline:** `a89e5ccbe67400168aaea8367f7aa00ca0de7625`
**Status:** `AUTHOR_TESTED__INDEPENDENT_ACCEPTANCE_NOT_ISSUED__WHOLE_SCOPE_NOT_YET_PROVEN`

The repair is implemented in the two permitted directories. No other repository
source/control/science/actor/PRE-MAIN file was edited. Operating journal history
bytes are unchanged; the quarantine bytes were not rewritten. No provider,
controller, credential, deployment, force-push or reset operation was used.
Model/provider/effort remained OpenCode Go / DeepSeek V4.1 Flash / MAX.

## Finding → repair → proof

| # | Review finding | Repair | Proof |
|---|---|---|---|
| 1 | Caller strings, wildcard scope, unrelated real document/commit or arbitrary appointment could establish acceptance. | `_verify_acceptance_record` now ignores caller-written evidence fields. It requires the record to be one of the node's own immutable source refs, parses reviewer/role, exact reviewed cut, accepting assertion, verdict and appointment seal from the record bytes, requires the node's exact subject to match the accepting assertion, requires a real appointment commit that binds the subject, and rejects wildcard/unrelated scopes. Seed JOIN-V records are verified at build time; `JOIN_E_7BF` and `JOIN_V_SCOPE_ACCEPTANCE` now carry the exact `7bf2da3` subject and are marked verified only from the existing JOIN-V record. | `repair_r1_probes.json:acceptance`; `repair_r1_cli_acceptance.json`; `test_repair_r1.py::test_acceptance_rejects_arbitrary_record_wildcard_and_unrelated_subject`; existing JOIN-V exact-scope tests. Arbitrary record → `REVIEW_RECORD_NOT_A_NODE_SOURCE`; wildcard → `WILDCARD_SCOPE_NOT_ACCEPTED`; unrelated subject → `NODE_SUBJECT_NOT_IN_REVIEW_RECORD`; shared-lineage subject under the fork-atomicity assertion → `NODE_SUBJECT_DOES_NOT_MATCH_ACCEPTING_ASSERTION`; JOIN-V applied to `CP-A5-R2` → rejected. |
| 2 | Cold replay imported a changed O-SCIENCE patch under its old declared digest. | `ingest_oscience` always recomputes `_digest(patch)` and fails closed when a supplied digest differs, before the duplicate-import branch. `_apply_event` recomputes the file digest and compares it with the event assertion before import. | `test_repair_r1.py::test_oscience_patch_digest_is_recomputed_before_import_and_duplicate`; `probe_faults.py` patch-tamper section. Changed semantic payload with unchanged counts/declared digest → `OSCIENCE_PATCH_DIGEST_MISMATCH`; duplicate path also fails. |
| 3 | A valid journal prefix with a dropped complete accepted final event silently replaced newer state; concurrent state writers could overwrite newer derived state. | `_load_state` now compares the journal prefix against the known state/snapshot head/revision and raises `JournalRegression` on regression. `recover` is the explicit recorded path. `_save` uses an exclusive lock, revision CAS and monotonic-revision guard. `commit_event` serializes append + rebuild + save under a commit lock. | `test_repair_r1.py::test_complete_tail_loss_is_refused_without_overwriting_newer_state` and `::test_concurrent_commit_event_writers_preserve_all_events_and_monotonic_state`; `probe_faults.py`. Complete-tail drop → `JOURNAL_PREFIX_OLDER_THAN_KNOWN_STATE:2<3`, state bytes unchanged; explicit recovery marked. Two concurrent `commit_event` CLI writers → 3 events, revision 3, head matches, state digest equals cold replay. |
| 4 | Restoration ignored active review/engineering/science/authority negatives on required causal prerequisites. | `_recompute_consumer_grades` now checks source, review, engineering, science and authority negatives on the target and on every exact `REQUIRED_CAUSAL` predecessor. Unrelated holds and non-causal relations are not scanned. | `test_repair_r1.py::test_live_and_cold_withdrawal_restore_preserves_review_and_engineering_negatives`; `repair_r1_probes.json:withdrawal_restore`; `repair_r1_cli_withdrawal.json`. After source restore, `P1_LATER_HELP_CONSUMER` remains `INVALIDATED_BY_UPSTREAM` because `P1_B` review is `REVIEW_FAILED` and `P1_A` engineering is `FAILED`; GT0 and Q-GAME paths are unchanged. |
| 5 | A present-source record was accepted as proof of source absence/withdrawal. | Added `SOURCE_WITHDRAWAL` and `AUTHORIZED_EXCLUSION` evidence kinds with explicit basis/authority/scope. Operating withdrawal requires a recorded `EVIDENCE_WITHDRAWAL` qualification event (or an explicit scoped exclusion). Present `SOURCE_RECORD` cannot declare absence. Statuses distinguish qualified absence, owner withdrawal, integrity loss and authorized exclusion. | `test_repair_r1.py::test_present_source_cannot_prove_withdrawal_or_absence`; `test_p1_whole_program.py::test_demo8_qualified_withdrawal_restoration_live_and_cold`; `repair_r1_cli_withdrawal.json`. Present source → `QUALIFIED_WITHDRAWAL_EVIDENCE_REQUIRED`; unrecorded declaration → `QUALIFIED_WITHDRAWAL_EVENT_REQUIRED`. Live and cold replay both exercised. |
| 6 | Fake `a*40` or unrelated commit could become a returned artifact; caller-written requirements became source-backed work-now. | `intake_candidate` requires a real commit SHA, binds `sha == source.commit`, verifies the source object, and accepts requirements/gaps/node updates only with a verified locator/quote in the return. Unlocated claims remain visible as `CALLER_CLAIM_UNVERIFIED` (or explicitly labelled `HQ_INFERENCE`) and are not source-backed. New nodes/edges require verified locators. | `test_repair_r1.py::test_return_intake_requires_real_sha_and_source_locator`; `repair_r1_cli_return_intake.json`; `repair_r1_probes.json:return_intake`. Fake SHA and SHA/source mismatch → quarantined; unlocated gap → `CALLER_CLAIM_UNVERIFIED`, `source_backed=false`, node operational `CANDIDATE_ONLY`; located gap → `SOURCE_LOCATED`, `source_backed=true`. The historical W1-A journal gap has no locator and is retained visibly as `CALLER_CLAIM_UNVERIFIED`. |
| 7 | Nodes with local external refs claimed `SOURCE_EXACT` from ref existence alone. | Per-node source verification is derived at build time. Missing local external bytes → `UNREAD`; byte mismatch → `WITNESS_MISMATCH`; invalid refs → `SOURCE_REF_INVALID`. Status reaches axes, home `source_witness`, focus, maturity and derived `GAP_WITNESS_*` gaps. Exact failure remains visible; no global skip or source deletion. | `test_p0_trust_repair.py::test_source_refs_report_missing_external_witness_honestly`; `test_repair_r1.py::test_external_witness_reaches_home_focus_maturity_and_gaps`; `repair_r1_verify_sources.json`; `repair_r1_focus_v3.json`; `repair_r1_probes.json:views`. Disposable matching bytes verify; mismatched bytes fail with `LOCAL_EXTERNAL_SHA256_MISMATCH`. |
| 8 | Home began with implementation status/terminal obligations, not purpose/experience/100-101 constraints. | `home_view` and generated HTML now begin with source-qualified unchosen-neighbour purpose, Astra B/D experience and 100/101 constraints, then status and terminal obligations. Values come from the existing canonical nodes, not a second narrative store. | `test_repair_r1.py::test_home_is_purpose_first_and_work_now_has_no_descendant_priority`; `repair_r1_home.json`; `repair_r1_html_receipt.json`; `repair_r1_probes.json:views`. CLI first keys: `schema`, `purpose`, `intended_human_experience`, `constraints_100_101`; HTML purpose precedes terminal obligations. |
| 9 | Work-now used descendant-count priority. | Removed the `-downstream_required_count` sort. Candidates use stable parallel-group/domain/id order; impact remains information. Each candidate exposes `terminal_contribution` and `uncertainty`. | `repair_r1_work_now.json`; `repair_r1_probes.json:views`; focused test above. `no_scalar_priority=true`; candidate order equals group/domain/id order. |
| 10 | Persisted reference presented inherited O-LIVE `67f667` as the engineering baseline. | `ENGINEERING_BASELINE=a89e5cc…` is now `build_startup`, `version_vector.sorok_startup`/`engineering_baseline`; inherited O-LIVE `67f667…` is separate `olive_source`/`baseline_identity.olive_source_cut`. GENESIS payload claims are preserved and labelled `INHERITED_OLIVE_SOURCE_IDENTITY_NOT_ENGINEERING_BASELINE`. History was not rewritten. | `test_repair_r1.py::test_baseline_identity_separates_olive_source_from_engineering_baseline`; `state.json:baseline_identity`; `00_START_HERE.md`. |
| 11 | `commit_event` did not pass CAS and state saves could be overwritten by a stale writer. | Covered by the commit lock, atomic locked CAS, monotonic revision guard and concurrent `commit_event` probe in finding 3. | `test_concurrent_commit_event_writers_preserve_all_events_and_monotonic_state`; `probe_faults.py:concurrent_commit_event`. |

## Test corrections (defective expectations removed)

- `test_source_refs_verify_against_git_and_local_external_bytes` previously
  required a global `PASS` while local external V3 witnesses were absent. It now
  asserts the exact `UNREAD` / `LOCAL_EXTERNAL_SOURCE_NOT_PRESENT` negative and
  separately tests disposable matching and mismatched witness bytes.
- `test_real_return_is_candidate_only_and_survives_cold_rebuild` previously
  expected an invented caller requirement and an unlocated node update to become
  operating candidate evidence. It now expects `CALLER_CLAIM_UNVERIFIED`,
  `source_backed=false`, and no operational promotion without a locator.
- `test_self_authored_or_selfhashed_acceptance_record_is_refused` previously
  exercised caller-written acceptance fields. It now checks that caller fields
  cannot override the record and that a self-hashed/foreign record is not a node
  source.
- `test_demo8_withdrawal_restoration_live_and_cold` previously used a
  present-source `SOURCE_RECORD` to declare `SOURCE_NOT_FOUND`. It now uses a
  qualified `EVIDENCE_WITHDRAWAL` event plus a scoped `SOURCE_WITHDRAWAL`
  transition, and exercises live and cold replay.
- Added `test_repair_r1.py` for the repaired boundaries above.

## Commands and observed results

```sh
cd SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
python3 -m pytest -o addopts= -q -p no:cacheprovider \
  test_living_reference.py test_living_reference_r2.py \
  test_p0_trust_repair.py test_p1_whole_program.py test_repair_r1.py
```

Observed: `62 passed in 155.66s` (exit 0). Evidence: `evidence/repair_r1_pytest.txt`.

```sh
python3 living_reference.py verify-journal
```

Observed: `PASS`, 4 events, head
`22565fd2a79b1d40cb0d67a546edd4cd417b10ee33d8af366f0de1b147be8d84`,
state digest `bfb9465b5914398c9534e5bbc1281eea7b59e2b7aa702105b49c3d844a6ade3c`.
Evidence: `evidence/repair_r1_verify_journal.json`.

```sh
python3 verify_source_manifest.py
```

Observed: `PASS`, 144 Sorok rows, 3 references, 0 errors.
Evidence: `evidence/repair_r1_source_manifest.json`.

```sh
python3 living_reference.py verify-sources
```

Observed: `FAIL`, 80 local refs checked, 3 external refs not re-read locally,
6 exact `LOCAL_EXTERNAL_SOURCE_NOT_PRESENT` failures on
`V3_RUN_ONE_YEAR`, `V3_PERSONA_SHEET`, `V3_EXTERNAL_SIMULATION`,
`V3_SERVER_TURN`, `V3_V2_LOADER`, `V3_EXTERNAL_MEMBER_HASH_MISMATCH`.
This is the honest current witness negative, not a global source failure.
Evidence: `evidence/repair_r1_verify_sources.json`.

```sh
python3 r2_live_transaction.py
python3 probe_faults.py
python3 repair_probes.py
```

Observed:

- disposable demo operating files byte-identical; self-review remains
  `PENDING_INDEPENDENT_ACCEPTANCE`; synthetic requirement quarantined; second
  independent RED preserved; cold digest equal.
- `probe_faults.py`: concurrent journal appends retained 3 events with stale flags
  `[false,true]`; concurrent `commit_event` writers retained 3 events at revision
  3 with matching head and state digest; complete-tail drop refused with state
  unchanged and explicit recovery recorded; patch tamper refused with
  `OSCIENCE_PATCH_DIGEST_MISMATCH`.
- `repair_probes.py`: acceptance, exact/locator return intake, qualified live/cold
  withdrawal-restore, purpose-first views, witness status and baseline identity
  all report the repaired behavior.

Actual CLI/HTML evidence:

- `evidence/repair_r1_home.json`
- `evidence/repair_r1_work_now.json`
- `evidence/repair_r1_whole_gaps_T.json`
- `evidence/repair_r1_whole_gaps_all.json`
- `evidence/repair_r1_maturity_q_health.json`
- `evidence/repair_r1_focus_q_health.json`
- `evidence/repair_r1_focus_v3.json`
- `evidence/repair_r1_lateral_can011.json`
- `evidence/repair_r1_cli_return_intake.json`
- `evidence/repair_r1_cli_withdrawal.json`
- `evidence/repair_r1_cli_acceptance.json`
- `evidence/repair_r1_probes.json`
- `evidence/repair_r1_fault_probe.json`
- `evidence/repair_r1_demo_isolation.json`
- `evidence/html/programma_home_r1.html`

## Operating and quarantine preservation

The canonical journal remains 4 events with head
`22565fd2…be8d84`; its bytes were not edited. The historical quarantine files and
manifest were not rewritten. The derived `state.json`/`SNAPSHOT.json` were
regenerated from the same journal plus frozen seeds. The repair only stages the
two permitted directories.

## Verdicts

**ENGINEERING — AUTHOR_TESTED; independent acceptance of this repair not issued.**
The inherited suite plus focused repair tests pass locally, including
subprocess/cold replay, complete-tail-loss refusal, patch tamper, concurrent
`commit_event` writers, qualified withdrawal/restore, exact/locator return intake
and external-witness fixtures. This is author evidence only.

**SCIENTIFIC — no new scientific issuance.**
O-SCIENCE remains `UNREVIEWED_CANDIDATE_EVIDENCE`; P1 remains
`TEST_ONLY_SOURCEFREE_NOT_NATIVE`; JOIN-V remains scoped to `7bf2da3`; no new
psychological rule, native CAN/ADP/SCI05 grant or human A5 claim is issued.

**AUTHORITY — candidate reference only.**
No owner/native/human/PRE-MAIN adoption, controller activation, production
deployment or external custody is claimed. Local hashes are integrity checks, not
external custody.

**WHOLE SCOPE — `WHOLE_SCOPE_NOT_YET_PROVEN`.**

## Remaining limits

- The six local external V3 witnesses are absent in this checkout. Their exact
  `UNREAD` negative is visible; no archive recensus was run and no external file
  was copied.
- JOIN-V certifies only the historical `7bf2da3` fork-atomicity scope. It does not
  certify this implementation or migrate to native C9/C12.
- The historical W1-A return intake had no locator, so its gap remains visibly
  `CALLER_CLAIM_UNVERIFIED`; a locator-qualified intake is demonstrated separately.
- C9/C12/C11, native CAN008/CAN011/ADP/SCI05, Pyat N11/N12, human A5, ethics and
  PRE-MAIN integration remain held or missing.
- No independent reviewer has accepted this exact repaired commit. HQ verification
  remains required for the changed boundary.
- This is the first repair tranche, not whole-estate completion or an actual
  developmental person.
