# PYAT HQ280 — C02H / A03I / D02Z three-return science and security adjudication R1

**State:** THREE_RETURNS_REMOTE_CUSTODIED__B01E_AND_A04TU_STILL_DISPATCHED_NOT_YET_RETURNED__NO_CANONICAL_OR_OPERATIVE_ADOPTION.
**Governing:** HQD-2026-10-10-280; canonical `integration/pre-main-reconciliation-r1 @ a70a069fa948e0f3c041b389edcc732b6b948a4f`, semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` unchanged by this report.

## Remote SHA and ancestry

- **A03I** `agent/rabochii-pyat-hq280-pv3-a03i-metadata-custodian-decision-r1 @ ff059f0a3eb560026e070097d856aaa09d4eab15`, exactly one ahead and zero behind sealed `b5064dc424e35c35ded43af2f0c03ddb3518c0e0`; six new return/report files including manifest, no owner edits.
- **D02Z** `agent/rabochii-pyat-hq280-pv3-d02z-legal-source-native-contract-r1 @ 8fbcc84f3ec7664ef2ea565c6813d6e2c1723761`, exactly one ahead and zero behind sealed `36314fca8ae98c1ddc9311bf194762e151ce5b10`; nine new report/repro files, *all* in WORKER_RETURNS, including standalone Python candidate/unittest, zero accepted owner edits.
- **C02H** actual alternate `agent/c02h-separated-principal-0e01de5 @ 82309fe17c70324217382d0550ce1cc591e39eae`, exactly one ahead and zero behind sealed `0e01de5fe1cd50d48fcb11eb378a14559c586b75`; 12 new return/repro and source-free candidate files, zero accepted B5/M2 owner edits. Assigned longer branch `agent/rabochii-pyat-hq280-pv3-c02h-separated-producer-principal-r1` was still at startup during readback. Actual C02H return report internally names the commissioning lineage; custody must refer to actual shorter GitHub branch.

**Other two still running/out:** `B01E` assigned `agent/rabochii-pyat-hq280-pv3-b01e-batch-durable-integration-r1` sealed `2fb5e8cc9971fe05899bbbeff837cd6cd049a969`, and `A04TU` assigned `agent/rabochii-pyat-hq280-pv3-a04tu-test-scope-mutation-hostiles-r1` sealed `ff859444355724658bf6b8b00a3ae3354abe0c9f`; both assigned GitHub branches were still exactly at startup at check. User reports they are active on secondary Mac; absence of push is NOT proof of inactivity/failure. Do not relaunch or disturb their worktrees.

## A03I — authority decision, no new respondent read

Actual HQ262 §B metadata-only charter explicitly foregrounded Ghana Q43 and generic column names/labels, **not specifically Q86A**. HQ271 M01 completed an actual retained Afro R5 metadata-only source witness (SHA `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`) including Q86A dictionary; HQ272 credited physical evidence but did NOT retrospectively confirm widened permission. A03I's exact `02_READY_FOR_COMPETENT_Q86A_RATIFY_OR_HOLD_DECISION.md` distinguishes:
1. qualified HQ262 successor + actual source custodian may RATIFY historical metadata-only read based on documented contemporaneous general-column dictionary scope, **if competence/charter warrants**; or
2. historical ratification HELD/REFUSED, with separately issued *prospective* narrow Q86A metadata-only permission if needed.
A later decision cannot rewrite historical legality without actual grounds. This HQ report grants neither option. Exact source-reader location and respondent risks beyond metadata remain unqualified; `PERMITTED_ISSUED=[]`, `issued_E=[]`, `B02_runnable=0`. No new row or SAV inspection. First one-job Ghana Q86A RAW unary still needs actual GHA individual routing/asked risk, C11 original-source row read, I03 predicate/target-use signature, pre-run external expected E, and real source-local consumer.

**Grade:** `Q86A_DOCUMENTARY_AND_PRIOR_PHYSICAL_METADATA_EVIDENCE_CREDITED__COMPETENT_RETROSPECTIVE_SCOPE_RATIFICATION_UNISSUED__NO_B02`. Do not repeat archaeology.

## D02Z — genuine native data-only legal-rule *development* contract, not operative producer

First bounded source-free candidate in `WORKER_RETURNS/PYAT-HQ280-PV3-D02Z-NATIVE-LEGAL-RULE-PRODUCER-CONTRACT-R1/repro/pre553_documentary_rule_source_contract_candidate.py`, plus unittest with 35 proposed sourcefree positive/negative/held fixture cases. **Browser worker explicitly did not run Python**; 35 is number of **authored fixtures**, not 35 PASS. Candidate maintains proposed `RULE_TEXT_DOCUMENTED` as text-as-enacted statutory clause, no actual original PDF-byte digest, no competent issuer reference, no N5/N6/N9 adopted output. Ghana Act 591 §7 government BRR/GIS documentary text with Constitution Art6(2) still historical source-positive, not certified Gazette, statutory commencement, amendments/asof, current legal force, person citizenship, service access or causal effect. Local JSON input hash is not source PDF custody. No accepted existing native legal-source producer proved; new native one and scientific/legal source issuer decision required.

**Grade:** `DOCUMENTARY_TEXT_ORIGINAL_WARRANT_POSITIVE__SOURCEFREE_SCHEMA_FIXTURES_AUTHORED_NOT_EXECUTED__NO_NATIVE_PRODUCER_ISSUANCE`. Next smallest independent act: run supplied 35 unit tests in bounded Python and attack issuance/byte custody/version escalation; retain documentary source authenticity holds.

## C02H — substantial technical security caveats found by HQ source inspection

Worker claims `SEPARATE_PRINCIPAL_DEMO__OWNER_ISSUER_HELD__NONOPERATIVE` and returns a 13-log-entry court, including phase markers, unpatched actual B5 forgery, and demo credential refusals. A design/interface demonstrating *checks* is credited narrowly. **However, this does not demonstrate an adversarially enforced separate-principal trust boundary:**

1. `rawlsing_next/pre553_b5_separate_principal_verifier_candidate.py` creates deterministic fixed RSA key `p=61,q=53,n=3233,e=17` in `_rsa_keypair` (lines 72–80), so the signing key is trivially derivable by any caller who can read this code; `IssuerProcess`, `VerifierProcess`, `AttackerProcess` are Python classes in the same Python process, NOT separately isolated OS processes. Claims `caller cannot forge` and `ephemeral RSA private key` under genuine hostile assumptions are **NOT PROVEN**.
2. Module documentation and `DEMO_GRADE` falsely refer to `EPHEMERAL_HMAC` (lines 24–27/47), but implementation is deterministic toy RSA. Return report claims ephemeral RSA, yet private primes are fixed. This discrepancy must be corrected, not treated as production or even strong demo cryptographic proof.
3. `AttackerProcess.swap_root` and `self_register_issuer` at lines 249–257 simply `return False` rather than making an actual adversarial operation against `VerifierProcess._trusted_root` / `issuer_id` (which are ordinary mutable Python fields). These cannot demonstrate root isolation or issuer registry protection. Do not label them executed negative penetration tests.
4. `VerifierProcess.verify(..., expectation=...)` checks only `expectation.get("derived_from") == "subject_construction"` (lines 219–222). `SP_C2_tautology` supplies that explicit marker, rather than proving an unmarked output-derived expectation is rejected by independent pre-run issuer custody. A caller can omit/rewrite the marker absent an external commitment. A separate external issuer is still missing.
5. Court `repro/logs/separate_principal_court.json` has **13 entries including COURT_START/COMPLETE/PHASE/DISPOSITION**, NOT 13 distinct adversarial tests. Positive signature check with toy RSA and several refusal checks are meaningful code-shape tests, but only two unpatched cases actually invoke raw B5 owner; later `SP_` cases call new candidate `verifier.verify()`, not end-to-end adopted M2/B5 owner mediation.
6. Accepted B5/M2 lifecycle and checkpoint owners are not modified, `OWNER_ISSUER_HOLD` remains, no real production root, actual owner-level mandatory enforcement unproved, no CURRENT/G0b/G1/V3.

**Security disposition:** `C02H_DELIVERED_AND_DESIGN_CANDIDATE__SEPARATE_PRINCIPAL_SECURITY_PROOF_REFUSED__FIXED_TOY_KEY_AND_INERT_ATTACK_STUBS__OWNER_ISSUER_HOLD`. Future focused independent hostile must try recovering private key, direct mutable root substitution, expected provenance marker removal, attacker-issued credential accepted, then report exact owner API seam. Do not self-adopt and do not require an actual production issuer for a valid bounded cryptographic test demo, but demo must be honest and safe for its declared threat model.

## Next non-interfering actions

Let B01E and A04TU finish on secondary Mac. D02Z can undergo bounded Python evaluation on an available independent runner. C02H requires independent adversarial challenge and correction rather than acceptance of the reported separate-principal security claims; its positive architectural direction may be retained. A03I asks competent owner/custodian decision with yes/no textual charter grounds; HQ cannot silently ratify it.

**Terminal:** `HQ280_THREE_NONMAC_RETURNS_BANKED__B01E_A04TU_RUNNING__C02H_CRITICAL_DEMO_GAP__A03I_AUTHORITY_HOLD__D02Z_TESTS_UNEXECUTED`.
