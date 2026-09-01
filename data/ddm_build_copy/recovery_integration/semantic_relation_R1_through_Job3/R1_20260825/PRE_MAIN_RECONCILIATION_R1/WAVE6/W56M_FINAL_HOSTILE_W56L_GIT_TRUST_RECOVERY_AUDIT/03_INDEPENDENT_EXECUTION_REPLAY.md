# Independent deterministic execution replay

This court did not treat W56L's self-reported attack matrix as proof. Security-sensitive process/object behavior was independently replayed in a fresh local Git repository using the candidate's exact command envelope: absolute Git executable, `--no-pager`, `--no-replace-objects`, explicit `--git-dir`, explicit `--work-tree`, and a reconstructed environment matching W56L's declared keys with no PATH.

Host used for replay:

- Git: `/usr/bin/git`
- Git version: `2.47.3`
- Git SHA-256: `356db14e102d68a1a37d8a1ac577dfd678d45d46e92f468bef8b7154e7bfdc60`
- Python isolated replay flags: `isolated=1`, `ignore_environment=1`, `no_user_site=1`, `no_site=1`, `safe_path=true`.

## W56K PATH attack — PASS / defect actually closed

A hostile executable named `git` was placed first in a hostile parent PATH with a marker payload. The trust-bearing command was executed through the explicit absolute `/usr/bin/git` path and candidate-equivalent child environment with no PATH. Exact ref resolution succeeded and the hostile marker remained absent.

This independently confirms that W56K's original bare `subprocess.run(["git", ...])` process-resolution defect is closed.

## Baseline repository hardening — PASS

Before mutation:

- `rev-parse --is-shallow-repository` -> `false`;
- `for-each-ref refs/replace` -> empty;
- `rev-parse --show-toplevel` -> exact explicit repository root;
- `rev-parse --absolute-git-dir` -> exact `<root>/.git`;
- `rev-parse --git-common-dir` -> exact `<root>/.git`;
- graft and alternates locators remained within `.git` and files were empty/absent;
- top-level `.git/objects` was a real nonsymlink directory.

## Internal loose-object symlink attack — FAIL / fatal

Baseline canonical blob payload `GOOD\n` had requested OID:

`f49b81645e9b3e194103fb700187016b10427bf5`

The corresponding loose-object file `.git/objects/f4/9b81645e9b3e194103fb700187016b10427bf5` was replaced with a symlink to an external zlib object containing:

`EVIL_BYTES_FROM_EXTERNAL_SYMLINK\n`

The attacker's actual blob OID for those bytes was:

`5c64a24ef99cfc362b44e32eda32327aaecec25f`

Thus requested OID != attacker payload OID.

After the symlink mutation, every W56L repository-hardening probe listed above still returned the same passing result. Exact candidate-pattern command:

`/usr/bin/git --no-pager --no-replace-objects --git-dir=<root>/.git --work-tree=<root> cat-file blob f49b81645e9b3e194103fb700187016b10427bf5`

returned exit code 0 and stdout:

`EVIL_BYTES_FROM_EXTERNAL_SYMLINK\n`

Git therefore followed the internal object symlink and returned bytes not bound to the requested OID. W56L's `read_blob()` and `read_commit()` accept successful `cat-file` output without recomputing and checking the Git object hash.

## Internal ref symlink attack — FAIL / corroborating

The exact local canonical branch ref file beneath `.git/refs/heads/` was replaced by a symlink to an external file containing another valid commit SHA. Candidate-pattern:

`rev-parse --verify refs/heads/integration/pre-main-reconciliation-r1^{commit}`

returned the external file's SHA with exit 0. W56L does not reject symlink descendants beneath the pinned `.git` directory or bind resolved ref bytes to a nonsymlink metadata path.

## Python isolation regression — PASS

A sibling `argparse.py` that would create an execution marker was placed beside a probe reproducing the exact W56L pre-import five-flag barrier. `python3 -I -S` reported all five flags true, imported stdlib `argparse`, and left the hostile sibling marker absent. Non-isolated execution fails the required flag barrier.

The fatal result is not a reopening of W56J/W56K Python isolation or the PATH seam. It is an uncovered filesystem/object-store redirection seam below the top-level metadata-root check.
