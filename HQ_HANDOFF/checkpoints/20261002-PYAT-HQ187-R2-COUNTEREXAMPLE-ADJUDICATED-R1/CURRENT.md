# PYAT HQ187 — R2 COUNTEREXAMPLE UPHELD, RECORD CORRECTED

Status:
`R2_COUNTEREXAMPLE_UPHELD__M01_COURT_BINDS_PRE_C3_DECODER_CODEC__AUTHORITY_IS_C3_COURT_PLUS_C4C3__BLOCKERS_UNCHANGED_0_1_1_9__COUNTEREXAMPLES_NOW_1__HQ182_HOLD_UNLIFTED__RAW_SOURCE_EXECUTION_HELD`

Decision: `HQD-2026-10-02-187`

## Return adjudicated

R2 independent re-check returned at `afb1eb49b`, disposition
`MATERIAL_CORRECTION_REQUIRED`. HQ verified the branch: one return commit,
8 artifacts, zero `rawlsing_next/**` movement, HEAD matched the expected
`e00823a9`, anchor `dd008968` held at 23 commits over, no force-push.

## The counterexample is upheld

The reviewer was asked to try to break C1's withdrawal. It could not, but it
found a real defect in C1's *substitute* justification, and HQ confirms it.

`test_pre553_route_b_production.py` — 11 of the M01 court's 61 tests —
imports `rawlsing_next.pre553_physical_decoder` at line 29, and
`pre553_physical_decoder.py` imports `rawlsing_next.pre553_r5_codec` at line
21. Both are therefore inside the court's transitive closure.

Those two modules differ between every M01 binding and the freeze:

| Module | at `903c262e` | at `a1545aee` | at `46f3bec8` | freeze `8ff40d37d` |
|---|---|---|---|---|
| `pre553_physical_decoder.py` | `d2a074a4` | `d2a074a4` | `d2a074a4` | **`d3d828c1`** |
| `pre553_r5_codec.py` | `72f8f3c0` | `72f8f3c0` | `72f8f3c0` | **`6000a170`** |

All three of the final rebinds carry the pre-C3 decoder and codec. **No M01
court binding ever carried the C3-accepted bytes.** Both arrived with
`30686b18` "Integrate accepted C3 source-free repair".

So the M01 61/61 does **not** bind the freeze's exact closure bytes. Sol's
byte-identity statement remains true for the four files it names, and C1's
withdrawal stands. But it is not a closure claim, and neither was HQ's C4A
substitute offered as the replacement.

## Corrected authority basis

Authority for the decoder and codec at freeze bytes is **C3's accepted
six-file 55-test court plus C4C3's 55/55 twice**. HQ independently confirms
the freeze carries exactly the accepted C3 blobs:

- `pre553_physical_decoder.py` = `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`
- `pre553_r5_codec.py` = `6000a1704d713f65e07610d81e9b3fd8bdd515ca`

Both are two of the six pinned accepted C3 blobs, so they are inside the
authoritative C3 denominator directly.

The defect is in the **record**, not the evidence. Counterexamples go 0 to 1.
Stage blockers stay **0 freeze / 1 issuance / 1 live execution / 9 advisory**.

## Further corrections accepted

- **C2 residual class is BOTH**, not fingerprint-only. `narwhals` is absent
  from the 13-package `reproduce_command` and unpinned, so a re-resolve can
  select a different version. Bounded, off the C4 path, but not absent.
- **C4 count corrected: 6 of 8, not 8.** `expected_full_reads` and
  `expected_selected_reads` are present for SRC02, SRC06, SRC08, SRC12, SRC14
  and SRC26 only. **SRC27 and SRC35 carry neither.** SRC27 is the single
  governed full Route-B pass, so the most consequential read in the workload
  has no expected read counters bound in artifact 07. This **strengthens** R9.
- **C3 clarified**: 32/6/2/3 confirmed; 29 of the 32 are distinct; of 9 raw
  32-hex occurrences in text, 3 are prose in a narrative field.
- **C5 upheld**; `7dfb6...` is the only truncated identity value in the freeze packet.

## Reviewer disclosures, recorded

The reviewer caught its own vacuous pass — an initial MANIFEST extraction
guessed the field name and returned `None`, comparing `None == None`. It
dumped the record verbatim; the field is `blob_sha` and both blobs match.

It did **not** verify the 61/61 count itself, noting static counts of
11/4/14/30 against a claimed 32. HQ records that count as **unverified**.

It also recorded that the freeze and C4A are **not** ancestors of the review
branch, which diverges at `87029d34` and cites the freeze by SHA across
lineages. A verifier working only from HEAD cannot reach the freeze by
ancestry. Consistent with the commission; no effect on findings.

## Holds

Unchanged. C4 freeze unadopted. HQ182 hold unlifted. No locator, no warrant,
no raw source access, no production mutation.
