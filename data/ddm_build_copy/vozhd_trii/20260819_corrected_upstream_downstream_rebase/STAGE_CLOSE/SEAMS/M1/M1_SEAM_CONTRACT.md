# M1 — Temporal / V554 ingress seam exact contract

**Contract:** `M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0`  
**Authority:** dispositive only for the M1 SCR553→SCR554 seam  
**Base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**SCR553 authority:** `b261ff885b2b7fd2cd065917b862eb541e24c4a2` / `SCR553_EXACT_CONTRACT_CLOSED`  
**SCR554 authority:** `b5d745ac70c833324c8be0addf6c08ad72372263` / `SCR554_EXACT_CONTRACT_CLOSED`  
**Production implementation:** not authorized  
**Stage contracts rewritten:** no

## 1. Closure holding

M1 closes without harmonization. SCR553's compact, hash-bound producer objects can satisfy SCR554's richer V553-basis consumer slots by exact immutable dereference. The seam creates no new semantic family and changes neither local jurisdiction.

The binding route law is:

```text
same admission A
+ exact governed invocation U1 requiring no new V553 meaning
  -> SCR553: V553_NOT_REQUIRED_FOR_THIS_USE
  -> SCR554: SIG-001 may count DIRECT basis only if every SCR554 gate independently passes

same admission A
+ exact governed invocation U2 requiring new V553 meaning
  -> SCR553: exact TEMPORAL_* object(s) or typed limit
  -> SCR554: SIG-002/003 requires exact V553 basis; direct basis cannot substitute
```

There is no object-global `TEMPORAL` / `NONTEMPORAL` classification.

## 2. Exact seam invocation binding

M1 uses a nonsemantic control binding, not a new producer object family. For a V554-directed V553 request it binds:

```text
governed_use_id
use_owner = V554
v554_rule_ref { id, version, hash }
signature_id
target_use
focal_structural_proposition_ref
originating StructuralEmpiricalAdmission ref set
required_temporal_operations
SCR553 request/decision ref
required authority snapshots
```

A V553 negative is the *same semantic demand* as a V554 invocation only by exact governed-use/use-rule/signature/proposition/admission participation. Same labels, year, geography string, file adjacency, or provenance proximity cannot establish scope.

## 3. SCR553 producer projection into SCR554 consumer slots

Every SCR553 exported ref binds `family + object_id + content_hash + schema_version`. The content must resolve exactly; the resolved object's semantic hash/authority closure must also verify.

| V553 family | Directly supplies | Immutable dereference supplies |
|---|---|---|
| `TEMPORAL_KEY` | object identity, family, source universe, admission ref, temporal scope, rule/closure | focal proposition, native admission scope, estimand, measure/weight, use/admission authority |
| `TEMPORAL_OBSERVATION` | object identity, key ref, admission ref, source universe, value/status, value owner, rule/closure | focal proposition, key/native scope, estimand and measure/weight closure |
| `TEMPORAL_RELATION` | object identity, ordered/role-bearing participants, source universes, external-compatibility refs, rule, result/support state, closure | originating admissions, propositions, native scopes, participant measure/estimand authority |
| `TEMPORAL_LIMIT` | object identity, governed use, operation, state/reason, participants, blocked family, missing/negative refs, upstream negatives, rule/closure | originating admissions/propositions/source universes and any blocked estimand/measure/source-relation authority |

Thus SCR554's required slots—originating admissions, focal proposition, rule-relevant temporal refs, native scope, source universe, estimand, measure/weight authority, source-comparability authority where required, temporal limits/negatives, interpretation-critical authority, and replay root—are closed without copied payload or label reconstruction.

Any missing, mutable, ambiguous, or hash-mismatched required projection fails closed.

## 4. Mutual basis typing

| V554 signature | Counting basis | V553 role |
|---|---|---|
| `SIG-001` | `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION` | zero semantic support; any irrelevant/no-op V553 material is contextual/provenance only |
| `SIG-002` | `V553_TEMPORAL_OBJECT` | exact `TEMPORAL_KEY + TEMPORAL_OBSERVATION` required |
| `SIG-003` | `V553_TEMPORAL_OBJECT` | exact `TEMPORAL_KEY + TEMPORAL_RELATION + all rule-required support/limit refs` required |

`V553_NOT_REQUIRED_FOR_THIS_USE` means only that SCR553 created no new temporal meaning for that use. It does **not** prove SCR554 direct temporal completeness, rule eligibility, positive static authority, or F1 eligibility.

## 5. Source/composition authority firewall

V553 may consume separately governed source-comparability authority for an operation. Neither SCR553 nor SCR554 may manufacture:

```text
source equivalence
respondent linkage
sample pooling
measure compatibility
estimand compatibility
cross-universe composition
```

Provenance reachability proves reachability only. Temporal comparability does not imply linkage, pooling, or estimand composition. Missing/unknown required authority fails the operation closed.

## 6. Negative precedence

For one exact semantic demand:

```text
applicable TEMPORAL_LIMIT / NONCOMPARABLE / required gap
/ missing-or-unknown required temporal/source authority
=> no direct positive downgrade for that same demand
```

Mapping into SCR554 remains local-contract native: K08 for required temporal noncomparability, K09 for required temporal gap/absence, K06 for missing required static authority, K07 for unknown/conflicting required authority.

A genuinely separate invocation outside the negative's governed scope is evaluated independently. M1 neither broadens nor erases negatives.

## 7. Duplicate/no-op/extra-material law

A no-op V553 restatement plus the originating direct admission cannot create two supports. `basis_kind` is excluded from semantic equivalence, and SIG-001 counts the direct basis only.

Extra V553 material irrelevant to the exact rule invocation has zero support effect. It may remain reachable for provenance/replay but cannot alter the support-equivalence key, F1 multiplicity, confidence, weight, route count, or downstream participant count.

`EQUIVALENCE_UNKNOWN -> FAIL_CLOSED`.

## 8. HQ authority-version guard

One invocation binds **one exact V554 rule ID/version/hash**.

Before duplicate/support counting, SCR554's existing precedence runs:

```text
INTEGRITY
-> producer-governed precedence
-> applicable hard negative
-> STATIC_AUTHORITY_COMPLETENESS
-> temporal/signature gate
-> duplicate equivalence
-> support counting
```

Therefore competing unresolved required authority snapshots cannot be turned into two independent positive supports. If no exact producer-governed precedence resolves them, the invocation is K07/nonassertable before support counting.

Forbidden snapshot resolution includes semver, latest, recency, commit date, score, majority, file order, and row order.

## 9. HQ lineage guard

SCR554's admission-lineage component is interpreted under its own materiality clause:

- **identity-bearing lineage** participates only where governing authority makes the lineage difference change interpretation or lawful use;
- **provenance-only lineage**—direct/V553 path, reissue/alias receipt IDs, replay/transport path, storage path—does not split support and is preserved as alias/reference provenance;
- **unknown lineage role** makes equivalence unknown and fails closed.

This does not amend SCR554; it binds the contract's existing rule that only material equivalence components may distinguish support.

## 10. Replay

Same exact stage heads, rule/signature/use binding, immutable refs/hashes, authority snapshots, and semantic inputs must yield the same projection, negative gate, equivalence groups, support count, and M1 receipt regardless of file/row order or wall clock.

A changed material content/authority hash creates a new replay basis or fail-closed mismatch. No latest substitution is lawful.

## 11. M1 disposition

All eight commanded seam proofs and both HQ guards pass. No local contract rewrite, sibling legislation, D15 reopen, broad-topology change, production implementation, or source retirement is required.
