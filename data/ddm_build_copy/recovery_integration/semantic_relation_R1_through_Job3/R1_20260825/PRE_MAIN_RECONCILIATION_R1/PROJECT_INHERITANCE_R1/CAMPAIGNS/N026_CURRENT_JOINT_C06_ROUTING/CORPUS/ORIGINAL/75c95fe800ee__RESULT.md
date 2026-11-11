# C06 R2 — Lossless sibling-carrier adapter / real join closure

## Result

**PASS — Path B: `CURRENT_ROUTING_LEDGER_CONTRACT@2`.**

`C06_REAL_CURRENT_ROUTING_JOIN_R2_PASS`

The R1 blocker was a physical carrier-contract mismatch, not a routing-authority gap. The old C06 26-column schema required heterogeneous sibling evidence/provenance/predicate data to be duplicated into one row serialization. Frozen C02-C05 already conserve that information through exact row carriers, manifests, dictionaries, predicate/test sidecars, and content hashes. R2 therefore supersedes only the denormalized carrier shape. No routing disposition was reopened or reinterpreted.

## Executed current join

The exact frozen sibling adjudications reconcile to the exact current universe:

- input rows: **18,276**
- output rows: **18,276**
- unique current IDs: **18,276**
- missing: **0**
- extra: **0**
- duplicate: **0**
- family leakage: **0**
- `(source_family, wave, source_variable_code)` drift: **0**

Frozen disposition vector:

- `GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE`: **1,025**
- `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`: **1,574**
- `GOVERNED_SCOPED_NONAPPLICABILITY`: **17**
- `ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT`: **1,274**
- `STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT`: **14,386**

The exact unresolved taxonomy input therefore retains **14,386** rows.

## Why Contract@2 is lossless

Contract@2 retains the irreducible row state—current implementation identity and frozen disposition—and cryptographically binds every projected row back to its exact frozen source carrier. Evidence, scope, predicates, replay receipts, and provenance remain in the immutable source carriers/sidecars instead of being rewritten into counterfeit C06-v1 fields. See `FIELD_LOSSLESSNESS_MATRIX.csv`.

C05 is the decisive case: its frozen return does not emit a row-level mapping from its 4,768 unresolved IDs to the three aggregate blocker classes in its blocker manifest. R2 preserves that absence exactly. It does **not** manufacture 4,768 row labels from three counts.

## Canonical outputs

The successful durable outputs use the command-authorized **exact Library carrier + Git manifest** form.

- current routing ledger carrier: `/Rawlsing/CURRENT_ROUTING_AND_V550J_CARRIER_WAVE_R1/C06_LOSSLESS_ADAPTER_R2/CURRENT_ROUTING_DISPOSITION_LEDGER.contract2.carrier.json`
  - rows: **18,276**
  - bytes: **5,535**
  - SHA-256: `5fe7fc719453479397fb759a00341dd6dc51184c8547306f7955220091405dde`
- unresolved taxonomy carrier: `/Rawlsing/CURRENT_ROUTING_AND_V550J_CARRIER_WAVE_R1/C06_LOSSLESS_ADAPTER_R2/UNRESOLVED_TAXONOMY_INPUT.contract2.carrier.json`
  - rows: **14,386**
  - bytes: **1,460**
  - SHA-256: `36bd6f3be7f12e938183285dbee30c1db5198a65beab3890f889990e5d8c82ed`

`compile_contract2.py` deterministically materializes the normalized CSV views from the exact frozen C02-C05 carriers. The composite carrier, not a copied denormalization, is canonical authority.

## Tests

- admitted C06 suite: **22/22 PASS** in GitHub Actions run `33274270929`, job `99158136342`; that job also reconstructed the exact frozen C03 canonical carrier to SHA-256 `b08b5e4b...7a095c`;
- new Contract@2 hostile suite: **8/8 PASS**;
- exact local hash gates for the 18,276-row catalog, C02 carrier, and C04 carrier: **PASS**.

## Conservation declaration

No provenance, predicate, evidence, membership authority, or routing disposition was synthesized. Aggregate counts were used only as post-execution invariants.
