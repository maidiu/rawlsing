# R95 R06R2 author return — actual R05 product to P41 world consumer

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`
- Startup: `2c97293784392b708b3188574a260025d78cbb30`
- R2 contract: `fd06e5f9d57b436fe0f493193a49994e7ca354c0`
- R2 code: `2a884d54c22f90449cd93d61ef2d317056f332bf`
- Executor: existing OpenCode DeepSeek V4.1-Flash MAX/Global.

## Required R2 functions completed

### 1. Actual accepted R05 -> same actual world consumer view

The accepted R05 fixture and its retained-original `TrustedNativeGraphCoordinator`
produce an actual `LEARNED_CONSUMER_EXACT_SUPPORTED` result. That result (not a
label, copy or historical J42 provider) is supplied as the N10E step to an
actual P41 `P41Service` configured with:

- a real P41 `SelectedWorldCatalog` over the R05 empirical source identity;
- unchanged E04 `product.nonparent.consume`;
- actual P41 N10W progressive assembly;
- exact R05 learned/M1/M2/consumer/evidence/query/fact/coordinator refs in the
  selected-world block.

The new `select_r05_world_view` wrapper validates the actual P41 receipt and
binds it to the same R05 product. The R2 tests do **not** use the historical J42
build; R1's J42 evidence is preserved but is not the R2 integration path.

Severance/change controls refuse the same view before it can be served: wrong
source rows, wrong learned receipt, wrong M1/M2/evidence, wrong N10E query/fact,
tampered receipt, missing field, context-as-structural, person/household
pooling, unobserved pair and revoked currentness. The actual original restores.

### 2. Declared synthetic temporal pair consumed by the world machinery

T0 and T1 are actual explicit P41 `SelectedSnapshot` preimages:

| | T0 | T1 |
|---|---|---|
| clock | HISTORICAL, valid 2026-06-01, published 2026-04-15 | AS_OF, valid 2027-09-01, published 2027-09-01 |
| training_access | 1 | 0 (revision 2) |
| exit_cost | 2 | 8 (revision 2) |
| E04 training route | ELIGIBLE | BLOCKED_BY_MODELED_RULE |
| E04 exit route | WITHIN_MODELED_BUDGET | RESOURCE_CONSTRAINED |
| same R05 N10E consumer | exact hash | exact hash |

The same R05 learned empirical step and E04 consumer are used at both clocks;
the pair changes actual consumer routes and the P41 receipt/view hash. The pair
was explicitly declared in the request with a pair ref and observed-pair refs.
This is a synthetic sourcefree pair, **not original F7 measured-wave issuance**.
A clock-label/hash-only change is insufficient and is refused; the implementation
also refuses identical receipts, identical clocks and unobserved pairs.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r2/junit.xml -o addopts=''
```

Exit `0`; `10 passed`, `0 failed/errors/skips`; `189.912s`. The R2-specific
tests run in ~5s inside this suite. Cold replay runs a second fresh subprocess
over the actual R05->P41 construction and compares the full view hash, N10W
payload and temporal routes.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `d5429c470ae6c2d1912207638b3a6a5e8e341360` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `8ee623eb9d1aafa00b1bd311dba9d9b852799316` |

Only these two code paths changed. Existing accepted R03/R04/R05/R08 and
native/world/FF/F6/temporal/service/evaluator bodies were read-only.

## Import pins / upstreams

- R05 accepted candidate: `bc2b5465c8f0ec2ea4657c6206436cdfa9ca58d0`
- R05 review: `2f7faac6da620b7651c175ec074d7088d5a49343`
- R05 consumer/fixture at startup:
  - `rawlsing_next/pre553_learned_world_composition.py` blob `adbcc3316920c708580097dfe9f5aef4c9ca82fb`
  - `rawlsing_next/tests/test_universal_learned_consumer.py` blob `b0114a82c8852faffc52686c69585a50ee89ba9f`
  - `rawlsing_next/pre553_analytical_composition.py` blob `ed2b1680006ac2b89ddd40499e0a6d1429327d7b`
  - `rawlsing_next/pre553_universal_empirical_extension.py` blob `37279fa82001d5853dadf4906efc904e8dc3b9bc`
- Actual P41 consumer packet: `f27d1101048638bba395143a48efb7ef00bfcda4`,
  path `WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1`,
  materialized from Git into a temporary worktree directory per test run.
- R1 actual J42 packet preserved read-only: `f53cb0d2bce52640268c844c398bbd8007d28edc`.

## Explicit limits

- Original measured F7 waves, original 35x54/F6/F8, original source/science,
  CI/prod, N11/N12, Sorok and J52/W52 remain held. This is sourcefree synthetic
  engineering evidence and does not issue F5/F6/F7 science.
- The temporal pair is a declared synthetic modeled-rule pair, not empirical
  measured-wave comparison. It is not a substitute for original F7.
- P41 is invoked from its pinned historical callable packet through the new R06
  provider wrapper; no P41/J42/native source was edited or copied into the repo.
- R1 J42 tests remain as prior evidence; R2 does not claim them as the R05
  integration. Distinct independent reviewer required; no self-adoption.
