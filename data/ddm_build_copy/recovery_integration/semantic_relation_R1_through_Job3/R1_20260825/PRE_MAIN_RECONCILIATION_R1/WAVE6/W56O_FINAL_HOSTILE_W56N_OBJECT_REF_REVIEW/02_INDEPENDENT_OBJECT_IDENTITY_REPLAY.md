# Independent object-identity replay

W56O did not accept W56N's reported DV07-DV10/DV20-DV24 values as proof. It independently inspected the executable and reproduced benign Git-object identity calculations against exact candidate repository data.

## Executable construction

`GitTrust.read_object(requested_oid, expected_type)` does not expose `cat-file` output directly. It:

1. requires one exact 40- or 64-lowercase-hex OID;
2. uses the already-bounded trusted Git process to require the exact expected type;
3. obtains the payload for the requested OID;
4. independently computes `H(expected_type + SP + decimal_length + NUL + payload)` using SHA-1 for 40-hex or SHA-256 for 64-hex;
5. requires exact equality to the requested OID before returning bytes.

`commit_info` parses root-tree and parent OIDs only from `g.commit(o)`, which is the verified commit reader. `at_path` obtains the root tree only from a verified commit, each child OID only from a verified tree, and the final governance bytes only from a verified regular blob. `changed` obtains endpoint root trees from verified commits and recursively compares verified trees; no trust-bearing `diff-tree` result remains.

## Independent actual-object checks

Three distinct Git object layers were independently rebound from candidate data:

### Blob

Exact bytes returned for W56N `06_REF_PROVENANCE_CONTRACT.md` were recomputed with the canonical Git blob formula.

Computed SHA-1:

`e6c277b0e4154dc5b442affb480b282ad21c6525`

Repository blob OID:

`e6c277b0e4154dc5b442affb480b282ad21c6525`

Result: **MATCH**.

### Root tree

The terminal commit reports root tree `ef88d20ab4d4a44d8425a9d6b1dde3a2656b1359`. Independent tree reconstruction used the exact top-level entries and binary child OIDs:

- `100644 README.md -> 428bbcf6a5cbf5b6edf75078c63fe76ae116d058`
- `40000 data -> 9eee2fafb139b84e7e43a7c83b7ab0ca0f6f55c3`
- `40000 rawlsing_next -> f5673a55187f5a752cda0c23b2410d2405a0f045`
- `40000 section85 -> 7069b9051154a67d214291b61c08fc3117fe930b`

Computed Git tree SHA-1:

`ef88d20ab4d4a44d8425a9d6b1dde3a2656b1359`

Result: **MATCH**.

### Terminal commit

Independent commit reconstruction used the exact tree OID, direct parent `a81c6f09e32a9747813c1f57d01b1490e0d8a3c1`, author/committer identity and timestamp metadata, and exact message `W56N: append W56M and W56N ledger dispositions`.

Computed Git commit SHA-1:

`5bfcb9ddfc30a9f0958e675a5af6c611978284bf`

Requested/terminal OID:

`5bfcb9ddfc30a9f0958e675a5af6c611978284bf`

Result: **MATCH**.

These independent calculations establish that W56N's hash construction is the actual Git object identity construction across blob/tree/commit layers and that exact candidate objects reproduce under it.

## W56M substitution grain

The W56M attack depended on Git returning payload Y while the gate trusted requested OID X merely because `cat-file` succeeded. W56N's authority transition is now mathematically conditional on `GitObjectHash(expected_type, Y) == X`. If Y is a different valid Git object, its object hash is Y's OID, not X; the returned bytes are rejected before parent headers, tree entries, governance file bytes, or changed-path jurisdiction become authority.

Therefore:

`TRUST_BEARING_GIT_OBJECT_BYTES_ARE_CRYPTOGRAPHICALLY_BOUND_TO_THEIR_REQUESTED_OBJECT_IDS = CLOSED`