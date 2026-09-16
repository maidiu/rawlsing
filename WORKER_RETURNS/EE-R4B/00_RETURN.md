# EE-R4B — A/B/C exact executable-owner registry

Status: `PASS__EXACT_ABC_EXECUTABLE_OWNER_AND_INVOCATION_BINDINGS_RECOVERED`

Worker: `EE-R4B`  
Branch: `agent/rabochii-prev3-ee-r4b-abc-executable-owner-registry-r1`  
Commission tip: `b1c5ddeead65774af82cefffa30d9ce0d2f0f6b8`

## Authority

Current HQ resolves to checkpoint `20260916T1334-0400`, handoff `f9d94c83d8a1cdc99f2ac04d3a42f09e693952ab`, semantic PRE-MAIN `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

The binding R3G blocker was identity/configuration only. The accepted qualified A/B/C intake is SHA-256 `906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88`; the accepted HB04 common-harness freeze is SHA-256 `138482116b566482075e191800229f81357541d674646552e8c269e7640a755e`.

## Holding

The bounded accepted lineage resolves all three candidate classes positively. The common accepted harness execution tree is `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, qualified by HB04 return `46acf0b162bdcac5f47ce9cce0d9bb1d039fae2d`. Its exact candidate CLI owner is `rawlsing_next/as4/run_candidate.py` blob `0acb4cd17906b1c316c5ae381d3214ea98ac5baa`; transport/session dispatch is `rawlsing_next/as4/protocol.py` blob `590da3a2cc54666bd9786130409170b73310a700` and the exact intake loader is `rawlsing_next/as4/loader.py` blob `f608f72f711610ef6d07fd7c96f450a6ba2cac2a`.

The exact already-qualified HB04 CLI template is:

`python -m rawlsing_next.as4.run_candidate --candidate {A|B|C} --workdir {WORKDIR} --output {OUTPUT} --freeze <49A_HB04_QUALIFIED_ABC_INTAKE_FREEZE_R1.json> --bounded-fixture`

For real-source execution, the accepted callable entrypoint is `rawlsing_next.as4.protocol.prepare(candidate, HB04PreparedSource(... exact production bindings ...), loaded_manifest, workdir, allow_bounded_fixture=False)`. The accepted CLI intentionally gates real-source preparation separately; this return does not invent a new production CLI or adapter.

### A

Physical meaning: `R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE`.

Exact candidate owner: `rawlsing_next/pre553_r5_source_backed_adapter.py`, blob `d4915e7e6755ba1850756aebff72f982f73a332b`, at the accepted integrated HB04 owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`. Route-A full qualification is `fa340c007f5f9d2835e6117daf1dc9545a173bc9`. Immediate physical pins include compact carrier blob `92e364b31eaf27be1bca2081eff65f6ffb779c3d`, single-pass Authority-69 audit blob `ffb063b93c86e215604eecb29a9545c7efdff399`, and the HB04-integrated source-backed facade blob `7c509c2098d0030f253344eb3f682471378812a8`.

Harness binding: common entrypoint with candidate `A`; protocol dispatches to `build_r5_source_backed_c11_repository`. The exact Route-A implementation blob is also hard-pinned by the qualified 49A intake, so this is the current accepted candidate instance rather than a later unqualified R5 variant.

### B

Physical meaning: `SOURCE_BACKED_VIRTUAL_C11`.

Exact harness-facing owner: `rawlsing_next/pre553_source_backed_c11_facade.py`, blob `7c509c2098d0030f253344eb3f682471378812a8`, at accepted integrated HB04 owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`. The accepted real-source Route-B production execution/seal is `40a0a0529fa78765c7fc87f7e1f12260a2335f72`, using qualifying driver commit `f43c4be11d4f8fa98f538727337ec075d99d03bc`; the exact production driver path is `.../WORKERS/B16_C05R2B_REAL_LITS1_PRODUCTION_I05_R1/01_C05R2B_PRODUCTION_EXECUTION_DRIVER.py`, blob `26d1e3ede625499a26c712844bffaff4d77e13da`, effective source SHA-256 `59ce6903776df5f5b17bc074b15d9ae06334a5a1c30fad91096fc3fb6a014a3f`.

Harness binding: common entrypoint with candidate `B`; protocol invokes `build_source_backed_c11_repository(..., cache=None)`. The physical configuration retains zero persistent transformed empirical payload and zero retained transformed accelerator surfaces across the accepted session boundary. Immediate pins include the common protocol, source-backed facade, and accepted physical decoder blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`.

### C

Physical meaning: `SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS`.

Exact owner: `rawlsing_next/pre553_route_c_accelerators.py`, blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`, at accepted integrated HB04 owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`. Route-C full qualification is `9e6b537c636c6d28b00e2345221a5dbbf2491190`, over execution tree `e7007ff50d1e8577f522d8691486f55c3679dbcb`; exact qualification driver blob `9ed1a68300453bfcd4af4877bab397ed00b0e0e6`.

Harness binding: common entrypoint with candidate `C`. Exactly two accelerator surfaces are permitted: `CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE` and `CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK`, with pinned `pyarrow==25.0.1`. They are optional, deletable, regenerable execution representations only. The mandatory semantic core remains exact source + governed projection -> source-backed C11 -> unchanged exact I03/I05 engines; extra cache/index surfaces are forbidden. Candidate hash: `a476e6e44c21b8029ae5d3e6d387428a5fa19549a2126d61aae7c71c50c64a3c`.

## Stop rule

A: positive. B: positive. C: positive. Further genealogical search is therefore forbidden by the commission stop rule.

No adapter was implemented. No OP001–OP022 operation was run. No A/B/C comparison or ranking was run. No candidate was redesigned. MAIN and semantic PRE-MAIN were not modified.

Terminal: `PASS__EE_R4B_EXACT_ABC_OWNER_REGISTRY_FROZEN__READY_FOR_BOUNDED_R3G_SUCCESSOR_WITHOUT_FURTHER_GENEALOGICAL_SEARCH`
