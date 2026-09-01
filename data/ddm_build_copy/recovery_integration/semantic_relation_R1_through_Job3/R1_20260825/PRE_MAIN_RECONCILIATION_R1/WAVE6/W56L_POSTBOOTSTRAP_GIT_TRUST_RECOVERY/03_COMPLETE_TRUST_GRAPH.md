# W56L COMPLETE TRUST GRAPH

Exact launch canonical: `b53f8843092e776fb83ec584399641f5f2fc3de3`.

W56K established that canonical object addresses were correct but the process used to read them was not inside a declared trust boundary. Final W56L review then exposed one additional distinction: an explicit worktree root is not by itself an object-database identity if Git is still allowed to discover `.git` indirection. The final graph below includes that correction.

| Node | Dependency | Classification | Required disposition |
|---|---|---|---|
| A | Python interpreter executable | TRUSTED_EXTERNAL_PREREQUISITE | Explicit host prerequisite. Candidate cannot select or replace it. |
| B | Python import resolution | UNTRUSTED_AND_REJECTED unless isolated | `python3 -I -S`; all five isolation flags required before shadowable imports; repository import paths rejected. |
| C | predecessor validator blob | CANONICAL_REPOSITORY_AUTHORITY | Executing bytes must equal exact live-canonical blob. |
| D | Git executable identity/resolution | TRUSTED_EXTERNAL_PREREQUISITE | Supplied as an absolute host path; no PATH resolution; no repository-contained target; no symlink path; identity fingerprint recorded before and after execution. |
| E | environment inherited by Git subprocesses | UNTRUSTED_AND_REJECTED | Parent environment is not forwarded. A minimal explicit child environment is constructed. |
| F | Git configuration sources | UNTRUSTED_AND_REJECTED where semantically optional | System/global/injected configuration authority is suppressed. Repository-local format metadata may describe the pinned repository but cannot choose another repository/worktree or invoke helpers in the used plumbing path. |
| G | Git executable-helper resolution | IRRELEVANT_TO_TRUST_BEARING_OPERATION for the admitted command set | Only Git builtins/plumbing are used. No PATH is provided; lazy fetch is disabled; no external helper is permitted or required by the trust-bearing command set. |
| H | repository/worktree locator | TRUSTED_EXTERNAL_PREREQUISITE | Absolute repository root supplied explicitly by the host and validated independently of Git before first Git call; script must lie beneath it. |
| H2 | repository metadata/object-store root | TRUSTED_EXTERNAL_PREREQUISITE deterministically derived from H | Must be concrete canonical `<repository-root>/.git` with concrete `<repository-root>/.git/objects`; gitfile, symlink, linked-worktree/common-dir, and discovery-selected metadata roots are rejected before Git execution. Every command uses explicit `--git-dir` and `--work-tree`; Git-reported Git/common dirs must equal the pinned root. |
| I | Git refs | CANONICAL_REPOSITORY_AUTHORITY | Exact full refnames only, resolved inside the pinned repository under sanitized environment; malformed/non-OID output fails closed. |
| J | Git object database reads | CANONICAL_REPOSITORY_AUTHORITY mediated by trusted host Git and pinned H2 | Exact commit/tree/blob reads only. Environment object redirection removed; top-level object-dir symlink, alternates, common-dir indirection, and shallow ancestry are rejected. |
| K | replacement refs / graft-like ancestry | UNTRUSTED_AND_REJECTED | replacement objects disabled by both global option and environment; raw commit-parent traversal used instead of merge-base/rev-list semantics; nonempty graft file rejected; shallow repository rejected. |
| L | external diff/textconv/filter/helper execution | IRRELEVANT_TO_TRUST_BEARING_OPERATION | Worktree diff is not trusted. `diff-tree -z --name-only --no-renames --no-ext-diff --no-textconv` is used only for tree path enumeration; object/blob reads use `cat-file`. No filters/hooks/pager/editor are used. |
| M | authorization/audit immutable refs | CANONICAL_REPOSITORY_AUTHORITY + external authorization predicate | Parsed only as immutable `commit:path`; bytes read from exact object IDs; authorization must be direct child of live canonical and outside candidate lineage. |
| N | canonical manifest/schema reads | CANONICAL_REPOSITORY_AUTHORITY | Read only by exact `cat-file blob <live>:<path>` from live canonical. No candidate fallback. |
| O | candidate worktree/files/tree | CANDIDATE_INPUT_ONLY | Candidate commit/tree may be inspected but cannot provide trusted executable code, schemas, manifests, helpers, repository selectors, or authority. |
| P | operating system/process/filesystem semantics | TRUSTED_EXTERNAL_PREREQUISITE | Includes stable absolute-path execution and stable filesystem identity for the duration of the gate. Host compromise is outside repository-governance threat model. |

No dependency required by the repaired repository-controlled trust path remains classified `UNRESOLVED`. Independent hostile review is still unresolved as an **adoption prerequisite**, not as an unclassified local dependency.

## Minimal trusted-host prerequisite set

`TRUSTED_HOST_EXECUTION_PREREQUISITES = { trusted Python interpreter, trusted absolute non-symlink Git executable, stable operating-system process/filesystem semantics, externally supplied absolute repository root }`

The admissible metadata/object root is not a fifth freely selected prerequisite: it is deterministically fixed as the concrete `<repository-root>/.git` under the root contract. The repository must prove candidate-controlled state cannot choose or substitute any member of the prerequisite set or redirect the derived metadata root.

## Required command reduction

The repaired gate requires only these Git builtins/plumbing families:

- `rev-parse --verify` for exact refs and repository-state probes;
- `cat-file` for exact commit/blob existence and reads;
- `diff-tree -z` for commit-tree changed-path enumeration;
- `for-each-ref` only to detect replacement refs.

All commands are executed through the exact declared Git executable with explicit `--git-dir=<repository-root>/.git --work-tree=<repository-root>`.

Ancestry and direct-parent facts are computed by Python from raw commit-object `parent` headers, not Git replacement/graft-sensitive graph traversal.

## Trust invariant

`TRUST_BEARING_GIT_FACTS_DEPEND_ONLY_ON_EXPLICIT_TRUSTED_HOST_PREREQUISITES_AND_IMMUTABLE_REPOSITORY_OBJECTS`

Operationally, canonical mutable refs are admitted only as the named canonical/authorized branch authority that resolves to an exact commit OID; after resolution, schema/manifest/evidence/ancestry facts are exact object reads under the pinned repository identity. Candidate-controlled files, PATH/config selectors, replacement mechanisms, and discovery-selected repository metadata are not trust authorities.
