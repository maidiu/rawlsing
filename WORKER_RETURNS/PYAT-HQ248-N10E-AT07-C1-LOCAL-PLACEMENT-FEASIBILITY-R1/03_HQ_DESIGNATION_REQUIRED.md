# PYAT HQ248 — C1 AT07 local deployment placement feasibility — designation requirements

**NON-AUTHORIZING. This document designates nothing and approves nothing.**
Authority: `HQD-2026-10-08-248`. It is inventory and pre-approval feasibility only.

---

## 1. The one-sentence answer

The local Mac can technically host a durable single-writer journal, but **it cannot host
an independently controlled verifier**, because exactly one human principal administers
the machine and disk encryption is off. HQ therefore cannot yet make a binding owner
designation that rests on real trust separation at this site.

---

## 2. What is actually deployed here — nothing

| Question | Finding |
|---|---|
| Real C1-01 source-free release assembly | `rawlsing_next/tests/test_pre553_analytical_composition.py` (blob `2210fc1b…`, **unchanged** from HQ247's citation) |
| How it is invoked | `python -m pytest` with `PYTHONPATH=.`; no conftest/pytest.ini/pyproject at repo root; **not** pip-installed |
| Where the 100-row material lives | **in process memory** (`rows = []` at line 92); the module only `read_text`s committed JSON and never writes |
| Owner process / service deployment identity | **none exists** |
| Boundary between test helper and product deployment | **does not exist** — there is no product deployment to bound against |
| N10E `build_provider_case` product-path callers | **0**; every caller is under `tests/` |
| Rawlsing-owned LaunchDaemon / LaunchAgent anywhere on the machine | **none** (all 20 system daemons are third-party consumer software) |

The consumer `pre553_analytical_composition.py` (blob `604c8d59…`, also unchanged) is an
imported library in the *same interpreter* as the test that builds the fixture. There is
no process boundary, no principal boundary, and nothing deployed to designate.

## 3. Journal feasibility — feasible at the filesystem grain

APFS (local, journaled) provides everything a single-writer durable journal needs. Verified:
`O_CREAT|O_EXCL`, `os.replace` atomic rename, `fcntl.flock`, `fcntl.lockf`, `os.fsync`,
and **directory** `fsync`.

But feasibility at the filesystem grain is **not** the same as a lawful writer:

- Physical writer identity is governed by **one human principal** (uid 501) who is
  simultaneously the console user, the admin-group member, and the current shell principal.
- Root-owned locations (`/Library/Application Support`, `/var/root`) are not writable
  without `sudo`, and `sudo` is password-gated to that same human.
- APFS gives atomicity, **not** append-only immutability against a principal who owns the
  containing directory. Sequence monotonicity and nonreuse must be enforced by the owner
  application; they do not come for free.
- The git working tree is **not** a journal substrate: unsigned (`commit.gpgsign` unset),
  no active hooks, rewritable by the same principal.

## 4. Why the verifier cannot be independent here — the blocking finding

- Exactly **one** human account (uid ≥ 500); the other three are system/service.
- That human is admin, console user, current principal, and holder of the sudo credential.
- **FileVault is OFF** — there is no at-rest encryption boundary, so a verifier reading on
  this host shares the owner's confidentiality boundary.
- No verifier service, installer, or root distribution channel exists at any privilege level.

A root-owned LaunchDaemon *would* provide a distinct **runtime** principal. It would **not**
provide an **independently controlled** one, because the same single human would install it.
Per this commission's instruction, independence is not faked: **this is reported as BLOCKED,
with physical/human separation proposed.**

## 5. Exact evidence holes preventing a binding owner designation

1. **No concrete unique deployed writer/owner/principal.** Nothing is deployed.
2. **No independently pinned verifier reader/installer.** No installer exists or could be
   independently controlled here.
3. **No epoch space and no genesis.** No epoch machinery exists anywhere in the C1/N10E/AT07
   lane; the only epoch symbols in the tree belong to out-of-scope V3 contact-witness lanes.
4. **No approved root.** No `trust_root` or `issuer_root` symbol exists in any code surface.
   The single `OWNER_ROOT` constant found is a frozen GT34 literal and must **not** be read
   as a root or a principal.
5. **No registrar.** Zero `REGISTRAR` symbols exist; there is nothing to consult.
6. **No bootstrap/collision/rollback/fork design** for a C1 AT07 build registry. The only
   collision logic found belongs to the unrelated C11 repository lane.

Items 3–6 are **not** local competence blockers; they are simply undesigned and were
deliberately left unallocated by this non-authorizing commission.

## 6. Minimal recommended legal next steps

**Prerequisite (physical/human separation) — must precede any owner designation:**
Either (a) a second, physically distinct human-controlled host or principal to administer
the verifier side, with root material distributed out-of-band; or (b) at minimum, enable
FileVault, provision a dedicated non-human service account, and place the verifier on
*different hardware* under a different administrator.

Then, in the mandated order — **no step may be skipped or self-approved**:

```
1. HQ designates one competent C1-01 owner candidate        (distinct decision)
2. HQ separately designates the verifier installation authority (distinct decision)
3. Designated owner PROPOSES exact placement/genesis/epoch    (proposal, not approval)
4. HQ approves exact immutable bytes                         (exact root approval)
5. Owner INSTALLS approved writer + separately distributed verifier root
6. INDEPENDENT VERIFIER ACKs
7. HQ ACTIVATES the epoch
```

Only after step 7 may the owner-issued **C1 → N10E registered handoff** become non-null. A
direct invocation → N10E registration path remains forbidden at every stage, and a null
handoff is legal only post-activation. No tests representing real activation were written
or run here.

## 7. Disclosures

- **I inadvertently mutated and then reverted a filesystem ACL.** While probing whether
  the Data volume supports POSIX ACLs, I issued `chmod +a "everyone deny list"` against the
  repository root directory. That command *wrote* an ACL rather than testing support. I
  detected it immediately and reverted it with `chmod -a`; verification confirmed the ACL
  entry is gone, the source tree is clean, and `HEAD` is unchanged at `9716656ee`. **No
  production or source content was modified**, and the change was filesystem metadata only,
  fully reverted. It is disclosed rather than omitted.
- **Human identities are redacted.** Only structural facts (counts, uid classes, ownership
  classes, permission shapes) appear in the artifacts. No password, key, token, or
  environment secret was accessed or emitted. `sudo` was probed for password-requirement
  only and was never used to execute anything.
- The git object store emits unrelated `gc` warnings; no action was taken on them.

**Terminal:** `HQ248_C1_AT07_LOCAL_PLACEMENT_FEASIBILITY_RETURNED__HQ_DESIGNATION_DECISION_REQUIRED`