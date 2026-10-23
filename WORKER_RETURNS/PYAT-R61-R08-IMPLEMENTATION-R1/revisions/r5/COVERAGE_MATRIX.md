# R08 R5 completeness matrix

## R61Q D1-D6

| Requirement | R5 status | Evidence |
|---|---|---|
| D1 no implicit root | PASS | `EvidenceResolver()` no verifier/executor -> UNKNOWN/NO_CONFIGURED_TRUST_ROOT; import/export/reader refuse |
| D2 owner permission != execution | PASS | producer admission + context/owner checks; mandatory `admitted_producer` identity pin; substituted callable never invoked |
| D3 complete executed envelope | PASS | signed `ExecutedEvidenceEnvelope@1`; complete signed projection used by reader, e04_step, cache export/import/replay |
| D4 verification-only ingress + real consumer | PASS | verifier has no issue/sign; reader requires same verifier + signed envelope; unsigned result fields never served |
| D5 cold replay independent root | PASS | fresh process with key delivered via stdin; wrong root/missing envelope/forged values refuse; verifier-only replay works without producer pin |
| D6 versioning/unchanged meaning | PASS | cache @3/result @3/admission @2; legacy default refuses; native/status/K semantics unchanged |

## Eight R61Q falsifier categories

1. No-config/legacy refusal — PASS (`test_default_unconfigured_resolver_and_reader_refuse_admitted_support`).
2. Pinned genuine positive + changed case — PASS (`test_positive_actual_producer_consumer_values_read`, changed-source/A0-A1 cases).
3. Forged context/attacker issuer/callable substitution — PASS (`test_forged_caller_context_cannot_mint_owner_admission`, `test_attacker_issuer...`, `test_missing_live_producer_pin...`).
4. Copied permission + same/cross-source evidence forgery — PASS (`test_default_cache_rejects_missing_admission_and_forged_same_source_evidence`, cache intersection checks).
5. Envelope metadata/status/receipt/query/model mutation — PASS (`test_reader_serves_only_signed_projection_for_all_mutated_fields`, `test_callable_substitution_and_signed_envelope_metadata_mutation_refuse`).
6. Direct fabricated result/evidence — PASS (reader/e04_step refuse unsigned mutation; signed envelope required).
7. Cold positive + wrong root/legacy refusal — PASS (`test_cold_process_cache_replay_preserves_same_consumer_values`, wrong-root assertion in cache test).
8. Upstream/context/evidence mutation + restoration — PASS (`test_changed_typed_values...`, `test_consumer_assertion_mutation_and_restoration`).

## All signed/served field classes checked

K/request; context/owner; source/release; producer query/predicate; producer
receipt/fact/state; evidence ref + complete content digest; consumer query/model;
evaluator state/hash; eligibility/execution/result axes; uncertainty; denominator;
cells; consumer values-read (denominator, cells, state, evidence ref, nested
mapping); trust domain/version/grade. Reader, e04_step, export, import and replay
share the same projection/equality logic.

## Intentional supersessions / omissions

The two R4 probes that assert the old defect (read must return unsigned 999
values) fail by design: the repaired reader raises `EvidenceAssociationError`
instead. Successor R5 tests assert refusal and signed-projection service. Other
R4 probes pass. No probe/skip is hidden; archived probes were not edited.

## Limits

J42/P41/E04 live integration NOT_REACHED. No source/science/rights, production,
CI, N11/N12, F6/F7/F8, actor, Sorok, J52/W52 or protected-capture claim. Same-UID
host/key compromise, ptrace/root and dishonest competent issuer out of scope.
