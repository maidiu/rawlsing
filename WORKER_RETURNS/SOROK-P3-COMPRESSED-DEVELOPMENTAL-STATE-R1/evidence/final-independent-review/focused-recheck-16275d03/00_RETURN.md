# SOROK P3 focused changed-cut re-review — ACCEPT_SCOPED_TEST_ONLY

**Reviewed SHA:** `16275d03fc4724a694c48ed9d447c4eeadbe25f2` on remote `agent/sorok-p3-compressed-developmental-state-20261106-r1`; remote head verified exactly.
**Review branch:** `review/sorok-p3-focused-recheck-20261107-r1`.
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516` (ancestor unchanged).
**Reviewer:** same distinct nonauthor, OpenCode `opencode-go/deepseek-v4.1-flash` variant `max`; effective metadata verified; quota **UNKNOWN**. Same model/provider/harness, no account/region/effort/UI change.
**Write scope:** `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/final-independent-review/focused-recheck-16275d03/` only. No runtime/tests/fixtures/production/PROGRAMMA/checkpoint edits; no merge.

## Verdict

**ENGINEERING: ACCEPT_SCOPED_TEST_ONLY for the exact runtime cut.** M1, M2 and M3 are repaired and independently verified at this SHA. PRIMARY, cold reopen, denial/cross-root, real-process crash, store/owner, unit and resource cases pass at the exact source. The 13/13 author/HQ matrix at source commit `486d42a4a` is consistent with this tree; I inspected all 13 logs and source hashes but did not execute the full matrix myself.

**One non-runtime provenance correction remains:** the reviewed evidence commit `16275d03` does **not** change only evidence/checkpoint records; it also changes three `PROGRAMMA_SOROK` records (`08…`, `09…`, `10…`). All matrix `source_sha256` values still match the reviewed tree. This is an evidence/commit-scope mismatch, not a source/runtime mismatch; a pure evidence/checkpoint cut or explicit HQ provenance disposition is needed for clean receiving. **No native science, production rule, source grant, B/human validity, CAS or merge is claimed.**

## Source closure

Matrix `source_sha256` values were checked with `git show 16275d03:path | shasum -a 256`; all six match:

| Path | SHA-256 |
|---|---|
| `p3/compression.py` | `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4` |
| `p3/p3_owner.py` | `e735ada798533a8f568739e823767bb2e2b4272c3c03d84dc2cd47f73cf65df1` |
| `p3/state_store.py` | `173d4d6d3e94580804cac90039a01bfe6e3adfffcda9e806a56132b10ecc06bf` |
| `run_p3_vertical_slice.py` | `1a895a4b68ae190679827197d2c58591afd0985c3ee30387bba1432b8d145462` |
| `tests/p3_fixture_support.py` | `7c3490178921c0765c8dfd42c9fb3f39d0c4696d2d048340094d746120b958eb` |
| `tests/test_p3_vertical_slice.py` | `0501754503a2af007154494654ed7f1edf5957e91ae56892949392f51b39c7ff` |

Additional exact hashes: `tests/test_p3_owner.py` `40ac0103…`, `tests/test_state_store.py` `03429d6d…`, `p3/projections.py` `ca405dda…`, `p3/test_rules.py` `27272cd4…`.

## Exactly executed at this SHA

All execution used a `git archive` scratch copy of the reviewed SHA; no runtime/test edits.

| Command / case | Actual result |
|---|---|
| `tests/test_state_store.py tests/test_p3_owner.py` | **61 passed, 1 skipped in 36.44s** (missing-store guard) |
| `test_compression.py test_projections.py test_projection_receiving.py test_rules.py` | **37 passed in 7.82s** |
| M1/M2 target: `test_finish_before_commit_and_receipt_link_mismatch_refuse`, `test_finish_binds_receipt_ref_access_and_compression_evidence`, `test_compression_evidence_survives_psych_committed_crash` | **3 passed in 5.85s** |
| PRIMARY | **1 passed in 441.08s** |
| H cold reopen | **1 passed in 280.46s** |
| H wrong identity/time + cross-root | **2 passed in 7.32s** |
| H real-process crash | **1 passed in 7.05s** |
| Resource case with independent metrics path | **1 passed in 226.77s** |

## M1/M2/M3 dispositions

### M1 — repaired and verified

`p3_owner._result` now includes `effects_receipt_hash` and `P3_PSYCH:<receipt.response_hash>`. `state_store._validate_result` requires a receipt link, exact receipt reference, receipt-bound actor surface, and receipt-bound compression. `commit_effects` stores projection/compression in the receipt before `receipt_hash`. The new negative tests refuse omitted/wrong link, forged ref, wrong accessible and missing/wrong compression; the full store/owner suite passes 61P/1skip.

### M2 — repaired and verified

`p3_owner._effect` computes projection and compression **before** `commit_effects`; the receipt stores both; `PSYCH_COMMITTED` recovery reads them from the receipt and `_result` includes them. `test_compression_evidence_survives_psych_committed_crash` passes: injected `finish` failure leaves PSYCH_COMMITTED, cold reopen recovers the exact receipt compression envelope and effects hash, operation completes. The owner suite also passes the real child crash boundary.

### M3 — repaired and verified

`measure_case` now uses incremental DB+WAL bytes. Independent resource metrics:

```
bytes_per_record = 741,600.0
bytes_per_event  = 247,200.0
db_bytes = 4,096; wal_bytes = 1,536,792; db_plus_wal = 1,540,888
incremental_db_plus_wal = 1,483,200
provider_calls = 3; batches = 3+3; retrospectives = 2
provider_context_bytes = 4,359
cold_open_seconds = 10.512
batch latencies = 35.511 / 161.456 / 17.413 s
```

Per-record/event values are positive and include WAL; the prior zero metric is closed.

## Full13 matrix audit

- `matrix_summary.json`: source commit `486d42a4aa5dcd449564b95567ae93b59c4679a4`; **13 passed, 0 failed**.
- All 13 logs: `executed=true`, `exit=0`, `status=PASS`, stdout `1 passed`; `case_results.tsv` matches.
- All six matrix `source_sha256` values equal the reviewed tree.
- All 13 commands target the exact test IDs; no renamed/deleted/weakened tests in matrix logs.
- The logs were produced in the author worktree at the source commit; they are author/HQ matrix evidence, not my execution. I independently ran PRIMARY, cold, denial/cross-root, crash, resource and the owner/store/unit/M1/M2 suites.
- Author terminal intake: exit **1** (`Failed to execute statement`), no commit, no `00_RETURN`, no remote update; E rerun3 PASS 216.10s and H-cold rerun2 PASS 304.36s use harness SHA `ebf970…`, while the combined matrix uses `050175…`. The terminal uncommitted state is not acceptance; the combined 486d42a4 matrix is the 13/13 evidence. Author terminal bytes are preserved, not adopted.

## Commit-scope mismatch (reported, not hidden)

`git diff 486d42a4..16275d03` contains the combined matrix evidence/checkpoint plus **three PROGRAMMA_SOROK record changes** (`08_INITIAL_EVIDENCE…`, `09_INHERITED_144…`, `10_RECONCILIATION_QUEUE…`). Therefore the prompt's statement that the reviewed commit changes only evidence/checkpoint records is inaccurate. The six runtime/test source hashes still match; no source/runtime hash mismatch. A pure evidence/checkpoint cut or explicit HQ records-provenance disposition is required before protected receiving; this is not an engineering runtime defect.

## Executed vs inspected

**Executed:** store+owner 61P/1skip; units 37P; M1/M2 3P; PRIMARY; H cold; H identity/time+cross-root; H crash; resource.  
**Inspected only:** all 13 matrix logs/case_results, matrix source hashes, author terminal intake and E/H-cold terminal logs, matrix A/B/C/D/E/F/G/H identity cases.  
**Not run:** all 71 inherited #704 tests (separate lane), all13 full matrix independently, native/authority operations.

## Limits / residual uncertainty

- Full13 is author/HQ evidence; only the primary/cold/resource/denial/crash + owner/store/unit/M1/M2 cases are my execution.
- The reviewed evidence commit's PROGRAMMA changes are a provenance scope mismatch; source/runtime hashes match.
- Author terminal intake exit1/no commit is not acceptance; combined matrix is separate.
- No native CAN/ADP, ADP016/017, original actor/B, human validity, production registry, CAS or merge is accepted.

**Verdict: ACCEPT_SCOPED_TEST_ONLY** for exact runtime engineering cut `16275d03fc4724a694c48ed9d447c4eeadbe25f2`; M1/M2/M3 closed; commit-scope provenance correction required separately. Science and authority remain HOLD.
