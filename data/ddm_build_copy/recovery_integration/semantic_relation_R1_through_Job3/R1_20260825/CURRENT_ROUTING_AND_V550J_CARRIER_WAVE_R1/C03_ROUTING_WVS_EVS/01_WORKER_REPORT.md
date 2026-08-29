# C03 — Full-Current Routing / Applicability Court — WVS / EVS R1

## Disposition

`C03_COURT_EXECUTION = COMPLETE_WITH_TYPED_UNRESOLVED`

`C03_ROUTING_AUTHORITY_COMPLETENESS = NOT_COMPLETE`

The court begins from the exact governed current WVS + EVS implementation surface only: **3,443 unique implementations** = EVS **2,224** + WVS **1,219**. Every current implementation receives exactly one Authority-45 disposition. Historical 700/99/600 trial membership is not loaded or used.

The row ledger uses compact lossless scope/evidence references. `08_SCOPE_AND_EVIDENCE_DICTIONARY.csv` expands every country, form/instrument, module, split, source-filter, decision-basis, rule, and blocker reference to its exact governed/source value with SHA-256. Each row also carries an exact `source_record_ref` into the pinned W05/W07 `O06_IMPLEMENTATION_ROUTING` carrier plus any exact clause IDs; archive identities and hashes are pinned in `05_SOURCE_MANIFEST.json`.

## Exact accounting

| Authority-45 disposition | EVS | WVS | Total |
|---|---:|---:|---:|
| `GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE` | 603 | 0 | 603 |
| `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | 0 | 0 | 0 |
| `GOVERNED_SCOPED_NONAPPLICABILITY` | 0 | 0 | 0 |
| `ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT` | 188 | 205 | 393 |
| `STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT` | 1433 | 1014 | 2447 |
| **TOTAL** | **2224** | **1219** | **3443** |

## Unresolved blocker accounting

- `SOURCE_ROUTING_UNRESOLVED_AFTER_BOUNDED_REVIEW`: **2241** (EVS 1,263; WVS 978).
- `NATIVE_CONDITIONAL_LACKS_EXECUTABLE_PREDICATE_AND_C03_3WAY_PROOF`: **158** (EVS 122; WVS 36).
- `DERIVATIVE_ONLY_CONDITIONAL_NOT_NATIVE_AUTHORITY`: **48** (EVS 48; WVS 0).

Total typed unresolved: **2447**.

## Why the 158 native conditional findings are not promoted

B03 lawfully preserved exact-current native conditional source evidence. C03 has a stronger positive-routing admission rule: executable predicate + positive case + negative case + deterministic replay. The pinned W05/W07 O06 carriers expose `routing_status`, exact clause/evidence references, and prose source condition summaries (W07 additionally exposes `predicate_type`), but no structured executable predicate field and no per-row C03 three-way execution proof. A repository-wide schema-key check across the two pinned returns finds `predicate_type` but no predicate expression/operator/operand or positive/negative/replay proof fields. C03 therefore retains every exact source clause as evidence in the ledger and refuses to counterfeit executability.

## Admitted current authority

- EVS **603** rows: exact native explicit `ASK ALL` / common-handoff proof -> `GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE`.
- EVS **188** + WVS **205** rows: exact current governed/source-substrate administrative or nonrespondent context -> `ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT`.
- No scoped nonapplicability is asserted from country coverage or missing metadata.

## Conservation / anti-drift

- exact current ID + `(source_family, wave, source_variable_code)` equality checked for all 3,443 rows;
- source scope columns are carried without turning observed country coverage into routing authority;
- B03 derivative-only conditional evidence remains quarantined;
- no neighboring-wave analogy, missing-metadata inference, historical-trial membership, V550J member authority, sibling C-wave output, architecture selection, or V3 work is used;
- current ledger accounting is complete, but routing authority is **not** complete because 2,447 current implementations remain typed unresolved.

## Exact sources

- Authority 45: `16a212b7343206c81634b26f2546ad8b60a77475`
- adopted B03 evidence return: `3d1cdd242fe10f544bdcbb5bb91cf042c56ef787`
- governed 35-wave catalog bundle SHA-256: `b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d`
- EVS catalog member SHA-256: `61c6f77d266e59f5218babecbd07636619ff90d04b4ffc837357204225729d3b`
- WVS catalog member SHA-256: `cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0`
- EVS W05 source-return SHA-256: `7b01f8aa1cb10abede4b76c77b915727d6e472b1e097f9fbb64594c7681a649d`
- WVS W07 source-return SHA-256: `d23abc9e786b4d6093bbf7bd9be9f15c7a3ca1384ba47723d532a082141359cc`

`C03_WVS_EVS_FULL_CURRENT_ROUTING_COURT_R1_COMPLETE`

## Git transport

The exact canonical 3,443-row ledger is transported losslessly as 81 ordered 1 KB base64 text chunks of an XZ stream. `02_LEDGER_MANIFEST.json` pins canonical CSV SHA-256 `b08b5e4b539cd7936ad24c04a45d8b8e672913f1656482ffc0d3dce5437a095c`, compressed SHA-256 `a317b664799b87b287eb32c35225ec6f5cc82d53fc7994cd03e2fa90cc03d60d`, every chunk hash, and the reconstruction command.

The exact 349-row scope/evidence dictionary is carried the same way in 28 chunks; `08_SCOPE_MANIFEST.json` pins canonical SHA-256 `957cee048fbdefe7d276b15d31a86074b26d3b1bb695d48843149fa3612c2eeb`. Local reconstruction of both carriers was byte-for-byte verified before Git staging.
