# P1 minimal sourcefree fan-in and authority holds

**Grade:** `TEST_ONLY_SOURCEFREE_NOT_NATIVE`. The product is a lawful local partial; it does not merge PRE-MAIN, create native authority, or silently promote a sourcefree target to an owner receipt.

## Smallest path to the receiving product

The executable path is:

```text
candidate/p1_consumer.py
  -> candidate/deps/m35/install.py
     -> bp2_joined/material_source.py + producer.py
        -> M35 firstclass source binding
  -> joined/session.py::JoinedSession.start/open
     -> R31E first-neighbor do_help (later A0/A2 encounter)
  -> joined/refusal.py for C's targetless refusal
  -> candidate/p1_no_access.py for B's same-B/no-A-access targetless C12
  -> candidate/p1_s35.py for the isolated TEST_ONLY A/T predicate
  -> candidate/p1_cold.py for a separate interpreter cold read
```

The actual imported files are copied under `candidate/deps/m35/` (20 files), its exact 48-file BP2 vendor closure at `candidate/deps/m35_vendor/`, and `candidate/deps/join_e/` (478 files). The S35 JSON is copied as a resource under `candidate/deps/s35/`; it is not installed as a native rule. No 640-file blanket transplant, no live PRE-MAIN edit, no Pyat world, and no production/native write occurred.

## What is imported and what is rejected

| Input | Actual use |
|---|---|
| M35 `@4170fbf` | First-class typed B owner/operation/quantity/event/clock/E1 source; validated before C8; tool state derived from B; same R31E consumer |
| JOIN-E `@7bf2da30` | `JoinedSession`, targetless `RefusalProduct`, lineage/provenance, cold reopen; no fork/targetless lineage reopened |
| S35 `@888ccae5` | Six conditional A/T specifications and explicit `T=NO_CHANGE`; P1 adapter is independent TEST_ONLY code |
| F1 `@1973d28` / `@8d958529` | Read only as pending receiving packet; not imported, not an acceptance |
| C9R two-act automatic route | Deliberately not installed; the S35 adapter does not call it or claim it as law |
| Native C8/C9/C12, ADP/SCI05, CAN008/011, Pyat | Not touched, not issued, not substituted |

The `NoAccessProduct` is a minimal extension of JOIN-E's targetless `RefusalProduct`: it appends one `GM01_NO_ACCESS` episode and a sidecar with `a_access_admitted=false`, no A response, and `target_id=""`. It does not make a second actor identity, does not alias B to A, and does not invent a C9 target.

## Authority and owner holds

| Surface | Status | Required owner/work |
|---|---|---|
| CAN008 A positive rule | HOLD | Original CAN008 issuer, method and receipt |
| CAN011 T practice/grant | HOLD | Separate original CAN011 owner; no acquired-practice inference |
| ADP/SCI05 actor E1/E2 | HOLD | Original ADP source and actor-access authority |
| Native C8 writer/anchor | HOLD | Protected C8 owner |
| Native C9/C12 and external owner anchor | HOLD | C9/C12 owner; separate custody/KMS |
| Targetless C10/C12 contract | HOLD | BP2P4/C9/C12 owner decision |
| C10/C11 | HOLD | Native owner |
| Pyat N11/N12 | HOLD | Pyat owner, separate flight |
| Human A5 and production adoption | HOLD | Accountable human/owner |
| Separate-root CP-A5/C9 actor | HOLD | Documented as a boundary; no aliasing or fake unification |
| F1 independent verdict | PENDING | Fresh independent receiver; not claimed by this return |
| P1 independent review | PENDING | One fresh I3 reviewer at the pushed SHA |

The product therefore has a functioning sourcefree end-user surface (A's own action, material stock, C9/C12 and later first-neighbor reply) while every native and external owner surface remains visibly held. No PRE-MAIN merge, no self-merge, no production activation, and no native person claim is made.
