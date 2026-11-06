# Universal35 D r6 — independent closure and local-read boundary

**VERDICT: ACCEPT_SCOPED_ENGINEERING** for D r6 plus the instructed fresh-load composed local-resolver use, at frozen target `d054e4066715c0e87a063cb717cc9a6257a3933a`.

- D code: `a286fe469f9622f6370af8993fca283b2f1af2c4`
- Prior G review: `bc01712c111c7522d92bbd27e8a318453c4518e3` (`REVISE` ABBA)
- Prior F input: `5e2cfc568588944479c6c7b44b8db72c114b0828`
- Review branch: `codex/pyat-universal35-d-r6-local-read-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## Grades

- **D code: PASS_SCOPED.** Actual production-wrapper sourcefree probe: positive/restore 30 facts, 15 expected operations, 18 candidates, anti/op-anti true. The old ABBA shape (now decode-B, decode-post-B, consumer-A) refuses `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`; changed post-consumer decision and revoked-after refuse; revoked-before refuses; exact restore passes. No extra pre-call remains; the captured actual decode decision is the comparison baseline.
- **F cached instance: FAIL_SCOPED_LIVE.** Existing instance confirms valid 35 decisions and all tested request mismatches, but after live grant revocation or user-authorization change it still returns `CURRENT_GRANTED`; it caches grant/auth at construction and `_current` checks only the stored interval.
- **F fresh-load composed use: PASS_SCOPED.** A fresh default `LocalEngineeringResolver` per `resolve_current` loads the exact grant/auth before use: after grant revocation it refuses `SOURCE_READ_LOCAL_ENGINEERING_GRANT_CHANGED_OR_REVOKED`; after auth change it refuses `SOURCE_READ_USER_AUTHORIZATION_CHANGED`; missing auth refuses `SOURCE_READ_USER_AUTHORIZATION_MISSING`; valid fresh input remains accepted. Expected grant/auth SHA checks are not disabled. This is the instructed D actual-run adapter, and no product owner fix is needed for that use.

## Preserved evidence / limits

- Prior G held/unselected-Y positive and selected-missing refusal remain unchanged (9 B tests from R5); no eligible operation is dropped.
- Sourcefree wrapper positive and old ABBA negative are explicitly TEST_ONLY_SOURCEFREE; official F positive receipt `fdc6f3f9…`/`233d2272…` remains historical.
- Current route-qualified frontier 7/694/683/11 and 28 no-explicit sources; historical 20/991 non-F1 scope; route 676/4,705/249; plan 18,276/18,413/18,467.
- Local grant SHA `9e433cd9…` and auth SHA `18b2b571…` verified against the code expectations. Valid decisions preserve host `oldMac.lan`, purpose `UNIVERSAL35_ORIGINAL_ENGINEERING_RAW`, scope `RAW_OBSERVED_SAMPLE`, currentness, and retention/export limits.
- Actual original data, actual D original run, E/native handshake, all35 facts, native/S3/science and protected acceptance remain **NOT_RUN/HOLD**. No original source bytes were read, no full-estate/600 s rerun, no product/test/guide/progress/controller/protected edit.
