# R61-R08 evidence-binder ingress map

## Exact source

- R08 binder blob: `3ca860e409f1d063da4cd03dd1691a89c67333f6`.
- Exact R8 code commit used for the current-provider test:
  `80bb8c18241ebcd7ddbe559b76c6b39a72025b89`.
- Author branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`.
- Current `rawlsing_next` tree: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` at
  `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Current source **does not contain** `pre553_universal_evidence_binding.py`.

The exact binder was not committed into this branch. The reproducible runner
extracts the exact module and test from Git into an isolated temp tree:

```bash
./repro/run_r08_current_binder.sh
```

It copies current `rawlsing_next`, the exact binder/test blobs, the exact C1
fixtures, and the R8 review probes. It writes no production file.

## Current-provider receipts

| Court | Command | Result |
|---|---|---|
| R08 author suite | `pytest rawlsing_next/tests/test_universal_evidence_binding.py` | **113 passed**, exit 0 |
| R8 targeted probes | `pytest probes/test_r08v_r8_targeted_refusal_codes.py probes/test_r08v_r7_semantic_adapters.py` | **8 passed**, exit 0 |
| R8 review claim | R8 review `00_RETURN.md` | 126/126 author suite (113 R08 + 13 C1), 76/76 R7 successor probes |
| Current C1/N10E/F8 | `pytest test_source_backed_positioned_subject_possibility.py test_pre553_analytical_composition.py test_pre553_empirical_possibility_provider.py` | **69 passed**, exit 0 |
| Current learned-world | `pytest test_pre553_learned_world_composition.py` | **30 passed**, exit 0 |

The 113-pass test proves the exact binder survives against the current
`rawlsing_next` at sourcefree test scope. It does not prove a current production
receiver.

## Source-owned provider identities

The R08 fixture binds:

- AT07 synthetic forward: 54 yes / 60 denominator = 9/10.
- AT07 changed-source: 54 yes / 16 no / 70 denominator; forward 27/35;
  reverse remains 54/8/62 = 27/31.
- Exact synthetic source/release/universe/risk refs from the C1 freezes.
- `TrustedAdmissionAuthority` and `TrustedCacheIssuer` are **TEST_ONLY ephemeral
  HMAC authorities**; they are not original issuer or source warrants.

## Enforced ingress/refusal boundaries

| Boundary | Actual evidence |
|---|---|
| Missing binder | Current import is absent; runner stages exact blob only in temp |
| Foreign issuer / forged context | `test_attacker_issuer_and_fabricated_envelope_do_not_satisfy_real_reader`; `test_forged_caller_context_cannot_mint_owner_admission` |
| Stale source / stale cache | `test_cache_cold_replay_and_authenticated_tamper`; R8 probe `STALE_OR_UNAUTHENTICATED_CACHE` |
| Altered evidence | `test_export_refuses_mutated_evidence_query_and_rule_objects`; `test_reader_serves_only_signed_projection_for_all_mutated_fields` |
| Unsafe cache / self-seal | `test_cache_carries_full_k_and_issuer_boundary_rejects_self_seal`; `test_default_cache_rejects_missing_admission_and_forged_same_source_evidence` |
| Replay / cold process | `test_cold_process_cache_replay_preserves_same_consumer_values`; R8 probes |
| Missing live producer pin | `test_missing_live_producer_pin_is_fail_closed_before_execution` |
| Callable/owner substitution | `test_callable_substitution_and_signed_envelope_metadata_mutation_refuse` |
| Current descriptor pin | R8 probe `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; correct pin restores 60 |
| Missing verifier | R8 probe `NO_CONFIGURED_TRUST_ROOT`; no support |
| Legacy binding pins | R8 probe `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`; import/export limits preserved |

## Production-receiver GAP CARD

**R08 evidence binder current production receiver: MISSING.**

- No `rawlsing_next/pre553_universal_evidence_binding.py` at current.
- No current production import or call site.
- The exact binder can be staged and run against current N10E/C1/F8 sourcefree
  fixtures, but that is a test harness, not a production receiver.
- The HMAC trust authorities are local ephemeral test double; they do not grant
  original source or actor authority.
- A production receiver must be named by the current owner, must bind an actual
  source-owned provider, and must be independently reviewed. Until then R08
  remains **ENGINEERING HOLD / NOT ADOPTED**, despite 113+8 sourcefree passes.

## Interpretation

The missing R08 primitives are recoverable as a bounded sourcefree binder over
current producers. They are not currently integrated. Do not transplant the
118 KB binder into production blindly, and do not treat 113/113 or 8/8 as native
source warrant, model use or scientific issuance.
