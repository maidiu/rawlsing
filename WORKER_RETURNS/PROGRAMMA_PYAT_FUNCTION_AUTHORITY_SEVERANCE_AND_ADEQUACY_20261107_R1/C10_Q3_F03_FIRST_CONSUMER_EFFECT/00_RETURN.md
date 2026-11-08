# C10 Q3 F03 first-consumer effect

**Verdict:** `Q3_F03_TEST_TIME_REPLAY_OBSERVED__ORIGINAL_HISTORICAL_RUN_NOT_OBSERVED__Q4_CURRENT_GENERIC_OWNER_AND_BOUNDED_FQRA_PIN_PRESENT__FULL_F03_ADAPTER_AND_CURRENT_SELECTION_NOT_PROVED__NO_POSITIVE_SEVERANCE_FINDING__CURRENT_SELECTION_UNPROVED`

**Author cut:** `0d548b033a0a20c9738fa4a3412ba5acd01217c5`
**Write lease:** `C10_Q3_F03_FIRST_CONSUMER_EFFECT/` only.
**Test-time replay only:** the replay below exercises the unchanged historical
consumer now; it is not evidence that the original historical run occurred.

## Authority and module pins

| Item | Pin |
|---|---|
| AR-0005 full relation authority | `data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv` |
| AR-0005 SHA-256 / bytes | `0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13` / `47,874,248` |
| AR-0006 relation registry | `data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv` |
| AR-0006 SHA-256 / rows / bytes | `a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b` / `700` / `1,119,028` |
| Historical source cut | `9ba4764bef551b1ce498e5772d60b73d69337d4b` |
| FQRA module | `data/ddm_build_copy/ddm_v550_question_relation_authority.py` |
| Module SHA-256 / bytes | `2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c` / `38,858` |
| Actual entrypoint | `apply_question_relation_authority` (`:727`), with `load_question_relation_authority` (`:564`), `validate_active_universe` (`:861`) and `derive_legacy_latinobarometro_1995_residual` (`:441`) |

The exact AR-0005 and AR-0006 bytes were restored from the pinned historical Git
cut into a disposable replay root. The module's own `ROOT` resolved to that
disposable root, so its fixed full-authority and calibration paths were used;
no substantive reader or constant was monkeypatched.

## Observed historical consumer replay

### Full authority audit

`validate_active_universe` resolved all **18,518** authority rows:

| Resolver outcome | Rows |
|---|---:|
| `RESOLVED_CONTEXT_ONLY_AUTHORITY` | 12,611 |
| `RESOLVED_DIRECTIONAL_AUTHORITY` | 4,622 |
| `RESOLVED_ADMINISTRATIVE_AUTHORITY` | 952 |
| `RESOLVED_EXPLICIT_BLOCK` | 60 |
| `BLOCKED_EXCLUDED_ASIAN_W6` | 259 |
| `BLOCKED_AMBIGUOUS_AUTHORITY` | 14 |

`active_closed_35_waves()` returned **35** active source/wave scopes and
excluded Asian Barometer W6. The full authority has 36 source/wave pairs before
the W6 exclusion. The positive row observations below are a nine-source-family
sample, not a substitute for the full 35-wave audit.

### Positive first-consumer observations

For one actual positive row from each of the nine source families,
`apply_question_relation_authority` returned
`RESOLVED_DIRECTIONAL_AUTHORITY`, `GOVERNED_DIRECTIONAL`,
`semantic_role=RELATION_EVIDENCE`, and all six structural coordinates. Concrete
tokens and full output hashes are in `TRACE.jsonl` (`C10-F03-POS-01` through
`C10-F03-POS-09`). Example:

- Row: `QRA35V1::AFROBAROMETER::R1::demele` (`Afrobarometer`, `R1`, `LS`).
- Returned: `RESOLVED_DIRECTIONAL_AUTHORITY`; six coordinates; output hash
  `c511a6e88af9134178a5db690f61de627f20581f825e45a97e7abe0b7ffb7eb0`.

The other eight positive source families are Arab Barometer, Asian Barometer,
EVS, GSS, Latinobarómetro, LiTS, South Asia and WVS; their exact rows and output
hashes are in TRACE.

### AR-0006 residual consumer

`derive_legacy_latinobarometro_1995_residual` returned the expected **20**
Latinobarómetro `1995` rows. Residual CSV SHA-256:
`634d4a3edbe384c8c9c8122daf1381d8dbd0935d76fff4c1c0a8d77d6baa2774`.
This is the narrow AR-0006 residual use, not an all35 witness substitute.

## Negatives and restore

| Negative | Observed behavior |
|---|---|
| Actual explicit block row `QRA35V1::AFROBAROMETER::R1::pid` | `RESOLVED_EXPLICIT_BLOCK`; `semantic_role=UNKNOWN`; coordinates cleared; output hash `cee3ab67530d13d76a9eef3a4de396514df03bbe4b8c6a98048ab75931775b29` |
| Actual ambiguous row `LiTS III DURATION1` | `BLOCKED_AMBIGUOUS_AUTHORITY`; fail-closed; output hash `80736f70a5e7040c08b55cf6fc0846bce5b8c737af3ef3dd43c6f9444cd6a7f2` |
| Missing exact row (suffix-derived from an actual positive row) | `BLOCKED_MISSING_AUTHORITY`; `semantic_role=UNKNOWN`; coordinates cleared; output hash `13c9dbe3618058fbd7ae2adb8de73f9dba37dc22d40a877d0d34477465610f52` |
| Limited/wrong authority: AR-0006 700-row registry supplied for the full AR-0005 row | `BLOCKED_MISSING_AUTHORITY`; no full-scope directional promotion; output hash `40d0b122770874d40fd6aabde05fe1cee88b3737f81e5e61f14c9258d61f183b` |
| Missing authority file | `FileNotFoundError` observed; no fabricated success |

Cold restore: a second disposable root with the exact module and authority bytes
produced the same positive output hash
`c511a6e88af9134178a5db690f61de627f20581f825e45a97e7abe0b7ffb7eb0`. The
restored authority copy hash is
`0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`.

## Execution scope and limits

- This is an **unchanged historical consumer replay on nonrespondent authority
  metadata**. It is not an original historical invocation, original run
  manifest, respondent execution or current native/S3 operation.
- No respondent, SAV/DTA/DB or source microdata was read. No production module
  was executed and no current QREL/Q_USE implementation or engine was built.
  The current Q4 files were read-only hashed for pin identification.
- Downstream `ddm_v550_bridge.py:1008` and
  `compile_v551_relation_evidence_atoms.py:160-185` were **not** run. The exact
  remaining boundary is the V550 bridge/relation-atom downstream, not the
  authority-to-apply consumer observed here.
- The full audit covers all 18,518 authority rows and all 35 active waves; the
  nine positive observations are rows, not a substitute for all35 positive
  traces.

## Q4 current successor location and boundary

HQ correction under independent review ac8f10220dfbc489cd2d261d1d66e228f2bc2424
(C10R-01/02/03): the following are examined pins, not a completed whole-PRE-V3
functional responsibility map. An absent candidate filename does not establish a
missing function. F03 remains UNPROVED_CURRENT_SELECTION.

Exact current pins at author cut `0d548b0`:

| Current location | SHA-256 / status |
|---|---|
| `rawlsing_next/pre553_source_backed_c11_facade.py:268-356` `GovernedC11Projection` | `7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf` |
| `rawlsing_next/pre553_empirical_query.py:685-740` `execute_empirical_query` | `7cd7fd4f8ccf79cb07b037ef9cdda5e60ed3c3ba0631c9f4030d09f4d666be94` |
| `rawlsing_next/pre553_empirical_authority.py:114-133` `validate_authority_snapshot` | `c32b96cd67274d2bcb44ca509afd87e085748bd2e32565716c10313b0609a29a` |
| `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py:68,202-243,534-544` bounded FQRA-pinned coordinate materializer | `a88d623f0496d7f7d4291e91b33662b816fa20f17ca1c45a0c4ca6dc5198e402` |
| C6 candidate `rawlsing_next/pre553_historical_authority.py` | `ABSENT_AT_0d548b__C6_CANDIDATE_NOT_INSTALLED` |

The generic current consumers accept caller-supplied `AuthoritySnapshot`/
`AuthorityRegistry`; they do not demonstrate a current full FQRA adapter. The
bounded WVS7 materializer pins the exact FQRA SHA and the rule
`QRA35V1::WVS::W7::B_COUNTRY`, but its scope is `FROZEN_P2_ROUTING_ONLY`,
substantive evidence use is false, and it consumes one coordinate rather than
the full F03 relation authority. Its current execution is
`NOT_RUN__REQUIRES_WVS7_SOURCE/PHYSICAL_RESPONDENT_DATA`.

**Current adoption:** `CURRENT_GENERIC_AUTHORITY_OWNER_AND_BOUNDED_FQRA_PIN_PRESENT__FULL_F03_FQRA_ADAPTER_AND_CURRENT_SELECTION_NOT_PROVED__NO_POSITIVE_SEVERANCE_FINDING__CURRENT_SELECTION_UNPROVED`.

The historical selected input is present and the unchanged historical consumer
works on it. No positive severance finding is established; current selection
remains UNPROVED. Absence of a severance finding is not evidence of non-severance
or proof that the current consumer selects and enforces these inputs.
Current full-F03 selection/equivalence remains **unproved**, and the C7
checkpoint's `F03=UNPROVED_CURRENT_SELECTION` status is preserved.

## Distinct evidence layers

- **Historical selection:** C6 AR-0005/AR-0006 selected states and exact pins.
- **Historical runtime:** this test-time replay; original historical run remains
  `NOT_OBSERVED`.
- **Current adoption:** generic current authority owners plus one bounded
  FQRA-pinned WVS7 coordinate; no current full-F03 adapter/equivalence.

## Evidence files

- `TRACE.jsonl` — 19 concrete events: authority load, full audit, nine positive
  rows, explicit block, ambiguity, missing row, limited authority, missing file,
  cold restore, AR-0006 residual and Q4 current mapping.
- `scripts/replay_f03.py` — deterministic replay using the exact historical
  module and artifact bytes.
- `logs/replay_results.json` — detailed counts, selected rows, output hashes,
  negatives, restore and current pins.
- `logs/replay_stdout.txt` — build/run summary.

TRACE SHA-256: `53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184`.
