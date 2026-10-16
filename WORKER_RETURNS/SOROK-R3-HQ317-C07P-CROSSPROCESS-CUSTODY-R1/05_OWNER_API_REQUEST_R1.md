# SOROK HQ317 C07P — minimal owner API request

**From:** the HQ317 C07P experimenter.
**Status:** `OPEN__AWAITING_COMPETENT_OWNER`.
**Nature:** a request for two small public interfaces on the pinned custody prototype. It is **not**
a proposal to add a real institution, a real signer or a real issuer, and it must not be read as one.

Both holds below were found by a **measured** audit of the native `EscrowState` public surface
*before* any adapter was written, and both are stated in the preregistration at commit `82ba75680`.
Neither was worked around by mutating internal state, because doing so would forge the exact authority
this experiment is testing.

---

## 1. `C07_DEPENDENCY_TS` — escrow event timestamps cannot be restored faithfully

### What was measured

`EscrowState.unblind(capsule_id, holder)` and `EscrowState.record_exposure(capsule_id, exposed_to,
purpose)` both stamp `time.time()` internally. Neither exposes a timestamp parameter, and the class
offers no `replay_event`, `restore`, `import` or `export` counterpart.

Consequence: replaying an authorised lifecycle through the public API reproduces `committed`,
`_capsule_seals`, `released`, `holder_roles`, the exposure log and `verify_ledger_integrity() ==
True` — but **re-stamps every escrow event timestamp**. The journal retains the true values, so they
remain verifiable as *journal* facts; they are simply not carried into the reconstructed escrow.

Note this does **not** affect the capsule: `capsule_envelope_commitment` is a pure function of the
capsule's 18 fields and contains no escrow timestamp, so **full 18-field envelope binding survives a
restart exactly**. The gap is confined to escrow event times.

### Why it was not worked around

Three tempting workarounds were all rejected:

| Workaround | Why rejected |
|---|---|
| rewrite `state.ledger` entries after replay | forges the ledger the experiment is meant to validate |
| `object.__setattr__` on the reconstructed state | forges authority through a private channel |
| persist a pickled live `EscrowState` | unsafe, unversioned, and would restore private internals verbatim |

Each would have produced a green test and a dishonest claim.

### Minimal request

Either is sufficient; both are small and additive.

**Option A — optional timestamp on the two writers**

```python
def unblind(self, capsule_id: str, holder_person_id: str,
            *, at: Optional[float] = None) -> Dict[str, Any]:
    ...  # use at if supplied, else time.time()

def record_exposure(self, capsule_id: str, exposed_to: str, purpose: str,
                    *, at: Optional[float] = None) -> None:
    ...
```

**Option B — an explicit replay entrypoint**

```python
def replay_event(self, record: Mapping[str, Any], *, at: Optional[float] = None) -> None:
    """Apply one already-authorised event. Caller must supply `at`."""
```

Option A is smaller. Either keeps the existing default behaviour byte-identical, so the 898-case
accepted closure should not move.

### What would be proven afterwards

A cross-process restore in which `ledger[i]["ts"]`, `unblinded_at` and `exposure_ts` are **bit-identical**
across processes, and `C07_DEPENDENCY_TS` can be closed.

### Owner decisions this does NOT pre-empt

- Whether escrow event times should be replayable at all, or whether they are deliberately ephemeral
  runtime facts that must **not** be persisted. That is a contract question, not an implementation one,
  and this experiment takes no position on it.
- Any change to the append-only or integrity semantics.

---

## 2. `C07_DEPENDENCY_REVOKE` — custodian revocation is not expressible

### What was measured

`EscrowState.authorize_holder(person_id, role)` exists. There is **no** revocation counterpart: no
`revoke_holder`, no `deauthorize`, no way to remove a grant through the public API. `holder_roles` is a
plain public dataclass field, so it *can* be mutated directly — which is exactly why the adapter does
not: direct mutation would let a caller silently manufacture a revoked or reinstated custodian outside
the journal, defeating the point of the experiment.

`test_N16_revoke_holder_is_not_expressible_through_the_public_api` asserts the **absence** of the
interface. This is the honest outcome: revocation was requested for testing and is not available, so
it was not tested.

### Minimal request

```python
def revoke_holder(self, person_id: str) -> None:
    """Remove a fixture custodian grant and make it journal-visible."""
```

Expected semantics for the owner to decide:

- Must refuse to revoke a holder who has already unblinded a capsule, or must cascade — the answer is
  a policy call.
- Must leave a journal-visible event so revocation survives a restart and is auditable.
- Should refuse to revoke the fixture's built-in `runner1` / `custodian-alice` defaults, or should the
  defaults become ordinary grants that can be revoked.

### What would be proven afterwards

An authorised custodian commits, a second is granted and then revoked, the journal records the
revocation, process A dies, process B restores, and the revoked holder is genuinely refused by the
reconstructed escrow — across a real process boundary.

---

## 3. Explicitly out of scope for either hold

Neither request authorises, implies or anticipates:

- a real signer, institutional custodian, or external escrow service;
- an externally anchored or cryptographically protected journal;
- production durability claims;
- semantic issuance or any widening of the lexical/Unicode leakage gate;
- production, V3, N12, CURRENT or PRE-MAIN admission;
- adoption of C07P itself, which still requires a **distinct independent review**.

The anti-tamper ceiling documented in `03_CRASH_FATE_MATRIX_AND_THREAT_OUTCOMES_R1.md` §4.2 — an
attacker who can rewrite both the state and its unkeyed digest — is **not** closable by either of these
interface changes. Closing it needs an external append-only anchor or a key held outside the journal's
trust domain. That is a different, much larger authority question, and C07P does not ask for it.
