# W56N VOZHD return

Worker branch: `agent/vozhd-premain-w6s-object-identity-ref-provenance-recovery-r1`

Exact starting HEAD: `a94c5613dba1f3d3121be244296d0d3733003507`

W56M hostile terminal consumed: `4d7e806ac31317d500b94a18171d76295ebf01f7`

Local ruling: `LOCAL_COMPLETE_UNRECONCILED__OBJECT_IDENTITY_AND_REF_PROVENANCE_RECOVERY_READY_FOR_EXTERNAL_REVIEW`

W56N repairs the two W56M trust propositions without collapsing them. Object authority is now cryptographic identity: an exact requested OID selects SHA-1 or SHA-256 by width, trusted Git supplies the expected object type and exact payload, and Python stdlib independently recomputes `H(type + SP + decimal_byte_length + NUL + payload)` and requires equality to the requested OID before the bytes can become governance evidence. Object-storage pathname is not object authority.

Ref authority is separately bounded metadata provenance: only exact full `refs/heads/...` and `refs/remotes/...` values read directly beneath the pinned `.git` metadata root from nonredirected loose ref files and/or `packed-refs` are admissible. Symbolic refs, malformed values, symlinked files/components, unsupported ref storage, duplicate/ambiguous packed storage, and loose/packed disagreement fail closed. A resulting OID is not accepted as a ref target until it independently verifies as a commit object.

Canonical governance paths no longer use `commit:path`; ancestry no longer trusts an unverified commit payload; changed-path jurisdiction no longer trusts `diff-tree`. All three are reconstructed from verified commit/tree/blob objects.

Defensive local replay: 24/24 deterministic checks PASS, including W56M-grain loose-object substitution where raw `git cat-file` succeeds but W56N rejects the payload by hash mismatch, redirected ref storage rejection, loose/packed determinism, packed-object compatibility, and SHA-256 OID selection.

W56L process-isolation properties remain: Python `-I -S`, no repository import path, explicit absolute trusted Git outside the repository, no child PATH authority, minimal Git environment, stable executable fingerprint, explicit repository and `.git` roots, and replacement/graft/alternate/shallow protections.

Status remains local and unreconciled. Bootstrap is exhausted. No PRE-MAIN movement, `main` movement, integration, Global HQ banking, or canonical inheritance is performed or implied. Exact terminal SHA is returned externally after the final evidence/ledger commit because a commit cannot contain its own SHA without self-reference.