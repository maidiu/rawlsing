# R08 R8 coverage / limits

| Surface | Result |
|---|---|
| live first resolve with legacy binding pins | SUPPORTED 54/6/60 |
| identical cache hit | UNKNOWN / LEGACY_BINDING_PINS_REQUIRE_MIGRATION |
| wrong descriptor pin cache hit | UNKNOWN / CACHE_OWNER_DESCRIPTOR_NOT_PINNED |
| normal cache hit | SUPPORTED 60, signed descriptor/envelope unchanged |
| legacy import/export | explicit migration refusal preserved |
| native positives | 54/6/60 and 54/16/70 unchanged |
| descriptor owner inventory | 13 classes refuse; pristine restores 60 |
| cold verifier-only replay/re-export | signed positive preserved |
| status controls | observed zero, ZERO_SUPPORT, valid products, Z denom16 |

R61AF normal form, no-admission transport, live producer pin, verifier-only
replay and archived probes are unchanged. Full J42/P41/E04 remains NOT_REACHED.
No original data/science, production/CI, N11/N12, F6/F7/F8, actor, Sorok,
J52/W52 or protected-capture authority.
