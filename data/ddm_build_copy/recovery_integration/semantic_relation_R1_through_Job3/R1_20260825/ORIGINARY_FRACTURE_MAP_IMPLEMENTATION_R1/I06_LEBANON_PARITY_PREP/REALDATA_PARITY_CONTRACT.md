# I06 REAL LEBANON FRACTURE-MAP PARITY CONTRACT R1

Status: `PREPARED__PRODUCTION_CONTROLLER_PARITY_NOT_EXECUTED_IN_I06`

Authority: `37_ORIGINARY_FRACTURE_MAP_FULL_JOIN_AND_IMPLEMENTATION_AUTHORITY.md` at commit `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`.

Frozen empirical oracle: exact L02 return `c9acd7e9ff887dd3a4a29d91f45688cb9c0705a3`.

This contract prepares the named real-data acceptance gate. It does **not** modify controller semantics and does **not** claim the integrated production controller has already passed.

## 1. Anti-leak theorem

The acceptance procedure is deliberately split into two phases.

### Phase A — answer-free controller execution

The controller may receive only:

- the exact Wave VIII source identity and source bytes supplied outside the repository;
- the exact questionnaire/codebook identities;
- the governed Q873 substantive multi-select surface and its source-native option/routing semantics;
- the source/universe/risk-set/weight authority;
- the governed positional-coordinate catalog and deterministic derived-coordinate definitions;
- Authority-37 Controller Law V1 and its explicit tunable thresholds;
- the required controller observation schema.

The committed `CONTROLLER_SEED.json` is the complete I06 seed. It is regenerated from the exact Library source/codebook and audited by `run_i06_lebanon_parity_harness.py`.

The seed MUST NOT contain L02 outcome answers, including any of the following:

- Lebanon's observed SES selection share or modal pattern;
- the corrected Wave-VIII routed SES share or the legacy 43.523% value;
- any country/denomination/income/predictor winner;
- any non-SES, MA+, no-formal, or deeper branch membership/support result;
- any response-pattern winner or full response-pattern census hash;
- any expected parity output.

The seed audit rejects forbidden answer-bearing key names and a bounded set of exact L02 answer literals. This is a guardrail, not the sole anti-cheat argument: the controlling rule is that the production controller receives only the committed seed/source authority surface.

### Phase B — post-execution oracle comparison

The controller observation and an independent replay observation are read and SHA-256 sealed **before the frozen L02 oracle is opened**. Their replay metadata must bind:

- the exact committed seed SHA-256;
- Authority-37 commit `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`;
- policy ref `Authority37_Controller_Law_V1`.

Only after those seals exist may `FROZEN_L02_PARITY_ORACLE.json` be loaded. Oracle values may then be used for acceptance comparison, never to create controller reachability.

`ORACLE_COMPARISON_AFTER_EXECUTION != ORACLE_GUIDANCE_DURING_DISCOVERY`

## 2. Frozen source authority

The controller observation must bind these exact source bytes:

| Source | SHA-256 |
|---|---|
| `ArabBarometer_WaveVIII_English_v3.sav` | `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998` |
| `ENG-Arab-Barometer-Wave-VIII-Questionnaire-RELEASE-FIN-NOV-2024-1.pdf` | `d72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb` |
| `Arab Barometer Wave 8 codebook.csv` | `328bbbbfa6cb8a78eacad52847b1432a56a81ec9ecfcd4f18754e05532afd4fc` |

The harness independently verifies all three hashes before generating/auditing the seed.

## 3. Governed Q873 surface supplied to the controller

Q873 is preserved as source-native multi-select 0/1 toggles. The seed supplies the source semantics for `Q873_1..Q873_13`, `Q873_98`, and `Q873_99`, but supplies no observed answer distribution.

Binding routing/denominator law:

- released analysis weight: `WT`;
- `Q873_8` is asked only for country codes 7, 8, 9;
- `Q873_10` is asked only for country codes 10, 21;
- routed structural missingness is not non-selection;
- substantive denominator: `Q873_1 nonmissing AND Q873_98 != 1 AND Q873_99 != 1`;
- `Q873_13` (`none_of_these`) is exclusive of other substantive selections.

The seed may specify Lebanon as the named exact universe (`COUNTRY=10`), because named source/universe authority is an input to this acceptance test. It may not specify what Lebanon's Q873 answers turn out to be.

## 4. Authority-37 controller policy supplied to the controller

The seed freezes policy, not outcomes:

- weighted support determines V1 modal ordering where positive weight authority exists;
- maximal ties remain multimodal unresolved rather than being forced to one winner;
- all lawful atomic categorical/boolean coordinate conditions remain reachable;
- normalized mutual information by target entropy is descriptive ranking only and does not prune reachability;
- branch roles are `CONFORMER`, `DEVIANT_EXIT`, `ALT_CONVERGER`, `ALT_MINORITY`;
- `minimum_split_raw_n=50`;
- `minimum_report_raw_n=25`;
- `maximum_depth=4`;
- stopped retained branches are not deleted;
- `maximum_target_arity_J=3`.

No L02 ranking result is in this policy surface.

## 5. Controller observation contract

The integrated controller (or a post-run adapter that cannot affect controller reachability) must emit one JSON object with schema:

`I06_CONTROLLER_OBSERVATION@1.0.0`

Required top-level surfaces:

- `source`
- `semantics`
- `routing`
- `branches`
- `determinicity`
- `response_pattern_census`
- `replay`

### Post-run normalization rule

I06 compares semantic results, not internal object names. A post-run acceptance adapter MAY map controller-native branch/object refs onto the frozen acceptance aliases only **after controller execution is complete**, using exact emitted predicates/ancestry. That mapping is a comparison projection and MUST NOT be fed back into discovery or reachability.

The acceptance aliases are:

- `LB_SES_SELECTED`
- `LB_NON_SES`
- `LB_EDU_NO_FORMAL`
- `LB_EDU_NO_FORMAL_NON_SES`
- `LB_EDU_MA_PLUS`
- `LB_EDU_MA_PLUS_NON_SES`
- `LB_EDU_MA_PLUS_NON_SES_NON_RELIGION`

Likewise determinicity target aliases are post-run comparison names, not seed hints.

## 6. Frozen parity comparisons

### 6.1 Routed Wave-VIII denominator correction

Exact checks include released rows, Q873 observed/routed rows, structurally missing Kuwait rows, DK/refusal counts, substantive denominator, and weighted denominator.

The corrected routed Wave-VIII weighted SES-selection share must match L02 within absolute tolerance `1e-9`.

The old `43.52302383575661%` value is frozen as a **forbidden legacy denominator artifact**, not an acceptable target. The observation must explicitly classify its disposition as `CORRECTED_DENOMINATOR_ARTIFACT`.

### 6.2 Lebanon root

The observation must reproduce the exact Lebanon Q873 substantive denominator and weighted denominator plus Lebanon weighted SES share within `1e-9`.

### 6.3 Exact multi-label morphology

The controller must preserve the exact Q873 response-pattern census, not merely item marginals or the modal row.

The post-run normalized census uses fields:

`branch_id, pattern_rank, response_pattern, n, weighted_n, unweighted_pct, weighted_pct, support_class`

with canonical LF CSV serialization in the emitted row order. The harness computes the hash itself; it does not trust a controller-supplied hash.

Frozen L02 census:

- data rows: `370`;
- canonical monolithic SHA-256: `8a642a5cf133843512d84b039af475f70c13b739f3e26908899193ccee886ed9`.

A modal-only or marginal-only output cannot pass this gate.

### 6.4 Lebanon SES/non-SES and support/stop behavior

The controller must independently discover and preserve the named root SES/non-SES morphology, then preserve the bounded no-formal/MA+ routes and support states required by the oracle.

This includes the distinction:

- retained + recursion eligible;
- retained exploratory + recursion stopped;
- retained underpowered + no split.

`STOP_RECURSION != DELETE_BRANCH` is part of parity.

### 6.5 MA+ non-SES alternative morphology

The MA+ non-SES branch must reproduce its bounded religion/nationality/none/region weighted distribution and the deeper non-religion retained exploratory distribution within `1e-9`.

These values exist only in the Phase-B frozen oracle.

### 6.6 Descriptive determinicity

For each frozen acceptance target, the controller must emit the complete expected predictor ordering and normalized-MI values. Predictor identity/order is exact; NMI absolute tolerance is `1e-12`.

This checks descriptive determinicity parity while preserving Authority 37's law:

`DESCRIPTIVE_RANK != EXCLUSIVE_SEMANTIC_WINNER`

A ranking match never proves causality or actor/personality semantics.

### 6.7 Source/routing/weight semantics

Exact semantic checks include:

- Q873 multi-select form;
- exact substantive-denominator rule;
- `WT` weight identity;
- Lebanon Q873 tribe structural missingness;
- Lebanon Q873 sexual-orientation routing availability;
- zero Lebanon `none_of_these` exclusivity violations;
- explicit disposition of the legacy denominator artifact.

### 6.8 Deterministic replay

Two independent production observations from the same exact source, seed, authority and controller build must be supplied.

I06 requires equality of the oracle-independent parity projection containing source, semantics, routing, branches, determinicity, response-pattern census, and replay binding refs. Physical/log metadata outside that projection may differ.

## 7. Required production execution protocol

After integration, a production acceptance runner must follow this order:

1. materialize/verify exact source files;
2. run `prepare` or `audit-seed` against the committed seed;
3. invoke the integrated production controller using only the exact source authority + `CONTROLLER_SEED.json`;
4. save controller observation A;
5. repeat the identical controller execution independently and save observation B;
6. do not provide the L02 oracle path/content to either controller invocation;
7. invoke I06 `compare`, which seals A/B and seed before loading the frozen oracle;
8. require every comparator check to pass and retain the generated parity receipt.

Example comparator invocation after controller integration:

```bash
python run_i06_lebanon_parity_harness.py compare \
  --seed CONTROLLER_SEED.json \
  --observation controller_observation_A.json \
  --replay-observation controller_observation_B.json \
  --oracle FROZEN_L02_PARITY_ORACLE.json \
  --receipt production_parity_receipt.json
```

## 8. Prep-lane pass condition

I06 preparation itself passes when:

- exact source hashes are verified from Library;
- seed regeneration is deterministic;
- committed seed equals regenerated source/authority seed;
- answer-leak injection is rejected;
- oracle is source-bound and schema-valid;
- incomplete/fabricated observations fail closed;
- the harness is syntactically valid and its committed artifacts are hash sealed;
- no raw survey bytes or production controller changes are committed.

This is **not** the same as the later production parity pass.

`HARNESS_PREP_PASS != PRODUCTION_CONTROLLER_PARITY_PASS`
