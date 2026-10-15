# 03 — separate independent I2 review request and hostile acceptance matrix

## 1. Reviewer independence

**Requested reviewer class:** I2 High independent interface/authority reviewer,
**distinct from** the SC0 candidate author (HQ298), the RC0 reviewer
(`86bd2a54687b40401f7c4247607bd1873c585619`), the PE/C1/N10E owner authors and
this HQ300 repair implementer.  The author of this repair may not accept or
self-adopt it.

## 2. Hostile acceptance matrix (fixed scope for the reviewer)

| # | Hostile check | Evidence to reproduce | Acceptance condition |
|---|---|---|---|
| A1 | RC0 custody | `staging/rc0/` blob SHA-1s vs `86bd2a54…`; `staging/rc0/test_rc0_hostile.py` byte-identical | test source unmodified; expectations ledger sha256 `8eda5d91…` |
| A2 | 12 RED repair | `bash repro/run_hq300_battery.sh [2]` | all 12 former REDs PASS with the frozen reviewer source |
| A3 | 13 PASS preservation | same run | none of the 13 prior PASSes regressed |
| A4 | K9 8 / K10 28 | `[1]` | frozen expected classes unchanged (oracle-loaded, not retyped) |
| A5 | envelope schema | `TwoContractAdapter.validate_receipts` + `staging/rc0/test_rc0_hostile.py::test_direct_receipts_satisfy_original_frozen_envelope_schema` | 0 jsonschema errors on BOTH receipts against the pinned draft-2020-12 envelope |
| A6 | 12-state negative algebra | `test_full_original_negative_state_distinctions_survive` | exact equality with the oracle baseline's 12 `status_rows` incl. `DENIED_USE` |
| A7 | permission fail-closed | `test_adapter_denied_world_read_must_not_emit_consumer_values` | DENIED_USE at adapter entry for BOTH providers, before any value read |
| A8 | demand closure | `test_foreign_demand_cannot_be_labelled_complete` | foreign demand never served COMPLETE |
| A9 | clock lookahead | `test_knowledge_asof_cannot_consume_future_publication` | no 2010 publication consumption under 2009 knowledge; hostile 2009/2010 pair refuses |
| A10 | reversal dereference | `test_matching_issuer_string_cannot_authorize_foreign_scope_or_target[scope/target/…]` | scope AND target mutations held; independent reverse issuance recorded |
| A11 | producer connection | `port/test_connection.py` | run() produces real PE/C1/N10E call events; static-hint-only lane raises INTEGRITY_FAILURE |
| A12 | values-read / intervention | `test_actual_value_intervention_changes_both_consumers_and_only_affected_route` | true world-value read both consumers; empirical support invariant |
| A13 | facade lineage | `round_trip_two_contracts` with lineage removed (adversarial) | REJECT_SEMANTIC_LOSS when consumer values/effects lineage is discarded |
| A14 | owner suites | `[4]` `[5]` | 56 + 21 pinned suites green |
| A15 | fixture-correction audit | `02_EXECUTION_RECEIPTS.json#fixture_correction_disclosure` | reviewer adjudicates whether as_of 2009→2011 fixture correction is acceptable or demands an alternative |

## 3. Owner-blocker register (competent authority required; NOT taken here)

| # | Blocker | Owner | State |
|---|---|---|---|
| O1 | Operative N9 selected-world service (real source release, currentness, demand closure) | N9/world-serving authority | MISSING_IMPLEMENTATION; port stays sourcefree fixture grade |
| O2 | N10W joint world+empirical model-use grant | model/use issuer | MISSING_SOURCE_AUTHORITY |
| O3 | Real reverse-query issuer (target/risk/denominator beyond fixture scope) | statistical issuer | MISSING_SOURCE_AUTHORITY |
| O4 | Adopted model authority / use grant refs (the envelope requires non-null refs; the port supplies TEST_ONLY refs) | model/use issuer | TEST_ONLY refs are placeholders of the fixture grade, not adoption |
| O5 | PE candidate's own validated defects (from RC0's nine PE REDs adjudication) | Pyat PE owner | unchanged here; RC0's 05_OWNER_ACTION_REGISTER stands |
| O6 | Acceptance of this repair candidate | independent I2 reviewer | PENDING (this request) |

## 4. Escalation law

No I3/Astra escalation: the repaired items are ordinary candidate interface
defects and missing dependencies; no accepted-authority contradiction was
demonstrated.  If the reviewer finds that the envelope's non-null
`model_authority_ref`/`use_grant_ref` requirements conflict with the fail-closed
"no fabricated issuer" law, that single question is an accepted-authority
collision and may go to I3 with a precise packet.
