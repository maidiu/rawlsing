# Actual SRC04 witness caller

This is SRC04-specific. The reusable machinery is the producer/supervisor/fresh-reader pattern; the q217 hold, 177/3 scope and accepted historical accounting are SRC04 witness checks. Do not describe it as a generic all-wave acceptance.

## Gate

The `run` command cannot start without `--authorized-source-launch`; do not use it before independent construction G5 and the existing source permission. Preflight and synthetic refusal need no source.

## Exact command

```bash
python3 witness_caller.py \
  --mode run \
  --candidate-tree /path/to/exact-aee954-plus-ffa4520f-final-tree \
  --candidate-patch /path/to/candidate.patch \
  --config /path/to/SRC04/source.config.repaired.v2.json \
  --runtime-config /path/to/exact-accepted-ba886d-runtime-config.json \
  --binding-dir /path/to/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118 \
  --work-root /path/to/private-work \
  --authorized-source-launch

# After a checkpoint-preserving interruption, omit the source path semantics:
# add --resume-checkpoint <private>/prepared-sections.checkpoint.json
# The resume process verifies the checkpoint HMAC, exact source/config/request,
# grant/decision refs, and all spool file sizes/hashes; it does not decode.
```

The candidate tree must hash as `pre553_source_i02_handoff.py = 6ab7cb50…` and the final patch as `ffa4520f…` before import.

## Behavior

1. Supervisor verifies candidate/patch hashes and opens a unique private root.
2. Producer verifies exact grant/request, q217 hold and 177/3 scoped config before source decode.
3. Producer uses localized `single_pass_handoff.py`: one admitted decode, exact projected sections, and the existing `write_direct_estate` directly. The compact spool uses shared field headers plus positional typed JSON arrays in deterministic gzip; the existing canonical object codec reconstructs exact objects at the writer boundary. It removes the duplicate replay body journal and explicit first I02 pass; it does not change the core writer.
4. At the prepared-sections boundary, the producer writes an authenticated checkpoint (HMAC key private 0600) containing exact source/config/request/decision refs and complete spool hashes/counts. Writer publication remains atomic. After interruption, resume from this checkpoint without re-decode; altered/missing/partial checkpoints are refused before publication.
5. Supervisor enforces 6 GiB process-tree RSS and the 8 GiB in-flight free-space floor separately from the 26,907,826,727 B startup working-room gate. It reaps the producer before a fresh reader.
6. If the exact `ba886d877…` runtime overlay is absent, the caller refuses before source with `RUNTIME_OVERLAY_REQUIRED_FOR_RUN`; base v2 stops at slot 176 q716withoutmorocco.
7. Reader checks producer is gone, opens exact held roots/manifest with a real grant-scope callback (not allow-all), records family counts, identity/routing digests, release-ref comparison and precise differences from the accepted historical receipt.
8. No wall clock cutoff; abort only on RSS/free-space caps or failure.

Startup working-room gate: **26,907,826,727 B** (R3 terminal stage less duplicate journal + 8 GiB reserve). In-flight abort floor: **8 GiB**. RAM cap: 6 GiB. Current commercial-free availability was 15,924,334,592 B, leaving a **10,983,492,135 B startup gap**; no real run was launched.

## Follow-on hostile integration repair (source-static; not a new test receipt)

The original b3dd caller bypassed the launch flag through direct producer invocation,
created the checkpoint under root/private but resumed from root, and allocated an
unrelated run root on restart. Reader differences and release mismatch were advisory
only, and its CURRENT callback missed decision/revocation/source-format/locator checks.

Direct producer mode now enforces the flag *as well as* independent grant/currentness;
the supervisor passes it to the child. For resume supply the original --work-root and
--resume-checkpoint path inside its private directory; do not make a new root. A
resume is writer continuation with no additional source decode. The exact SRC04
reference witness now rejects count/release mismatches, and preflight rejects
request/grant divergence. Source-format and custody locator are included in full
CURRENT checks.

No actual original SRC04 source launch or real resumed writer has been carried out
for this patch; the old three green sourcefree tests apply to b3dd only. New tests
are authored but unexecuted and independent receiving remains held.

## Second hostile author repair — offline sourcefree entrypoint

The original caller used undrained PIPEs for potentially large producer/reader
progress messages; at the operating SRC04 scale this can deadlock. The
supervisor now writes logs directly to private files and never loses them by
child-side truncation. Monitor failure terminates and reaps the process group,
rather than leaving an unsupervised producer; missing reference-count families
now fail closed. The manifest now distinguishes sourcefree fixture reads from
original SRC04 source access.

Run `run_sourcefree_checks.sh` on the exact repaired Git worktree with the
`EXPECTED_ANVIL_HEAD` environment variable set to the 40-character head.
It checks the manifest file hashes and executes stdlib-only offline tests.
**It never launches an original source read.** These new author-side tests
are not claimed passing until a real local receipt is returned.

## Disk-light pinned archive test (no new full worktree)

Archive only this witness folder from an existing local repo at the **exact**
commit, then set `EXPECTED_ANVIL_HEAD` and
`ANVIL_ARCHIVE_FROM_REPO=/absolute/path/to/existing/rawlsing` to run
`run_sourcefree_checks.sh` inside the extracted tree. The runner verifies
itself, its manifest and key code files against the immutable Git SHA,
then all manifest SHA256/byte lengths, Python source compile, and
**six new and three inherited** no-source guard tests. No real source,
writer, remote process or host-grant action is performed by that script.
