# L02 RESULT — REAL ARAB BAROMETER VIII LEBANON FRACTURE-MAP R1

Status: `PASS__REAL_SOURCE_RECONSTRUCTED__ORACLE_FROZEN`

Branch: `agent/verkhovod-fracturemap-l02-lebanon-realdata-r1`  
Exact start: `066519ead239dcde3328248b8420b59d2db6c7a9`

## Holding

The real Wave VIII source supports the Lebanon fracture-map exemplar and reproduces nearly all remembered Lebanon percentages exactly to rounding. It also exposes one important upstream denominator error: the remembered **Wave-VIII SES share of about 43.5% is not a valid source-routed Q873 estimate**.

With Q873 routing respected and don't-know/refusal removed, the Wave-VIII weighted SES-selected share is **47.2873%** (`n=14,024`, weighted `n=13,990.2832`). The remembered **43.5230%** is reproduced only by retaining Kuwait's `1,210` structurally missing Q873 rows in the denominator and treating their missing SES toggle as non-selection. That denominator construction is rejected by this oracle.

Lebanon itself is unaffected by that routing issue. Among source-routed substantive Lebanese respondents (`n=2,339`, weighted `n=2,334.6956`), SES is selected by **57.4608%** weighted (**57.0329%** unweighted), confirming the remembered ~57.5% claim.

## Lebanon overall / fracture structure

Q873 is genuinely multi-select. In Lebanon the weighted selected-response distribution begins:

- socioeconomic class: **57.4608%**
- religion: **43.6151%**
- nationality: **28.9659%**
- region: **27.7265%**
- skin color: **20.4227%**
- race/ethnicity: **15.0299%**
- none of these: **13.0178%**
- gender: **11.1955%**
- disability: **11.0035%**

The response-pattern oracle confirms why selection presence cannot be collapsed into exclusive categories. The largest exact same-respondent patterns include **SES only 18.9613%**, **none only 13.0178%**, **religion only 5.8154%**, and **SES + religion 5.6781%**. There are 230 distinct applicable Lebanon response patterns; option-13 exclusivity has zero violations.

The Lebanon SES-selected branch has `n=1,334` (weighted `n=1,341.5350`). The non-SES branch has `n=1,005` (weighted `n=993.1606`). Within non-SES, weighted alternative presence is religion **35.9982%**, none **30.6020%**, nationality **21.7652%**, region **21.4907%**, and skin color **15.5282%**.

## Education exemplar replication

The old education points reproduce from source:

- no formal education: SES **74.5259%**, `n=45`, weighted `n=44.6147`;
- preparatory/basic: SES **61.4950%**, `n=485`, weighted `n=445.2554`;
- BA: SES **54.1926%**, `n=455`, weighted `n=493.3215`;
- MA+: SES **54.0547%**, `n=156`, weighted `n=165.8209`.

The no-formal branch is only `n=45`, so it is exploratory. Its non-SES child is **n=12** (weighted `n=11.3652`) and therefore hard-stops under the originary support law. Its distribution nevertheless reproduces the remembered direction: religion **34.4330%**, none **26.1168%**, nationality **21.9823%**, region **18.0835%**. After also conditioning out religion, only **n=8** remain; none is **39.8322%**, region **27.5802%**, nationality and skin **13.8104%** each, migration **12.1618%**. **No stable splitter ranking is accepted for either tiny branch.**

The MA+ branch is substantially better supported. Among MA+ non-SES respondents (`n=72`, weighted `n=76.1869`), religion is **40.4338%**, nationality **32.2467%**, none **27.3821%**, and region **23.1242%**. After also conditioning out religion, `n=42` (weighted `n=45.3817`) remain, so the branch is exploratory-only: none **45.9692%**, nationality **22.3129%**, skin **12.8205%**, migration **11.4806%**, region **7.1981%**.

## Descriptive determinicity

The frozen determinicity oracle is deliberately association-only.

For Wave-VIII SES selection, **country** is the strongest tested splitter (normalized weighted MI `0.06220`), far ahead of household financial situation (`0.00863`), country-local income rank (`0.00546`), religiosity (`0.00402`), and education (`0.00287`). This source-backed result supports the originary claim that country fractures the modal SES response.

Within Lebanon, SES selection is most distinguished in this tested set by country-local income rank (`0.02866`), followed by combined denomination (`0.01220`) and household financial situation (`0.00941`). Within Lebanon's non-SES branch, religion selection is most associated with combined denomination (`0.02985`), while nationality selection is most associated with education (`0.02679`). None-of-these selection is most associated with combined denomination in the tested set; exact rankings and complete-case support are frozen in `BRANCH_DETERMINICITY_ORACLE.csv`.

For **MA+ non-SES religion selection**, combined denomination ranks first (`normalized MI=0.13074`), ahead of household financial situation (`0.05830`) and income-rank quintile (`0.05598`). This reproduces the old “denomination strongest” signal as a **descriptive branch association**, not a causal or actor-level claim. The MA+ non-SES/non-religion residual has only `n=42`; its determinicity rows are therefore explicitly `EXPLORATORY_ONLY`.

## Acceptance oracle

The committed replay pipeline is `analyze_lebanon_fracture_map.py -> normalize_and_shard_oracles.py`. The second script is serialization-only: it canonicalizes CSV newlines to LF and converts the full response-pattern monolith to the repository sharded form without changing any empirical row. Two fresh executions of this exact two-step pipeline were byte-identical.

The committed CSVs freeze:

- `RESPONSE_PATTERN_ORACLE.csv` is a hash-sealed manifest over eight full census shards (`RESPONSE_PATTERN_ORACLE_PART_01.csv` through `_08.csv`). Concatenating shard data rows beneath one header reconstructs all 370 replay rows with canonical monolithic SHA-256 `8a642a5cf133843512d84b039af475f70c13b739f3e26908899193ccee886ed9`; no row is omitted.
- branch definitions, support, weights, and alternative-response presence;
- exact same-respondent multi-label patterns;
- descriptive branch determinicity profiles;
- routing/missingness/support ledger;
- claim-by-claim replication/correction against the originary exemplar.

These are suitable as a named real-data oracle for later autonomous-discovery tests. They do **not** select an architecture, modify production Rawlsing, infer personas, or assign substantive meaning to residual/none categories.

## Noninterference

- No sibling findings consumed.
- No production Rawlsing files modified.
- No V3/persona/actor inference.
- No A/B/C or physical-architecture judgment.
- Mandatory Library sources were read only.

`L02_LEBANON_WAVEVIII_FRACTURE_MAP_REALDATA_R1_COMPLETE`
