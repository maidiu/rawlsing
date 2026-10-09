# HQ262 E01 — release, version, variance and authority gaps

Because both authorized carriers are absent on this host (see `00_…` and `01_…`), **no** release,
version, variance or authority determination was made from physical metadata. This file records the
gaps that must be closed and the ceiling that holds until the carriers are restored.

## 1. Official released-version bridge — STILL `UNVERIFIED`

Nothing in this lane links the expected SHA-256 values to an *official released edition* of the two
Afrobarometer files. The repository manifests and the source-byte inventory record a filename, a byte
size and a hash, but **a filename and a size do not establish which official release edition a file
is**, nor whether it is the country-original or an all-country merged build. HQ262 Part B is explicit:
no country release edition match may be claimed without an independent official edition witness.
Therefore:

- `Afro Barometer Round 5.sav` @ `c9200ba3…` — **UNVERIFIED against any official released bytes**.
- `Afro Barometer Round 9.sav` @ `3afcecd0…` — **UNVERIFIED against any official released bytes**.
- Not even the physical presence of these hashes was confirmed here; the hashes remain *expected*
  values from prior inventory.

## 2. Design / variance authority — not established, and not establishable from a dictionary

Even if the dictionaries are eventually read successfully:

- **Header PSU/stratum labels do not certify a correct design estimator.** A `PSU`/`stratum`/`EA`
  column or label is a *presence* witness, not a qualified variance plan; the sampling weights,
  with-replacement/without-replacement assumption, finite-population correction, calibration and
  replicate structure must be separately qualified by a competent survey-statistics owner.
- **R5 `withinwt` and R9 `withinwt_ea` / `withinwt_hh` are not interchangeable.** They target
  different inclusion-probability bases (EA level vs household level with `ADULT_CT`); any use must
  name the exact candidate and its semantics for its own wave, and no R5→R9 weight transfer is
  authorised.
- **Region / `URBRUR` are not verified PSU or stratum identifiers.** The prior documentary return
  already flagged that national codebooks list `REGION` and `URBRUR` without proving unique PSU IDs
  or a complete replicate-weight recipe.
- **`RESPNO` upper bound `GHA2369` vs published headline n = 2400** stays unresolved: the dictionary
  cannot settle it, because the question is about respondent-level scope, which metadata must not
  read.

Native uncertainty remains **`UNCERTAINTY_UNQUANTIFIED`**; no weight may be assumed.

## 3. What a qualified survey-statistics / EE12 authority owner must fix next

1. **Physical custody restore** of the two exact carriers (or an authorised locator), verified by
   streaming SHA-256 against the expected digests.
2. **Official edition witness** independently linking each frozen byte identity to a named official
   Afrobarometer release (country-original vs merged), with release name and version.
3. **Native dictionary readout** (metadata-only) establishing: Ghana country selector column and
   codes; the exact mapped Q43/Q31 column labels and native value/missing labels; age, citizenship
   and asked/routing fields; the exact weight candidate names and types; and whether any PSU/stratum/
   replicate metadata exists at all.
4. **Design qualification** by a survey-statistics owner: the correct estimator per wave, weight
   semantics, stratification/clustering, calibration/post-stratification and design-based variance —
   for each wave separately, with no cross-wave weight substitution.
5. **Reconciliation** of `RESPNO GHA2369` against published n = 2400, which requires a *separately
   authorised* respondent-scope decision, not a metadata read.
6. **A distinct source-operation permission** before any respondent-backed producer fact, and only
   then a **pair-specific EE12/C7 relation** by explicit HQ issuer. None of these exists here.

## 4. Ceiling preserved

- This is not a source-use grant; the retained-product read did not even occur.
- No source-backed `q`, share, count, weight, trend, variance or uncertainty was computed.
- No FF02 LiTS work, no N9/N10W world or actor claim, no causal or objective-change claim, no V3, no
  EE14 model use, no G0b grant.
- Passing a future metadata read would be **readiness for a later distinct scientific design/custody
  authority court**, not permission for quantitative execution.
- A worker result is not independent acceptance.

**Terminal:** `HQ262_E01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.
