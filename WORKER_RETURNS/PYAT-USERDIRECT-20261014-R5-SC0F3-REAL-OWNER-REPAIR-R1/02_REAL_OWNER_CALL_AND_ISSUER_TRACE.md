# Actual owner call and issuer trace

The final six full captures each contain one completed call to all three required native functions (18 completed calls across these captures). This count excludes other tests and earlier iterations. Real source/license issuance remains HOLD; all calls here consume sourcefree synthetic inputs.

| Capture | Actual cell counts / denominator | Used-object append events |
|---|---|---|
| baseline_A | {'cells': {'no': 6, 'yes': 54}, 'denominator': 60} | 262 |
| baseline_B | {'cells': {'no': 6, 'yes': 54}, 'denominator': 60} | 262 |
| changed_A | {'cells': {'no': 10, 'yes': 50}, 'denominator': 60} | 262 |
| changed_B | {'cells': {'no': 10, 'yes': 50}, 'denominator': 60} | 262 |
| reverse_A | {'cells': {'P1': 54, 'P2': 8}, 'denominator': 62} | 264 |
| reverse_changed_A | {'cells': {'P1': 50, 'P2': 8}, 'denominator': 58} | 260 |

Every capture retains actual argument material (including repository object preimages and typed authority/query/witness material), argument digest, actual returned material/digest, imported module path relative to this repro, and exact Git source blob. `repro/runs/candidate__r5/execution.json` independently inventories actual imported `module.__file__` bytes. `source_manifest.json` identifies the original commit/path for each predecessor byte. There is no digest of the word `imported` standing in for a call.

The callback watches the imported functions’ exact Python code identities, records call and return events, and restores the prior profiler in `finally`. It separately watches the empirical evaluator’s actual `_UsedObjectAccumulator.append` to retain objects that the evaluator consumed; this is provenance observation, not another probability estimator.

The native forward counts change 54/6→50/10 at denominator60. Both consumers read the resulting geometry, and both physical providers produce identical complete results for each law. Structural-world values/support remain independent. Reverse calls build a different predicate/target through the existing native fixture; their denominators are62 and58, not the forward60. The strict receipt’s options dereference to real native cells including exact fractions.

The TEST_ONLY owner contains fixed records, source catalog and two fixed response-law constructors. No caller may register or pass a native registry/repository into the new adapter. A copy of a known fixed test permit can be presented only for its exact fixed scope; altering identity/type/scope/target/risk/operation/time fails. The old frozen enrollment API is retained as evidence and for serializer import closure; an actual self-registration attack against it cannot grant anything in SC0F3. This is separation from untrusted caller data, not independent authorship or hostile-host cryptographic attestation.

Positive TEST_ONLY warrant records bind native source/release/target/risk refs as well as reversed denominator, world source/release, operation, knowledge-asof, not-before, expiry and revocation. Dates are intentionally active: use after the recorded grant window holds. Earlier knowledge exception is one explicitly hypothetical fixed test record with source/release/content/time verification; arbitrary non-null strings or changed world contents refuse.

The exact old original-source/operation permission is not issued. Original-source demand fails the active catalog gate (`DEMAND_CLOSURE_INCOMPLETE`); the owner action is `HOLD_ORIGINAL_SOURCE_NATIVE_RELEASE_AND_OPERATION_GRANT_UNAVAILABLE`. No model, actor, original data or canonical operation is implied by the local runner.
