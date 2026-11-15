# VC4 C02 — C11 DERIVABILITY & MINIMUM PERSISTENCE COURT

Status: `PREPARED__NOT_LAUNCHED`
Branch: `agent/vozhd-chetiri-c02-c11-derivability`
Write scope: `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C02/`
Runtime writes: `FORBIDDEN`
Raw source probing: `TARGETED_METADATA_ONLY__HQ_PINNED_IF_NEEDED`

## MISSION

Determine, field by field and obligation by obligation, what C11 information must persist separately from exact source bytes + governed authority, and what can be reconstructed exactly on demand.

Do not assume that source-cell geometry equals semantic event identity. Do not assume that current R5 physical layout is semantically required.

## DEPENDENCIES

None beyond campaign launch and common contract.

## ADDITIONAL READ-FIRST

Read C11 schema/constructors/integrity/repository code and tests; source constitution; decoder contract; current ExactRef/content-hash rules; relevant topology/routing/weight/design authorities.

## EXACT PROCEDURE

1. Enumerate M01–M18.
2. Map each obligation to every concrete C11 field/relation currently needed to satisfy it.
3. For each field/relation, identify the smallest exact determinant set.
4. Identify authority proving the determinant relation and exact scope.
5. Define deterministic reconstruction function.
6. Enumerate exception domain; if unbounded/unknown, do not claim derivability.
7. State integrity binding required to make reconstruction trustworthy.
8. Classify persistence using the frozen vocabulary.
9. Test hostile cases: missingness classes, signed zero/types, strings/control text, topology, routing, zero-incidence metadata, weights/design, source relations, ExactRef, future open-world queryability.
10. Apply no-starvation and terminal vision checks.

## REQUIRED MATRIX COLUMNS

`m_obligation,logical_relation,field_or_fact,semantic_owner,determinants,determinant_authority,scope,reconstruction_function,exception_domain,integrity_binding,persistence_class,hostile_case_coverage,consumer_needs,terminal_risk,unresolved`

## ABSOLUTE DERIVABILITY RULE

A field is not derivable merely because:

- all observed rows agree;
- current WVS/LiTS files are rectangular;
- current code reconstructs it heuristically;
- the value can be inferred from variable name or label;
- current I03/I05 tests do not exercise it;
- event occurrence often equals source cell.

Derivability requires exact law.

## REQUIRED HOSTILE CASES

- SAV system missing vs user-missing declarations/ranges;
- DTA system missing vs `.a`–`.z` extended missing;
- empty string vs null;
- finite `-0.0` where exposed;
- integer/float/text type identity;
- Unicode/control/NUL text;
- repeated/ranked/componentized/multiple-response topology;
- source-cell locator != event occurrence identity;
- routed-out/applicable/observed distinctions;
- weight/design/estimand authority;
- zero-incidence variable declarations;
- cross-source relation/nonduplication provenance;
- deterministic content hash/ExactRef;
- unforeseen future lawful predicates.

## REQUIRED OUTPUTS

- `C11_MINIMUM_PERSISTENCE_MATRIX.csv`
- `SOURCE_BACKED_C11_INFORMATION_PROOF.md`
- `IRREDUCIBLE_PERSISTENCE_WITNESSES.md`
- `C02_RESULT.json`
- common return files.

`IRREDUCIBLE_PERSISTENCE_WITNESSES.md` must say `NONE` if none.

## FINAL DISPOSITIONS

- `C02_PASS__C11_RECONSTRUCTABLE_FROM_SOURCE_PLUS_GOVERNED_SIDE_MATERIAL`
- `C02_PASS__SPARSE_CANONICAL_EXCEPTION_MATERIAL_REQUIRED`
- `C02_BLOCK__IRREDUCIBLE_EVENT_GRAIN_PERSISTENCE_REQUIRED`
- `C02_BLOCK__UNRESOLVED_DERIVABILITY`
- `C02_BLOCK__TERMINAL_STARVATION_OR_LEAKAGE`

STOP token: `VC4_C02_RETURNED`
