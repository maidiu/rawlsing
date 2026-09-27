# I2 M2 — M1 TO M2 INTERFACE RECEIPT

HQ118 adopted the direction:

`M1 LearnedEmpiricalDisposition -> M2 exact ReleaseCore -> B5 lifecycle`

I2 implements only the M2 side of that interface.

## Synthetic source-free witness

The hostile suite registers an exact subject ref with:

- exact kind: `LearnedEmpiricalDisposition`;
- release subject kind: `TYPED_DISPOSITION`;
- exact M1 producer-contract ref;
- exact typed state;
- exact producer-declared authority/dependency/determinant/replay/explanation requirements.

M2 then constitutes a ReleaseCore and resolves the same producer-owned exact subject.

Test:

`test_20_m1_learned_empirical_disposition_is_exact_release_subject`

Governed result:

`PASS`

## Noncollapse

M2 does not interpret M1's adjudication outcome.

It neither:
- reruns a family validator;
- decides whether the disposition is positive;
- changes the disposition state;
- grants a structural use;
- creates a lifecycle publication event;
- selects it as current.

The exact interface is therefore:

`M1_EXACT_SUBJECT_REF + M1_PRODUCER_CONTRACT + PRODUCER_DECLARED_CLOSURES -> M2_RELEASE_CORE`

not:

`M1_FIELDS_COPIED_INTO_M2_GENERIC_MEANING`.

## Negative-state witness

The same release path passes for exact typed states:
- `VALID_EMPTY`;
- `NONCOMPARABLE`;
- `BLOCKED`;
- `UNKNOWN`;
- `INTEGRITY_FAILURE`.

This proves the M1 -> M2 seam is state-preserving rather than positivity-selective.

Disposition:

`M1_TO_M2_EXACT_REF_INTERFACE_SOURCE_FREE_GREEN`
