# EVS 2008 V372 — Sentinel / Missing-State Authority

Worker: `CLOSED35-L2R-EVS2008`

Scope is exactly `EVS2008_V372_SENTINEL_REASON`. This return does not reopen EVS 2008 MR topology, routing, malformed-text alignment, or F201.

Canonical Rawlsing source identity inherited from the accepted CLOSED35 estate:

- file: `EVS 2008.sav`
- SHA-256: `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`
- accepted physical v372 user-missing rendering: `1582-10-13`
- accepted physical user-missing count: `1917`
- accepted ordinary-present count: `64363`
- source rows: `66280`
- accepted source variable ordinal: `466`

No raw SAV bytes were opened in this worker.

## Holding

The string/date `1582-10-13` is **not an EVS producer semantic code or a substantive interview date**.

It is a date-format rendering boundary created when one or more EVS standardized negative missing codes are represented through an SPSS date-format variable.

The exact producer missing-code vocabulary applicable to **all variables** in ZA4800 v5.0.0 is:

| Numeric code | Producer meaning |
|---:|---|
| `-1` | don't know |
| `-2` | no answer |
| `-3` | not applicable — including missing values caused by filter questions and missing values in administrative variables |
| `-4` | question not asked — e.g. question absent from a country's field questionnaire or not provided by the national program |
| `-5` | other missing — explicitly includes system missing, wild codes, and illogical answer patterns |

Authority: EVS 2008 Variable Report, ZA4800 v5.0.0, section 5.1.1 “Missing values”.

SPSS date-format variables are numeric internally and stored as seconds from midnight 14 October 1582. Values immediately below zero therefore render on the previous calendar day when converted to a date-only object. Consequently, negative EVS missing codes can collapse to the same apparent calendar date, `1582-10-13`, after a date conversion.

Authority: IBM SPSS Statistics documentation, “Dates and Times in IBM SPSS Statistics” and “Input versus display formats”.

## V372-specific producer authority

The current producer Variable Report defines:

- `v372`: **date of interview (Q137)**
- representation intended by questionnaire: day/month/year.

It records three v372-specific national exceptions:

1. **Great Britain** — invalid interview dates before/after the official survey period were recoded into **system missing**.
2. **Netherlands** — Q137 was not implemented in the field questionnaire, but data were nevertheless supplied by the country.
3. **Sweden** — date data are not available because data collection used a postal questionnaire.

Authority: EVS 2008 Variable Report, v372 page 1263.

The v372 page does **not** publish a v372-specific frequency table giving the negative numeric subcode for each of those exception classes. It also does not say that all 1,917 missing v372 records share one missing reason.

## Exact code finding

There is no lawful single-code equation:

`1582-10-13 == -N == ONE_SEMANTIC_REASON`.

The exact producer **code domain** for missing v372 values is the standardized set `{-1,-2,-3,-4,-5}`. The accepted Rawlsing physical evidence retained only the converted date-form sentinel declaration `1582-10-13`, not the underlying negative numeric subcode(s).

Because SPSS date conversion is many-to-one at day granularity for these negative second values, the rendered date cannot identify which member(s) of `{-1,-2,-3,-4,-5}` generated the 1,917 user-missing records.

Therefore the strongest lawful semantic state for the accepted physical sentinel is:

`EVS_STANDARDIZED_MISSING__NEGATIVE_SUBCODE_NOT_RECOVERABLE_FROM_DATE_RENDERING`

and **not** any one of:

- `DONT_KNOW`
- `NO_ANSWER`
- `NOT_APPLICABLE`
- `QUESTION_NOT_ASKED`
- `OTHER_MISSING`
- `SYSTEM_MISSING`

unless a later exact numeric-code witness from the canonical source or a producer-issued v372 frequency/code manifest establishes the subcode.

## Scope

This rule is **v372-only** at the affected physical representation.

It does not authorize collapsing other date/time variables, and it does not alter the already-closed routing/text/MR/F201 authority from `CLOSED35-L2-EVS2008`.

## Realization rule

A future source-specific realization may lawfully:

1. preserve all 1,917 accepted v372 sentinel records as missing;
2. bind the producer's standardized missing-code dictionary `-1..-5`;
3. keep `missing_reason_detail = UNKNOWN_WITHIN_PRODUCER_NEGATIVE_MISSING_DOMAIN` where only the rendered `1582-10-13` witness is available;
4. preserve v372-specific producer notes for Great Britain, Netherlands, and Sweden without assigning those notes to individual records by inference;
5. upgrade the subreason only if the exact canonical source's numeric storage code is lawfully exposed by a later authorized physical realization.

It must not infer v372 subreason from adjacent variables.

## Authorities

Producer:

- EVS, GESIS (2022), *EVS 2008 - Variable Report*, ZA4800 v5.0.0, DOI `10.4232/1.13841`.
  - section 5.1.1, Missing values
  - v372, page 1263
  - https://access.gesis.org/dbk/59828

Technical representation:

- IBM SPSS Statistics, *Dates and Times in IBM SPSS Statistics*
  - https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=wizard-dates-times-in-spss-statistics
- IBM SPSS Statistics, *Input versus display formats*
  - https://www.ibm.com/docs/en/spss-statistics/30.0.0?topic=type-input-versus-display-formats

## Closure

`EVS2008_V372_SENTINEL_REASON` is closed at realization-authority grain as a **producer-standardized missing state with nonrecoverable subreason under the inherited date-rendered witness**.

The worker does not pretend that `1582-10-13` is itself the producer code, or that one of the five producer missing meanings can be selected from the date rendering alone.
