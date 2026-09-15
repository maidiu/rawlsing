# Verified ancestry and changed paths

## Ancestry

`DIRECT_CHILD` and `ANCESTOR` no longer consume an unverified `cat-file commit` payload. Every commit whose parent header is inspected first passes the W56N object-ID rebind. The parser then accepts the root-tree and parent OIDs only from that verified payload and requires the same repository hash family.

The ancestry walk verifies the descendant before trusting its parents and also verifies the target ancestor commit before accepting a reached OID as proof. Traversal is bounded and fails closed on any unreadable, malformed, mixed-algorithm, or hash-mismatched commit.

The defensive replay replaces a requested commit object's loose storage with a different valid commit object. Raw Git can read the substituted commit under the requested pathname on the fixture host; verified parent traversal rejects it before any parent header becomes evidence.

## Changed-path jurisdiction

The old trust-bearing `diff-tree` call is removed. W56N computes endpoint changed paths from verified commit/tree objects:

- verify both endpoint commits and obtain their verified root trees;
- recursively compare verified tree entries by name, mode, and OID;
- cryptographic tree-OID equality closes an unchanged subtree; changed/add/delete subtrees are enumerated from verified tree objects;
- bound both tree-object and entry counts and fail closed on malformed structures.

This produces the candidate, authorization, and audit changed-path sets used for protected-path and jurisdiction checks without delegating hidden object traversal to `diff-tree`.

A deterministic fixture produces exactly `added.txt` and `plain.txt` as the endpoint change set and confirms the computation remains independent of `diff-tree` authority.