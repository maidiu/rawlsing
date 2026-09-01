# FFX001-B — WORKER RETURN

Experiment: `FFX001-B — RESPONDENT CARRIER / PREDICATE-EXECUTION BINDING RECONNAISSANCE`

Worker branch: `agent/rabochii-field-forge-r2-ffx001b-respondent-binding-r1`

Starting / pre-banking HEAD: `ac88a482a3623b5c711999525c49bf7c1020e5fe`

Canary: `Afrobarometer R5 Q86A–Q86F`

## Terminal ruling

`OBSERVABILITY_LIMIT__NO_EXACT_CURRENT_RESPONDENT_BINDING_ESTABLISHED_AFTER_BOUNDED_SEARCH`

Blocker subtype:

`CURRENT_RESPONDENT_BINDING_NOT_CANONICALLY_REACHABLE_FOR_Q86_CANARY`

## Exact holding

Within the bounded CURRENT governed search, no canonically reachable respondent-grain carrier/binding was established that connects the Afrobarometer R5 Q86 question implementations and their governed routing predicates to an executable respondent entity. Therefore actual respondent exposure cannot currently be materialized for this canary at the required authority grain.

This is an observability / authority-boundary holding. It is **not** a claim that Afrobarometer respondent microdata do not physically exist, nor that Rawlsing has never contained respondent data.

## What was established

1. Current C04 routing authority gives exact question-level routing rows for Q86A–Q86F, each with `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`, exact question-implementation identity, exact R5 release scope, exact predicate ID, and exact native-primary evidence reference.
2. The six current predicates compile identically to `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}` and are backed by `merged_r5_codebook_2.pdf`, SHA256 `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`.
3. Current W33/C06 Contract@2 is a deterministic current routing re-expression at question-implementation grain. Its canonical projection contains no respondent identifier, respondent entity, respondent→country binding, or respondent-level execution relation.
4. Contract@2 explicitly conserves non-projected evidence/provenance/predicate/scope authority by immutable reference to source carriers rather than synthesizing it.
5. The bounded search did not establish a separate CURRENT governed respondent carrier plus governed respondent-key/scope binding that could supply respondent-grain `COUNTRY_ALPHA3` to the Q86 predicate.
6. No respondent exposure rows were emitted.

## Exact current carrier identities used

- C04 canonical routing ledger: `library:/Rawlsing/CURRENT_ROUTING_AND_V550J_CARRIER_WAVE_R1/C04_ROUTING_ARAB_AFRO_ASIAN/C04_FULL_CURRENT_ROUTING_LEDGER.csv`
  - current source commit: `2fe01e4a9508b64f041d6bc13d3c9880661489d3`
  - rows: `3425`
  - SHA256: `c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90`
- C04 positive predicate carrier: `C04_POSITIVE_ROUTING_PREDICATES.jsonl`
  - SHA256: `78af4494282dbabc6b331e4f12dcf7df4c3c47a9cb2b5e154b9b801dcbad5576`
- C04 closure evidence index: `C04_CLOSURE_EVIDENCE_INDEX.jsonl`
  - SHA256: `6042f4f8927b6b959f4391b1ed3b7456ff70bfbe4ede0c600d98a600b9218423`
- C04 full-current court archive used to replay those sidecars: `C04_FULL_CURRENT_COURT_ARTIFACTS.tar.xz`
  - SHA256: `04297a2b9bc9297d5a79a88bb39277bf28617566ccd166c5f7ef1295d9ff1d57`
- Current Contract@2 routing carrier identity is pinned by W33 `INPUT_MANIFEST.json`:
  - rows: `18276`
  - SHA256: `5fe7fc719453479397fb759a00341dd6dc51184c8547306f7955220091405dde`
  - compiler Git blob: `71f965a792b1791fd9b8c590b4444676aded4ead`
  - hostile-test Git blob: `507cc385d5333fef25333f999807f4021b6941c9`

## Authority boundary

`PHYSICAL_DATA_EXISTENCE != CURRENT_AUTHORITY`

`HISTORICAL_EXECUTABLE_CARRIER != CURRENT_CANONICAL_RESPONDENT_BINDING`

`QUESTION_LEVEL_ROUTING_AUTHORITY != RESPONDENT_LEVEL_PREDICATE_EXECUTION`

`RESPONDENT_RESPONSE_PRESENT != PROOF_OF_EXPOSURE`

`RESPONDENT_RESPONSE_MISSING != PROOF_OF_NONEXPOSURE`

`SOURCE/WAVE_MEMBERSHIP != EXECUTABLE_RESPONDENT_JOIN`

## Smallest successor question

Determine whether consolidated/current Rawlsing contains a separately governed respondent-grain empirical carrier whose identity/scope can be losslessly bound to current `question_implementation_id` and routing-predicate authority, or whether that bridge itself remains an unmaterialized current project obligation.

Do not infer the answer from this worker.

Terminal commit: the commit containing this return and its eight sibling receipts.
