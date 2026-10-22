# Frozen case replay and exact results

The actual replay is `evidence/replay.json`: **36/36 pass**, all expected decisions, ceilings, reason lists and requested diffs checked.

| Case | Actual decision | Ceiling | Core check |
|---|---|---|---|
| C00 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | full 18, 13/1/2/1/1 |
| C01 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | ARC1 subset remains local |
| C02 | HOLD_GENERIC_R09 | LOCAL_ONLY_POLICY_CONSISTENT | generic needs R09 |
| C03 | REFUSE_FRONTIER | NONE | 18 missing / 2 extra |
| C04 | REFUSE_FRONTIER | NONE | clone witnesses not heterogeneity |
| C05 | REFUSE_PIN | NONE | candidate self-pin |
| C06 | REFUSE_FORGED_EVIDENCE | NONE | candidate native=true |
| C07 | REFUSE_FORGED_EVIDENCE | NONE | trace only |
| C08 | REFUSE_FRONTIER | NONE | count-preserving swap |
| C09 | REFUSE_FRONTIER | NONE | duplicate occurrence |
| C10 | REFUSE_STATUS | NONE | admin/unadministered promotion |
| C11 | REFUSE_STATUS | NONE | PENDING as completed |
| C12 | REFUSE_STATUS | NONE | UNKNOWN to NA/positive |
| C13 | REFUSE_IDENTITY | NONE | old edition K |
| C14 | REFUSE_IDENTITY | NONE | typed condition value |
| C15 | REFUSE_AUTHORITY | NONE | revoked permission replay |
| C16 | HOLD_ORIGINAL_G8 | NONE | synthetic 35 aliases |
| C17 | HOLD_ORIGINAL_G8 | NONE | exact names, U/Epre null |
| C18 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | restore after hostile |
| C19 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | observed zero with denominator |
| C20 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | valid null |
| C21 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | valid empty |
| C22 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | retry counted once |
| C23 | REFUSE_DUPLICATE_COUNT | NONE | duplicated scientific count |
| C24 | HOLD_UNIMPLEMENTED_RELATION | NONE | unlinked person/household |
| C25 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | separate units, held joints |
| C26 | HOLD_GENERIC_R09 | LOCAL_ONLY_POLICY_CONSISTENT | mock transport (mock parsing only) |
| C27 | REFUSE_FORGED_EVIDENCE | NONE | stale/wrong attestation |
| C28 | REFUSE_AUTHORITY | NONE | original host/purpose mismatch |
| C29 | REFUSE_FRONTIER | NONE | held IDs cannot be dropped |
| C30 | HOLD_TRUSTED_NATIVE | LOCAL_ONLY_POLICY_CONSISTENT | honest native assertion, no R09 |
| C31 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | administered all-missing |
| C32 | ALLOW_LOCAL_POLICY_CONSISTENT | LOCAL_ONLY_POLICY_CONSISTENT | full bijective rename local |
| C33 | REFUSE_FRONTIER | NONE | 2 renamed, 16 missing |
| C34 | HOLD_GENERIC_R09 | LOCAL_ONLY_POLICY_CONSISTENT | full renamed, generic no R09 |
| C35 | REFUSE_FRONTIER | NONE | noninjective candidate rename |

Additional independent tests:

- subset of 3 non-case-named operations → local allow;
- reordered full multiset → local allow;
- one semantic field mutation → frontier refuse, restore → allow;
- substitute policy dependency → frontier refuse, cold reload → local allow;
- gate source contains no C00–C35 case switch and no q301 literal blacklist;
- untrusted non-handle object → `REFUSE_PIN`.
