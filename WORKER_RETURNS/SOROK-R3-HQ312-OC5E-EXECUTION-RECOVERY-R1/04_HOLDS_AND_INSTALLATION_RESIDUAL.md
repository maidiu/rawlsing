# SOROK HQ312 OC5E — holds and installation residual

## Scope of every executed case

All 349 executed cases are scoped to **TEST_ONLY synthetic custody**:

* ephemeral fixture credentials whose secret is publicly derivable
  (`sha256(f"{person_id}:{role.value}:EPHEMERAL_FIXTURE")`);
* a transparent `TEST_ONLY_EPHEMERAL_ROOT` verification root;
* a sourcefree corpus with no raw survey data and no real subject;
* an explicitly modeled, not observed, structural premise channel.

A mock signer does **not** create real independent custody.  Hash equality is
**not** independent semantic agreement.

## Not claimed

| Item | Status |
|---|---|
| Real signer institution | **NOT CLAIMED** |
| Protected holdout | **NOT CLAIMED** |
| Durable external journal | **NOT CLAIMED** |
| Independently issued semantic oracle | **NOT CLAIMED** |
| Cross-process `C07` | **NOT_REACHED** — absent an API |
| External model calls | **NONE** |
| Original survey data | **NONE** |
| V3, product / PRE-MAIN / CURRENT edits | **NONE** |
| Adoption | **NOT CLAIMED** |

## Author-source residual

The author source was **not** repaired inside this independent review, as
required.  The following remains open for the OC4 author:

| Family | Cases | Residual |
|---|---:|---|
| A1 normalization-equivalent alias of an allowed field | 10 | multiplicity-discarding set comparison in `detect_leakage` |
| A2 NFKC-invisible confusable leak tokens | 6 | normalization-only value scanning |
| A3 malformed signature objects | 18 | no `isinstance` guard before attribute dereference in `require_second_signature` |
| A4 non-enum role string | 1 | role used as enum without validation |
| A5 unhashable unblind holder | 3 | holder identity not type-checked before dict access |
| A6 capsule identity field types | 11 | no capsule field type validation before commitment derivation |

Boundary observation (not a RED): the holder-grant registry sits outside the
escrow event seal by design; substituting it is undetected but still fails
`unblind`, and `authorize_holder` refuses non-`CUSTODIAN` roles.

## Ten historical original REDs

All ten remain literally failing and are **retained**, not concealed: six are
procedural or early-refusal, four are content-only mock-signature positives
superseded by the stricter full-capsule commitment law.  No canonical
capsule-signature identity requirement is weakened by this review.

## Installation residual

Nothing is installed.  OC4 remains a sourcefree candidate; adoption remains
with the competent owner and requires a distinct independent court.  The
next concrete step is the OC4 author repairing A1–A6 and re-running this exact
court, after which the regression bank must flip from 49 RED to 49 PASS with
the 110 controls unchanged.

## Environment

Python 3.11.3, pytest 9.1.1, macOS, isolated local runtime under
`/tmp/oc5e-runtime` with `PYTHONPATH` pointing at the staged sealed closure.
Muse Spark inside the existing Muse-configured OpenCode installation; one Muse
agent completed staging, the whole native court, the new hostiles, the verdict
and the push.  No Codex, DeepSeek-Harness, helper, automatic model switch or
paid calls.  Cash/quota was not observable and was not used.
