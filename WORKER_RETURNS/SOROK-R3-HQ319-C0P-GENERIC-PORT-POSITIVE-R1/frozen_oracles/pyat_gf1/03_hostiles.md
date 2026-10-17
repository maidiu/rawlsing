# 03 — SOURCE / ROLE / MISSINGNESS / COLD / GRANT HOSTILES

All executed against the real accepted native chain in the isolated court.
**44/44 pass.** Nothing below was skipped, xfailed or relabelled.

## 1. Source and custody hostiles (refuse at the installed trusted owner)

| Hostile | Observed |
|---|---|
| Foreign expected root (`payload_json` altered) | refused `ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT` |
| Foreign register root (real register object, forged digest field) | refused `REQUEST_REGISTER_NOT_INSTALLED_ROOT` |
| Tampered relation object identity | refused at construction (`object_id/content_hash do not match`) |

## 2. Fact / source content mutation (re-hashed, so the CANDIDATE must refuse)

The native objects are immutable canonical semantic objects, so these forgeries
present **coherently re-hashed** material. A pure hash check cannot catch them —
the candidate's own structural validation does.

| Hostile | Observed |
|---|---|
| `raw_numerator_support` mutated to 999 (not re-hashed) | refused `producer fact semantic identity mismatch` |
| One joint cell removed | refused `native fact does not preserve the complete native joint domain` |
| Zero cell relabelled `OBSERVED_POSITIVE` | refused `zero joint count has inconsistent cell state` |
| Support count set negative | refused `nonnegative exact integer` |
| Weighted numerator injected | refused `may not consume a weighted numerator` |
| Nonbinary category added to the native domain | refused `frozen at two-binary-item domains` |
| `target_domain_identity` forged | refused `producer target-domain identity mismatch` |

## 3. Role / permission hostiles

| Hostile | Observed |
|---|---|
| target/conditioner swap with no grant | refused `REVERSE_PAIR_GRANT_REQUIRED` |
| swap with an unknown grant | refused `REVERSE_PAIR_GRANT_UNKNOWN` |
| swap with the authorized reverse grant | **succeeds**, `REVERSE_GRANTED`, distinct object id |
| non-native role ref | refused `must be an exact native ref` |
| relation permission widened to `PRODUCTION` | refused `GenericPermissionWideningError` |
| blocked producer state carrying counts | refused at construction |

## 4. Missingness and zero-semantics preservation

| Requirement | Observed |
|---|---|
| Observed zero inside supported risk | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`, kept distinct from `ZERO_SUPPORT` |
| Zero risk (no eligible respondent) | distinct code path; `ZERO_SUPPORT` never silently substituted |
| Y-ineligible row R3 | never becomes a zero; excluded by eligibility, not by a count |
| Consumer refusal when no relational input exists | `RESPONSE_INPUTS_VALID_EMPTY`, `downstream_value_produced = False` |
| Non-relation object handed to the consumer | refused `CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION` |
| Source-native response options | preserved: `SCALAR_SINGULAR`, `SUBSTANTIVE_RESPONSE`, native response authority refs intact |

## 5. Grant / independence

| Requirement | Observed |
|---|---|
| Independent source unchanged under A intervention | 2 of 4 QUERY consumers move; 2 keep exact baseline counts, risk `2`, ceiling `SOURCE_FREE_DEV` |
| Accepted specialized GT2 output unchanged | asserted equal to its declared original material in every consumer and profile |
| Accepted specialized source bytes unmodified | Git blob `a70decb20747d84cbcbe27d1280babc6de88ef33` re-derived |
| Native tree re-attestation | 74/74 from the original PV3 manifest after untouched staging |

## 6. Cold / replay / durability

- **6 real P01 `UnitExecutionReceipt`s per profile** (3 profiles), each reconciled
  against its durable checkpoint with matching `manifest_hash`.
- Deterministic generic replay re-derives the identical `object_id` and
  `content_hash`; drift is refused.
- Replay recomputes source; it does not fabricate offline fact restoration. Fresh
  offline history refusal remains an accepted-code path, unchanged by GF1.

## 7. Deliberately NOT claimed

SIGKILL/abrupt-termination re-execution, the full offline-restoration court, and
a complete 74-file owner regression re-run were **not** repeated. PV3N's qualified
frozen evidence (`816aaac8…`) covers those at this method grain, and the commission
explicitly directs reuse rather than re-running all 74 owner regressions. This
worker does not claim independent re-verification of those courts.