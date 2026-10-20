# Native source, import and owner graph

## Import graph (actual runtime imports)

```
candidate/pipeline.py
    ├── candidate/identity.py          → (no native imports)
    ├── candidate/events.py            → (no native imports)
    ├── candidate/conditioning.py
    │       └── rawlsing_next.v3_psepf_zero_positive_guard   [NATIVE, blob e0528d65…]
    ├── candidate/response_rules.py    → (no native imports)
    ├── candidate/target_rules.py      → (no native imports)
    ├── candidate/transaction.py       → (no native imports)
    ├── candidate/later_action.py      → (no native imports)
    └── candidate/action_admission.py  → (no native imports)

candidate/native_custody.py
    ├── rawlsing_next.v3_psepf_zero_positive_guard   [NATIVE]
    ├── rawlsing_next.wsc_gt0_protocol               [NATIVE]
    └── rawlsing_next.wsc_gt0_v3_runtime             [NATIVE]

candidate/release_gate.py              → (no native imports)
candidate/canon.py                     → (stdlib only)
```

## Owner graph (jurisdictional dependencies)

```
[Pyat source / original35 / world / clock]  (READ-ONLY demand from Sorok)
    │  source/provenance/as_of grant; cannot grant actor meaning
    ▼
[ADP-007 V3 entity creation + actor activation]  ← CAN008_RULE_ISSUER_UNVERIFIED
    │  actor identity/subject binding
    ▼
[ADP-010 generated encounter OR ADP-019 admitted occurrence]  ← ADP019_ACTOR_EVENT_WITNESS_MISSING
    │  occurrence owner + immutable ID/hash/time + receivability
    ▼
[CAN008 R2 semantic owner = V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE]
    │  semantic adoption VERIFIED (a6bc1555… → b80dd692…)
    │  concrete RULE_A: UNISSUED ← CAN008_RULE_ISSUER_UNVERIFIED
    ▼
[CAN011 V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY@1.0.0]
    │  canon VERIFIED (1ed04e62…)
    │  concrete RULE_T: UNISSUED ← CAN011_TARGET_UNISSUED
    ▼
[CAN011 persisted V3MS_PRACTICE, immutable transition]
    │  next event E2, effective_time > previous transition
    ▼
[CAN008 R2 evaluate E2; action admissibility separately granted]
    │  ACTUAL actor action cannot be inferred from response label
    ▼
[later-action consumer READS committed target state]  ← LATER_ACTION_CONSUMER_UNBOUND
    │
    ▼
[performed-action owner admission]  ← PERFORMED_ACTION_OWNER_UNPROVED
    │
    ▼
[ADP-015 relationship / ADP-016 memory / ADP-017 belief+claim access]
    │  only IF their own independent effect rules allow
    ▼
[M6 V2 bounded render]
```

## Source custody (pinned authorities)

| Authority | Git blob | Status |
|---|---|---|
| CAN008 R2 HQ adoption record | `a6bc1555489271e1adb2271ed02d46bb7f888170` | verified |
| CAN008 R2 adopted semantic body | `b80dd6925066510ecbbfec7b427bf9f688475663` | verified |
| CAN008 v1 predecessor | `976c59086b938992114f68621f149687670e306d` | verified |
| CAN011 canon | `1ed04e62a363493bc7032a99139454a3126e6ea0` | verified |
| ADP007 | `28813c575c681abf3c6235ff23c6f01f7123acc7` | referenced |
| ADP008 | `6428e26f4e85ede66a10ea2761362ff0cd84fc5e` | referenced |
| ADP019 | `5c38772ea193e5a3f20da23c16df086a153ab2f2` | referenced |
| ADP016 | `0b7bbe29f6509e31ac7d842962a2bf3d636daa2c` | referenced |
| ADP017 | `6b4162df27003bec413074178c46fea6360d71a0` | referenced |
| v3_psepf_zero_positive_guard | `e0528d65215cb431196570c38bac4eae94217a1b` | imported at runtime |
| B1 bfirst.py | `94ffc52847e4c8ae760212d1bc8543594ba793fa` | technical reference |
| B3AS return | `1a25b19dd01e8e7954e38c59ffc7e52c50739c9f` | technical reference |
| S1 return | `0d47fe863671d1e1d57f26102462be6595c5d7ea` | scientific reference |
| LIFE1 return | `7ffc20ddb30f71034abf8d02c224d13d6952e11f` | native defer authority |
| Proof-integrity law | `a83d054a656ff9d7bf32b18495bd0a1843c02da9` | binding |
