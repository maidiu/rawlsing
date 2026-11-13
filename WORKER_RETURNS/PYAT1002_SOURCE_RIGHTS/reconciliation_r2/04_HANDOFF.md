# PYAT1002 R2 — historical grant reconciliation handoff

**Contract:** `PYAT1002-HISTORICAL-GRANT-RECONCILIATION-R2`
**Prior return:** `58ee21134730eb0afaa48842647d568e63c884b8`
**Branch:** `agent/pyat1002-source-steward-r1`
**Correction scope:** `SRC04` and `SRC17` historical grants and actual positives only; other 33 rows preserved
**R2 source opens / reads / hashes / native executions:** `0 / 0 / 0 / 0`
**New grants minted:** `0`
**Integration:** `UNMERGED`
**Self-acceptance:** none

## Result in one paragraph

The prior return's core omission is corrected. The earlier search of the R157
fixture cut correctly found no source-use grant **in that cut**, but later actual
source-native campaigns are locally present and directly relevant. SRC04 has
human user operational grants for full source read/C11 construction and
observed-response empirical use, an actual accepted-scoped C11 release, and a
partial actual empirical execution. SRC17 has a True-HQ D1/D2 source-read/C11
grant and an actual independently reviewed C11 release. Those grants and
positives are now recorded separately from the R157 nonrespondent fixtures. No
new permission was minted, and no source was opened in this correction.

## Engineering court

`PASS` for the bounded factual reconciliation.

- Corrected 35-row matrix: `35_row_source_rights_matrix.json` / `.csv`.
- SRC04/SRC17 grant and positive provenance map:
  `01_HISTORICAL_GRANT_PROVENANCE_MAP.json`.
- RED→corrected proof: `02_RED_TO_CORRECTED_ACCOUNTING.md`.
- One Browser High decision: `03_ONE_BROWSER_HIGH_DECISION.md`.
- Other 33 row metadata is unchanged; canonical digest before/after is
  identical (`411fe181…`).
- Prior nine return files are frozen and hash-preserved.
- No product/test/other-worker/accepted-code write.
- No source bytes opened, read, decoded or hashed in R2.

## Scientific court

The historical actual positives are reported at their exact scopes; R2 reran
none of them.

### SRC04

- Actual source read and C11 release:
  `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`.
- Independently reviewed `PASS_SCOPED_ORIGINAL_SRC04_RELEASE` at
  `e21f28f2657027bfde37d27e5fe5dad2f7fd3908`.
- Accepted scoped at `ba41253681212be14a0cde009afb99d77e14935e`.
- 7,337 rows; 177 selected response fields + 3 coordinates; 1,298,649 response
  positions; q217 held at exactly 38 source-unbound cells.
- Actual original empirical execution is **partial**: 208 operations (177 unary
  + 31 joint), 0 refused, 4,427 aggregate cells. The full 15,546-operation
  frontier was stopped on scale, not rights; no full-success or full-workload
  claim. No independent G5 for the partial empirical frontier was located.
- Its R157 nonrespondent fixture is separate and is not counted as actual.

### SRC17

- Actual source read and C11 release:
  `2f81b527ba1a62ecb79c7cc858063d60a10826a91af7d689606ed83e6bbd039e`.
- Independently reviewed `PASS` at
  `24f2f3f22f05ed1f0d71dbdf61dbab62d7269358`, grade
  `SOURCE_NATIVE_C11_POSITIVE_QUALIFIED_WITH_RECORDED_HISTORICAL_PROCESS_DEVIATION`.
- 1,504 rows; 258 selected response fields; 21 held response slots; 2
  coordinates; 339/339 physical slots accounted.
- The review records a pre-admission `ls -la` metadata listing; no source bytes
  were read/hashed outside admission and no material effect was observed.
- The D2 grant explicitly does **not** authorize SRC17 I03/I05, population,
  canonical, weights or additional source reads.
- Its R157 nonrespondent fixture is separate and is not counted as actual.

## Authority court

`PARTIAL / HOLD_FOR_ONE_BROWSER_DECISION`.

The corrected register is:

| Decision | Count |
|---|---:|
| `AUTHORIZED_FOR_THIS_HOST_PURPOSE` | 2 (`SRC04`, `SRC17`) |
| `UNKNOWN_OWNER_DECISION` | 33 |
| `DENIED` | 0 |
| `EXPIRED` | 0 |
| `NOT_LOCATED` | 0 |

The two authorized rows have different scopes:

- **SRC04:** source read + C11 + observed-response statistic/source-local I03
  consumer. No eligible-risk, population/weight, canonical/signed direction,
  causal, structural or FieldForge authority. The full pairwise frontier is a
  scale/architecture blocker, not a rights blocker.
- **SRC17:** source read + C11 construction only. I03/I05 are explicitly not
  authorized; 21 response slots remain held.

Four layers are kept separate:

1. **User operational read authorization:** present for both (SRC04 human user,
   SRC17 True-HQ D1/D2 disposition with user/source decision refs).
2. **Documented dataset licence/rights:** no separate dataset-owner licence
   located in the read set. A user operational grant is not relabelled as a
   publisher licence.
3. **Scientific issuer/claim authority:** SRC04 observed-response statistic
   only; SRC17 C11 construction only.
4. **Runtime resolver representation:** SRC04 uses campaign-specific grant
   schemas; SRC17 `GRANT_AUTHENTICATION` carries request and user/source decision
   refs. Schema/field mismatch is not evidence that the human authorization
   never existed.

No expiry was inferred from age. No revocation was invented. The actual grants
state `CURRENT_GRANTED`; SRC04 and SRC17 record `revocation: NONE_RECORDED`;
SRC17 has the exact effective interval
`2026-10-27/TRUE_HQ_D1_D2_PINNED_CONTROL_3b703e8`.

## The prior proposal is withdrawn

The prior return's proposed new SRC04 decision — new host
`RAWLSING_LOCAL_DARWIN_SOURCE_HOST`, new purpose string, 30-day retention — was
a worker proposal, not required source-owner terms. It is **withdrawn** because
exact SRC04 grants already exist. R2 does not reuse or rename those proposed
fields as permission.

## One unresolved decision

The smallest remaining authority/scope question is in
`03_ONE_BROWSER_HIGH_DECISION.md`:

> Does the exact existing human/True-HQ operational authorization satisfy
> 1002's required "existing competent current source right" for the intended
> source-native first-read, without a separate documented dataset-owner licence?
>
> Choose:
> - **A.** Yes, sufficient for the exact existing scopes (SRC04 observed-response
>   statistic; SRC17 C11 construction only, I03/I05 still excluded).
> - **B.** No, a separate dataset-owner licence is required; name the exact
>   missing licence/owner.
> - **C.** Partial: operational authorization suffices for source read/C11 but
>   the 1002 U/Epre/first-I03 step needs a separate scientific issuer; name the
>   exact issuer/scope.

This is not a request for a new generic source grant, a new publisher signature,
new paid data, new web scraping or new scientific scope. It is a precise
authority/scope decision for Browser High.

## Prior-return preservation

The prior nine return files remain byte-identical at their `58ee2113` hashes:

| File | SHA-256 |
|---|---|
| `00_HANDOFF.md` | `4e0d1b630c559238f9ce4ff05ca97ab6953c42f6694fad73f9fcc58244388bf6` |
| `01_SOURCE_METADATA_CENSUS.md` | `972f44cd1152f111162fe66e4d4a2a0d9fb6d8caad70aaedfcfb2517d233503b` |
| `02_PERMISSION_PROOF_SEARCH.md` | `3af3db3180ba54c7a224f5ea2e1d25c3035a5864ac9c3bd39b9c367444056829` |
| `03_HISTORICAL_SRC04_SRC17.md` | `77be5fb6c9fc82baa81d571ea90abd69bab7ee89f30011101a7e304ea69e1b71` |
| `04_ONE_HIGHEST_IMPACT_GRANT.md` | `c56fc52942ad59756aba69ea5f3ca06309a1b124c1c9fbb4067456a465ad93c9` |
| `05_NATIVE_SOURCE_HOLD_AND_GATES.md` | `5576cfad92c2e682bd832d8f0356c2ee69504db4b6f15446422ada64ba4170c3` |
| `35_row_source_rights_matrix.json` | `03116d64152abe1b7cd67cdfe639fe0de0c35c811c228bafe20aad292fe65907` |
| `35_row_source_rights_matrix.csv` | `9cb8507633cdf3bf87b449c36e4b63b8658afa286a79eb63a31c067fbe003b08` |
| `receipt.json` | `761e1c33f6fc22271090b3b1ab80032c5b030ff787ae70216df883a77fd825bf` |

Canonical digest of the other 33 rows:
`411fe181a00a2b54d507b2cfd050d2a96248e32fd1ecfad4f7da7d18ae059a67`
before and after.

## What was not done

- No respondent source open, read, decode, hash or native execution in R2.
- No U/Epre execution, I02 persistence or first I03 fact in R2.
- No new source grant, licence, issuer, host or purpose.
- No model/provider/account/effort/region/harness/VM change.
- No protected merge, production CURRENT, original35 science issuance, W03/W04
  restart or accepted packet court reopened.
- No old evidence edited; no existing test weakened; no test added.
- No public respondent cells, member lists, IDs or credentials.
- No self-acceptance or automatic G5.

## Next indispensable dependency

The one Browser High decision above. If A is chosen, the next lawful action is
within the exact existing grant scopes; if B/C, the exact missing authority
artifact/issuer must be named. SRC04's remaining full-frontier work is a scale
architecture blocker, not a source-right request. SRC17 I03/I05 remains outside
the current grant regardless.
