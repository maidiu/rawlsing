# R61-R08 R4 implementation return

**Verdict: REVISE for full-progressive reach only (unchanged owner/allowlist gap). The R61Q D1-D6 trusted-host admission/consumer boundary is implemented at the assigned two-path grain. Positive native, actual evaluator, status and cold replay remain live under explicit trusted configuration.**

## Custody

- Startup: `84704f4a775d0419ad4a08c8c687bc815df47adc`
- API/trust contract commit (banked before code): `07d94592af4773afb7fa01cdde1f605d820b44f4`
- R4 code commit: `3c69a13e64dd2bca65858906a367347e895f9d82`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- R61Q decision read: `99222514afbac4fc1671dbc90f02b210e6c1f6ce`
- R3 review read/preserved: `5b7e338086cd86a9a011c1e911a2b85b9170239f`
- Writes only the two allowlisted code/test paths plus this `revisions/r4/`
  root. Prior v1/R2/R3/review/HQ bytes unchanged.

## Delivered function

`API_TRUST_CONTRACT.md` was committed before code. It specifies the trusted
supervisor/executor, verification-only subject ingress, producer/owner pinning,
complete executed-result envelope, cold verifier provisioning and intentional
legacy-default incompatibility.

- **D1:** `EvidenceResolver()` has no accepting default. Without a configured
  verifier it returns `UNKNOWN` / `NO_CONFIGURED_TRUST_ROOT`; import/export and
  reader refuse. The source-visible default key/singleton was removed.
- **D2:** producer admissions are issued only by trusted setup; bind verifies the
  HMAC over exact context ref + actual owner identity, checks exact typed
  conditions/source/release/query/predicate/risk/role/clock/consumer/model, and
  pins the actual producer callable (`admitted_producer`). Callable substitution
  is not admitted.
- **D3:** `ExecutedEvidenceEnvelope@1` is signed only after actual provider and
  unchanged evaluator completion. It binds full K material/hash, context/owner
  identity, source/release, provider receipt/fact/state, evidence ref and full
  content digest, consumer query/model, evaluator hash, separate
  eligibility/execution/result axes, uncertainty, denominator/cells/values and
  trust domain/version/grade. Cache export preserves the original envelope; it
  does not re-sign arbitrary results.
- **D4:** `TrustedAdmissionVerifier` exposes verification only; resolver/reader
  expose no signing/key export. `EvidenceConsumerReader(request, result,
  verifier=...)` requires the same configured root and a valid envelope. A
  caller-created result, attacker issuer with the same id, or self-consistent
  evaluator hash alone cannot satisfy the real consumer.
- **D5:** cold cache carries request/owner/envelope/evidence/query/rule/result and
  signature, never a key. The key is delivered separately to the fresh process
  via stdin (no key in committed files/logs/argv/cache). Wrong-root, missing
  envelope and forged evidence refuse.
- **D6:** cache `@3`, result `@3`, admission `@2`; implicit-default legacy records
  refuse rather than auto-upgrade. K/typed condition/status/science semantics are
  unchanged.

## Positive and status evidence

Actual AT07 forward provider: 60 respondents, `yes=54`, `no=6`, denominator 60,
`EXACT_SUPPORTED`; actual evaluator called and values-read bound to signed
envelope. Actual observed-zero: denominator 60, `no=0`, supported. Actual
POSITION=P3 ZERO_SUPPORT: denominator 0, no evidence/values. VALID_NULL/DIFFUSE/
VALID_EMPTY/OBSERVED_ZERO remain distinct productive states; Z `UNRESOLVED`
denominator 16 is retained and never exact support. Changed A0/A1 and
`CHANGED_SOURCE_LAW` cases remain genuinely distinct.

## Tests

Command (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r4/junit.xml
```

**31 passed, 0 failed, 0 errors, 0 skipped, 7.267 s** (18 R08 tests + 13
unchanged C1 composition regressions). See `COVERAGE_MATRIX.md` for exact D1-D6
and eight-falsifier mapping.

The R1/R2/R3 probes that depended on implicit public-key/default acceptance are
intentionally superseded under D1/D6; they are not counted as safety failures.
The same positive/zero/cold/status controls are re-qualified with an explicitly
configured trusted host fixture. No archived probe was edited.

## Reach and limits

Covered at this callable grain: signed trusted-host admission, actual
provider/evaluator/consumer values-read, complete executed envelope, cache
replay, status reduction. NOT_REACHED: live J42 `E41ProviderAdapter.step`, live
P41 progressive and repaired live E04 terminal. This remains an owner/
integration-allowlist boundary; archived returns were not edited.

No original data/source/science, production/CI, N11/N12, F6/F7/F8, actor,
Sorok, J52/W52 or protected-capture authority is issued. Same-UID host/key
compromise, ptrace/root and a dishonest competent issuer remain outside this
scoped threat model. Author validation only; distinct R4 hostile reviewer has
not been launched or self-adopted.
