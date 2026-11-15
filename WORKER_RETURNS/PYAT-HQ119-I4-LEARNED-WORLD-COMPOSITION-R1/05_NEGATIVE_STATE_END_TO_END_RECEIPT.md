# Negative-State End-to-End Receipt

I4 treats negative, absence, unresolved, and integrity states as typed producer output. It does not convert them into affirmative or negative semantic claims.

## Conserved states proved

| State | M1 origin | I4/M2 handling | End-to-end proof |
|---|---|---|---|
| `RULE_NOT_SATISFIED` | substantive family-rule outcome | M2 subject typed state remains `RULE_NOT_SATISFIED`; no semantic claim is minted | T07, T18 |
| `VALID_EMPTY` | exact empirical/discovery state | retained in disposition state vector; disposition ref becomes exact product ref | T19 |
| `NONCOMPARABLE` | exact empirical state | retained in state vector without conversion to zero/false | T20 |
| `BLOCKED` | exact prerequisite state / M1 terminal | prerequisite state remains `BLOCKED`; terminal remains `BLOCKED` | T20 |
| `UNKNOWN` | exact prerequisite state | prerequisite remains `UNKNOWN`; M1 terminal remains `UNRESOLVED` | T20 |
| `UNRESOLVED` | M1 terminal axis | product typed state and receipt terminal state remain `UNRESOLVED` | T20 |
| `INTEGRITY_FAILURE` | M1 validator/input integrity axis | product typed state and receipt terminal state remain `INTEGRITY_FAILURE` | T20 |

The receipt's `conserved_state_material` carries:

- disposition class;
- adjudication outcome;
- rule outcome;
- exact reason code;
- semantic assertion polarity/state;
- conserved empirical-state rows;
- conserved authority-state rows;
- required prerequisite-channel state mapping;
- support-uncertainty material.

The receipt also carries the exact M1 disposition ref, determinant root, replay root, and explanation root.

## Negative semantic truth prohibition

T18 proves the critical distinction:

`RULE_NOT_SATISFIED != NEGATIVE_SEMANTIC_TRUTH`

The M1 output still carries typed absence for semantic claim identity and `semantic_assertion_polarity_or_state = NONE`. I4 copies the producer-owned disposition identity and state; it never synthesizes an opposite claim.

## Absence versus zero versus incomparability

I4 does not inspect source values and has no source-semantic branch. Therefore it cannot collapse `VALID_EMPTY`, `OBSERVED_ZERO`, `ZERO_SUPPORT`, or `NONCOMPARABLE` by convenience. The M1 owner already conserves those distinctions and I4 binds the exact M1 disposition as the released product.

Governed qualification: run `36331313683`, combined court `135 passed`.
