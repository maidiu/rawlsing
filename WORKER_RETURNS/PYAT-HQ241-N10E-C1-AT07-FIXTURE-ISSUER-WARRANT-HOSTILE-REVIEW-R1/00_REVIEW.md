# PYAT HQ241 — AT07 fixture-use issuer warrant independent hostile review — R1

**Disposition: `C1_AT07_FIXTURE_ISSUER_WARRANT_PARTIAL__NAMED_DEFECT`**

**Reviewed immutable candidate:** `agent/rabochii-pyat-hq240-n10e-c1-at07-fixture-issuer-authority-warrant-r1 @ 3c6cfa0d29e10c1e2654e5fe22b0b62a0db891b9`  
**Commission tip:** `09f7a2a6c9c89791e8ec9639fa69c319fcef914c`  
**Mode:** Independent Browser/GitHub documentary hostile review only. No issuer, credentials, runtime or authority adoption.

## Disposition and calibrated result

HQ240 is a real improvement over the HQ236 R3 context proposal: it explicitly introduces a **new, prospectively HQ-granted, source-free AT07 build-instance issuance jurisdiction**, not a pretend extension of the existing C1-01 acceptance. It also separates registration of the exact source-free build, sealing of query/witness invocation, and recording of per-site use; proposes persistent epoch+sequence allocation, independent owner journal resolution, negative lifecycle, two exact site tokens and both preconstruction/provider gates.

Those elements **PASS as bounded documentary intentions**, not as presently admitted runtime authority. But the proposed warrant still leaves two authority-origin/entrypoint invariants to be invented by the eventual implementer. That is too much semantic discretion at the point HQ is asked to **adopt the warrant**. This review therefore does **not** recommend adoption yet.

### Blocker 1 — `HQ241-DEFECT-TRUST-ROOT-BOOTSTRAP-AUTHORITY-001`

The candidate's `candidate_issuer_epoch.root_bootstrap` describes an `owner deployment trust-root manifest pinned by authorized bootstrap` and root rotation `by explicit governed event`. The precise competent authorizer and **immutable bootstrap/rotation proof** are not frozen. The review does **not** demand an already minted key, live epoch/ref, or deployed verifier (all are correctly null at candidate grain). It demands a **candidate authority law** specifying which HQ-authorized operation records the initial issuer epoch, registrar writer capability, independently provisioned verifier journal root and its authoritative record; how the verifier distinguishes that root from an equally self-consistent forged root; and who may record a later root rotation/revocation.

The accepted C1-01 source-free content, I02 seal, I01 exact snapshot resolution, Z06 semantic maintenance and C1-03R product registration do not themselves grant this root-provisioning right. Nor does saying `authorized bootstrap` constitute its grant. Without this distinction, the proposed trust root can remain a caller or implementer-selected root dressed in an official ref. The fix is a **small additional HQ-rooted bootstrap receipt law**, not a new generic fixture registry, cryptographic signature regime, or F7 threat-model expansion.

### Blocker 2 — `HQ241-DEFECT-N10E-HANDOFF-SITE-EVENT-CUSTODY-002`

HQ240 correctly requires distinct `SOURCE_FREE_C1_01_COMPATIBILITY` and `SOURCE_FREE_N10E_LIFECYCLE` site credentials and says a N10E handoff must use **the same original registered build instance**. But the precise registration state machine permits `INVOCATION_SEALED -> SITE_USE_ACTIVE` for `C1 or N10E`; `candidate_site_use_record_preimage.cross_site_handoff_ref_or_null` is optional/null, with no N10E-specific non-null parent invariant. Its `owner.authorize_N10E_site_handoff` additionally lists an `exact C1→N10E handoff event` as an **input**, without defining the competent issuer or immutable event from which that input must come.

An implementation could consequently register a N10E site directly from a sealed build with a correct N10E token, **without proving a preexisting issuer-recorded C1 site-use parent**. Or it could accept a syntactically plausible externally provided handoff ref. Neither is the C1→N10E owner custody the commission requires. The correction must freeze a *distinct owner-issued handoff transition* containing the originating C1 site ref, exact originating invocation/witness, original unique build/receipt, authorized N10E recipient site, immutable issuer/journal event and non-null N10E handoff parent, independently resolved before provider/replay/lifecycle.

## Jurisdiction and conservation — PASS, not adoption

- HQ is the proposed competent future authorizer; `C1_AT07_SOURCE_FREE_FIXTURE_OWNER_ISSUER` is a **symbolic future issuer**, not a current accepted exact authority ref.
- Accepted C1-01 adoption `5fafb499d53dddadaf8a7b4fd46506e91a09d270` grants source-free producer–consumer/witness correctness, **not issuer competence**.
- I01 still has **18** literal kinds; the proposed `POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_MODEL_RULE` is not a currently adopted nineteenth kind. A narrowly administrative HQ fixture-use warrant is not itself an I01 snapshot. Any future I01 kind requires its own positive gate.
- I02 preserves validated `C11LogicalRelease`, Z06 governs semantic-authority revision/currentness, and C1-03R registers consumed dependent products; none is reassigned credential issuance.
- R8 exact `AT07_BIDIRECTIONAL_100`, full `REL-c1-at07` SHA256 `dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`, universe `ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2` and manifest `01ee5fa6db95efad3ce0acecd656f51beb6c2f2e21bc30e49bd358633f9ad6a1` match the accepted records. Older R3 release `8afa...` and the 110-row changed-source fixture are excluded.
- Static snapshot scope `AT07_FIXTURE_ONLY` is distinct from **actual canonical null** conditioner and 16-key witness effective time. The caller's `real_source_effect=false` string is not proof of fixture origin.
- No new real-source, actor/V3, semantic, comparability, pooling, threshold/smoothing, prediction, normative, field/proxy/walkback or model-rule authority is granted. Legacy `C1-AT07-MODEL@1.0.0` fixture remains nongenealogical, with historical rejected candidates excluded.

No jurisdiction conflict requiring outright REJECTION has been established. The two defects are **repairable, bounded candidate completeness gaps**; status remains PARTIAL, not ACCEPTABLE or adopted.

## Actual entrypoint crosswalk and productive proof

At the reviewed code blob, C1's test `_model(source)` builds from fixture `AuthorityRef` and `compose_positioned_subject_possibility` accepts it without registered context; the N10E request/provider/replay take eight input determinants and no `fixture_use_context_ref`. HQ240 correctly calls for distinct owner-native preconstruction factory + C1 compose ingress gate, owner-verified N10E locator/request, provider/receipt/replay identity and genuine Z06/C1-03R consumed determinants. These are **future contract interfaces**, not existing code. The handoff-specific registration law needs the above repair before these can be independently implemented.

I independently enumerated **30/30 unique hostile cases and six/six unique productive cases**. Their intended rejection and acceptance outcomes are explicit, but none was executed by this documentary review. Positive paths include C1 forward `54/60 = 9/10`, reverse `54/62 = 27/31`, N10E provider/replay, refused-result provenance without geometry, all six admitted Z08/A05 public states, and historical audit of revoked credentials. This is not a refusal-only contract; the missing trust and handoff invariants must be added **while preserving these positives**.

The six public Z08/A05 states remain `EXACT_SUPPORTED`, `EXACT_UNRESOLVED_PROXY_AVAILABLE`, `UNRESOLVED`, `VALID_EMPTY`, `NONCOMPARABLE`, `FAIL_CLOSED`. New issuer/credential validation failures are **preconstruction exceptions**, not a new seventh public state or laundering into returned `FAIL_CLOSED`. `FAIL_CLOSED` remains returned on the original specified Z08 source-scope and cross-source/release proxy conditions.

## Required correction and wake

**First**, repair the proposed warrant's HQ-rooted bootstrap/writer/verifier trust-root approval and rotation record; **second**, repair the C1→N10E owner-issued handoff event and mandatory N10E predecessor rule. Supply new hostile witnesses for forked roots and direct N10E registration with absent/forged C1 parent, plus positive cases exercising real C1→N10E handoff and lawful root rotation.

Then obtain another **independent warrant hostile review**. Only after a green disposition may HQ **explicitly adopt the bounded issuer warrant and its exact authority bootstrap**. Only then a separate commissioned R3→R4 model-rule authority correction/recomputation, new independent R4 hostile review, HQ R4 adoption, and separately commissioned Space Bunny production qualification/lifecycle re-freeze.

No production or tests were changed; no credential/issuer/root was instantiated, no model-rule R4 identity was frozen, and no merge, self-adoption, real-source, or actor operation occurred.

**TERMINAL: `C1_AT07_FIXTURE_ISSUER_WARRANT_PARTIAL__NAMED_DEFECT`**
