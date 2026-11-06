# Universal35 C prebuilt-release/coordinate-hook review

**VERDICT: REVISE** at frozen C head `6f9e41f3aa85b6e26120e78744a72380f4d013d2`.

- Code: `8c5e8236ba08dca9d2e5921f938b3ce3d480e3bc`
- Prior C return read: `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-ORIGINAL-SCALE-20261106-R1/00_RETURN.md`
- A producer/test references: `bc84799edbeaefd7785e178a0aaacc94f76260fe`, `c84ea32de832f83656005f6e531cf837d1a58282` (F `dcb2ff81…`)
- Review branch: `codex/pyat-universal35-c-release-reuse-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Blocking — sealed prebuilt release is trusted without revalidation

Baseline `build_source_backed_c11_repository` reuses the prebuilt release and
preserves its exact release/replay refs. Wrong source SHA and wrong projection
identity are correctly refused. However, a sealed release modified via
`dataclasses.replace(prebuilt_release, semantic_release_hash="0"*64)` is
**accepted** and returned as a `C11LogicalRelease` with that zero release hash.
Only the stream's source-SHA string and caller-supplied projection-identity
string are checked; the release itself is not checked against the existing
validator/authority/replay binding.

This is the exact "source SHA + caller projection hash must not substitute for a
genuinely validated matching release" boundary. Use the existing typed-release
validator/binding to prove the attached release, or reject it; do not add a new
signature framework.

### Coordinate hook — partial

The hook selects exactly one `CoordinateSlotRule` by matching name and ordinal,
refuses empty/multiple mismatches, and the author's UNKNOWN-state fixture passes.
But it does not verify the rule's source qualification/authority/provenance:
a rule with the correct slot name/ordinal but foreign coordinate ref
(`urn:wrong:source`) is accepted into the projection. A source-UNKNOWN/MISSING/
DEFER state value is preserved, but a wrong-source rule can carry it. The actual
A-produced SRC15 rule and actual C adapter join remain NOT_RUN.

## AXES / TESTS

```text
pytest -q rawlsing_next/tests/test_pre553_original35_scale.py
# 2 passed in 0.97s

pytest -q rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
# 10 passed in 1.45s
```

- **Release reuse: FAIL/REVISE.** Exact baseline ref/replay reuse works; source/
  projection mismatch refuses; tampered sealed release accepted.
- **Coordinate hook: PARTIAL.** Exact selection/ordinal and UNKNOWN state pass;
  source-qualified identity is not enforced.
- **Scale evidence:** author 28+3 PASS may be reused where unaffected; no
  favorable timing claim. SRC10 first-materialize 169.265 s + compile >425.861 s
  at the 601.8 s ceiling; SRC09 materialize >347 s; actual facts 0. No full-plan
  success or 600 s improvement claimed.
- **Limits:** no original reads, SRC15 join, full-estate, native/S3/science,
  protected adoption, source grant, or C fix. No code repair in this review.

No new validator/signature framework, source/native semantics, or permission was
introduced by the review.
