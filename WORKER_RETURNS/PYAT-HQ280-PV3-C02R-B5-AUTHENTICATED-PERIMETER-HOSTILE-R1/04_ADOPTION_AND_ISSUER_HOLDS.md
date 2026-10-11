# 04 — Adoption, issuer and trust holds

**Disposition:** `INDEPENDENT_HOSTILE_REVIEW__BOUNDED_CANDIDATE_ACCEPTED_AS_HONEST__NOT_CERTIFIED_AS_AUTHENTICATED_PERIMETER__F8F_B5_TRUST_HOLD_OPEN__NO_ADOPTION`

This review issues nothing, adopts nothing and authorises nothing. It records that the candidate
does the same.

---

## 1. Holds that remain OPEN after this review

### H1 — PRODUCER-ISSUER HOLD (carried forward from F8F, unchanged)

No accepted producer credential, key registry, signature scheme or issuer exists in the repository.
Runtime evidence: `H3` finds **0** modules performing signature or credential verification, and the
accepted M2 release owner has **0** lines mentioning issuer/credential/signature/authorization.
`M2.register_producer_subject` and `M2.constitute_release` take plain data.

Consequence: nothing in this candidate, and nothing in the accepted M2 owner, establishes that any
release was **issued by a competent producer**. The candidate's own summary sentence — a subject
"corresponds to material the M2 owner actually issued" — is **not supported**; the runtime supports
only "corresponds to a well-formed release present in the owner's M2 repository".

**Required act to close:** an accepted producer-issuance authority (custody, credential and
revocation semantics), which no commission in this wave grants.

### H2 — ENFORCEMENT-SURFACE HOLD (new, raised by this review)

The perimeter is an optional parallel surface, not an enforced boundary:

- `pre553_learned_world_composition.py` publishes to B5 at lines 1203/1206/1219 and **never imports**
  the C02 module;
- `LearnedProductLifecycleExecutor.stage_protocol` / `from_checkpoint` remain public accepted-owner
  entries that bypass the perimeter;
- the perimeter's only gated entry is `AuthenticatedB5Ingress.publish`.

**Required act:** either (a) make the perimeter mandatory for every B5 publication path including
rehydration (a change to accepted owners, out of this commission's scope and not granted), or
(b) rename this artefact honestly as a **caller-side facade** and record H2 as an open F8F-family
hold. Option (b) is available now and requires no new authority.

### H3 — REPLAY HOLD (C02 residual R2, confirmed accurate)

`REPLAY_COMPLETE` remains an owner-held claim, gated by the M2 replay closure's declared
`replay_grade`. C02 binds it honestly and refuses non-accepted grades (probe E5). It is **not** an
independent replay re-execution. `HISTORICAL_EXPLANATION_ONLY` remains publishable and correctly
labelled.

### H4 — AUTHORITY HOLD (C02 residual R1, confirmed accurate)

The semantic `authority_snapshot_refs` are owner-held; no accepted AuthoritySnapshot issuer exists.
Probe G6 shows the **permission ceiling** is likewise pure owner custody: any ceiling, including a
self-declared `urn:c02r:TOTAL_CONTROL`, publishes successfully. Nothing validates a ceiling.

### H5 — IN-PROCESS ENFORCEMENT-STATE HOLD (new, minor)

`EXPECTATION_KEY_TYPES` is a module-level mutable `dict`. Probe L1b weakens it and admits a
wrong-typed expectation past the fail-closed type gate (value comparison still refused the
mismatch). The custody containers themselves are correctly `MappingProxyType` and have no unmount
surface (L2).

---

## 2. What this review explicitly does NOT do

- No canonical, PRE-MAIN, root-manifest or semantic mutation.
- No adoption of C02, of F8F, or of itself.
- No G0b, no G1 selected service, no operative CURRENT publication, no V3 actor permission.
- No scientific-competence claim about the producer, and none is inferred from technical
  authenticity.
- No source read (no raw SAV/DTA), no respondent-lineage republication.
- No ZIP relay; delivery is commit and push only.

## 3. Development-grade custody versus an operative issuer

The commission required this distinction, and the runtime makes it unambiguous:

| property | C02 perimeter | an operative issuer would require |
|---|---|---|
| who can admit a release | whoever holds the `M2Repository` and writes custody | a credential/custody authority outside the caller |
| what "authentication" compares | owner-built subject vs owner-authored expectation | subject vs issuer-signed/evaluated preimage |
| revocation | owner-held exact sets (`RevocationLedger`) | issuer-published, externally attestable revocation |
| trust root | the owner process's own state | an issuer independent of the publishing process |
| in-process attacker | explicitly unproved (R4), and bypassed via F1/F2 | attacker-resistant |

So: **C02 is development-grade owner custody. It is not an operative issuer and not an
attacker-resistant trust root.** C02 says this itself; this review confirms it from runtime
behaviour rather than from the declaration, and adds that the bypass is not hypothetical — it is
reached from a production composition module and from a one-dict checkpoint.

## 4. Certification statement

- **Bounded technical candidate: ACCEPTED AS HONEST WORK.** Its evidence reproduces exactly, its
  refusals are real, its positives are real, and its declared residuals R1–R4 are materially
  accurate.
- **Authenticated B5 perimeter: NOT CERTIFIED.** F8F K4/K5 remains open at owner level (B1/B2/B3)
  and at rehydration level (H1/H2); no producer authenticity is established (D1/H3).
- **Adoption / G0b / CURRENT / trust root: NONE.**
- Terminal: `HQ280_PV3_C02R_B5_AUTHENTICATED_PERIMETER_HOSTILE_REVIEW_RETURNED__NONISSUING__GITHUB_PUSHED`
