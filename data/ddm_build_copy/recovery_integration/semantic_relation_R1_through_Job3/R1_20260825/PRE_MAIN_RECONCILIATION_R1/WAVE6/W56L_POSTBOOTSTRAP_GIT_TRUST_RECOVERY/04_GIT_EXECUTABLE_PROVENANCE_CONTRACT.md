# Git executable provenance contract

Authoritative predecessor invocation now requires:

`python3 -I -S .../validate_enforcement_candidate_from_canonical.py --repository-root <ABSOLUTE_REPO_ROOT> --trusted-git-executable <ABSOLUTE_GIT> <candidate> <audit_ref> <authorization_ref>`

## External trusted-host prerequisites

1. trusted Python interpreter;
2. trusted absolute non-symlink Git executable;
3. stable operating-system process/filesystem semantics for the duration of execution;
4. externally supplied absolute repository root.

The validator proves candidate-controlled state cannot select the Git executable by requiring an absolute path, rejecting missing/non-file/non-executable targets, rejecting symlink components, rejecting any Git target resolving inside the repository, and never using PATH to select Git.

The exact Git path and a pre-execution fingerprint are recorded: realpath, SHA-256, device, inode, size, and mtime_ns. The same fingerprint is recomputed after all trust-bearing operations; mismatch fails integration eligibility.

The repository root is established independently of Git from the explicit absolute host argument. A relative, symlink-containing, nonexistent, noncanonical root fails before the first Git subprocess. The executing script must lie beneath that root.

There is no fallback to bare `git`, `which git`, candidate helper code, or repository-local executable discovery.

TOCTOU beyond the pre/post identity check is bounded by the declared external prerequisite of stable host filesystem/process semantics; host kernel or privileged binary substitution is outside repository-controlled authority.