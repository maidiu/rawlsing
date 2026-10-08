# PYAT HQ248 — N10E C1 AT07 local deployment placement feasibility — R1

**STATUS: `BLOCKED`**
**AUTHORITY:** `HQD-2026-10-08-248` — non-authorizing inventory and pre-approval feasibility
**BRANCH:** `agent/space-bunny-pyat-hq248-n10e-at07-deployment-placement-evidence-r1`
**TIP:** `9716656ee47fb04bf8bd6e842982d78b6490cca8` (verified remote head, matches commission exactly)

**Nothing was designated, approved, installed, allocated, or activated.** No epoch, no root,
no genesis, no credentials, no trust-store change, no real source execution, no raw survey.

---

## 1. Headline

The Mac can technically host a durable single-writer journal. It **cannot** host an
independently controlled verifier, because exactly one human principal administers the
machine and disk encryption is off. HQ therefore cannot yet make a binding owner
designation resting on real trust separation at this site.

The commission gave an explicit conditional: *if genuine independent principal separation
cannot be established, return BLOCKED, propose physical/human separation, do not fake
independence.* That condition is met, so **`BLOCKED`** is the honest status — not
`PARTIAL_NAMED_REAL_PLACEMENT_GAP`, because the blocker is trust separation, not a named
local placement detail.

## 2. HQ247's blocker, re-tested locally

HQ247 returned `AT07_OWNER_ROOT_PLACEMENT_PREFLIGHT_PARTIAL__NAMED_COMPETENCE_OR_DEPLOYMENT_BLOCKER`
from Browser/GitHub only, and stated it could not establish physical/local placement or
principal separation by inspecting role templates. HQ248 is the local follow-up. It
confirms the blocker on the actual machine and names its cause precisely.

## 3. What is deployed here: **nothing**

| Item | Finding |
|---|---|
| C1-01 source-free assembly | `rawlsing_next/tests/test_pre553_analytical_composition.py`, blob `2210fc1b4cb…` — **byte-identical to HQ247's citation** |
| Consumer | `rawlsing_next/pre553_analytical_composition.py`, blob `604c8d591d4…` — **also identical** |
| Where the 100 rows live | **in process memory** (`rows = []`, line 92); module only `read_text`s committed JSON |
| Writes performed | **none** |
| Invocation | `python -m pytest` with `PYTHONPATH=.`; no conftest/pytest.ini/pyproject/tox at repo root; **not** pip-installed |
| N10E `build_provider_case` product-path callers | **0** — every caller is under `tests/` |
| Rawlsing-owned LaunchDaemon/LaunchAgent | **none** (all 20 system daemons are third-party consumer software) |
| Test-helper ↔ product-deployment boundary | **does not exist** — there is no product deployment to bound against |

The consumer is an imported library in the *same interpreter* as the fixture that builds the
data. No process boundary, no principal boundary, nothing deployed to designate.

## 4. Journal feasibility — feasible, but not yet lawful

APFS (local, journaled) provides every primitive a single-writer durable journal needs.
Verified on the live volume: `O_CREAT|O_EXCL`, `os.replace` atomic rename, `fcntl.flock`,
`fcntl.lockf`, `os.fsync`, and **directory** `fsync`.

Feasibility at the filesystem grain is **not** a lawful writer:

- Physical writer identity is governed by **one human principal** (uid 501) who is also the
  console user, the admin, and the current shell principal.
- `/Library/Application Support` and `/var/root` are root-owned and unwritable without
  `sudo`; `sudo` is password-gated to that same human.
- **APFS gives atomicity, not append-only immutability** against a principal who owns the
  containing directory. Sequence monotonicity and nonreuse must be enforced by the owner
  application — they do not come free.
- The git tree is **not** a journal substrate: unsigned, no active hooks, rewritable by the
  same principal.

## 5. Why the verifier cannot be independent — the blocking finding

- Exactly **one** human account (uid ≥ 500); three system/service accounts.
- That human is admin + console user + current principal + sudo holder.
- **FileVault is OFF** — no at-rest confidentiality boundary, so a verifier reading here
  shares the owner's boundary.
- No verifier service, installer, or root distribution channel exists at any privilege level.

A root-owned LaunchDaemon would give a distinct **runtime** principal but the same human
would install it, so independent **control** is not established. Not faked. Reported BLOCKED.

## 6. Code census corroborating HQ247

`REGISTRAR`, `ISSUER_ROOT`, `TRUST_ROOT`, `INSTALL` → **0 files each**.
`epoch` → 4 files, all in **out-of-scope V3 contact-witness lanes**. Nothing in C1/N10E/AT07.

Two traps worth naming explicitly:

- The only `OWNER_ROOT` in the tree is `CURRENT_ACCEPTED_OWNER_ROOT`, a **frozen GT34
  literal** in `gt34_u2_v3p1_authenticated_subject_materializer.py`. It is a static
  constant, **not** a deployed root and **not** a principal.
- The only `JOURNAL` occurrence is an unrelated **FIABC T4 accounting** schema, not a C1
  AT07 build journal. Likewise `pre553_c11_repository.py` has collision logic, but it belongs
  to the C11 lane and must not be borrowed as owner authority.

## 7. Design-level boundaries — undesigned, deliberately unallocated

No epoch space, no genesis, no pinned root, no registrar, no bootstrap/collision/rollback/
fork design for a C1 AT07 build registry. Nothing was allocated. Findings 3–6 are **not**
local competence blockers — they are undesigned, and this non-authorizing commission
correctly left them alone.

Four observations for the future owner proposal: advisory locking suffices for single-writer
but nonreuse must be app-enforced; a journal inside the git tree is unsuitable; fork defence
ultimately rests on one human's exclusivity; rollback must be defined so a retired sequence
number can never be reissued (nothing currently prevents that).

## 8. Handoff discipline retained

Owner-issued **C1 → N10E registered handoff** remains mandatory; direct invocation → N10E
registration was neither present nor created (no registration surface exists at all).
`AT07_BIDIRECTIONAL_100` retained unchanged with forward 54/60 and reverse 54/62; **actual
effective context remains null** — the static `AT07_FIXTURE_ONLY` snapshot is *not* the
actual effective context. No tests representing real activation were written or run.

## 9. Disclosures

**I inadvertently mutated and then reverted a filesystem ACL.** Probing whether the volume
supports POSIX ACLs, I issued `chmod +a "everyone deny list"` against the repository root.
That command *wrote* an ACL instead of merely testing support. I caught it immediately and
reverted it with `chmod -a`; verification confirms the entry is gone, the source tree is
clean, and `HEAD` is unchanged at `9716656ee`. No production or source content was modified,
and the effect was filesystem metadata only. Disclosed rather than omitted.

Also: human identities are **redacted** — artifacts carry only structural facts (counts, uid
classes, ownership classes, permission shapes). No password, key, token, or environment
secret was accessed or emitted; `sudo` was probed for password-requirement only and never
used to execute anything. This commission named the launch tip exactly, so no tip
discrepancy arose (unlike HQ221/HQ222).

## 10. Artifacts

```
WORKER_RETURNS/PYAT-HQ248-N10E-AT07-C1-LOCAL-PLACEMENT-FEASIBILITY-R1/
  00_FEASIBILITY.md
  01_LOCAL_OWNER_AND_VERIFIER_EVIDENCE.json
  02_DEPLOYMENT_AND_JOURNAL_FEASIBILITY.json
  03_HQ_DESIGNATION_REQUIRED.md
  FINAL_DISPOSITION.json
```

Read `03_HQ_DESIGNATION_REQUIRED.md` for the evidence holes and the minimal recommended legal
next sequence. **No self-approval at any step.**

**Terminal:** `HQ248_C1_AT07_LOCAL_PLACEMENT_FEASIBILITY_RETURNED__HQ_DESIGNATION_DECISION_REQUIRED`