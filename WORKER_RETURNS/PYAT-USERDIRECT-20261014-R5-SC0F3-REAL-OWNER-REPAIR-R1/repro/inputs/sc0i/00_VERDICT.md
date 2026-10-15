# SC0I Independent Verdict on SC0F

**Commission:** PYAT-USERDIRECT-20261014-R3-SC0I-INDEPENDENT-REPAIR-COURT-R1
**Branch:** `agent/userdirect-pyat-20261014-r3-sc0i-independent-repair-court-r1`
**Sealed startup:** `b87fe719dd822ae243e29ddc40b000cf32649fcd`
**Candidate SC0F:** `7add9ef5a1a4698d4aed177be8a158b75e220a5d`
**Blobs verified:** producer_bridge `3738e27b…98717e`, adapter `03f0c509…8806b60`, strict_receipts `10de6bae…97fed79`, tests `e9b9aae7…c00ed`

## Verdict: RED

SC0F's 10 author tests pass as executed (10/10). The passing suite does not
establish real producer computation or issuer-warrant security. Two REDs are
proved by independent execution; additional HOLDs recorded.

## RED-1: Import-only producer computation (proved)

`SC0FProducerBridge._compute_via_n10e_c1` imports
`provide_empirical_possibility_slice`, `compose_positioned_subject_possibility`,
`evaluate_positioned_subject_possibility` and **never invokes any of them**.
Monkeypatch counters on the real functions record zero calls.
The tracer writes `sha256(b"imported")` as both args and result digest, then
`_compute_via_fixture_cells` computes from fixture cells.
Import availability is therefore not accepted producer computation.
Hostiles: `test_h01_n10e_c1_imported_never_invoked`,
`test_h02_import_trace_uses_sha256_of_imported` — both PASS (defect present).

## RED-2: Forged warrant self-registration accepted (proved)

`register_issuer_warrant` is an unrestricted public mutation of module-global
`ISSUER_REGISTRY`. An adversary calling it with a forged grant first, then
presenting the same forged grant to `request_role_reversal`, receives
`REVERSAL_PERMITTED_UNDER_REGISTERED_GRANT`.
Hostile: `test_h03_forged_warrant_accepted_after_self_registration` — PASS
(defect present). A forged warrant must be refused even after self-registration;
this requires an independent issuer signature or registry not writable by the
attacker. No real reverse-role grant exists.

## HOLDs (structural, not blocking source-free interface grade)

- H04: `test_06` asserts options nonempty, not the actual 50/10 numeric
  propagation to both readsets.
- H05: `selection_state` defaults to COMPLETE when missing.
- H06: `fx:scope:town2008` is an unconditional allowlist entry.
- H07: `earlier_knowledge_evidence_ref` is accepted by presence, not by
  issuer validation.

## Consistency with prior courts

- RC0 (`86bd2a54`): CHANGES_REQUIRED with 12 independent REDs — consistent.
- SC0F author report of all-green suites conflates NEW SC0F, ORIGINAL SC0,
  and unrelated accepted-owner suites; this review executes SC0F's 10 plus
  7 independent hostiles and distinguishes them.

## Scope

No N9/N10W issuance, no V3, no canonical adoption, no C0 adoption.
SC0F code unchanged. Frozen oracles unchanged.

## Terminal

`SC0I_VERDICT_RED__PRODUCER_COMPUTATION_UNPROVED__ISSUER_REGISTRY_UNGUARDED__NO_ADOPTION`
