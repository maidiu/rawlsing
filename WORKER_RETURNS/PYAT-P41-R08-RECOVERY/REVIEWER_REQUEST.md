# Independent reviewer request

**Reviewer:** distinct I3+ sourcefree ABI/consumer and scientific-hostile reviewer.
Not the P41/R08/E03/SC0/PE author, not this integrator, not an own reviewer.

**Exact branch:** `agent/pyat-recover-p41-r08-world-evidence-consumer-20261030-r1`.

**Exact SHA:** reported after push/readback; reviewer must verify remote SHA
before execution.

## Fixed review scope

1. Re-run the exact P41 19 suite and the three `.proof.json` severance witnesses;
   confirm W1/W2/W3 are `BOUNDED_MUTATION_DETECTED` and the restored suite is
   green.
2. Re-run current E03 18, current C1/N10E/F8 69, learned-world 30.
3. Re-run selected-world 24 and exact seam 27; confirm the seam remains
   **26/1** `KeyError exact_probabilities`; do not accept the 24 positives as
   masking it.
4. Re-run the bounded selected-world repair 5 and verify source-owned value
   change 3/4→1/2, stale-contract refusal, zero-vs-missing, cold restore and
   mutation/restore.
5. Re-run the current P41-style adapter 5; verify current E03 geometry, as-of/
   rule-clock metadata, empirical revocation, historical archival, cold restore
   and tamper refusal.
6. Re-run `repro/run_r08_current_binder.sh`; verify 113 author tests + 8 R8
   targeted probes against current `rawlsing_next`.
7. Inspect for any production import, shared-file overwrite, ephemeral HMAC
   overclaim, actor/person creation, original-source read or merge.
8. Decide whether the current production-receiver GAP CARD is sufficient HOLD or
   whether a named current adopter exists.

## Required adversarial checks

- missing binder -> fail closed, not green;
- foreign issuer / forged admission -> refused, no support;
- stale source/cache -> typed refusal, no support;
- altered evidence/query/rule object -> refusal, no signed projection leak;
- unsafe cache/self-seal/replay -> refusal; correct cold restore works;
- source-owned numeric mutation under old selected-world contract -> refused;
- rebound source-owned values -> changed exact output;
- P41 current empirical revocation -> consumer refused, producer geometry still
  exact, historical receipt retained;
- P41 current receipt tamper -> hash refusal;
- selected-world zero vs missing -> distinct `ZERO_SUPPORT` and `NO_SUPPORT`;
- actor/V3/person/route probability remain absent.

## Commands

```bash
./repro/run_sourcefree_adapters.sh
./repro/run_r08_current_binder.sh
```

Historical courts are documented in `TEST_RECEIPTS_AND_FAULT_NEGATIVES.md` with
exact commands, exits and temp-tree provenance.

## Reviewer verdict fields

- six-axis engineering verdict;
- source/science authority verdict;
- original P41/R08/selected-world meaning preservation;
- current production receiver: named or GAP CARD;
- merge/adoption recommendation (default NO MERGE);
- exact SHA and any scope corrections.

No self-review, no automatic worker spawn, no PRE-MAIN merge.
