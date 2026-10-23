# R61-R08V R2 finite defects

Verdict: **REVISE.** R2 repairs the prior named request-label and cross-source
cache probes and the valid-product summary conflation, but the public default
trust boundary still accepts forged caller-owned contexts and self-sealed
same-source evidence preimages. Two critical local defects remain at the callable
grain. Full progressive J42/P41/E04 adoption is separately NOT_REACHED for an
owner/allowlist reason and is not counted as a local defect.

Severity order: D1-R2 (critical) > D2-R2 (critical). Prior D3 is repaired.

## D1-R2. Caller-owned context can relabel the unchanged real producer

**Expected:** source/dataset/wave/edition/byte digest/instrument/units/estimand/
weight/design/uncertainty/direction/role/consumer-use/grammar/custody/clocks/
permission must match resolved owner objects or an independently authenticated
admission. A caller must not be able to construct a context that changes those
labels while the same actual producer is accepted as exact support.

**Observed:** a caller-built `AdmittedEvidenceContext` (and matching
`EvidenceRequest`) naming `FORGED_SOURCE`, edition `1999-01`, a forged byte
digest, instrument, sampled/reporting units, estimand, weight method, design,
uncertainty, direction `ANSWER_YES_TO_POSITION`, role `REVERSE_AUTHORIZED`,
consumer use, grammar, custody, 1999 clocks and a forged permission was bound to
the unchanged forward P1 provider. `resolve` returned `SUPPORTED`, denominator
60, provenance `CANONICAL_PRODUCER`; `EvidenceConsumerReader.read()` returned the
forged labels and denominator 60. Observation:
`outcomes/hostile_observations.json` key `forged_context`.

**Why:** `AdmittedEvidenceContext.__post_init__`
(`rawlsing_next/pre553_universal_evidence_binding.py:328-376`) validates shape,
not owner provenance. `EmpiricalProducerBinding.__post_init__` (`:936-960`)
cross-checks only `source_universe_ref`, `release_ref`, `risk_set_ref`,
`target_ref` and `authority_refs`. `_context_matches_request` (`:894-915`) and
`mismatch_reason` (`:962-1010`) compare the request to the same caller context,
so mutually consistent forged labels pass. The return's claim that context
labels are "tied to actual owner objects" holds only for that subset.

**Minimal correction direction:** derive the remaining context labels from the
actual source/repository/instrument/design/permission/admission owners, or
require an externally pinned authenticated context/binding hash (or issuer) and
fail closed when unresolved. Do not treat a caller-authored hash as owner
authentication. At minimum, refuse `SUPPORTED` when a context label has no owner
anchor, and expose the caller-trust assumption explicitly rather than as
subject-facing evidence. Probe fails as expected:
`probes/test_r08v_r2_hostile.py::test_caller_owned_context_labels_cannot_relabel_real_producer`.

## D2-R2. Default self-sealed cache accepts forged same-source denominator/values

**Expected:** default public cache ingress must reject a self-sealed/rehashed
evidence preimage that is not bound to the actual producer, including a
same-source semantic substitution with changed denominator/cells. A checksum or
association digest is not issuer authentication.

**Observed:** using the victim request K and its exported producer-binding/query/
rule material, a resealed entry with forged evidence `raw_support = 999` and
forged `yes=999, no=0` cells imported successfully with default
`EvidenceResolver()`. `resolve(victim)` returned `SUPPORTED`, denominator 999,
provenance `AUTHENTICATED_CACHE`, trust grade
`FULL_K_PRODUCER_ASSOCIATION_SHA256`; `EvidenceConsumerReader.read()` returned
denominator 999. Observation: `outcomes/hostile_observations.json` key
`forged_cache`. The prior cross-source forgery is now rejected by the retained
probe; same-source rehashing is not.

**Why:** `export_cache` (`:1624-1660`) includes evidence material but
`import_authenticated_cache` (`:1662-1842`) verifies only the self-seal,
request-K preimage equality, internal context/query/rule/condition consistency,
and evaluator replay over the supplied evidence. It never authenticates the
evidence against a producer, and `raw_support`/geometry are not bound to
`evidence_ref` by a content digest. `EvidenceResult` then accepts the forged
denominator/cells, and `_replay_cache` (`:1552-1622`) recomputes only from the
forged evidence.

**Minimal correction direction:** require an authenticated producer evidence
preimage at the default ingress (externally pinned trusted binding/evidence
hash or issuer), verify the evidence content digest, and rebuild evidence from
the actual producer. If the default is intentionally only an association cache,
it must not resolve as `AUTHENTICATED_CACHE`/serve subject-facing values without
an explicit issuer-bound or trusted-binding configuration; self-sealed
candidate input must be typed refusal. Probe fails as expected:
`probes/test_r08v_r2_hostile.py::test_self_sealed_same_source_denominator_999_must_refuse`.

## D3 (prior). Repaired at this grain

`reduce_required_support` now emits distinct `VALID_NULL_PRODUCTIVE`,
`DIFFUSE_PRODUCTIVE`, `VALID_EMPTY_PRODUCTIVE`, `OBSERVED_ZERO_PRODUCTIVE` and
`MIXED_VALID_PRODUCTS`; `ZERO_SUPPORT`/`UNKNOWN` do not become exact/all-support;
Z UNRESOLVED denominator 16 is retained; a supported positive remains
`EXACT_SUPPORT`. Reviewer status probe 2/2 passes.

## Replayed repairs (not defects)

- Request-label/typed/order/clock/permission mutations against the original
  binding now refuse; prior hostile 8/8 pass.
- Actual provider/evaluator values-read, independent 54/60 arithmetic, fresh
  process cold cache, changed current/as-of/permission non-hit all pass.
- Author 26/26 and retained reviewer 19/19 pass.
- Cross-source cache transposition refuses.

## Non-defect reach boundary

At `f419e9a4b`, `git grep -l pre553_universal_evidence_binding -- '*.py'` finds
only the module and its own test. Historical J42 (blob
`40f1e9f69fafff37f6bc44474b0189543d4997b3`) records a synthetic evaluator trace
without an actual call; historical P41 (blob
`7d428106c79bcc56973f7c0044fc273a2b354554`) consumes trace entries by index with
a `CACHED_PRODUCTION_CONSUMPTION` fallback; archived E04 (blob
`2181b832d3c4376d4b9428e13f4354f273be8f32`) still returns top-level success for
a `ZERO_SUPPORT` step. These are immutable archived recovery targets outside the
R08 write allowlist. Editing them would be false adoption. The remaining
full-progressive gap is an integration-permission/owner-interface requirement,
not a local module defect; the exact amendment is in `outcomes/reach.json`.
