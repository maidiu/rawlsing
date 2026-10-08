# PYAT HQ242 — C1/N10E source-free AT07 issuer warrant root and handoff correction — R2

**Disposition:** `C1_AT07_FIXTURE_ISSUER_WARRANT_R2_CANDIDATE_COMPLETE__READY_FOR_HOSTILE_REVIEW`  
**Commission tip:** `1cac84eac8846130bd12e9bf591ff3010c9c4b62`  
**Governed parent:** HQ241 hostile review `7c7937ff68ddd6209858cc23194b9f292b299e66`  
**Status:** **PROPOSED_NOT_ADOPTED**. Documentary authority-warrant candidate only, not permission to issue or install credentials.

## Precisely two corrected defects

**(1) `HQ241-DEFECT-TRUST-ROOT-BOOTSTRAP-AUTHORITY-001`: freeze HQ-controlled trust-root bootstrap and rotation.** Only HQ can authorize the initial issuer epoch and separately approve its immutable root placement by `HQ_APPROVE_AT07_ISSUER_ROOT_PLACEMENT`, then **activate** after independent C1 owner installation and verifier-read-root acknowledgment by `HQ_ACTIVATE_AT07_ISSUER_EPOCH`. The registered issuer is the future single HQ-designated C1-01 source-free fixture-owner assembly, not a test fixture, I01, I02, Z06, C1-03R or a caller. The record form is frozen: exact adopted warrant/HQ approving event, issuer and unique epoch, C1 owner assembly/deployment manifest, journal genesis/root content hash, registrar writer principal+capability ID, independently pinned verifier reader root/ID, callsite ingress identities, exact root approval/activation events and validity. All refs remain **null/unissued** here. Root bytes are prepared by the designated C1 owner, *approved by HQ*, installed through a deployment artifact pinned to that exact approval independently of the caller and registrar response, independently acknowledged by the verifier, then activated by HQ. An equally internally self-consistent forged root cannot satisfy that independently placed approval-and-activation chain. No cryptographic key or operational root has been generated.

Rotation/revocation is also a specific **HQ-governed** operation: exact prior active epoch and root, new distinct issuer epoch and approved deployment manifest, atomic cutover/negative currentness receipt, independent verifier placement, historical audit only under revoked old root. No `LATEST`, default, branch-head fallback, silent root reuse, duplicated sequence after restart or caller-originated root. The root-placement operator is a constrained function of the named C1 owner assembly, **not a new independent authority**. Against ordinary caller data this is a proposed independent trusted placement; it does **not** claim security against arbitrary hostile privileged Python code. If a stronger threat model or an independent external provisioner later proves necessary, HQ must explicitly authorize that separate power; this packet grants none.

**(2) `HQ241-DEFECT-N10E-HANDOFF-SITE-EVENT-CUSTODY-002`: require owner-issued C1 predecessor for N10E.** The overly general HQ240 `INVOCATION_SEALED → SITE_USE_ACTIVE` transition is superseded. The **only** permitted chain for N10E is:

`BUILD_REGISTERED → INVOCATION_SEALED → C1_COMPATIBILITY_SITE_USE_ACTIVE → C1_TO_N10E_SITE_HANDOFF_REGISTERED → N10E_SITE_USE_ACTIVE`.

The future C1 owner's **privileged registrar** issues `REGISTER_C1_TO_N10E_SITE_HANDOFF`, but only after retrieving a CURRENT, journal-committed, issuer-authenticated C1 compatibility use event. The handoff freezes **the original unique build-instance/receipt, exact C1 site, invocation seal, producer query/predicate, consumer query, conditioner fingerprint and CLOSED 16-key witness, source/universe/release, actual null effective context, issuer/epoch, trusted C1 ingress and approved N10E receiver**. A proper N10E site requires a **non-null independently resolved** `cross_site_handoff_ref`, same original instance and a distinct separately registered `SOURCE_FREE_N10E_LIFECYCLE` use. The C1 site alone may lawfully have no handoff predecessor.

A valid-looking caller handoff locator, separately rebuilt 100 identical AT07 rows, mere use-token string, issuer-null registration, revoked C1 parent or wrong N10E receiver is **REFUSED before provider/replay**. Both positive and REFUSED provider receipts, replay and genuine consumed dependency records retain exact issuer root, original build, C1 site, handoff and N10E site lineage. Archival audit never reactivates a revoked parent.

## Boundaries explicitly conserved

Only synthetic `AT07_BIDIRECTIONAL_100`; R8 exact `REL-c1-at07` full hash `dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`; universe `ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2`; source manifest `01ee5fa6db95efad3ce0acecd656f51beb6c2f2e21bc30e49bd358633f9ad6a1`. Changed-source `AT07_BIDIRECTIONAL_110_CHANGED_SOURCE_LAW` excluded; obsolete R3 release excluded. Source-free `real_source_effect=false` must be owner-proven, not caller-selected. `AT07_FIXTURE_ONLY` is the static AuthoritySnapshot interval, **not** the actual conditioner and 16-key witness effective context: both actual values must be canonical `null`, not wildcard.

No I01 nineteenth kind has been admitted (18 current kinds); no independent model rule, positive real-source, source semantic, cross-source composition/comparability, actor/V3, P07/F7, threshold, smoothing, prediction or normative authority is acquired. The six original Z08/A05 public result states remain `EXACT_SUPPORTED`, `EXACT_UNRESOLVED_PROXY_AVAILABLE`, `UNRESOLVED`, `VALID_EMPTY`, `NONCOMPARABLE`, `FAIL_CLOSED`. Wrong issuer, bootstrap, scope or handoff are **preconstruction exceptions**, never manufactured returned `FAIL_CLOSED`. Earlier HQ236 R3 eleven hashes were independently verified but remain **unadopted** and nongenealogical; this R2 does **not** mint R4 model-rule identities.

## Entrypoint and proof coverage

The actual C1 test `_model(source)` can construct a fixture model without an issuer; the real C1 `compose_positioned_subject_possibility` presently has no context gate. The actual N10E `EmpiricalPossibilityProviderRequest` still takes **eight fields**, with no `fixture_use_context_ref`. This R2 **proposes**, but does not implement, separately owner-gated C1 stable-rule creation and composition, owner-issued handoff, N10E separately registered site, required N10E `fixture_use_context_ref: ExactRef` plus independent issuer-root/ancestor verifier, and exact receipts/replay/currentness. Existing unrelated C1 routes are not silently made unconstructible.

The original 30 future hostile and six positive courts are copied **unchanged** into the R2 court packet, with **13 additional hostile** and **four additional positive** discriminating cases covering forged roots, wrong approver, absent approval, stale/rotated root, duplicate epoch/sequence, absent C1 ancestry, fake non-null handoff, wrong original build/witness/receiver, revoked parent, and actual HQ-rooted C1→N10E positive provider/replay plus root-rotation positives. **No court executed in HQ242.** Refusal-only success remains prohibited; forward 54/60 and reverse 54/62 and all six Z08/A05 states must remain productive once all independent later gates are lawfully green.

## Strict authority sequence

This is a **candidate** for a fresh independent hostile R2 review. If and only if green, HQ may separately decide to adopt the narrow issuer warrant and then issue/approve/activate exact trust-root and issuer operational records. **Only afterward** separately commission the owner-native R3→R4 model-rule candidate with exact *adopted* warrant dependency, all transitive hash recomputation, an independent R4 hostile review and explicit HQ model-rule adoption, followed by separately commissioned production Space Bunny implementation and governed runtime/lifecycle courts.

No authority adoption, bootstrap approval, root activation, journal write, handoff/credential issue, test or production mutation, real-source work, actor/V3 work, R4 freeze, self-adoption or merge occurred.

**Terminal: `C1_AT07_FIXTURE_ISSUER_WARRANT_R2_CANDIDATE_COMPLETE__READY_FOR_HOSTILE_REVIEW`**
