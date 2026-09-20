# LAT2011_SOURCE_SPECIFIC_OWNER_V1 — Realization Contract

## 1. Purpose

`LAT2011_SOURCE_SPECIFIC_OWNER_V1` is the one candidate-neutral source-specific owner for later A/B/C processing of:

- file: `Latinobarometro 2011.sav`
- SHA-256: `a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e`
- Authority72 class: `L0_EXECUTION_PACKET_READY__NO_NAMED_DOCUMENTARY_BLOCKER`

This is the clean Latinobarometro baseline. It adds no source-specific machinery beyond what the accepted 2011 packet actually requires.

Physical carriers remain nonsemantic. Candidate A/B/C may differ in execution strategy, but none may construct an alternative 2011 semantic/source-authority surface.

## 2. Canonical source and replay identity

The canonical root is exact filename + SHA. Any SHA drift fails closed before semantic projection.

Replay identity is:

`SOURCE_SHA256 + PHYSICAL_ROW_ORDINAL`

The physical row ordinal supplied by the generic source-incidence/R35 layer must be preserved exactly. This contract does not renumber it or replace it with an interview identifier.

`NUMENTRE` and `(IDENPA, NUMENTRE)` are source-native attributes. The accepted Authority71 packet observed that `NUMENTRE` repeats globally and that the pair is injective in this exact snapshot, but injectivity is not semantic identity authority. Neither field nor pair may replace the hard replay key or create cross-release continuity.

## 3. Native reader boundary

The source is a governed native SAV source.

Required baseline configuration:

- `pyreadstat.read_sav`;
- `user_missing=True`;
- `apply_value_formats=False`;
- no source-specific encoding override;
- no automatic encoding guessing/fallback;
- compatibility decoding has no role in this source realization.

The Authority71 packet also preserves the ordinary SPSS header/dictionary baseline for this exact snapshot. This browser worker does not remeasure those physical facts and does not convert them into a whole-source qualification receipt.

## 4. Source-local variable identity

Every source variable is owned by:

`exact canonical source SHA + exact source variable name + physical variable ordinal`

Variable names are source-local. Name equality across Latinobarometro waves is not equivalence authority.

In particular, this realization does not import any 1995-to-2011 alias rule and does not allow the 47 exact-name collisions documented between 2011 and 2024 to create cross-wave semantic identity.

Any later harmonization is derivative work requiring its own authority and must not mutate the source-native owner surface.

## 5. Country coordinate

The accepted source-local country coordinate is `IDENPA`, documented as country of interview.

The accepted 2011 packet freezes exactly 18 source codes with counts totaling 20,204:

| IDENPA | Rows |
|---:|---:|
| 32 | 1200 |
| 68 | 1200 |
| 76 | 1204 |
| 152 | 1200 |
| 170 | 1200 |
| 188 | 1000 |
| 214 | 1000 |
| 218 | 1200 |
| 222 | 1000 |
| 320 | 1000 |
| 340 | 1000 |
| 484 | 1200 |
| 558 | 1000 |
| 591 | 1000 |
| 600 | 1200 |
| 604 | 1200 |
| 858 | 1200 |
| 862 | 1200 |

This is a source-local coordinate structure, not a family-wide country-code law. A/B/C may index it differently only if the raw code, row association, exact source scope, and R35 physical receipt remain identical.

## 6. Physical missing-state owner

The realization preserves the generic physical distinction among:

- `OBSERVED_STORAGE_VALUE`;
- `SYSTEM_MISSING`;
- `FORMAT_USER_MISSING_VALUE`;
- `FORMAT_USER_MISSING_RANGE`;
- any other governed generic physical missing state carried by the decoder.

For every cell, raw value, physical state, source missing declaration, row ordinal, variable ordinal, and variable name remain bound together.

No missing state is promoted by itself into refusal, don't-know, not-asked, route ineligibility, or other semantic meaning.

The accepted packet's `P1ST=-2` fixture is a layer-boundary witness: the released SAV/user-missing representation must survive even though the administered questionnaire prints a different instrument-layer code. The questionnaire does not rewrite the source storage layer, and the source storage layer does not rewrite the questionnaire.

## 7. WT carrier owner

`WT` is preserved as an exact source carrier and the official codebook identifies its documentary role as `Weighting`.

That fact authorizes neither:

- an automatic default weight;
- one universal 18-country target population;
- a pooled aggregate estimand;
- renormalization across countries;
- construction of a weight from another field;
- clipping or replacing the raw carrier.

The accepted methodology contains country-specific weighting/design descriptions. Those descriptions remain authority at their documented country scope. They do not silently compose into one universal aggregate estimand.

Therefore:

`WT present != aggregate estimand authorized`

and:

`WT present != default use authorized`.

Any later weighted analytical workload must bring the exact estimand/design/use authority it requires.

## 8. Documentary authority layers

The realization retains three source-native documentary surfaces without collapsing them:

1. 2011 questionnaire: administered wording, batteries, routing/instrument-layer response codes.
2. 2011 released-data codebook: released variable identities/storage-code semantics, `IDENPA`, `NUMENTRE`, `WT`.
3. 2011 methodology: country sample counts, coverage, sampling/design, country-specific weighting descriptions.

Where instrument and released-storage codes differ, both layers remain represented. One does not overwrite the other.

## 9. Cross-wave isolation

No Latinobarometro family analogy is semantic authority.

The following are explicitly foreign to this realization and must not be imported:

- 1995 Brazil 120-row release/methodology discrepancy;
- 1995 interview-ID special case;
- 2024 nominal-case-size 174 versus 332 physical-layout anomaly;
- 2024 WT published-domain conflict;
- 2024 P2ST/P13ST/P19ST semantic repurposing rules.

Likewise, the absence of these special hazards in 2011 is not authority to declare them absent in another wave.

## 10. S35/R35 binding

Applicable S35 edge classes are exactly:

`EC01; EC05; EC12; EC13`

They bind:

- exact format/source identity;
- multiclass physical missingness;
- weight/design carrier/domain preservation;
- source-local coordinate carriers.

R35 integration hooks are frozen for:

- I01 physical metadata;
- I02 derivative parentage if the future input is not the direct canonical raw root;
- I03 source physical scope, expectation, candidate realization and whole-source physical-equivalence receipt.

Required later physical dimensions include physical metadata, variable order, raw storage, missing declarations/states, row replay identity, reader configuration, coordinate carriers, and weight/design carriers.

These hooks have no semantic authority. This worker did not issue an I03 physical-equivalence receipt.

## 11. Candidate-neutral handoff

Later qualification order:

1. exact source identity freeze;
2. R35 source/reader/physical-equivalence receipt;
3. `LAT2011_SOURCE_SPECIFIC_OWNER_V1` identity freeze;
4. exact physical carrier-to-owner binding;
5. candidate A/B/C start;
6. common semantic/replay comparison.

All three candidates must consume the same source-specific realization identity.

Candidate-specific differences in native IDs, missing interpretation, country coordinate meaning, WT use, or imported cross-wave law are disqualifying even if some terminal values happen to match.

## 12. Claim boundary

Current state:

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

Not claimed:

- real source execution;
- remeasurement of accepted Authority71 fixtures;
- whole-source physical equivalence;
- candidate execution;
- I05;
- measured P2X;
- source certification beyond inherited authority.

The browser implementation is ready for a later A/B/C qualification court only after its physical prerequisites are supplied.
