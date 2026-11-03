# Real source metadata binding — SRC04 Arab Barometer Wave 1

**Base:** `6949efbc3bb17d1ee2b00c9c0935f921a6a93fd8`
**Branch:** `agent/pyat-pdev01-gap007-sourcefree-r1`
**Metadata origin:** `agent/pyat-pre553-r157-integration@056849e23`
**Mode:** TEST_ONLY sourcefree metadata binding; no original source read.

## Result

The existing R157 source-configuration package and actual C11 owner now bind the
real SRC04 Arab Barometer Wave 1 metadata without the synthetic `Q00A/Q00B`
fixture assumptions.

- Real edition: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- Rows / columns: `7337 / 181`
- Source config canonical SHA: `0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284`
- Source config file SHA-256: `eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900`
- Crosswalk: `034d626365249941618d66f6103a557209fce5d95362e3ddf77e29f2fe7fba23`, 181 exact-name entries
- Codebook: `8ad1af17b782d1ff3beb84c2d2331977195ac3bb48dbcc94a94a08ca725b288f`, 181 rows
- Directionality authority: `a071c8896a63a8fe7109a33159ba38dd870324169a1915331b45464cb152c039`, 181 rows (122 CERTIFIED / 59 NOT_CERTIFIED)
- Response-option authority: `5ef7a0e9da60c7c39eda494dd4a8684a2d7bfdd3714d55c91445afa82e1b1f15`, 12,160 rows
- Existing C11 validation receipt: `c008704857b415e1a4515e55ae417097836fa37d628a0e521e9715d839fe5ee7`, status PASS

## Actual existing-owner calls

Crosswalk and caller were found before writing:

- Crosswalk: `rawlsing_next/source_configuration/data/SRC04/crosswalk.json`
- Actual C11 caller: `rawlsing_next.source_configuration.factory.build_governed_c11_projection`
- Actual native validator: `rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config`
- R03 normal key entrypoint: `rawlsing_next.universal_grammar.types.OccurrenceKey`

Observed C11 result from the real original metadata projection:

- Projection ref: `60206b998f89711801fa689283c20a6589281b77575a5ab002ad7c8cf23a51a8`
- Respondents: 7,337
- Questions / response slots: 178 / 178
- Coordinate slots: 3
- Routing facts: 1,305,986
- Original source read: **false**

The C11 fixture release, built only from the declared nonrespondent fixture,
matches the prior C11 engineering receipt:

- Release: `9026fa33bb5739b87b06309f12e1d31fe6fd21fb471237eda870d6d278d47f42`
- Public objects: 2,880
- Fixture source: `506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b`
- Existing validation release match: **true**

## Trace and gates

| Field | Result |
|---|---|
| Edition | exact source SHA/row/column metadata |
| Item | 181 configured items; exact config/crosswalk names |
| Option | 178 configured response slots; 12,160 option-authority rows |
| Form/repeat | accepted 42-slot slice is single interview-row: `form_id=None`, `repeat_id=None`; no fabricated form identifiers; not an estate-wide claim |
| Route | **not exact**; selected 42 routing entries remain `ROUTING_UNKNOWN` |
| Eligibility/risk set | **not exact**; selected 42 risk-set refs are unresolved |
| R03 policy/direction grant | **absent**; no policy supplied or fabricated |

R03 candidate keys were constructed for 178 configured response items through
the normal `OccurrenceKey` entrypoint, but they are item-only candidates. No R03
inventory, policy or execution was accepted or created.

## First exact input missing (corrected per review)

**Artifact:** exact questionnaire routing/skip rule and risk-set/eligibility
denominator handoff for the accepted SRC04 42-slot slice.

**Question:** `q101` is the first selected field; the same state applies to all
42 selected fields.

**Fields:** `routing[].typed_state`, `routing[].routing_rule_ref`,
`routing[].risk_set_ref`, `risk_set_refs`.

**Owner:** ARAB lane / P3 integration owner named in the SRC04 exception ledger.

Current evidence: all 42 selected routing entries are `ROUTING_UNKNOWN`, all 42
risk-set refs are unresolved, and no exact skip rule is present. The accepted D1
tally provides source-record/event denominators and response-state counts, but
not an eligibility denominator or a routed-out category. The downstream missing
artifact is an exact R03 `GrammarPolicy`/authorized direction grant, owned by the
R03 policy/direction owner. No policy or routing is inferred from observed
counts or labels.

Correction receipt: `04_ROUTING_CORRECTION.json`. The form/repeat null shape is
scoped to the accepted single-SAV/source-interview-row 42-slot slice; it is not
an estate-wide absence claim.

## Tests

`test_metadata_binding.py`: **4 passed** in 0.03s.

## Limits

- No original SAV/DTA or respondent rows were read.
- No restricted labels or question text are reproduced in this receipt.
- No original workload was issued and no R03/C11 execution was performed.
- No production edit, policy fabrication, merge or CI.
- The C11 fixture release is nonrespondent fixture engineering evidence, not an
  original-source empirical result.
- This binding is generic over input paths; no per-wave source literal is used
  by the executable adapter.

**Distinct nonauthor review is required for the positive C11 metadata-binding
claim.**

## Review correction

Independent review `bdeace786` corrected the original form/repeat-first-missing classification. The accepted 42-slot slice has form/repeat null; routing/eligibility/risk-set is the first genuinely unresolved input. See `04_ROUTING_CORRECTION.json` and `routing/`.
