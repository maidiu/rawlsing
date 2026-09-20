# CLOSED35-R1-EVS1999 — Realization Contract

Schema: CLOSED35_R1_EVS1999_SOURCE_REALIZATION@1.0.0

## 1. Court object

This contract defines the one lawful EVS 1999 source-specific semantic realization that Candidates A, B and C must share.

Physical realization is allowed to vary by candidate. Source identity, documentary jurisdiction, routing jurisdiction, unknown-state behavior and downstream semantic ownership are invariant.

The source-specific relation is:

exact canonical EVS 1999 root
-> exact physical reader/config
-> physical-only compatibility extraction
-> exact source-variable identity
-> producer ZA3811 v3.0.0 documentary authority
-> candidate-neutral source-backed C11 semantic surface.

The forbidden shortcut is:

latin1 compatibility rendering
-/-> semantic label, value meaning, routing meaning, or text repair.

## 2. Canonical source identity

Canonical filename: EVS 1999.sav

Canonical SHA-256: 6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a

Format: SAV

Replay identity: SOURCE_SHA256+ROW_ORDINAL

Producer release identity:

- European Values Study 1999 integrated dataset;
- ZA3811;
- version 3.0.0;
- release date 2011-11-20;
- DOI 10.4232/1.10789.

The Rawlsing canonical SHA is the physical source root. ZA3811 v3.0.0 is the producer documentary release identity accepted by L2. Neither may be replaced by a same-wave file, national revision, trend file, alternate export, or compatibility-decoded derivative.

## 3. Exact reader/config contract

Qualification reader/config is frozen to:

- decoder implementation: rawlsing_next/pre553_physical_decoder.py;
- reader: pyreadstat.read_sav;
- reader/runtime version pin: pyreadstat 1.3.6;
- encoding override: latin1;
- user_missing=True;
- apply_value_formats=False;
- automatic encoding guessing/fallback forbidden;
- source-native declared encoding: UTF-8;
- source-native character code: 65001;
- compatibility mode: SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8;
- compatibility semantic scope: PHYSICAL_EXTRACTION_ONLY__NO_SOURCE_TEXT_OR_SEMANTIC_AUTHORITY;
- semantic_authority=False.

The version pin is execution identity, not producer authority. Any later reader revision requires a new governed config identity and qualification.

Changing encoding, reader version, missing-state mode, value-format application, decoder implementation or compatibility semantic scope changes the reader/config identity and fails this realization contract until requalified.

## 4. Malformed-text quarantine

The canonical SAV's malformed human-language metadata remains physical evidence.

No operation in this realization:

- repairs malformed embedded bytes;
- declares latin1 the true source encoding;
- normalizes compatibility-rendered strings;
- fuzzy-matches compatible-looking labels;
- uses readability as a semantic tie-breaker.

Compatibility-rendered text may be logged as physical/debug evidence only.

The semantic resolver deliberately discards compatibility_rendered_text before documentary resolution.

## 5. Producer documentary alignment

The authority order is fixed.

### Tier 1 — integrated release authority

ZA3811 v3.0.0 Variable Report.

Owns, after exact source-variable alignment:

- data-file variable semantics;
- producer variable labels;
- value/value-label dictionaries;
- release-specific construction notes;
- release-specific country notes;
- producer-published corrected/standardized labels.

### Tier 2 — exact national authority

National field questionnaire, bilingual variable report, or national variable report.

Owns only exact country-specific wording or deviation at an established country + variable/question join.

### Tier 3 — Master default

EVS 1999 Master Questionnaire.

Owns default wording and questionnaire flow only where no higher-precedence exact release/national rule governs.

### Failed join

If an exact join cannot be made:

DOCUMENTARY_ALIGNMENT_UNKNOWN

No neighboring variable, apparent cognate, readable compatibility string, frequency pattern, missingness pattern or national revision may fill the gap.

## 6. Projection binding

The source-local authority module does not fabricate a 513-variable logical release without executing the source.

Instead it supplies the authority resolver that later materialization uses to populate the generic source-backed C11 facade.

For a physical source slot to acquire semantic projection:

1. the physical slot retains exact source variable identity;
2. exact variable identity joins to an admitted producer documentary entry;
3. requested raw-value semantics, if any, join to that exact variable's documentary dictionary;
4. question/topology/routing authority is attached from the admitted producer document;
5. unresolved grains remain DOCUMENTARY_ALIGNMENT_UNKNOWN;
6. only then may the generic C11 projection emit its governed logical object.

Compatibility labels are never an alignment key.

This is sufficient for Candidate A/B/C qualification because all candidates target the same authority resolver and the same PRE553_SOURCE_BACKED_C11_FACADE@1.0.0 semantic owner, while their physical delivery paths remain independently testable.

## 7. Routing and filter authority

Routing precedence:

1. exact ZA3811 v3.0.0 construction/country note;
2. exact national document;
3. Master default;
4. DOCUMENTARY_ALIGNMENT_UNKNOWN.

Source-local recovered rules include v49_filt, v50_filt, v51_filt, v290_hu and the documented Master skips for v87, v101, v103, v293, v296, v306, v307, v309 and v315.

Observed physical missingness is not an input to the routing decision. The resolver accepts it only to prove that it has no authority and then discards it.

A routing rule that is not documentary-aligned remains unknown rather than being derived from:

- user-missing incidence;
- system missing;
- variable name;
- compatibility label;
- row-frequency pattern;
- source layout.

## 8. S35 physical edge scope

Applicable exact edge classes:

EC01 — FORMAT_FAMILY_SAV_DTA

Requires baseline whole-source physical identity and preservation of physical metadata, ordered variable inventory, raw storage values and row replay identity.

EC02 — EXPLICIT_TEXT_DECODING_MODE

Requires exact reader/config identity. Automatic encoding discovery/fallback is forbidden.

EC03 — MALFORMED_DECLARED_TEXT_QUARANTINE

Requires compatibility-decode evidence and the physical-only semantic-scope tag. Compatibility text remains nonauthoritative.

EC10 — FORM_MODULE_SKIP_ROUTING_CARRIERS

Requires physical preservation of routing/filter carriers while routing itself is supplied only by producer documentary authority.

EC14 — COMPOUND_EDGE_INTERACTION_COURT

Requires simultaneous survival of EC01, EC02, EC03 and EC10. It adds no new semantics and no EVS-specific physical adapter.

## 9. R35 hooks

### R35-I01

Required schema:

PRE553_PHYSICAL_METADATA@1.0.0

The qualification receipt must preserve raw-layout/file/display/reader metadata and its canonical digest. Equality of semantic outputs cannot substitute for this physical evidence.

### R35-I02

Required for any non-DIRECT_RAW realization:

FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0

A persisted compatibility-decoded copy or other derivative cannot become a source merely because it asserts the canonical SHA. Its immutable parentage must close to the exact canonical root through the accepted generic receipt chain.

### R35-I03

Required schemas:

- FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0;
- FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0;
- FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0;
- FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0.

Required EVS1999 dimensions:

- physical_metadata;
- variable_inventory_order;
- raw_storage_values;
- row_replay_identity;
- reader_configuration_digest;
- compatibility_decode_evidence;
- form_module_skip_routing_carriers.

All R35 hooks are physical/provenance-only and have semantic_authority=False.

## 10. A/B/C invariant

Each candidate binding must contain the same:

- canonical source SHA;
- source-specific realization identity;
- producer release identity;
- documentary alignment law;
- routing law;
- unknown-state behavior;
- generic semantic owner surface.

The implementation computes one deterministic SOURCE_SPECIFIC_REALIZATION_IDENTITY from that complete source law.

Qualification requires the exact candidate set A, B and C to carry that same identity.

Candidate-specific physical optimization may change cost and representation. It may not change source meaning.

## 11. Failure law

Wrong/unproved source root:
BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED

Noncanonical alternate source:
BLOCKED__ALTERNATE_SOURCE_SUBSTITUTION

Non-direct derivative without R35-I02 closure:
BLOCKED__DERIVATIVE_LINEAGE_TO_CANONICAL_ROOT_UNPROVED

Compatibility decoding promoted to semantic authority:
BLOCKED__COMPATIBILITY_DECODE_PROMOTED_TO_SEMANTIC_AUTHORITY

Requested semantic grain lacks exact documentary join:
- preserve DOCUMENTARY_ALIGNMENT_UNKNOWN where the workload permits typed unknown;
- otherwise BLOCKED__REQUIRED_SOURCE_SEMANTIC_AUTHORITY_MISSING.

Candidate semantic-law divergence:
BLOCKED__SEMANTIC_OWNER_DIVERGENCE

Candidate lacks an executable physical binding despite common source law:
BLOCKED__CANDIDATE_RUNTIME_BINDING_MISSING

## 12. Integration boundary

The exact L2-HQ base contains S35-3/S35-4 and the generic source-backed C11 facade, but not the later R35-I01/I02/I03 implementation files.

This worker read those accepted R35 worker branches and binds their exact schemas/interfaces. It does not merge or duplicate their generic implementations.

Therefore later ABC qualification must first consume the accepted R35 generic implementation line, then materialize EVS1999 physical receipts against this source-specific law.

No real-source physical-equivalence PASS is claimed here.
