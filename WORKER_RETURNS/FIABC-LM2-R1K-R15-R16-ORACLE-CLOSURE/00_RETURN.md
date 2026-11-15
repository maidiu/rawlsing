# FIABC-LM2-R1K — R15/R16 Common-C11 + Fresh WVS Oracle Closure

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-lm2-r1k-r15-r16-oracle-closure-r1`

Exact common base: `357cc2ac6952a478fa2e38f9adbe45ebb3671081`

## Disposition

R15 **PASS**. R16 **BLOCKED fail-closed before oracle freeze**.

Terminal:

`FIABC_LM2_R1K_R15_PASS__R16_BLOCKED__FROZEN_DISCOVERY_AUTHORITY_VALIDATION_KIND_ENVELOPE_INCOMPLETE__LOCK2_PRESERVED__CANDIDATES_NOT_STARTED`

The R1J physical→native representation repair successfully removed the old R15 physical-key blocker. Strict real-material common C11 was built from the persisted Q291 carrier without rereading the SAV and produced a new exact logical release.

R16 then exposed an independent pre-existing P2F2 authority defect. The frozen DiscoveryAuthority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab` has no `validation_rules.kinds` grant, while its exact frozen candidate grammar `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6` uses:

- `TARGET_CELL_SUPPORTED`
- `JOINT_NOT_PRODUCT_OF_MARGINALS`
- `DISTRIBUTION_DIFFERS_FROM_BASELINE`

The current generic I05 executor explicitly requires every compiled candidate validation kind to be contained in `DiscoveryAuthority.validation_rules.kinds`. The first real neutral I05 attempt therefore stopped with:

`Pre553AuthorityError: candidate validation rule exceeds exact discovery validation authority`

No bypass was used. No oracle was minted.

## R15 exact result

- source: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- carrier: `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`
- projection identity: `f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665`
- logical release: `e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f`
- replay manifest: `996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f`
- source release manifest: `a79ec6404330d34f0ae7cc365b895d09592e2f66749b5706111f42d6fb835570`
- public objects: **486110**
- internal records: **97222**
- complete exact Q291G5/Q291P5 response-slot law retained
- generic int/float coercion: **none**
- raw-value semantic inference: **none**

## R16 blocker provenance

The validation-kind guard is not an R1J change. It already existed on the original EE-P2F2 issuer branch. That issuer compiled/froze the 46-candidate frontier but did not execute the generic I05 evaluator that enforces the validation-kind ceiling.

Repairing the frozen DiscoveryAuthority would change its identity and the Lock2 material that binds it. This worker is forbidden to mutate Lock2, so the lawful result is a bounded stop rather than an authority rewrite.

## Conservation

Lock2 remains exactly:

`8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`

The exact 46-candidate frontier and family shape 10 / 1 / 10 / 25 remain unchanged.

Candidate outputs consulted: **0**

Candidate A/B/C processes started: **0**

WVS SAV/ZIP opened: **0**

Measured P2X: **0**

Historical LM2 oracle/blocker reused as fresh truth: **no**

The next lawful court must repair/reissue the P2F2 DiscoveryAuthority validation-kind envelope together with whatever Lock2 successor that necessarily entails, then re-enter R16. R15 itself does not need semantic patching.
