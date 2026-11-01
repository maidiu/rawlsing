# SOURCE RIGHTS AND SCOPE

## Execution boundary

- Surface: S2 exclusive local Git worktree, original-sourcefree pytest.
- No S3/native execution, raw survey source read, native/protected source read, actor object, CAN/ADP, N11/N12, Sorok, or PREMAIN authority was used.
- Synthetic SAV/DTA bytes were created only under pytest `tmp_path` for reader-path and custody regression. The pyreadstat reader was not run against any raw survey source.
- No source meaning, text semantics, survey semantics, estimand, U/E_pre, permission, issuer, use, science, adoption, merge, or PR was issued.

## D01 source-pair provenance and rights

The three full D01 identities were derived from original authoritative sourcefree code, not from file names or inference:

- candidate decoder `37013eb52efb8b61ef202b0d686f729f459d79c5` at `3cefb4ebf61ccdb6a8c5a03815438bdcda021292`;
- accepted D01 integration `1f9990fec3d305ea89dfe25bdeae89a967adb21b`.

The exact pairs are:

```
ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2 -> BIG5
5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2 -> WINDOWS-1252
66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec -> WINDOWS-1252
```

The same literal hashes are corroborated in current PREMAIN data manifests. Those manifests are not encoding authority and were not used to invent or infer the pairs; the encoding pairs come from the original code. A source SHA-256 is a physical identity only. It is not a license, permission, rights grant, or source-use authorization.

No raw source was opened or decoded under these encodings. All three pairs are admitted as physical decoder configuration only. Actual raw-source use remains HELD to the PRE-MAIN physical-decoder/native-source-rights owner.

## D02 source rights

D02 carries only the exact representation of built-in naive `datetime.date`, `datetime.time`, and `datetime.datetime` objects. It does not infer survey date/time meaning, calendar semantics, display-format meaning, timezone meaning, or source authority.

Timezone-aware values are refused. No timezone-aware carrier authority is claimed. If a later task needs one, it requires a separate explicit decoder-carrier authority decision.

## PR526 custody

The current PR526 custody contract is preserved and not replaced:

- private content-bound source snapshot;
- hash while copying;
- read-only `O_RDONLY` descriptor;
- `/dev/fd` reader binding;
- stability and hash verification;
- unlink of the private path;
- idempotent close.

No R9 broker/session/binding or historical source-path reader was transplanted. The historical decoder snapshot was not imported wholesale.

## Write scope actually used

Production and tests:

- `rawlsing_next/pre553_physical_decoder.py` — D01 exact declared lane and D02 decoder seam.
- `rawlsing_next/pre553_r5_codec.py` — D02 opaque carrier and normalization; byte-equal to accepted C3 blob `6000a1704`.
- `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py`
- `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py`
- `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py`

Return:

- `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/**` (the five required documents)

No PREMAIN/main, Sorok, native/protected source, other worktree, branch deletion, force push, PR, merge, self-review, issuer/use, or `#580`–`#584` state was written or mutated.

## Authority and unresolved owner choices

1. D01 source-use authorization: HELD to the PRE-MAIN physical-decoder/native-source-rights owner. Exact encoding admission does not grant source use.
2. D02 timezone-aware carrier: HELD; values fail closed until a separate explicit authority exists.
3. G01 native-int to float64 representation authority: HELD to the G01/C11 owner. The two G01 hostile failures exist identically at startup `8e44ca9c` and were not changed. Numeric coercion was not broadened.
4. R9 broker/session/binding, real issuer/role, source permission, and science: outside this return and HELD.
5. Actual raw-source qualification of the declared encodings: HELD to the owner with raw-source rights.

## Conflict handling

No original/current D01 or D02 semantic conflict was found. The original accepted D01 lane and D02 carrier were restored at the current receiver with the current PR526 contract.

The only observed conflict is the separate G01 native-int/float hostile expectation. It is outside D01/D02 scope. The current G01 code was preserved unchanged; both the startup and repaired behavior were measured and recorded. No alternative G01 version was invented or committed.
