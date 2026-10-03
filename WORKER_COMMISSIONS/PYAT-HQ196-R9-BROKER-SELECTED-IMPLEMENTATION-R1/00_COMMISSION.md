# PYAT HQ196 — R9 brokered source access + selected-reader implementation — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / SOURCE-FREE IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq196-r9-broker-selected-implementation-freeze-r1`

Exact implementation base / executable freeze:
`8ff40d37de69db2d8a6053a7c2242f481677f1a4`

This branch is deliberately rooted on the executable freeze lineage, NOT documentary control.

Checkout mode:
`SPARSE_REQUIRED`

Sparse materialization manifest:
- `/WORKER_COMMISSIONS/PYAT-HQ196-R9-BROKER-SELECTED-IMPLEMENTATION-R1/`
- `/WORKER_RETURNS/PYAT-HQ196-R9-BROKER-SELECTED-IMPLEMENTATION-R1/`
- `/rawlsing_next/`

Exact startup SHA is supplied by HQ after this commission commit.

Do not clone the repository.
Do not materialize the historical HQ/data estate.
Read non-ancestor HQ195/HQ196 evidence with `git show <sha>:<path>`.

## Mission

Produce a source-free candidate that closes BOTH current implementation seams:

1. make the literal source-path open account application-owned, countable and enforceable using pyreadstat's existing file-like-object bridge;
2. implement the frozen selected-variable physical-read route for sources whose law requires selected reads rather than full reads.

No real survey source access.

## Governing refs

Read via Git objects:
- HQ195 feasibility `63f10827e673a4b3c53a0a123303b2b9bb96c59a`;
- HQ195 stage `66929dad727410b8bfd33831cd2d8c632d5ccf4a`;
- HQ195 contract review `6df3257c5e362947c988d3260302cef2372e0809`;
- HQ196 adjudication `d43756fb3c80645ac887cca90026ecbdb10dd18c`.

The contract meaning is not in scope for redefinition.

## Phase 0 — complete reader/access census

Before editing, census every source-file operation in the exact freeze:
- existence/access checks;
- SHA-256 pass;
- raw-layout/header-prefix read;
- metadata read;
- compatibility/full read;
- selected read;
- batch/chunk read;
- any direct pyreadstat path-string call.

Show exact call sites and which path-open/read account each creates.

The repository-wide pyreadstat census is expected to be confined to `pre553_physical_decoder.py`; verify rather than assume.

## Phase 1 — application-owned governed broker

Implement the smallest production candidate that:
- opens the source path under application control;
- counts every application-owned source path open;
- exposes/records read calls and bytes;
- has explicit pre-operation budgets/guards;
- passes a file-like object to pyreadstat so the compiled reader does not receive/open the source path;
- keeps path opens, hash passes, header reads, reader invocations, decoder invocations and byte counts separately typed.

Prefer one physical source path-open for a governed decode scope if correct; do not force "one" if correctness requires more. The count must follow the implementation, not the desired warrant value.

Route the SHA/hash pass and header-prefix access through the governed access context where feasible so the literal source path-open account is complete rather than only covering the decoder.

Do not mutate pyreadstat, ReadStat, system libraries, or the accepted R7 environment.

Pin/assert the pyreadstat seam/version so an incompatible future version fails closed.

### DTA chunk constraint

The HQ195 feasibility lane found that reusing one broker object across row-offset parses fails unless parser position/reset expectations are satisfied.

Develop and prove the correct design:
- fresh logical broker/view/reset per chunk while preserving truthful OS/path-open accounting; OR
- another exact mechanism.

Do not silently fall back to raw path strings.

## Phase 2 — selected-variable physical read

Frozen O1-C07 requires:
- SRC02: selected_reads=1, full_reads=0;
- SRC06: selected_reads=1, full_reads=0;
- SRC14: selected_reads=1, full_reads=0.

Implement an exact selected-variable reader route using the underlying library's supported column-selection mechanism where competent.

Requirements:
- selected variable names and ordinals are bound before the data read;
- unexpected/missing selected columns fail closed;
- no unselected row-data columns are read by the governed selected route where the library can enforce that;
- selected-read count and configuration are separately recorded;
- full-read count remains zero on the selected route.

Do not change survey semantic authority, missingness classification, typed-value semantics or witness truth.

If the existing public decoder API cannot represent the operation cleanly, add the smallest explicit API/contract needed; document it.

## Phase 3 — source-free courts

Use synthetic carriers only.

Mandatory:
1. brokered metadata read;
2. brokered ordinary decode;
3. brokered SAV selected-variable read;
4. brokered DTA route;
5. batch/chunk route including DTA reset/fresh-broker constraint;
6. excess open/read/byte budget failures before excess operation;
7. raw path-string escape negative case;
8. selected-column unexpected/missing negative cases;
9. exact accounting separation.

### Full prior court

Re-run the existing 55-carrier source-free court at its declared grain using the brokered candidate.

Compare candidate output against the accepted baseline for:
- pass/fail denominator;
- metadata and physical declarations;
- columns/shape/values where applicable;
- relevant identity/receipt fields.

Run twice if the prior governing court required twice.

Do not call synthetic equivalence survey-semantic equivalence.

## R7/C4C3 interpretation

The interpreter/package binary identity should remain unchanged if no dependency is modified.

Nevertheless the APPLICATION path changes, so:
- repeat the appropriate C3/C4C3 source-free qualification court;
- do not claim prior 55/55 unchanged as proof of the new call path;
- report exact new code/tree identities.

## Allowed write terrain

- `rawlsing_next/pre553_physical_decoder.py`
- new narrowly scoped `rawlsing_next/pre553_*source_access*.py` module if justified;
- `rawlsing_next/tests/**`
- `WORKER_RETURNS/PYAT-HQ196-R9-BROKER-SELECTED-IMPLEMENTATION-R1/**`

No other production files without STOP/HQ recommission.

## Allowed dispositions

Exactly one:
- `BROKER_SELECTED_CANDIDATE_READY_FOR_HOSTILE_REVIEW`
- `BROKER_CANDIDATE_READY__SELECTED_ROUTE_BLOCKED`
- `SELECTED_ROUTE_READY__BROKER_ACCOUNTING_BLOCKED`
- `MATERIAL_IMPLEMENTATION_GAP_REMAINS`
- `CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED`

No self-adoption.

## Return law

Commit substantive candidate + evidence, push, re-fetch, verify.
Report branch, exact pushed tip, substantive SHA, disposition and terminal.

Terminal:
`HQ196_R9_BROKER_SELECTED_IMPLEMENTATION_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero real-source access, locator discovery, warrant issuance, live C4, C7 or actor/person work.
