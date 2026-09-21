# FIABC-LM2-R1J-C — Authority Ontology Extension

## Holding

The current PRE553 ontology has no honest authority kind for the exact relation:

`source-native code/state -> decoder-observed physical representation`.

`SOURCE_SEMANTICS_TOPOLOGY` is ceilinged to native meaning/state/topology. `NATIVE_CANONICAL_MAPPING_HARMONIZATION` is ceilinged to native-to-program/canonical transformation. Neither may be relabeled to grant decoder representation.

Worker C therefore prepares one new, deliberately narrow kind:

`SOURCE_PHYSICAL_NATIVE_REPRESENTATION_BINDING`

with ceiling:

`exact source/variable/native-code to exact decoder representation binding`.

This is an ontology extension only. Worker C does **not** issue a real WVS7 authority instance.

## Governed operation

`BIND_EXACT_SOURCE_NATIVE_CODE_TO_DECODER_REPRESENTATION`

The operation accepts only an explicitly authorized tuple:

- exact source artifact SHA-256;
- exact physical variable ordinal + name;
- exact source-native integer code;
- exact native response state;
- exact decoder representation encoded as an R5 token;
- exact physical missing-state class;
- exact source missing declaration.

It yields the exact physical binding key by passing the **authorized decoder representation** to the unchanged `physical_value_binding_key`.

There is no observed-value coercion and no `float.is_integer() -> int` path.

## Governed object family

The authority is admissible only for `RespondentEvent@1.0.0` response binding. It does not grant coordinate, weight, routing, source-relation, or canonical-question semantics.

## Exact conditional WVS7 scope

A future real authority may be issued only if R1J-A and R1J-B independently establish the missing premises. Its maximum scope is:

- source artifact: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- Q291G5, ordinal 388;
- Q291P5, ordinal 394;
- substantive native codes 1, 2, 3, 4, 5;
- special native codes -5, -4, -2, -1;
- only the exact decoder representation class proved by the accepted A+B fan-in;
- exact source missing declaration for the special-code physical preimages.

No other integral float, variable, source, wave, or decoder lane is covered.

## Parent classes

The representation authority has exactly one semantic-authority parent:

- `EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY@1.0.0`, content hash `c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`.

It must also carry exactly two non-authority evidence dependencies:

1. accepted R1J-A upstream decoder representation law, including the 1.3.2 / 1.3.6 parity disposition;
2. accepted R1J-B exact Q291 variable-type/source-format evidence.

Those evidence objects are prerequisites, not substitutes for source semantics.

The R1E mapping authority is **not** a parent for A->B. It remains the separate layer-C transform authority for substantive response tokens only.

## Negative limits

A real authority must explicitly preserve all of the following:

- no global int/float equivalence;
- no numeric-resemblance inference;
- no inference from carrier frequencies/order;
- no other WVS variable or wave;
- no other source;
- no canonical question mapping;
- no native-to-canonical grant;
- no special-code canonicalization;
- no cross-source equivalence, pooling, linkage, or backfill;
- no coordinate/weight/design/estimand authority;
- no candidate-output parentage;
- no system-missing binding through this authority.

System missing remains the separate exact `None / SYSTEM_MISSING` R6S rule.

## Replay and interpretation fingerprint law

The interpretation fingerprint is a semantic hash over:

- the authority contract/kind/operation;
- the full exact scope envelope;
- exact parent authority refs;
- exact upstream evidence refs;
- exact negative-limit refs.

Any change to source, variable, native code, native state, decoder token, physical missing state, missing declaration, parentage, evidence, or negative limits changes the fingerprint and therefore requires a different immutable authority object.

## Validator behavior

`validate_representation_authority` fails closed unless:

- the new authority kind is exact;
- the governed operation and object family are exact;
- all representation rows are explicitly enumerated and unique;
- every row names the same exact source as the authority scope;
- source-native codes are exact R5 integer tokens;
- decoder values are exact reversible R5 tokens;
- system missing is absent;
- canonical-question/native-to-canonical/cross-source/candidate-parentage ceilings remain negative;
- the source-semantics authority is the sole authority parent;
- both independent A/B evidence classes are present;
- the interpretation fingerprint replays exactly.

## Why R5 and C11 remain unchanged

`R5TypedValueCodec` already correctly distinguishes integer and float lanes. `physical_value_binding_key` already correctly includes exact typed representation. C11 already correctly requires exact physical-key lookup and refuses semantic inference.

The defect exposed by R1I is therefore not in those mechanisms. It is in the missing authority-gated R6S preimage construction. The repair belongs immediately before R6S creates each response rule key.
