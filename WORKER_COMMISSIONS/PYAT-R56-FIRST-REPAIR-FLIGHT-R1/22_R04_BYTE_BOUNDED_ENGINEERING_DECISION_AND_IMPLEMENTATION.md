# R04.byte bounded engineering decision — close the snapshot write capability
Date: 2026-10-22. State: ENGINEERING_DECISION_COMPLETE__MECHANICAL_IMPLEMENTATION_NEXT.
Decision baseline: director1c89cdaa6a13b44aef8144bdf49a9caa4e66a82f, candidateea0d6f0f9840db0e33645b40ceda54456612709e, review228387c59b42590338636cd176feee3ccc9a6abc.
Task I3 native engineering. Exact selected model/effort unexposed; user requested this bounded Sol High decision. No architecture/science court reopened.

## Decision and causal finding
Keep the unlinked snapshot and /dev/fd reader route. Replace the retained O_RDWR snapshot descriptor with a separately opened O_RDONLY descriptor before any snapshot object, reader call or incidence escapes acquisition. Close every decoder-owned writable descriptor and retain no writable mapping. Verify the read-only descriptor against the copied content identity before publication. This capability handoff is the primary repair; mtime/ctime signatures remain ancillary diagnostics, not content authentication.
No per-batch full-file hashing or whole-SAV buffering is required by this decision. Preserve SAV streaming. DTA's already disclosed full-frame fallback remains a local qualification limit, not certified original35-scale execution.

Why: current acquisition opens the snapshot O_RDWR, writes it, fchmods it0400, unlinks its name, then returns the SAME writable descriptor. chmod does not downgrade an existing open descriptor. The reviewer can therefore mmap ACCESS_WRITE through the exact supplied fd. Dirty pages need not synchronously alter APFS stat times; the signature guard cannot authenticate bytes. The existing full digest would detect the change, but its later invocation occurs after facts escape.
The probe's full_digest_after_attack field is assigned snapshot.sha256 (cached acquisition digest), not recomputed bytes. Its unchanged value does not contradict the later DecoderError from actual verify(). The failed C11/I03 value assertion remains the relevant observed counterexample.

## Exact implementation contract
Modify only the allowed decoder and byte-custody tests/witness, plus author's own successor return.
In _acquire_source_snapshot:
1. Keep source and construction writer private. Complete copy/hash and validate expected digest; no reader may see construction state.
2. Apply0400 to the created inode. Open a distinct O_RDONLY reader descriptor (CLOEXEC and no-follow where supported). Compare device/inode/size with the construction writer, refusing substitution. Do not merely dup the writer: dup retains its access mode.
3. Close the construction writer before handoff and on every failure path. Do not retain it or a writable map anywhere in decoder state.
4. Unlink the bound inode's construction name. Verify the retained reader is read-only, identifies the intended regular inode, has the bound size and content digest, and the bound inode has no remaining link created by this acquisition. If the recorded path was replaced, do not consume it or delete unrelated replacement content; either preserve the verified unlinked inode or typed-refuse.
5. Only then construct/return _SourceSnapshot with the reader fd and acquisition identity. Methods reader_path/read_prefix/rewind/verify/check_stable must fail closed on closed, invalid or non-read-only retained descriptors. Derive capability checks from OS state rather than a caller-set boolean. Cleanup must not leak either descriptor or alter foreign replacements.
Existing full hash checks before/after metadata/full reads remain. Keep the descriptor binding for all reader calls; never reopen original source or snapshot pathname. Preserve applicable stat/lifetime checks as diagnostics. Existing cached compatibility frames were read and hash-verified before exposure; do not pretend later source changes retroactively change already verified in-memory frames.

## Trust boundary and guarantee
After handoff, ordinary write/pwrite/ftruncate/shared writable mmap operations using the decoder-supplied reader fd must be denied BEFORE any modification; readers get only read capability. The decoder controls construction and must create no other writer aliases/maps. This directly prevents the existing attack rather than declaring it out-of-scope.
The process's trusted operator/code is still responsible for not deliberately manufacturing NEW privileges or corrupting private decoder state: e.g. fchmod followed by acquiring a new write fd, opening process fd internals as privileged supervisor, dup2 substitution, ptrace/root or rewriting Python objects/code. No in-process Python library can promise isolation from an operator able to replace its own verifier/state. This is the existing trusted-runtime assumption, now with the unnecessary supplied write capability removed. Do not broaden the claim to hostile same-UID supervisor isolation.
If independent evidence shows a writable alias can be obtained through the ordinary declared reader interface WITHOUT a new permission grant/private-state substitution, this design fails and must not be accepted. Do not evade such evidence by changing the threat statement.

## Discriminating evidence performed here
Inspected exact decoder acquisition/lazy/full-read code and the review's actual mmap probe/failing test.
Two sourcefree OS capability probes used temporary arbitrary bytes only, no survey and no candidate edit:
- distinct read-only fd refers to same inode; /dev/fd read returns original bytes;
- pwrite on that fd refuses errno9; shared writable mmap refuses errno13;
- reopening its /dev/fd path O_RDWR refuses errno13 on this host.
Receipt23 records these observations. No pyreadstat/SAV/DTA or complete repair qualification is claimed by this probe.

## Implementation-ready instruction — SAME existing R04.byte author
Continue branch agent/rabochii-pyat-r56-r04byte-consumed-byte-custody-r1 from EXACT parent ea0d6f0f9840db0e33645b40ceda54456612709e. Verify actual head/no duplicate writer and isolated worktree; record actual model/effort/host/usage and proceed on match, no separate seal round.
Use qualified user-selected DeepSeek V4.1-Flash MAX/OpenCode for the now-settled implementation. Do not silently switch provider or keep using Sol High for clerical work.
Read this decision at its enclosing director commit, the candidate source, and exact review:
https://github.com/maidiu/rawlsing/blob/228387c59b42590338636cd176feee3ccc9a6abc/WORKER_RETURNS/PYAT-R56-R04BYTEV-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/00_RETURN.md
Read its actual test and evidence/probe_r2_mmap_fact_bypass.py. Preserve original failing evidence. Shared native contract remains at directoreb28fdcc311e2534b66def445e745cb25cb8a9bd; review shared contract485f31e52ca82905dcfbbc79c5f8c8294fb55f49; frozen policy6d95a78b... read-only.
WRITE ONLY rawlsing_next/pre553_physical_decoder.py, rawlsing_next/tests/test_universal_source_byte_custody.py, R57-approved non-executable sibling witness and WORKER_RETURNS/PYAT-R56-R04BYTE-CONSUMED-BYTE-CUSTODY-R1/revisions/r3/. Preserve all earlier returns.
Implement the handoff above. Fix generalized writable-fd ownership/lifetime, not a special branch for mmap or the failing fixture.

Required finite qualification:
- Assert actual retained fd O_RDONLY, writer closed, no decoder-owned writable aliases/maps and correct inode/hash; exercise cleanup/failure paths.
- Port the existing mmap counterexample as an ordinary passing regression: either write-capability acquisition is denied and the SAME C11/I03 baseline fact remains unchanged, or a typed refusal prevents any affected release. A raw OS error by itself without the unchanged-fact/typed-no-release control is insufficient evidence.
- Update earlier tests that REQUIRE successful pwrite/ftruncate of the supplied fd: verify denied write plus unchanged positive consumer, preserving their original negative evidence. Do not simply delete attacks. Writable injection via NEW privileged/private-state tampering is a separately labelled supervisor fault, not the ordinary supplied-fd contract.
- Actual SAV+DTA metadata/full/lazy public paths, original/private-path replacements, new-source/new-digest, repeated reads, cold fault/restore and cleanup. Verify pyreadstat works with O_RDONLY /dev/fd; raw-byte probe alone does not prove it.
- Preserve SAV chunking; avoid O(number_of_chunks × file_size) rehashing or whole-SAV buffering as a silent shortcut. Retain explicit POSIX requirement and DTA full-frame O(rows×cols) limit; extended-missing writer skip stays unqualified. Synthetic encoding allowlist tests issue no original encoding authority.
- Same-assertion mutation and fresh restore through actual C11/I03, changed-test/proof-integrity receipts, exact source/import/hash manifest. Generate manifests after receipts and use declared repository-root paths to avoid another custody loop.
Return one repaired candidate and handoff/attack/lifetime matrix; SAME still-independent R04BYTEV reviewer performs affected qualification on exact returned SHA. No new general audit. A concrete failure of the read-only handoff/native reader contract returns the exact capability evidence, not another guessed mechanism.

## Terminal disposition
Engineering: selected implementable within existing decoder/test grant; native acceptance still pending.
Science: no new issue or inference. Authority: existing R56/R57 only; no production/R09/N11/N12 adoption, original source reads or R03/R04.joined. J52/W52 stopped.
R00 and R02 scoped local qualifications remain. Combined-candidate proof waits for accepted R04. This engineering decision is finished; downshift now.
