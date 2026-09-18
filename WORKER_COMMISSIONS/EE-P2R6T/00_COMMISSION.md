# EE-P2R6T — LARGE GOVERNED JSON GIT TRANSPORT PACKAGING

Repository: `maidiu/rawlsing`

## Execution surface

**BROWSER**

## Library access

**NO**

Do not access Library files, LiTS/WVS carriers, source bytes, empirical outcomes, or performance measurements.

Exact branch:

`agent/rabochii-prev3-ee-p2r6t-large-json-transport-packaging-r1`

Exact base:

`26d530c6ed762c4702845b7143c4ea91ae95cec7`

Before any work, resolve live canonical HQ through `HQ_HANDOFF/LATEST.json` and verify its immutable checkpoint packet.

## Trigger

EE-P2R6L-R2 completed local repaired verification and sealing successfully.

Reported local terminal:

`EE_P2R6L_PASS__ACCEPTED_I02_SUCCESSOR_RELEASE_MINTED_AND_VERIFIED__READY_FOR_CONCRETE_REALIZATION_BINDING_ISSUANCE`

Reported local commit:

`32cc3ab101104d33eb625176299d7dc09cf29190`

Push failed because:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_replay_manifest.json`

is approximately 113.02 MB and exceeds GitHub's 100 MB per-file push limit.

The local worker did not alter, split, compress, LFS-convert, regenerate, or otherwise mutate the governed output files after the failed push.

The remote R6L branch therefore remains at:

`26d530c6ed762c4702845b7143c4ea91ae95cec7`

The existing large JSON remains the single logical governed artifact and must remain byte-authoritative.

## Exact grain

`GOVERNED_LARGE_JSON_GIT_TRANSPORT_CHUNKING_AND_RECONSTRUCTION_ONLY`

This is transport/storage packaging only.

It is not semantic transformation.

It is not empirical rerun.

It is not permission to rewrite the JSON into several independent JSON documents.

## Mission

Prepare a deterministic, content-addressed Git transport representation for the oversized governed replay-manifest JSON while preserving the original logical artifact identity exactly.

The correct model is:

`ONE_LOGICAL_JSON_ARTIFACT -> BYTE_EXACT_TRANSPORT_CHUNKS + MANIFEST -> BYTE_EXACT_RECONSTRUCTION`

The original logical JSON's byte stream, byte length, SHA-256, and filename remain authoritative.

## Transport format

Use raw-byte chunking, not JSON-structural splitting.

Default chunk size:

`25165824 bytes` (24 MiB)

For a ~113 MB logical artifact this should yield approximately five chunks, each comfortably below GitHub's 100 MB file limit.

Chunk names must be deterministic and lexical-order safe, e.g.:

`successor_release_replay_manifest.json.part00000`
`successor_release_replay_manifest.json.part00001`
...

Do not depend on shell-specific `split` naming conventions.

## Required transport manifest

Prepare a manifest schema that binds at minimum:

- schema/version;
- logical artifact relative path;
- logical artifact filename;
- logical artifact byte length;
- logical artifact SHA-256;
- transport mode:
  `BYTE_EXACT_FIXED_SIZE_CHUNKS`;
- chunk size bytes;
- exact ordered chunk count;
- for each chunk:
  - zero-based ordinal;
  - deterministic filename;
  - byte length;
  - SHA-256;
- concatenation law:
  `CHUNK_BYTES_IN_ASCENDING_ORDINAL_ORDER`;
- reconstructed byte length;
- reconstructed SHA-256;
- statement that chunks are transport encoding only and are not independent semantic JSON artifacts.

The manifest itself must be small enough for normal Git.

## Required packager

Prepare a deterministic Python packager that:

1. accepts the path to one existing logical artifact;
2. opens only that file;
3. computes original size and SHA-256 before writing chunks;
4. writes fixed-size raw-byte chunks into a specified transport directory;
5. computes per-chunk size/SHA-256;
6. writes the transport manifest;
7. reconstructs to a temporary file from the chunks;
8. proves reconstructed size/SHA-256 exactly match the original;
9. deletes the temporary reconstructed copy after proof;
10. never mutates the original input file.

The packager must fail closed on partial writes, duplicate chunk names, unexpected pre-existing output files, or hash mismatch.

## Required reconstruction/verifier

Prepare a deterministic verifier that works without the original logical file being present.

Given only:

- transport manifest;
- chunk directory;

it must:

1. require exactly the declared chunk set and no extras matching the artifact chunk prefix;
2. verify every chunk size and SHA-256;
3. stream concatenated bytes in ascending ordinal order;
4. verify reconstructed logical byte length and SHA-256;
5. optionally reconstruct to a specified output path;
6. if reconstructing, refuse to overwrite an existing file unless an explicit safe flag is supplied;
7. verify the reconstructed output after writing.

## Git law

The oversized original file must **not** be committed to Git if doing so prevents push.

Instead, Git may contain:

- transport manifest;
- raw byte chunks;
- R6L governed return/receipt;
- the other three existing JSON outputs if each is under GitHub's limit.

The R6L governed receipt must continue to bind the original logical replay-manifest SHA-256 and byte length, not pretend a chunk is the replay manifest.

It may additionally bind the transport manifest SHA-256 and chunk set.

The historical logical artifact path remains:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT/successor_release_replay_manifest.json`

The Git transport representation should live under a deterministic sibling directory such as:

`WORKER_RETURNS/EE-P2R6L/RUN_OUTPUT_TRANSPORT/successor_release_replay_manifest.json.chunks/`

with a small manifest adjacent or inside that directory.

## Existing local commit handling

Prepare exact local instructions for the already-existing unpushed commit `32cc3ab...`.

The instructions must preserve all governed output bytes.

Preferred safe workflow:

1. verify current local HEAD is the reported unpushed R6L PASS commit and remote is still at the commissioned R6L tip or a known HQ-authorized successor;
2. record the four governed output hashes from the committed/local receipt;
3. remove only the oversized replay-manifest path from the Git index/history to be rewritten for transport, while keeping the working-tree file byte-identical;
4. run the exact packager on that preserved working-tree file;
5. verify the transport manifest/chunks reconstruct to the exact original SHA-256 and size;
6. update the governed R6L local receipt only to add transport metadata, without changing the original logical artifact hash;
7. amend/recreate the unpushed commit so the Git tree contains transport chunks instead of the >100 MB logical file;
8. verify all other governed files are unchanged;
9. push.

Do not authorize destructive commands that can discard the local original file.

Do not require carrier/source access.

Do not rerun R6L source execution.

## Transport chunk count

Do not hard-code exactly five chunks as a semantic requirement.

Chunk count is determined mechanically by:

`ceil(logical_size_bytes / 25165824)`

For the current ~113 MB file, five chunks are expected, but the manifest is authoritative.

## No Git LFS unless separately proved necessary

Do not introduce Git LFS in this commission.

The goal is plain-Git deterministic transport with no new external storage dependency, quota, pointer semantics, or repository configuration.

## Qualification

Use generated nonempirical fixture bytes only.

Prove at minimum:

- one logical file chunks deterministically;
- exact expected chunk count for representative >100 MB-equivalent tiny fixture scaled by test chunk size;
- chunk reordering fails reconstruction verification;
- missing chunk fails;
- changed chunk byte fails;
- unexpected extra matching chunk fails;
- changed manifest hash fails;
- reconstructed bytes equal original exactly;
- packager does not mutate original;
- verifier works without original present;
- receipt transport metadata can bind logical artifact and transport artifact separately;
- no JSON parsing or semantic rewriting occurs.

## Required outputs

Write only under:

`WORKER_RETURNS/EE-P2R6T/`

At minimum:

1. `00_RETURN.md`
2. `01_LARGE_JSON_TRANSPORT_CONTRACT.json`
3. `02_PACK_GOVERNED_ARTIFACT.py`
4. `03_VERIFY_RECONSTRUCT_GOVERNED_ARTIFACT.py`
5. `04_R6L_LOCAL_COMMIT_REWRITE_PACKET.json`
6. `05_BROWSER_QUALIFICATION_RECEIPT.json`

## PASS terminal

`EE_P2R6T_PASS__BYTE_EXACT_GIT_TRANSPORT_PACKAGING_READY__R6L_OVERSIZED_LOGICAL_JSON_CAN_BE_PUSHED_AS_RECONSTRUCTIBLE_CHUNKS_WITHOUT_EMPIRICAL_RERUN`

PASS wakes HQ adjudication only.

## Hard forbidden

- no Library/carrier/source access;
- no source driver rerun;
- no regeneration of governed R6L outputs;
- no JSON-semantic splitting;
- no lossy transformation;
- no Git LFS;
- no actual realization binding;
- no P2X or BE1;
- no Candidate-C repair;
- no selector remint;
- no D02/F02 workload mutation;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement of the R6L logical identity.

Run governed Browser qualification, commit and push on the exact branch, and return PASS/BLOCK with final tip, packager/verifier blobs, qualification evidence, and exact local rewrite instructions.
