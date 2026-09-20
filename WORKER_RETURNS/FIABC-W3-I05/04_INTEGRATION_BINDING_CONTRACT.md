# FIABC-W3-I05 — Integrated P2X Oracle Binding Contract

## Purpose

The Wave-3 base does not contain the later divergent `ee_p2x_darwin_stage_backend.py` audited by Wave 2. This contract tells HQ exactly how the integrated P2X runner must consume the new independent oracle without importing the old S03 self-replay law.

## Required ordering change

The old audited ordering is unlawful:

`S01 candidate output -> S03 freeze pseudo-oracle -> same candidate I03 twice -> parity bit`.

The integrated ordering must be:

`SOURCE/LOCK VERIFICATION -> COURT-NEUTRAL ORACLE MATERIALIZATION/FREEZE -> S01 candidate lifecycle -> C11/I03/I05 candidate output -> ORACLE MATCH -> PERFORMANCE ADMISSION`.

The oracle must therefore exist before the first candidate-output event for that source.

## Required S03 semantics

S03 (or its integrated successor gate) must **not** call the candidate binding to derive expected truth.

It must:

1. load the already-frozen source-local oracle;
2. call `verify_frozen_oracle(...)`;
3. collect the candidate's completed governed comparison observation;
4. call `validate_candidate_observation(...)`;
5. record the resulting independent oracle-match receipt;
6. keep any same-candidate fresh replay result in a separate `SELF_REPLAY_OK` field;
7. refuse performance admission if oracle match fails.

The integration must have no transition:

`SELF_REPLAY_OK -> SEMANTIC_PARITY_PASS`.

## Whole-source A/B/C gate

After all admitted A/B/C cells for one source have completed their independent matches, call:

`validate_three_way_parity(frozen_oracle, {"A": ..., "B": ..., "C": ...})`.

The gate requires exactly A, B, and C and the same oracle identity. A/B-only agreement cannot PASS. Copying A's observation into B/C cannot PASS because candidate identity is checked independently.

## Candidate observation contract

A candidate observation must bind:

- `candidate`;
- `oracle_identity_sha256`;
- `source_identity`;
- `court_constitution_refs`;
- `semantic_authority_closure`;
- `authority_closure_digest`;
- `projection_and_release_refs`;
- `frontier_manifest`;
- `frontier_digest`;
- `fact_manifest`;
- `learned_product`;
- `replay_manifest`;
- `exact_ref_manifest`;
- `negative_state_manifest`;
- optional `self_replay_ok` as replay evidence only.

The learned product must bind complete I05 coverage, not only a scalar product hash.

## State isolation

The frozen oracle is court evidence, not candidate state.

Forbidden:

- mounting oracle C11 repositories into a candidate;
- giving a candidate oracle-created caches/accelerators/sessions;
- using candidate durable/scratch roots while building the oracle;
- resolving expected refs from candidate output;
- using candidate A as golden output for B/C;
- majority vote;
- post-output oracle rewrite;
- frontier mutation after outcome access.

Any such condition invalidates parity independently of whether numeric values match.

## LiTS integration

Use `build_lits_i_oracle(...)` with:

- immutable ASTRA-D04-R2 product/replay evidence;
- current candidate-neutral exact-ref/authority closure;
- current comparison fact manifest at the governed terminal grain;
- exact current projection/C11 identities;
- an independence-preserving freeze receipt.

ASTRA-D04-R2 supplies accepted prior factual truth. Current PRE553 authority supplies current exact identity. Neither candidate A/B/C supplies expected truth.

## WVS integration

Execute `03_WVS7_LOCAL_MATERIALIZATION_PROTOCOL.md` before WVS candidate A begins. The resulting frozen oracle identity becomes the sole expected-truth identity for WVS A/B/C parity.

## Sibling interaction

This I05 module does not assume ownership of sibling burdens:

- I03 Candidate-C production binding determines how C physically reaches the common semantics;
- I04 runtime packaging rebind determines stable runtime packaging;
- I06 equal-work instrumentation owns measurement isolation/accounting;
- I07 succession preflight must require a valid independent-oracle contract/receipt;
- I08 terminal verifier must require the oracle PASS and the full I05 terminal.

Do not move oracle semantics into any of those components. They consume the oracle contract or receipt; they do not redefine expected truth.

## Fan-in acceptance check

The integration is complete only if a code review can answer **yes** to all of these:

- Is the oracle frozen before candidate output?
- Can the oracle be built without any A/B/C output/state?
- Is the WVS frontier exact, ordered, and immutable?
- Are full I03 facts/typed states and full I05 coverage compared?
- Are ExactRefs, authority closure, semantic identity, replay identity, output identity, and negative-state law compared?
- Does A matching itself fail to imply parity?
- Does A/B pairwise agreement fail to imply three-way parity?
- Does missing C fail closed?
- Does stale authority/replay fail despite equal values?
- Is performance admission downstream of independent oracle match?

If any answer is no, the integrated S03/parity gate remains unqualified.
