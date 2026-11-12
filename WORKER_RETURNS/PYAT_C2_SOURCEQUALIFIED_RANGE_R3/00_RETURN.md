# PYAT C-2 — Agent B R3 source-qualified range construction and adversarial receiving

**Disposition:** `REVISE / MODEL-LEVEL CORRECTION EXECUTED / NATIVE C-2 HOLD`.

**Original commission:** [#919](https://github.com/maidiu/rawlsing/issues/919) under [#909](https://github.com/maidiu/rawlsing/issues/909). **Opposing exact construction:** [PR #927](https://github.com/maidiu/rawlsing/pull/927) @ `06ecd2e290c967743c6be70b66389be078130bc1`. **Protected source read baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Isolated correction:** [draft PR #930](https://github.com/maidiu/rawlsing/pull/930), branch `review/pyat-c2-sourcequalified-range-r3-20261112`, stacked directly on the exact #927 head. No protected source, PR #910, original35, W03/W04 paused branch, or active science worker modified. Exclusive Mac writer lease NOT VERIFIED; collision prevented by unique new review branch and immutable starting SHA, not represented as headquarters appointment.

## 1. What Agent A R2 won

Preserve, don't replace: the R2 reference construction genuinely implements disk-backed SQLite event/selector postings, a unique occurrence index, SHA-256 leaf/node commitments, finite Merkle paths for each selected member, authenticated immediate lower/upper boundaries for nonempty/empty selectors, native/canonical/component alias union with repeated events and exact ref ordering, domain-root binding, and sourcefree hostile tests. It concedes that local index roots are not external I02 issuance, complete source-to-index correspondence, or source/host/science authority.

Its critique of our R1 entire-root-on-every-selection model was valid. The original #919 commission is **read-only/sourcefree investigation**, so lack of a protected production implementation is not an independently established contractual violation. The #925 FF01 return in the pasted relay is another commission and is NOT changed or received here.

## 2. Deeper defect: semantic range membership is not source-universe question qualification

Actual native `rawlsing_next/pre553_c11_ingest.py` (blob `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`, lines 623–642) builds the set of `(exact universe_ref, exact native_question_ref)` pairs from `QuestionVariableBinding` and requires every `RespondentEvent` to resolve to one. `_pre553_query_predicate._select_respondent_events` (blob `1b82b6df993bf14afa5e78782d988cba6e76b668`, lines 18–56) selects events by native/canonical/component and optional state under the already qualified release. I03 applies separately governed routing and query semantics.

At #927, R2 `Scope.targets` was a global tuple of names: e.g., `("NQ7","CQ7","SUB7","ALIAS","ABSENT")`. R2's `test_missing_empty_range_is_authenticated_not_scope_inference` treated an empty `ABSENT` range as valid without creating an admitted exact native question binding in U1. Moreover, `CQ7` was globally known and could be requested against U2 even if the source's canonical alias grant was U1-only. The cryptographic proof correctly attested **there are no postings under this key in the accepted index**, but the R2 wrapper had not attested **this question is legitimately in the declared source-universe question domain**. A false permitted-empty query and a genuine no-event question were indistinguishable.

This is not a break of the production I03 engine; it is a material defect in R2's proposed sourcefree certification ABI and tests. Reference integrity and index absence are not query-scope/meaning permission. The merged source-native requirement must derive this domain from independently I02-governed `QuestionVariableBinding` and real authority snapshots, not model strings.

## 3. Implemented correction inside existing R2 model

Changed **only** `WORKER_RETURNS/PYAT_C2_COUNTERCONSTRUCTION_R2/tests/test_verified_range.py` plus a branch-scoped sourcefree CI workflow, and this bounded receiving document. The original 19-test suite and entire disk-backed Merkle tree/SQLite proof mechanism are retained.

- Added `QuestionBinding(universe, native, topology_authority_ref, canonical, canonical_authority_ref, components)` fixture record; immutable `Scope.root()` now hashes all its exact-universe grants, respondent scope and legacy declared names.
- Builder rejects duplicate/ungoverned question binding, missing topology or canonical authority, any event outside admitted universe/respondent, unknown exact native question, or unqualified canonical/component alias **before publishing its selector root**.
- Saved `select()` requires `scope.allows_target(universe,target)` after verifying scope-root equality against the independently presented expected anchor. An allowed exact empty query must therefore have an admitted native source question even if there are zero respondent events.
- Discovered and repaired an *own correction regression*: treating the legacy global `Scope.targets` list as an additional hard permission gate would reject a legitimate U2-specific canonical alias (`CQ8`) when the global list happened to omit it. Global vocabulary remains hashed as legacy fixture metadata, but is no longer the source of truth for query permission. Exact per-universe binding is.
- Corrected U2 event canonical alias from `CQ7` to `CQ8` so actual fixture events agree with the separately qualified U2 binding; otherwise the new prepublication guard correctly rejected the test fixture itself.

This is a controlled upgrade of the adversary's actual code, not merely a new adversarial document or another independent toy model.

## 4. Actual executed negative/positive court

[GitHub Actions run #43167809531](https://github.com/maidiu/rawlsing/actions/runs/43167809531) — event `pull_request`, head `ff2ea980e708e5082e49d978f0f2e55e0984691b`, **success**, job `sourcefree-court`, Python `unittest` **25/25 PASS**, ~0.440 s, zero failures/skips. Full inherited 19 R2 tests passed plus 6 adversarial tests:

| New test | Discriminating positive / negative |
|---|---|
| `test_global_target_is_not_exact_universe_question_binding` | U1 canonical `CQ7` cannot be borrowed in U2; legitimate U2 native `NQ7` and separate U2 canonical `CQ8` still work even if global legacy names omit `CQ8` |
| `test_global_whitelist_cannot_convert_unissued_question_into_valid_empty` | Newly globally admitted `GHOST` with no exact U1 question binding refuses, despite a well-formed locally rooted empty range |
| `test_fabricated_canonical_alias_fails_before_root_publication` | Event-substituted unauthorized `FAKE_CANONICAL` alias refuses at qualified builder |
| `test_out_of_domain_event_fails_before_accepted_selector_root` | Unrecognized U9/R8 event refuses before index seal |
| `test_legitimate_no_event_question_has_positive_binding_but_no_postings` | Real fixture U1 `ABSENT` has explicit question binding and empty postings; unissued U2 `ABSENT` refuses |
| `test_mapping_authority_removed_with_same_events_invalidates_store` | Missing canonical mapping authority blocks construction, and changing the scope grant invalidates the accepted root |

Git blob of executed test file: `fd65a6fe0ddf8c6096a6f14add8022358f0a1d0c`. The action checked out the PR HEAD and `git hash-object` logged that same blob. Branch-scoped runner: `.github/workflows/pyat-c2-sourcequalified-range-r3-sourcefree.yml` (stdlib sourcefree only, no privileges or datasets). No new native tests claimed.

## 5. Challenges refuted or delimited

- **Claim that R2's Merkle neighbor proofs are fake or fundamentally nonfunctional:** Not established. They survive all 19 inherited tests at R3. They are proof of **an accepted index's** range, not self-sufficient evidence of source-meaning rights.
- **Claim that original A failed #919 by not modifying native production:** Refuted by original commission's read-only/sourcefree boundary.
- **Claim that a single global question-name list suffices:** Refuted by the U1/U2 canonical mapping split and legitimate U2 `CQ8` positive. Exact source-question binding must precede *both positive and empty* indexed selections.
- **Claim that arbitrary new QueryBinding strings supply real science authority:** Refuted. Strings here are declared sourcefree fixture grants; only separately verified native I02 `QuestionVariableBinding` and competent authority snapshots could support actual acceptance.

## 6. Open shared failures and new attack surfaces

1. Neither R1, R2 nor this R3 **has implemented the real I02 physical source-to-selector multiset bijection** against an independently issued source snapshot, exact source event occurrences and all M01–M18/replay/source families. A well-formed fixture root proves only fixture consistency.
2. R3 `QuestionBinding` is modeled with text IDs, not real typed `ExactRef`/`AuthorityRef`, `AuthorityRegistry`, certified cross-universe comparator or physical source. Its positive and empty claims stay SOURCEFREE MODEL ONLY.
3. The R2 lower-level `range()` generator still yields a posting before its final boundary checks. The public `select()` buffers until all checks finish, but direct generator exposure would be unsafe. A native bounded reader needs a proof-first immutable snapshot/verified cursor protocol without O(K) unbounded live output.
4. Real `_ReleaseIndex`, `_select_respondent_events`, direct I03, I05, Batch and joined-resume first consumers are not integrated with any disk-backed certified adapter. Actual exact full answer/fact/replay parity, revocation and restore remain HOLD.
5. Current issuer revalidation and source/host/purpose/cold B5 publication are external qualified obligations, not an internally self-hashed anchor. Host/process-tree 100k 6 GiB performance, recovery and original35 source-native P05 equivalence were not executed.
6. R3's legacy global `targets` metadata should eventually be retired from the native admission ABI; retaining it solely for fixture backward-compatibility is not a new source proof.

## 7. Immutable provenance and receiving boundary

- Opponent HEAD `06ecd2e290c967743c6be70b66389be078130bc1`; protected source observed `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Tested R3 HEAD `ff2ea980e708e5082e49d978f0f2e55e0984691b`, test blob `fd65a6fe0ddf8c6096a6f14add8022358f0a1d0c`; CI #43167809531 PASS.
- This document is added after successful suite; **final branch HEAD must be read back**. The semantic sourcefile and test blob are unchanged by this report-only commit.
- No production merge, native source, W03/W04 HQ restart, issuer grant, Mac worker lease, S2/S3 native proof, or scientific adjudication.
- Disposition: **S1 strengthened at exact sourcefree model grade; C-2 original commission and PR #910 engineering acceptance still HOLD.** One independent receiving should verify the physical source/question authority boundary; no new review fleet or registry is required.

## 8. Strongest challenge back to Agent A

Supply a single I02-owner algorithm that independently derives the *full* `(exact universe, native question, topology/canonical alias grant, respondent membership, physical occurrence)` domain from authoritative source and `QuestionVariableBinding`, checks every derived semantic posting in both directions, and commits the **complete** question/routing/domain/ref/replay roots under one accepted release **without duplicating the full object corpus**.

Then show that the existing native first consumer can distinguish (a) an admitted source-universe question with zero events, (b) a question absent from the source's native instrument in that universe, and (c) known question with held/unknown routing. Prove positive, false-absence/severance and restoration through I03 and at least Batch. A better Merkle index alone cannot accomplish this.

**Conclude at sourcefree model level. Do not promote any of the above to S2/native I02 acceptance.**
