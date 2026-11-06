# SOROK P3-S1 — independent input review

**Subject:** `5a505a911509073eb38102f0022f445e7ec602e5` / PR734
**Protected base:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`
**Review branch:** `review/sorok-p3-s1-input-20261106-r1`
**Scope:** bounded source/construct-validity review of four S1 files; no S2 implementation, native science, sourcepack/runtime/PROGRAMMA edit or merge.

## Verdict

**`ACCEPT_SCOPED_TEST_ONLY_DESIGN_INPUT__H1_H2_H3_COVERED__SAFE_CONTRACTS_REQUIRED_FOR_A-E__NATIVE_HOLD`**

The four-file S1 return is sufficient as **explicitly test-only design capital** for the current P3 A–E implementation. H1, H2 and H3 are present, materially distinct, and correctly refuse fabricated witnesses, global multipliers, automatic lifecycle mutation, canonical memory/claim issuance and native psychological issuance. The return does **not** constitute implementation, measured resource acceptance, source-verified empirical psychology or a protected receiving decision.

No blocking **semantic** contradiction was found in H1/H2/H3 at design grade. Four promotion blocks remain finite and explicit below.

## What the four files actually cover

- `00_RETURN.md`: H1/H2/H3 synthesis; inherited architecture and gate boundaries; research grades; H1/H2/H3 summary; GO/HOLD handoff.
- `01_MECHANISM_CONTRACTS_AND_BUDGETS.md`: five evidence forms, proposed noncanonical compression envelope, H1/H2/H3 contracts, opacity, budget envelopes, stopping rule.
- `02_CASES_TESTS_AND_HUMAN_EVALUATION.md`: six adversarial life cases, proposed N01–N16 negative matrix and qualitative human-verisimilitude design. No execution claim.
- `03_HANDOFF_AND_SOURCE_REGISTER.json`: source register, mechanism/case/negative IDs, configuration scope, public references and authority holds.

The original launch was truncated after “A high”; the return transparently records this and does not claim that unprovided later instructions or outputs existed. The four-file consolidation covers the stated substantive design categories, not S2 execution.

## H1 — compressed participation

**Accepted design points**

- Distinguishes objective occurrence, actual actor participation, actor state, memory, knowledge and rendered observation.
- Uses `REPRESENTATIVE_EPISODE` / `ACCUMULATED_INTERVAL` / `RETROSPECTIVE_CRYSTALLIZATION` as analytical evidence forms, not new event kinds.
- Rejects invented witness counts, hidden thousand-event simulation, global salience multipliers and other-actor achievement imported into A.
- Keeps material opportunity, actual participation and possible practice formation separate.
- Leaves `MISSING_RULE` / unevaluable distinct from evaluated `NO_CHANGE`.

**Blocking for Workstream C implementation**

The proposed `CompressionEvidenceEnvelope@TEST_ONLY/1` is a documentation shape, not a safe runtime contract. `event_id`, `episode_ref`, `coverage_basis`, source readsets, content hashing and validation are placeholders. It must not be implemented directly. Required safe contract:

```text
immutable envelope_id = SHA256(canonical envelope without id)
existing event_id + event_hash
actor_id + root + branch + exact clock/window
representation_form
represented_window.from/to + coverage basis
source refs with immutable source identity/hash and observed/unobserved scope
actual actor_participation refs
distinct other_actor contribution refs
material/relation refs
content hash and integrity state
```

It remains a read-only external evidence envelope: no new `EventProposal` circumstances, no P2 proposal fields, no actor-state writer, no invented act receipts, no multiplier. The actual P2 event ledger remains authoritative.

## H2 — contextual activation and contradiction

**Accepted design points**

- Read-time activation/inhibition is explicitly **not** CAN-011 `REACTIVATE`/`DORMANT` lifecycle mutation.
- Multiple contradictory mediators, tensions, practices, expectations, strivings and relations may coexist.
- No scalar winner, personality type, demographic selector, forced reconciliation or equivalent global trait.
- Context includes opportunity, authority, sanction, relation, access and interlocutor; transfer remains unknown until demonstrated.
- If Rule A / target-transition issuance is absent, the result is a diagnostic counterfactual proposal, not an authorized response or mutation.

**Blocking for Workstream D implementation**

There is no exact read-time activation adapter or output schema. The implementation owner must supply an exact pure-read contract with source record IDs/hashes, actor/root/branch/clock, context/access inputs, and finite `ELIGIBLE` / `INHIBITED` / `UNKNOWN` / `CONTRADICTION` outcomes. It must not write activation flags, lifecycle fields or a scalar winner. The prose contract is sufficient design input but not an ABI.

## H3 — retrospective recontextualization and asymmetric access

**Accepted design points**

- Objective history remains immutable.
- Actor perception/memory and user-visible expression are distinct from objective history and from analyst causal explanation.
- `UNAVAILABLE` memory is never rehydrated from analyst history.
- LLM retrospective impressions remain proposals; “I remember” prose cannot create ADP-016 memory or ADP-017 claim permission.
- `MISSING_RULE` / deferred memory basis remains distinct from evaluated no-change.
- Two users can see compatible different surfaces without forking actor history.

**Blocking for Workstream E implementation**

There is no exact read-only actor-memory / claim / renderer adapter. The implementation must use issued ADP-016/017 semantics or remain held; the S1 prose cannot be treated as an ADP-016 formation rule or ADP-017 claim permission. Any renderer output must use an exact actor-accessible envelope and must not expose analyst-only causes.

## Source and construct consistency

**Verified here**

- Canonical sourcepack `03_RUNTIME_FIRST_CONSUMER_AND_SUPERSESSION.md` and `04_PRELIMINARY_SCIENCE_DECISION_COURT.md` support the stated CAN-011 three-kind model, valid-empty/contradiction, ADP-016 event-referential/causal-trace memory and ADP-017 knowledge/belief/uncertainty/nonknowledge separation.
- `06_P3_START_AND_READINESS_CONTRACT.md` supports the stated native holds, `MISSING_RULE` versus evaluated `NO_CHANGE` distinction, wrong-root/source/cold requirements and no-native-writer boundary.
- Current runtime blobs match S1's source register: `p2_owner.py` `3160eb1…`, `contracts.py` `c4ce557…`, `ABI.md` `f6e12a9…` at protected `c852…`.
- S1 correctly records that P2Owner accepts only its constrained proposal fields and does not accept a compression field.

**Not independently verified**

- The scholarly book propositions and exact page locators were not re-read by this review. S1 itself reports targeted primary readings; the source register supplies no immutable PDF paths/hashes or claim-level page artifacts. These remain author-reported source readings, not independent empirical evidence.
- Some page ranges differ across S1 and sourcepack 12: Dreier `181–189` versus `182–191`; Lahire PDF `71–81` versus around `69–86`; Sève `193–202` versus `193–205`. No semantic inversion was found, but exact locators require reconciliation before any source-warrant promotion.
- `sourcepack/00_READ_FIRST.md` records a preconstruction protected baseline `62f189…`, while this subject is at `c852…`; current code hashes match `c852`. Treat the header as stale documentation until the sourcepack owner reconciles it.

## Finite promotion blocks

1. **H1 envelope is not a safe runtime ABI.** Do not implement the placeholder JSON or add it to P2 proposal grammar. Implement only the immutable external contract above with exact hash/identity validation.
2. **H2/H3 have no exact read-only adapter contracts.** Workstream D/E need owner-defined pure-read activation and actor-safe memory/claim/render interfaces; S1 prose is design input, not ABI.
3. **No actual A–E implementation, two-batch P3 vertical slice, measured resource receipts or P3 A–H counterfactual execution exists in S1.** Those remain engineering work, not S1 acceptance.
4. **No independent verification of scholarly books or exact source page artifacts.** S1 may be used as constructive design capital, not as native scientific source warrant.

## Nonblocking limitations

- N01–N16 and the human-verisimilitude design are proposed tests, not executed tests.
- Budgets are envelopes and instrumentation plans; no measured token, byte, database-read, latency or cold-reopen result is claimed.
- The original pasted launch was truncated; no claim is made that every post-“A high” requested output existed.
- The sourcepack is a source/currentness package, not an original CAN/ADP issuer.
- No actual P2 compression column, ADP-016 memory writer, ADP-017 claim permission or native CAN-008/CAN-011 rule is issued.

## Safe acceptance scope

**Accepted as TEST_ONLY design input:**

- H1 compressed participation logic, with external evidence-envelope guardrails and no fabricated acts/multiplier.
- H2 conditional read-time activation and coexistence of contradictions, with no automatic lifecycle or scalar winner.
- H3 asymmetric access and retrospective reinterpretation, with objective history immutable and memory/claim issuance held.
- The six cases and N01–N16 as proposed validation design, not executed evidence.

**Not accepted:**

- Any native CAN/ADP law or source-verified empirical claim.
- Any H1 sidecar as runtime schema without owner-issued exact ABI.
- Any H2 activation implementation without an exact read-only contract.
- Any H3 memory/claim output without ADP-016/017 issuance.
- Any P3 A–E implementation, measured economy, human validation or protected receiving.
- Any new P2 proposal field, universal completeness gate, research fleet or new psychological theory.

## Evidence

- `01_SOURCE_CLAIM_MAP.json` — exact S1/sourcepack hashes, source claims and verification grades.
- `02_VERDICT.json` — machine-readable verdict, promotion blocks and acceptance scope.
- `03_SAFE_CONTRACTS.md` — guardrails for H1/H2/H3 implementation.
- `PASSPORT.json` — sanitized runtime metadata.
- `MANIFEST.json` — file hashes and provenance.
