# P3A task return

Status: `BLOCKED_EXECUTION_EXPOSED_CONTRACT_DEFECT`.

Completed: v27 checksum and 33/33 verifier; corrected 13,127-row participation/workset mismatch; exact DDL rollback smoke on real PostgreSQL; one-line COMMIT derivative install; catalog proof of 75 tables in `p3a_v27_shadow`.

Blocker: live execution of delivered `P3_DDL_VALIDATION_QUERIES_v7.sql` fails at `q17_candidate_event_contiguous` with SQLSTATE 42803 because `candidate_family_id` is selected while grouping by `candidate_revision_id`.

No real candidate packet was generated and no canonical J-family authority was authorized.
