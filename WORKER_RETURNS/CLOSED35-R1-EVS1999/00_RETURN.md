# CLOSED35-R1-EVS1999 — EVS 1999 Governed Source-Specific Realization

Repository: maidiu/rawlsing

Base: agent/vozhd-closed35-l2-documentary-fanin-r1@5c582e2325ecc2b37377cd518fe4c456331c81d8

Worker branch: agent/rabochii-closed35-r1-evs1999-realization-r1

Canonical source: EVS 1999.sav

Canonical SHA-256: 6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a

Producer release authority: ZA3811 v3.0.0, DOI 10.4232/1.10789, release 2011-11-20

## Disposition

PASS at source-specific realization implementation grain.

The EVS 1999 documentary closure is now represented by an executable, candidate-neutral source law in:

- rawlsing_next/closed35_evs1999_realization.py
- rawlsing_next/tests/test_closed35_r1_evs1999_realization.py

No local/raw SAV bytes were opened. The source was not executed. No measured P2X was run.

## Implemented law

### Exact source and reader/config

The source realization pins:

- exact canonical SHA-256;
- SAV format;
- source-declared UTF-8 and character code 65001;
- explicit latin1 compatibility execution;
- pyreadstat 1.3.6 as the qualification reader-version pin;
- user_missing=True;
- apply_value_formats=False;
- no automatic encoding guessing;
- compatibility semantic scope PHYSICAL_EXTRACTION_ONLY__NO_SOURCE_TEXT_OR_SEMANTIC_AUTHORITY.

The pyreadstat version is an implementation/qualification pin, not producer encoding authority.

Compatibility decoding cannot change the source root and cannot acquire semantic jurisdiction.

### Documentary semantic ownership

The realization uses the L2-authorized producer-document precedence:

1. ZA3811 v3.0.0 Variable Report for exact integrated-data variable semantics, value dictionaries, and release-specific construction/country notes;
2. exact national field questionnaire or bilingual/national variable report for country-specific departures;
3. EVS 1999 Master Questionnaire for default wording/flow;
4. DOCUMENTARY_ALIGNMENT_UNKNOWN.

Exact source variable identifier is the alignment key.

Compatibility-rendered text is explicitly discarded as an input to semantic resolution. A readable latin1 rendering therefore has no possibility of outranking or supplementing producer documentary authority.

If an exact source-variable documentary join is absent or cannot close the requested value/text grain, the realization returns DOCUMENTARY_ALIGNMENT_UNKNOWN.

### Routing authority

Routing is resolved only through the producer documentary estate.

The source-local rule set binds the recovered v3.0.0 constructions and Master flow for:

- v49_filt;
- v50_filt;
- v51_filt;
- v290_hu;
- v87;
- v101;
- v103;
- v293;
- v296;
- v306;
- v307;
- v309;
- v315.

Observed missingness is explicitly discarded before routing resolution.

### Candidate-neutral semantic owner

The realization binds its downstream semantic owner to:

PRE553_SOURCE_BACKED_C11_FACADE@1.0.0

A, B, and C must carry the same:

- canonical source root;
- source-specific realization identity;
- documentary authority law;
- routing law;
- unresolved-alignment law.

Physical execution strategy may differ. Semantic jurisdiction may not.

### S35 physical edge classes

Exact EVS 1999 edge-class scope is frozen as:

- EC01 FORMAT_FAMILY_SAV_DTA;
- EC02 EXPLICIT_TEXT_DECODING_MODE;
- EC03 MALFORMED_DECLARED_TEXT_QUARANTINE;
- EC10 FORM_MODULE_SKIP_ROUTING_CARRIERS;
- EC14 COMPOUND_EDGE_INTERACTION_COURT.

No extra source-local edge class was invented.

### R35 physical-equivalence hooks

The source realization binds the accepted generic contracts:

- R35-I01: PRE553_PHYSICAL_METADATA@1.0.0;
- R35-I02: FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0 for every non-direct-raw realization;
- R35-I03 source scope / expectation / candidate realization / whole-source physical-equivalence receipt schemas.

Required EVS1999 physical dimensions include:

- physical_metadata;
- variable_inventory_order;
- raw_storage_values;
- row_replay_identity;
- reader_configuration_digest;
- compatibility_decode_evidence;
- form_module_skip_routing_carriers.

The generic R35 implementation branches were read as accepted implementation inputs but are not physically present in the L2-HQ base. This worker therefore binds their exact schemas and seams without silently merging or duplicating their generic code. ABC qualification must consume the accepted R35 implementation line before issuing real physical-equivalence receipts.

## Synthetic test court

Added source-independent tests proving:

- malformed compatibility text cannot become semantic authority;
- producer documentary mapping overrides readable compatibility garbage;
- unresolved labels remain DOCUMENTARY_ALIGNMENT_UNKNOWN;
- fuzzy/neighbor variable matching is forbidden;
- routing derives from producer authority, not missingness;
- release-specific routing outranks Master default at the same exact field;
- compatibility mode preserves the exact canonical source root;
- reader/config drift fails closed;
- A/B/C share one source-specific realization identity;
- exact S35 edge scope and R35 hooks remain frozen.

The tests do not open or execute EVS 1999 bytes and were not used to perform measured P2X.

## Qualification boundary

This implementation does not claim:

- real-source physical-equivalence PASS;
- source execution;
- A/B/C execution;
- measured P2X;
- malformed-text repair;
- producer checksum equivalence beyond the accepted Rawlsing source lineage.

Those belong to later qualification.

## Terminal

CLOSED35_R1_EVS1999_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION
