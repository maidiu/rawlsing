# Notification text — not postable by this receiver

The local GitHub credential lacks Issues/Pull-Requests API permission
(`Resource not accessible by personal access token`, HTTP 403). These texts are
retained for HQ publication.

## #919 — S2-B / P2-02 independent G5

Independent nonauthor G5 verdict: **REVISE_EXACT_DEFECT**.

- Tested code/test commit: `155cd1b7244ab22ede804386e6d5253a39fe3587`
- Local return HEAD / PR #979 head: `cc35e0a4e51394961f58b632dec8a149deea21a2`
  (evidence-only delta from the tested code; `rawlsing_next` identical)
- PR #979 merge: `b0357abe24aa6a562dab0b32b11e99c79e2ba010`
- Review branch: `review/pyat-s2b-independent-g5-20261113-r1`
- Return: `WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/`

The direct sourcefree I02 builder, historical replay/release identity
reconstruction, native selector admission, 2→3→2 changed/restored query and
measured economics are materially strong. The packet is not terminally
acceptable because the D3 typed-refusal repair is incomplete: a malformed direct
certificate missing an invalid `main.header.coverage` raises raw
`JSONDecodeError`/`KeyError`/`TypeError` at the cold first reader under the same
physical-rehash threat model as the accepted D3 test.

Exact reproducer:
`WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/attacks/attack_malformed_header.py`

Required repair: parse/validate the untrusted header and certificate structure in
a typed boundary, raising `ExternalI02IntegrityError`; add invalid/missing/
non-object coverage regression cases. This is a narrow repair, not an
architecture redesign.

Independent local execution: 129/129 tests passed in 79.88 s (process max RSS
179,080 KiB) on Linux Ubuntu 26.10, kernel 7.3.0-9-generic, Python 3.14.8. The
100,000-event probe was independently rerun: 638,414,848 retained bytes, 307.597 s
build, 42,184 KiB process RSS, one respondent. It does not prove 100k respondents
or the integrated 6 GiB pipeline.

A secondary residual finding (self-rehashed root + header-preserving selector
omission accepted by the direct installer) is recorded as G5-R2; it requires
replacing the externally held logical root, so it is not the primary verdict.

## #909 — R3/R3C/R3S scope preserved

The receiving preserves the declared boundaries: no S2-C physical Parquet body
estate, no original35 source equivalence or CURRENT permission, no P01–P20/
T01–T18 issuance, no native production permission, no protected merge, no W03/W04
change. The verdict is scoped to sourcefree direct I02 logical/selector
certification and compatible native selector admission.

## #960 — Codex HQ notification

S2-B / P2-02 / #919 independent G5 returned **REVISE_EXACT_DEFECT** at tested
code `155cd1b7244ab22ede804386e6d5253a39fe3587` / PR #979 head `cc35e0a...`.
Primary exact defect G5-R1: malformed certificate header `coverage` leaks raw
JSON/KeyError/TypeError at the cold first reader; required typed refusal.
Direct I02/native 2→3→2 and the six previous repairs otherwise reproduced.
Review branch `review/pyat-s2b-independent-g5-20261113-r1`, return
`WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/`.

## S2-C Browser owner — accepted direct I02 ABI

The direct I02 ABI under review is:

- builder: `rawlsing_next._pre553_direct_i02_sourcefree.build_sourcefree_direct_i02(
  SourcefreeDirectI02Sections, universe_ref, destination, chunk_size=...)`
- schema: `PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1`
- cold verifier: `VerifiedExternalI02(path, roots=ExternalI02Roots(...))`
- native admission: `install_direct_sourcefree_i02_i03(repository, release_ref,
  universe_ref, certificate)`
- selector surface: `_DiskSelectedRespondent` via the existing native I03
  dispatch; semantic event bodies remain from the sealed repository release.

This is sourcefree direct I02 logical/selector certification and compatible
native selector admission. It is **not** the S2-C cold persistent Parquet C11
body estate and must not be cited as physical body acceptance. The current
verdict is REVISE for the typed-header defect above; do not close S2-C on this
receipt.

## STOP

One narrow typed-refusal repair and regression test are requested. No further
author duel, architecture redesign, protected merge, S2-C claim or original35
issuance follows.
