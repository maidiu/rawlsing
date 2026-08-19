# 21 — AUTHORITY BUNDLE MANIFEST & PRECEDENCE PROTOCOL

## 1. Purpose

A worker must never implement against a floating pile of filenames, remembered rulings, or a branch that may have moved.

G1 owns one immutable, content-hashed authority manifest for every command dependency epoch.

## 2. Authority manifest record

For every binding authority, record:

- authority ID;
- semantic title;
- repository path or governed external immutable locator;
- accepted commit SHA;
- blob/content hash;
- authority class;
- jurisdiction;
- precedence rank within jurisdiction;
- supersedes / superseded-by relations;
- negative-authority consequences;
- downstream contracts affected;
- status: ACTIVE / SUPERSEDED / MIGRATION_ONLY / EVIDENCE_ONLY / BLOCKED_EXTERNAL;
- exact parent adjudication that made the status binding.

A path without commit/content identity is not a frozen authority reference.

## 3. Bundle identity

The governing authority bundle hash is computed from deterministic serialization of the ordered authority-manifest entries, not from directory names or timestamps.

Any change to an ACTIVE entry changes the bundle hash and triggers G6 dependency analysis.

## 4. Precedence law

Authority conflicts are resolved by explicit jurisdiction and accepted parent precedence, never by:

- latest file modification time;
- higher version-looking filename;
- stage number;
- more detailed prose;
- implementation behavior;
- majority of documents;
- worker preference.

If precedence cannot be proven from accepted authority, the seam is `AUTHORITY_CONFLICT` and stops.

## 5. Evidence versus law

The manifest must distinguish:

- dispositive governing law;
- accepted non-dispositive evidence;
- historical implementation evidence;
- migration compatibility authority;
- test oracle;
- superseded material.

Rabochii may read all relevant evidence but may not promote evidence to governing law because it makes implementation easier.

## 6. Authority compilation

G1 + the appropriate semantic owner compile prose authorities into machine contracts only by preserving the original jurisdiction and ceiling.

A compiled contract must record:

- source authority IDs/hashes;
- compilation rule/version/hash;
- semantic checksum;
- explicit nonclaims / forbidden interpretations;
- hostile fixture vectors derived from negative authority.

Compiled contracts may clarify execution but may not silently add meaning absent from source authority.

## 7. Worker launch rule

Every worker receives:

- authority bundle ID/hash;
- exact subset manifest of authorities material to its task;
- precedence statement;
- explicit superseded/legacy exclusions.

The worker confirms the manifest hash before writing.

## 8. Authority drift detection

Inspectorate/G6 compare every returned `SEMANTIC_DIFF` and `CONTRACT_CONFORMANCE` against the issued authority subset.

Any behavior whose semantic justification cannot be traced to an issued authority or lawful local engineering freedom is:

`UNAUTHORIZED_SEMANTIC_DRIFT`.

It cannot be integrated.

## 9. External authority

If a necessary authority cannot be stored in GitHub, the manifest must bind an immutable external identity and record access/replay constraints.

Mutable URLs, current/latest aliases, or human-memory references are not acceptable.

## 10. Activation requirement

No campaign Activation Receipt is valid until G1 publishes the complete ACTIVE authority manifest and its content hash for the final whole-machine architecture.
