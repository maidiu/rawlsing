# R56-R02V — RESUME CHECKPOINT

**State:** Finite independent review pass complete. Verdict `REVISE` for the
normalized mapping collision. No production/science/authority acceptance.

**Candidate:** `236fd4d1064f7c14113616db300c955294a474ac`
**Reviewer branch:** `agent/rabochii-pyat-r56-r02v-independent-projection-review-r1`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing/R56-R02V-independent-projection-review-wt`
**Reviewer session:** `ses_e9dea5a24ffeBtsLScgC81lfet` (OpenCode, opencode-go,
deepseek-v4.1-flash, variant max)

## Immediate state

- 15/15 author focused tests still pass.
- 42/42 retained facade/query tests still pass.
- 7/7 independent positive/consumer tests pass.
- 2/2 independent defect reproducers fail as expected (`DID NOT RAISE`).
- Proof lint PASS; proof witness 2 claims PASS with assertion-level RED.
- Adapter unchanged: SHA-256 `2cf5e98bc29081678c364d3ff591c71f11ce7ebf3564419af8a26f5f04113b64`.

## Defects handed back to the same R02 implementer

1. **D1:** normalize mapping values before the duplicate-respondent-key check;
   reject a plan whose normalized values collapse two source respondents onto
   one C11 respondent. Current reproducer:
   `evidence/defect_normalized_respondent_key.py`.
2. **D2:** normalize mapping keys before building the token key map; reject
   duplicate normalized source keys instead of silently taking the last value.
   Current reproducer: `evidence/defect_ambiguous_source_key.py`.

After repair, rerun:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -m pytest \
  rawlsing_next/tests/test_universal_source_projection.py -q -rA
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint \
  rawlsing_next/tests/test_universal_source_projection.py
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  rawlsing_next/tests/test_universal_source_projection.py.proof.json --root .
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -m pytest \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_empirical_query.py -q -rA
```

Expected after repair: 24/24 focused tests pass; author 15 and retained 42
remain green; the two defect tests transition from RED to PASS.

## Non-blocking follow-ups

- Validate an exact order key for `REPEATED_EVENT` occurrence bindings before
  C11 release construction. Current I03 fails closed with
  `INTEGRITY_FAILURE`/`UNRESOLVED`, not false support.
- Make the repeated-vs-scalar source shape explicit; an omitted plan currently
  follows the S1 row path and cannot be detected from a selected response rule.
- Name/export the transformed `physical_stream` explicitly; it is not the raw
  decoder stream, and strict declaration receivers reject the envelope.
- Replace the author's `domain_from_bundle()` test oracle with the prospective
  source-derived domain added by this review.

## Do not

- Do not claim R00E gate integration; it was not run.
- Do not claim original35/N11/N12, production adoption, protected CI, or
  R03/compiler/lowering.
- Do not edit the reviewer's return root or overwrite the author's return.
