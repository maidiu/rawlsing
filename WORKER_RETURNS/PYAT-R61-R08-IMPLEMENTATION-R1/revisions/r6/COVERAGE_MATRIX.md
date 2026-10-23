# R08 R6 completeness matrix

## D1-D6

| Requirement | Status | Evidence |
|---|---|---|
| D1 no implicit root | PASS | no-config resolver/import/reader typed refusal |
| D2 owner permission != execution | PASS | producer admission + context/owner + mandatory live producer pin; missing pin call count 0 |
| D3 complete executed envelope | PASS | envelope @2 signs original provenance/mode + full result relation; reader/e04/export/import/replay share projection |
| D4 verification-only ingress + real consumer | PASS | reader requires same verifier + signed envelope; unsigned provenance cannot change served grade; export validates objects |
| D5 cold replay independent root | PASS | fresh-process key via stdin; cold read and cold re-export at verifier-only resolver |
| D6 versioning/unchanged meaning | PASS | cache/result/envelope @4/@4/@2; legacy refusal; native/status semantics unchanged |

## Eight falsifiers

1. no-config/legacy refusal — PASS.
2. pinned genuine native positive + changed case — PASS (54/6/60, 54/16/70).
3. forged context/attacker issuer/callable substitution — PASS (call count 0 without pin).
4. copied permission + same/cross-source evidence forgery — PASS.
5. envelope/status/receipt/query/model mutation — PASS.
6. direct fabricated result/evidence — PASS (signed envelope required; unsigned fields not served).
7. cold positive + wrong-root/legacy refusal + re-export — PASS.
8. upstream/context/evidence mutation and restoration — PASS.

## Field classes / consumer paths

Signed/served: K/request, context/owner, source/release, producer query/
predicate/receipt/fact/state, evidence ref + full content digest, consumer
query/model, evaluator state/hash, eligibility/execution/result, uncertainty,
denominator, cells, consumer values, execution provenance/mode, trust
domain/version/grade.

Paths: `EvidenceConsumerReader.read`, `e04_step`, `EvidenceResolver.resolve`,
cache `export_cache`, `import_authenticated_cache`, `_replay_cache`, verifier-only
re-export, fresh-process cold replay. All use the same projection/equality and
object-content checks.

## Omissions / versioned probes

Old R5 probes that require unsigned `cache_trust_grade` or assert downstream
import refusal after export already refused are superseded. Successor R6 tests
cover signed provenance, no unsigned grade, mutated object export refusal and
verifier-only re-export. All other R5 controls pass. No archived probe edited.

## Limits

J42/P41/E04 live integration NOT_REACHED. No source/science/rights, production,
CI, N11/N12, F6/F7/F8, actor, Sorok, J52/W52 or protected-capture claim.
Same-UID host/key compromise, ptrace/root and dishonest competent issuer out of
scope.
