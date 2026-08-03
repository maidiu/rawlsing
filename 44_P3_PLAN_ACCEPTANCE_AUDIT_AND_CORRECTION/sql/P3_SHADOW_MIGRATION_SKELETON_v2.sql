-- Rawlsing P3 shadow migration skeleton v2. Not executable until a live repository is designated.
BEGIN;
-- 1. Acquire migration lock and assert target namespace is shadow-only.
-- 2. Apply p3_postgresql_compatible_ddl_v2.sql without its terminal ROLLBACK in a controlled migration copy.
-- 3. Load authority release and versioned vocabulary codes.
-- 4. Generate p3_enforce_vocab_code triggers from P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v2.csv.
-- 5. Load read-only upstream object references and exact release snapshot.
-- 6. Load P3 canonical artifacts in foreign-key order.
-- 7. Execute P3_DDL_VALIDATION_QUERIES_v2.sql and compare expected returns.
-- 8. Build V550J/V551J/V552J in shadow mode and write comparison return.
-- 9. On approval, append PROMOTED event and transactionally replace p3_runtime_promotion_pointer singleton.
-- 10. On any failure, ROLLBACK; prior pointer and authority remain unchanged.
ROLLBACK;
