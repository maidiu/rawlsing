# LiTS Representation Blocker Holding

## Local observation

The user ran governed pre-candidate preflight from the correctly fast-forwarded P2X execution branch at:

`e8909490cdc619beb884029cdabdc7027db663cf`

Lock-1 runtime and exact LiTS/WVS source hashes passed. WVS candidate-neutral standardization passed. LiTS candidate-neutral oracle production stopped before oracle output with:

```text
SourceBackedC11FacadeError:
unbound response value/state; no label/frequency/missingness inference
```

The user reported that no T3 freeze, succession preflight, Candidate A/B/C, or measured P2X ran.

## Documentary diagnosis

This is not presently adjudicated as a missing LiTS response-semantic rule.

The accepted historical LiTS-B real-source C11 pass is:

`WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json`

It records:

- Candidate-B owner blob: `7c509c2098d0030f253344eb3f682471378812a8`;
- exact LiTS source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- projection identity: `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
- C11 logical release: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
- status: PASS.

That accepted owner computed physical response keys as:

`semantic_hash({"raw": canonicalize(raw_value), "physical_state": state, "declaration": canonicalize(declaration)})`.

The current source-backed facade blob:

`8a761119e4a8d68eb291fc4edfadb52e027f8284`

uses `PRE553_PHYSICAL_VALUE_BINDING@2.0.0` and `R5TypedValueCodec`, explicitly preserving Python/physical representation lanes such as int, float64 finite bits, Decimal tuple, string, and exact missing-declaration representation.

Therefore the current facade intentionally no longer assumes the historical canonicalized numeric-equivalence relation.

The current LiTS candidate-neutral oracle producer decodes the real DTA and passes the resulting physical incidence directly to that stricter current facade. The first physical response key not present in the governed rule map fails closed exactly as observed.

## Rejected shortcut

A speculative repair that replayed the banked helper `exact_cell()` was investigated and then removed before user adoption.

Reason: the helper converts Python floats using `Decimal(str(value))`, while the current R5 codec preserves Decimal exponent. That alone is insufficient documentary proof that the resulting physical token equals the current governed response-rule token.

No numeric coercion has therefore been admitted as authority.

## Current holding

**BLOCK — LITS PHYSICAL/NATIVE REPRESENTATION AUTHORITY NOT YET CLOSED FOR THE CURRENT TYPED PHYSICAL-KEY CONTRACT.**

This is analogous in kind, but not automatically identical in content, to the previously closed WVS7 R1J representation-authority problem.

There is currently a WVS7 representation-authority module:

`rawlsing_next/fiabc_lm2_r1j_wvs7_representation_authority.py`

There is no corresponding LiTS representation-authority module in the current tree.

## Next evidence step

Run only the candidate-neutral diagnostic:

`WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/08_LITS_REPRESENTATION_DIAGNOSTIC.py`

against the exact LiTS source under the already-qualified Lock-1 runtime.

It records, for only q301_2 and q301_7:

- exact decoder-observed R5 physical token classes;
- exact physical missing-state and missing-declaration token classes;
- current governed response-rule keys;
- current-key match/nonmatch counts;
- the banked `exact_cell()` representation as evidence only, without granting it authority.

It deliberately does not use value labels, frequencies, or missingness to infer semantics and does not construct an oracle, T3 freeze, candidate output, or measured P2X result.

The resulting receipt is evidence for a separate bounded LiTS representation-authority closure. Do not resume pre-candidate oracle production until that authority is closed and source-free qualification is green on any resulting code change.
