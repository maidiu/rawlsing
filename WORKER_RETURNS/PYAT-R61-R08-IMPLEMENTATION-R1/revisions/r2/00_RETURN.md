# R61-R08 R2 implementation return

**Verdict: REVISE for whole-progressive reach (unchanged owner/allowlist gap); R2 local repair is bounded-clean.** D1/D2/D3 are repaired at the assigned two-code-path boundary. The historical J42/P41/E04 bodies remain immutable archived recovery targets, so no full progressive PASS is claimed.

## Exact custody

- Correct R2 startup: `7beffc6d86bcd5585a63ea2c1afa6262bc9ca208`
- R2 code commit: `abf77ee10691adccb1127abd78aec49c6623ea37`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- Preserved v1/review/HQ artifacts untouched; writes only the same two code
  paths and this `revisions/r2/` report directory.
- Independent review input preserved: `1cc09784b007f63b2e486091466530f427900510`
  (review of earlier candidate `ad9c3088…`). HQ mechanical replay supplement at
  `WORKER_RETURNS/PYAT-R61-HQ-INTAKE-R1/r08_final_supplement/` read, not edited.

## What changed

### D1 — full K now binds actual producer determinants

`EvidenceRequest` K is versioned `@2` and now includes `request_id` plus the full
typed source/occurrence/unit/risk/target/condition/measure/authority/binding/
clock material. A producer binding is not accepted merely because a fresh K was
registered:

- `AdmittedEvidenceContext` is an explicit admitted context with source/
  release/risk/target refs tied to the actual owner objects, actual predicate
  authority refs, provenance refs, admission ref and all source/unit/measure/
  direction/role/clock/permission labels.
- Ordered condition occurrence and typed value are derived from the actual
  predicate leaves and consumer conditioner bindings, not copied from caller
  labels. Count, order, binding id, item/question semantic ref, option/exact
  value, typed tag/value, form/repeat and domain/state version must match.
- `EmpiricalProducerBinding.mismatch_reason` compares the complete requested K
  against the admitted context and actual owner determinants before any value
  can be served. Wrong-condition, boolean/null/integer value, extra/reordered
  condition, edition/digest/as-of/direction/role/design/weight/source and
  permission/clock mutations now resolve `UNKNOWN` / `IDENTITY_MISMATCH`, not
  `SUPPORTED`.
- The actual canonical provider call and unchanged
  `evaluate_positioned_subject_possibility` values-read survive; wrong requests
  cannot borrow the positive producer result.

### D2 — cache ingress now carries and verifies the full K/producer preimage

`CACHE_SCHEMA` is `@2`. Every exported entry now carries:

- `request_material` (full K preimage; recomputed hash must equal `request_key`);
- `producer_binding` (admitted context, actual-condition identities, validated
  conditions, binding hash, producer/query/predicate/release/model identities);
- evidence, consumer query, model rule, result and canonical seal (plus optional
  ephemeral issuer seal).

Import recomputes the full K hash, requires the context labels/refs and validated
conditions to equal K, requires query/rule/evidence source-release-target and
conditioner ids to equal K, replays the actual evaluator, and rebuilds
denominator/cells/values from producer evidence. Cached forged denominators or
cross-source evidence are rejected, not trusted. A self-sealed cross-source
forgery no longer imports or serves the victim K.

Trust is labelled honestly: default ingress is
`FULL_K_PRODUCER_ASSOCIATION_SHA256` (integrity/association, not issuer
authentication). `TrustedCacheIssuer` provides a test-only ephemeral HMAC
boundary for cold caches; without the exact issuer key a self-sealed record is
refused. No production secret is read.

### D3 — valid products no longer collapse to NO_SUPPORT

`reduce_required_support` now emits distinct productive states
(`VALID_NULL_PRODUCTIVE`, `DIFFUSE_PRODUCTIVE`, `VALID_EMPTY_PRODUCTIVE`,
`OBSERVED_ZERO_PRODUCTIVE`, or `MIXED_VALID_PRODUCTS`) while keeping
`ZERO_SUPPORT`, `UNKNOWN_SUPPORT`, `NO_SUPPORT`, `PARTIAL_SUPPORT`,
`EXACT_SUPPORT` and valid-empty-frontier distinct. Z `UNRESOLVED` denominator 16
is retained in `unresolved_denominator_support` and never exact support.

## Proof

Author suite with JUnit (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r2/junit.xml
```

**26 passed, 0 failed, 0 errors, 0 skipped, 7.13 s** (13 R08 tests + 13
unchanged C1 composition regressions).

Exact independent-review probe replay, from the immutable review blobs, with
JUnit (exit 0):

```text
PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q \
  .r61/reconciliation/r2/probes/test_r08v_baseline.py \
  .r61/reconciliation/r2/probes/test_r08v_hostile.py \
  .r61/reconciliation/r2/probes/test_r08v_e04_fixed_semantics.py \
  .r61/reconciliation/r2/probes/test_r08v_reach.py \
  --junitxml=.../revisions/r2/reviewer_probes_replay.xml
```

**19 passed, 0 failed, 0 errors, 0 skipped, 5.06 s.** This includes the original
7 canonical-positive/cold/severance/status controls, the 8 hostile probes that
formerly produced 7 D1/D2 failures, the actual E04 fixed-semantics observation
and the 3 reach/static probes. HQ's frozen baseline replay is therefore still
green, and HQ's exact hostile failures are now typed refusals.

Positive arithmetic remains independent: AT07 forward `POSITION=P1` cohort is
60 respondents, `yes=54`, `no=6`. Actual observed-zero law keeps denominator 60
with `no=0` and remains a supported/productive product. Actual `POSITION=P3`
ZERO_SUPPORT keeps denominator 0, no evidence/values, and no exact support.
Fresh-process cold replay of the full-K cache reproduces denominator 60 and the
same consumer result hash.

## Changed paths and blob refs

| Path | Git blob |
|---|---|
| `rawlsing_next/pre553_universal_evidence_binding.py` | `88e66ddd5de3c588e54470bf9aebcf2326d4f7d7` |
| `rawlsing_next/tests/test_universal_evidence_binding.py` | `5f05634ca49916eb7faf4ecf5a04895c11bd0dcc` |

Native owners used unchanged: provider `23167aa25291fb148b1e3cf210ac33fe7769b783`,
analytical composition `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`,
positioned evaluator `62e5eced47b64512f47b004e3e13a6ef3fe21de7`, empirical
objects `a61365b994e5c3c50de0f598fcf40e90abf757b6`, AT07 fixture
`0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`.

## Remaining exact boundary

Full J42/P41 progressive adoption and a repaired E04 terminal remain **NOT
REACHED**: at this candidate cut there is still no maintained non-test caller,
and the only exact adapter/service/terminal bodies are archived historical
returns outside the R08 allowlist. This is not converted into a global absence
claim and no archived return is edited.

Required separately granted owner amendment (unchanged from review `reach.json`):

1. live progressive adapter step: build/validate full K from actual producer
   objects, resolve through `EvidenceResolver`, return `EvidenceConsumerReader`
   values instead of a synthetic evaluator trace;
2. live progressive service: bind each step to its exact K, provenance and
   actual consumer result hash; remove trace-index association and
   unauthenticated `CACHED_PRODUCTION_CONSUMPTION`;
3. live E04 terminal: prove ZERO_SUPPORT/UNKNOWN/absent state fails the same
   top-level success assertion; this is a separate terminal proof, not a new
   broad court.

No new evaluator, source/science right, production/CI, original data, actor,
N11/N12, F6/F7/F8 or Sorok authority is issued. Author validation only; the
distinct independent reviewer for R2 has not been launched or self-adopted.
