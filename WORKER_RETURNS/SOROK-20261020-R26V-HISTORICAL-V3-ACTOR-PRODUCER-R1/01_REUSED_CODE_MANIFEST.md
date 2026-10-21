# R26V reused-code manifest

- BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae`: staged `bp2p4/` and vendor **code**; the origin `vendor/source_manifest.json` has 150 files, but upstream `tests/` were excluded from this candidate to keep unproven upstream courts out of the changed-gate scope. Exact origin manifest is in `evidence/bp2p4j_vendor_source_manifest.json`.
- BP2 `5065e2e6934e9d5bca800cbf88c79e461bcf2393`: `bp2_joined` producer/ports/binding and BP1/G18/C9R/C8 vendor.
- BP4 `d868e82c7c83def2df18295244d93af9706e647f`: C10/C12/M6/A0–A3 product.
- BP1 `vendor/bp2/vendor/bp1/bp1/{composer,ledger,source,canon}.py`: actor source/ledger/composer.
- G18 `vendor/.../lab_sgi1/*`: material/history receipts.
- C8/C9R/OUT9 vendor: BP2 C8 keyed journal, C9 target store, E1/E2 ports.
- Live `rawlsing_next/m6_actor_safe_expression.py` and `v3_psepf_zero_positive_guard.py`: BP4 pinned live modules, unmodified.

No upstream file was edited. `historical_actor_producer._patch_actor_builder` changes only the **in-process function reference** `bp2_joined.producer.build_two_actor_life`; source bytes remain exact. `bp2p4.reunion._assemble` and `bp2p4.product.JoinedProduct` are used as the real chain.
