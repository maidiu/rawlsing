# Re-evaluation of W56L evidence

The W56L evidence package was read as claims to test, not as inherited PASS authority.

## Findings retained

- `03_COMPLETE_TRUST_GRAPH.md`: correctly identifies trusted Python, trusted Git, repository locator, environment/config, refs, object reads, ancestry semantics, external authorization, and OS/process semantics as distinct trust nodes. Its narrow diagnosis of W56K is correct.
- `04_GIT_EXECUTABLE_PROVENANCE_CONTRACT.md`: absolute non-symlink Git, no PATH fallback, outside-repository executable requirement, and pre/post fingerprinting are materially sound for the W56K executable-resolution seam.
- `05_GIT_ENVIRONMENT_AND_CONFIG_CLOSURE.md`: reconstructed child environment materially closes the enumerated environment/config injections.
- `06_GIT_COMMAND_TRUST_MATRIX.tsv`: command minimization to Git builtins/plumbing reduces helper attack surface.
- `08_PYTHON_ISOLATION_REGRESSION.md`: the Python `-I -S` boundary remains intact.
- `10_POSTBOOTSTRAP_RECOVERY_SEQUENCE.md`, `12_LEDGER_CORRECTIVE_DISPOSITION.md`, and `14_NEXT_HOSTILE_AUDIT_CONTRACT.md`: nonpromotion, append-only correction, bootstrap exhaustion, and external authorization/audit separation are valid.

## Findings rejected at certification grain

`03_COMPLETE_TRUST_GRAPH.md` classifies Git object-database reads as canonical repository authority once environment object redirection, alternates, shallow state and replacement/graft semantics are closed. That closure is incomplete because filesystem indirection below the top-level object directory is not checked and returned object bytes are not rehashed against requested OIDs.

`05_GIT_ENVIRONMENT_AND_CONFIG_CLOSURE.md` states repository metadata attacks are closed by replace/graft/alternates/shallow/root checks. The independent loose-object and ref symlink replays refute that completeness claim.

`07_VALIDATOR_REPAIR.md` and `09_GIT_HOSTILE_ATTACK_RESULTS.tsv` omit the internal object/ref symlink classes. The 20-row matrix therefore does not cover the whole stated object/ref trust boundary.

`FINAL_VALIDATION.json` may retain the narrow statements `path_resolved_trust_bearing_executables_remaining = 0`, `git_child_environment_inherits_path = false`, and the Python isolation PASS. Its broader local conclusion that the post-bootstrap Git trust recovery is ready for external PASS cannot be certified because the immutable-object reader substrate remains redirectable.

## Court disposition

W56K is not reclassified away: its exact PATH-mediated Git executable defect is closed. W56M nevertheless discovers a deeper fatal seam in the same trust chain. W56L is therefore a valid negative-design/recovery step but not PRE-MAIN integration-ready.
