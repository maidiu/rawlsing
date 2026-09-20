# CLOSED35-R2-EVS2008 — Realization Contract

Contract: `CLOSED35_R2_EVS2008_SOURCE_REALIZATION@1.0.0`

## 1. Source identity

The realization is valid only for:

- canonical filename: `EVS 2008.sav`
- canonical SHA-256: `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`
- format: SAV
- replay key: `SOURCE_SHA256+ROW_ORDINAL`

Any source-SHA drift fails closed.

The accepted reader path is the exact-SHA latin1 compatibility path defined by the generic physical decoder. That path is execution/extraction authority only.

`latin1 compatibility output != intended text != producer semantic authority`

## 2. Producer authority namespace

Documentary release identity:

- EVS 2008 Integrated Dataset
- GESIS ZA4800
- version 5.0.0
- release 2022-06-08
- DOI 10.4232/1.13841
- documented geometry 66,280 × 477

The admitted authority order is:

1. ZA4800 v5.0.0 Variable Report / integrated variable catalogue;
2. EVS 2008 Master Questionnaire for question wording, response design and routing;
3. method, national, translation and errata documentation for bounded country-specific corrections/deviations.

Malformed compatibility-rendered SAV prose has no semantic fallback role.

Exact source variable or producer question identity is the join key. Fuzzy label similarity, vector equality, ordinal adjacency, or compatibility-decoded text cannot create an alignment.

Unjoined semantic text remains `UNKNOWN_PRODUCER_TEXT`.

## 3. Producer checksum boundary

The producer release identity is documentary.

The canonical Rawlsing SHA is internal exact byte identity.

No public producer SHA-256/MD5/signed manifest was admitted by CLOSED35-L2R-EVS2008.

Therefore:

`RAWLSING_CANONICAL_SHA != CLAIMED_PRODUCER_PUBLISHED_DIGEST`

unless future producer checksum evidence is separately admitted.

The realization rejects any producer-checksum claim manufactured from documentary alignment.

## 4. Native MR topology

Exactly 13 native MR-set identities are admitted.

| Set | Members | Producer battery | Rank/order law | Alias/overlap law |
|---|---|---|---|---|
| q5a | v10–v25 | Q5a | category order only | exact-member alias of evs_q5a |
| evs_q5a | v10–v25 | Q5a | category order only | exact-member alias of q5a |
| vv25 | v10–v24 | Q5a substantive body | category order only | q5a minus v25=None |
| q5b | v28–v43 | Q5b | category order only | exact-member alias of evs_q5b |
| evs_q5b | v28–v43 | Q5b | category order only | exact-member alias of q5b |
| vv43 | v28–v42 | Q5b substantive body | category order only | q5b minus v43=None |
| evs_q6 | v46–v60 | Q6 | category order only | none |
| q14 | v69–v86 | Q14 | category order only | exact-member alias of evs_q14 |
| evs_q14 | v69–v86 | Q14 | category order only | exact-member alias of q14 |
| q52 | v170–v181 | Q52 | maximum five selections; no rank significance | exact-member alias of evs_q52 |
| evs_q52 | v170–v181 | Q52 | maximum five selections; no rank significance | exact-member alias of q52 |
| evs_q107 | v323,v324a–v328a | Q107 | category order only | b-side counts stay outside set |
| evs_q108 | v329a–v334a | Q108 | category order only | b-side ages stay outside set |

The implementation freezes one `MR_TOPOLOGY_IDENTITY` digest over exact native set names, ordered membership, alias/overlap roles, selection-cap law, and distinct nonmember roles.

### Noncollapse law

The following are forbidden:

- dropping one alias set because its member list equals another;
- counting alias sets as two independent producer batteries;
- rewriting vv25 into q5a;
- rewriting vv43 into q5b;
- folding Q107 b-side count variables into the MR set;
- folding Q108 b-side age variables into the MR set;
- converting Q52 category order or selection cap into preference rank.

## 5. MR item missing-state law

Where ZA4800 documents the integrated MR vocabulary:

- 1 = mentioned / yes;
- 0 = not mentioned / no;
- -1 = don't know;
- -2 = no answer;
- -3 = not applicable;
- -4 = question not asked / not provided;
- -5 = other missing, including producer-described system/wild/illogical cases.

The semantic owner distinguishes ordinary 0 from missing states.

The producer negative vocabulary is not generalized to unrelated fields by analogy.

Physical missing classification remains an independent physical fact and is not routing authority.

## 6. Routing and applicability

Routing/applicability is documentary and variable/question × country scoped.

Implemented closed examples include:

- Q5b Denmark: not implemented -> -4;
- Q6 Austria, Belarus, Denmark, France, Italy, Norway, Slovenia: not implemented -> -4;
- Q6 Finland: no-such-groups auxiliary -> 0; cannot-say -> -1;
- Q107 Finland: none-above -> presence indicators 0;
- Q108 Finland: none-above -> 0; cannot-say -> -1;
- Q107 flow: Q105=00 skips Q106 and proceeds to Q107; Q107 itself does not become inapplicable.

Outside an admitted exact country/question rule, the realization returns `BOUNDED_UNKNOWN`.

Observed missingness is discarded as an authority input.

## 7. V372 law

Producer variable:

- `v372`
- Q137
- date of interview

Accepted inherited physical witness:

- rendered user-missing date: `1582-10-13`
- affected records: 1,917
- ordinary-present records: 64,363
- accepted source ordinal: 466

ZA4800 standard negative domain:

- -1 don't know
- -2 no answer
- -3 not applicable
- -4 question not asked / not provided
- -5 other missing

The date rendering is many-to-one with respect to those negative numeric values.

Therefore the exact realization state is:

`EVS_STANDARDIZED_MISSING__NEGATIVE_SUBCODE_NOT_RECOVERABLE_FROM_DATE_RENDERING`

with:

`UNKNOWN_WITHIN_PRODUCER_NEGATIVE_MISSING_DOMAIN`

No negative subcode may be selected from the rendered date alone.

Producer notes for Great Britain, Netherlands and Sweden remain documentary context and cannot be assigned to individual records without an exact numeric/storage witness.

## 8. Flag relations

The realization preserves closed flag authority, including:

- `f201 -> v201/v202`;
- f201 0 = consistent, 1 = inconsistent;
- `f25` Q5a body-versus-None consistency;
- `f43` Q5b body-versus-None consistency;
- `f86` Q14 body-versus-None consistency;
- `f180` Q52 more-than-five-selection flag.

The misleading compatibility-rendered f201 heading has no authority.

## 9. Candidate neutrality

A/B/C bind one immutable:

`SOURCE_SPECIFIC_REALIZATION_IDENTITY`

The identity includes:

- canonical source root;
- producer documentary release namespace;
- compatibility-text quarantine;
- exact 13-set MR topology;
- missing-state law;
- routing authority boundary;
- V372 bounded missing state;
- flag relations;
- S35 edge scope;
- R35 contract seams.

A candidate may choose a different physical strategy only if later physical qualification proves the same governed incidence. It may not alter this semantic owner.

## 10. S35/R35 physical contract

Applicable S35 classes:

`EC01; EC02; EC03; EC08; EC14`

R35 hooks:

### I01

`PRE553_PHYSICAL_METADATA@1.0.0`

Must preserve generic physical metadata, raw layout declarations, normalized geometry, display metadata, decoder/config identity and physical metadata digest. No semantic authority.

### I02

Canonical-source / derivative-parentage receipts are required for non-direct-raw or persisted derivative carriers.

A self-asserted parent SHA is not parentage.

No semantic authority.

### I03

Later source qualification must bind the candidate-neutral whole-source physical-equivalence schemas:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

Required EVS2008 physical dimensions include:

- physical metadata;
- variable inventory/order;
- raw storage values;
- typed missingness;
- row replay identity;
- reader/config digest;
- compatibility-decode evidence;
- native MR topology.

A future I03 PASS remains:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

## 11. Implementation boundary

Implemented:

- browser-side source-specific owner;
- exact native MR contract;
- documentary text quarantine/authority resolver;
- MR missing/routing law;
- V372 bounded missing realization;
- producer-checksum negative law;
- candidate-neutral semantic identity;
- S35/R35 seams;
- source-independent hostile tests.

Not performed:

- raw SAV open;
- real decoding;
- real-source physical receipt;
- A/B/C execution;
- I05;
- measured P2X.

