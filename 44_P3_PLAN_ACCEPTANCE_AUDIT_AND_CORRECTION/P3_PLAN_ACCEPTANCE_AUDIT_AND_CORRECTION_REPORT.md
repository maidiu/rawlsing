# Rawlsing P3 Plan Acceptance Audit and Correction Report

## Verdict

The v21 plan was conceptually coherent but **not implementation-ready**. Its packaging verifier passed because it tested presence and headline doctrine, not cross-contract executability. This review corrected the contract before P3A began. No candidate inventory or canonical J-family authority was generated.

## Critical findings corrected

1. **Upstream undercount.** V21 froze 641 proposition relations. Correct precedence yields 19,175 effective direct pair authorities and 658 connective proposition pairs. Seventeen exact-only proposition edges and 327 exact-only constraints/coordinates were omitted.
2. **Authority precedence absent.** 407 pairs occur in both registries. Semantic-priority closure now explicitly governs overlaps; exact rows remain superseded provenance.
3. **JSON Schema graph broken.** Relative `$ref` values lacked resolvable schema identities. V2 assigns absolute local schema IDs and validates templates offline through a registry.
4. **Draft/final decision confusion.** The empty decision form could not satisfy the final decision schema. V2 separates draft and completed schemas and provides a valid final example.
5. **Lifecycle/classification conflation.** Two candidate classes were unreachable in the state machine. V2 separates lifecycle stage, diagnostic classification, and terminal decision status.
6. **Canonical-family persistence missing.** V1 DDL lacked canonical family and immutable revision tables. V2 adds stable family identities, revisions, memberships, variants, exclusions, genealogy, and release snapshots.
7. **Weak referential integrity.** Many member/endpoint IDs were untyped text. V2 registers inherited and P3 objects and uses registry foreign keys.
8. **Vocabulary leakage.** Numerous categorical fields were hard-coded or unconstrained. V2 expands controlled vocabularies and adds closure tests.
9. **Release contract mismatch.** JSON release objects and DDL did not share object counts/change tracking. V2 adds release status events, object snapshots, and change ledgers.
10. **Schema dictionary contradiction.** V1 stated direct endpoint authority could be true, contradicting the universal no-path-authority rule. V2 regenerates the dictionary from DDL and preserves `creates_endpoint_authority=false`.
11. **Identity strategy underspecified.** V2 distinguishes inherited, content-addressed derived, and registry-allocated durable objects, preventing either renumbering or false persistence.
12. **Downstream references incomplete.** V2 preserves response-contract, structural-context, and licensing references without claiming P4/P5 authority.
13. **Proposition signatures structurally underconstrained.** A free-form array could duplicate one field twelve times while omitting others. V2 requires exactly the twelve governing signature dimensions and records open-ended source values separately from optional normalized codes.
14. **Candidate packets undertyped.** Generic object arrays could satisfy the schema while omitting the actual adjudication surface. V2 types signature, response, pair, collision, closure, variant, and exclusion summaries.
15. **Promotion history impossible.** A partial unique index allowed only one PROMOTED event across all history. V2 preserves append-only promotion events and uses a transactional singleton pointer for the current runtime release.
16. **Categorical vocabulary was documentary rather than enforceable.** V2 adds field-to-vocabulary bindings and a migration-time PostgreSQL enforcement function/trigger contract.

## Upstream compatibility proof

- 18,831 semantic-priority rows; all origin ruling IDs resolve to delivered source-section CSVs.
- 751 exact-foundation rows.
- 407 overlaps.
- 344 exact-only governing pairs.
- 19,175 unique effective direct pair authorities.
- 658 connective proposition pairs.
- Every endpoint resolves to the 13,526 source-local lineage registry.

## Downstream posture

The corrected contract now supports P4 measurement compatibility, P5 structural authority, P6 shadow installation, P7 persona/pressure integration, new-wave attachment, P2 correction blast-radius analysis, and source-license provenance without importing those authorities into P3.

## Acceptance boundary

V22 accepts the **P3 structure and implementation plan v2**. P3 execution remains unstarted. The next step is `P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION`.
