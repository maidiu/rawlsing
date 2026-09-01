# W56L COMPLETE TRUST GRAPH

Exact launch canonical: `b53f8843092e776fb83ec584399641f5f2fc3de3`.

W56K established that canonical object addresses were correct but the process used to read them was not inside a declared trust boundary. W56L terminal review then exposed three nested distinctions that had to be closed rather than rhetorically collapsed: an explicit worktree root is not an object-database identity if `.git` discovery can redirect; an explicit `--git-dir` is not a ref-store boundary if `refs`/`packed-refs` can redirect; and an OID pathname is not authenticated immutable content if the object payload is not verified against that OID.

| Node | Dependency | Classification | Required disposition |
|---|---|---|---|
| A | Python interpreter executable | TRUSTED_EXTERNAL_PREREQUISITE | Explicit host prerequisite. Candidate cannot select or replace it. |
| B | Python import resolution | UNTRUSTED_AND_REJECTED unless isolated | `python3 -I -S`; all five isolation flags required before shadowable imports; repository import paths rejected. |
| C | predecessor validator blob | CANONICAL_REPOSITORY_AUTHORITY | Executing bytes must equal authenticated exact live-canonical blob. |
| D | Git executable identity/resolution | TRUSTED_EXTERNAL_PREREQUISITE | Supplied as an absolute host path; no PATH resolution; no repository-contained target; no symlink path; identity fingerprint recorded before and after execution. |
| E | environment inherited by Git subprocesses | UNTRUSTED_AND_REJECTED | Parent environment is not forwarded. A minimal explicit child environment is constructed. |
| F | Git configuration sources | UNTRUSTED_AND_REJECTED where semantically optional | System/global/injected configuration authority is suppressed. Repository-local format metadata may describe the pinned repository but cannot choose another repository/worktree or invoke helpers in the used plumbing path. |
| G | Git executable-helper resolution | IRRELEVANT_TO_TRUST_BEARING_OPERATION for the admitted command set | Only Git builtins/plumbing are used. No PATH is provided; lazy fetch is disabled; no external helper is permitted or required by the trust-bearing command set. |
| H | repository/worktree locator | TRUSTED_EXTERNAL_PREREQUISITE | Absolute repository root supplied explicitly by the host and validated independently of Git before first Git call; script must lie beneath it. |
| H2 | repository metadata/object-store root | TRUSTED_EXTERNAL_PREREQUISITE deterministically derived from H | Must be concrete canonical `<repository-root>/.git` with concrete `<repository-root>/.git/objects`; gitfile, symlink, linked-worktree/common-dir, and discovery-selected metadata roots are rejected before Git execution. Every command uses explicit `--git-dir` and `--work-tree`; Git-reported Git/common dirs must equal the pinned root. |
| I | Git ref storage / exact authoritative refs | CANONICAL_REPOSITORY_AUTHORITY inside pinned H2 | Top-level `.git/refs` and `.git/packed-refs` may not symlink/escape; each exact loose-ref path is symlink-checked; ref syntax is bounded before revision interpolation; malformed/non-OID output fails closed. Mutable refs only select exact commit OIDs. |
| J | Git object database storage | UNTRUSTED_AS_CONTENT_UNTIL_AUTHENTICATED | Object alternates are rejected; shallow ancestry is rejected; the pinned database must pass full `git fsck` before trust-bearing reads. |
| J2 | exact commit/blob payloads | IMMUTABLE_REPOSITORY_AUTHORITY only after OID authentication | Returned commit/blob bytes are independently re-hashed in Python with Git object framing and must reproduce the requested 40- or 64-hex OID. |
| K | replacement refs / graft-like ancestry | UNTRUSTED_AND_REJECTED | replacement objects disabled by both global option and environment; raw authenticated commit-parent traversal used instead of merge-base/rev-list semantics; nonempty graft file rejected; shallow repository rejected. |
| L | external diff/textconv/filter/helper execution | IRRELEVANT_TO_TRUST_BEARING_OPERATION | Worktree diff is not trusted. `diff-tree -z --name-only --no-renames --no-ext-diff --no-textconv` runs only after full object integrity; object/blob reads use exact OIDs. No filters/hooks/pager/editor are used. |
| M | authorization/audit immutable refs | CANONICAL_REPOSITORY_AUTHORITY + external authorization predicate | Parsed only as immutable `commit:path`; commit and blob bytes are OID-authenticated; authorization must be direct child of live canonical and outside candidate lineage. |
| N | canonical manifest/schema reads | CANONICAL_REPOSITORY_AUTHORITY | Exact authenticated live-canonical commit/path resolves to exact blob OID; returned blob bytes are re-hashed; no candidate fallback. |
| O | candidate worktree/files/tree | CANDIDATE_INPUT_ONLY | Candidate commit/tree may be inspected but cannot provide trusted executable code, schemas, manifests, helpers, repository selectors, ref storage, or authority. |
| P | operating system/process/filesystem semantics | TRUSTED_EXTERNAL_PREREQUISITE | Includes stable absolute-path execution and stable filesystem identity for the duration of the gate. Host compromise is outside repository-governance threat model. |

No dependency required by the repaired repository-controlled trust path remains classified `UNRESOLVED`. Independent hostile review is still unresolved as an **adoption prerequisite**, not as an unclassified local dependency.

## Minimal trusted-host prerequisite set

`TRUSTED_HOST_EXECUTION_PREREQUISITES = { trusted Python interpreter, trusted absolute non-symlink Git executable, stable operating-system process/filesystem semantics, externally supplied absolute repository root }`

The admissible metadata/object/ref root is not a fifth freely selected prerequisite: it is deterministically fixed as the concrete `<repository-root>/.git` under the root contract. The repository must prove candidate-controlled state cannot choose or substitute any member of the prerequisite set or redirect the derived metadata/ref root. Object content is not trusted merely because it resides under that root; it becomes immutable authority only after OID authentication.

## Required command reduction

The repaired gate requires only these Git builtins/plumbing families:

- `rev-parse --verify` for exact refs and exact commit-path to blob-OID resolution, plus repository-state probes;
- `cat-file commit` / `cat-file blob` for exact object reads whose returned bytes are re-hashed in Python;
- `fsck --full --no-reflogs --no-progress` as the mandatory full object-database integrity gate;
- `diff-tree -z` for commit-tree changed-path enumeration only after integrity is established;
- `for-each-ref` only to detect replacement refs.

All commands are executed through the exact declared Git executable with explicit `--git-dir=<repository-root>/.git --work-tree=<repository-root>`.

Ancestry and direct-parent facts are computed by Python from authenticated raw commit-object `parent` headers, not Git replacement/graft-sensitive graph traversal.

## Trust invariant

`TRUST_BEARING_GIT_FACTS_DEPEND_ONLY_ON_EXPLICIT_TRUSTED_HOST_PREREQUISITES_AND_IMMUTABLE_REPOSITORY_OBJECTS`

Operationally, canonical mutable refs are admitted only as named canonical/authorized authority locators inside the pinned in-root ref store. They may select an exact commit OID but do not supply trusted content. After resolution, schema/manifest/evidence/ancestry facts are accepted only through cryptographically authenticated immutable objects. Candidate-controlled files, PATH/config selectors, replacement mechanisms, external ref stores, discovery-selected repository metadata, and unauthenticated object payloads are not trust authorities.