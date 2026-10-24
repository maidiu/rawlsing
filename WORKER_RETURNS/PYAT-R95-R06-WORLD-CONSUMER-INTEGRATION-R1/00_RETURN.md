# R95 R06 author return — source-separated world selected-view binding

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`
- Startup: `a7f5cc70520e5236c24bbac241fad071c026d881`
- Contract commit: `2f1d67e87a9803d3db6db2773cf3b2589877999c`
- Code commit: `7f28ca4ad241a749e85ce6bbdac8f25795b80468`
- Executor: existing OpenCode DeepSeek V4.1-Flash MAX/Global.

## Delivered

Added `pre553_universal_world_binding.py`: typed source-indexed world fields,
selection request and selected-view result. The binding validates exact source/
release/field/unit/role/clock identities, refuses unlinked unit pooling without
an authorized transport relation, refuses context promoted to structural without
FF authority, refuses unobserved temporal pairs, and requires consumer
conditioner bindings to match the field coordinate/subject-fact set.

Positive qualification invokes the actual unchanged N10E positioned-subject
consumer through `compose_positioned_subject_possibility` with two distinct
admitted fields (X and O). Both fields affect the same consumer result/view
hash; cold subprocess recomputation reproduces the exact view/consumer hash.
Hostile controls cover wrong source/release, person/household pooling, contextual
structural promotion, unobserved temporal pair, and revoked currentness.
Authorized relation/transport plus observed temporal-pair controls pass.

## Commands

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/junit.xml -o addopts=''
```

Exit `0`; `4 passed`, `0 failed/errors/skips`; `2.43s`.

## Blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `6ecc472378efb5b2bf6d87b218a23147ec2bda45` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `50ee595980c91227ba6bcced04475abf1e997b7f` |

Manifest excludes itself. Existing W41/F43/FF/temporal/J42/P41/N9/N10W/E04 and
accepted R03/R04/R05/R08 bodies were not edited.

## Explicit limits / unmet requirement

The actual two-field view is wired to the N10E positioned-subject consumer. The
R05 learned-world consumer path was not completed for the two-field predicate:
the learned product is bound to its original single-conditioner producer
predicate, and substitution correctly refuses. Full learned-product/world
integration therefore remains open. No N9/N10W/E04 replacement engine was
created. No original source/science, FF/F6/F7 issuance, R04/R05 replacement,
CI/prod/N11/N12/Sorok/J52/W52. Distinct reviewer required; no self-adoption.
