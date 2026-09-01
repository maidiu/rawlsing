# FFIF002 — SPECIAL STATE SEPARATION LAW R1

## Law

`COMPUTATIONAL NA IS NOT A SEMANTIC STATE.`

Rawlsing must preserve distinct source/data-generation states even when a runtime library represents several of them with the same missing-value sentinel.

At minimum, the semantic substrate must be able to distinguish:

1. `DK` — respondent could answer / was asked but reports not knowing;
2. `REFUSED` — respondent was asked but declines an answer;
3. `NOT_ASKED` — instrument or sample design did not ask this respondent/item;
4. `ROUTED_NONAPPLICABLE` — routing logic lawfully determines the item does not apply;
5. `NOT_IN_FORM` — the item does not exist in the administered form/wave/instrument;
6. `UNRESOLVED_ROUTING` — current authority cannot determine whether observed absence is explained by routing;
7. `SUBSTANTIVE_MISSING` — a distinct source-recognized missing/invalid response condition not reducible to the above.

## Numeric special codes are local encodings

Values such as `8`, `9`, `98`, `99`, `-1`, or blanks never have universal semantic meaning.

Code may decode a numeric special state only from explicit source/codebook/form authority at the correct scope. Numeric pattern matching is not semantic authority.

## No inference from missingness alone

A blank/null observation does not prove:

- nonapplicability;
- routing;
- refusal;
- don't know;
- item absence;
- respondent absence;
- substantive missingness.

Without form/routing/source provenance, the correct state may be `UNRESOLVED_ROUTING` or another explicitly unresolved disposition. Runtime must not repair uncertainty by choosing the most convenient missing type.

## No project-wide NA collapse

The common observation substrate must retain typed state identity/provenance beneath any computational missing representation.

A method may later exclude or map special states only when:

- the transform/exclusion is explicitly authorized;
- source-native special-state ancestry remains recoverable;
- information loss is declared;
- the downstream claim is compatible with that loss;
- for FFX002 common-input comparison, semantic eligibility/exclusion is frozen identically before the fork if it changes the empirical universe.

## Distinct substantive consequences

The states differ because they arise from different processes:

- `DK` may itself describe uncertainty or knowledge distribution;
- `REFUSED` may reflect sensitivity, distrust, risk, or survey interaction;
- `NOT_ASKED` describes instrument/sample design;
- `ROUTED_NONAPPLICABLE` encodes a prior substantive condition and routing logic;
- `NOT_IN_FORM` encodes instrument history rather than respondent response;
- `UNRESOLVED_ROUTING` encodes an authority gap;
- `SUBSTANTIVE_MISSING` encodes a source-defined response/data state.

Collapsing them does not merely lose metadata. It changes what empirical events are said to have occurred.

## Law for representation methods

No representation may define its own upstream missing ontology while still claiming to consume the same common input.

Permitted post-fork behavior:
- a method may be unable to use one or more frozen special states and exclude them under a method receipt;
- a visualization may display or suppress special states for legibility while retaining them in provenance;
- sensitivity analysis may compare multiple authorized treatments.

Not permitted:
- geometry silently maps DK/refused to one category while atlas treats them separately and both outputs are called a duel on the same semantic input;
- a representation reinterprets `UNRESOLVED_ROUTING` as `ROUTED_NONAPPLICABLE`;
- special-state numeric codes enter metric distance as ordinary quantities.

## Source-native versus project-created missingness

If the source itself only supplies one undifferentiated missing code, Rawlsing records that exact source-native state and its limitation. It must not invent distinctions the source cannot support.

If Rawlsing itself creates an analytic missing/exclusion grouping, that grouping is downstream, lossy, claim/method-scoped, and ancestry-reversible.

## Terminal rule

`SPECIAL STATES REMAIN SEPARATE UNTIL AN EXPLICIT SCOPED AUTHORITY PERMITS A DOWNSTREAM TREATMENT; NO DOWNSTREAM TREATMENT ERASES THEIR SOURCE-NATIVE ANCESTRY.`