# S00CR findings and smallest bounded correction (review only; do NOT edit candidate)

## D1 — CRITICAL for producer-qualified value use: coherent rewritten counts retain stale producer refs

The author tests *intentionally* change original native synthetic channel counts (Q86B=1 Y0:1→2, Y1:3→2) and rehash the bundle, while preserving the old `producer_evidence_ref` string and `selected_world_contract`. The consumer computes 1/2 and reports success. **A positive conditional value-dependency test therefore simultaneously demonstrates that the consumer accepts numeric substitution under stale claimed upstream producer identity.** The hash authenticates only the rewritten self-consistent bundle.

**Minimal correction:** At the selected-world seam resolve an exact owner-issued producer result/value from an immutable (for synthetic, reproducibly rederived) root; compare every channel cell/count, condition denominator, native role and selected release/risk with that resolved result. In native 2×2 synthetic tests, bind the four-cell joint law to its synthetic `SelectedWorldContract` exact content identity, then refuse any changed channel law without a newly constructed selected-world contract and output evidence lineage. In a future real-source mode, use exact issued EmpiricalFact and consent/target-use refs, not an arbitrary caller dictionary.

## D2 — HIGH: internally conflicting numerical projections accepted

`_validate_bundle` and `compute_scenario` do NOT require `channel.value.raw_probability_exact_fraction` to equal recomputed Fraction(raw numerator, denominator). They also do not require `steps[].cells[cat].numerator` (or fraction) to match the actual numeric reads. A caller can set reported fraction to 100/101 while retaining raw count 3/4, or set `steps[].cells["1"].numerator=234` while leaving channels at 3; rehash locally and obtain `status=COMPUTED` with contradictory bundle and consumer output.

**Minimal correction:** canonicalize/recompute and compare every displayed fraction, all step geometry, positive/zero denominators, target topology, raw count closure and evidence refs. Refuse a mismatch before marking any value-used receipt. Use a canonical self-excluded digest, but do not treat recomputability alone as authorization.

## D3 — HIGH: historical S00 false contract remains an active downstream documentary authority hazard

The historical manifest `WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json` remains frozen with `RETAINED_SOURCE_CONDITIONED`, source-sounding `CH_01_DEMOCRACY_SUPPORT`/`CH_02_INSTITUTIONAL_TRUST`/`CH_03_DEMOCRATIC_ATTITUDES`, Likert 1–4 interpretations and a documentary 19,210 coexposure reference miscast as eligible complete-case. There is NO source-scientific warrant to adopt this. Critically, the inherited author test `test_s00_contract_manifest_exists_and_is_valid` continues to *assert these false labels are valid*; missing file on L01 sparse host produces FileNotFoundError; complete terrain would run that test without semantic invalidation.

The S00C consumer does not import or parse this manifest; it is not automatically corrupted by the file itself. But other consumers of the same historical manifest, tests, R3 plan or app binding can still read false assertions as source authority. The S00C code's scenario guard searches only exact uppercase `DEMOCRACY_SUPPORT`, `INSTITUTIONAL_TRUST`, `DEMOCRATIC_ATTITUDES` tokens, allowing lower/mixed case to label a valid synthetic numeric result as democracy support. It retains `SOURCE_FREE_SYNTHETIC` on output, mitigating but not eliminating display/consumer contamination.

**Minimal correction:** Separate authorized historical target/plan remediation must mark S00 original as `INVALID_SOURCE_SEMANTICS__HISTORICAL_REFERENCE_ONLY` and furnish a new native Q86B→Q86A binary citizenship-opinion target contract with correct use/risk and documentation. Consumers must bind exact contract type/id/version and source-permission evidence, not arbitrary scenario strings; reject any unissued S00 manifest regardless of casing and require separate classification for visual labels. Replace existing false-accepting manifest test only under an authorized contract-owner commission; S00CR may not modify it.

## D4 — MEDIUM: duplicated receipt provenance not independently witnessed

Read receipts are an improvement (`VALUE_READ_ONLY`→`VALUE_USED_IN_EXACT_CONDITIONAL`) but the use marking is still performed by the same consumer after it evaluates local values, without independent upstream resolution. On positive calculations the raw numerator and output fraction genuinely depend on read values, so do **not** misstate D4 as "receipt-only." Instead classify as local introspective logging, not externally authenticated source-use evidence. `distributions` is reconstructed directly from the bundle channels after arithmetic, not from the recorded read list; ensure full output field dependency coverage if needed.

## D5 — still intentionally HOLD: no actual retained GT2 use

`build_retained_gt2_bundle` always throws the explicit scientific HOLD. Canonical R5 Q86A/Q86B are binary citizenship-inclusion opinions, with distinct 9/997/998/-1 states and exact Q86B conditioner/Q86A target; original frozen 19,210 is a common coexposure risk carrier, not a demonstrated substantive complete-case denominator, weighted population estimator, national law, material causal mechanism or structural fact. Missing exact independently issued source-owned numeric aggregate, original routing/respondent/risk/permission, consumer target-use and custody. Do NOT fill with P04 synthetic 58 or homemade 2×2 counts.

## Ranked acceptance gate

1. Execute `test_hq284_s00cr_value_dependency_hostiles.py` in qualified L01 isolated candidate+test overlay and record casewise evidence. No silent pytest inference.
2. Correct D1 and D2 on a new authorized writer branch and pass repeated independent hostile court; preserve P04 and deterministic sourcefree fixtures.
3. Quarantine/replace old S00 contract only through its separately competent owner. Never mutate it as part of this review.
4. Independently approve only bounded source-free code after L01 produces full court and owner recomposition. Real GT2 mode remains hold until actual issuance and source-value consumption.
