# A04S — Issuer, custodian and consumer holds

## 1. Issuer (independent, pre-run)

`V2IssuerRecord` carries `issuer_id`, `issuer_authority_ref`, `issuer_signature`
(SHA-256 over the declaration preimage), `issuance_timestamp` and scope version.
The recorded issuer is `A04S-SOURCEFREE-FIXTURE-ISSUER` — a development
fixture issuer, **not** a competent scientific authority. No real issuance is
claimed; adopting this frontier for any real slice remains a competent owner's
act, and the issuer slot is **held open** for that act.

A missing pre-run issuer identity is itself a hostile (`EXPECTED_SET_OUTPUT_DERIVED`
fires when the frontier cannot be reproduced from the frozen declarations).

## 2. Custodian (independent, pre-execution)

`V2CustodianRecord` carries the frozen frontier digest, the expectation
preimage hash, the issuer signature and a custodian timestamp. It is
established **before any owner runs**; the positive run proves
`frontier == custodian.frozen_frontier_digest`. This is the v2 answer to
"merely hash-equal afterward": equality is necessary but the **chronology**
(pre-run freeze, then execute, then compare) is what makes it independent.

## 3. Consumers: modelled, not executed

The positive run's consumer receipts are **modelled from real produced refs**
(`EmpiricalFact.ref`, `DiscoveryResultReceipt.ref` bound to each
`expected_work_key` through a separate `consumer_obligation_key`). The
required-consumer check genuinely fires (`H12`: every job present, one
consumer missing → `REQUIRED_CONSUMER_OMITTED`).

Invoking a *real* C1 analytical-composition or Field-Forge owner is **B02's
licensed act** and requires existing authority plus a fixture that makes it
lawful. That authority is absent here, so the gate is recorded HOLD:

- exact call signatures the consumer would need: `execute_i03(query_ref,
  predicate_ref)` results → `pre553_analytical_composition`; joint/conditional
  facts → `field_forge_conditional_support`; discovery receipts →
  learned-empirical adjudication;
- **B02 gate:** real consumer invocation waits for an A03-issued slice and a
  competent consumer authority. Until then, modelled receipts prove the
  * join works*, not that consumption happened.

## 4. Typed H/D/NA preserved

Four non-runnable obligations (O/R HELD, V DENIED, U SOURCE_NONAPPLICABLE)
stay visible in every export and never appear as jobs. Removing them is caught
(`HELD_OR_DENIED_WORK_NOT_VISIBLE`, H13); executing them is refused at
declaration time (no owner refs allowed on non-RUNNABLE).

## 5. What the v2 contract does NOT establish

- No original-source read (0 `.sav`/`.dta`); no source-use grant.
- No all-35 scientific eligibility; WGC/WGD/WGE are not workloads.
- No model permission, no G0b/EE12, no operative publication.
- No canonical/PRE-MAIN mutation; no self-adoption; no merge.
- Old A04/A05 evidence is **rewritten nowhere**; their 41/18 suites pass unchanged.
- `declared_to_a04_key` translation (short names → owner URN tokens) is a
  development-scope adapter detail, not a claim about canonical naming.

**Terminal:** `HQ280_PV3_A04S_SOURCEFREE_V2_EXPECTATION_BINDER_ORACLE_ACTUAL_JOIN_RETURNED_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED`.