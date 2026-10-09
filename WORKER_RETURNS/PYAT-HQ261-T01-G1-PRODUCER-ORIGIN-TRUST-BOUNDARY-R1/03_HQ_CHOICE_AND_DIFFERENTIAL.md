# HQ261 T01 — HQ choice, differential and one implementable successor

**Terminal:** HQ261_T01_RETURNED__NO_SELF_ADOPTION  
**Classification:** INDEPENDENT_SECURITY_SEMANTIC_REVIEW__CONDITIONAL_INGRESS_ARCHITECTURE_FOUND__NO_EXECUTION_OR_AUTHORITY_ADOPTION  
**Scope:** G1 first producer-origin trust, source-free C1→selected applicability/G2→F8 only.

## A. Differential against G01's return (not an author paraphrase)

| Issue | G01 returned claim/evidence | Independent T01 ruling |
|---|---|---|
| Is G1 genuine? | Caller replaces PossibilitySliceEvidence provenance_refs/authority_refs; F8 result and replay unchanged. Reported test file blob 4babf7eeada1241dd69ac9742dd87819a95341d6, 10 pass. | **AFFIRM.** F8 and bound F8 inspect source admission but not evidence provenance/authority; exposed caller-evidence route is untrusted. |
| Does C1 already carry producer lineage? | G01 acknowledges composed identity binds authority/provenance, but calls it disconnected from F8. | **AFFIRM with important qualification.** C1 evidence_ref is computed from a preimage that *already includes* source, geometry, authority and provenance, while the C1 composed hash binds evidence_ref and full ancestry. A selected **owner-executed** direct call can preserve that provenance rather than reconstruct it from caller claims. |
| Does recomputable hash disprove every in-process repair? | G01 claims no in-process control can authenticate producer origin because Python modules are mutable and caller may recompute a digest. | **REJECT categorical inference.** It disproves relying on a **caller-supplied graph and self-hash**; it does not disprove code execution in a service-owned process to which a data-only external client has no Python/import/memory access. The actual service principal/caller boundary must, however, be declared and tested; no deployed process is proven here. |
| Must F8's standalone result_hash change? | G01 asks to carry an owner identity into F8 result identity. | **NOT NECESSARY FOR MINIMUM SAFE SELECTED ROUTE.** Keep F8 numeric contract intact; a selected-service receipt must bind original C1 evidence/preimage and composed identity to the F8 result/G2, and the ingress must refuse caller evidence. Numeric hashes can stay equal for identical geometry while origin claim/refusal differs. |
| Does G2 authenticate evidence source? | Original binder authenticates applicability/source scope only. | **NO.** Branch-observed binder blob 848d2d0eedb04b792747e9d6aaa49bb39d108a2c re-derives scope and passes evidence unchanged; it must be supplied owner-produced evidence at a higher-level ingress. |
| Is strong same-process threat protection proven? | G01 assumes malicious caller can mutate entire Python trust boundary. | **NO.** If same-process arbitrary code execution is required protection, ordinary in-process owner-only API is insufficient; independently administered runtime/principal is mandatory. Present evidence does not establish that EE14 promises protection from such arbitrary code. |
| Does this review demonstrate an actual trusted ingress/T1? | G01 wrote no ingress and no q1/q2 positive court. | **NO.** This review is documentary, not a fix. The narrow owner-only service implementation, actual privilege boundary and independent final-sha hostile acceptance remain missing; G0b permission unissued. |

## B. HQ's decisive choice

**Recommended Fork A — authorize a bounded engineering commission ONLY AFTER fixing service caller privilege.**

Explicitly declare the bounded G1 attacker as a data-only external service client or other request principal **separate from** the owner-controlled service execution context; ensure no arbitrary Python/plug-in/eval/pickle-like arbitrary-object execution or user-writable authority registry/fixture on that ingress. No need to pre-install an additional AT07 cryptographic issuer merely for this caller model. This is *not* a claim to resist the service operator or compromised process.

Commission **one owner-executed C1→G2/F8 positive seam**, reusing accepted C1, service source applicability and G2, with:

1. Actual C1 executed on privately registered source-free fixture/producer/authority inputs for q(C|A=1) and q(C|A=1,B=0); no evidence/composition hash, registry, witness, rule or permission object accepted from external callers.
2. Original C1 composition identity plus evidence canonical preimage, fact/witness/authority/provenance/replay verified against owner-held upstream objects; exact C1-generated evidence passed directly to evaluate_bound_positioned_subject_possibility, with no object substitution.
3. Owner selected-service receipt binds C1 full identity, evidence preimage identity, actual G2 authenticated applicability/request/rule, F8 result, and independently owner-issued model use/B5 selected current/as-of only when each exists. A hash or caller-produced AuthorityRef alone conveys **zero** trust.
4. Independent clean final-SHA positive/hostile court H1–H7/N1 from 02_POSITIVE_HONEST_HOSTILE_COURT.md, including the positive q1/q2 same-respondent joint, forged provenance with identical F8 hash, recomputed caller preimages, direct F8 bypass, and owner global-mutation threat distinction. Do not rewrite accepted F8 core just to force numeric provenance claims.

**Smallest positive engineering write surface (proposed, not granted):** one owner-controlled entrypoint in the existing EE14 selected-service integration surface and one focused source-free integration test; avoid new general-purpose provenance framework, no production changes in this review. HQ/implementer should inspect exact selected caller/deployment entrypoint and fix a bounded module/test path and baseline before issuing a code commission. Any internal fixture runner may be used to demonstrate positive owner custody at T0 but does **not** alone certify the live externally isolated service contract.

**Mandatory residual HOLD even if Fork A engineering PASS:** independent G0b EE14 model/use grant, G3 independent final-SHA acceptance + selected service current/as-of join, actual selected T1 issuer/consumer/replay grade, and any other route-specific permissions. Source-free fixture is not an empirical respondent-backed or objective-world claim.

**Fork B — if HQ requires hostile arbitrary Python in the owner's own process:** hold G1; require a named independently controlled executable/service principal, immutable or independently governed code/authority registry and authenticated cross-process ingress/verification. Do not pretend an in-process token, private-looking Python name, dataclass, hash, or self-signed receipt can solve this. The precise external requirement is **hostile caller cannot execute or mutate C1/service authority/verifier state**, with independently managed service execution trust and a verifier whose expected source is not caller-supplied. This may be met by a separate service process/account with controlled deployment and RPC, not necessarily a new semantic issuer. The currently inspected library-only path has no demonstrated protection from a hostile same-process principal.

**Fork C — if HQ will not declare or provision either trustworthy caller model:** maintain specific hold `G1_PRODUCER_ORIGIN_AUTHENTICATION_UNPROVED__SELECTED_T1_DENIED`. Do not fall back to the G01 false-positive hash, and do not imply the whole architecture is impossible; the obstruction is the unbound principal/ingress.

## C. One short, executable next commission for HQ (prospective only)

**Title:** HQ262 G1 — owner-only C1 producer-to-authenticated F8 ingress and independently replayed XOR hostile court — R1.  
**Owner:** EE14 service integration implementer; reviewer MUST be independent of implementation and of G01.  
**Inputs:** C1 owner blob 604c8d591d4cc2b646e9b149cdb233fc9d69cf6b, F8 blob 62e5eced47b64512f47b004e3e13a6ef3fe21de7, actual G2 binder blob 848d2d0eedb04b792747e9d6aaa49bb39d108a2c, applicability owner blob 3e40caca29e8c96ee1f412f919cfc7dba63f96c4, HQ253 source-free XOR fixture/oracle, G01 diagnostic regression, HQ261 T01 return files. Freeze fresh actual control code SHAs and caller boundary at issuance.  
**Do:** implement exclusively registered owner-input source-free q1/q2 selected entrypoint; authenticate C1 evidence preimage/owner lineage and source scope; emit owner-issued *technical origin* receipt without granting model-use. Preserve C1 numerical and F8 APIs. Independently test positive + malicious caller evidence and direct bypass + same-process adversary limitation at committed SHA, with exact interpreter/tests/exits.  
**Stop:** No G0b model-use issuance, real-world empirical service, FF02, EE12, F7/AT07 install or V3. Any missing runtime/caller access boundary -> document explicit HOLD rather than report green security.  
**Pass for HQ review:** specific external data-only caller boundary defended by owner-produced C1 evidence, honest q1/q2 integration, refused forged selected-service origin, no caller-hash trust and independent clean committed test receipt. **No self-adoption.**

## D. Provenance and limitations

Observed live HQ261 control @ 1ff7c74f6bef580ba3ce0738b7a9ac6b560ca2d7, sealed checkpoint CURRENT.json for 20261009-PYAT-HQ261-G1-TRUST-G3-LOCAL-LITS-P1-GHANA-R1, commissioned review tip d8e01876423f55a844773a13fdc008a2c78e953e. Reviewed exact G01 return @ 6ea8fd5cc963e0217d42027e8c190d41e6fa1b11, C1/F8/applicability/binder implementation at commissioned branch, HQ250 S01 owner/API map and HQ251 R01 oracle, HQ255 N01 proposed model-use clause, HQ261 decision. All citations are repository artifacts, not asserted externally administered runtime facts. The review used **GitHub documentary read/write only**, no source/retained files, machine/worktree, interpreter, local test, new protected key or signer.

**Final:** HQ261_T01_RETURNED__NO_SELF_ADOPTION.
