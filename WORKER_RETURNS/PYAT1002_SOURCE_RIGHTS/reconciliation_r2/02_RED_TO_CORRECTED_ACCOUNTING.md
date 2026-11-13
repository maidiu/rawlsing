# PYAT1002 R2 — RED → corrected historical accounting

**Prior return:** `58ee21134730eb0afaa48842647d568e63c884b8`
**Correction contract:** `PYAT1002-HISTORICAL-GRANT-RECONCILIATION-R2`
**Prior source cut searched:** `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`
**Later evidence now read:** `303a5785…`, `b6be4058…`, `5b1b9bd5…`, `24f2f3f2…`, `e21f28f2…`, `ba412536…`
**R2 source opens/reads/hashes/native executions:** `0 / 0 / 0 / 0`

## RED claim in the prior return

The prior return at `58ee2113` said, in effect:

1. No current source-use grant was located for any of the 35.
2. SRC04 and SRC17 had no actual original respondent positive; the inspected
   `PASS` artifacts were R157 nonrespondent fixtures.
3. The highest-impact unlock was a new SRC04 decision using the worker's proposed
   host name, purpose string and 30-day retention.
4. All 35 rows were `UNKNOWN_OWNER_DECISION`.

The first and third statements were **scope errors**, not new scientific
findings. The prior search correctly read the R157 fixture cut, but omitted the
later actual source-native campaigns that are locally available in the same
repository.

## Corrected factual accounting

| Prior claim | Exact later evidence | Corrected accounting |
|---|---|---|
| No SRC04 source-use grant | `303a5785…:campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json` SHA-256 `d8f13c67…`; `b6be4058…:campaign_src04_completion/empirical/USER_EMPIRICAL_GRANT.json` SHA-256 `757ee9e0…`; earlier `3b703e87…:PYAT_CONTROL_ROOM/CAMPAIGN_A_SRC04_USER_GRANT.json` SHA-256 `feb8320a…` | Actual human user operational grants exist: full SRC04 read/C11 construction, observed-response empirical operation, and an earlier first-source grant superseded by the full grant. |
| No SRC04 actual source-native positive | `303a5785…` actual primary; accepted scoped at `ba412536…`; independent review `e21f28f2…` verdict `PASS_SCOPED_ORIGINAL_SRC04_RELEASE`; release `9ddec985…`; `b6be4058…` actual partial empirical execution | Actual original C11 release exists and was accepted scoped: 7,337 rows, 177 selected responses + 3 coordinates, 1,298,649 response positions, q217 held at 38 source-unbound cells. Actual original empirical execution is partial: 208 operations (177 unary + 31 joint), 0 refused, full frontier scale-blocked, no full-success claim. |
| No SRC17 source-use grant | `5b1b9bd5…:campaign_d2_src17/evidence/TRUE_HQ_GRANT.txt` SHA-256 `f51de878…`; `GRANT_AUTHENTICATION.json` SHA-256 `f7fb429b…`; `USER_GRANT.json` SHA-256 `d6272ba6…` | Actual True-HQ D1/D2 operational grant exists with `CURRENT_GRANTED`, host `USER_LOCAL_MAC`, purpose `SECOND_FAMILY_ORIGINAL_SOURCE_C11_POSITIVE`, exact SRC17 SHA, no revocation recorded, effective interval pinned to control `3b703e8`. |
| No SRC17 actual source-native positive | `5b1b9bd5…` original C11 release `2f81b527…`; independent review `24f2f3f2…` verdict `PASS`, grade `SOURCE_NATIVE_C11_POSITIVE_QUALIFIED_WITH_RECORDED_HISTORICAL_PROCESS_DEVIATION` | Actual original C11 release exists and was independently reviewed PASS: 1,504 rows, 258 selected responses, 21 held, 2 coordinates. The review records a historical pre-admission metadata listing; no source bytes were read/hashed outside admission and no material effect was observed. |
| One new SRC04 grant is the highest-impact unlock | Existing SRC04 full/empirical grants | The prior proposed new SRC04 host/purpose/30-day grant is **withdrawn** as redundant and not required by the actual grant terms. No new grant is minted. |
| All 35 unknown | SRC04 and SRC17 actual grants; other 33 unchanged | Corrected register: **2 authorized** (`SRC04`, `SRC17`) under exact historical scopes; **33 remain `UNKNOWN_OWNER_DECISION`**. SRC17 is authorized only for source read/C11 construction, not I03/I05. SRC04 is authorized for observed-response statistic/I03-conusumer scope, not eligible/population/canonical/causal. |
| R2 did no source read | R2 only read Git evidence | Still true: R2 opened/read/hashed/executed no source bytes and minted no permission. Historical campaign reads are reported, not repeated. |

## Exact actual positives vs fixtures

### SRC04 actual positive

- Source: `2a48ba4b…`, 7,337 rows, 181 columns, host `USER_LOCAL_MAC`.
- C11 release: `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1`.
- Accepted scoped: `ba41253681212be14a0cde009afb99d77e14935e`.
- Independent review: `e21f28f2657027bfde37d27e5fe5dad2f7fd3908`,
  `PASS_SCOPED_ORIGINAL_SRC04_RELEASE`.
- Selected: 177 response fields + 3 coordinates; q217 held at 38 unbound cells.
- Actual empirical: 208 operations executed, 0 refused; remaining 15,546-operation
  full queue stopped on scale, not on rights. No full-frontier claim.
- R157 fixture positive: separate `R157_FIXTURE_RELEASE/SRC04`, 8 nonrespondent
  rows; not counted as actual.

### SRC17 actual positive

- Source: `59e65801…`, 1,504 rows, 339 columns, host `USER_LOCAL_MAC`.
- C11 release: `2f81b527ba1a62ecb79c7cc858063d60a10826a91af7d689606ed83e6bbd039e`.
- Independent review: `24f2f3f22f05ed1f0d71dbdf61dbab62d7269358`, verdict `PASS`
  at `SOURCE_NATIVE_C11_POSITIVE_QUALIFIED_WITH_RECORDED_HISTORICAL_PROCESS_DEVIATION`.
- Selected: 258 response fields; 21 held; 2 coordinates; 339/339 physical slots
  accounted.
- No SRC17 I03/I05 authorized by the D2 grant.
- R157 fixture positive: separate `R157_GSS_FIXTURE_RELEASE/SRC17`; not counted
  as actual.

## Four authority layers (not conflated)

| Layer | SRC04 | SRC17 |
|---|---|---|
| 1. User operational read authorization | **Present** — full-source grant + empirical grant, host `USER_LOCAL_MAC` | **Present** — True-HQ D1/D2 disposition, host `USER_LOCAL_MAC`, user/source decision refs |
| 2. Documented dataset licence/rights | **Not located in read set** — user operational authorization is not a dataset licence | **Not located in read set** — same |
| 3. Scientific issuer/claim authority | Observed-response statistic and source-local I03 consumer only; no eligible/population/canonical/causal/structural/FF | C11 construction only; no I03/I05/population/canonical/weight |
| 4. Runtime resolver representation | Actual `PYAT_FULL_SOURCE_READ_GRANT` and `USER_EMPIRICAL_GRANT` schemas, campaign runners; not a generic `IssuedSourceReadDecision` | `GRANT_AUTHENTICATION` carries request and `USER_SOURCE_READ_DECISION` refs, currentness; actual `USER_GRANT` schema is separate |

A field-name or schema mismatch in layer 4 is **not** evidence that layer 1 or
layer 3 is absent. Conversely, the presence of layer 1 does not manufacture
layer 2 or expand layer 3.

## Continued applicability

- SRC04 full grant: `currentness: CURRENT_GRANTED`, `revocation: NONE_RECORDED`,
  no expiry stated. No later revocation was located.
- SRC04 empirical grant: `currentness: CURRENT_GRANTED`, `revocation` not stated,
  no expiry stated. No later revocation was located.
- SRC17: `currentness: CURRENT_GRANTED`, `revocation: NONE_RECORDED`,
  `effective_interval: 2026-10-27/TRUE_HQ_D1_D2_PINNED_CONTROL_3b703e8`.
  No expiry was inferred from age and no later revocation was located.
- No new publisher signature, web scrape, paid source or new terms request was
  made or inferred.

## Other 33 rows preserved

The prior matrix's other 33 rows are unchanged. Canonical digest before/after:

```text
before: 411fe181a00a2b54d507b2cfd050d2a96248e32fd1ecfad4f7da7d18ae059a67
after:  411fe181a00a2b54d507b2cfd050d2a96248e32fd1ecfad4f7da7d18ae059a67
```

The prior nine return files also remain unchanged at their exact hashes; the
R2 receipt records all nine. Only this new `reconciliation_r2/` directory is
changed.

## What is still unresolved

For SRC04, the source/C11 and observed-response empirical path is authorized
within its stated limits. The remaining SRC04 full-frontier issue is a
scale/architecture blocker, not a source-right blocker.

For SRC17, source read and C11 construction are authorized; **I03/I05 are
explicitly not authorized by the D2 grant**. The smallest consequential
authority question is whether the 1002 intended U/Epre/first-I03 step is outside
that grant and therefore needs a separate scientific issuer, and whether the
absence of a separately documented dataset-owner licence matters for that step.
That question is sent to Browser High in
`03_ONE_BROWSER_HIGH_DECISION.md`; it is not decided here by model authority.
