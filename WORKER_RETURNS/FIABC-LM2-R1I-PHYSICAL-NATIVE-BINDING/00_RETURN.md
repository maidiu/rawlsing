# FIABC-LM2-R1I — WVS7 Real-Material Physical→Native Response Binding Court

Terminal:

`BLOCKED__FIABC_LM2_R1I__REAL_PHYSICAL_TO_NATIVE_BINDING_AUTHORITY_ABSENT__NO_RAW_VALUE_INFERENCE_PERMITTED`

## Exact commission state

- repository: `maidiu/rawlsing`
- exact base: `7dd1f3a434aecd66e1774c7ea8f01b7e2c842bb3`
- branch: `agent/rabochii-premain-fiabc-lm2-r1i-physical-native-binding-court-r1`
- source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- frozen Q291 carrier SHA-256: `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`

R1I did not reopen the SAV/ZIP or perform a new source read.

## Court holding

R15 exposed a real **Layer A→B physical/native representation contradiction**.

For each of Q291G5 and Q291P5:

- realized physical key count: **9**;
- governed response-rule key count: **10**;
- exact key intersection: **0**;
- `PHYSICAL_KEYS - RULE_KEYS`: **9**;
- `RULE_KEYS - PHYSICAL_KEYS`: **10**.

Every realized Q291 physical witness is R5 `float64_finite`.

The five physically `OBSERVED_STORAGE_VALUE` keys are floats. The four physically `FORMAT_USER_MISSING_RANGE` keys are also floats.

The governed R6S rules, by contrast, are constructed from:

- five substantive Python `int` source-code constants;
- four special Python `int` source-code constants;
- one `None/SYSTEM_MISSING` rule.

Because the R5 physical key includes exact type, none of the int-built response-rule keys equals any float-built carrier key.

This explains the R15 exception exactly.

## What the court does **not** infer

R1I does **not** infer that a particular float witness has a particular native source meaning merely because its numeric display resembles a documented native code.

Therefore the court does not turn:

`float 1.0`

into:

`native code 1`

by Python equality, display resemblance, frequency, ordering, target token, or downstream expectation.

The evidence is deliberately two-sided:

- physical carrier: exact typed physical material;
- semantic/rule estate: exact native codes/states and mappings.

The missing object is the authoritative relation between those sides.

## Substantive, special, and system-missing findings

### Substantive

All five **rule-side substantive** int keys are absent from the realized physical keyspace.

All five physical `OBSERVED_STORAGE_VALUE` float keys are absent from the governed rule keyspace.

There is no accepted authority allowing R1I to pair those two sets semantically.

### Special states

All four **rule-side native-special** int keys are absent from the realized physical keyspace.

All four physically `FORMAT_USER_MISSING_RANGE` float keys are absent from the governed rule keyspace.

The rule-side special states remain exactly:

- -5 → `MISSING`
- -4 → `NOT_ASKED`
- -2 → `SOURCE_SPECIFIC_SPECIAL`
- -1 → `DK`

with:

- `canonical_value=None`;
- no R1E mapping transform authority.

R1I does not assert which physical float key corresponds to which native special state.

### System missing

The projection contains one exact `None/SYSTEM_MISSING` rule. The frozen carrier contains zero realized Q291 system-missing cells. This rule is unused, not a failure cause, and remains distinct from source user-missing codes and semantic missing states.

## Authority archaeology

No already-accepted A→B representation authority was found.

The inspected estate establishes separate facts:

- physical decoder/R5: exact type-preserving physical material;
- WVS physical expectation/R35: candidate-neutral physical evidence, explicitly **not semantic authority**;
- EE-R6A/P2F2: exact source-native response codes/states and topology;
- R1E: exact substantive native→program-token mapping;
- R1D: raw physical witness remains opaque and raw-token equivalence is not assumed.

Critically, the accepted WVS structural preimage replay gives:

- Q291G5 storage type: `null`;
- Q291P5 storage type: `null`.

The historical WVS materializer explicitly discarded storage type when it constructed the structural `PhysicalVariable` objects.

That eliminates the LiTS-N1-style P3 route: LiTS had an accepted source-specific `float` storage-type witness; WVS Q291 does not.

The current authority ontology also contains no dedicated physical→native representation authority kind.

## Repair-class disposition

- **P1 — C11 integral-float coercion:** REJECT.
- **P2 — assign rule semantics from observed carrier values:** REJECT.
- **P3 — reissue physical rules from an already-accepted WVS representation authority:** NOT AVAILABLE.
- **P4 — derive new bounded representation authority from current parents:** BLOCKED; the parent set proves both sides separately but lacks the relation itself.
- **P5 — workload/native redesign:** NOT MINIMAL; first recover the earlier A→B representation boundary.

## Earliest lawful recovery boundary

HQ must reopen only the WVS7 **physical→native representation authority boundary before R6S response-rule key construction**.

The missing premise must independently bind:

- exact WVS7 source;
- exact Q291G5/Q291P5 variables;
- exact reader/decoder/config;
- exact physical representations;
- exact native codes/states;
- negative limits forbidding global coercion, other variables/sources, canonical mapping, cross-source equivalence, and candidate parentage.

That premise cannot be manufactured from the existing carrier’s numeric resemblance.

If such a premise is later lawfully adopted, the minimal downstream reissue is R6S physical response binding material → R6S projection authority/snapshot/identity → common C11 → fresh oracle. R1E mapping authority, P2F2 workload, candidate grammar, frontier, and Lock2 remain upstream of that repair.

## Hostile court

Final GitHub/browser hostile execution:

- run: `35575217306`
- job: `106255410406`
- evidence execution SHA: `a25fead3cdfaea22aef1b18972da220fb27cdfb6`
- result: **9 passed in 301.39s**
- protocol self-court: **20 passed in 0.08s**

No R15 retry was performed.

## Changed paths

Court scaffolding/tests:

- `.rabochii/court_spec.json`
- `rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py`
- `rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py`

Return packet:

- `WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/00_RETURN.md`
- `01_PHYSICAL_KEY_INVENTORY.json`
- `02_GOVERNED_RULE_KEY_INVENTORY.json`
- `03_KEYSPACE_SET_DIFFERENCE.csv`
- `04_PHYSICAL_NATIVE_AUTHORITY_ARCHAEOLOGY.md`
- `05_REPAIR_CLASS_COURT.csv`
- `06_SPECIAL_AND_SYSTEM_MISSING_COURT.md`
- `07_MINIMAL_INVALIDATION_BOUNDARY.json`
- `08_REQUIRED_HOSTILE_REGRESSION_COURT.md`
- `RETURN.json`

No production Rawlsing implementation file was changed.

## Execution boundary preserved

- SAV/ZIP opened: 0
- new source reads: 0
- Candidate A/B/C: 0
- I03: 0
- I05: 0
- measured P2X: 0
- R15 retries: 0
- raw-value semantic inference: 0
- C11 weakening: 0
- mapping authority broadening: 0

## Terminal

`BLOCKED__FIABC_LM2_R1I__REAL_PHYSICAL_TO_NATIVE_BINDING_AUTHORITY_ABSENT__NO_RAW_VALUE_INFERENCE_PERMITTED`
