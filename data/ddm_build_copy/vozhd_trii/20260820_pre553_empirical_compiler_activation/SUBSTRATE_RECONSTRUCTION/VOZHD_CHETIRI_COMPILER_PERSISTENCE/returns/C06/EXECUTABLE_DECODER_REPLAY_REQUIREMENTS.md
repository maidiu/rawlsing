# C06 — Executable Decoder Replay Requirements

Status: `NAMED_EVIDENCE_REQUIRED__R13`.

## Finding

Current source law correctly pins source bytes, decoder code/configuration and compatibility behavior. Current `pre553_physical_decoder.py` also records `reader="pyreadstat"`, `reader_version`, `user_missing=True`, `apply_value_formats=False`, and exact compatibility encoding/status.

That is necessary but not sufficient for **durable executable replay**.

A package name/version is a label. It does not itself preserve the historical package artifact, the native ReadStat code it used, build options, interpreter/ABI behavior, or another output-sensitive dependency. The decoder also contains code-sensitive normalization and missing-value logic, so future “equivalent” environments cannot be assumed equivalent by name.

## Informational closure required

Durable replay must preserve or immutable-address enough material to reconstruct and verify:

1. decoder source/code content identity;
2. exact decoder configuration and format path;
3. exact compatibility allowlist/override authority;
4. dependency lock with artifact/content hashes, not only version strings;
5. transitive native-library/build identities where output-sensitive;
6. interpreter/runtime/ABI/platform determinants where output-sensitive;
7. package/source/build artifacts or another immutable resolution mechanism that does not depend on mutable registries;
8. build/reconstruction instructions/configuration needed to reproduce the executable behavior;
9. hostile decode test-vector identity and expected canonical incidence digest;
10. source extraction receipt binding the closure actually used.

An executable environment/capsule is one possible realization. A content-addressed reconstructable dependency/artifact closure is another. C06 selects neither.

## Environment determinants are evidence-driven

Do not blindly make every OS bit semantic identity. A determinant belongs in decoder replay identity when changing it can alter governed decoded incidence or when equivalence is not established. Differential hostile replay may prove some environment detail nonsemantic; until then, fail closed rather than silently assume equivalence.

## Minimum hostile vectors

The durable oracle should exercise, as applicable to governed source formats:
- system missing;
- format user-missing discrete/range states;
- Stata extended missing;
- labels/dictionaries;
- string/Unicode encoding and every frozen compatibility override;
- numeric boundary/representation cases actually admitted by source law;
- repeated/multiple-response metadata;
- row/variable counts and ordinals;
- metadata-only versus full/chunked path parity where both are lawful;
- the exact source hashes that require compatibility handling.

Expected output should be a canonical manifest/digest, not screenshots or prose.

## Invalidation

Any source hash, decoder code, output-sensitive dependency/artifact, configuration, compatibility rule, or hostile-vector expectation change creates a new decoder/extraction identity and requires equivalence review before historical replay can be called exact.

## Failure modes

Fail closed on:
- package version resolves to different bytes;
- artifact unavailable;
- native dependency drift;
- automatic encoding guess/fallback;
- compatibility override not bound to exact source SHA;
- test-vector mismatch;
- source incidence digest mismatch;
- replay environment cannot execute.

This gap requires no permanent canonical event carrier. It requires durable executable decoder closure.
