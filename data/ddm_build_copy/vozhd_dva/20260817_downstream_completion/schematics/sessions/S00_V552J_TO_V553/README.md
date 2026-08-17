# S00 Session — upstream availability → V553 → V554 demand

**Status:** PREPARED_FOR_BREAKOUT  
**Owner:** Vozhd Dva  
**Primary immediate seam:** canonical V552J → V553  
**Broader intake scope:** every lawful upstream/co-authority input available to V553  
**Downstream consumer:** V554

## Governing question

S00 does **not** begin by assuming a neat serial handoff. It begins by establishing two envelopes:

1. **Upstream availability envelope:** everything lawfully available upstream that V553 could potentially draw on, whether through V552J, direct V552 outputs, or earlier authority/provenance/validation context.
2. **V554 demand envelope:** everything V554 actually needs V553 to deliver in order to perform V554's bounded-affordance transformation without guessing, reconstructing, or reaching behind V553.

Only after both are mapped do we define V553's job.

The governing sequence is:

`WHAT IS AVAILABLE UPSTREAM`
`+ WHAT V554 NEEDS TO ARRIVE`
`→ WHICH UPSTREAM MATERIAL V553 SHOULD LAWFULLY CONSUME`
`→ WHAT V553 MUST / CAN CREATE FROM IT`
`→ EVERYTHING V553 CAN LAWFULLY EMIT`
`→ THE MINIMUM V553 OUTPUT CONTRACT THAT SATISFIES V554 WITHOUT DOING V554'S WORK`

In compact form:

`UPSTREAM AVAILABILITY → V554 REQUIREMENT → V553 LAWFUL INTAKE → V553 TRANSFORMATION → V553 REACHABLE OUTPUT ENVELOPE → REQUIRED V553→V554 CONTRACT`

## Why this order matters

V552J is the immediate governed handoff, but current V553 also exposes/directly consumes V552 structural-fact and temporal-key-source indexes and consumes semantic/directionality/position authority overlays plus thin-readiness context. S00 must determine which of those are legitimate semantic co-inputs, which are authority/provenance/validation context, which should already be represented through V552J, and which should not be consumed by V553.

At the same time, V554's actual needs constrain which V553 transformations and outputs matter. V553 should neither starve V554 of meaning that upstream authority makes available nor inflate itself with semantics that V554 or later named capabilities do not require.

## S00 law

For every proposed V553 output field/object answer, in order:

1. **What upstream evidence/authority capable of supporting this exists?**
2. **Does V554 actually need this information, and for what operation?**
3. **Which upstream surface should V553 consume to obtain its lawful basis?**
4. **What genuinely new transformation does V553 perform?**
5. **What output becomes lawfully reachable after that transformation?**
6. **Which reachable output must be part of the V553→V554 contract?**
7. **What must remain unresolved, absent, noncomparable, blocked, or forbidden?**

Current direct reach-back is evidence to assess, not architecture to preserve automatically.

V553 must transform governed upstream structure; it may not replace existing structural identity with convenience labels simply because those labels are easier to aggregate.

The corrected POSTG5-004 consumer boundary on canonical `main` is part of the factual starting point. Its integrity behavior is accepted; the complete semantic intake architecture remains subject to S00 adjudication.

## Breakout cells

- `FORWARD_V552J/` — build the **upstream availability / reachable-output** side: inventory everything lawfully available to V553, classify proper intake jurisdiction, and determine what V553 can lawfully create.
- `BACKWARD_V554/` — build the **V554 demand / required-output** side: determine what V554 actually needs, then identify the lawful upstream basis and V553 transformation required to supply it.

The two workers are independent. They should not read or modify one another's result files before reconvening.

## Return files

Each worker returns exactly:
- `RESULT.md`
- `RESULT.json`

inside its own cell.

## Reconvening

After both returns, Vozhd Dva compares:
- upstream availability;
- downstream demand;
- proposed lawful V553 intake;
- proposed V553 transformation;
- reachable output envelope;
- required V553→V554 contract.

The authoritative ruling is written to:

`schematics/synthesis/S00_V552J_TO_V553_RULING.md`

No worker-local object grain, co-input classification, or schema proposal is Rawlsing law before that ruling is written.

## Exit condition

S00 is complete only when Vozhd Dva freezes:
- the complete upstream availability map relevant to V553;
- the actual V554 demand map;
- the lawful V553 intake composition;
- which authority must arrive through V552J versus direct co-input/context;
- the V553-specific authorized temporal operation;
- the V553 reachable output envelope;
- the minimum semantically complete V553→V554 output contract;
- preserve/derive/reformat/aggregate/drop/forbid/unresolved law;
- concrete current seam/reach-back defects;
- implementation obligations and tests;
- the exact accepted V553 output contract that becomes S01's upstream input law.
