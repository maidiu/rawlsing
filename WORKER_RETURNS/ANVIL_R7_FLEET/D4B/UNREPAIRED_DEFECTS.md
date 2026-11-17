# UNREPAIRED_DEFECTS

Scope: supplied R7 instrument and my bounded private-package strict overlay.
No item below is repaired in product code, shared package or protected refs.

## A. Supplied instrument — confirmed, not repaired by me

1. **Synthetic-ledger laundering.** `r7_transfer_conservation.transfer()` accepts
   any object with schema `ANVIL_SPINE_R5/R6`; `check_history()` checks 118 IDs
   and six prose fields, not source rows (`tools/r7_integrated.py:57-79`).
   Attack H01 `PASS_TRANSFERRED`, H02 FRAME PASS.
2. **No K3 re-derivation in the active path.** `row_sha256` may be `'d'*64`
   (the author's own fixture, `tools/test_r5.py:18`) and FRAME still passes.
   Attack H03.
3. **The only strong K3 check is inoperable.** `anvil.py:95` builds
   `k3_source_root + '/' + file`, but `03_FROZEN_SOURCE_CUTS.json:5` already ends
   in `/`; the resulting `//` makes `git rev-parse` fail and emits
   `K3_PINNED_FILE_MISMATCH` for every group. Verified directly with Git.
   The active R7 gate never calls `anvil.validate()` anyway.
4. **Provenance-only source pins.** `source_ref()` (`r7_integrated.py:44-55`)
   accepts any file under the caller-chosen source root with a matching SHA-256
   and quote; no protected-head/blob/owner anchor. Attack H04.
5. **Negative/risk omission tolerated.** `negative_meaning` only needs 12
   characters. Attack H05 replaces three K3 negatives with a generic sentence
   and FRAME passes.
6. **No 118→design conservation.** `check_decision()` reconciles only
   `frame.requirements` (`r7_integrated.py:177-201`). Deleting every per-118
   disposition leaves DECISION PASS. Attack H07.
7. **Boundary contracts are decorative.** Neither FRAME, DECISION nor
   C_INTEGRATED reads `02_BOUNDARY_CONTRACTS.json`. All seven T1–T7 contracts can
   be removed and replaced by one sentence. Attack H08.
8. **No actor firewall.** Survey→actor causal claims are not rejected; the only
   domain prohibition is FICTIONAL→OBSERVED inside the unused `anvil` graph
   check. Attack H09.
9. **No release/revocation.** A `REVOKED` release and `a*40` protected head still
   pass. The author's own fixture uses `'a'*40`
   (`tools/test_r7_integrated.py:41`). Attack H10.
10. **Builder command not executable.** `check_builder()` prefix-checks
    `test_command` (`tools/r7_stage.py:84`) but never resolves or runs it.
    Attack H11. Additionally the package ships no `FRAME.json`/`DECISION.json`/
    `C.json`, so the documented CLI cannot be run cold.
11. **False S1 dependency still present.** FRAME requires an
    `historical_source_spine` with schema `ANVIL_SPINE_R5/R6`; no accepted R5 P2
    SPINE exists (`20_RECOVERY...` says it was expected output). My faithful
    stand-in is a reconstructed test object, not the elimination of that
    dependency. The correct repair is direct reconstruction from the K3 TSVs +
    SEAM/25/26 + ANVIL/15, which I did not implement.
12. **K3 semantic truth not proved.** Row SHA-256 authenticates bytes, not
    meaning. My negative-vocabulary check is a heuristic; a determined author
    can paraphrase a false negative using source words.

## B. My strict overlay — bounded, not accepted

13. It is authored by the same worker that wrote the attacks; it is not
    independent C and cannot accredit itself.
14. Boundary checks compare frozen fields and require positive/negative/restore
    prose, but do not execute an actual boundary first effect.
15. Release/revocation is a record check; no C11 release service exists here to
    revoke cold.
16. Actor firewall is regex-based; paraphrase defeats it.
17. Builder check verifies file existence only; it does not execute
    `test_command`.
18. The 118 coverage check enforces one disposition per identity and
    non-boilerplate arguments; it does not prove that a disposition is true.
19. H05 catches two of the three mutated rows; one generic replacement shares
    enough source tokens to pass the heuristic.

## C. Not run / missing

20. **Final integrated candidate: not supplied.** All attacks against its exact
    bytes are `NOT_RUN`. Attacks here are against the old package plus my
    private reconstructed packet.
21. Live GitHub currentness was not re-queried; the local protected copy at
    `31291d0...` is the authority used. `LIVE_GITHUB.json` was not revalidated
    against the API in this pass.
22. No native SAV/DTA run, no 100k dense workload, no 6 GiB process-tree
    measurement, no C11/I03/I05 first reader. All such claims would be false.
23. No source, scientific, actor or protected receiving rights were issued or
    exercised.
24. The #1097/ZL-15 `52/24/21` crosswalk, the full V549/V550/V550J/F26 bodies,
    SEAM/25, SEAM/26 and ANVIL/15 exact bytes were not read. Any statement about
    them is limited to the protected summaries cited in `GROK_PROOF.md`.
