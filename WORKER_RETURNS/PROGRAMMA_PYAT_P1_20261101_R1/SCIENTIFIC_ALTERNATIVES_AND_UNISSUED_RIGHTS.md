# Scientific alternatives and unissued rights

## 1. The scientific method boundary

P1 uses a **declared method input**, not an inferred method:

| Method | Constructor behavior |
|---|---|
| `DIRECT_MEASURED` | Requires an exact measure authority per item and the measure kind in the source grant. |
| `PROXY_MODELLED` | Requires an independent method owner and authority ref, exact method/item kind match, and an explicit proxy measure kind in the grant. Otherwise typed HOLD. |
| `HYPOTHETICAL` | Same owner/authority gate; no measured claim. |

A direct method with a proxy/native measurement is a typed HOLD
(`MEASURE_NOT_IN_SOURCE_GRANT` / `MEASURE_METHOD_KIND_MISMATCH`). A proxy method
without an owner is a typed HOLD (`SCIENTIFIC_METHOD_OWNER_ABSENT`). The
constructor never silently substitutes a proxy for a measured operation.

## 2. M48 grammar coverage

M48 proposal `M48_SCIENTIFIC_GRAMMAR@1` defines broader classes. P1 deliberately
implements only a finite, explicit subset:

**Implemented sourcefree operation classes:**

- `DISTRIBUTION`
- `CONDITIONAL`
- `JOINT`
- `HETEROGENEITY`
- `RECURSIVE_BRANCH`

**Not implemented / held for a future owner:**

- `CO_TRAVEL`
- `FORK`
- `INTERACTION / REVERSAL`
- `STATE / ROBUSTNESS`
- `CROSS_SOURCE`
- `TEMPORAL`
- `POSSIBILITY`
- `STRUCTURAL`

The P1 constructor is therefore an executable finite request frontier, not the
complete M48 scientific grammar. It does not claim 432 symbolic operations, 15
native operations, 1,890 original operations, or any particular all35 coverage.

## 3. Alternatives and why they are not used as measured truth

| Alternative | Status |
|---|---|
| R157 source configuration | Historical preparation, 0/119 current; 19 code paths absent. Preserve 35-wave/18,276 metadata identities; not U/E_pre. |
| B49 source-rule/native adapter | Current sourcefree adapter at its own scope; 1 synthetic native fact; not original35 E_pre. |
| G50 symbolic grammar | Proposal/test-only; 432 symbolic/15 native; not source evidence. |
| M48 grammar | Proposed method requirements; not issued science. |
| S04 trend/interpolation/backoff | Not imported; no trend, rate, midpoint or `gap_years * 0.05` uncertainty. |
| Proxy/model alternative | Allowed only under an exact independent method owner and authority; otherwise HOLD. |
| Cross-source pooling | Not authorized by this constructor; JOINT is declared same-unit binding, not source pooling. |
| Temporal comparison | Not implemented; F7 comparability owner and real wave products remain absent. |
| Selected-world/N9/N10W | Not implemented; E03 remains a 58-row synthetic oracle, not a world. |

## 4. Unissued rights and counts

The constructor produces no original-source result. These remain absent:

- wave-scoped original source/host/purpose/export rights;
- exact original item registry and native instrument inventory;
- per-wave route/weight/respondent-eligibility authority;
- exact C11 logical releases and I03/I05 operation authorities;
- a named empirical consumer;
- original U/E_pre, N11/N12, Field Forge, actor or model-use authority;
- actual 35-wave occupancy and actual 1,890-cell operation count.

`all35_populated_claim` and `sourced_results_claim` are always `False` on this
candidate. An `ORIGINAL_SOURCE_ISSUED` input scope only labels the external input;
it does not create an issuer or a measured result.

## 5. Scientific verdict

**HOLD** at every scientific claim beyond sourcefree construction. The method
boundary is explicit, noncomparability/abstention is preserved, and no
proxy/modelled alternative is promoted without an owner. The actual source
science remains with the original source/semantic/use issuers.
