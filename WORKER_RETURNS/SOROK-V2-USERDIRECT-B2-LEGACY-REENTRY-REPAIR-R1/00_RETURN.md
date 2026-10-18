# User-directed B2 legacy reentry repair

The E2 gap is fixed in the B2 candidate. An existing identity mapping now requires **exactly one occurrence at that event ID, keyed by the mapped content hash**, before B2 can reuse an admission or invoke B1. The check executes inside the existing `BEGIN IMMEDIATE` writer lock. A conflicting direct B1 row inserted after mapping returns `DENIED / EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE`, `event_admission=NOT_PERFORMED`, and `b1_invoked=false`. Checkpoint and all committed objective facts remain unchanged.

This is seven added and two removed lines in candidate `WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1/bridge.py`, plus this repair return. Original R1 `358fd1086eac0a4aa7791ca14abc25c45b935ddd`, E2 `8983315b3aee130e9446d43bd983c4a91c6f0437`, all owner source, and frozen tests remain immutable. The new branch is `codex/b2-legacy-reentry-repair`. User authorization is the direct follow-up asking whether this acceptance gap can be fixed; the prior reviewer now acts as repair implementer, not independent acceptance reviewer.

## Actual verification

| Court | Result |
|---|---|
| Exact E2 strict tests on original R1 | **2 RED reproduced** |
| Same frozen E2 strict tests on fix | **2 PASS** |
| Unchanged inherited + B2 checks | **330 PASS** |
| Unchanged R1 repair court | **45 PASS** |
| Additional controls | **5 PASS** |
| Whole frozen E2 court | **42 PASS / 2 expected old-behavior observation failures** |
| Whole frozen X2 court | **16 PASS / 1 expected old-collision demonstration failure** |
| Frozen native F1 | **17 RED, exit 1, unchanged** |

The two whole-E2 failures are `test_direct_b1_after_wrapper_limit_is_measured[False/True]`, which explicitly assert that polluted-ledger replay returns the former admitted object. They fail because the fix now refuses it. E2's two actual acceptance assertions, `test_legacy_after_mapping_must_fail_closed_at_b2_reentry[False/True]`, are green. No frozen source, expectation, skip marker, or failure classification was edited; complete raw pytest output and JUnit preserve these different oracle purposes. X2 likewise continues to preserve the old assertion that the original duplicate-admission defect exists.

The five new controls verify that an unrelated legacy event does not block a lawful replay (both checkpoint states), an exact-content B1 duplicate remains idempotent (both states), and a fresh B2 process blocked by a competing SQLite writer sees the newly committed conflicting legacy row before proceeding. The last case records process ID, actual SQL trace, before/after tables and refusal. Both original E2 SQL snapshots now show refusal with every pre-existing row preserved.

R1 and E2 concurrency, killed-writer recovery, distinct event identities, missing identity/ingress/occurrence checks, exact replay and cold persistence all run unchanged. Positive and journal-only two-event trace files are byte-identical to R1. Native F1 retains the same 17 REDs and 19 boundary/17 N/A accounting; no native positives are manufactured.

## Reproduction and custody

```sh
python3 verify_repair.py before
python3 verify_repair.py after
python3 finalize.py
```

Run from this return directory. The scripts use the existing authorized Git store to materialize exact R1 B2 and 69 imported files, stage frozen R1/E2 tests by exact Git commit, and replace only the candidate bridge for the after run. Every imported source hash and frozen-test Git identity is verified. Actual module paths/hashes, commands, logs, JUnit and SQL states are under `evidence/`. Temporary source staging is ignored; no prior return evidence is overwritten. `source_diff.patch`, `verification_receipt.json` and `artifact_manifest.json` identify the exact change and evidence bytes. Evidence copies remove local paths and hostnames without changing test results or source bytes.

The check uses a full occurrence scan, as the prior unmapped legacy check did, appropriate to this bounded registrar; this is not a production indexing migration. Direct privileged B1/SQL writes remain possible outside B2. The repair detects inconsistent prestate on B2 reentry and does not delete or retroactively authorize facts. It does not create production ADP019 authority, actor permission, new psychological law, B3 integration, or survey execution.

Grade: **`SOURCEFREE_LEGACY_REENTRY_REPAIR_CANDIDATE_PENDING_INDEPENDENT_REVIEW`**. E2's original report remains a correct report about the exact old R1 SHA. Independent acceptance of this new repair remains a separate reviewer action. The normal push and direct remote verification identify the final SHA outside its own commit preimage.
