# I06 REAL LEBANON FRACTURE-MAP PARITY HARNESS PREP R1 — RESULT

Status: `I06_LEBANON_PARITY_PREP_R1_COMPLETE`

Worker branch: `agent/verkhovod-fracturemap-i06-lebanon-parity-prep-r1`

Verified starting HEAD: `1f19084bf3c2c5e92cdc3faaa8e61ffcaf483c23`

Authority: Authority 37 at `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`.

Frozen real-data oracle: exact L02 return `c9acd7e9ff887dd3a4a29d91f45688cb9c0705a3`.

## Holding

I06 has prepared a deterministic, fail-closed real Lebanon parity harness that can test the integrated Authority-37 fracture-map controller against the frozen L02 oracle **without supplying L02 answers to controller reachability**.

The preparation gate passes.

The integrated production controller itself was **not executed in this worker**, so I06 does not claim production parity has already passed.

`HARNESS_PREP_PASS != PRODUCTION_CONTROLLER_PARITY_PASS`

## Anti-leak construction

The harness has two physically ordered phases.

### Phase A — answer-free seed/controller phase

`CONTROLLER_SEED.json` contains only:

- exact source/wave/universe identity;
- governed Q873 source-native multi-select semantics;
- exact routing/denominator/weight authority;
- governed coordinate catalog and deterministic helper-coordinate definitions;
- Authority-37 Controller Law V1 policy;
- required observation shape.

It contains no Lebanon result, no routed SES answer, no non-SES/MA+/no-formal route answer, no determinicity winner/value, no branch support, no response-pattern winner, no L02 oracle commit and no full pattern oracle hash.

`run_i06_lebanon_parity_harness.py` regenerates the seed from the real Library source/codebook, verifies source hashes, and audits the seed for forbidden outcome-bearing keys/literals.

Committed seed SHA-256:

`454b858e8f9677419fd6e386feb7cd06e9115788d8a5e87deee7d76f1c271f36`

### Phase B — sealed post-execution comparison

The comparator reads and SHA-seals controller observation A, controller replay observation B, and the exact answer-free seed before opening the frozen oracle.

Both observations must bind:

- the exact seed SHA;
- Authority-37 commit;
- `Authority37_Controller_Law_V1`.

Only then does the comparator load `FROZEN_L02_PARITY_ORACLE.json`.

This prevents a correct-looking observation from an unbound/oracle-informed run from passing merely because its numbers match.

## Exact Library source verification

The required Library sources were materialized read-only and independently SHA-256 verified:

| Source | SHA-256 |
|---|---|
| `ArabBarometer_WaveVIII_English_v3.sav` | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` |
| Wave VIII questionnaire | `d72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb` |
| Wave VIII codebook | `328bbbbfa6cb8a78eacad52847b1432a56a81ec9ecfcd4f18754e05532afd4fc` |

No Library source was mutated and no raw survey bytes are committed.

## Frozen parity surface

`FROZEN_L02_PARITY_ORACLE.json` freezes only the bounded answer surface required by I06. It includes:

1. routed Wave-VIII denominator/missingness and corrected weighted SES share;
2. Lebanon substantive denominator and weighted SES share;
3. exact full multi-label response-pattern census by row count + canonical content hash;
4. Lebanon SES/non-SES branch support;
5. no-formal and MA+ support/retention/stop behavior;
6. MA+ non-SES alternative response distribution;
7. bounded descriptive normalized-MI orderings/values;
8. exact source/routing/weight semantic checks;
9. tolerances.

Frozen oracle SHA-256:

`856001d87bab197a4d09a3bdab3e356141c26d8021e2d86ceedc66eefd6e37fe`

The comparator specifically rejects the old `43.52302383575661%` Wave-VIII value as a corrected-denominator artifact by requiring the exact L02 disposition and the routed `47.287269199071936%` target.

## Exact multi-label morphology check

The oracle does not need to inject the 370 response-pattern rows into controller execution.

After controller execution, the observation must expose the complete post-run normalized pattern census. The harness independently serializes those rows with the frozen field order and LF line endings and computes SHA-256 itself.

Required census:

- rows: `370`
- canonical SHA-256: `8a642a5cf133843512d84b039af475f70c13b739f3e26908899193ccee886ed9`

A modal-only or marginal-only result therefore cannot pass.

## Determinicity parity

The frozen acceptance oracle compares full bounded predictor ordering and normalized-MI values for:

- Wave-VIII SES selection;
- Lebanon SES selection;
- Lebanon non-SES religion selection;
- Lebanon MA+ non-SES religion selection.

Predictor order is exact; normalized MI tolerance is `1e-12`.

This remains descriptive only and cannot control reachability or imply causality/personality.

## Support/stop parity

The oracle preserves Authority-37/L02 support distinctions:

- `n >= 50`: supported and potentially recursion eligible under remaining positive authority;
- `25 <= n < 50`: retained exploratory, recursion stopped;
- `n < 25`: retained underpowered, no recursive split.

The frozen named cases include both no-formal and MA+ paths, including the MA+ non-SES non-religion `n=42` exploratory retained stop and the no-formal non-SES `n=12` underpowered retained stop.

## Self-test result

Fresh-process verification passed:

- Python syntax compile;
- exact source hash verification;
- deterministic seed regeneration;
- byte-identical regenerated/committed seed;
- anti-leak injected-answer rejection;
- oracle schema/source binding;
- fail-closed incomplete-observation comparison;
- observation/replay seed+authority pre-oracle binding.

A deliberately incomplete controller observation produced exit code `2` and a `FAIL` receipt with 127 failed checks. There is no false-positive path through missing data.

Exact details are in `TEST_RECEIPT.txt`.

## Prepared artifacts

- `CONTROLLER_SEED.json`
- `FROZEN_L02_PARITY_ORACLE.json`
- `run_i06_lebanon_parity_harness.py`
- `REALDATA_PARITY_CONTRACT.md`
- `SOURCE_SHA_LEDGER.csv`
- `TEST_RECEIPT.txt`
- `RESULT.md`
- `RESULT.json`
- `CHANGED_FILES.txt`

No production code is changed.

## Production handoff

After the integrated controller is available, the acceptance runner must:

1. run the controller twice independently from the exact seed/source authority only;
2. save both observations;
3. keep the L02 oracle unavailable to controller execution;
4. run I06 compare mode;
5. require every parity and replay check to pass;
6. retain the generated parity receipt for HQ.

Success token:

`I06_LEBANON_PARITY_PREP_R1_COMPLETE`
