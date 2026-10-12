# A04T — Competent issuer and real consumer holds

## 1. Issuer: HELD, explicitly

No independently authenticated source-science issuer exists in this scope.
The v2 `V2IssuerRecord` (self-computed SHA-256 + asserted timestamp) is
**not** provenance — A04SR proved a preimage hash proves integrity, never
principal, and an asserted timestamp proves nothing about time. The verifier
therefore:

- recomputes the frontier digest from the separately authored payload and
  compares it to any claimed custodian digest (`CUSTODIAN_MISMATCH` on
  divergence; `CUSTODIAN_ABSENT` when none is supplied);
- reports a structurally consistent custodian as
  `STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN` — integrity without custody;
- records backdated timestamps without trusting them (`timestamp_trusted:
  false` always);
- reports `EXTERNAL_CUSTODIAN_ISSUER_HOLD` **unconditionally**, pass or fail.

What *would* close the hold: an independent custodian holding the expected
set before execution, publishing an authenticated (signed) commitment to a
preimage it controlled, with a time source the candidate cannot set —
ideally an append-only transparency log. No fake key issuance is proposed;
until such an authority exists, the hold stands and every frontier is a
development-grade expectation, never an issued authority.

## 2. Real consumer: MODELLED, never executed

No real C1 / Field Forge / learned consumer was executed in this scope, and
none is claimed. Purported receipts (built from real produced
`EmpiricalFact`/`DiscoveryResultReceipt` refs) satisfy the **structural**
consumer join only. The separate `actual_consumer_court` holds
`REAL_CONSUMER_MODELLED_NOT_EXECUTED` even on a structural pass — including
against hypothetical "authenticated" input, whose receipt class is not
established here.

The pre-existing C1 / Field Forge / learned target first consumer remains
the owner to bind. Its exact runnable prerequisites for a separately issued
**B02** (A03-issued slice, competent consumer authority, real invocation)
are unchanged from A04SR §6 and are **not** met here.

## 3. Typed H/D/NA preserved

O/R HELD, V DENIED, U SOURCE_NONAPPLICABLE stay visible in every export and
never appear as jobs. Removal is caught (`HELD_OR_DENIED_WORK_NOT_VISIBLE`);
execution is refused at freeze.

## 4. What this packet does NOT establish

- No original-source read (0 `.sav`/`.dta`); no source-use grant.
- No all-35 scientific eligibility; WGC/WGD/WGE are not workloads.
- No model permission, no G0b/EE12, no operative publication, no temporal or
  actor/V3 grant.
- No canonical/PRE-MAIN mutation; no self-adoption; no merge.
- No v2↔A05 key equality, ever: the migration audit declares
  `NONREPRESENTABLE` at full-key level unconditionally, triple mapping only
  where the grammar genuinely overlaps, and set-level non-injectivity where
  Y-RAW/Y-WEIGHTED would collide. The old A05 oracle is valid for its own
  contract only.
- Old A04/A04S/A05 evidence is rewritten nowhere; their 41/26/18 suites pass
  unchanged alongside the v2 verifier's 44.

**Terminal:** `HQ280_PV3_A04T_ACTUAL_V2_INDEPENDENT_NO_DROP_VERIFIER_JOIN_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`.