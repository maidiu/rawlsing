# W56L ref-store and object-ID authentication correction

This receipt supersedes the earlier W56L local seals at two final trust grains discovered during terminal VOZHD review. It does not alter W56I/W56J/W56K history and does not authorize PRE-MAIN movement.

## Residual seams found

### 1. Loose / packed ref-store redirection

Pinning `<repository-root>/.git` and using explicit `--git-dir` was necessary but not sufficient. Git will follow a symlinked `.git/refs` directory, and it will also read a symlinked `.git/packed-refs` file. A local deterministic fixture demonstrated that an exact `rev-parse --verify refs/heads/<name>^{commit}` can therefore return a commit selected by an external ref store even though `--git-dir` and `--work-tree` are explicit.

The repaired gate now rejects symlinked/noncanonical top-level `refs` and `packed-refs` storage before trust-bearing ref resolution and, for each exact authoritative ref it resolves, rejects symlink components in that loose-ref path. Ref names are syntax-bounded before interpolation into Git revision syntax.

### 2. OID pathname does not authenticate object bytes

A second deterministic fixture wrote one loose blob, retained its original object pathname/OID, then replaced the compressed payload with different valid blob bytes. `git cat-file blob <original_oid>` returned the substituted payload with exit status zero. Recomputing the Git object ID over the returned bytes produced a different SHA.

Therefore `cat-file <type> <oid>` is an object-addressed read, but not by itself proof that the returned bytes still hash to that OID.

The final gate closes this grain in two layers:

1. before any canonical ref, ancestry, schema, manifest, authorization, audit, or changed-path fact is consumed, trusted Git must pass `fsck --full --no-reflogs --no-progress` over the pinned repository object database;
2. every raw commit and every blob returned for a trust-bearing exact object read is re-hashed independently in Python using the Git object framing `<type> <length>\0<payload>` and must equal the requested 40- or 64-hex OID.

Because the host filesystem is explicitly required to remain stable for the duration of the gate, the full pre-read integrity pass plus per-read authentication closes mutable object-store substitution without enlarging repository authority.

## Regression verification

Local benign deterministic checks against the exact repaired source:

- `python3 -m py_compile`: PASS;
- ordinary non-isolated invocation: exit `97` before shadowable imports: PASS;
- isolated `-I -S` invocation on an ordinary repository: repository hardening reached `full_object_database_fsck = PASS`: PASS;
- symlinked `.git/refs` fixture: rejected before canonical resolution with `repository-refs-dir-symlink-component`: PASS;
- symlinked external ref store under explicit `--git-dir` was independently shown to resolve successfully in unpatched Git, proving the attack premise: PASS;
- loose-object payload substitution under an unchanged OID was independently shown to be returned by `git cat-file`, proving the attack premise: PASS;
- the repaired gate rejected that tampered object database with `repository-object-or-ancestry-hardening-failed` and `full_object_database_fsck = FAIL`: PASS;
- the committed validator blob SHA equals the locally syntax-checked/tested source blob SHA: PASS.

## Final local trust proposition

`TRUST_BEARING_GIT_FACTS_DEPEND_ONLY_ON_EXPLICIT_TRUSTED_HOST_PREREQUISITES_AND_IMMUTABLE_REPOSITORY_OBJECTS = LOCALLY_ESTABLISHED`

The explicit trusted-host prerequisite set remains:

`{ trusted Python interpreter, trusted absolute non-symlink Git executable, stable operating-system process/filesystem semantics, externally supplied absolute repository root }`

Canonical and authorized mutable refs are only authority locators into the pinned in-root ref store. Once resolved, trust-bearing content/ancestry facts are accepted only through cryptographically authenticated immutable repository objects. PATH, candidate code, repository discovery, external ref-store redirection, object alternates, replacement/graft/shallow semantics, and unauthenticated object payloads are excluded from the trust-bearing path.

## Nonpromotion

W56L remains `LOCAL_COMPLETE_UNRECONCILED` and `NOT_HOSTILE_CERTIFIED`. The exhausted W56I bootstrap is not reopened. No main or PRE-MAIN movement and no Global HQ adoption is authorized by this receipt.

The next lawful act remains a fresh external recovery authorization rooted directly at exact `b53f8843092e776fb83ec584399641f5f2fc3de3`, outside the W56L candidate lineage, followed by an independent hostile audit of the exact terminal W56L successor and its complete Python/Git/ref-store/object-integrity trust envelope.