# R61-R08 R3 implementation return

**Verdict: REVISE only for full-progressive reach (unchanged owner/allowlist gap). R3 closes the two R2 critical default-ingress defects at the assigned callable boundary with a real owner-admission/evidence-admission function. Positive actual provider/evaluator/consumer and fresh-process authenticated cache remain live.**

## Exact custody

- Startup: `f419e9a4b16638cf2de7700da60ab2a7e71986d9`
- R3 code commit: `3e5a53ce8905a361bce5a1ef9ddea05638b86f99`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- R2 independent review preserved: `db356748251c01e237df3a360a532ed8ffe45ec6`
- Writes only the same two code/test paths plus this `revisions/r3/` report root.
- Prior v1/R2/review/HQ artifacts were not edited.

## Generic function implemented

### Owner admission (D1-R2)

`TrustedOwnerAdmission` + `TrustedAdmissionAuthority` add a pinned, external
trusted-configuration boundary:

- Producer admission binds the exact admitted context ref, actual owner identity
  preimage (producer query, predicate, release, consumer query, model, actual
  predicate leaves/conditions, source/risk/target refs) and the full context
  labels.
- `EmpiricalProducerBinding` carries the admission. `EvidenceResolver.bind`
  verifies the HMAC against the resolver's trusted admission authority; a
  binding whose context differs from the admitted ref is stored but resolves as
  `UNKNOWN` / `OWNER_ADMISSION_UNRESOLVED`. It does not serve values.
- Caller construction of a matching request + context is therefore insufficient:
  the R2 forged-context pair (`FORGED_SOURCE`, 1999 clocks, forged digest/
  design/custody/permission/direction/role) is refused because the independently
  issued admission names the canonical owner context, not the caller's labels.
- Default resolver uses an explicitly labelled TEST_ONLY pinned admission
  authority. A host may pass its own `TrustedAdmissionAuthority`; its key/pins are
  trusted configuration, never accepted from request/context/cache material.

### Authenticated default cache ingress (D2-R2)

Cache entries now require both a trusted producer admission and, for supported
results, a trusted evidence admission:

- Producer admission verifies context ref, owner identity hash and HMAC.
- Evidence admission binds the exact evidence ref and `SHA256` of the complete
  evidence material content digest.
- Import recomputes the full K, context/query/rule/evidence source-release-target-
  condition association, verifies both admissions, replays the actual evaluator,
  and rebuilds denominator/cells/values from admitted evidence.
- Missing producer admission, a self-sealed entry, a rehashed same-source
  evidence preimage with denominator 999, a cross-source transposition, or a
  forged context all refuse before values are served.
- A legitimate cache exported by a resolver carries valid admissions and still
  replays in a fresh process with the same denominator 60 and consumer hash.
- `cache_trust_grade` remains the seal-layer label
  `FULL_K_PRODUCER_ASSOCIATION_SHA256`; `admission_grade` is the separate
  `TRUSTED_OWNER_EVIDENCE_ADMISSION_HMAC_SHA256`. The reports do not claim the
  seal alone is authentication.

### Preserved behavior

- Actual canonical AT07 provider remains `yes=54`, `no=6`, denominator 60, with
  the unchanged `evaluate_positioned_subject_possibility` invoked and values-read
  bound to the request K.
- Actual observed-zero keeps denominator 60 and `no=0`; actual ZERO_SUPPORT keeps
  denominator 0, no evidence/values, and no exact support.
- Typed condition values/order/occurrence, source/edition/digest/risk/direction/
  role/design/weight/clock/permission and currentness remain exact-K bound.
- Total axes and valid NULL/DIFFUSE/EMPTY/OBSERVED_ZERO productive states are
  preserved; Z `UNRESOLVED` denominator 16 remains unresolved, never exact.

## Proof

Author suite (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r3/junit.xml
```

**28 passed, 0 failed, 0 errors, 0 skipped, 7.04 s** (15 R08 tests + 13
unchanged C1 regressions).

Immutable independent R2/R1 probe replay (probe files reconstructed from the
pinned review commit; executable copies are disposable and untracked), exit 0:

**24 passed, 0 failed, 0 errors, 0 skipped, 6.03 s**, comprising:

- 7 retained baseline controls (positive arithmetic, actual evaluator spy, cold
  process, severance, observed-zero, zero-support, clock/permission),
- 8 retained hostile request-label probes (all now safe refusals),
- 1 actual E04 fixed-semantics observation,
- 3 reach/static probes,
- 3 R2 probes: forged caller context, self-sealed same-source denominator-999
  cache, default/issuer boundary,
- 2 R2 status probes: valid-product states and Z UNRESOLVED16.

The two R2 critical probes that previously failed now pass as typed refusals; the
actual positive and cold replay remain green.

## Changed paths and blob refs

| Path | Git blob |
|---|---|
| `rawlsing_next/pre553_universal_evidence_binding.py` | `759c5978a6ad876e2d013f3d98c06c6ccb8dd270` |
| `rawlsing_next/tests/test_universal_evidence_binding.py` | `db85977af03842cb3946e5cca6f74049516d4a69` |

Native owners unchanged: provider `23167aa2…`, composition `604c8d59…`,
evaluator `62e5eced…`, empirical objects `a61365b9…`, AT07 fixture
`0e384f72…` (full refs in proof_witness).

## Trust assumptions and limits

- The default TEST_ONLY admission authority/pin is trusted configuration in code;
  it is not accepted from request/cache subject material and issues no original
  source/science/CI authority.
- A host needing a different trust root must pass its own
  `TrustedAdmissionAuthority`; cache records from another authority refuse.
- This does not claim to defend against a hostile same-UID host with code or key
  access, and it is not R09 capture or a deployed protected service.
- Full J42/P41/E04 maintained integration remains **NOT_REACHED**: no maintained
  non-test caller exists at this cut, and the exact historical bodies are
  archived returns outside the R08 allowlist. The separately granted owner
  amendment (adapter step, per-step progressive K/provenance, E04 terminal
  proof) remains required. No archived return was edited and no full-progressive
  PASS is claimed.

No original data, source/science issuance, production/CI, N11/N12, F6/F7/F8,
actor, Sorok or J52/W52 authority is issued. Author validation only; the distinct
R3 independent reviewer has not been launched or self-adopted.
