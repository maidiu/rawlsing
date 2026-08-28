# L03 BRANCH-SPECIFIC SAME-RESPONDENT CO-SIGNATURE REAL-DATA COURT R1 — RESULT

Status: `L03_BRANCH_COSIGNATURE_REALDATA_R1_COMPLETE`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-fracturemap-l03-cosignature-realdata-r1`

Verified starting HEAD: `ea40d252401f789982d2b94dab26fefbba5042cb`

Scope: sibling-blind documentary + exact real-data court only. No production mutation. No architecture ranking. No actor belief/personality inference.

## Holding

The originary Rawlsing requirement for **branch-conditioned same-respondent co-signature / attitude cotravel** is supported on exact Arab Barometer Wave VIII Lebanon respondent data.

Terminal holding:

`BRANCH_CONDITIONED_SAME_RESPONDENT_COSIGNATURE_REALDATA_PROVED__PAIRWISE_ONLY_NOT_INFORMATION_EQUIVALENT__PREDICTORS_REMAIN_NON_ATTITUDE`

`NO_REALDATA_CASE_PROVED` does not apply.

## Exact source and branch

Primary source: `ArabBarometer_WaveVIII_English_v3.sav`

SHA-256: `a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998`

The exact replay script directly decodes the SPSS byte-compressed source without `pyreadstat` or an intermediate empirical carrier. Verified geometry:

- layout code `2`
- nominal case size `692` eight-byte storage slots
- compression `1`
- declared and decoded cases `15,627`
- bias `100.0`
- data offset `176,848`
- retained numeric variables `688`
- decoder final byte `12,275,728`, exactly equal to source size

The codebook maps `COUNTRY=10` to Lebanon. Lebanon has `2,403` unique respondent IDs.

Court branch:

`COUNTRY == 10 AND Q873_1 == 1`

Q873 is multi-select; option 1 is `Socioeconomic class`. Therefore branch membership means only that the respondent selected socioeconomic class as **one perceived basis of discrimination**. It is not objective socioeconomic class and not an actor identity.

Counts:

- Lebanon: `2403`
- branch: `1334`
- complement `Q873_1 == 0`: `1069`
- raw branch share: `0.5551394091`

Sorted respondent-ID SHA-256 receipts:

- Lebanon: `a6eddf236aa11073caa813a79a92a02fa74068c85176afc03f495e3be6735e7a`
- branch: `ee6d4b46cdfc6dbcab7acc3673231517283fed65aabdbf9bfa2e43b6c65f3d50`
- complement: `cc0ca1d852d94445130843bb3d18bc3f03ff211795b35d76fc3b800b29c92184`

## Branch-conditioned marginal morphology

A bounded nine-question screen spans discrimination policy, governance/democracy, religion/state and gender-role responses. `WT` is used only for descriptive marginals; `98/99` DK/refusal are excluded, while substantive `Q885=97` remains substantive.

Branch-versus-complement weighted total-variation distances:

| Question | TV |
|---|---:|
| Q885 | 0.198029 |
| Q605 | 0.138514 |
| Q533_4 | 0.114938 |
| Q511 | 0.113687 |
| Q601_3 | 0.111663 |
| Q512 | 0.108686 |
| Q601_4 | 0.100159 |
| Q606_2 | 0.092804 |
| Q606_4 | 0.085119 |

All nine distributions are in `REALDATA_BRANCH_COSIGNATURE_ORACLE.csv`.

Demographic cohorts are retained only as predictors/conditioners: women (`n=1191`), age 18–29 (`n=599`), no formal education (`n=46`), and MA+ (`n=162`). The oracle records their branch prevalence and selected response-distribution contrasts. They are not attitude nodes or matched causal controls.

## Branch-specific same-respondent relation

A clean cross-domain case is `Q606_4 × Q867B`:

- branch: `n=1208`, raw complete-case Cramér's V `0.1768354317`
- Lebanon overall: `n=2181`, V `0.1166404038`
- complement: `n=973`, V `0.0543498407`

The relation is therefore not invariant to branch conditioning. A whole-universe relation cannot substitute for branch-conditioned same-respondent evidence.

The matrix also retains additional pairs, including:

- `Q511 × Q601_4`: branch `0.268235`, overall `0.197627`, complement `0.141585`
- `Q201A_1 × Q601_4`: branch `0.094104`, overall `0.148773`, complement `0.240020`
- `Q512 × Q631`: branch `0.286099`, overall `0.212068`, complement `0.168413`

No causal interpretation is attached to these descriptive relations.

## Pairwise-only information loss proved on real data

Primary three-way configuration:

`Q201A_3 × Q606_2 × Q606_8`

For each scope, iterative proportional fitting constructs the maximum-entropy/no-three-way table reproducing **all three observed pairwise margins**.

Branch (`n=1265`):

- maximum pairwise-margin error `4.55e-13`
- observed-vs-pairwise-model three-way joint TV `0.0839505583`
- `G²=87.32678819`, `df=27`
- diagnostic `p=2.79842299e-08`
- largest residual cell `(4,4,1)`: observed `204`, expected `224.1389789`

Complement (`n=1004`):

- maximum pairwise-margin error `1.71e-13`
- joint TV `0.0440333882`
- `G²=29.90147538`, `df=27`
- diagnostic `p=0.318598906`

The p-values are diagnostics only; this court creates no significance threshold. The information result is direct: **exactly reproducing every pairwise margin does not reproduce the observed three-way joint**. Pairwise summaries are therefore not information-equivalent to the branch-conditioned k-way workload.

Two corroborating real three-way cases are also in `PAIRWISE_VS_BRANCH_CONDITIONED_MATRIX.csv`.

## Required co-signature grain

Semantic parity requires exact same-respondent incidence or a positively proved information-equivalent carrier sufficient to replay authorized branch-conditioned pair/k-way joints. The capability must preserve or regenerate exact source/wave/universe identity, respondent identity, branch predicate and membership receipt, predictor/conditioner role separate from response-node role, source-native response semantics and typed special states, per-node and joint denominators, raw pair/k-way tuple counts or equivalent incidence, weighting authority where used, minority/higher-order configurations, deterministic provenance/replay, and the PRE-V3 noninference ceiling.

`OBJECT_GRAIN_AND_REPLAY_REQUIREMENTS.csv` gives the machine-readable requirement ledger.

## Replay

`run_l03_cosignature_realdata.py` is the exact replay script. Script SHA-256:

`4887d3f9405f1d3b0a69a14a6d6a64ce084b2158a738fe6fe4a2f7a6d03432fd`

It verifies source hashes and SAV geometry, direct-decodes all cases, reconstructs exact Lebanon and Q873_1 membership, executes the bounded marginal and predictor screens, five pairwise branch/parent/complement relations, and three pairwise-margin-preserving higher-order tests, then writes both real-data matrices with deterministic LF line endings.

## Negative ceiling

This court establishes no causation, individual belief/personality/ideology, universal support threshold, semantic meaning for every observed association, architecture winner, or production implementation.

Success token:

`L03_BRANCH_COSIGNATURE_REALDATA_R1_COMPLETE`
