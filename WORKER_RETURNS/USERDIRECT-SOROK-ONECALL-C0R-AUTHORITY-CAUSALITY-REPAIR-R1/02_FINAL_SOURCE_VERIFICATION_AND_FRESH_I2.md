# C0R post-publication verification and independent-I2 handoff
**Disposition:** `C0R_SOURCEFREE_REPAIR_CANDIDATE_PENDING_FRESH_I2` (NOT acceptance, issuer authority, or production). This is an authored test-only repair.

## Exact current remotely verified implementation
The repaired `onecall_c0.py` **is now directly committed as readable source in this directory** at Git blob `76bd3a6ea26fd72ef59816d62013fd694bf8e774` (SHA-256 `298ff2bdbf4f916049ae21167e238767d2da682f369820a29c7d5ffa1a5461f9`). `test_c0r_hostiles.py` is also committed as readable source (SHA-256 `acace6c3c0d8f09b3277f0ca91f47ab6a27a6842e9cb2b9335ca307cb540a801`). The earlier conditional note in 00_RETURN about future upload is now satisfied. There is NO reason to assume the archive is the sole executable source.

## Physically reverified local execution
- Original unchanged C0 source with its original 32-case suite: **32 PASS**, observed exit=0.
- Repaired code with 54 newly authored translations of the A01–A32/R32–R43 hostile requirements and ten mutation probes: **54 PASS**, observed exit=0.
- Repaired code with unchanged 32-case original C0 suite: **31 PASS / 1 RED**, observed exit=1. The single exact incompatible **R08** expected cosmetic `possible_relevance_domains` text to change canonical event hashes. Independent R35 requires the opposite; the repaired rule preserves R35 and an **unchanged historical R08 RED**. No test was edited or marked xfail.
- Two *new* interpreter processes `PYTHONHASHSEED=17` and `791` independently produced byte-identical 18,384-byte outputs, SHA-256 `1949122dd8761e9c742477b502f6a73b82dd98670408361b5002473b5581dbdf`.

**Critical proof limit:** C0F's exact pinned immutable independent tests were **not** re-executed byte-for-byte against this repaired source. The author's 54 new tests are *falsifier translations*, not an independent I2 verdict. The historical Phase-A frozen oracle and original source-exact R42 retain their exact original authority and scope.

## Fresh independent I2 instructions
1. Verify source and test Git blobs from the current branch, plus exact C0 source `f45e4f5573495f060503f92b7630ec83531ced4d` and exact C0F originals `df31181c22afe3f8ec178b02f0e769e3cb610c81`.
2. Run untouched independent A01–A32, R32–R43, preserving **original R42 on original C0 only**; separately verify repaired identity, not by changing original R42's expected preimage.
3. Challenge fail-closed source/owner rule under `python -O`, source replacement between validation and append, forged current/partial-state identity, parent denial and cyclic dependencies, material-context independent counterpart refusal, immutable event hash, causal/noncausal relevance isolation.
4. Treat a valid unsupported subannual-time refusal as a refusal, **not** proof of a functioning 90-day scheduler. Do not infer B3/CAN actor psychological rules, arbitrary issuer, original surveys, deployed actor, calibrated probability, native F1 repair or production grant.
5. Grade sourcefree repaired author positive independently; preserve a named hold on all unissued owner boundaries.

### Downloadable exact evidence
A separate attached archive `ONECALL_C0R_COMPLETE_SOURCE_AND_EVIDENCE.zip` contains the repaired and original runnable source, tests, stdout/JUnit, replay JSON, and proof limits; SHA-256 `851df67d8b68ad3b9ee28745f561677643b39fd3fc2f1cba8707e902ab7748e8`. Its archive SHA is a transport receipt, not a source owner grant.

**No original C0/C0F source, frozen oracles, production modules, PRE-MAIN controls or other owners were mutated by this return.**
