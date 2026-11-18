# SRC04 admission boundary

## Verdict

**`NOT_COMPATIBLE__EXACT_CURRENT_ADAPTER_AND_Q2_INPUT_BUNDLE_MISSING`**

No executable source build command is available yet. Starting from this state
would not be a lawful `build_source_i02_handoff` build.

## Existing grant and accepted reference

The human grant is present and exact:

- Path: `campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json`
- Commit: `303a57851785557fff8229e29a5554717168cbd1`
- SHA-256: `d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139`
- Issuer: `HUMAN_USER_VIA_EXISTING_PYAT_HQ`
- Source: SRC04, `2a48ba4b…`, 7,337 rows, 181 columns
- Host/purpose: `USER_LOCAL_MAC` / `FULL_SRC04_ORIGINAL_C11_CONSTRUCTION`
- Consumer: `EXISTING_PRE553_SOURCE_BACKED_C11`
- Currentness: `CURRENT_GRANTED`; revocation: `NONE_RECORDED`
- Full source/181 slots; not first slice

The accepted C11 reference at `ba41253681212be14a0cde009afb99d77e14935e`
has the accepted scoped census: 7,337 rows, 177 selected responses, 3
coordinates, 1,298,649 response positions, q217 held at 38 unbound cells.

## Why it is not directly compatible

Current accepted code `aee954…` defines the
`SourceReadDecisionResolver` protocol but has **no concrete current adapter**.
The historical `FullGrantResolver` exists only in the 303a campaign runner and
imports the absent historical `rawlsing_next.source_configuration` package. It
is not a current accepted ANVIL resolver.

`build_source_i02_handoff` additionally requires, for the original source:

- exact `SourceConfig`;
- `FrozenInputCensus`;
- `SourceInventory`;
- `GrammarPolicy`;
- `ScientificFrontier`;
- `SourceSavedBodySink` transport.

The human full-source grant supplies none of those Q2 census/frontier inputs.
The accepted C11 release reference is not a Q2 `FrozenInputCensus`, inventory,
policy or frontier.

First refusal at the builder: `SOURCE_READ_RESOLVER_REQUIRED` for the original
binding. Even after a resolver adapter, the missing Q2 input bundle remains.

## Source config pin

Historical repaired-v2 config:

- `rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json`
- file SHA-256 `5e107de4…`
- canonical SHA-256 `28630f26…`
- pinned commit `da23c65d…`

This is not present in the current accepted tree.

## Smallest conservative wiring from the existing grant

No new grant is minted.

1. A **harness-only adapter** revalidates the exact grant path/SHA and maps the
   existing human grant to `IssuedSourceReadDecision`, with the exact request:

```text
source_id = SRC04
source_sha256 = 2a48ba4b…
source_format = SAV
custody_locator_binding = exact source.config identity.locator binding
host = USER_LOCAL_MAC
purpose = FULL_SRC04_ORIGINAL_C11_CONSTRUCTION
consumer_use = EXISTING_PRE553_SOURCE_BACKED_C11
read_operation = SOURCE_RESPONSE_DECODE
physical_read_extent = EXACT_FILE
metadata_freeze_refs = exact config metadata witness
semantic_use_scope =
  SOURCE_NATIVE_RESPONSE_INCIDENCE
  NO_SEMANTIC_ADOPTION
  SRC04
  FULL_SRC04_C11_CONSTRUCTION
currentness = CURRENT_GRANTED
revocation_ref = None
retention/export = local only; respondent data outside Git/stdout;
                   nonidentifying aggregates only
```

2. Load the exact repaired-v2 source config from the read-only 303a/B snapshot
   at the pinned path/hash.

3. Supply or construct the exact SRC04 `FrozenInputCensus`, `SourceInventory`,
   `GrammarPolicy` and `ScientificFrontier`. These are the decisive missing
   inputs; they are not inferred from the grant or C11 release.

Only after those exist can `build_source_i02_handoff` with
`SourceSavedBodySink` produce one build and permit a cold reopen.

## Competent boundary

- Source read/C11 construction: `HUMAN_USER_VIA_EXISTING_PYAT_HQ` (existing
  303a grant).
- Q2 operation/fate/frontier and scientific operation authority: the existing
  Pyat HQ/user scientific boundary; not supplied by the source-read grant.
- No new grant, no TEST_ONLY relabel, no source science or respondent values.

## Limits

No raw source opening/reading/hashing, no source build, no respondent values,
no heavy benchmark, no product edit, no new grant.

Own return: `WORKER_RETURNS/ANVIL_SRC04_ADMISSION_20261118/`.

**STOP at the prerequisite; no source-build command yet.**
