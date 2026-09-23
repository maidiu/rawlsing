# FIABC LiTS PRE-ORACLE CLOSURE INDEPENDENT AUDIT — R1

## Disposition

**PASS as an audit / HOLD as a pre-oracle promotion state.**

The two commissioned closure obligations are real at baseline `4513eae0ec2c55c3252871c77cd52fc3dd0f07cd`:

1. **I03 successor jurisdiction is incomplete.** The successor authority record carries `runtime_catalog_identity` and `parent_operation`, but the generic successor resolver does not consume either field as an executable jurisdictional predicate.
2. **Current LiTS ↔ ASTRA substantive conservation is incomplete.** The current LiTS oracle producer admits the current neutral result using 50 candidates, 77 roles, 49 supported / 1 valid-empty, and well-formed current identities, while accepted ASTRA-D04-R2 contains materially richer empirical truth. Cardinality and terminal-state agreement are not substantive parity.

No raw survey file was opened or materialized. No source-backed LiTS was run. No Candidate A/B/C, real I05, measured P2X, or P3 was run. No production code was changed.

## Baseline

- repository: `maidiu/rawlsing`
- audited branch: `agent/rabochii-premain-fiabc-lits-representation-authority-repair-r1`
- exact audited head: `4513eae0ec2c55c3252871c77cd52fc3dd0f07cd`
- audit branch: `agent/rabochii-premain-fiabc-lits-preoracle-independent-audit-r1`
- accepted ASTRA evidence read from: `agent/rabochii-prev3-astra-d04r2-learned-workload-execution-r2`
- immutable ASTRA product identity: `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`
- immutable ASTRA semantic replay identity: `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`
- LiTS source SHA: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

## Direct answers to the 15 adversarial questions

1. **Can 50/77 and 49/1 with altered empirical values currently freeze? — YES.** `_bind_current_lits_execution_to_astra()` checks exact cardinalities and terminal counts, but not ASTRA's P0–P4 empirical values. `_validate_terminal_identity()` later validates the current identities syntactically and repeats the same coverage checks. A current result can therefore retain 50/77 and 49/1 while its empirical witnesses drift and still reach oracle freeze if the other structural gates pass.

2. **Can a successor declared for one runtime catalog currently be consumed under another? — YES, conditional on the other currently matched dimensions remaining valid.** `I03OperationSuccessorContract.runtime_catalog_identity` is parsed and hash-bound into the authority record, but `authorize_i03_operation_successor()` receives no runtime-catalog argument and never compares the field.

3. **Can a successor whose declared parent operation is not authorized by the supplied historical snapshot currently pass? — YES, if the successor record is itself lawfully adopted/rehashed and its currently checked dimensions match.** `parent_operation` is parsed but never compared to `snapshot.governed_operations`. A casual in-place mutation is already caught by authority-content-hash/adoption law; that is not equivalent to executable parent-operation jurisdiction.

4. **Is the catalog-binding repair generic or LiTS-specific? — GENERIC.** The defect sits in generic PRE553 I03 successor resolution/execution. LiTS is the first concrete consumer that exposes it.

5. **What exact object should carry catalog identity at execution time? — The exact `RuntimeObjectCatalog` bound to the `CarrierNeutralResearchExecutor`.** Its `receipt()["catalog_identity"]` is already the canonical identity of the authorities + predicates + queries + discovery authorities actually used. That identity should be passed explicitly through the I03 execution seam to successor authorization; an ambient/global authority set or an `AuthorityRegistry` alone is insufficient.

6. **Does the current result retain enough empirical preimages for ASTRA normalization without another source decode? — YES, at the live neutral-I05 result boundary.** `ExactBoundedDiscoveryResult.empirical_facts` retains full `EmpiricalFact` preimages and receipts retain candidate/query-role→fact closure. The reduced `learned_empirical_execution_receipt()` and current oracle manifests do not retain enough by themselves. Parity must therefore be computed before those preimages are discarded.

7. **Can parity be established from current execution receipts alone? — NO.** The execution receipt carries refs/counts/replay identity, not the exact constituent cell counts, denominators, fractions, and witnesses. Consume the constituent `EmpiricalFact` preimages plus candidate identity / role mapping.

8. **Empirical truth vs provenance/identity metadata.** Empirical truth includes the R2/R7/R27 risk-set membership/count premise, P0 supports/denominators, P1 joint-dependence witness, P2 conditioned first-difference witnesses, P3 pooled/stratum fractions and signs, P4 keyed cell supports, and the typed terminal outcomes these facts entail. Provenance/identity metadata includes source SHA/shape, decoder/runtime/authority commits and blobs, runtime catalog/release refs, ASTRA product/replay object identities, receipt-ledger hashes, and workload/frontier identities. Some metadata is nevertheless mandatory to prove that the empirical comparison is about the same governed workload.

9. **Legitimately comparable old/new hashes.** Equality is lawful only inside the same semantic/hash domain: exact source SHA; exact same-schema candidate hashes; same-definition frontier seal; same-definition R2/R7/R27 risk-set roots; same-definition selector row/subset roots; exact same canonical authority/ref identities when the same authority object is required. Historical ASTRA product/replay hashes remain comparable to their own immutable accepted copies, not to differently shaped current objects.

10. **Structurally incomparable hashes.** Never equality-gate historical `ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0` object hash against `PRE553_LEARNED_EMPIRICAL_EXECUTION_RECEIPT@1.0.0`; historical ASTRA output-byte/product hash against the current neutral receipt/output identity; or historical ASTRA semantic replay hash against a current replay hash where the schemas/canonical material differ. Normalize substantive facts, then compare the normalized values.

11. **Could a P4 cell permutation evade a naïve summary? — YES.** “25/25 supported” and even a multiset of 25 positive supports lose cell identity. Parity must compare the keyed 5×5 cell→support mapping.

12. **Could P2 support survive while its first-difference witness drifts? — YES.** The validator only needs some distributional difference to remain supported. Exact conditioned denominator/support and the canonical first-difference witness must therefore be conserved.

13. **Could P3 remain valid-empty for the wrong empirical reason? — YES.** Valid-empty can result from materially different non-reversal facts. ASTRA's exact target cell, eight pooled/stratum fractions, pooled sign, and three stratum signs must be conserved, not merely the terminal label.

14. **Where must the parity gate sit? — After current neutral I05 has produced full retained `EmpiricalFact` preimages and before `build_lits_i_oracle()` / `freeze_oracle()`.** The natural seam is inside `_neutral_lits_material()`, replacing/strengthening the present count-only `_bind_current_lits_execution_to_astra()` path. A failed parity comparison must make oracle construction unreachable.

15. **Any additional independent pre-oracle obligation? — YES, one qualification-surface blocker is visible, but it is not a third semantic repair lane.** `rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py` still pins obsolete WVS Lock2 `8e5842...` and the pre-successor materializer blob, while current backend law and the accepted WVS successor oracle use Lock2 `5e2a53f0...` and successor DiscoveryAuthority `3aee3601...`. This stale regression must be reconciled before “full canonical source-free qualification” can truthfully be green. Do not fold that repair silently into A or B.

## Promotion holding

The user's rough order requires one repository-law correction: the current governed pre-candidate script requires execution on the existing P2X branch and itself produces the standard WVS oracle, fresh LiTS oracle, T3 freeze, and succession preflight. Therefore the **qualified code must be explicitly adopted/transitioned and the existing governed P2X branch fast-forwarded before the fresh local pre-candidate source pass**, while candidate execution remains prohibited.

Exact sequence is frozen in `06_POST_REPAIR_PROMOTION_SEQUENCE.md`.

## Terminal

`PREMAIN_FIABC_LITS_PREORACLE_INDEPENDENT_AUDIT_R1__JURISDICTION_AND_SUBSTANTIVE_PARITY_LAW_FROZEN__SOURCE_FREE_ONLY__NO_CANDIDATES_RUN`
