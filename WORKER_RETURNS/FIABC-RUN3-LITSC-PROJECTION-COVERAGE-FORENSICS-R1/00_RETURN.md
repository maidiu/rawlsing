# FIABC RUN3 — LiTS/C Projection Coverage and Representation Authority Forensics — R1

Status: COMPLETE — documentary/GitHub forensics only

Base / measured execution head: bc832181b4284ac110d2be44fc83504e04de081e

Owned branch: agent/rabochii-fiabc-run3-litsc-projection-coverage-forensics-r1

No raw LiTS/WVS respondent-level source was opened, materialized, decoded, or inspected. No Candidate A/B/C process, I03/I05 real-source execution, or measured P2X was run. No production code was modified.

## Terminal classification

RUN3_LITSC_VOID_AS_CANDIDATE_EVIDENCE__COMMON_PROJECTION_OR_REPRESENTATION_DEFECT_PROVED

RUN3 LiTS/C S01 is not admissible as Candidate-C-local correctness evidence. The throwing line is in the common source-backed C11 projection seam, and the repository already contains an accepted LiTS representation court proving that the qualified DTA decoder produces q301 response values in a float64 physical lane while the governed projection bound at RUN3 carries Decimal-keyed response rules. The accepted candidate-neutral LiTS oracle route explicitly applies a bounded representation authority and projection-owner adaptation before replay. The measured RUN3 backend does not apply that authority/adaptation on the Candidate-C S01 path.

The defect is therefore a common LiTS typed-representation / projection-key-domain integration defect. Candidate C reaches it first because its S01 realization directly feeds the decoded PhysicalSourceIncidence into the current source-backed facade.

## 1. Exact physical binding law at the measured head

Current measured facade:

- path: rawlsing_next/pre553_source_backed_c11_facade.py
- measured-head blob: 8a761119e4a8d68eb291fc4edfadb52e027f8284
- contract: PRE553_SOURCE_BACKED_C11_FACADE@1.0.0
- physical binding schema: PRE553_PHYSICAL_VALUE_BINDING@2.0.0
- typed codec: PRE553_R5_TYPED_VALUE_CODEC@1.0.0

At bc832181..., physical_value_binding_key(raw_value, missing_state, declaration) constructs exactly:

1. Normalize missing_state to its PhysicalMissingState string value.
2. R5TypedValueCodec.encode(raw_value).
3. R5TypedValueCodec.encode(declaration).
4. Form the canonical material:
   - schema = PRE553_PHYSICAL_VALUE_BINDING@2.0.0
   - codec = PRE553_R5_TYPED_VALUE_CODEC@1.0.0
   - raw_value = exact R5 typed token
   - physical_state = normalized missing-state string
   - source_missing_declaration = exact R5 typed token
5. Serialize with the R5 canonical JSON byte law.
6. SHA-256 the canonical bytes.

The execution-side _cell_key(cell) calls that exact function over:

- cell.raw_value
- cell.missing_state
- cell.source_missing_declaration

The response lookup then constructs:

by = {rule.physical_key: rule for rule in slot.values}

and performs exact hash lookup. On absence it raises:

SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference

There is no fallback equivalence relation.

### Typed representation consequences

R5TypedValueCodec intentionally distinguishes host/physical types.

- int -> int/int_escape token
- finite float -> float64_finite with exact IEEE-754 bits
- Decimal -> decimal with sign/digits/exponent
- str -> str
- None -> none
- mappings, including missing declarations, are recursively typed and canonicalized

Therefore numerically equal int, float, Decimal, and string values are not interchangeable physical keys. Decimal("1.0") and Decimal(1) are also distinct because the Decimal tuple exponent is retained.

## 2. Exact governed response-map construction law

RUN3 LiTS projection construction is in ee_p2x_darwin_stage_backend._lits_projection.

The measured backend:

- pins LITS_BANKED_COMMIT = 3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f;
- deploys the banked AS2B builder:
  data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2b/run_as2b_lits1_mechanical_certification.py
- pins builder blob c51b56779ab9d79126619b7733d41f5253c8150f;
- copies the accepted AS2A slot ledger and source-specific projection authority package;
- calls read_banked_authority() and build_projection(...);
- fails closed unless projection.cache_identity equals:
  84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872

The AS2B build_projection response rules are exactly scoped to:

- q301_2 / ordinal 194
- q301_7 / ordinal 199

For each slot it constructs rules for values 1..7 using Decimal(value):

- 1..5 -> SUBSTANTIVE_RESPONSE
- 6..7 -> SOURCE_SPECIFIC_SPECIAL
- None + SYSTEM_MISSING -> MISSING

Each rule's physical_key is produced by physical_value_binding_key(...). Because the old builder is loaded into the current measured process and imports the current facade law, these current governed rules are typed R5 keys over Decimal(code), not decoder-native float64 keys. The representation authority records the governed-rule Decimal tokens as exponent 0.

The calls omit the declaration argument, so the governed response rules bind source_missing_declaration = None.

### Equality audit for the exact q301 scope

The previously accepted LiTS representation diagnostic closes the dimensions independently:

- raw-value representation: NOT identical. Qualified decoder-native response cells are float64; current governed response rules are Decimal.
- missing-state representation: identical for the authorized scope. Observed response cells use OBSERVED_STORAGE_VALUE; system missing uses SYSTEM_MISSING.
- source-missing declaration representation: identical for the authorized scope. The representation authority requires None for the admitted observed cells and exact system missing.
- numeric host-language representation: intentionally non-equivalent under the current typed key law.
- string representation: a separate lane; no numeric/string equivalence exists or is authorized.

Thus the proved defect is not an unclosed missing-state or source-missing-declaration semantic question. It is the raw physical representation/key-domain mismatch.

## 3. Projection authority genealogy

### AS2A source-specific authority

Accepted source-specific package:

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json

Projection authority content hash:

9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06

Slot ledger:

.../banked_as2a/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv

Slot ledger SHA-256:

65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60

The package binds the exact LiTS-I source SHA:

7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09

and records the compatibility decoder call decode_dta(source_path, encoding="latin1"), while explicitly denying that this is source-text encoding authority.

It owns two bounded proving response slots, five coordinate slots, zero weight slots, and excludes the remaining source slots from this bounded projection.

### AS2B mechanical certification / historical accepted B

The banked AS2B builder used a compatibility helper:

exact_cell(cell): float -> Decimal(str(float))

before sending response cells to the historical source-backed facade.

Historical accepted Candidate-B C11 evidence:

WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json

records:

- owner commit: 0b96b8de9aac774566f872cf0630ebd4ddeb70e6
- owner blob: 7c509c2098d0030f253344eb3f682471378812a8
- projection identity: 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872
- accepted C11 release: e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26
- accepted replay: 6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd
- status: PASS

The historical owner used the older physical-key law:

semantic_hash({"raw": canonicalize(raw_value), "physical_state": state, "declaration": canonicalize(declaration)})

This is a different hash domain from PRE553_PHYSICAL_VALUE_BINDING@2.0.0.

### Current typed-facade transition

At the measured head the repository copy of pre553_source_backed_c11_facade.py is blob:

8a761119e4a8d68eb291fc4edfadb52e027f8284

It replaces the historical numeric-equivalence/canonicalize key behavior with exact R5 typed physical material. That transition is intentional and global; it is not lawful to silently coerce int/float/Decimal back together.

### LiTS representation blocker and diagnostic

WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/09_LITS_REPRESENTATION_BLOCKER_HOLDING.md documented the same exception in the candidate-neutral preflight and held:

LITS PHYSICAL/NATIVE REPRESENTATION AUTHORITY NOT YET CLOSED FOR THE CURRENT TYPED PHYSICAL-KEY CONTRACT.

The accepted candidate-neutral diagnostic then produced receipt SHA-256:

74fc2c53610ad2af5867e4c36728604a812cf9ad3d7b0e4bceebda68fe4ac74b

The closure in 10_LITS_REPRESENTATION_AUTHORITY_CLOSURE.md records:

- exact q301_2/194 and q301_7/199 scope;
- 58,004 response cells;
- 57,989 observed cells in the seven exact float64 code-token classes;
- 15 exact system-missing cells;
- no observed float64 response cell matched the current Decimal-keyed response rules;
- the old Decimal(str(value)) helper also did not match the current typed Decimal rule tokens because Decimal exponent -1 and exponent 0 are distinct under R5TypedValueCodec.

This is direct prior adjudication of the representation mismatch RUN3/C has rediscovered.

### Bounded representation authority

Production module:

rawlsing_next/fiabc_lits_i_representation_authority.py

Authority kind:

PHYSICAL_NATIVE_REPRESENTATION_BINDING

Authority content hash:

9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d

Authority snapshot hash:

9ac03b6d6e1464da29018ad1e6e803c490ff652a1ec4d9b18691b3e82d98ec7b

The authority enumerates only:

- exact LiTS-I source SHA;
- q301_2/194 and q301_7/199;
- seven exact decoder float64 bit patterns;
- seven exact accepted banked Decimal("N.0") witnesses;
- exact system missing;
- exact qualified reader/runtime configuration;
- exact historical facade owner, projection, C11 release, and replay.

Negative limits expressly include:

- NO_GLOBAL_INT_FLOAT_DECIMAL_COERCION
- NO_CURRENT_TYPED_KEY_EQUIVALENCE
- NO_LABEL_OR_FREQUENCY_AUTHORITY
- NO_MISSINGNESS_INFERENCE
- NO_RESPONSE_SEMANTIC_REMAP

Source-free qualification at d1833f9ebe363258575c6bd95737eb8f1b0f4154 passed the governed court and preserved projection identity 84361298....

### Legacy physical-key owner adaptation

A subsequent candidate-neutral rerun exposed the next representation seam: current typed projection key strings cannot simply be handed to the pinned historical facade, because the historical facade hashes the same accepted physical representation under a different key law.

WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/16_LITS_LEGACY_PHYSICAL_KEY_CLOSURE.md records the bounded projection-owner adaptation. Code head ea0baa4d87244a548ba9a6a46a883d307c65e3e4 converts only the authorized q301 response keys and declared system-missing coordinate bindings into the historical owner's key domain. Qualification closure:

4c1641d1f1ec51a4116d0664dbf149e915465bdb

No global key-law change was made.

### Current candidate-neutral oracle path

rawlsing_next/fiabc_final_oracle_freeze_producers.py imports:

- authorized_replay_cell from fiabc_lits_i_representation_authority;
- the bounded representation authority snapshot/material;
- the pinned historical facade owner.

Its _lits_accepted_legacy_projection() converts exact current governed response-rule keys into the pinned historical owner's key domain.

Its _lits_accepted_legacy_base_candidate() builds an ExactPhysicalCellStream that applies:

decoder-native PhysicalCell
-> authorized_lits_replay_cell(...)
-> banked exact_cell(...)
-> pinned historical facade

and fails closed unless the accepted base C11 release and replay identities are reproduced exactly.

This is not speculative: the final source-backed canonical LiTS closure succeeded and retained representation authority 9fce3b... in its authority closure. The final ASTRA substantive parity receipt also passed, while explicitly keeping historical/current native hash domains distinct.

### Canonical empirical closure / ASTRA-current parity

The later canonical LiTS closure retains the bounded representation authority and current PRE553 canonical objects in checkpoint v3.

Final durable source-retry evidence records:

- representation authority 9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d;
- runtime catalog 5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02;
- authority closure PASS;
- current/ASTRA substantive parity PASS;
- no candidate process/output as oracle parentage.

ASTRA-D04-R2 remains a historical regression anchor, not the current physical-key identity domain. The later ASTRA hash-domain repair explicitly rejected cross-schema object-hash equality.

## 4. What RUN3 measured backend actually binds

At bc832181..., ee_p2x_darwin_stage_backend.py hard-binds:

LITS_PROJECTION = 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872

Its _lits_projection() reconstructs that projection with the banked AS2B builder under the current typed facade law.

For Candidate C, _compose_lits() calls _compose_current_candidate_c(...).

rawlsing_next/pre553_candidate_c_production_binding.py then:

- requires exact LiTS source SHA;
- requires projection identity 84361298...;
- declares zero applicable accelerators for the current LiTS workload;
- uses EXACT_SOURCE_BACKED_FALLBACK_FOR_CURRENT_F02;
- calls build_source_backed_c11_repository(source, projection, cache=None).

Because that module imports the repository's current facade, C's S01 physical response cells are keyed under PRE553_PHYSICAL_VALUE_BINDING@2.0.0 exactly as decoder-native values.

Critically, the measured backend contains no invocation of:

- fiabc_lits_i_representation_authority;
- authorized_replay_cell;
- the candidate-neutral producer's legacy projection-owner adaptation.

So RUN3/C passes decoder-native float64 physical response cells directly against Decimal-keyed governed response keys. That is the already-proved mismatch.

## 5. A/B/C commonality

### Candidate C

C has no candidate-specific semantic decision at the throwing point. Its production binding explicitly states that Candidate C owns a physical realization policy while empirical semantics remain with the common source-backed C11 owner. With no applicable accelerator, C delegates directly to the common facade. The exception occurs there.

Therefore the observed S01 failure is not Candidate-C-local correctness evidence.

### Candidate B

The measured driver pins Candidate B to:

- owner commit 0b96b8de...
- pre553_source_backed_c11_facade.py
- blob 7c509c2098d0030f253344eb3f682471378812a8

That is the historical facade/key-law owner.

B currently has an earlier type-universe/class seam under separate adjudication. Once that seam is crossed, merely handing the current projection's physical-key strings to the historical owner is still invalid. This exact condition was already proved by 16_LITS_LEGACY_PHYSICAL_KEY_CLOSURE.md: current typed projection keys and historical facade keys inhabit different physical-key hash domains.

Therefore B would encounter the shared projection/representation seam after a type-only repair unless that repair also lawfully imports the already-qualified projection-owner adaptation and representation authority.

### Candidate A

Candidate A is pinned to pre553_r5_source_backed_adapter.py blob d4915e7e6755ba1850756aebff72f982f73a332b.

The R5 seam encodes PhysicalCell.raw_value with R5TypedValueCodec and the adapter decodes it exactly, verifies re-encoding equality, reconstructs PhysicalCell, and feeds the common source-backed facade. It does not perform float/Decimal semantic coercion.

Thus a current R5 carrier built from the qualified decoder preserves the native float representation. Once A's earlier provenance/parentage seam is crossed, A is exposed to the same common q301 typed-key mismatch unless the common representation adaptation has been integrated before C11 lookup.

### Common conclusion

C reaches the shared failure earliest because its S01 source-backed fallback directly enters the common physical->C11 projection path. A and B have independent earlier seams that mask the same downstream representation integration defect.

No A/B/C ranking follows from this result.

## 6. Exact RUN3 first failing physical key

The repository evidence examined does not bank the exact first RUN3 row/key that threw inside the live C S01 process.

EXACT_RUN3_FAILING_PHYSICAL_KEY_REQUIRES_READ_ONLY_LOCAL_FORENSIC_EXTRACTION

This extraction is confirmatory/localizing evidence only. The common defect classification does not depend on it because the exact source/slot representation incompatibility was independently established by the earlier governed LiTS diagnostic and the measured backend's omission of its accepted bridge is documentary fact.

A read-only Codex extraction from the retained RUN3 S01 failure state/receipt should emit only:

- stage address and exception provenance;
- variable name and ordinal;
- row ordinal only as necessary to localize the first failing cell;
- canonical current physical_value_binding_key hash;
- raw-value representation TYPE/TAG only (for example the R5 token class), not an interpretation of the value;
- physical missing-state value;
- exact canonical source-missing-declaration representation;
- projection identity;
- sorted available governed physical-key hashes for that response slot;
- boolean membership of the failing key in that map;
- facade/module blob and owner/provenance used by the throwing process.

Do not ask Codex to report a label, frequency, inferred response meaning, inferred missingness meaning, or semantic translation of the raw value. Do not reread or decode the source solely for this extraction.

## 7. Adjudicated failure scope

Primary scope:

COMMON TYPED-REPRESENTATION INCOMPATIBILITY AT THE LITS PHYSICAL->C11 BINDING SEAM

Concrete integration defect:

THE MEASURED RUN3 BACKEND BYPASSES THE ALREADY-ACCEPTED LITS REPRESENTATION AUTHORITY / PROJECTION-OWNER ADAPTATION THAT THE CANDIDATE-NEUTRAL ORACLE PATH REQUIRES.

Not established:

- Candidate C local correctness defect;
- missing LiTS response semantics;
- incomplete source-semantic response-option coverage;
- decoder corruption;
- a lawful generic numeric equivalence.

Projection coverage is semantically closed for the authorized q301 scope but physically incomplete in the measured current typed-key domain. The earlier diagnostic found that only exact system missing matched the current Decimal-keyed rules, while observed decoder-native float64 response cells did not.

## 8. Minimal lawful repair invariant

The repair must be common and authority-preserving, not Candidate-C-specific.

Invariant:

Every LiTS path that binds decoder-native q301 physical cells to governed C11 response slots must place the physical cell and the response-slot rule in the SAME authority-sanctioned physical-key domain before exact lookup.

There are only two lawful categories visible in current repository authority:

1. Reuse the already-qualified accepted replay route:
   - apply only representation authority 9fce3b... within its exact source/slot/type/state/declaration scope;
   - apply the already-qualified projection-owner adaptation when replaying through the pinned historical facade;
   - reproduce the accepted C11 identities exactly;
   - expose the resulting common C11 repository to candidate realization without making a candidate the semantic owner.

2. If measured architecture requires the current PRE553_PHYSICAL_VALUE_BINDING@2.0.0 facade directly, issue and qualify a NEW common projection/representation authority whose response-slot physical keys enumerate the decoder-native float64 representations. That reissued authority must prove exact semantic/replay conservation and may not claim the old projection identity unless identity law actually permits it.

The existing 9fce3b... authority alone does NOT authorize a shortcut from float64 to current typed Decimal equality; its negative limits expressly deny NO_CURRENT_TYPED_KEY_EQUIVALENCE.

## 9. Qualification plan

Before another measured LiTS candidate result can be admitted:

1. Source-free representation court
   - instantiate the accepted 84361298... projection from banked authority;
   - use only authority-enumerated synthetic/fixture float64 tokens and system missing;
   - prove the repaired common seam binds every authorized representation and rejects adjacent types/tokens/states/declarations.

2. Cross-owner key-domain court
   - if the historical facade remains in any candidate route, prove current->legacy projection-key adaptation is exact and bounded;
   - reject any unlisted slot/key.

3. Commonality court
   - prove A, B, and C ultimately consume the same semantic C11 truth surface after their carrier-specific realization;
   - candidate ownership may change physical realization only, never response meaning.

4. Identity conservation
   - preserve/reproduce the accepted source identity;
   - preserve the correct projection authority lineage;
   - reproduce required accepted C11 release/replay identities where the accepted replay route is used;
   - preserve runtime catalog and current successor release identities;
   - keep ASTRA comparison in its explicit cross-schema logical domain.

5. Hostile representation tests
   - reject int for float, Decimal exponent drift, string numerics, neighboring float bits, altered declarations, altered missing states, other variables, other waves, and other sources.

6. Full governed source-free qualification
   - no source read;
   - no candidate execution;
   - no measured P2X.

7. Only after adoption/guard rebinding may HQ perform a fresh measured retry. The old RUN3/C terminal must remain void as candidate evidence.

## 10. Explicitly prohibited shortcuts

- No generic int/float/Decimal coercion.
- No use of label text or frequency to assign response meaning.
- No inference of missingness from a raw value.
- No hard-coding of the first observed failing raw value.
- No Candidate-C-only semantic patch.
- No mutation of the global PRE553 typed physical-key law merely to recover historical numeric equality.
- No reuse of a historical projection identity for changed key material without proving that identity law authorizes it.
- No treatment of ASTRA historical hashes as current PRE553 native hashes.
- No source reread to obtain the exact RUN3 first-failing key when retained RUN3 evidence can be inspected read-only.
- No interpretation of the extracted key/value as a human response meaning.

## Final holding

RUN3/C did real measured work, but the result stopped at a shared, already-known representation authority seam that the measured backend failed to integrate. The generic wrapper CANDIDATE_LOCAL_FAILURE is therefore overbroad for this event.

Terminal:

RUN3_LITSC_VOID_AS_CANDIDATE_EVIDENCE__COMMON_PROJECTION_OR_REPRESENTATION_DEFECT_PROVED
