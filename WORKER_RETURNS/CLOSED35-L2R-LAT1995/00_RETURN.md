# CLOSED35-L2R-LAT1995 — Latinobarómetro 1995 Residual Brazil / ID / Weight Authority Recovery

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2-documentary-fanin-r1@5c582e2325ecc2b37377cd518fe4c456331c81d8`

Branch: `agent/rabochii-closed35-l2r-lat1995-residual-authority-r1`

Return: `WORKER_RETURNS/CLOSED35-L2R-LAT1995/`

## Boundary

This is the final targeted documentary recovery pass for the exact residual set inherited from `CLOSED35-L2-LAT1995`.

Research surface:
- GitHub repository evidence;
- current producer documentation;
- historical JDS/ASEP distributor/archive pages;
- public archival/catalog evidence;
- contemporaneous and later documentary corroboration.

Forbidden and not performed:
- opening raw SAV bytes;
- row inspection;
- numeric-distribution inference;
- source normalization;
- dropping or reclassifying Brazil rows;
- treating later harmonized files as replacement canonical roots.

Canonical source remains unchanged:

- `Latinobarometro 1995.sav`
- SHA-256 `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7`

## Governing inherited facts

The L2 fan-in already settles:
- the canonical raw source is authentic;
- final producer release `v1995.1` exists;
- producer 1995 substantive tables recognize Brazil `N=1200`;
- producer technical documentation reports Brazil `N=1080`;
- the contradiction is real;
- `ENC` is an interview-number carrier;
- `WT` is a weighting field.

This worker does not relitigate those facts.

## Result

The deeper archival pass found **real release-history evidence**, but no document closes any of the source-specific causal/estimator residuals.

The strongest new lead is a JDS/ASEP archive notice documenting that files from 1995–2005 were later updated/replaced as part of documentation/harmonization work. The notice states the scope: adding or revising **Region, City, and Political Party** coding/labels. A related 2013 notice says files would be replaced after review of those codes for 1991–2010.

That is material provenance evidence because it proves that historical distributed files were not a single timeless publication object. It is **not** authority that:
- Brazil's 120-row delta resulted from that replacement;
- `ENC` uniqueness changed;
- `WT` was reconstructed;
- `WT` was normalized;
- any Brazil rows were removed or added.

No archived changelog, erratum, producer note, country fieldwork report, syntax file, or weighting memorandum was recovered that links the 1995 Brazil `1200/1080` contradiction to a documented operation.

## Brazil adjudication

The archival record now has three distinct layers:

1. **Contemporaneous producer layer** — inherited L2 evidence: report tables use Brazil `N=1200`; technical sheet uses `1080`.
2. **Contemporaneous external corroboration** — an August 1995 El País report says the first eight-country survey comprised `9,077` interviews.
3. **Later archive/version layer** — JDS/ASEP documents later replacement/harmonization of 1995–2005 files for named geography/party coding work, without identifying case-count changes.

A later mirror of the producer-branded 2005 report prints 1995 bases of `9,070` for at least one trend chart and `9,069` for another. Those are chart/question bases, not an identified full-wave correction, and they do not establish Brazil provenance. Their only lawful use here is negative: published `n` surfaces across later trend products cannot be treated as a release-size genealogy without explicit producer linkage.

Therefore:

`BRAZIL_120_ROW_CAUSAL_PROVENANCE = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`

Neither `1200` nor `1080` is declared erroneous.

## ENC adjudication

No 1995 producer/distributor documentation recovered in this pass gives `ENC` a uniqueness contract.

The historical archive treats country×wave selections as samples, but that does not turn `ENC` into a country-local key. No documentation states:
- globally unique;
- country-local unique;
- explicitly nonunique;
- stable across files/releases;
- respondent/person identifier;
- longitudinal key.

The most precise frozen state is:

`ENC_UNIQUENESS_SCOPE = UNDOCUMENTED`

Operational consequence remains:
- preserve `ENC`;
- preserve collisions;
- do not deduplicate;
- do not promote `PAIS+ENC` to a key;
- replay identity remains `SOURCE_SHA256 + ROW_ORDINAL`.

## WT adjudication

The residual search recovered no 1995-specific weighting note, syntax, calibration table, post-stratification margins, target-population statement, or normalization rule.

Current producer ODA documentation explicitly says its statistics apply the **sample weight provided for each selected sample by default**. Current study-level documentation describes country surveys as samples and the aggregate file as a wave-level combination.

This closes only a modern **ODA platform behavior**:
- selected sample → supplied sample weight when available;
- ODA default statistics → weighted.

It does **not** establish for the 1995 raw field `WT`:
- its target estimand;
- its population domain;
- whether normalization is mean-1, sum-to-sample-N, population expansion, or another rule;
- construction/calibration inputs;
- whether one may combine countries with the same `WT`;
- an external raw-file default estimator;
- any causal connection to Brazil `1200/1080`.

Historical JDS pages preserve the official 1995 questionnaire/technical record and codebook, but no separate 1995 weighting memorandum is listed. Search results for archive weighting documentation surfaced detailed WVS weighting materials, not a Latinobarómetro-1995 analogue; those WVS rules are explicitly non-transferable.

Frozen statuses:

- `WT_ESTIMAND_AND_POPULATION_DOMAIN = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `WT_NORMALIZATION = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `WT_CONSTRUCTION_CALIBRATION = IRREDUCIBLE_DOCUMENTARY_UNKNOWN`
- `EXTERNAL_RAW_DEFAULT_WEIGHTED_ESTIMATOR = NO_1995_PRODUCER_AUTHORIZATION_RECOVERED__DO_NOT_DEFAULT`

The last item is a closed **authority state**, not a claim that the producer never intended weighting. It means this documentary court cannot authorize an external default estimator.

## Stop-law application

A concrete new archive lead **was** found and followed:
- historical files were updated/replaced;
- the documented scope was region/city/political-party harmonization;
- no residual-relevant case-count/ID/weight changelog was found.

No additional concrete producer archive lead remains after targeted searches across:
- current release/documentation surfaces;
- JDS/ASEP collection, documentation, sample-selection, release/update notices;
- contemporary 1995 reporting;
- CEPAL catalog for the 1997 Latinobarómetro-1995 study;
- historical computer-file citations / secondary archive references;
- exact searches for 1995 weighting, `WT`, `ENC`, Brazil 1080/1200, errata, and file substitution.

Under the commissioned stop law, the residual set is now frozen rather than recursively web-searched.

## Admission consequence

Safe source-specific realization may preserve:
- exact canonical root;
- all canonical rows;
- `PAIS`;
- `ENC` as a non-key source-native carrier;
- `WT` as a source-native weighting carrier;
- the Brazil contradiction as explicit documentary provenance.

This worker does **not** authorize:
- row removal;
- `ENC` uniqueness;
- `PAIS+ENC` uniqueness;
- default weighted raw estimation;
- cross-country use of `WT`;
- `WT` renormalization/recalibration;
- treating current ODA semantics as the missing historical 1995 estimator contract.

Weighted source-specific realization remains blocked at estimator semantics unless a future **concrete producer record** is discovered outside the exhausted public documentary surface.

## Terminal

`CLOSED35_L2R_LATINOBAROMETRO1995_RESIDUAL_AUTHORITY_FROZEN__IRREDUCIBLE_UNKNOWN_SET_RETURNED`
