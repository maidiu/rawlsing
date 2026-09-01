# BOUNDED CURRENT WITNESS

Witness type: `BOUNDED_NEGATIVE_IDENTITY_WITNESS`

This witness does **not** execute FFX002 and does not infer empirical non-exposure. It tests whether one exact current routing object can be carried all the way to one governed respondent row.

## Selected current object

- family: `Afrobarometer`
- wave/release: `R5`
- qimpl: `question_impl.phase0.391123a4e7d3c8f0fd3b`
- raw variable: `Q73D`
- question identity: `Afrobarometer:R5:Q73D`
- current routing disposition: `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`
- decision detail: `native_country_plus_employment_eligibility`
- predicate: `C04P.f751f53c113a339f2cb8`
- predicate specification: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`
- evidence grade: `NATIVE_PRIMARY`

C04's positive predicate has deterministic hostile-positive, hostile-negative, and replay proof at predicate-specification grain. Thus routing is not the missing object.

## Attempted current row proof

Required respondent witness fields:

1. exact current respondent carrier identity/hash;
2. exact respondent key;
3. respondent's exact Afrobarometer R5 source/scope identity;
4. row-bound Q73D measurement identity;
5. row value for `COUNTRY_ALPHA3`;
6. row value/authorized derived value for `RESPONDENT_HAS_PAID_EMPLOYMENT`;
7. deterministic predicate result;
8. actual Q73D measurement exposure/opportunity;
9. response value/state, if separately present.

This court found current authority for the qimpl, source variable, routing disposition, and predicate specification, but **not** items 1–6 as a single governed current respondent carrier/binding. Therefore items 7–9 cannot lawfully be materialized.

## Witness ruling

`NEGATIVE_BRIDGE_WITNESS__CURRENT_ROUTING_REAL__CURRENT_RESPONDENT_BINDING_NOT_PROVED`

Nothing here says a historical Afrobarometer R5 respondent lacked Q73D, employment eligibility, or a response. The failure is current identity/carrier authority.
