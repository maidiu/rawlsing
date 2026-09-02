# FFP036 — EXACT DISCOVERY-TO-FOLLOWUP GENUINE EXECUTION HANDOFF R1

## Commanded worker

Repository:

`maidiu/rawlsing`

Branch:

`agent/rabochii-field-forge-r2-ffp036-discovery-followup-genuine-execution-r1`

Exact starting HEAD:

`b7798a9bc48582e341309610c218aadce4355ea2`

The later commit that adds this handoff file is instruction evidence only. Working ancestry must begin exactly at the sealed pre-output SHA above.

Library:

`AUTHORIZED AND REQUIRED FOR EXACT FROZEN INPUT/OUTPUT EVIDENCE`.

No new sources.

## Mission

Execute only the exact mechanically frozen `DISCOVERY_TO_FOLLOWUP_LINKAGE_MINIMUM@1` court established by FFIF014.

Do not redesign it.

Do not select a different predicate subset, external operand, query, risk set, challenger universe, support law or assertion bundle after target output.

The target court is:

- frozen risk set: `19,210` respondents;
- frozen discovery surface: `Q76A,Q76B,Q86A,Q86B,Q86C,Q86D,Q86E,Q86F`;
- complete frozen predicate roster: `62,609` predicates;
- predicate roster canonical SHA-256: `5bf42464f3ff93e97d80f8ce178d670aa7fee98d13144f9c2d29d4f59032bced`;
- frozen `X`: `COUNTRY_ALPHA3`;
- exact country domain: `BFO;BOT;CVE;KEN;LES;MAU;MLW;MOZ;NAM;SAF;UGA`;
- target relation: `COMPLETE_COUNTRY_STRATIFIED_PREDICATE_SUPPORT@1`;
- complete target cell universe: `688,699` predicate-country cells;
- challenger universe: W0–W5 exactly; W6 excluded.

## Mandatory input verification before target output

Re-materialize and hash-check the exact governed inputs.

At minimum verify:

- risk-set artifact SHA-256 `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`;
- selected response-facts SHA-256 `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`;
- selected exposure-facts SHA-256 `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`;
- frozen predicate-roster deterministic gzip SHA-256 `4968bb74fc733cbbd3dd4db4d3aa4dfe7439b172d3fcdf62ee0ee2bc2f01319c`;
- frozen predicate-roster canonical uncompressed SHA-256 `5bf42464f3ff93e97d80f8ce178d670aa7fee98d13144f9c2d29d4f59032bced`.

Use the exact Library path frozen by FFIF014:

`/Rawlsing/FIELD_FORGE_R2/FFIF014_DISCOVERY_FOLLOWUP_PREOUTPUT_JOIN_R1/ffif014_frozen_discovery_predicate_roster.tsv.gz`

Fail closed before target adjudication on any mismatch.

## Canonical normalized target schema

For all 688,699 rows, canonical fields and ordering are exactly:

`predicate_id,subset_size,subset_mask,variables,state_pairs_json,original_support,COUNTRY_ALPHA3,country_support,status`

Sort by frozen predicate-roster order and then frozen country lexical order.

Status:

- `OBSERVED_POSITIVE` if `country_support > 0`;
- `OBSERVED_ZERO` if `country_support == 0`.

Enforce for every predicate:

`sum_country(country_support) == original_support`.

Canonical serialization is UTF-8 TSV, header present, LF line endings, exact integer decimal supports, exact status strings.

## Required mechanical realizations

### ORACLE-A / W1 — DIRECT UPSTREAM REQUERY

Using the frozen predicate definitions plus exact producer-owned current same-unit response facts and current `COUNTRY_ALPHA3`, regenerate the complete normalized target without using any FIELD-FORGE-local stored predicate-membership table.

This is the architecture-dispositive challenger.

### ORACLE-B / W5 — INDEPENDENT FULL-STATE REALIZATION

Independently construct the exact frozen wide same-unit eight-variable state surface plus country context, enumerate/group by the frozen predicates, and regenerate the same canonical target through a materially distinct algorithmic route.

Do not reuse ORACLE-A's already-materialized target rows as the calculation source.

### W4 — PREDICATE MEMBERSHIP + QUERY

Materialize exact predicate/respondent membership, join the exact country token, and regenerate the canonical target. Membership may be large; bank it only if useful for independent evidence. Persistence itself is not a success criterion.

### W3 — FOLLOW-UP-STRATIFIED SUMMARY

Materialize the exact frozen Q1 sufficient statistic after target execution, then independently reconstruct the canonical target from that summary. Record its strict Q1 ceiling.

### W2 — SUPPORT-ONLY DISCOVERY SUMMARY

Use only the frozen predicate identity/original support object. Do not give it upstream response facts or predicate membership. If the external country joint relation is not derivable, return:

`UNDEFINED_FOR_OBJECT`

for AS06 rather than fabricating values.

### W0 — FINAL ASSERTION CACHE ONLY

May serve a frozen final assertion cache but must be marked replay-incomplete for AS07 unless an independent regeneration path exists outside the cache.

### W6

`EXCLUDED__NO_PREOUTPUT_FUSION_TRIGGER`.

Do not execute or resurrect W6.

## Exact equality / replay requirements

At minimum require:

- ORACLE-A run A == ORACLE-A cold/repeated run byte-for-byte at canonical semantic serialization;
- ORACLE-A canonical semantic hash == ORACLE-B canonical semantic hash;
- W4 canonical semantic hash == oracle hash if W4 executes lawfully;
- W3 reconstructed canonical semantic hash == oracle hash if W3 executes lawfully;
- every predicate satisfies the support-sum invariant;
- all observed-zero cells remain explicit;
- no unregistered country/predicate cell is dropped.

Record row counts, positive/zero status counts and exact SHA-256s.

## Evidence banking

Large result artifacts should be banked immutably in Library under:

`/Rawlsing/FIELD_FORGE_R2/FFP036_DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_R1/`

At minimum bank the canonical oracle target and any large independently materialized evidence needed for hostile replay. Record exact Library paths, ids, byte sizes and SHA-256s in Git receipts.

Commit deterministic execution code and bounded receipts/results to the worker branch.

## Required Git return package

Write only a new FFP036 directory, preferably:

`FIELD_FORGE_R2/UNBLOCKERS/FFP036_DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_R1/`

At minimum return:

- `00_MACHINE_RETURN.json`
- `01_COMMON_INPUT_REPLAY_RECEIPT.json`
- `02_FROZEN_PREDICATE_AND_QUERY_BINDING.json`
- `03_CHALLENGER_AS01_AS08_COVERAGE.tsv`
- `04_CROSS_CHALLENGER_EXACT_AGREEMENT.tsv`
- `05_REPLAY_AND_INDEPENDENT_RECONSTRUCTION_RECEIPT.json`
- `06_ARCHITECTURE_EVIDENCE_VECTOR.json`
- `07_HUMAN_EMPIRICAL_SUMMARY.md`
- deterministic execution script/code;
- exact hashes/Library evidence bank manifest.

## Architecture ceiling

Execution may establish mechanical facts only.

It may not issue CVCR, COCR or terminal FIELD FORGE architecture.

In particular:

- W1 exact PASS mechanically supplies a counterexample candidate to universal FIELD-FORGE-local respondent-membership necessity; the worker may record that bounded evidence vector but may not issue the semantic architecture ruling;
- W1 failure is not universal carrier necessity;
- W3 PASS is Q1-specific and cannot establish arbitrary-future follow-up sufficiency;
- W4/W5 PASS does not promote persistence;
- exact agreement does not establish general semantic identity;
- no strong sociology or V3/person inference is authorized.

## Fail-closed

If any frozen input, common risk set, predicate roster, query identity, country domain, challenger identity or firewall condition fails, stop and return the exact typed blocker from FFIF014. Do not repair by changing the experiment.

Successful terminal should be equivalent to:

`PASS__DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_COMPLETE__FROZEN_W0_W5_EVIDENCE_BANKED__NO_ARCHITECTURE_VERDICT`.
