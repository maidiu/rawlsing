# SOROK O-LIVE R2 — persistence, transition authority and hostile tests

## Runtime

- Worktree: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/olive-r2-return`
- Candidate: `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1`
- Python 3.11.3, pytest 9.1.1, macOS 13.7.8 x86_64.
- 23 tests pass; source manifest 144+3 PASS; tampered manifest FAIL.

## Commands

```sh
cd SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1
python3 -m pytest -o addopts='' -q test_living_reference.py test_living_reference_r2.py
python3 verify_source_manifest.py
python3 r2_live_transaction.py
```

Observed test result:

```text
.......................                                                  [100%]
23 passed in 21.53s
```

## A — persistence is a merge, not a reset

`refresh_state(existing, observed_source)`:

1. builds the frozen seed state;
2. merges missing nodes, edges and source rows into the existing state by stable ID;
3. preserves `history`, `axes`, `evidence_imports`, `legacy_records`,
   `missing_functions`, `intake_gaps` and `authority_holds`;
4. appends `REFRESH_MERGE` and records source-cut deltas;
5. recomputes derived gaps/work-now/coverage/blocked views;
6. writes `state.json` and `SNAPSHOT.json` atomically.

The live transaction proves:

| Step | Result |
|---|---|
| Baseline | 198 nodes / 423 edges / 22 gaps / 22 work-now candidates |
| Import O-SCIENCE | 212 nodes / 649 edges / 37 gaps / 37 work-now candidates |
| Source withdrawal (S5) | 3 required dependents + S5 self invalidated; 4 new invalidation gaps |
| Source repair (exact S5 source record) | 4 invalidation gaps removed; restored `L3_S5_NORMATIVE_MODEL`, `L4_S5_FLOURISHING_OWNER`, `L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE` |
| New requirement intake | `GAP_SOROK_R2_NEW_REQUIREMENT`; final 38 gaps / 38 work-now candidates |
| Refresh | history still contains `OSCIENCE_PATCH_IMPORTED`, the withdrawal hold, review gate, engineering upgrade, repair, intake, pending owner evidence and `REFRESH_MERGE`; axes and import digest preserved |
| Cold process `export` | exit 0, 212/649, history 9, import digest present, **state_digest equal** |
| Duplicate import | `DUPLICATE_IMPORT_IDEMPOTENT`, 212/649 unchanged |

A changed input SHA is visible as `SOURCE_CUT_CHANGED` plus
`GAP_SOURCE_CUT_STALE`; it does not reset the state or auto-GREEN currentness.

## B — real evidence ingest, not an inbox

`ingest_oscience` validates the exact counts, all 17 targets, all 14 new node
IDs, all 226 endpoints and all edge types. It adds:

- 17 candidate-evidence workstream records, preserving original S0–S16
  question/output exactly;
- 14 `MISSING_FUNCTION_01..14` candidate nodes, each bound to one of the 14
  C12→A5 backward consumer rows;
- 226 candidate edges, `176` `SCIENTIFIC_PRODUCT_REQUISITE_LINK__CANDIDATE` and
  `50` `REQUIRES_SOURCE_INPUT_TRANSFORMATION_FIRST_CONSUMER`;
- 102 legacy records with exact R3 source identity.

All 226 imported edges are `hypothetical`/candidate and `required=false`; they
cannot create a false required/causal blocked path. Duplicate digest imports
append only a no-op history record.

## C — 102 original source records are no longer empty

For every O-SCIENCE `legacy_definition_records` row, the integrated derivative
copies the matching R3 `rows[*].evidence_source`:

- `commit`, `path`, `git_blob`/`object_id`, `object_type`, `source_timestamp`;
- `source_grounding = R3_KEYED_EXACT`;
- `102/102` grounded, `0` missing.

The O-SCIENCE branch and its immutable return were not edited.

## D — no fake authorization

`_apply_transition` now requires a typed evidence object. Accepted/refused
behavior:

| Request | Result |
|---|---|
| Plain `owner_evidence="OWNER_GRANT fake"` string | `REFUSED / UNKNOWN_EVIDENCE_KIND` |
| `OWNER_GRANT` with fabricated commit/path/blob | `REFUSED / FORGED_OR_MISSING_GIT_SOURCE` |
| `OWNER_GRANT` with real Git source and competent owner slot | `PENDING_MANUAL_VERIFICATION`; axis `OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION`; no native/adopted claim |
| Plain `HUMAN_PARTICIPANT fake` string | `REFUSED / UNKNOWN_EVIDENCE_KIND` |
| Structured human participant record without external verification | `SIMULATED_NOT_ADOPTED`; axis `CANDIDATE_LAB_DEMO_NOT_HUMAN_A5`; never `PROVEN` |
| `ORIGINAL_SCIENCE_ISSUANCE` request | `PENDING_MANUAL_VERIFICATION`; axis `HOLD_MANUAL_VERIFICATION`; never issued |
| Positive sourcefree engineering candidate | `APPLIED_CANDIDATE_ONLY` or `SIMULATED_NOT_ADOPTED`; no native/owner/human change |

Preimage mismatch, wrong owner slot, unrelated reviewer and forged Git object are
refused. `authority_holds` records pending owner evidence for manual competent
verification.

## E — causal, typed invalidation

Edges are classified into causal/required, consumer, governance, epistemic and
hypothetical/index types. Source withdrawal traverses only `required && causal &&
!hypothetical` dependents. Positive upgrades record affected candidates but
invalidate nothing.

Observed:

- S5 source withdrawal invalidated `L3_S5_NORMATIVE_MODEL`,
  `L4_S5_FLOURISHING_OWNER` and `L5_S5_HARMFUL_ATTACHMENT_COUNTEREXAMPLE`;
- `M01`, `V3CORE-R1`, `S0` and the Pyat boundary remained unchanged;
- repair with the exact S5 source record restored only those dependents to
  `CANDIDATE_READY`;
- O-SCIENCE hypothetical edges were excluded from required invalidation;
- cycles and non-causal/index edges did not silently turn red.

## F — dynamic gaps/work-now/blocked-chain

`work_now` is derived from `gaps`, not a module constant. Each candidate carries
its owner, source/science state, required blockers, consumer, and downstream
impact. Groups are explicit (`PRODUCT_WORKSTREAM`, `C12_A5_FUNCTION`,
`NATIVE_PERSON`, `SCIENCE_OWNER`, `REVIEW`, `EXTERNAL_BOUNDARY`,
`RECOVERY`, `DISCOVERED_REQUISITE`); no scalar priority is issued.

`blocked-chain` is a typed required-blocker/impact view. `critical-path` is
retained only as a labeled legacy DAG shortest-path illustration, not a claim of
scientific criticality.

## G — currentness and actual workers

`observe_source_cut` reads the actual local Git refs and records the exact read
timestamp:

| Source | Observed SHA |
|---|---|
| PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| O-LIVE | `67f667421fc90b22aad95cfc253a16feabc92348` |
| R3 | `e50d32eb6816578145d17dcd637a0b90b3a1ef40` |
| R3 review | `06f40a3eabb4acfc57f433144224695c2427c25f` |
| O-SCIENCE | `45efe65f73475e6a815e5fe93c3ee5179de27f67` |

The old `3f3d9ec2…` R2 independent negative court is recorded separately and is
not called R3 acceptance. SEALED is not running. Branch presence is not a
process lease and a missing local process is not proof of owner absence.

## H — single-state readback and hostile negatives

The live transaction performs:

1. exact R1 baseline build;
2. complete O-SCIENCE import;
3. precise S5 source disqualification;
4. genuine scoped sourcefree reviewer engineering evidence on `CP-A5-R2`
   (candidate engineering `INDEPENDENT_ACCEPT_SCOPED`; human `NOT_PROVEN`;
   authority unadopted);
5. source repair, new requirement intake, refresh and cold reread;
6. duplicate import idempotence;
7. tampered source-manifest object id → verifier FAIL;
8. fake owner/human credentials → refused;
9. restore known-good state and re-run all 23 tests.

Evidence file: `candidate/r2_live_transaction.json`.

## NOT_RUN

- Independent review, owner adoption, native science, Pyat native source,
  human participant A5, production/PRE-MAIN, PR or other branch mutation.
- Full external historical suite beyond the explicit 23 local tests and the
  source manifest verifier.
