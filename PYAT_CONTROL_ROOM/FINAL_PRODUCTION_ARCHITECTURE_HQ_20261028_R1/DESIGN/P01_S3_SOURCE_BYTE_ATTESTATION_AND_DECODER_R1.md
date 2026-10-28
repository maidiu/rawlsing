# P01-S3 precision addendum — real source-byte decoder, changing-path risk and reuse

**Direct current-control evidence, 2026-10-28:** `maidiu/rawlsing@299f41e97a43c67be9cc76a79fa49b48f4e12e54`.

## Verified names, no imaginary module
- `rawlsing_next/pre553_source_read_admission.py` is **NOT PRESENT at this exact control path**. Neither `rawlsing_next/source_configuration/factory.py` nor `pre553_source_read_gate.py` exists at this exact cut. They may be present on later feature branches; absence here is NOT a whole-repo/all-branch negative.
- The actual physical decoder is `rawlsing_next/pre553_physical_decoder.py`, blob `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5`. `_decode` (439–521) computes `source_sha = _sha(source)` at 451 and rejects `expected_source_sha256` mismatch at 452–461, *before* returning `PhysicalSourceIncidence`. It also computes file metadata, reader settings and `physical_metadata_digest`.
- `PhysicalSourceIncidence.iter_batches` (108–149) can read `_frame` if compatibility/full read, OR when streaming, call `pyreadstat.read_file_in_chunks(reader, self._source_path, ...)` later (roughly lines 134–149). Its source path is a string and the file can theoretically change after the original SHA pass. Therefore `_decode` SHA alone is not an unconditional attestation that subsequent emitted physical cells came from unchanged bytes.
- `rawlsing_next/fiabc_whole_source_physical_equivalence.py`, blob `acdbc3f99f38d228d20d6a27ab7e89558af354af`, is existing *physical-only* candidate-neutral evidence with no survey semantics or source-read permission. It may supply independent physical-equivalence dimensions in its actual accepted scope, not serve as a substitute I02 seal.
- `rawlsing_next/pre553_source_local_universe_admission.py`, blob `b968fa16c6620cd06b191ebdb5da7da86f524393`, is source-local universe semantic admission under caller-supplied authority; it explicitly does NOT itself infer source authority or population/weighted/pooled use. It is NOT proof that original file bytes were read and unchanged.

## Selected precise source-admission design
1. Qualifying source owner (NOT this Browser HQ document) establishes an **immutable source snapshot lease** for an approved local source path/storage snapshot, verifies SHA against expected exact snapshot. The worker may use a secure private read-only copy or immutable custody mechanism as actual host/filesystem allows; do not silently copy private raw respondents into Git/public storage.
2. Use the *same verified immutable bytes* for `decode_sav`/`decode_dta` and physical cell extraction. Current decoder may reopen pathname; source owner must prevent concurrent mutation by immutable custody/read-only lease and, where useful, verify unchanged SHA again after all rows. A before/after SHA alone without immutable custody cannot strictly exclude malicious or intermittent modification; it is supplementary.
3. Bind actual SHA, source-retention ref, decoder implementation/version, reader configuration, physical metadata digest, row and physical slot inventory, governed semantic projection/slot owner authority refs to the admission receipt. Names of exact existing external grant/custody receipt are **UNVERIFIED** until current Pyat SRC04 owner grant trace is read; DO NOT invent a fully-qualified native permission class.
4. Existing `pre553_source_backed_c11_facade.GovernedC11Projection` (264+) checks source_snapshot_retention_ref hash against expected_source_sha256 and row/slot binding; this still does not alone replace the original-byte custody check.
5. New `C11VerifiedSourceView` registration requires BOTH the complete old-I02 journal validation receipt and this independently qualified source-byte/retention receipt. No `ExactPhysicalCellStream(source_sha256=...)` caller assertion or physical hash alone mints it.

## Exact negative/positive tests for P01-B03
- Mismatched expected source SHA at `_decode` must refuse before governed decode.
- Mutate a temporary synthetic source file after `_decode` but before `iter_batches`; without immutable snapshot guarantee, the test must expose the unsafe pattern rather than qualify a view. Under immutable leased file or dedicated private snapshot, emitted row/slot cells and SHA/metadata belong to the same unchanged bytes.
- Change file content and restore original digest between checks: demonstrate SHA-before-and-after alone is not a complete integrity guarantee (no need to create malicious code; use a controlled fixture). Require immutable custody.
- Wrong retention hash even with self-consistent I02 candidate must refuse new view, without retroactively rewriting old I02 behavior.
- Source file missing/revoked: no new original-source view, no authority from retained acceleration.
- Existing FIABC physical evidence is used only for physical dimensions at original scope, never to certify user meaning/population/FF or original source permissions.

## Closure / owner
Implementation owner: source/custody qualified Pyat original-source producer and current `pre553_physical_decoder.py`; I02 integration owner remains separate. P01-B03 is blocked for real original source until exact issuer grant/receipt location is identified. Source-free tests may use test-only synthetic attestation clearly marked fixture. S3-HR-037 (time-of-check/time-of-use) must be tracked in high-resolution ledger. This is a **precise engineering dependency**, not an invitation to reopen physical route or semantic source selection.
