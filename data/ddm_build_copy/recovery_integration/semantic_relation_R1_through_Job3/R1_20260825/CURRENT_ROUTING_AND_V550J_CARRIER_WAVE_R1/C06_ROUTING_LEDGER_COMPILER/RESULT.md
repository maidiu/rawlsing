# C06 — CURRENT 18,276 ROUTING LEDGER COMPILER / COVERAGE VALIDATOR R1

Status: `COMPILER_VALIDATOR_IMPLEMENTED__NO_SOURCE_AUTHORITY_DECISIONS`

Repository: `maidiu/rawlsing`

Worker branch: `agent/verkhovod-c06-routing-ledger-compiler-r1`

Verified starting HEAD: `2a733b78d63f6582acfd1ec68c0ef87cca5a8faa`

Governing authority:
- Authority 45 blob: `44edd0f87da778a2c08e33869a129e5a36830bbc`
- Authority 44 correction blob: `a301e4c8fe0aa08f9c462228130d078099c06dcf`

Exact tested implementation commit:
`1c657b984406695e57a1790ad9590d7de4caf417`

## Holding

C06 implements the deterministic current routing/applicability ledger compiler and coverage validator only.

It makes **zero source-authority decisions**.

It does not decide whether any real current implementation is:
- unconditional/general;
- positively routed;
- scoped nonapplicable;
- administrative/nonrespondent;
- unresolved.

Those dispositions must be supplied by future authorized source-family adjudication ledgers.

## Exact current catalog binding

The compiler is pinned to the HQ-joined governed Layer-1 current implementation catalog:

- archive: `LAYER1_GOVERNED_35WAVE_CATALOGS.zip`
- archive SHA-256: `b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d`
- active implementations: **18,276**
- active scopes: **35**
- source families: **9**

Exact family file bindings:

| Source family | Rows | Catalog SHA-256 |
|---|---:|---|
| GSS | 6,021 | `74496af09f5feba9defc1d2991977e79343da97c87c1fce93f1e9ab4ada31b99` |
| LiTS | 4,434 | `068cd24a9bcbaaf0e8b70c6c384296884247467f09fd380753d941e09afd39ea` |
| EVS | 2,224 | `61c6f77d266e59f5218babecbd07636619ff90d04b4ffc837357204225729d3b` |
| Arab Barometer | 1,698 | `1111699fdde0bbd082267b1ba5eb3b76bbfdcf89aa1e08f500c8393200c394cf` |
| WVS | 1,219 | `cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0` |
| Afrobarometer | 913 | `01561b89960c10a77cec15552a8b065a0d043fe29c99bc77f4cb316991225181` |
| Asian Barometer | 814 | `b27afc4e1ba8bd5707db61388b592525467657d522e782a07c31d04d6b4430cd` |
| Latinobarómetro | 812 | `9993607de206a00ed1d6c63b599e5115dc0c1925bffcb10a81544eadaf83cf8c` |
| South Asia | 141 | `1e31a8bc40a76a921668497ad8268e4d048c5c19e65003d44424a89b5a4f73f1` |

The nine family counts sum exactly to **18,276**.

The repository's 700-row QRA trial surface is not accepted as a current routing catalog and is never used by the compiler as membership authority.

## Implemented disposition schema

Exact Authority-45 disposition vocabulary:

1. `GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE`
2. `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`
3. `GOVERNED_SCOPED_NONAPPLICABILITY`
4. `ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT`
5. `STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT`

Every adjudication row must bind:
- exact current `question_implementation_id`;
- SHA-256 of the exact normalized current catalog row;
- source family, canonical wave, source variable;
- country/form/module/split scope where present;
- member-applicability scope;
- source-universe/filter scope;
- exact disposition;
- evidence authority type/ref/hash and evidence scope;
- exact membership basis;
- predicate/replay contract when executable;
- unresolved blocker class when unresolved;
- adjudication provenance ref/hash.

Required membership basis:

`EXACT_CURRENT_IMPLEMENTATION_CATALOG_ID`

## Coverage law

For each family ledger:
- every current family implementation must appear exactly once;
- duplicate IDs fail;
- extra/non-current IDs fail;
- cross-family IDs fail;
- catalog-row hash drift fails;
- family/wave/variable/scope drift fails.

For the joined ledger:
- all nine family ledgers must be present;
- total coverage must be exactly **18,276**;
- family counts must equal the Authority-45 counts;
- no missing/duplicate/extra current implementation identity is accepted.

## Predicate and replay law

`POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` requires:
- explicit predicate contract version;
- JSON-object predicate serialization;
- exact canonical predicate SHA-256;
- explicit replay contract version;
- replay input/reference.

All other dispositions are forbidden from carrying executable predicate/replay semantics.

The compiler does not generate or interpret predicate meaning.

## Scoped nonapplicability law

A nonapplicability row must remain bound to:
- the exact current implementation identity;
- exact family/wave;
- exact catalog scope where the catalog specifies country/form/module/split;
- the supplied evidence scope.

Widening tokens such as `ALL`, `GLOBAL`, `*`, or equivalent are rejected on scoped-nonapplicability evidence/member/universe scopes.

This widening restriction is not applied to governed general/unconditional rows; C06 does not reinterpret a lawfully supplied general universe as nonapplicability.

## Typed unresolved law

`STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT`:
- requires an explicit blocker class;
- may preserve a partial evidence ref only when both exact ref and hash are present;
- cannot contain executable predicate/replay semantics;
- is never converted by the compiler into unconditional, routed, nonapplicable, or administrative.

## Historical-denominator hostile rejection

The validator explicitly rejects these membership bases:

- `HISTORICAL_700_TRIAL_SET`
- `HISTORICAL_99_SOURCE_SIGNALED`
- `HISTORICAL_600_LMQ004`
- `HISTORICAL_699_UNRESOLVED`
- `AGGREGATE_COUNT`
- `SOURCE_COLUMN_PRESENCE`
- `INFERRED_COMPLETION`
- `QUESTION_TEXT_OR_THEME`
- `NEIGHBORING_WAVE_ANALOGY`

Thus old trial membership, aggregate equality, source-column existence, wording/theme, or inferred completion cannot satisfy current coverage.

## Deterministic fixture hashes

The native test fixture supplies all dispositions explicitly; C06 invents none.

Across reordered input family mappings the compiler reproduces:

- joined-ledger semantic SHA-256:
  `97e96e539c1e328ade142d559ed336597d29b1ec3a7ebc512437e5df7392f39c`
- unresolved-summary SHA-256:
  `58520955874699f896f2afb429dddc6d133bffb1b60784924a73429f462397f1`

Fixture unresolved count: **4**, preserved by family/blocker class.

## Test receipt

Hosted run:
- workflow run: `33240338272`
- job: `99068478664`
- Python 3.12
- pytest 9.1.1
- result: **22 passed in 0.13s**

No real 18,276-row routing disposition ledger was emitted because no authorized C02-C05 source-family adjudication results were consumed and C06 is forbidden to invent dispositions.

## Files implemented

- `rawlsing_next/current_routing_ledger.py`
- `rawlsing_next/tests/test_current_routing_ledger.py`
- `data/ddm_build_copy/authority/current_routing_ledger_contract_v1.json`

## Sibling blindness / negative ceiling

C06 did not consume C02-C05 results.

C06 did not:
- decide source authority;
- transform missing evidence into semantic disposition;
- use the historical 700/99/600/699 partitions as modern membership;
- perform V550J work;
- perform architecture work;
- perform V3 work.

Prior A07 material was consumed only through the Authority-44/45 HQ-joined chain of custody to recover the exact governed current catalog file identities/hashes.

## Return

`C06_CURRENT_ROUTING_LEDGER_COMPILER_R1_COMPLETE`
