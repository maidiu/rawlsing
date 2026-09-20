# FIABC-LM1-R1D-C required regression court

Status: TESTS_AUTHORED__NOT_EXECUTED

This worker is GitHub/browser-only. The following suite is the minimum hostile regression court that must pass after the narrow C11 physical-boundary repair and before the one-success replacement authority is consumed.

## Court premise

The repair may change only the representation of physical binding/raw-witness material. It may not widen generic semantic canonicalization, assign semantic missingness, alter source cells, change candidate-specific semantics, or rebuild R5.

The accepted physical mechanism is PRE553_R5_TYPED_VALUE_CODEC@1.0.0. Generic pre553_empirical_objects.canonicalize() must continue to reject Python float values in semantic identity.

## R1 — exact physical token court

For each case, obtain the physical token through the accepted R5 typed-value codec and verify deterministic canonical bytes.

Required cases:

1. finite positive float 1.5 -> float64_finite / 3ff8000000000000;
2. finite negative float -2.25 -> float64_finite / c002000000000000;
3. +0.0 -> bits 0000000000000000;
4. -0.0 -> bits 8000000000000000;
5. decoder-observed NaN -> float64_nan_decoder_state only;
6. +Infinity -> float64_pos_inf;
7. -Infinity -> float64_neg_inf;
8. integer 1 versus float 1.0 -> distinct typed material;
9. bool True versus integer 1 -> distinct typed material;
10. string "inf" versus float +Infinity -> distinct typed material;
11. Unicode strings with different code-point sequences -> remain distinct if the decoder produced distinct strings.

Reject any implementation that invents a NaN payload or normalizes signed zero.

## R2 — global semantic ban must remain intact

Direct calls to generic C11 canonicalize() with:
- finite Python float,
- NaN,
- +Infinity,
- -Infinity

must still raise Pre553IntegrityError with the existing float/NaN/Infinity prohibition.

This test is mandatory because a repair that merely makes downstream objects pass while silently widening canonicalize() is a court failure.

## R3 — physical_value_binding_key

For the repaired physical-value key function:

- same typed physical value + same PhysicalMissingState + same physical declaration material -> same key;
- any change in finite float bits -> different key;
- +0.0 and -0.0 -> different keys;
- NaN decoder state and either infinity -> different keys;
- +Infinity and -Infinity -> different keys;
- integer 1 and float 1.0 -> different keys;
- bool True and integer 1 -> different keys;
- string "inf" and float +Infinity -> different keys;
- physical missing/declaration state remains part of the key;
- no raw float is sent through semantic canonicalize().

If the source-missing declaration contains physical numeric material, it must be represented through the same accepted typed physical mechanism rather than being semantically retyped.

## R4 — response raw-witness seam

Construct a source-backed response projection with a governed ResponseValueRule whose physical key matches a finite float and another whose key matches a non-finite physical state.

Verify:

- lookup succeeds only on exact physical key;
- RespondentEvent.raw_response_value carries typed physical witness material rather than a Python float;
- canonical_response_value_if_authorized still flows through existing semantic canonicalization;
- a binary float placed in the canonical semantic value without authority still fails;
- no NaN/Infinity becomes missing, UNKNOWN, or None;
- response event replay identity is deterministic across repeated runs.

## R5 — coordinate raw-witness seam

Exercise both:
- explicit CoordinateValueRule;
- copy_observed_raw=True for an observed physical value.

Verify:

- raw_coordinate_value carries typed physical witness material;
- canonical coordinate value remains separately governed;
- +0.0 and -0.0 do not alias;
- an unbound/missing coordinate still cannot acquire semantics;
- no Unicode normalization or float-to-string conversion occurs at the physical seam.

## R6 — weight court

The float-boundary repair must not alter weight semantics.

Verify:

- weight physical-key lookup uses the repaired exact physical key;
- existing WeightValueRule.exact_value remains semantic/authorized material;
- existing copy_observed_numeric behavior, when explicitly enabled by the projection, remains its own governed path and is not generalized to response/coordinate values;
- non-finite raw weights are still rejected by existing weight logic unless a separate explicit governed rule authorizes a semantic value;
- no NaN/Infinity is converted to missing, zero, one, UNKNOWN, or a valid weight merely by the boundary repair;
- weight basis, design authority, estimand authority, normalization reference, and effective scope are unchanged.

## R7 — unprojected physical-cell preservation

Feed physical cells, including finite and non-finite float states, for slots not owned by response/coordinate/weight projection.

Verify:
- no semantic object is emitted;
- the cells are not dropped from or rewritten in the R5 carrier;
- no candidate-specific side effect is introduced.

## R8 — deterministic replay

Repeat the same synthetic physical stream and governed projection at least twice.

Require byte-/hash-stable:
- physical binding keys;
- response replay roots;
- coordinate replay roots;
- weight replay roots where applicable;
- candidate C11 release identity generated from the same repaired contract.

Input iteration order changes that are already normalized by the governed projection must not create a new result. Physical state distinctions listed in R1 must never normalize together.

## R9 — Candidate A/B/C neutrality

The repaired helper/contract must live in the shared C11 physical seam or another candidate-neutral common module.

Reject:
- Route-A-only float special cases;
- source-name checks;
- LiTS-I-specific numeric conversions;
- Candidate B/C bypasses;
- any path where a candidate receives different physical token semantics for the same decoded physical value.

No real Candidate A/B/C execution is required by this worker; this is a structural regression obligation.

## R10 — existing R5 root reopen

Against the accepted root 7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd, the eventual recovery run must use the accepted Route-A adapter path.

That adapter already invokes single_pass_full_audit during inspect_reopened_r5_physical_source before C11 projection. Require exact convergence on:
- physical root;
- logical stream 076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba;
- rows 34,745,595;
- members 2,121;
- member inventory 04dce8c3e942fc81a0558354c21a4b4a56faab417ce362657286f978b6686703.

Any mismatch is a physical-carrier failure and must not be papered over by the C11 repair.

## Failure conditions

The repair court fails if any test shows:
- binary float admitted as an ordinary semantic numeric identity;
- finite float converted to Decimal/Fraction/string merely for admission;
- NaN/Infinity interpreted as semantic missingness;
- non-finite cell deletion;
- signed-zero collapse;
- int/float or bool/int physical-key aliasing;
- string/float infinity aliasing;
- new opaque physical codec competing with R5 typed-value authority;
- R5 member rewrite/rebuild caused only by the C11 boundary repair;
- candidate-specific behavior.

Only after R1-R10 pass may CURRENT CONSUMER ADMISSION be treated as eligible for a new successful receipt.
