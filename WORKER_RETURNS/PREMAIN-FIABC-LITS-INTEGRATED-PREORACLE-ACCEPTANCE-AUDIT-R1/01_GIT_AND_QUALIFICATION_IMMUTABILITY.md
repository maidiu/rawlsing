# Court 1 — Git / Qualification Immutability

## Result

**PASS**

## Worker-A ancestry

Baseline:

`4513eae0ec2c55c3252871c77cd52fc3dd0f07cd`

Worker A final:

`91cded28b252f1fe09c76d1bd954c53335178395`

Git comparison proves Worker A is 10 commits ahead of the exact baseline with the baseline as merge base.

Qualified integrated implementation:

`516643348181048381ebe732ac8ea748d9a82fd7`

Git comparison proves it is 11 commits ahead of Worker A with Worker A as merge base. Thus jurisdiction law was not discarded by a side-line replacement.

## Worker-B donor integration

Worker B final:

`6350ebefbd269e2deedbe90757f23383ba8a9bb8`

Worker B and Worker A diverge from the same baseline; Worker B is a donor, not an ancestor.

The integrated parity module retains **all 23 Worker-B functions**. Its only new helper functions are:

- `_sha256_text`
- `_selector_populations`

Worker-B parity tests: 10 named tests.

Integrated parity tests: 19 named tests.

All 10 Worker-B tests remain; the nine additions are selector-substrate / selector-freeze hostile tests.

Therefore the intended Worker-B substantive material was incorporated while Worker-A jurisdiction remained in ancestry.

## Qualified implementation → documented final

Qualified:

`516643348181048381ebe732ac8ea748d9a82fd7`

Final integrated tip:

`56d33a910ccf0df3c50f7bb053dbab57cad5b271`

Git comparison:

- 8 commits ahead;
- changed paths are exactly eight files under
  `WORKER_RETURNS/PREMAIN-FIABC-LITS-PREORACLE-INTEGRATED-CLOSURE-R1/`;
- no production code;
- no tests;
- no runtime packages;
- no court workflow/spec.

Therefore no production code changed after source-free qualification.

## Temporary court mutations are absent

The broad CI evidence tree used temporary qualification mutations in:

- `.rabochii/court_spec.json`
- `.github/workflows/rabochii-governed-bounded-court.yml`

The semantic candidate named by both focused and broad court specs is:

`9f12ebde3b0c3b074d219cdc1f9fb397475c2157`

Comparing that semantic candidate directly to `516643...` shows **no file differences**: the trees are identical.

At `516643...`:

- court spec blob = `95bceba63be84c502e3ec46a1b1a3039365ff50d`
- workflow blob = `a974469aa1d83514d896e3de591d7618310ca493`

Both are byte-identical to Worker A's pre-integration versions.

The final qualification commit itself is titled:

`Restore governed court workflow after source-free qualification`

and removes the temporary `pandas` test dependency, returning the workflow to `pytest` only.

No temporary CI/court-spec mutation remains.

## Governed P2X

Branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

still resolves exactly to:

`78caf7eb4396dd576cf478c860372b7e26455cd9`

This audit did not mutate it.

## Execution boundary

The two qualification jobs execute only bounded pytest courts. The audited Git changes contain no candidate-execution result and the governed P2X ref is unchanged.

This audit itself started no Candidate A/B/C process and no measured P2X process.
