# FIABC LiTS R1 source-backed return

**Terminal:** `BLOCKED__CANONICAL_ROLE_QUERY_PREDICATE_CLOSURE_VALIDATION_FAILED`

Executed from pinned implementation `8e35e9b0d41c6a404a84ea511761d5123323af35` on the exact local source path. The producer passed its source identity and shape gates, decoded once, and wrote the current I05 precheck. Its aggregate envelope matched the expected current result: 50 candidates, 77 roles, 49 `EVALUATED_SUPPORTED`, 1 `EVALUATED_VALID_EMPTY`, and 60 supported empirical facts. Candidate A/B/C processes and outputs were both zero.

The producer then failed before writing the v3 checkpoint:

`FinalOracleProducerError: LiTS role predicate/query preimage substitution or omission`

The exact traceback is in [sourcebacked_command_stderr.log](sourcebacked_command_stderr.log). The retained precheck is [current_i05_precheck.json](court/oracle_producers/LITS_I/current_i05_precheck.json), SHA-256 `1ffbcb0f02e0c6b89a09cb255ce9342cbcb162ab2a1302de0ca8ade24990eed6`. It is only a compact precheck. Full EmpiricalFact, EmpiricalQuerySpec, predicate, authority, release, replay, exact-ref, and role-binding preimages did not survive the process exit.

## Required follow-on dispositions

- Checkpoint write: failed validation before write; no fresh checkpoint exists.
- Zero-source resume: not run because no complete checkpoint exists. No source-free repair input contains the missing full preimages and execution receipt.
- LiTS oracle: not written or verified.
- ASTRA regression comparison: not reached; it follows checkpoint write in the pinned producer.
- FF02: not ready; full canonical objects and provenance closure are absent. FF02 and structural admission were not run.
- Candidate neutrality: preserved; no Candidate A/B/C process or output.
- Source access: no separate operator prehash, no retry, and no source reread after the producer returned its failure. See [source_access_telemetry.json](source_access_telemetry.json) for pinned-code path accounting; OS syscalls were not traced.

The source-free work stops at this exact closure blocker. No semantics or expected counts were altered, and the protected execution branch was not advanced.
