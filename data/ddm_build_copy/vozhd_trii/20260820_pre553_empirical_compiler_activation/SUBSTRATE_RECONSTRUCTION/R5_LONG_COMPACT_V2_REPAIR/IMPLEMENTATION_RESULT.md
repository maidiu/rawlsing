# R5 LONG_SHARDED COMPACT V2 repair implementation

Status: `IMPLEMENTED__TARGETED_PHYSICAL_REPAIR__EXACT_REPOSITORY_AND_REAL_WVS_PREFIX_COURT_PENDING`

Exact starting HEAD: `46a9d35d0edecc7dc9182038baeb0d0748c50fdc`

Frozen failed V1 implementation: `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`

WVS7 failure witness: `3f39e6af83c7fd7cea600c9c7822dfee3ec13230`

Compact V2 implementation/test head before this receipt: `b643ea6ea08a6ed29e31453135ac9113286d581d`

## Repair scope

The repair is additive and confined to Authority-63 physical representation/testing surfaces:

- `rawlsing_next/pre553_r5_compact_carrier.py`
- `rawlsing_next/pre553_r5_compact_shadow.py`
- `rawlsing_next/pre553_r5_compact_density_court.py`
- `rawlsing_next/test_pre553_r5_compact_carrier.py`
- `rawlsing_next/test_pre553_r5_compact_shadow.py`
- `rawlsing_next/test_pre553_r5_compact_frozen_integration.py`

No V1 file, decoder, C11 semantic/integrity/repository module, I03, I05, I04, V553+, V3 or V2 file was modified.

## Failed mechanism removed

V1 wrote one self-describing canonical JSON object per physical cell, repeating row schema, relation, object family, deterministic object id, hex content hash, source identity and coordinate material. WVS7 crossed 4 GiB after only 5,327,336 physical cells.

Compact V2 preserves the exact reconstructed `R5CanonicalRow` but gives `source_physical_cells` a specialized physical lane. It stores the irreducible/retained physical-cell fields, while reconstructing:

- fixed relation and family;
- object id from exact source SHA + row ordinal + variable ordinal;
- explicit source-coordinate tuple from the exact row/variable ordinals;
- content hash from the exact reconstructed canonical payload.

Generic non-cell relations retain an exact generic escape representation.

Independently closed members and external sort runs are compressed with deterministic gzip framing. Root/inventory/member whole-byte integrity remains flat and content-addressed; logical member/global digests are computed over the full reconstructed V1-equivalent canonical row projection rather than compressed bytes.

The compact inactive publication path reuses the existing generation-stamped CAS/serving-law semantics and changes only the builder/reader pair.

## Non-dispositive local mechanical evidence

HQ's execution container does not provide `pyreadstat`, so it cannot honestly execute the frozen `decode_sav` real-source gate locally.

A local mechanical prototype of the same compact physical-cell scheme nevertheless established before publication:

- exact row reconstruction/audit smoke: PASS;
- duplicate exact identity rejection: PASS;
- whole-member corruption rejection: PASS;
- same-config input-reorder determinism: PASS;
- WVS-shaped hostile synthetic 10,000-cell sealed density: approximately `13.62 B/event`;
- WVS-shaped hostile synthetic 100,000-cell sealed density: approximately `13.45 B/event` in the development prototype.

These measurements are deliberately NON-DISPOSITIVE. Authority 63 still requires the exact repository test court and actual WVS `.sav` prefix measurements at 250k / 1M / 2M before any full-source authorization.

## Required next gate

Run the frozen exact-repository validation against implementation head `b643ea6ea08a6ed29e31453135ac9113286d581d` without modifying candidate code. Then run `pre553_r5_compact_density_court.py` against exact WVS source SHA at 250k, 1M and 2M physical-cell checkpoints.

If any candidate change is needed, return the minimal witness to HQ. Do not repair inside the validation cell.
