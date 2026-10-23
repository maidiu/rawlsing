# R61-R08V R3 finite defects

Verdict: **REVISE.** R3 closes the two exact R2 probe shapes but the actual
public issuance/admission boundary is not externally trusted. Two critical
callable-grain defects remain; both use the module's own public default
authority and source-visible key, not a forbidden same-UID host attack.

Severity: D1-R3 (critical) = D2-R3 (critical). The prior no-admission probes are
repaired. Positive capability is present and preserved.

## D1-R3. Default public authority mints admission for a forged full context

**Expected:** the public default path must not let an untrusted caller mint an
accepted producer admission for source/edition/digest/instrument/units/estimand/
weight/design/uncertainty/direction/role/consumer-use/grammar/custody/clock/
permission labels it chose. A source-visible default HMAC key plus public
`issue_producer` is not external trusted issuance.

**Observed:** with a forged context (`FORGED_SOURCE`, edition `1999-01`, forged
digest/design/direction/role/clocks/permission) and matching request, the caller
called the exported default
`R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY.issue_producer(context_ref=<forged>,
owner_identity_material=<forged binding>)`. `EvidenceResolver.bind` accepted the
HMAC; `resolve` returned `SUPPORTED`, denominator 60, provenance
`CANONICAL_PRODUCER`; `EvidenceConsumerReader` read denominator 60. The actual
producer was still the unchanged forward P1 provider. Observation:
`outcomes/r3_observations.json` key `forged_context_public_mint`.

**Why:** `R61_TEST_ONLY_OWNER_ADMISSION_KEY` is a source constant at
`pre553_universal_evidence_binding.py:1345`; a live default authority is created
at `:1532`; `EvidenceResolver()` selects it by default at `:1578-1584`; `bind`
verifies with it at `:1601-1607`. The author's
`test_forged_caller_context_cannot_mint_owner_admission` signs the *canonical*
context while binding the forged one, so it only tests a mismatched pair. It
does not exercise the public minting factory with a self-consistent forged pair.

**Minimal reproduction:** `probes/test_r08v_r3_issuance_boundary.py::test_default_public_authority_must_not_admit_forged_caller_context`.
Expected safe result is typed refusal/UNKNOWN and consumer
`EvidenceAssociationError`; observed `SUPPORTED` / 60 / consumer 60.

## D2-R3. Default cache ingress accepts forged evidence re-signed with the public key

**Expected:** default public cache ingress must not accept a same-source
denominator/value forgery merely because the caller can invoke the module's own
public evidence-admission factory. The complete-content digest is only useful
if the issuer/key is not available to the subject.

**Observed:** starting from a legitimate exported cache entry, the caller built
forged same-source evidence (`raw_support=999`, yes=999, no=0), called
`R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY.issue_evidence(producer_admission=<valid
exported producer admission>, evidence=<forged evidence>)`, and resealed the
entry. Default `EvidenceResolver().import_authenticated_cache` accepted it;
`resolve` returned `SUPPORTED`, denominator 999, provenance
`AUTHENTICATED_CACHE`; `EvidenceConsumerReader` served denominator 999 with
`admission_grade=TRUSTED_OWNER_EVIDENCE_ADMISSION_HMAC_SHA256`. Observation:
`outcomes/r3_observations.json` key `forged_evidence_public_resign`.

**Why:** evidence admission is signed and verified with the same public default
authority (`issue_evidence` `:1464-1490`; import verification `:1978-2080`). The
factory is a public oracle for exactly the content digest check the design
relies on. Separately, `issue_evidence` checks only `authority_id`, not the
producer token, before issuing.

**Minimal reproduction:** `probes/test_r08v_r3_issuance_boundary.py::test_default_ingress_must_reject_evidence_resigned_with_public_default_key`.
Expected refusal; observed import/`SUPPORTED`/999/consumer 999.

## Repaired at this grain (not defects)

- Exact R2 D1 probe with **no** admission: `UNKNOWN` /
  `OWNER_ADMISSION_UNRESOLVED`, consumer raises. Reviewer probe
  `test_missing_admission_still_refuses_old_r2_context_relabel` passes.
- Exact R2 D2 probe with **no** producer/evidence admission: import raises
  `EvidenceCacheIntegrityError`; author and retained R2 probe pass.
- Legitimate canonical admission, actual provider/evaluator values-read, and
  fresh-process cache replay remain green (reviewer positive control passes;
  author 28/28; retained probes 24/24).
- Status axes and Z UNRESOLVED16 remain unchanged in retained controls.

## Missing function

External trusted issuance/authentication of admissions. The default must either
accept no admission authority and fail closed/typed-UNKNOWN until a host injects
an externally pinned authority whose key is not source-visible, or consume an
external issuer attestation the request/cache subject cannot mint. This is one
bounded stronger-engineering decision, not a fourth canary patch or another
named-probe branch. A caller-configured issuer/authority remains legitimate
protected-host configuration only when the subject-facing default cannot supply
or mutate it.

## Non-defect reach boundary

Live J42 `E41ProviderAdapter.step`, live P41 progressive serving and the live
E04 terminal remain NOT_REACHED at this candidate cut. The prior reach evidence
is retained by identity at `db3567482` / `1cc09784b` and the historical blobs
named there; no archived return was edited. This is an owner/integration
permission boundary, not authority to broaden the R08 allowlist or fake
adoption.
