# PYAT HQ280 PV3 C02HR — Independent producer-authentication hostile

**TERMINAL:** `HQ280_PV3_C02HR_PRINCIPAL_BOUNDARY_INDEPENDENT_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**SECURITY GRADE:** `NOT_A_TRUST_BOUNDARY__DEMO_ILLUSTRATION_ONLY`
**Branch:** `agent/reviewer-pyat-hq280-pv3-c02hr-separate-principal-hostile-r1` @ `f279541a53f2fd996ea8074b754928c2b96720e9`
**Candidate C02H:** `82309fe17c70324217382d0550ce1cc591e39eae` — module blob `eabb25c8a2b50256cf3fe85c1f6e7376da9e19f5`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **Review only.**

## 1. I forged a valid credential and the verifier accepted it

The commission asked me to *actually* forge with the known keys rather than trust the candidate's examples. I did, and it worked.

**F3 — REAL FORGERY ACCEPTED.** I took a genuine credential, substituted its `credential_id` and `scope`, re-serialised its `signed_material()`, and signed the new canonical bytes with the **known private exponent recovered from the candidate's own source constant**. `VerifierProcess.verify()` **accepted it**. No special access was needed beyond the committed source.

## 2. Why it cannot be a trust boundary (all four verified at source + runtime)

| # | finding | evidence |
|---|---|---|
| **F1** | the keypair is a **fixed hardcoded constant**, identical for every principal | `_rsa_keypair()` returns `p,q = 61,53 → n=3233, phi=3120, e=17, d=2753`; `pow(e,-1,phi)` is computable by anyone |
| **F2** | honest baseline verifies | control |
| **F3** | **forgery accepted** | substituted credential re-signed with `(n,d)` verifies |
| **F4** | the trust root is a **caller-supplied constructor argument**, not a pinned constant | `VerifierProcess(trusted_root=<any string>)`; `_public_keypair` just `int()`s the string. A self-anchored "EVIL-ISSUER" verifier accepts its own credentials — i.e. **root swap is achievable by construction**, which is precisely what the candidate's stub declines to attempt |
| **F5** | the candidate's adversarial helpers are **inert stubs, not tests** | `AttackerProcess.forge_credential` sets `signature = semantic_hash({"forged": True})` — **not an RSA integer** — and its docstring says "Will fail verification"; `swap_root` and `self_register_issuer` each `return False` **unconditionally without attempting anything** |

**This is exactly the failure mode the commission warned about: the "13-case court" passes because its attackers never attack.** A stub that returns `False` is indistinguishable, in a green test run, from a boundary that holds.

## 3. Cryptographic vs security verdict

- **Cryptographic:** the RSA arithmetic is *correct*; signatures verify. The design is a faithful **illustration** of issuer/verifier separation.
- **Security:** `e=17, n=3233, d=2753` is factorable by inspection; a **single shared keypair** across all principals means "separation" separates *objects*, not *principals*; and an unauthenticated root argument means the verifier trusts whoever constructed it. **A demo key and a demo root are not an authentication mechanism**, and no amount of green court output changes that.

## 4. B5/M2 publication exposure (reproduced)

The same weakness I documented in F8F holds: **`LearnedProductLifecycleExecutor` treats a caller-supplied subject as trusted**, so a forged closure claim, fake permission ceiling and fake receipt refs all publish. C02H does **not** close that path — it wraps a *demo* credential in front of it. The accepted-owner enforcement paths that remain open are therefore unchanged: **(a)** B5 publication/currentness accepts caller-supplied provenance; **(b)** no producer-issued subject credential exists to bind a real publication to a real principal. C02H provides neither.

## 5. Exact holds

1. **No competent issuer exists** — a fixed shared demo key is not a principal, and a caller-supplied root is not a trust anchor.
2. **`REAL_EXECUTION` / production credential issuance: NOT GRANTED** (and not performed).
3. **G0b / CURRENT / selected-service: NOT GRANTED.**
4. **B5/M2 caller-supplied trust boundary: OPEN** (unchanged).
5. Not executed here and recorded **UNKNOWN, not PASS**: real HSM/keystore integration, key rotation, revocation-list authority, and multi-principal separation with distinct keys.

**Terminal:** `HQ280_PV3_C02HR_PRINCIPAL_BOUNDARY_INDEPENDENT_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
