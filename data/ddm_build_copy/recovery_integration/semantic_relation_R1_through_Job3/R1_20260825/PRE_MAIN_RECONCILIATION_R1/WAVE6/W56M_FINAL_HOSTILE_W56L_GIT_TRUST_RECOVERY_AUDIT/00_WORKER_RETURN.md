# W56M FINAL HOSTILE W56L GIT TRUST RECOVERY AUDIT — WORKER RETURN

Starting HEAD: `f069eae072fae136e5dfda0a43a3c4b62c2debde` (exact immutable W56M authorization).
Candidate: `a94c5613dba1f3d3121be244296d0d3733003507`.
Canonical recovery base: `b53f8843092e776fb83ec584399641f5f2fc3de3`.
Authorization nonce: `decbab4c9cb208e24e529fadb59fe9e7`.

## Terminal ruling

`BLOCKED__ENFORCEMENT_NOT_INTEGRATION_READY`

Exact fail-closed blocker:

`FAIL_CLOSED__INTERNAL_GIT_OBJECT_STORE_SYMLINK_REDIRECTION_ALLOWS_OID_BYTES_SUBSTITUTION`

W56L genuinely closes W56K's narrow bare-PATH Git executable substitution defect: the candidate requires an explicit absolute non-symlink Git executable, removes PATH from the Git child environment, and preserves Python `-I -S` isolation. Independent replay confirmed an attacker-prepended fake `git` did not execute.

However W56L does not close the complete repository-object trust boundary it claims. It validates only the top-level `<repository>/.git/objects` directory. It does not reject symlinked loose-object files or object-store descendants. In an independent deterministic fixture satisfying W56L's shallow/replace/root/gitdir/common-dir/graft/alternates hardening predicates, a loose object path for requested OID `f49b81645e9b3e194103fb700187016b10427bf5` was replaced by a symlink to an external zlib object whose actual blob OID was `5c64a24ef99cfc362b44e32eda32327aaecec25f`. Exact trust-sensitive `git cat-file blob <requested-OID>` returned the external attacker bytes with exit 0.

A second independent fixture showed a symlinked `.git/refs/heads/...` file redirects exact `rev-parse --verify <full-ref>^{commit}` output to an external ref file. This is corroborating ref-redirection evidence; the loose-object substitution is independently fatal.

Therefore required propositions 4, 5, 6 and 14 do not pass at the disputed grain. Canonical schemas, manifests, commit objects, ancestry headers, and immutable evidence bytes cannot be certified as coming from the intended immutable repository objects merely because the Git executable, environment, and top-level metadata directory are pinned.

No candidate repair, PRE-MAIN movement, `main` movement, integration, bootstrap reuse, or Global HQ adoption was performed.
