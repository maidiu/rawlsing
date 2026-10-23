# R08 R4 coverage matrix — R61Q D1-D6

| Requirement | Implementation | Qualification |
|---|---|---|
| D1 no implicit admitted authority | `EvidenceResolver()` has no verifier/executor default; `resolve` returns `UNKNOWN` / `NO_CONFIGURED_TRUST_ROOT`; cache import/export and reader refuse without pinned config; no default key/singleton in source | `test_default_unconfigured_resolver_and_reader_refuse_admitted_support`; `test_default_cache_rejects_missing_admission_and_forged_same_source_evidence` |
| D2 producer permission != execution; owner/recipe pin | `TrustedOwnerAdmission` issued only by configured `TrustedAdmissionAuthority`; bind verifies HMAC over exact context ref + actual owner identity; `admitted_producer` identity pin; typed conditions/source/release/query/risk/role/clock/consumer/model checked | `test_forged_caller_context_cannot_mint_owner_admission`; `test_wrong_actual_condition_or_admitted_labels_refuse_positive`; `test_callable_substitution_and_signed_envelope_metadata_mutation_refuse` |
| D3 complete executed-result envelope | `ExecutedEvidenceEnvelope@1` signed by trusted execution authority only after actual provider/evaluator; binds K material/hash, context/owner, source/release, provider receipt/fact/state, evidence ref+content hash, query/model, evaluator hash, axes/uncertainty, denominator/cells/values, trust domain/grade | `test_positive_actual_producer_consumer_values_read`; `test_attacker_issuer_and_fabricated_envelope_do_not_satisfy_real_reader`; envelope tamper in `test_callable_substitution...` |
| D4 verification-only ingress + real consumer pin | `TrustedAdmissionVerifier` exposes verify only; resolver/reader have no sign/key-export; `EvidenceConsumerReader` requires same verifier + valid signed envelope, rejects direct fabricated/signed-by-attacker result | `test_attacker_issuer_and_fabricated_envelope_do_not_satisfy_real_reader`; `test_default_unconfigured_resolver_and_reader_refuse_admitted_support`; `test_consumer_assertion_mutation_and_restoration` |
| D5 cold replay, independent root | cache carries request/owner/envelope/evidence/query/rule/result + envelope signature, no key; verifier key delivered via stdin fixture pipe separately; wrong root refuses | `test_cold_process_cache_replay_preserves_same_consumer_values`; wrong-root assertion in `test_cache_carries_full_k_and_issuer_boundary_rejects_self_seal`; forged same-source in `test_default_cache_rejects_missing_admission_and_forged_same_source_evidence` |
| D6 version/compatibility and unchanged meaning | cache `@3`, result `@3`, admission `@2`; legacy implicit-default acceptance removed and refuses; K/typed condition/status science unchanged | `test_condition_a0_result_cannot_resolve_a1_request`; `test_typed_encoding...`; `test_valid_products...`; `test_actual_zero_support...`; `test_actual_observed_zero...` |

## R61Q eight falsifier categories

1. **No-config / missing root / legacy** — PASS: default resolver, import, export and reader typed refuse. Old implicit-default probe expectations are intentionally incompatible (D6); successor tests above replace them.
2. **Pinned genuine native positive and changed case** — PASS: actual AT07 provider 54/6/60; changed-source `CHANGED_SOURCE_LAW` and A0/A1 cases remain distinct actual computations.
3. **Forged context / attacker issuer / callable substitution** — PASS: forged context refuses; attacker issuer with same id cannot satisfy real reader; substituted callable fails admitted-producer pin.
4. **Copied permission + same-source/cross-context evidence forgery** — PASS: copied envelope is bound to original evidence content; same-source 999 and cross-source mutations refuse at cache import.
5. **Envelope metadata/status/receipt/query/model mutation** — PASS: signed envelope mutation and result status mutation refuse; envelope/evidence/query/rule association is recomputed.
6. **Direct fabricated result/evidence with evaluator hash** — PASS: `EvidenceResult` SUPPORTED requires signed envelope; forged/attacker signature refused by real reader.
7. **Cold original positive + wrong-root/legacy refusal** — PASS: fresh process positive 60 and same consumer hash; wrong verifier root and envelope-less cache refuse; key delivered separately via stdin.
8. **Upstream/context/evidence mutation and restoration** — PASS: severance/condition/label/value mutations refuse; original exact request/context restores SUPPORTED 54/6/60; cached positive restores.

## Deliberate supersessions / deselections

The R1/R2/R3 probes that required `EvidenceResolver()` to accept a module-default
public key and produce positive support are intentionally incompatible under D1/
D6. They are not counted as safety failures; the same positive/zero/cold/status
controls are re-qualified through an explicitly configured trusted host fixture
in the R4 tests above. No original archived probe was edited.

## Limitations

Full live J42/P41/E04 maintained integration remains NOT_REACHED. No original
source/science, N11/N12, F6/F7/F8, actor, Sorok, J52/W52, production/CI or
protected-capture authority is claimed. Same-UID host/key compromise, ptrace/root
and dishonest competent issuer remain outside this scoped threat model.
