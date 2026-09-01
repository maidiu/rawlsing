# W56L COMPLETE TRUST GRAPH

Exact launch canonical: `b53f8843092e776fb83ec584399641f5f2fc3de3`.

This graph is established before validator repair. The W56K defect is that canonical object addresses were correct but the process used to read them was not inside a declared trust boundary.

| Node | Dependency | Classification | Required disposition |
|---|---|---|---|
| A | Python interpreter executable | TRUSTED_EXTERNAL_PREREQUISITE | Explicit host prerequisite. Candidate cannot select or replace it. |
| B | Python import resolution | UNTRUSTED_AND_REJECTED unless isolated | `python3 -I -S`; all five isolation flags required before shadowable imports; repository import paths rejected. |
| C | predecessor validator blob | CANONICAL_REPOSITORY_AUTHORITY | Executing bytes must equal exact live-canonical blob. |
| D | Git executable identity/resolution | TRUSTED_EXTERNAL_PREREQUISITE | Must be supplied as an absolute host path; no PATH resolution; no repository-contained target; no symlink path; identity fingerprint recorded before and after execution. |
| E | environment inherited by Git subprocesses | UNTRUSTED_AND_REJECTED | Parent environment is not forwarded. A minimal explicit child environment is constructed. |
| F | Git configuration sources | UNTRUSTED_AND_REJECTED where semantically optional | System/global config disabled. Injected config env is absent. Repository config may describe repository format but may not drive helpers, pager, diff/textconv, aliases, replacement semantics, or worktree content into the used plumbing path. |
| G | Git executable-helper resolution | IRRELEVANT_TO_USED_GIT_PLUMBING if command minimization holds | Only Git builtins/plumbing are used. No PATH is provided; lazy fetch disabled; no external helper is permitted or required. |
| H | repository/worktree locator | TRUSTED_EXTERNAL_PREREQUISITE | Absolute repository root supplied explicitly by the host, validated independently of Git before first Git call; script must lie beneath it. |
| I | Git refs | CANONICAL_REPOSITORY_AUTHORITY | Exact full refnames only, resolved under sanitized environment; malformed SHA output fails closed. |
| J | Git object database reads | CANONICAL_REPOSITORY_AUTHORITY mediated by trusted host Git | Exact commit/tree/blob reads only. Environment object redirection removed; alternates file rejected; shallow repository rejected for ancestry-sensitive use. |
| K | replacement refs / graft-like ancestry | UNTRUSTED_AND_REJECTED | replacement objects disabled by both global option and environment; raw commit-parent traversal used instead of merge-base/rev-list semantics; nonempty graft file rejected; shallow repository rejected. |
| L | external diff/textconv/filter/helper execution | IRRELEVANT_TO_USED_GIT_PLUMBING | Worktree diff is not trusted. `diff-tree -z --name-only --no-renames --no-ext-diff --no-textconv` is used only for tree path enumeration; object/blob reads use `cat-file`. No filters/hooks/pager/editor are used. |
| M | authorization/audit immutable refs | CANONICAL_REPOSITORY_AUTHORITY + external authorization predicate | Parsed only as immutable `commit:path`; bytes read from exact object IDs; authorization must be direct child of live canonical and outside candidate lineage. |
| N | canonical manifest/schema reads | CANONICAL_REPOSITORY_AUTHORITY | Read only by exact `cat-file blob <live>:<path>` from live canonical. No candidate fallback. |
| O | candidate worktree files | CANDIDATE_INPUT_ONLY | Candidate commit/tree may be inspected but cannot provide trusted executable code, schemas, manifests, helpers, or authority. |
| P | operating system/process/filesystem semantics | TRUSTED_EXTERNAL_PREREQUISITE | Includes stable absolute-path execution and filesystem identity for the duration of the gate. Host compromise is outside repository-governance threat model. |

## Minimal trusted-host prerequisite set

`TRUSTED_HOST_EXECUTION_PREREQUISITES = { trusted Python interpreter, trusted absolute non-symlink Git executable, stable operating-system process/filesystem semantics, externally supplied absolute repository root }`

The repository must prove that candidate-controlled state cannot choose or substitute any member of that set. No other executable is admitted to the trust-bearing path.

## Required command reduction

The repaired gate should require only these Git builtins/plumbing families:

- `rev-parse --verify` for exact refs and repository-state probes;
- `cat-file` for exact commit/blob existence and reads;
- `diff-tree -z` for commit-tree changed-path enumeration;
- `for-each-ref` only to detect replacement refs if retained as a defense-in-depth probe.

Ancestry and direct-parent facts are to be computed by Python from raw commit-object `parent` headers, not Git replacement/graft-sensitive graph traversal.

## Trust invariant

`CANONICAL_OBJECT_ADDRESSING == TRUSTED_CANONICAL_OBJECT_READ` only when the canonical locator, repository identity, Git executable, Git environment, object-store path, ancestry semantics, and output validation are all simultaneously closed.
