# Whole product mapping and path adversarial review

## 1. Exact primary source is real

Both Program Map versions were independently retrieved from Git:

| Version | Commit | Blob | Status |
|---|---|---|---|
| Current HQ | `865b5b01e1a27e99020cf2bb389af8cd4c874b57` | `2a0a3a42d66f566f92d5c333fbbea4a5adb383b2` | `ACTIVE_EXPLORATORY_PROGRAM_R1` |
| Earlier original | `3c423a0f74915a01911197b0023de9f85fd74aff` | `6271bb66b3cd2d92e2b814c4cd626220c2cdfe40` | `ACTIVE_EXPLORATORY_PROGRAM_R1` |

Both contain all 17 headings `S0`–`S16`, each with a question and output. The
current version adds only a prepended needs-first trajectory; all 17 S sections
are byte-equivalent at the question/output level. The 17 registry S rows carry
the current commit, exact path and exact blob; their questions and outputs match
both maps. The earlier commit/blob pair is recorded in every S row.

These are historical exploratory product workstreams. They are not V3 Courts
S0/S1 research stages, not the modern S39–S52 coding series, and not current
canonical adoption. The index states this in the S rows and in the correction
note.

## 2. Denominators and row source coverage

The registry contains 144 Sorok rows:

- 19 C/A
- 40 M
- 12 Sorok N
- 16 O
- 15 E
- 17 S0–S16
- 4 returned assets
- 10 additional cross-component edges
- 8 pre-existing production/experiment lineages
- 3 F1C/F1CR source rows

The L0–L5 index contains 189 nodes and 431 edges. The validator reports 74 L3
nodes, 40 owner slots, 3 traversals and 66 explicitly typed containment cycles.

This satisfies count coverage. It does **not** establish that every source
reference is a real exact Git object.

## 3. Source-reference defects

### 3.1 Null source blobs

Five Sorok rows have a real commit and path but `evidence_source.blob = null`:

| Row | Commit | Path | Actual Git blob |
|---|---|---|---|
| `B1` | `c0f4588c...` | `.../bfirst.py` | `94ffc52847e4c8ae760212d1bc8543594ba793fa` |
| `B2` | `950ecf0b...` | `.../bridge.py` | `5c84ace202d04076e829461afee98dd0ae8ba5b7` |
| `B3` | `47b46a85...` | `.../developmental_loop.py` | `a8fc1bf2247072e8530e20635cdb575873cf484a` |
| `BP2P4J` | `5b3e6577...` | `.../bp2p4/product.py` | `8f7177a6b4e3ae0cae6316a13cf57adf363e0460` |
| `R15_V2` | `4ce79541...` | `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1` | tree `9237abd31cdadfd6888d2114a534c2f0a536e1b9`; not a file blob |

The validator does not require a blob for non-S rows. This is not an exact
source preimage claim.

### 3.2 Paths that do not resolve at the stated commit

Three rows use shortened/non-repository paths:

| Row | Claimed path | Git result | Actual source path at cut |
|---|---|---|---|
| `B3A` | `candidate/integration.py` | no such path at `8bd4d6b...` | `WORKER_RETURNS/SOROK-20261018-B3-X3-ATOMIC-ADMISSION-REPAIR-R1/candidate/integration.py`, blob `604e09986d87f404daa9857b25758ec2e1fe491d` (also a frozen copy exists) |
| `B3AS` | `candidate/integration.py` | no such path at `16f15a12...` | `WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-R1/candidate/integration.py`, blob `d3a324bb93c17fdaf12670dd153aeb138d9c426a` |
| `S39_S52` | `s52/session.py` | no such path at `c821b488...` | `WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52/session.py`, blob `c347d8a902f4f451852aca1054e9a3cd99d4c3f0` |

These are path/identity defects even if the intended source is obvious from the
title. A source-exact map must not use a relative or nonexistent path.

### 3.3 Source metadata is not bound to Git

All listed `source_cut_metadata` timestamps currently match the actual Git
commit dates, including the `865b5b01` and `3c423a0f` maps. However the validator
only checks that the timestamp is non-empty. A forged non-empty timestamp passes
(see `02`), so the timestamp table is not proof of source freshness.

## 4. S5, S7, S11, S13, S14, S15

The registry preserves the exact primary questions and outputs for all six:

- S5: benefit to the other independent of liking/compliance/dependency;
  normative model, evidence base, uncertainty law, anti-therapist-God constraints.
- S7: valid inference from repeated relational behavior without pseudo-diagnosis;
  player-model schema, feedback cadence, privacy model.
- S11: encounter/advancement/opacity/time/commitment/repair/retrospection UX;
  flows, prototypes, progressive disclosure, accessibility.
- S13: what can be sold without attachment/suffering/compulsive return as the
  revenue engine; aligned revenue hypotheses and prohibited incentives.
- S14: domination, harassment, sexual pressure, manipulation, stalking, gaming,
  exploitation, and user-exposure safety; safety constitution, abuse simulation
  law, privacy boundaries.
- S15: minimum product that can falsify the core theorem; alpha spec, prototype
  sequence, qualitative + quantitative evaluation.

That is necessary but not sufficient. The L0–L5 graph does not give them
distinct product, science, UX, economic, safety or evaluation nodes:

| S | Outgoing graph targets |
|---|---|
| S5 | `L1_GOVERNANCE` ×2, `L5_S_WORKSTREAM_PRIMARY_SOURCE`, `L1_PERSON` |
| S7 | `L1_GOVERNANCE` ×2, `L5...`, `L1_PERSON` |
| S11 | `L1_GOVERNANCE` ×2, `L5...`, `L1_PERSON` |
| S13 | `L1_GOVERNANCE` ×3, `L5...` |
| S14 | `L1_GOVERNANCE` ×3, `L5...` |
| S15 | `L1_GOVERNANCE` ×2, `L5...`, `L1_PERSON` |

All six are also members of `L1_GOVERNANCE.member_ids`. There is no specific
flourishing, player-feedback/privacy, UX/accessibility, revenue/incentive,
safety/abuse/privacy, or alpha/evaluation node; no L0 outcome and no L4 consumer
is specific to these workstreams. The three traversals T1/T2/T3 do not include
any of S5/S7/S11/S13/S14/S15. The 40 owner slots contain only the aggregate
`S0_S16_SOURCE` adoption question, not per-workstream product/science/HQ slots.

This is precisely the warned disappearance into generic `L1_GOVERNANCE`. HQ can
read the source questions, but cannot traverse their actual obligations and
outputs through the product map.

## 5. Full traversals reviewed

| Traversal | Path length | What it does | Limit |
|---|---:|---|---|
| `T1_CAREGIVING_PERSON` | 29 | L0 person → L1 person/actor → N02/N04/N05/N12 → O02/O04/O16 → C4/C5/C6/C12 → A0–A3 → M19/M25 → CP-A5/C9C12 → E10/E12/E13 → L5 tests/negatives | caregiving encounter is not authorized A5; theory requirements stay open |
| `T2_MATERIAL_REFUSAL` | 27 | L0 material → L1 world → N07/O08/O09/O16 → C4/C6/C8/C9/C10 → M02/M21/M25 → F1C/F1CR/R5/B-F1CR/V3CORE → E04/E05/E09/E12 → L5 | F1CR bytes missing; targetless is not native B; V3 annual clock is not N11; no B cash in A public view |
| `T3_HISTORICAL_TRANSFORMATION` | 26 | L0 history → L1 actor → N08/N09/N10/O07/O10–O13/O16 → C5–C9 → M19/M21/M26 → C9C12 → E02/E08/E14/E15 → L5 | no native issuer/causal law; same-count substitution RED; unknown stays unknown; no-change needs evaluated receipt |

These traversals are substantive and preserve limits. They omit the product
workstreams above; they are not a complete navigation of S0–S16.

## 6. R6/R7 and asset crosscheck

- R6 `28e38ebbf...`: 39 rows, 94 files, 9 material families, R41 133 pinned
  files, 26 selected tests. Registry records the same grain. No pooling with
  other assets.
- R7 `7f25fb9bf...`: 102 historical definitions and source/consumer evidence;
  its S0–S16 absence conclusion is superseded by the exact primary map. Its
  other source findings, F1CR missing bytes, reconstruction distinction, ZIP
  container mismatch and historical REDs remain valid caveats.
- `F1CR_CLAIMED_PATCH` remains absent; `F1CR_R5_RECONSTRUCTION` is distinct and
  not original source; V3 ZIP selected 31/31 and 488/488 Python members but
  whole-container hash mismatch is preserved.
- Current PRE-MAIN is `87755f02...`, three Pyat S6/H1/PE intake files ahead of
  the candidate’s `5fc1d43e...` build cut. No automatic rebase was performed;
  the candidate’s “current PRE-MAIN” label is therefore stale for this review.
- Four assets remain sourcefree author-tested candidates: CP-A5-R2 59 tests,
  C9C12-R2 6, B-F1CR-R2 R5 13/13 + 3/3 (no single `author_tests` count), V3CORE
  46. None is independently reviewed or native; registry status `CANDIDATE_ONLY`
  is correct at that grain.

## 7. Stale evidence text

The corrected JSON is 189 nodes / 431 edges and the test file has 9 tests
(8 negative mutations + 1 positive). The following stale text remains:

- `00_START_HERE.md:21,38` — 188 nodes / 414 edges.
- `03_RECOVERY_AND_FOUR_RETURN_ASSET_INDEX.md:12,153` — 17 S0–S16 “holds” and
  188/414.
- `05_VALIDATOR_AND_READBACK.md:39` — 188/414, seven-test suite, six mutations,
  and preserved old `VALIDATION_RESULTS.json`.
- `claim_epochs.s0_s16` — `R7_EXACT_HOLD` while the corrected S rows and
  `source_of_truth_basis` say `POST_SOURCE_CORRECTION`.

These are documentation/proof-epoch defects. They do not erase the source
correction, but they prevent treating the current package as a clean source of
truth.

## 8. Conclusion

The primary-source recovery is **real and exact**. The corrected validator passes
its current tests and detects the explicitly tested S0/S16/native/edge/Pyat
mutations. The whole-map substrate is **not yet acceptance-grade**:

- source fields for non-S rows are not bound to actual Git objects;
- three source paths do not resolve;
- five source blobs are null/tree, not exact file blobs;
- S5/S7/S11/S13/S14/S15 are not product-traversable outside generic governance;
- stale counts/test epochs remain in the package;
- current PRE-MAIN is one intake ahead of the candidate build cut.

Recommendation: `REVISE_PRECISE_DEFICIENCIES`, not `ACCEPT_SOURCEFREE_INDEX_SCOPED`
and not `HOLD_EXACT_SOURCE` (the S0–S16 primary source is present).
