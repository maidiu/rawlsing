# C06 — Adaptive Discovery Replay Requirements

Status: `MISSING_AUTHORITY__FAIL_CLOSED` for the recovered adaptive program.

## Current narrow authority

`rawlsing_next/pre553_discovery_exact.py` implements `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`. It freezes a finite/finitely-constructible frontier **before data are examined**, executes every candidate, requires `NONE_EXACT_EVALUATE_ALL`, forbids proposal randomness, rejects ranking that controls reachability, and fixes `CANONICAL_CANDIDATE_HASH_ORDER`.

That is replayable for its declared frontier.

The same module explicitly says: **No adaptive traversal.** It therefore cannot answer R12's recovered adaptive-discovery replay burden.

## Exact governing information required before an adaptive program can be called replayable

Authority must settle, or explicitly declare irrelevant, every determinant below that can change reachable candidates or accepted learned products:

- candidate universe construction and enumeration order;
- backend-independent logical candidate order;
- branch expansion/queue/stack/frontier selection law;
- branch parentage and ancestry identity;
- pruning/screening theorem or heuristic and its effect on completeness claims;
- ranking/scoring role and whether ranking controls reachability;
- all tie-breaking rules;
- floating-point/exact-numeric comparison, tolerance and tie behavior where relevant;
- resource/search budget units and accounting;
- stop conditions and stop-reason precedence;
- RNG algorithm, stream names, seeds, counter/state derivation, or explicit absence;
- subsampling/bootstrap/resampling law;
- validation split construction and identity;
- candidate→validation→accepted/rejected state transitions;
- model-selection rule/version where selection affects the learned world;
- cache/index iteration order if it can affect semantics;
- parallel execution reconciliation and deterministic merge law;
- source-universe/risk-set/time/topology/measure scope;
- frontier visited/pending/pruned accounting;
- interruption/restart semantics;
- typed terminal states.

## Backend-independence hostile law

`SAME SOURCE + SAME SEMANTIC/SEARCH AUTHORITY + DIFFERENT PHYSICAL BACKEND`

must produce the same semantic frontier trajectory and learned-product identity whenever the governing law claims deterministic replay.

Filesystem order, shard arrival, thread scheduling, worker number, database plan, dictionary order, cache presence, or physical row group layout cannot silently select a different branch. If a choice is semantically intended, it must be elevated into explicit logical authority rather than inherited from a backend.

## Replay receipt after law exists

A run receipt must bind:
- exact search authority/algorithm identity;
- candidate grammar/universe/frontier refs;
- source/decoder/authority roots;
- deterministic parameters;
- named RNG/subsample/split refs;
- initial frontier state;
- canonical branch/state transition commitments sufficient to reproduce/audit the trajectory;
- visited/pruned/pending counts or exact frontier digest under the governing law;
- budget consumed and budget ceiling;
- exact stop reason;
- candidate and validation terminal states;
- learned release refs;
- interruption/restart state if any.

Persist only the run-specific material not exactly derivable from frozen law and authoritative inputs. Do not persist respondent payload merely to remember a branch trajectory.

## Typed completeness

A run that ends because of failure, budget, unsupported domain, interruption, or unresolved validation cannot emit a complete empirical negative. `VALID_EMPTY` is lawful only under the exact semantics of its governing stage and must not be widened into “the world contains no relation.”

## Missing authority returned to HQ

C06 does not invent:
1. the recovered adaptive search/enumeration/branch-expansion algorithm;
2. its pruning/completeness theorem or permissible coverage claim;
3. budget/termination law;
4. randomness/subsampling/split law if used;
5. candidate→validation/model-selection state machine.

Until those are frozen, adaptive replay is `UNRESOLVED_BLOCKING` and no backend comparison may claim “same learned world” for the recovered adaptive capability.
