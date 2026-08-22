# SOURCE CERT PREP71 — R04 EVS — FUTURE EXECUTION ORDER

Status: **NON-DISPOSITIVE PACKET PREPARATION ONLY. DO NOT CERTIFY FROM THIS FILE.**

The later governed source-certification court must execute each source independently in this order:

1. **SHA gate.** Re-materialize `surveys.zip`, verify ZIP SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`, extract only the assigned EVS member, and verify its exact source SHA before any read.
2. **Decoder/config gate.** Read the source-native SPSS subtype-20 encoding declaration and machine character code. For EVS 1999/2008, the default UTF-8 reader path must reproduce the governed failure; only then use the exact `latin1` compatibility execution path for physical extraction. `latin1` is never source-text authority.
3. **Hostile physical fixtures.** Execute every source-specific row/missingness/raw-byte fixture in `HOSTILE_FIXTURES.csv`; any mismatch is fail-closed.
4. **Metadata/topology fixtures.** Preserve variable order, coordinate variables, weight/design candidates, ranked slots, routing coordinates, and all native MR sets exactly. For EVS 2008, all 13 MR set identities must survive even where memberships duplicate or overlap. For EVS 2017, preserve Q4 and Q11 as native MR sets.
5. **Documentary semantic assertions.** Apply only claims explicitly supported by source-native or exact-release documentary authority. Compatibility-decoded 1999/2008 human-language strings are not semantic authority.
6. **Exact carrier/C11 equivalence assertions.** Only after physical and documentary gates pass, test the future carrier against the source-certification/C11 information-equivalence contract. This packet does not define or change that contract.
7. **Negative/fail-closed fixtures.** Prove no silent decoder fallback, no latin1-as-source-encoding promotion, no missing-state collapse, no native-ID promotion, no default weight, no MR deduplication, no adjacency repair, and no routing inference from missingness.
8. **Future disposition gate.** A separately authorized G-SR09 court may then issue its governed source disposition. This packet itself MUST NOT emit `CERTIFIED`, `FAILED`, promotion, or G-SR09 closure.

## EVS 1999 documentary gate

The exact source **declares UTF-8** in SPSS subtype 20 and machine `character_code=65001`, but the frozen byte stream contains metadata byte sequences invalid under UTF-8. The exact later blocker is therefore not “unknown intended encoding.” It is: **no producer-authoritative, exact-release, field-level correction/alignment rule has been located that authorizes repair/rendering of every malformed human-language string in this exact SHA.** Official GESIS ZA3811 v3.0.0 documentation can support semantic alignment, but it does not authorize an unbounded byte-repair heuristic. Label-dependent certification remains blocked until this is closed or the governed certification contract explicitly retains the affected strings as raw/non-semantic UNKNOWN.

## EVS 2008 documentary + MR gate

The exact source likewise **declares UTF-8** with `character_code=65001` yet contains invalid UTF-8 metadata bytes. The same field-level repair/alignment blocker therefore applies. Independently, the future court must preserve all 13 native MR sets by set name/type/counted value/member list. Duplicate-member aliases and overlapping sets are source information, not duplicates to clean up. MR physical topology may be tested even while MR label text remains authority-blocked.

## EVS 1981 / 1990 / 2017

These are not “simple” sources. Their packets retain source-specific missing declarations, coordinate/weight drift, ranked/routing structures, and native MR state where present. Unknown identifier, weight-estimand, routing, or sentinel semantics must remain typed unknown unless exact documentary authority is invoked by the future court.
