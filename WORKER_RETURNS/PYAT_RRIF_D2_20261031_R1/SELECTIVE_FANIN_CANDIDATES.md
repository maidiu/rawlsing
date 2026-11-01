# SELECTIVE FAN-IN CANDIDATES

**Bottom line:** no immediate selective fan-in is justified by this pass. Two lineages are already current/test-only, two are retired as current candidates, and two remain held for an owner/issuer/consumer decision. No speculative patch is proposed.

| Candidate | Source cut | What would be fanned in | Preconditions | Current status |
|---|---|---|---|---|
| **B5 N04 + C02J + C02H** | N04 `b5a6b6409`; C02J `8959803`; C02H `82309fe` | Bounded checkpoint correction + owner-held verifier + separate-principal verifier | An independent B5/M2 owner must hold the expectation and issuer/principal; an external expectation root must exist; must not revive 14 branches as separate capabilities | **BLOCKED — HOLD_UNPROVED.** No issuer/separate principal; accepted owners do not provide mandatory ingress. |
| **EE14 G1 owner ingress** | HQ268 `f10523e1`, current blob `74e6ee82` | Current owner-internal C1→G2→F8 data-only ingress | A real production consumer and independent owner; explicit acceptance that shallow nested `_source` freeze is a trusted-harness residual, not a trust root | **NO FAN-IN NEEDED — CURRENT_RETAINED test-only.** No production consumer found. |
| **R56 source-native adapter** | R02 `6f4be338`, current blob `a6299c1a` | Current exact adapter with production imports | Owner acceptance of the sourcefree adapter; raw source/N11/N12 remain separate; do not import the `2d83cea` review variant | **NO FAN-IN NEEDED — CURRENT_RETAINED exact current.** R02V-R2 requalification passed. |
| **R157 source configuration** | Final review `d81bc2c67`; foundation `519355ec`; integration `056849e2` | Historical configuration preparation estate (19 introduced paths) | A real source-configuration consumer and owner; explicit proof it is not being substituted for original U/E_pre or F1–F8 | **RETIRE — no current path/consumer.** Do not fan in 13 lane branches. |
| **SRC04 observed/co-observed response** | Observed empirical `b6be4058`; current query core modified | Historical `pre553_observed_response.py` contract + observed/co-observed denominator policy | A named current consumer and exact observed-response/weight authority; proof that recorded response is not the eligible denominator or population estimate; sourcefree denominator/weight drift tests | **BLOCKED — HOLD_UNPROVED.** Current query core retained; observed-response extension absent and unconsumed. |
| **S00D value quarantine** | HQ285 `4c8168b7` | Producer binding, fraction/step closure, false S00 semantic quarantine | A current S00/P04 consumer and its `r3_s02_seam_witness` dependency; explicit Q86A/Q86B binary semantics; no democracy/trust Likert interpretation | **RETIRE — absent standalone module.** Preserve requirement if a consumer returns. |

## What would make a fan-in actionable

1. **B5:** an actual owner-issued expectation/issuer and separate principal. Without that, the N04 correction alone is a bounded checkpoint fix, not a trust boundary.
2. **SRC04:** a real observed-response consumer plus weight/denominator authority. Without that, adding `pre553_observed_response.py` would be a speculative new capability.
3. **S00D:** a real S00/P04 consumer. Without that, the module cannot even import because its seam-witness dependency is absent.
4. **R157:** a real config consumer. Without that, the 19-path configuration estate is historical preparation only.

## Non-candidates

- **R26V/R27P/R31J/R31E, BP/C9/C12, G15/G17/G18, B3AS/C9R/JOIN-E** are outside this D2 six-lineage scope. They are not re-opened here.
- **R61 R09V runner reviews** are not R56 adapter reviews. They concern `CROSS_HQ_CONTROL_ROOM/universal_runner_verify.py`; do not use them as evidence against the current R56 adapter.
