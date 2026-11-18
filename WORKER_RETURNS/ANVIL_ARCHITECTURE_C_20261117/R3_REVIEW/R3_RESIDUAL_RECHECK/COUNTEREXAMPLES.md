# R3 residual recheck — exact remaining counterexample

## G1-REVERSE — `FF01KProduct.target_roles = k>=2` conflicts with reverse `P(D|Y)`

**Claim:** `R3_FIELD_AND_ADAPTER_CONTRACT.md` §6.2, lines 162–164, defines
`FF01KProduct` with:

- `direction = FORWARD (P(Y|D))` or `REVERSE (P(D|Y))`;
- `conditioner_roles = ordered tuple ...`;
- `target_roles = ordered tuple k>=2`.

The table applies `k>=2` to `target_roles` for both directions. That is
dimensionally wrong for the user-required reverse form `P(D|Y)`: the target
there is `D`, which need not be a k>=2 vector, while the conditioner is the
ordered `Y1..Yk` set. The forward `P(Y1..Yk|D)` correctly needs target Y
`k>=2`; the reverse needs conditioner Y `k>=2`, target D `>=1`.

`R3-RES-032` repeats “ordered k>=2 roles” without direction-specific
cardinality, so the research entry does not repair the ambiguity.

**Minimum correction:** make the role cardinality direction-specific:
- `FORWARD`: `conditioner_roles = D` (>=1), `target_roles = Y1..Yk` (k>=2);
- `REVERSE`: `conditioner_roles = Y1..Yk` (k>=2), `target_roles = D` (>=1);
- both retain separate risk/denominator bases, exact native fact/query/replay,
  weights/coverage/typed states, owner-held ratio, receipt and prospective
  consumer.
Update the table, `R3-RES-032`, and any decision/capability wording that repeats
`target_roles k>=2` unconditionally. No implementation or new science is
required.

## Resolved residuals (no counterexample found)

- **G4-A:** §2 lines 37–64 excludes state/value from stable identity keys;
  checked content conflicts refuse `TYPED_IDENTITY_CONTENT_CONFLICT`;
  repeated/ranked events, weight basis/scope/design, coordinate time and
  routing risk/rule distinctions remain explicit.
- **G4-B:** §3 lines 66–92 requires exact ordered candidate/risk/denominator
  member refs and nonselected typed states; counts are diagnostic; full
  `_ReleaseIndex` is the baseline; compact sidecar is proposed/owner-qualified.
- **G4-C:** §4 lines 94–110 separates selected page reads, full `O(R)`
  population/routing/weight validation, full membership, and refs/output;
  explicitly removes bounded-RAM/Q claims and keeps 6 GiB unproven.
- **G2EXT:** §5 lines 112–140 defines proposed `ExternalSourceArtifact` kind/ref/
  digest/source-lineage/native version/scope/rights/current/lookup/receipt/
  ambiguity/refusal; explicitly no existing general resolver and no false C11
  preservation claim.
- **Adapter retention:** the native adapter/`_ReleaseIndex`/`execute_empirical_query`
  path remains in the authoritative `R3_ARCHITECTURE_DECISION.md` §3.2–3.3, so
  it was not lost when the field contract was replaced.
- **G3/G5:** old 27 ledger entries byte-preserved; 32 total; decision/table/
  falsifier/contract refs resolve; F6 external/typed-absent wording remains
  explicit.
