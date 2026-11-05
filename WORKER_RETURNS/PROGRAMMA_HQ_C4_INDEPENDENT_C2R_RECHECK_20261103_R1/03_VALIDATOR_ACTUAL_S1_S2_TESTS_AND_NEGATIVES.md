# C4 R2 — Python validator independent source inspection

Subject `CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_three_frontdoors.py@45f327a9086b4c95d0807da0774742b9ed8a626a` blob `9442c623a88d15ee5adfce21911ba4a14ee69afa`; manifest blob `d99c2031eea888d1abbeba932cc1ed27fc0231c2`.

**Observed S1:** lines 12,23–29 parse stable tagged IDs; 39–56 enforce three court blocks and five *nonempty* fields; 58–100 compare manifest-defined IDs, 20 shared body copies, eight enumerated untagged bodies, passports and status strings. Lines 108–124 resolve Git commit:path blobs for *manifest-listed* source laws. No ref returns REVALIDATION_REQUIRED; pinned-only represents static-only pass, live NOT_VERIFIED. Actual Python commands were not run.

**Material M4 defect:** loop `for source in manifest["source_laws"]` at line 114 does not enforce an independently pinned complete law path set. An edited empty list evades all original/current law comparisons and reaches SELECTED_SOURCE_PARITY_PASS (line 121) with a selected ref. Likewise source+manifest synchronized untagged section deletion escapes an inventory defined only by the editable manifest. This is static control-flow proof, **not** executed mutation evidence. Nonempty placeholder court fields remain a semantic-review limitation.

**Source identities:** 15/15 listed original blobs independently matched @773bb; just 11/15 equal their original pins at current protected @4edc45f. Current selected law must be revalidated.

**S2_EXECUTION=NOT_RUN.** No independently qualified authorized full local Rawlsing checkout; `/mnt/data` is not its Git repo. No python3 invocation, pytest, stdout/exit, mutation/restore or S3 result was performed. Qualified owner must run pinned-only, no-ref exit2, selected law change exit2, commission missing-field, bilateral 00D, shared drift, IDs, eight untagged, and new synchronized-manifest-omission negatives on a disposable exact checkout. No JS imitation passed off as S2.

**VALIDATOR_S1=REVISE.**