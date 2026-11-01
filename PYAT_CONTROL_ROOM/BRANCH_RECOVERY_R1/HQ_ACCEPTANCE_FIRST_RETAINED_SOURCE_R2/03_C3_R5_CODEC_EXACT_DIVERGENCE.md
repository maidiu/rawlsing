# RRIF narrowed residual — C3 R5 accepted codec vs CURRENT PRE-MAIN

**Status:** `EXACT_SOURCE_ABI_DIFFERENCE_DEMONSTRATED__FUNCTIONAL_SUCCESSOR_NOT_ADJUDICATED`. The historical sourcefree C3 acceptance under `HQD-2026-09-30-131` is **not revoked**; current-source retention at the same functional scope is still at issue.

## Exact evidence

- Accepted C3 review/integration commit `30686b185d4ceb2c94f61815ef70d8c8e76255d6`, `rawlsing_next/pre553_r5_codec.py`, Git blob `6000a1704d713f65e07610d81e9b3fd8bdd515ca` (275 lines when displayed).
- CURRENT PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`, same path blob `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` (231 lines displayed).
- Both preserve `R5CodecError`, `R5OpaqueValue`, `R5TypedValueCodec`, `canonical_json`, `canonical_bytes`, float-bits and Decimal helpers.
- The historical C3 codec **also exports and implements** `opaque_decoder_value(value)` and `normalize_decoder_physical_value(value)` and imports Python `datetime` globally. The present codec **does not contain these two definitions or exports**.
- Historical behavior: exact opaque byte wrapping for built-in naive `datetime.datetime`, `datetime.date`, `datetime.time`, preserving timezone-aware refusal and fold; recursive normalization through tuple/list/mapping. It returned `R5OpaqueValue(type_id, payload)`, not an invented calendar meaning.
- The current `R5TypedValueCodec.encode` still handles **already wrapped** `R5OpaqueValue` and rejects naked date/time objects pending an explicit opaque decoder representation. Thus the omitted pre-normalization is a genuine *exposed helper/API difference* at this module, not proof that the current encoder silently corrupts dates. There may be another competent source-specific adapter elsewhere.
- Direct inspection of current `pre553_physical_decoder.py` and `pre553_source_native_preimage_adapter.py` found no definitions with those two exact names. This is not a repository-wide caller/behavior search; do not assert the capability absent from all alternative owners.

## Required smallest falsifiable successor test

1. Identify actual historical caller(s) and current first consumer of `normalize_decoder_physical_value` / `opaque_decoder_value` and any equivalent elsewhere. Do not resurrect code simply to preserve unused API.
2. Use legitimate sourcefree representative naive date/time values (including fold), nested list/tuple/mapping and timezone-aware negatives. Compare old C3 normalization + codec roundtrip against current qualified physical source-to-typed carrier path. Preserve exact byte identity and refusal.
3. If current same-grain successor is absent, repair only the actual missing adapter and demonstrate a real downstream receiver positive + severance/hostile negative, with distinct independent review.
4. Do NOT interpret date semantics, execute original survey code without permission, or treat the C3 acceptance as wholesale PRE-MAIN integration.

**Verdicts:** ENGINEERING `API_DIFFERENCE_CONFIRMED__LOSS_OR_REPLACEMENT_UNKNOWN`; SCIENCE `NO_SOURCE_NATIVE_DATE_SEMANTICS_ISSUED`; AUTHORITY `NO_CODE_CHANGE_OR_NATIVE_ADOPTION`.

This narrows C3/R9 residual work without dispatching a new all-845 archaeology shard.
