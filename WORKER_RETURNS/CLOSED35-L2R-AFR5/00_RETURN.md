# CLOSED35-L2R-AFR5 — Afrobarometer Round 5 Exact Residual Documentary Authority Recovery

Branch: `agent/rabochii-closed35-l2r-afr5-residual-authority-r1`

Base: `agent/vozhd-closed35-l2-documentary-fanin-r1@5c582e2325ecc2b37377cd518fe4c456331c81d8`

Canonical source: `Afro Barometer Round 5.sav`

Canonical SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

## Disposition

**RESIDUAL FROZEN.**

Terminal:

`CLOSED35_L2R_AFROBAROMETER_R5_RESIDUAL_AUTHORITY_FROZEN__IRREDUCIBLE_UNKNOWN_SET_RETURNED`

This worker attacked only the four residual surfaces returned by CLOSED35-L2-AFR5:

1. `Q10B=997`;
2. `Q47C=997`;
3. raw `COUNTRY`;
4. administrative routing carriers.

Already-closed Round-5 weighting authority was not reopened.

No raw source was opened. No source processing or measured P2X was run.

## 1. Q10B=997 — CLOSED

The first residual is now closed by a variable-local dictionary entry in a recognized archive of the Afrobarometer merged Round-5 release.

DataFirst UCT catalog `afr-afr34-2011-2013-v1`:

- collection: Afrobarometer;
- DOI: `10.25828/vz8c-af95`;
- created 27 August 2015;
- data file: `Merged 34 Country Database`;
- variable: `Q10B`, "Have been physically attacked";
- category **997 = Not asked**.

This evidence is materially stronger than transferring the meaning from another 997-bearing variable: it is the exact Q10B variable entry in the archived merged dictionary.

The prior official July-2015 Afrobarometer revision note independently proves the routing circumstance that Tanzania Q10B was dropped because the Swahili translation asked about fear of theft rather than physical attack.

Holding:

```
Q10B == 997
  => NOT_ASKED
```

This holding is **Q10B-local**. It creates no general Round-5 law that `997` means Not asked everywhere.

## 2. Q47C=997 — IRREDUCIBLE AFTER TARGETED RECOVERY

The second residual did not close.

Targeted recovery checked:

- the official final merged Round-5 codebook;
- the DataFirst exact merged Q47C variable dictionary;
- the inherited South Africa country codebook;
- recognized Round-5 country archive dictionaries.

The exact merged DataFirst Q47C entry documents:

- `-1 = Missing`;
- `98 = Refused`;
- `99 = Don't know / haven't heard enough`;

and **does not document 997**.

The official final merged codebook likewise omits 997 for Q47C.

Separately, South Africa's producer country codebook states that Q47C was **not asked** in South Africa. That is a valid country-routing fact. It is still not a producer statement that the merged numeric state `997` encodes that fact.

Because inherited exact physical evidence says Q47C has a declared numeric `997` user-missing state **and** separate SPSS system-missing incidence, neither state may be collapsed into the other.

Stop-law holding:

```
Q47C == 997
  => DOCUMENTARY_AUTHORITY_UNKNOWN_AFTER_TARGETED_RECOVERY
```

Forbidden:

- borrowing `997=Not asked` from Q10B;
- borrowing it from Q47D or another neighboring question;
- equating Q47C numeric 997 with system missing;
- inferring the numeric binding solely from South Africa's not-asked routing fact.

The South Africa routing fact survives separately:

`SAF_Q47C_DOCUMENTED_NOT_ASKED`.

## 3. Raw COUNTRY carrier — CLOSED DIRECTLY

The prior blocker existed because the official PDF codebook foregrounded `COUNTRY_ALPHA`, while the exact SAV carries a distinct raw `COUNTRY` field.

Recognized archives of the merged release directly expose **both** fields.

DataFirst's exact merged dictionary documents raw `COUNTRY` as:

| code | country |
|---:|---|
| 1 | Benin |
| 2 | Botswana |
| 3 | Burkina Faso |
| 4 | Cape Verde |
| 5 | Ghana |
| 6 | Kenya |
| 7 | Lesotho |
| 8 | Liberia |
| 9 | Madagascar |
| 10 | Malawi |
| 11 | Mali |
| 12 | Mozambique |
| 13 | Namibia |
| 14 | Nigeria |
| 15 | Senegal |
| 16 | South Africa |
| 17 | Tanzania |
| 18 | Uganda |
| 19 | Zambia |
| 20 | Zimbabwe |
| 21 | Mauritius |
| 22 | Sierra Leone |
| 23 | Niger |
| 24 | Togo |
| 25 | Burundi |
| 26 | Cameroon |
| 27 | Cote d'Ivoire |
| 28 | Guinea |
| 29 | Ethiopia |
| 30 | Swaziland |
| 31 | Algeria |
| 32 | Egypt |
| 33 | Morocco |
| 34 | Sudan |
| 35 | Tunisia |

This directly agrees with the inherited exact-source fixture:

`COUNTRY row0 = 31, label Algeria`

and with the inherited 35-entry raw dictionary.

The IHSN/World Bank archive independently identifies the merged file as:

`merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav`

with 51,587 cases and 348 variables including `COUNTRY`, `COUNTRY_ALPHA`, `COUNTRY.BY.REGION.NO`, and `COUNTRY.BY.REGION`.

Therefore:

```
raw COUNTRY
  => the direct 1..35 map above
```

No crosswalk through `COUNTRY_ALPHA` is needed.

`COUNTRY_ALPHA` remains a distinct official coordinate with its own alphabetical map. It must not replace or numerically reinterpret `COUNTRY`.

## 4. Administrative routing carriers — PARTIAL SUBCLOSURE, RESIDUAL FROZEN

### Regional filter family

The archived exact merged dictionary contains:

- `West.Africa.only` — `COUNTRY.BY.REGION = 1 (FILTER)`;
- `East.Africa.only` — `COUNTRY.BY.REGION = 2 (FILTER)`;
- `Southern.Africa.only` — `COUNTRY.BY.REGION = 3 (FILTER)`;
- `North.Africa.only` — `COUNTRY.BY.REGION = 4 (FILTER)`.

The inherited exact raw fixture for `WEST.AFR` supplies the identical variable label:

`COUNTRY.BY.REGION = 1 (FILTER)`.

That is sufficient to close the semantic role of exact raw `WEST.AFR` at this bounded grain:

```
WEST.AFR
  => administrative filter for COUNTRY.BY.REGION = 1 / West Africa
```

It is **not** authority to use `WEST.AFR` as a question-level not-asked oracle.

For the other raw abbreviations:

- `EAST.AFR`;
- `SOUTHERN`;
- `NORTH.AF`;

the archive supplies obvious semantic counterparts, but the recovered producer/archive material does not explicitly bind those literal raw names to the normalized archive names. This worker does not promote lexical resemblance into exact carrier identity.

They are therefore frozen as:

`DOCUMENTARY_AUTHORITY_UNKNOWN_AFTER_TARGETED_RECOVERY`

for the exact raw alias relation, while the archive-level region-filter family semantics are retained as documentary context.

### R1.ONLY..R4.ONLY

The exact merged archive dictionary confirms that:

- `R1.only`;
- `R2.only`;
- `R3.only`;
- `R4.only`

exist as administrative variables.

But each recovered entry is only self-labeled. No value dictionary, selection rule, inclusion criterion, or routing/not-asked semantics was recovered from:

- the exact merged archive dictionary;
- later merged Afrobarometer archive dictionaries, which continue carrying the same family;
- the official merged Round-5 codebook;
- the prior country/question documentation.

Therefore all four are frozen:

```
R1.ONLY..R4.ONLY
  => DOCUMENTARY_AUTHORITY_UNKNOWN_AFTER_TARGETED_RECOVERY
```

Presence and name are documentary facts. Meaning is not.

They may survive as opaque administrative metadata. They may not govern respondent/question eligibility, source-row filtering, or conversion to `997=Not asked`.

## 5. Exact residual result

### Newly closed

- `Q10B=997` -> **Not asked**.
- raw `COUNTRY` -> direct official/archive 1-35 Round-5 country map.
- `WEST.AFR` -> region-1 / West-Africa administrative filter at the documented label scope.

### Irreducible after targeted recovery

- `Q47C=997`;
- exact raw alias binding for `EAST.AFR`;
- exact raw alias binding for `SOUTHERN`;
- exact raw alias binding for `NORTH.AF`;
- `R1.ONLY`;
- `R2.ONLY`;
- `R3.ONLY`;
- `R4.ONLY`.

Every item above is now explicitly frozen as:

`DOCUMENTARY_AUTHORITY_UNKNOWN_AFTER_TARGETED_RECOVERY`

No further general-documentation search is authorized by this return.

## 6. Admission consequence

The Round-5 source is **not yet fully ready for unrestricted source-specific realization**, because the exact residual set still contains a semantic-code blocker (`Q47C=997`) and unresolved administrative-carrier semantics.

A bounded realization may now safely consume:

- Q10B `997=Not asked`;
- the direct raw `COUNTRY` map;
- `WEST.AFR` at its documented administrative region-filter role;
- all authority already closed by CLOSED35-L2-AFR5, unchanged.

It must preserve the remaining residuals as opaque/unknown and fail closed on any attempt to use them as semantic routing owners.

## Outputs

- `00_RETURN.md`
- `01_TARGETED_SOURCE_LEDGER.csv`
- `02_RESIDUAL_AUTHORITY_MAP.csv`
- `03_UPDATED_SOURCE_ADMISSION_PACKET.json`
- `RETURN.json`

## Terminal

`CLOSED35_L2R_AFROBAROMETER_R5_RESIDUAL_AUTHORITY_FROZEN__IRREDUCIBLE_UNKNOWN_SET_RETURNED`
