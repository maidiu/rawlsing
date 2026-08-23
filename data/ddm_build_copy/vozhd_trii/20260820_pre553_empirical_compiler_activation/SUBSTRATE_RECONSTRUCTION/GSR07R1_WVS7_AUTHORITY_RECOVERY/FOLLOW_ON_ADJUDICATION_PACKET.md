# G-SR07-R1 — SMALLEST LAWFUL WVS7 FOLLOW-ON ADJUDICATION PACKET

Status: `PROPOSED__DO_NOT_EXECUTE_IN_GSR07R1`

This packet is intentionally smaller than a 613-variable semantic re-review. Accepted FQRA R1 already supplies one governed semantic-disposition row for every WVS7 source slot. The remaining work is to bridge that authority into the C11 object model, close routing/risk sets, and recover country universe/design documentation.

## Packet A — C11 ownership bridge

Input:
- exact 613-row WVS7 subset of FQRA R1;
- accepted R14 topology;
- existing QRA/V550/V551/manual response-semantics bindings;
- C11 `QuestionVariableBinding`, `RespondentEvent`, `EmpiricalCoordinateFact`, `EmpiricalUniverse`, and `WeightMeasureFact` contracts.

Required output:
- one exact governed binding per WVS7 source slot, expressed preferably by stable accepted authority class plus exact exceptions, to:
  - `RespondentEvent`;
  - `EmpiricalCoordinateFact`;
  - `EmpiricalUniverse` / identity / provenance input;
  - `WeightMeasureFact`;
  - explicit nonparticipating / excluded source slot.

Forbidden:
- re-deciding FQRA meaning;
- inferring C11 ownership from a role label merely because it is machine-readable;
- resolving Q3/Q48 structural coordinates by convenience.

Q3/Q48 may retain downstream structural coordinates as typed UNKNOWN/fail-closed while source-native/C11 identity is separately bound.

## Packet B — routing/risk-set authority

Bank:
- master questionnaire explicit filters;
- selected-country Political Trust module;
- Middle East module country scope;
- Q294 50/50 form split;
- accepted R14 person-position/applicability facts;
- source semantic `-3`/`-4` distinctions.

Recover:
- country questionnaires/technical reports only where country omission/module/form scope is not already positively closed.

Manual adjudication:
- encode the distinct positive routing-rule families/scopes as governed C11 routing rules;
- never infer routing from physical missingness or response frequency.

Mechanical after adjudication:
- construct exact `risk_set_ref` and `member_set_replay_ref` identities from accepted rules + exact source-row/country/form facts.

## Packet C — country EmpiricalUniverse authority

Use the exact source-present country inventory and retrieve the corresponding official WVSA Wave-7 country technical/methodological records.

For each source-present country freeze:
1. target population / coverage and documented deviations;
2. sample frame;
3. actual sampling design regime;
4. PSU / strata / cluster / route details needed by any claimed design use;
5. exact document identity and scope.

The WVS wave-level rules are already banked as baseline authority. They do not replace country-specific documentation.

Official documentary index:
`https://worldvaluessurvey.org/AJDocumentation.jsp?COUNTRY=&CndWAVE=7`

## Packet D — claim-scoped weight/design authority

Bank without further adjudication:
- `W_WEIGHT` sociodemographic-adjustment purpose;
- `S018 = 1000/sample size` equal-country purpose;
- documented `W_WEIGHT * S018` equal-country combined purpose;
- `I_PSU` source meaning;
- no universal/default weight.

Do not invent:
- a default weight;
- a variance estimator;
- a query-to-weight binding beyond the exact source-documented purpose.

Only if a production/frozen-I03 profile actually claims a weighted/design estimand:
- adjudicate that exact query/estimand -> weight/design binding and recover the needed country design documentation.

## Packet E — mechanical WVS7 projection/replay closure

After A-C and any actually claimed D work close:
- content-address all accepted authority inputs;
- create the exact WVS7 projection/replay authority snapshots/refs;
- use `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`;
- rerun G-SR07 source-specific certification.

No new semantic interpretation is authorized in Packet E.

## Smallest critical path

`A C11 ownership bridge + B routing rules + C country universe/design documents -> E mechanical projection package -> G-SR07 relaunch`

Claim-scoped D may run only if the proving release actually asks for weighted/design semantics.

`MACHINE_READABLE_AUTHORITY != MACHINE_DERIVABLE_AUTHORITY`.
