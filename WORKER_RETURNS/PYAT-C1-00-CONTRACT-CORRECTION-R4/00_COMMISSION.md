# PYAT C1-00 — EXACT UNKNOWN-CURRENTNESS KEY SYNCHRONIZATION — R4

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser GPT-5.6 Sol High documentary exactness corrector

Branch:
`agent/rabochii-pyat-hq126-c1-00-contract-correction-r4`

Exact base / R3 return head:
`696210c2aca2c42b49eed1fe9f75dfca5bf2e93c`

R3 commission tip:
`e50bc716cf0fd017081e351a5803d3da61a00a38`

Implementation baseline owner:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

## HQ finding

R3 is not yet fit for independent rereview because the same frozen UNKNOWN_CURRENTNESS SelectionKey is represented by two incompatible exact refs.

Current R3 correction artifact:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/03_UNKNOWN_CURRENTNESS_FIXTURE.json`

freezes:

`B5Lifecycle:SELECTION_KEY | 53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`

But the current C1 packet freezes:

`B5Lifecycle:SELECTION_KEY | a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

in at least:
- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
- R3 return prose.

The R3 recomputation receipt does not independently recompute the owner-native SelectionKey ref.

This is a bounded documentary propagation/exactness defect. It does not reopen B/C/D semantics and does not authorize C1-01.

## Mission

Determine the single exact owner-native SelectionKey.ref for the frozen R3 UNKNOWN_CURRENTNESS fixture under the current B5 owner, then propagate that exact identity consistently across the current C1 packet.

Do **not** assume either `53683ac...` or `a0c54c...` is correct merely because it already appears in the packet.

Independently derive the exact ref from the current owner law:

`rawlsing_next/pre553_learned_product_lifecycle.py`
baseline blob:
`a11c9eb73abab9be118ef4f0b6e325e676059f27`

The governing owner code is:
- `SelectionKey.semantic_projection()`
- `SelectionKey.ref -> _record_ref("SELECTION_KEY", semantic_projection)`
- `LearnedProductLifecycleExecutor.selection_key(...)`

Use the exact frozen R3 input refs and `consumer_context_partition_ref=None`.

## Required correction

1. Independently recompute the exact owner-native SelectionKey ref from the frozen semantic projection.
2. Record:
   - exact semantic projection;
   - exact canonical material used by the owner's ref law;
   - recomputed SHA-256;
   - resulting `ExactRef`;
   - comparison against both existing candidate hashes.
3. Freeze exactly one as correct and classify the other as stale/wrong.
4. Propagate the correct ref to every current C1 artifact that claims this fixture's exact SelectionKey identity.
5. Add an explicit SelectionKey-ref recomputation check to the current R4 recomputation receipt.
6. Recompute any downstream documentary identity that actually embeds the corrected SelectionKey ref. Do not churn unrelated hashes.
7. Make current return/bookkeeping exact.

## Preserved accepted material

Do not alter:
- R3-B owner-native query-authority source scope except if a downstream identity mechanically embeds the corrected key, which is not expected;
- R3-D noncircular evidence identity except if a genuine dependency mechanically requires it, which must be demonstrated;
- accepted R2 A;
- accepted R2 E;
- all prior preserved holdings;
- production code/tests;
- raw-source status.

Do not modify historical R2/R3 review-return directories.

## Write terrain

May modify only current C1 packet files under:

`WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**`

where necessary to propagate the corrected key.

May add only:

`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/**`

Do not modify:
- production code;
- production tests;
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/**`;
- prior reviewer directories.

## Required R4 return

Under `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/**` return:

- `00_RETURN.md`
- `01_SELECTION_KEY_IDENTITY_RECOMPUTATION.json`
- `02_PROPAGATION_AUDIT.json`
- `03_UPDATED_BLOB_MANIFEST.json`

Report:
- exact final branch head;
- exact correct SelectionKey ref;
- exact stale/wrong ref;
- every current C1 artifact containing either ref after correction;
- all changed blobs;
- raw source reads = 0;
- C1-01 execution = none.

After R4, stop. Fresh independent rereview remains mandatory before HQ may freeze C1-01.

Terminal target:

`C1_00_R4_EXACT_SELECTION_KEY_SYNCHRONIZATION_READY_FOR_INDEPENDENT_REREVIEW`
