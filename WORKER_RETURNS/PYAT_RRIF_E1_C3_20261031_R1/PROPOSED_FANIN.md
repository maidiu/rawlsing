# PROPOSED FAN-IN — RRIF-E1 C3 D01/D02 CURRENT-DECODER REPAIR

## Proposed integration allowlist

| Path | Blob | Change |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` | modify |
| `rawlsing_next/pre553_r5_codec.py` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` | modify; byte-equal to accepted C3 codec |
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | add |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | add |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | add |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/00_RETURN.md` | `SELF_REFERENTIAL_NOT_EMBEDDED` | add |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/ORIGINAL_TO_CURRENT_SEMANTIC_DIFF.md` | `b28a5fe793b7cc64a4bdce52cf343a59bd6edeb4` | add |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/POSITIVE_AND_NEGATIVE_TESTS.md` | `9fa4531663ca0b534e55c9c0d201baf02c7b4a04` | add |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/SOURCE_RIGHTS_AND_SCOPE.md` | `bdd0b1bcff089364b347297b9dc034b5a12434ea` | add |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/PROPOSED_FANIN.md` | `SELF_REFERENTIAL_NOT_EMBEDDED` | add |

The three non-self-referential documentation blob IDs are final. `00_RETURN.md` and `PROPOSED_FANIN.md` cannot embed their own final blob IDs without changing those IDs; their authoritative blobs are the committed tree entries for the return commit.

## Commits and readback

- Startup/PREMAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- `2edf5df01fd9de66abca2733c0878c4ea981707d` — code and tests
- `1401bc7e0f5988bdeda9250e56ffe9fe26e306b1` — codec byte alignment to `6000a1704`
- `90c1c0eefc66263981ba9066faab22c35dc57f9f` — minimal D01 patch surface; final implementation commit
- Remote readback for `90c1c0eefc66263981ba9066faab22c35dc57f9f`:
  `90c1c0eefc66263981ba9066faab22c35dc57f9f`
- Final return-documentation commit and its remote readback are reported in the execution return.

## Exact production patch

Diff from startup `8e44ca9c751049d65e6def47600b5c073ee04b29` to final implementation `90c1c0eefc66263981ba9066faab22c35dc57f9f` (`git diff -U0`; zero context is used only to avoid markdown trailing-whitespace artifacts, the change set is exact):

```diff
diff --git a/rawlsing_next/pre553_physical_decoder.py b/rawlsing_next/pre553_physical_decoder.py
index 8732e34d0..d60e092f9 100644
--- a/rawlsing_next/pre553_physical_decoder.py
+++ b/rawlsing_next/pre553_physical_decoder.py
@@ -27,0 +28,2 @@ from typing import Any, Iterator, Mapping
+from rawlsing_next.pre553_r5_codec import normalize_decoder_physical_value
+
@@ -29,0 +32 @@ COMPATIBILITY_ONLY = "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUT
+SOURCE_DECLARED_ENCODING_ONLY = "SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY"
@@ -41,0 +45,6 @@ COMPATIBILITY_ALLOWLIST: Mapping[str, str] = {
+DECLARED_ENCODING_ALLOWLIST: Mapping[str, str] = {
+    "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2": "BIG5",
+    "5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2": "WINDOWS-1252",
+    "66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec": "WINDOWS-1252",
+}
+
@@ -163 +172 @@ class PhysicalSourceIncidence:
-                    raw = _jsonable(value)
+                    raw = _physical_value(value)
@@ -418,0 +428,16 @@ def _jsonable(value: Any) -> Any:
+def _physical_value(value: Any) -> Any:
+    """Preserve exact decoder-native naive date/time through the opaque R5 seam only."""
+    import datetime as _dt
+    if type(value) in {_dt.datetime, _dt.date, _dt.time}:
+        return normalize_decoder_physical_value(value)
+    if hasattr(value, "item"):
+        try:
+            item = value.item()
+        except Exception:
+            pass
+        else:
+            if type(item) in {_dt.datetime, _dt.date, _dt.time}:
+                return normalize_decoder_physical_value(item)
+    return _jsonable(value)
+
+
@@ -509,3 +534,6 @@ def _compatibility_config(source_sha: str, encoding: str | None) -> dict[str, An
-    if expected != encoding:
-        raise DecoderError("encoding override is not in the frozen exact SHA/config allowlist")
-    return {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}
+    if expected == encoding:
+        return {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}
+    declared = DECLARED_ENCODING_ALLOWLIST.get(source_sha)
+    if declared == encoding:
+        return {"encoding": encoding, "authority_status": SOURCE_DECLARED_ENCODING_ONLY}
+    raise DecoderError("encoding override is not in an exact SHA/config representation allowlist")
@@ -810,0 +839,2 @@ __all__ = [
+    "DECLARED_ENCODING_ALLOWLIST",
+    "SOURCE_DECLARED_ENCODING_ONLY",
@@ -821,0 +852 @@ __all__ = [
+    "_physical_value",
diff --git a/rawlsing_next/pre553_r5_codec.py b/rawlsing_next/pre553_r5_codec.py
index 72f8f3c03..6000a1704 100644
--- a/rawlsing_next/pre553_r5_codec.py
+++ b/rawlsing_next/pre553_r5_codec.py
@@ -9,0 +10 @@ from decimal import Decimal
+import datetime as _dt
@@ -37,0 +39,42 @@ class R5OpaqueValue:
+def opaque_decoder_value(value: Any) -> R5OpaqueValue:
+    """Preserve exact built-in naive decoder date/time objects as opaque bytes only."""
+    if type(value) is _dt.datetime:
+        if value.tzinfo is not None:
+            raise R5CodecError("timezone-aware datetime requires a separate explicit decoder carrier authority")
+        payload = struct.pack(
+            ">HBBBBBIB",
+            value.year, value.month, value.day, value.hour, value.minute,
+            value.second, value.microsecond, value.fold,
+        )
+        return R5OpaqueValue("python.datetime.datetime@1", payload)
+    if type(value) is _dt.date:
+        return R5OpaqueValue(
+            "python.datetime.date@1",
+            struct.pack(">HBB", value.year, value.month, value.day),
+        )
+    if type(value) is _dt.time:
+        if value.tzinfo is not None:
+            raise R5CodecError("timezone-aware time requires a separate explicit decoder carrier authority")
+        payload = struct.pack(
+            ">BBBIB", value.hour, value.minute, value.second, value.microsecond, value.fold
+        )
+        return R5OpaqueValue("python.datetime.time@1", payload)
+    raise R5CodecError(f"unsupported opaque decoder value type {type(value).__name__}")
+
+
+def normalize_decoder_physical_value(value: Any) -> Any:
+    """Recursively replace supported decoder date/time objects with opaque carriers."""
+    if type(value) in {_dt.datetime, _dt.date, _dt.time}:
+        return opaque_decoder_value(value)
+    if isinstance(value, tuple):
+        return tuple(normalize_decoder_physical_value(v) for v in value)
+    if isinstance(value, list):
+        return [normalize_decoder_physical_value(v) for v in value]
+    if isinstance(value, Mapping):
+        return {
+            normalize_decoder_physical_value(k): normalize_decoder_physical_value(v)
+            for k, v in value.items()
+        }
+    return value
+
+
@@ -228,0 +272 @@ __all__ = [
+    "opaque_decoder_value", "normalize_decoder_physical_value",
```

Final production diffstat: `2 files changed, 79 insertions(+), 4 deletions(-)` (decoder `35/4`, codec `44/0`).

## Fan-in requirements

1. A different hostile reviewer must inspect the exact final branch commit and re-run the declared sourcefree commands.
2. The integrator must apply only the five allowlisted project paths plus the five return documents; never replace the current decoder with the historical candidate.
3. G01, PR526 custody, source-use rights, timezone-aware carrier authority, issuer/use, and science remain outside this fan-in.
4. `#580`–`#584`, PREMAIN/main, Sorok, native/protected source, and other worktrees remain untouched.
5. No PR or automatic merge is proposed by this worker.

Terminal: `RRIF_E1_C3_D01_D02_CURRENT_DECODER_REPAIR__SOURCEFREE_SELECTED_GREEN__G01_PREEXISTING_HOSTILE_RED_HELD__INDEPENDENT_REVIEW_REQUIRED`
