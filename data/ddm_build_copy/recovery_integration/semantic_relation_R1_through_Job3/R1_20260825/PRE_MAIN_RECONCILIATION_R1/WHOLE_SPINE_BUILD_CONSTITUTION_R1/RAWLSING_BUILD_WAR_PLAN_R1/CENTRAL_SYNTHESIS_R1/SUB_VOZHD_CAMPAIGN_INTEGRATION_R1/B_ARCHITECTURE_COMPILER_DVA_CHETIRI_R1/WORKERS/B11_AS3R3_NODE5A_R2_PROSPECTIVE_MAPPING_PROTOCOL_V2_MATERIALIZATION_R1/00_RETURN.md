# B11 — AS3R3 Node5A-R2 prospective mapping replay protocol-v2 materialization R1

Terminal:

`AS3R3_NODE5A_R2_PROSPECTIVE_MAPPING_REPLAY_PROTOCOL_V2_MATERIALIZATION_COMPLETE__READY_FOR_NODE7_V2_RECOMMISSION`

## Holding

B11 materially closes the bounded protocol-v2 materialization grain.

The immutable HQ protocol spec and frozen mapping carrier verified exactly:

- HQ protocol spec blob: `befee68ee14f6e80e88cb3142947a37a7619fc5b`;
- frozen 19-row carrier blob: `26a7c35df2e6454c5e270a03b3571599bdf152fd`.

The exact prospective serializer was committed **before** qualifying replay proof:

- serializer commit: `84a80b6d0aec9525cae704093ae770415371a4aa`;
- serializer Git blob: `29b61fc7fef8db06e4ba95fedc788a20b8d28d5e`;
- serializer file SHA-256: `47307828a471cc525643f870c32ac15efa26565f063191d50ea32c48c72994b6`.

The serializer contains no historical mapping-payload digest, no constructor/remint path, and no alternate serialization selection logic.

## Prospective payload identity

Lawful materialization under:

`AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0`

produced the newly discovered payload identity:

- byte length: **12,364**;
- Git blob: `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- SHA-256: `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- payload commit: `6c03af3c4aed1ad6f305976d8cf60809167f8976`;
- UTF-8, no BOM;
- compact recursively sorted JSON;
- exact frozen row order;
- exactly one terminal LF.

This is a **prospective evidence identity**, not recovery or reproduction of the historical Node5A-R2 payload.

## Fresh-process proof

After the serializer commit and payload commit, two genuinely independent OS processes were launched with the byte-identical committed serializer implementation.

Both runs:

- exited 0;
- emitted no stderr;
- loaded the exact protocol-spec and carrier blobs;
- materialized 12,364 bytes;
- produced SHA-256 `06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db`;
- produced Git blob `d62847e9972362bf2fcaeac515360cd5cf99eab7`;
- were byte-identical to each other;
- were byte-identical to committed `02_MAPPING_PAYLOAD_V2.json`.

No output from run 1 was an input to run 2.

## Mapping invariants

The prospective payload preserves exactly:

- 19 mapping rows;
- exact 19-row frozen order;
- exactly nine row fields;
- all source IDs/object IDs/content hashes;
- all Node4A input hashes;
- all successor kinds/object IDs/content hashes;
- `role_key_lookup_preserved = true` for all 19;
- 18 distinct successor predicate content hashes;
- sole duplicate successor target exactly `{A000,A1RAPP}`;
- exact alias string `{A000,A1RAPP}` on A000 and A1RAPP only.

No semantic/canonical identity drift occurred.

## Historical/prospective separation

Historical mapping digest remains immutable nonreplayable provenance only.

B11 did not use it as:
- serializer input;
- materialization input;
- serializer-selection target;
- prospective success target;
- equality requirement.

Serialization variants searched: **0**.
Target fitting: **false**.

Historical Node6 was not rewritten.

## Boundary audit

B11 did not:
- execute `construct_successor_predicate`;
- execute `construct_successor_query`;
- enter Node7;
- remint any runtime object;
- modify Node5A-R2, Node4A, Node4B, Node5B, or Node6;
- create DiscoveryAuthority/frontier/replay identities;
- execute AS4I0, hostile validation, LiTS-I/I05/C05R2B, C08/G1, OBL037, or V3;
- modify central/PRE-MAIN/main or sibling campaigns.

Node7 is now ready **only for SUB-VOZHD B adjudication and v2 recommission**. B11 itself does not execute Node7.

Return to:

`SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI`.
