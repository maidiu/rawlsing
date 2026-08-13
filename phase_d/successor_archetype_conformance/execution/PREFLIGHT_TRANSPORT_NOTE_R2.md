# Phase-D retry transport note R2

For the successor anti-erase retry, the encoded text wrapper is transport only and is not a governing integrity surface.

The materialized response-option CSV remains the governing frozen payload. Its existing byte-level integrity check, row count, variable coverage, frozen candidate order, semantic authority, routing truth, and unchanged validator continue to govern.

This note supersedes only the earlier instruction to fail on the encoded wrapper's own text-byte hash. Nothing else in the retry scope changes.
