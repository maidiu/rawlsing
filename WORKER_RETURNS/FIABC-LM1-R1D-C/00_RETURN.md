# FIABC-LM1-R1D-C return

Terminal: FIABC_LM1_R1D_C_HOSTILE_COURT_COMPLETE__LAWFUL_REPAIR_CLASS_AND_MINIMUM_RERUN_PROVED

## Court disposition

Exactly one bounded repair class survives the hostile court:

- Candidate 1: PASS — use the already-accepted R5 typed-value representation as physical identity/raw-witness material at the C11 physical seam while leaving generic semantic canonicalize() unchanged.
- Candidate 2: REJECT — globally admitting Python floats into semantic canonicalize() widens semantic identity authority and destroys the existing float prohibition.
- Candidate 3: REJECT — repr()/Decimal/Fraction/string conversion is a semantic/numeric conversion, not preservation of the exact physical state, and is not authorized merely to make the consumer pass.
- Candidate 4: REJECT — NaN/Infinity may not be reinterpreted as None, missing, UNKNOWN, or any other semantic state.
- Candidate 5: REJECT — dropping non-finite cells destroys physical completeness and replay.
- Candidate 6: NOT AN INDEPENDENT SURVIVOR — an opaque token is lawful only if it is exactly the accepted R5 typed representation (or its canonical byte serialization). In that form it collapses to Candidate 1. A new opaque encoding would create a competing physical codec without authority.
- Candidate 7: no materially distinct accepted mechanism was found. The already-existing R5TypedValueCodec.encode()/typed_key()/canonical_bytes() mechanism is evidence for Candidate 1, not a second class.

## Exact boundary proved

The accepted R5 codec already preserves physical distinctions for finite float64 bits, signed zero, decoder-observed NaN state, positive and negative infinity, bool/int separation, int/float separation, and strings such as "inf". It explicitly refuses to fabricate lost NaN payload bits.

The current C11 facade violates the boundary by feeding decoded cell.raw_value into pre553_empirical_objects.canonicalize() in physical_value_binding_key, raw response witness handling, and raw coordinate witness handling. Generic canonicalize() expressly forbids all Python floats because it owns semantic identity.

The lawful repair is therefore narrow:

1. physical binding identity is derived from deterministic R5 typed physical material, not semantic canonicalize();
2. raw response and coordinate witness fields carry deterministic typed physical witness material;
3. semantic/canonical values continue to use the existing governed semantic canonicalizer and remain unable to acquire binary-float semantics without authority;
4. weight semantics remain governed by existing weight rules; the repair changes the physical key/witness seam, not the estimand or missingness contract;
5. unprojected physical cells remain untouched.

## Existing carrier holding

The accepted R5 root remains:
7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd

Logical stream remains:
076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba

Member inventory remains:
04dce8c3e942fc81a0558354c21a4b4a56faab417ce362657286f978b6686703

Rows/members remain 34,745,595 / 2,121.

No physical member rebuild is justified by this court. The accepted Route-A adapter already performs single_pass_full_audit while reopening the existing root before projecting C11, so the minimum recovery trial may begin at CURRENT CONSUMER ADMISSION after the narrow C11 seam repair and synthetic hostile regressions. Any consumer-facing identities/receipts whose currentness determinants include the repaired C11 code/runtime binding must be regenerated or resealed afterward; that does not authorize rebuilding R5 members.

## Execution boundary

This worker used GitHub/browser evidence only. It did not open LiTS bytes or /tmp carrier bytes, rebuild R5, execute Candidate A/B/C, run I03/I05, or run measured P2X.

Regression status: TESTS_AUTHORED__NOT_EXECUTED.

Required detailed artifacts:
- 01_CANDIDATE_REPAIR_COURT.csv
- 02_HOSTILE_IDENTITY_CASES.json
- 03_REQUIRED_REGRESSION_COURT.md
- 04_MINIMUM_RECOVERY_RERUN.md
- RETURN.json
