# FIELD FORGE R1 — PRESSURE ESTIMATION EVIDENCE HIERARCHY

Status: **EXPLORATORY / NON-BINDING / METHOD-GOVERNANCE CONTRACT**

Configuration-dependent pressure footprints will often encounter sparse respondent support.

Rawlsing must not solve sparsity by silently converting modeled estimates into empirical facts.

Hard law:

```text
DIRECTLY OBSERVED DISTRIBUTION
!=
PARTIALLY POOLED ESTIMATE
!=
MODEL-DERIVED PREDICTION.
```

All three may be useful. They carry different authority.

---

# 1. EVIDENCE LEVEL E0 — DIRECT EMPIRICAL

Requirements:

- exact lawful risk set;
- direct respondent support;
- correct weights/design;
- exact J/coadministration authority;
- sufficient support under a governed adequacy law.

Output state:

```text
DIRECT_EMPIRICAL_PRESSURE_EVIDENCE
```

This is the strongest footprint evidence.

---

# 2. EVIDENCE LEVEL E1 — DIRECT BUT THIN

The exact configuration exists but support is too small/unstable for reliable distribution estimation.

Output:

```text
DIRECT_BUT_UNDERPOWERED
```

Do not convert to `NO PRESSURE` or `NO DIFFERENCE`.

The cell can be forwarded to lawful pooling/walkback logic.

---

# 3. EVIDENCE LEVEL E2 — PARTIALLY POOLED / HIERARCHICAL

A statistical model borrows strength from related configurations while retaining the exact target configuration.

Possible methods:

- multilevel multinomial/logistic models;
- Bayesian hierarchical partial pooling;
- regularized log-linear models;
- generalized additive local models where appropriate.

Required output state:

```text
MODEL_SUPPORTED_PARTIALLY_POOLED_ESTIMATE
```

Must record:

- model identity/version;
- pooling hierarchy;
- priors/regularization;
- direct target-cell support;
- posterior/interval uncertainty;
- sensitivity diagnostics.

This is **not** direct respondent fact.

---

# 4. EVIDENCE LEVEL E3 — LAWFUL POSITION WALKBACK

Instead of estimating the exact sparse profile, Rawlsing may broaden the query through a separately governed positioned-subject walkback relation.

Examples conceptually:

```text
exact profile
-> broader position neighborhood
-> broader lawful region
```

The operation must expose information lost at every step.

Output:

```text
PROXY_POSITION_EVIDENCE
```

Hard law:

```text
PROXY
!= EXACT FACT.
```

FIELD FORGE should reuse the existing positioned-subject possibility/walkback program rather than invent a second broadening system.

---

# 5. EVIDENCE LEVEL E4 — MODEL EXTRAPOLATION

The model predicts a configuration with little or no direct local support.

This may be useful as exploratory computation but is weak authority.

Output:

```text
MODEL_EXTRAPOLATION_ONLY
```

Default persona-generation use should be highly constrained or fail closed unless the V3 consumer explicitly permits low-authority priors.

---

# 6. NO-EVIDENCE STATES

Preserve:

```text
NOT_OBSERVED
ROUTING_BLOCKED
J_AUTHORITY_BLOCKED
NONCOMPARABLE
OUT_OF_SCOPE
INSUFFICIENT_POSITION_ROLE_AUTHORITY
```

None may be converted into a modeled zero.

---

# 7. ADEQUACY LAW

FIELD FORGE needs a separate empirical adequacy contract governing when a cell/complex is sufficiently supported for E0.

Do not use one universal N threshold without considering:

- survey weights/effective sample size;
- outcome dimensionality;
- number of joint states;
- design effects;
- rare/minority branch preservation;
- requested uncertainty tolerance.

The adequacy law is technical/statistical rather than sociological, but it must be frozen/versioned.

---

# 8. PERSONA GENERATION

The positioned social-world packet should include evidence level with every disposition probability.

Example:

```text
complex A: .48
basis = DIRECT_EMPIRICAL

complex B: .31
basis = PARTIALLY_POOLED

complex C: .21
basis = PROXY_POSITION_EVIDENCE
```

V3 may weight/use these differently.

Never merge them into an unlabeled single posterior.

---

# 9. HOSTILE CASES

Reject:

- model estimate emitted as direct prevalence;
- underpowered cell emitted as no effect;
- zero observed cases emitted as impossible when sampling/routing could explain zero;
- proxy walkback concealed from consumer;
- pooling across semantically noncomparable contexts;
- hierarchical random effects treated as field ontology;
- strong shrinkage erasing real minority branches without diagnostics.

---

# 10. CURRENT RECOMMENDATION

Pressure-footprint computation should expose a **typed evidence ladder** rather than pretending all conditional probabilities have the same empirical status.

This makes sophisticated modeling compatible with Rawlsing's zero-loss epistemic discipline.
