# PRE553 R5 long-sharded shadow implementation

Starting HEAD: `ab19862b9485741228dfa84f4c976c6110171065`.
Final commit: recorded after the final receipt commit in the Git history.

The candidate is contained to `rawlsing_next/pre553_r5_*.py`, `rawlsing_next/test_pre553_r5_*.py`, and this small receipt directory. It does not alter R4, the frozen decoder, C11 semantic/integrity/repository modules, I03, I05, I04, V553+, V3, or V2.

The implementation adds independently closed JSONL LONG_SHARDED members, streamed whole-member inventory/root sealing, bounded reopen/audit, cacheless exact scans, a carrier-neutral row stream, and an isolated generation-stamped publication CAS simulator. Typed values use versioned exact lanes with float bits, signed zero, integer escape, exact text, and explicit opaque escape. Vectorization is limited to validated finite float64 extraction; all other values use the scalar path.

The independent bounded subset ran 73 tests with exit code 0, including hostile codec cases, bounded stream/reopen/audit, destructive member corruption, benign relayout identity comparison, stale-generation/root-pin publication controls, and existing C11/authority/query/whole-machine regressions. The complete G0-G8 court was not run in this worker: no full independent source/C11 equivalence, increasing-N memory measurement, or frozen cacheless I03/I05/I04 commitment protocol was claimed. No full WVS7 or LiTS execution was run.

Recommendation: `R5_BLOCKED__SOURCE_PHYSICAL_EQUIVALENCE` pending the remaining G0-G8 court gates.

Required return token: `PRE553_R5_LONG_SHARDED_SHADOW_IMPLEMENTATION_RETURNED`.
