# Code / architecture hostile audit

The R2 rewrite materially improves W55C's validator. Four schemas are actually invoked; live canonical-head equality is checked; top-level mode/effect enums are registry-bound; bounded children are structurally stripped of adoption/closure authority; touched-obligation dispositions are cross-checked; per-successor paths are exact; and known anti-resurrection promotions are structured.

It still fails the governing fail-closed standard.

## Material fail-open findings

1. **Unknown structured authority effect is accepted.** R2 schema requires only a nonempty string for `authority_effects[].requested_effect`. Validator logic asks whether that string is *not* in the target's forbidden list. A novel/typo promotion class therefore passes instead of failing unknown closed and can be mirrored into `work_return.authority_obtained`.
2. **Decision-domain laundering.** Required grounding is selected by packet-controlled `decision_domain`. There is no machine binding from the declared domain to task/result/closure/authority subject. `GENERAL_PROJECT_DECISION` is adoption-eligible with minimal Ground + State Now requirements and can be used to evade deeper physical/Field-Forge/etc. scopes.
3. **Shallow bounded parent can still bless execution.** Parent bytes, hash, receipt id, mode, head, Ground version, PASS, prohibition tokens, and child-subset checks are strong; the parent itself is not re-run against a machine-validated subject/domain relationship for the child's real work.
4. **Successor/parent coupling remains incomplete.** Exact successor mapping is fixed. The validator does not require outstanding successor returns to keep the parent obligation/reintegration grain nonterminal.
5. **Closure evidence is syntactic.** `closure_condition_addressed` need only be nonempty; `supporting_evidence_ref` need only resolve/exist. Exact authority string is copied from the obligation row, but no actor credential or evidence-content relation is established.
6. **Evidence identity is not immutable.** `resolve_ref` accepts existing working-tree paths and arbitrary Git-resolvable strings. A path can later change while the packet text remains unchanged.
7. **Unknown normalization inherits weak closure.** UNKNOWN/BLOCKED may close through the same weak closure claim; ABANDONED_BY_EXPLICIT_DECISION has no independent explicit-decision proof gate.
8. **Governance self-modification gap.** No candidate mechanism requires changes to the validator/schema/scope registry/enforcement map themselves to be adjudicated under a prior immutable enforcement version plus fresh hostile audit before use.

These are implementation defects, not a reopening of the Ground constitution.