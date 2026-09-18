# EE-P2R6A — ADOPTED R4A+R5A PRODUCTION RUNTIME IMPLEMENTATION

Repository: `maidiu/rawlsing`

Execution surface: **BROWSER**

Library access: **NO**

Exact branch:

`agent/rabochii-prev3-ee-p2r6a-r4a-r5a-production-runtime-implementation-r1`

Exact base:

`6586da01edac5e87fb81b6beb8d7b16fc0ea18ef`

First resolve live `HQ_HANDOFF/LATEST.json`, verify its immutable checkpoint packet, and consume the current HQ adoption of EE-P2R5A plus the already-adopted EE-P2R4A authority.

## Grain

`PRE553_PUBLIC_PREDICATE__MIXED_COMPOSITION__RELEASE_REALIZATION_RUNTIME_IMPLEMENTATION_ONLY`

No carrier access. No real realization binding. No P2X execution.

## Adopted semantic authority to implement

R4A adopted identities:

- respondent compatibility/refinement  
  `3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74`
- mixed grammar  
  `0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55`
- derived-predicate contract  
  `225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4`
- aggregate  
  `b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae`

R5A adopted successor authority, once HQ seal is current:

- release-realization authority  
  `9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5`
- concrete binding schema  
  `a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0`
- R4A release-precondition successor clause  
  `d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e`
- aggregate R5A authority  
  `d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2`

Do not proceed from this commission text alone if live HQ has not yet adopted those R5A identities.

## Mission

Implement the smallest generic production PRE553 machinery that consumes the adopted R4A and R5A authorities.

The implementation must remain fail-closed without a concrete realization binding.

It must not contain LiTS-, q310/q311-, F02-, D02-, or selector-hash semantic special cases.

## Required implementation

### 1. Public predicate dialect dispatch

Extend the accepted PRE553 predicate evaluator so an exact adopted predicate-grammar authority may select a governed interpreter contract.

For the adopted F02 child authority, the semantics are exactly:

`TRUE_IFF_SAME_ROW_GOVERNED_EVENT_HAS_EXACT_NATIVE_VALUE`

with exact question/value/source-native/release-scope material and missing=false.

Do not rewrite/remint the frozen selector AST.

Absent exact interpreter authority: fail closed.

### 2. Mixed predicate composition

Preserve the current exact-equality path unchanged.

When grammar/binding metadata differ, require an exact positive adopted compatibility/composition authority.

For adopted D02/F02 scope only:

- mixed operation = `AND`
- max arity = 3
- exact parent and child grammar refs required
- exact respondent refinement authority required
- no OR/NOT grant
- no cross-source/release grant
- no adjacent-family inference.

### 3. Derived-predicate construction

For mixed composition, do not inherit `predicates[0]` grammar/binding metadata.

Construct the derived predicate under the explicit adopted successor authority contract with deterministic canonical input ordering and unchanged input ExactRefs.

### 4. Release realization

Add the smallest generic exact release-realization authority/binding mechanism needed by R5A.

The frozen selector `release_ref` remains an exact opaque historical F02 scope anchor.

It must never be treated as the runtime I02 release or repository key.

Runtime evaluation is permitted only when:

1. selector release ref exactly equals the authority's frozen scope anchor;
2. exact adopted realization authority is present;
3. exactly one active positive concrete binding exists;
4. binding validates under the adopted R5A schema;
5. binding target is an accepted I02 `C11LogicalRelease`;
6. `C11Repository.resolve_release_exact(target_ref)` succeeds;
7. target/source/base/replay/M01-M18 facts satisfy the binding contract.

Zero or multiple active bindings: fail closed.

No latest/default/fuzzy/nearest behavior.

### 5. Genericity

Generic code may dispatch on exact authority refs and contract schemas only.

Do not encode source family names, question IDs, F02 hashes, selector hashes, or D02 lane IDs in runtime semantic branches.

Exact source-specific facts must remain data.

## Qualification without real carrier

Use mocks/tiny fixtures/banked exact authority objects only.

Prove:

- legacy same-grammar/same-binding behavior unchanged;
- unrecognized child dialect fails closed;
- F02-shaped AST without adopted child authority fails closed;
- adopted child dialect evaluates exact-native equality correctly in fixture form;
- mixed composition rejects absent/wrong authority;
- AND-only exact authorized path works;
- OR/NOT mixed path fails;
- derived mixed predicate gets explicit successor authority;
- release realization fails with zero bindings;
- fails with multiple bindings;
- fails with source/release/authority mismatch;
- fails if repository target absent;
- succeeds with one exact valid fixture binding + sealed fixture I02 release;
- no selector reminting.

## Do not

- access Library/carriers/outcomes/performance;
- issue a real realization binding;
- generate the real LiTS successor release;
- fan into P2X;
- run BE1;
- repair Candidate C;
- mutate D02/F02 workload;
- mutate Lock1/Lock2;
- modify MAIN or semantic PRE-MAIN;
- rebase or replace branch.

## Required outputs

Write under:

`WORKER_RETURNS/EE-P2R6A/`

At minimum:

- `00_RETURN.md`
- `01_RUNTIME_IMPLEMENTATION_RECEIPT.json`
- `02_R4A_PREDICATE_AND_COMPOSITION_RECEIPT.json`
- `03_R5A_RELEASE_REALIZATION_RECEIPT.json`
- `04_FAIL_CLOSED_AND_REGRESSION_RECEIPT.json`
- `05_BROWSER_QUALIFICATION_RECEIPT.json`

Production code changes may touch only the smallest relevant `rawlsing_next/` runtime/evaluator/composition modules and tests.

## PASS terminal

`EE_P2R6A_PASS__ADOPTED_R4A_R5A_RUNTIME_CONTRACTS_IMPLEMENTED_GENERICALLY__FAIL_CLOSED_WITHOUT_CONCRETE_BINDING__READY_FOR_EXACT_BINDING_AND_AB_REQUALIFICATION`

PASS wakes HQ adjudication only.

Return final tip, exact modified blobs, test identities, governed court run/job/artifact, and any blocker.
