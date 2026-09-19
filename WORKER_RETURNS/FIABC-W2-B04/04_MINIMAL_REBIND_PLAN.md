# FIABC-W2-B04 — Minimal Rebind Plan

This is a classification/repair specification only. FIABC-W2-B04 performs no production mutation and authorizes no new semantic work.

## Invariants that every repair must preserve

Any later implementation of this plan must preserve exactly:

- source SHA and source-local universe identities;
- accepted AuthorityRefs / AuthoritySnapshots and their content hashes;
- LiTS projection identity;
- LiTS R6O runtime catalog `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`;
- LiTS active binding `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`;
- LiTS runtime release `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`;
- WVS Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188` and replay identity;
- WVS projection identity `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`;
- P2R1 carrier-neutral seam blob `e7cda773e6a2426bfa12b22790fd8e005fe75153`;
- A/B/C frozen owner blobs at `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`;
- preserved LiTS-A/LiTS-B evidence and WVS-C negative-state law;
- no change in candidate semantic workload, candidate physical definition, or comparison accounting.

A repair that changes one of these is not a packaging repair.

## R1 — close the exact Node4A fan-in gap first

At audited P2X tip `617c9c9426db12a3c0f7fea6b68a582c10759553`, the adopted LiTS materializer requires:

`WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py`

with exact blob:

`504944f9533b7385d201076e2e834b8a9446dee8`

but that path is absent from the P2X tree. The exact accepted carrier exists on:

`agent/rabochii-prev3-ee-p2r6o-ab-owner-seam-requalification-r1`

Smallest lawful repair options, in order of mechanical simplicity:

1. fan in that exact blob unchanged at the path already required by the adopted R6S materializer; or
2. change only the R6S materializer's locator so it reads that exact immutable accepted object and verifies the same blob before use.

No predicate reconstruction is permitted. The Node4A carrier's embedded authority refs and exact semantic inputs remain unchanged.

This is the only debt item in this return where the audited P2X tree lacks a required accepted input carrier outright.

## R2 — rebind the LiTS derivative runtime materializer without rewriting it

The current backend directly imports:

`WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`

The content is a derivative materializer over accepted immutable determinants and current PRE553 contracts. It is not a semantic owner.

Minimal packaging repair:

- adopt the exact qualified materializer bytes into a stable current runtime binding, or bind to an exact immutable adopted blob;
- update only the backend locator/import binding;
- retain the exact D02/F02/Node4A/B6/AS3R3/R6N/HQ-registry determinant checks;
- require the same runtime-catalog, active-binding, release, 50-candidate, and 77-role checks.

Do not replace the determinant graph with a hand-authored JSON snapshot unless separate governance proves that snapshot is the accepted replay-equivalent product. Direct producer reuse remains lawful and preferred.

## R3 — rebind the WVS derivative runtime package

Current dependency:

`WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json`

Minimal repair:

- preserve the exact package bytes or constructor-complete equivalent whose refs/hashes are byte-for-byte checked against the accepted P2F2/Lock2 identities;
- give the backend a stable current runtime package/reference rather than an incidental worker-return locator;
- leave all WVS semantic authority with P2F2/adopted HQ authority and current PRE553 object contracts.

No SAV-derived semantic regeneration, fuzzy lookup, or Lock2 mutation is permitted.

## R4 — rebind the WVS source-specific projection materializer

Current dependency:

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

Minimal repair:

- adopt/rebind the exact qualified implementation bytes to a stable current executable reference;
- change the backend import/path binding only;
- keep the exact R6S projection identity, B_COUNTRY coordinate authority, Q291G5/Q291P5 bindings, raw/unweighted law, routing law, and replay identities;
- preserve the materializer's fail-closed structural checks and prohibition on using Q291 outcomes to construct semantic authority.

The generic `pre553_source_backed_c11_facade.py` remains an enforcement/projector contract, not a replacement source of WVS-specific semantic meaning.

## R5 — explicitly retain the lawful immutable roots

No rebind is required for:

- LiTS AS2A authority bytes;
- exact LiTS AS2B replay builder;
- D02/F02/B6/AS3R3 immutable determinant/replay roots;
- HQ registry/R6N proof;
- repetition-forbidden P2X receipts;
- P2R1 qualification and WVS-C negative-state evidence;
- P2R1 seam identity;
- frozen A/B/C owner modules and R5 helper closure;
- P2X S17 verifier for this bounded court.

In particular, do not replace the frozen Candidate-B blob with the current-tree facade merely because the module name matches. The blob differs and would change the candidate implementation.

## R6 — verification boundary after rebinding

A later implementation may claim packaging closure only if it mechanically proves:

1. every newly rebound file/object has the expected exact blob/hash;
2. all upstream authority/replay refs are unchanged;
3. LiTS and WVS runtime package/projection identities are unchanged;
4. the P2R1 seam and candidate-owner blobs are unchanged;
5. no fallback/default/latest/fuzzy semantic lookup was introduced;
6. no preserved stage was rerun;
7. static P2X binding resolves without a missing worker-return path.

A governed live-execution receipt is a separate burden. This B04 return does not convert static packaging closure into proof of post-repair P2X consumption and does not authorize measured P2X.

## Minimality conclusion

The repair surface is reference/fan-in only. No new compiler, adapter family, semantic authority, candidate implementation, source-specific fallback, or workload redesign is justified by this dependency estate.
