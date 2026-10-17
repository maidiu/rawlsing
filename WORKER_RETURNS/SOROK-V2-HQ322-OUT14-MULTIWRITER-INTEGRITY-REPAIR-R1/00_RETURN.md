# OUT14 — implementation-candidate evidence, authorization HOLD

Sealed startup: `ddf7f1550d76c8b94661f089631ba67432c37ee1`; branch `agent/rabochii-sorok-v2-hq322-out14-multiwriter-integrity-repair-r1`.

This source-free, return-local candidate binds writer_version to state via `version_state_digest` over canonical `schema/state/writer_version`, rejects malformed/missing/noncanonical journal versions without zero-coercion, checks accepted-ledger preservation and provides *actual* SIGKILL injection hooks alongside the historical os._exit(79) controls. The accepted OUT9 source and frozen OUT12/OUT13 tests are untouched.

**Binding limitation:** the accepted original Journal.commit remains independently callable without locking/version checking. Existing accepted/legacy writers can overwrite an earlier version and remove the version envelope. Subsequent candidate recovery now detects the incompatible receipt, but **cannot prevent the prior unauthorized overwrite**. The unkeyed envelope hash is integrity checking, not writer authentication; full valid-envelope replay/forgery requires an external trusted version anchor/authority. Hence `SOURCEFREE_AUTHORIZATION_BYPASS_UNCLOSED`: **NOT ACCEPTED; OWNER_REQUIRED** to close all legally callable writer paths.

**Execution evidence status:** Python 3.13.5, pytest 9.0.2, POSIX flock, subprocess verified locally. GitHub connector reads pinned sources but does not mount them in this Python sandbox; private GitHub cannot be directly cloned here (DNS unavailable). Neither the original 272, OUT12 nine, OUT13 23, nor new OUT14 tests have been claimed as executed in this return. Their inherited historical results remain documentary ONLY: OUT13 reported 270 PASS / 2 historical RED; 9 PASS; 23 PASS. No freshly invented counts. The new test file is unexecuted candidate code and requires a qualified exact pinned source staging before acceptance.

No power-loss, production ADP019, actor execution, exactly-once delivery, V3 or I2 adoption is claimed. Separate I2 review belongs to HQ after an executable repair, and owner resolution of the legacy write-grant is still required.
