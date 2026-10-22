# R56-R02 r2 — normalized mapping collision repair — RETURN

**Disposition:** `ENGINEERING_REPAIR_COMPLETE__AUTHOR_NATIVE_PASS__R02V_AFFECTED_REQUALIFICATION_REQUIRED`
**Branch:** `agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`
**Exact repair parent/startup:** `236fd4d1064f7c14113616db300c955294a474ac`
**R02V source:** `a287674b97a2bbde4bf9acf3b6badf19b5ce72f5`
**Return root:** `WORKER_RETURNS/PYAT-R56-R02-OCCURRENCE-PROJECTION-REPAIR-R1/revisions/r2/`

## Startup/provenance

| Field | Recorded value |
|---|---|
| Role | R02 author repair (I2–I3/S3), not R02V acceptance |
| Native session | OpenCode `ses_e9dea5a24ffeBtsLScgC81lfet` |
| Harness / provider / model | OpenCode PID 17569 / `opencode-go` / `deepseek-v4.1-flash`, variant `max` |
| Effort / usage | `max` selected; provider-side effort and quota/usage UNKNOWN (not exposed) |
| Host | `MacBook-Pro.lan`, macOS 13.2.1 (22D68), x86_64 |
| Python / pytest / pyreadstat / pandas | 3.11.3 / 9.0.2 / 1.3.2 / 2.3.1 |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing/R56-R02-occurrence-projection-wt` |
| Duplicate writer | None found. Only this worktree has the branch; no other R02 writer process observed. Remote branch read back at `236fd4d1` before repair. |

**Provenance limitation:** this native session previously produced the R02V
review return at `a287`. It is now acting as the R02 author for this bounded
repair. The affected R02V requalification must therefore be performed in a
fresh native session on the R02V branch, not by reusing this session's
authorship as an independence claim. The repair itself does not claim to be
independent review.

## Required reads

Read at the exact supplied refs: R57
`953eb07ad29cc424b2fc43cfeb13ef83355f3a50`; shared execution contract
`eb28fdcc311e2534b66def445e745cb25cb8a9bd`; review shared rules
`485f31e52ca82905dcfbbc79c5f8c8294fb55f49`; frozen R00P R2 policy at
`6d95a78bf6b7bcf70022e303a151255e65edc38a` (read-only); R02V return at
`a287674b97a2bbde4bf9acf3b6badf19b5ce72f5`, including
`03_R02V_OPEN_CHALLENGE_ADJUDICATION.md`, both defect scripts/outputs and the
reviewer tests. No review branch merge; relevant tests were ported into the
author test file with source attribution.

## Repair

The adapter no longer builds the lossy `{token(k): str(v)}` lookup before
checking collisions. `GovernedRowOccurrencePlan.normalized_respondent_mapping()`
now:

1. admits source identity keys on the exact normalized token representation
   (bool/int/string/finite float; unsupported types and non-finite floats
   refuse);
2. admits scalar destination keys on their historical string form and refuses
   empty strings, None, bytes and containers;
3. checks duplicate normalized source keys and duplicate normalized destination
   keys on lists of admitted pairs;
4. only then constructs the lookup dictionary and proceeds to respondent/C11
   construction.

No literal `0`/`1` or fixed-character special case was added. The raw
exact-duplicate guard remains, but it is no longer the only guard. Production
changes are confined to `rawlsing_next/pre553_source_native_preimage_adapter.py`.

## Defect result

| Defect | New typed refusal | Regression | Status |
|---|---|---|---|
| D1 `{0:"1",1:1}` | `DUPLICATE_RESPONDENT_KEY_MAPPING`, detail `1` | reviewer test + author r2 collision cases | PASS |
| D2 `{0:"P0","0":"P1",1:"P2"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY`, detail `0` | reviewer test + author r2 collision cases | PASS |

No C11 release or I03 fact exists after either refusal. The validation runs
before respondent identity and release construction. Full matrix:
`01_DEFECT_REGRESSION_MATRIX.md`; executable receipt:
`evidence/r2_defect_resolution_receipt.json`.

Near-positive controls with integer, float and string source keys, row
permutation, and injective numeric/string destinations all preserve exact
source/respondent/occasion/value tuples and I03 `SUPPORTED` denominator 3.

## Qualification

| Run | Result | Evidence |
|---|---|---|
| Author 15 tests | 15 passed | `evidence/pytest_author15.log` / `.xml` |
| R02V reviewer 9 tests (7 positives + 2 defects), ported | 9 passed | `evidence/pytest_reviewer9.log` / `.xml` |
| Full focused file (15 + 11 r2 tests) | 26 passed | `evidence/pytest_full.log` / `.xml` |
| Retained facade + empirical-query | 42 passed | `evidence/pytest_retained.log` / `.xml` |
| Proof AST lint | PASS | `evidence/proof_lint.json` |
| Proof witness, 4 same-claim faults | PASS, target assertion RED, adapter restored | `evidence/proof_witness.json` |
| Defect resolution receipt | both refusals + near positives | `evidence/r2_defect_resolution_receipt.json` |

The ported reviewer suite includes the prospective source-derived I03 domain,
omission/remap/value fault with fresh-process restore, typed missingness,
S1/scalar, separate-unit S2 positive and cross-unit refusal, MR/rank/admin,
incomplete-order typed failure, and the two reviewer defect tests. The two
additional author r2 tests cover equivalent normalization collisions and
near-positive controls.

## Binding-envelope limitation

Unchanged and explicit: the transformed `NativePreimageBundle.physical_stream`
is compatible with the tested adapter -> unchanged facade/C11 -> unchanged I03
route only. It is not a raw `PhysicalCell` replacement for strict receiver APIs
(`authorized_banked_raw_value`, `fiabc_lm2_r1e_common_c11._cells`). No facade
or strict receiver was changed, and no general raw-compatibility claim is made.

## Engineering / science / authority

**Engineering:** repair complete at author grain; all required suites pass.
This is not independent acceptance.

**Science:** TEST_ONLY synthetic sourcefree only; no original source/respondent
data, original35, E_pre, F1–F8, actor, N11 or N12 issuance.

**Authority:** R56 narrow grant and R57 delegated technical seal; no production
adoption, protected CI, R00E gate, R03/compiler/lowering, R04.byte/R04.joined,
R05/R06, or original-science claim. J52/W52 remain USER_STOPPED. N11 NOT_READY;
N12 HOLD. R03/compiler/original science holds unchanged.

## Next step

Return the successor candidate to the SAME R02V owner for an affected
requalification pass. That pass must run in a fresh native session, verify the
remote successor SHA and this r2 return, reproduce the two original reviewer
defects as PASS/typed refusals, rerun the 7 independent positives, the 15 author
tests, the 42 retained tests, and the proof witness against the successor
candidate. No new investigator or policy court is requested.
