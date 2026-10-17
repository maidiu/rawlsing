# 03 — Original source authority, hostiles and cold replay

All findings here are reviewer-executed against the accepted chain in the
returned staged closure. Nothing was edited.

## Custody

- Native closure: **74/74** files re-attested from actual bytes — Git blob SHA-1
  (`blob <len>\0<content>`), sha256 and byte count all equal to
  `court/source_selector.json`. **0 missing, 0 drift.**
- Accepted Field Forge GT2 module blob `a70decb20747d84cbcbe27d1280babc6de88ef33`
  — equal in the candidate stage, in the current tree, and to the commission pin.
  **Unmodified.**
- Precommitted oracle commit `686b1dae` ("R17 GF1: PRE-COMMITTED generic native
  PAIR oracle, frozen before candidate execution") is present and is the sole
  source of that oracle. My own oracle
  (`01_FROZEN_GENERIC_PAIR_AND_ROLE_ORACLE.json`) was derived independently and
  is not a copy.

## Eight operations preserved, both ORDERED opportunities still HELD

From `court/authority/register.json`: **6 RUNNABLE + 2 HELD**, and both HELDs
carry `hold_reason = ORDERED_OWNER_NOT_ISSUED`. The candidate did not quietly
promote an ORDERED opportunity. This is correct and is preserved.

## Hostiles executed by the reviewer (all fail-closed as expected)

| Hostile | Expected | Observed |
|---|---|---|
| reverse target/conditioner swap with **no** separate grant | refuse | `GenericNativePairError` |
| forged / never-issued reverse grant string | refuse | `GenericNativePairError` |
| relation permission ceiling widening beyond producer | refuse | `GenericPermissionWideningError` |
| non-native role ref (`urn:test:foreign:not-native`) | refuse | `GenericNativePairError` |
| replay determinism | identical identity | identical `content_hash` |

Not independently re-executed here (they belong to the unreproducible 44-case
suite): foreign expected root, foreign register root, fact-content mutation,
coherently rehashed structural forgery, weighted numerator, nonbinary category,
domain-identity mismatch, tampered relation object, source-A withdrawal.

## Missingness vs zero support — independently confirmed

The distinction the commission singles out holds in the executed material:

- **Zero cell inside an eligible risk set** → `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`.
- **Condition with no eligible respondent** (DISCOVERY, Y-ineligible) → per-condition
  denominator `0`, never a zero cell, and the relation's eligible joint risk
  drops to `1`.
- **`ZERO_SUPPORT` never appears** anywhere in any produced relation, at any
  profile.

So an absent eligible cell is not laundered into measured zero support.

## Cold / duplicate / replay — what is and is not established

**Established here:** in-process deterministic reproduction. Re-producing a
relation from the same fact/query/roles yields a bit-identical
`content_hash`.

**NOT established here:** a SIGKILL-grade, two-process cold replay at a *new GF1
relation identity*. I did not execute SIGKILL, so per the commission I do **not**
relabel PV3N's original cold run as a new independent GF1 cold proof. That cell
remains open and must be executed against the returned artifact once it exists.

## Source/authority holds (unchanged by this review)

- No original U/E_pre issuance; no source-use grant; no respondent data.
- The fixture is sourcefree (`SOURCE_FREE_DEV` permission ceiling throughout).
- No signed source grant is inferred from hashes anywhere in the executed path.