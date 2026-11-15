# GOVERNANCE ENFORCEMENT CHANGE PROTOCOL R1

Governance enforcement is constitutionally self-protected.

Protected paths are enumerated in `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`.

A candidate that changes any protected path is **not allowed to self-adopt**. The candidate validator must report `GOVERNANCE_SELF_INTEGRITY = false` while its protected blobs differ from live canonical PRE-MAIN, and `ADOPTION_ELIGIBLE = false` regardless of the packet's self-claims.

Audit separation is governed by `HOSTILE_AUDIT_INDEPENDENCE_PROTOCOL.md`.

## Canonical-predecessor dependency-closure law

`CANONICAL_TOP_LEVEL_SCRIPT != CANONICAL_EXECUTION` if that script imports, executes, parses, or trusts candidate-controlled dependencies.

The predecessor gate must therefore be authoritative over its **entire executable/trusted dependency closure**, not merely its top-level Python blob.

`tools/validate_enforcement_candidate_from_canonical.py` is intentionally a standalone Python-stdlib program. It MUST NOT import `governance_r2_support.py`, `validate_governance_packet.py`, or any other Rawlsing/candidate-side helper.

Every governance artifact the predecessor gate trusts must be read by the standalone gate directly from an immutable exact live-canonical locator:

`<LIVE_CANONICAL_SHA>:<repository_path>`

At minimum this includes:

- `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`;
- `HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json`;
- `HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`.

Schema validation used by the predecessor gate is implemented inside the canonical standalone script itself. Candidate-side schema libraries, schema files, Git helpers, ref resolvers, or parsing helpers are not trusted.

The live canonical protected-path manifest must itself declare the predecessor script and every trusted governance schema/manifest dependency. If a required trusted dependency is absent from canonical PRE-MAIN, absent from the canonical manifest, or cannot be parsed from the canonical tree, the predecessor gate fails closed.

Candidate worktree code may be inspected as the candidate under review. It may never supply executable machinery or governance facts used to authorize its own integration.

## Python process-isolation law

`STDLIB_NAME != TRUSTED_STDLIB_IMPORT` when repository-controlled search paths can shadow that name before the predecessor gate establishes its trust boundary.

Therefore the predecessor gate is not valid merely because its source text contains only apparent standard-library imports.

The authoritative invocation MUST use Python isolated, safe-path, no-site execution and explicit host trust-root arguments:

`python3 -I -S tools/validate_enforcement_candidate_from_canonical.py --repository-root <ABSOLUTE_REPOSITORY_ROOT> --trusted-git-executable <ABSOLUTE_TRUSTED_GIT> <candidate_sha> <audit_evidence_ref> <audit_authorization_ref>`

The gate itself MUST fail before importing any path-resolved module unless all of the following interpreter flags are already true:

- `sys.flags.isolated`;
- `sys.flags.ignore_environment`;
- `sys.flags.no_user_site`;
- `sys.flags.no_site`;
- `sys.flags.safe_path`.

Only the built-in `sys` module may be imported before this barrier. After the barrier the gate may import only Python standard-library modules. The explicitly supplied repository root is then validated without invoking Git, and every active `sys.path` entry resolving inside that repository is rejected before the first Git subprocess.

This means repository-local files such as:

- `argparse.py`;
- `csv.py`;
- `json.py`;
- `re.py`;
- `subprocess.py`;
- `pathlib.py`;
- `typing.py`;
- `sitecustomize.py`;
- `usercustomize.py`;

cannot become predecessor executable dependencies merely by being added beside the canonical gate or elsewhere in the repository.

`PYTHONPATH`, user-site initialization, `sitecustomize`, `usercustomize`, script-directory prepending, and current-working-directory prepending are outside the trusted path under the required isolated invocation.

A direct shebang launch or ordinary `python3 script.py` invocation is intentionally non-authoritative and must fail closed before shadowable imports occur.

## Trusted Git executable / process provenance law

`CANONICAL_OBJECT_ADDRESSING != TRUSTED_CANONICAL_OBJECT_READ` unless the executable and process envelope performing the read are also inside the declared trust boundary.

No trust-sensitive subprocess may invoke bare `git`, a PATH-resolved alias, or a repository/candidate helper.

The trusted Git executable is an **external host prerequisite**. It MUST be supplied explicitly by absolute path at authoritative invocation time and the gate MUST reject:

- relative Git paths;
- nonexistent targets;
- non-regular-file targets;
- non-executable targets;
- a Git path resolving inside the repository;
- a Git path containing symlink components;
- a Git path whose executable identity changes during execution, as detected by pre/post filesystem identity and SHA-256 fingerprint.

The repository root is likewise an explicit absolute host input. The gate MUST establish it without invoking Git and reject a relative, nonexistent, symlink-containing, or noncanonical root. The executing predecessor script must lie beneath that root.

The trusted repository metadata/object root is not discovered by Git. It is deterministically pinned to the concrete directory `<repository-root>/.git` before the first Git subprocess. A `.git` gitfile, symlinked `.git`, linked-worktree/common-directory indirection, symlinked top-level object directory, missing `.git/objects`, or any Git-reported metadata/common directory differing from this pinned root MUST fail closed. Trust-sensitive Git calls are invoked with explicit `--git-dir=<repository-root>/.git` and `--work-tree=<repository-root>`; `git -C` repository discovery is not an authority mechanism.

The gate MUST NOT inherit process `PATH` into trust-sensitive Git subprocesses. It constructs a minimal child environment rather than copying the parent environment. At minimum the authoritative envelope suppresses or replaces inherited Git configuration, repository redirection, object-store redirection, namespace, executable-helper, replacement-object, lazy-fetch, pager, prompt, and equivalent environment authority. The current implementation explicitly reconstructs the child environment and does not include `PATH`.

The trusted-host process contract does not make the Git executable Rawlsing authority. It makes candidate-controlled substitution of the host prerequisite impossible within the repository threat model.

## Git configuration, helper, and object-store law

The predecessor gate uses only a minimized set of exact Git builtins/plumbing. It MUST NOT depend on Git aliases, external subcommands, hooks, filters, textconv, external diff, pager, editor, credential helper, remote helper, or candidate-selected executable helper behavior.

System and global Git configuration are disabled for the trust-sensitive subprocesses. Injected `GIT_CONFIG_COUNT` entries are not inherited. Repository-local configuration is not treated as governance authority; the exact command set is chosen so that local aliases cannot override builtins and diff/textconv/helper execution is disabled or irrelevant. Repository configuration may describe the repository's own storage format, but explicit `--git-dir` / `--work-tree` binding prevents it from selecting a different repository or worktree, and Git-reported metadata/common-directory identity is cross-checked against the host-pinned metadata root.

The allowed Git operation families are bounded to:

- `rev-parse --verify` and repository-hardening probes;
- `cat-file` exact commit/blob existence and reads;
- `diff-tree -z --name-only --no-renames --no-ext-diff --no-textconv` for changed-path enumeration;
- `for-each-ref` only as a replacement-ref rejection probe.

Canonical schema/manifest/evidence bytes are read with exact object addressing through `cat-file`, not worktree files.

Ancestry and direct-parent facts are derived by the standalone Python gate from raw exact commit-object `parent` headers. They are not delegated to replacement/graft-sensitive `merge-base`, `rev-list`, or similar graph interpretation.

The gate MUST fail closed when:

- replacement refs are present;
- a graft file is nonempty;
- an object alternates file is nonempty;
- the repository is shallow for an ancestry-sensitive decision;
- `.git` is not the concrete canonical metadata directory immediately beneath the externally supplied repository root;
- `.git/objects` is absent, redirected, or symlinked at its top-level path;
- linked-worktree/common-directory indirection is present;
- Git reports an absolute Git directory or common directory different from the pinned `<repository-root>/.git`;
- the trusted Git command exits nonzero;
- an expected object/ref cannot be read;
- SHA/ref output is malformed;
- the Git-reported worktree root does not equal the externally supplied repository root;
- repository identity cannot be established.

Both the `--no-replace-objects` global Git option and `GIT_NO_REPLACE_OBJECTS=1` are used as defense in depth. `GIT_NO_LAZY_FETCH=1` prevents missing objects from becoming an implicit remote/helper execution path.

No fallback to bare Git, discovery-selected Git metadata, candidate helper code, candidate schemas, candidate manifests, or worktree authority is permitted.

## Trusted-host prerequisite law

The enduring external host prerequisite set is:

`TRUSTED_HOST_EXECUTION_PREREQUISITES = { trusted Python interpreter, trusted absolute non-symlink Git executable, stable operating-system process/filesystem semantics, externally supplied absolute repository root }`

The repository root contract deterministically binds the metadata/object root to `<repository-root>/.git`; no additional discovery-selected repository locator is admitted.

Compromise or substitution of those exact host prerequisites is outside the candidate-controlled repository threat model.

Candidate repository authority stops at this boundary. The repository remains responsible for proving that candidate-controlled state cannot select, shadow, redirect, or substitute any member of the prerequisite set.

## Lawful ordinary change sequence after trust-root recovery

1. begin from exact live canonical PRE-MAIN;
2. make the enforcement candidate on a separate branch;
3. record the candidate as `LOCAL_COMPLETE_UNRECONCILED`;
4. competent external VOZHD/HQ creates an immutable hostile-audit authorization commit rooted directly at the live canonical PRE-MAIN, outside the candidate lineage, naming the exact candidate, audit branch, challenge nonce, audit write scope, and exact allowed PASS rulings;
5. perform the hostile audit on the separately authorized audit branch;
6. validate the exact candidate + exact authorization + exact hostile-audit result using the **standalone canonical predecessor copy** of `tools/validate_enforcement_candidate_from_canonical.py` under the authoritative Python + repository-root + trusted-Git invocation contract above;
7. that predecessor copy must obtain its Git facts and governance schemas/manifests only through the closed trusted-host Git envelope and exact live-canonical objects;
8. if that predecessor gate passes, competent external VOZHD/HQ may advance canonical PRE-MAIN to the exact audited candidate by an explicit reintegration act;
9. only after canonical movement does the new enforcement version become eligible to validate ordinary adoptive packets.

The predecessor gate self-checks that its executing bytes are exactly the bytes stored at live canonical PRE-MAIN. A modified candidate helper/schema/sibling Python module or PATH-injected Git executable cannot stand in for any transitive predecessor dependency.

The gate also requires exact authorization/result schemas, direct-canonical-root authorization ancestry, branch/write-scope separation, exact candidate binding, challenge matching, and exact authorized PASS enumeration. Substring heuristics such as `READY` or `_PASS` are forbidden.

## Historical one-time bootstrap installation — exhausted

The live PRE-MAIN preceding W56I did not contain the canonical-predecessor meta-validator or authorization schemas. Therefore the first installation could not execute the future predecessor gate without circularly pretending the new script was already canonical.

The protocol permitted exactly one bootstrap for the exact post-W56H Python-isolation repair candidate. That bootstrap boundary was physically crossed when W56I entered canonical ancestry. The exception is therefore historically exhausted and **MUST NOT be reused**.

W56J correctly observed that the pre-bootstrap canonical tree lacked the future predecessor files. That observation remains true.

W56K later proved a separate deeper defect: the installed W56I predecessor script used bare PATH-resolved `git`, so its trusted executable dependency closure was not complete. W56K therefore supersedes any reading of W56I/W56J/bootstrap history as proof of complete enforcement certification at the security-readiness grain.

Physical canonical ancestry does not retroactively convert the defective gate into certified authority:

`GIT_REF_MOVEMENT != AUTHORITY_ADOPTION`

`CANONICAL_ANCESTRY != ENFORCEMENT_CERTIFICATION`

No candidate validator, schema, scope registry, anti-resurrection map, helper library, protected-path manifest, audit-authorization schema, hostile-audit-result schema, independence protocol, sibling Python module, meta-validator, or Git process can be its own proof of adoption.

## Extraordinary post-bootstrap trust-root recovery after W56K

The W56I bootstrap exception is exhausted. This section defines a distinct one-time **POST_BOOTSTRAP_TRUST_ROOT_RECOVERY** path for repairing the already-canonical predecessor trust root. It is not a second bootstrap.

The current defective predecessor gate is the object being repaired and is not competent at the exact Git-executable-provenance grain to certify its own successor. Therefore its PASS is neither sufficient nor required for this one recovery.

The only lawful recovery sequence is:

1. start from exact physical canonical base `b53f8843092e776fb83ec584399641f5f2fc3de3`;
2. produce the bounded W56L trust-root repair candidate off canonical;
3. leave that candidate `LOCAL_COMPLETE_UNRECONCILED`;
4. a later **external** authorization commit must be rooted directly at exact `b53f8843092e776fb83ec584399641f5f2fc3de3`, outside the W56L candidate lineage, and bind the exact candidate SHA, exact hostile branch, fresh challenge nonce, exact audit write prefix, exact allowed PASS rulings, and exact terminal-token prefixes;
5. an independent hostile court must attack the exact candidate, including the entire Python/Git/OS/repository trust envelope, using an evidence path independent of the defective current predecessor gate;
6. the hostile court must independently prove immutable Git/ref/object/ancestry facts, authorization independence, candidate jurisdiction, Git executable provenance, environment/config closure, explicit metadata/object-root pinning, replacement/graft/alternate/shallow closure, no helper execution, no PATH authority, and nonpromotion;
7. only an exact authorized hostile PASS may permit competent external VOZHD/HQ to move canonical PRE-MAIN to the exact audited W56L candidate;
8. the candidate branch and hostile worker possess no integration authority;
9. immediately after any such external movement, the newly canonical predecessor gate must be exercised against a fresh harmless probe successor or dedicated post-installation verification fixture, under the exact trusted-host invocation contract;
10. the post-installation probe must demonstrate the ordinary enduring canonical-predecessor path before ordinary enforcement successor commissioning is unblocked;
11. the `POST_BOOTSTRAP_TRUST_ROOT_RECOVERY` exception is then exhausted permanently;
12. every later enforcement change returns to the ordinary canonical-predecessor + external authorization + hostile audit + external ref-movement sequence above.

This W56L candidate may document this recovery sequence but **cannot authorize it**. Merely containing this section grants no project adoption, no PRE-MAIN movement, no main movement, and no Global HQ authority.

The canonical-predecessor / isolated-Python-process / trusted-host-Git-process / host-pinned-repository-metadata-root / canonical-dependency-closure / external-authorization / hostile-auditor / external-ref-movement separation is the enduring security boundary.
