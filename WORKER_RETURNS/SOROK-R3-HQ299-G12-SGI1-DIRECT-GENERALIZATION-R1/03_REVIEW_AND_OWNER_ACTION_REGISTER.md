# 03 — separate independent review / owner-action register

## 1. Independent review request (mandatory; implementer cannot self-review)

**Requested reviewer class:** I2 genealogy/domain reviewer **independent of** the
S-GI1 author (`agent/rabochii-sorok-sgi1-sourcefree-genealogy-k11-lab-r1`), the
GI2 surrogate author (`agent/rabochii-sorok-r3-hq298-sgi2-forward-generalization-r1`),
the G11 court, and this G12 implementer.  No self-adoption.

**Fixed review scope (six parts):**

1. **Custody:** verify `staging/sigi1_staging_manifest.json` (34 Git blob SHA-1
   preimages, NUL `blob <len>\0` header) against `27ca1f2792a5213064c0b5ea2e27b89e8acce0c3`;
   verify executed `module.__file__` blobs in `02_EXECUTION_RECEIPTS.json`.
2. **Original-suite reproduction:** re-run `repro/run_g12_battery.sh` on a
   separately prepared worktree; confirm 24/24 cases + 98/98 predicates with
   `SGI1_MODEL=0 SGI1_REUSE_RECORDS=1`, and confirm suite fingerprints match the
   original `staging/sigi1_reference/.../suite_fingerprints.json` (0/field diffs).
3. **GI2 oracle custody:** confirm `gi2/frozen_heldout_families.json` sha256
   `5b3339d5e28205032e44bd4e614b03e94de8a09bb90a0c66710b9efcf5f948ca` and that
   no oracle string was rewritten (expected statuses preserved verbatim in
   `02_EXECUTION_RECEIPTS.json#family_status_matrix`).
4. **Adapter-glue audit:** adversarially re-derive ≥3 family mappings from the
   frozen ledger and confirm `gi2/sgi1_bridge.py` introduces no genealogy
   semantics of its own; specifically check the declared interventions
   (fail_first schedule realisation via endpoint predicates; asymmetry knob;
   status-name back-map) are test-input/harness adaptations, not semantic patches.
5. **Gap adjudication:** independently confirm the 4 typed gaps (HW06 staleness
   semantics, HW10 pre-attempt future-requirement gate ×2 predicates, HW02
   older-child fixture schema) are genuinely absent from S-GI1 rather than missed
   adapter routes.
6. **Ceiling check:** confirm nothing in this return claims adoption, ADP015/020
   issuance, operative V3, original-source validity, or population calibration.

**Verdict vocabulary for the reviewer:** accept as
`PINNED_IMPORTED_OWNER_DIRECT_GENERALIZATION_EVIDENCE` / return RED / hold.
The reviewer may NOT accept as semantic adoption, N11/N12 readiness, or V3 wake.

## 2. Owner-action register (competent authority required; NOT taken here)

| # | Action | Competent owner | Why needed |
|---|---|---|---|
| O1 | Adjudicate whether `WORLD_EVIDENCE_STALE` (N9 evidence as-of/staleness custody) should become an accepted typed state | N9/evidence-custody authority | G12 found the semantic absent; adopting it is a semantic change, not a lab repair |
| O2 | Adjudicate whether a declared future-required endpoint must be refused pre-attempt as `FUTURE_CHILD_INFORMATION_LEAK` | ADP015/020 + embargo authority | S-GI1's guard audits anchor-visible fields only; the pre-attempt gate would be new law |
| O3 | Decide whether S-GI1's older-child fixture (M2) should grow GI2's `OLDER_CHILD*`/care-hours schema | genealogy fixture owner | currently a fixture-schema gap, not a semantic failure |
| O4 | Adjudicate whether default relation views must be asymmetric or independence-without-reciprocity suffices | ADP015 authority | S-GI1 default is equal-valued independent states; asymmetry is an intervention |
| O5 | Repair `run_pipeline`'s dead `extra_llm_candidates` parameter / expose candidate endpoint predicates | S-GI1 implementation owner | interface defect found; not repaired here (no owner mutation) |
| O6 | Independent acceptance of the 24/98 + 53/57 evidence grade | distinct I2 reviewer (see §1) | no self-adoption |

## 3. Conflict register

| Item | Conflict | Disposition |
|---|---|---|
| status names | GI2 expected-status strings vs S-GI1 typed vocabulary | mappings declared **before** execution in `01_FROZEN_GI2_EXPECTATION_LEDGER.json`; no oracle rewritten |
| fail_first semantics | GI2 surrogate forces failures by schedule; S-GI1 has no such knob | realised through S-GI1's own endpoint-mismatch mechanism (declared test intervention); no surrogate code executed |
| HW06/HW10 | GI2 expects typed statuses the owner cannot express | flagged AUTHORITY_GAP, never patched; no escalation to I3 (ordinary missing semantics, not an accepted-authority collision) |
| model_status label | S-GI1 summary says `AUTOMATED_LLM_PROPOSAL_EXECUTED` | label belongs to the frozen historical records; this G12 run made 0 model calls (recorded explicitly in receipts) |
