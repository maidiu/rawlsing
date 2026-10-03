# Competing interpretations of R9 — strongest case for each

Both convenient readings are attacked first, then the text is weighed.

## Interpretation A — "literal OS path-open accounting is non-substitutable"

**Strongest case FOR:**

1. **The account list is a list of distinct things.** Artifact 07 lists, as ten
   `mandatory_separate_accounts`, both `"path-level opens"` **and** `"decoder invocations"`
   and `"selected-column reads"` and `"full reads"` and `"metadata reads"`. If a
   path-open count were interchangeable with a reader/decoder count, the list could not
   contain both without redundancy.
2. **The law pre-empts the exact substitution.** The `explicit_warning` says: *"A count of
   'opens' is meaningless without stating whether it means OS-level path opens, reader
   invocations, or decoder calls. **These are different quantities** and C4B froze them as
   separate accounts."* This names reader invocations as a different quantity from OS-level
   path opens — the precise move a proxy would make.
3. **`path_opens` is the one slot singled out for a basis.** In the C4B template, six slots
   read `REQUIRED_EXACT_COUNT`, and `path_opens` reads
   `REQUIRED_EXACT_COUNT_AND_BASIS`. The drafters attached a *basis* obligation uniquely to
   this slot — consistent with it being the hardest and least self-evident account, and
   inconsistent with it being freely replaceable by an easier one.
4. **The principle sentence is absolute in form.** *"Access must be separately accounted at
   every distinct layer."* Not "may be approximated", not "where convenient".
5. **The `SRC27` hardened note forbids the analogous collapse explicitly**: the single
   governed full-route pass is a *workload* constraint, *"It does NOT license assuming one
   file open"*, and the misreading *"is expressly forbidden by Omega-1"*. The drafters were
   plainly alive to the class of error a proxy commits.
6. **The basis rule makes a proxy formally defective.** *"Each account must state its
   measurement BASIS, not only a count. A count without a stated basis is not an account."*
   A reader-invocation number offered as the path-open account states a basis that is not
   the account's basis. Under the rule, that is **not an account at all** — so substituting
   does not merely weaken the account, it produces no account.
7. **Independent prior work reached the same reading.** HQ190-C (Q11) marks `ACC-03
   path-level opens` **unbound** and states the freeze acceptance is currently
   *unsatisfiable*. HQ191 (Q12) reports that neither a count nor a basis is observable and —
   tellingly — **declines to relabel** the reader-invocation ceiling as an opens account,
   calling it *"an upper bound on accesses, NOT an account of opens"*. HQ194 (Q14) holds
   that R9 *"is not closed by replacing path opens with reader invocations or Python-level
   opens."*

**What would defeat A:** any text permitting an equivalent higher-level account, or stating
that the three quantities may be collapsed for the purpose of the accounting obligation. I
searched the named authorities and found no such text.

## Interpretation B — "a higher-level governed proxy preserves the intended principle"

**Strongest case FOR:**

1. **The underlying purpose is anti-collapse, not forensic literalism.** The principle is
   that a pass must not be reported as one access. A governed reader-invocation count *also*
   defeats "one pass = one access". If the purpose is served, the letter might be a
   means.
2. **`byte counts **where measurable**` shows the drafters accepted measurability limits.**
   The hedge "where measurable" acknowledges that some accounts may not be obtainable, and
   arguably licenses the nearest lawful account.
3. **An upper bound is conservative.** HQ191's reader-invocation ceiling *bounds* accesses
   from above. For a safety/authorization purpose, a conservative ceiling can be more
   useful than an exact count.
4. **AT20's phrase "declared read/decoder counts ... remain exact"** could be read as
   grouping reads and decoder counts into one exactness obligation rather than demanding a
   separate OS-layer figure.
5. **Practical necessity.** If the literal account is unobtainable on the qualified host,
   insisting on it makes C4 impossible — a reading that renders the governing contract
   unexecutable deserves scrutiny.

**Why each point fails on the text:**

- Point 1 asserts the purpose but the text *states* the quantities are different and froze
  them as separate accounts. Purpose cannot override an explicit enumeration.
- Point 2: "where measurable" attaches to **byte counts**, one specific account — it does not
  generalize into a licence to replace *any* unmeasurable account. Notably `path_opens`
  carries `_AND_BASIS`, not "where measurable".
- Point 3: the worker's own words concede the ceiling *"is not an account of opens and is not
  relabelled as one"*. A conservative bound is valuable, but it is filed under a different
  account; filing it as the path-open account is the relabelling the worker refused.
- Point 4: AT20's hostile witness says the counts *"remain exact"* — exactness of a declared
  count is not permission to relabel which quantity is declared.
- Point 5: the difficulty of satisfying a requirement is not evidence about its meaning.
  The commission says outright: *convenience is not authority.*

## Weighing

Interpretation A is supported by the primary enumeration, the enumerated basis rule, the
explicit non-substitution warning naming reader invocations, the SRC27 hardened note, and the
`_AND_BASIS` qualifier unique to `path_opens`. Interpretation B has no textual support and is
defeated by each of the four texts above; its strongest appeal is practical difficulty, which
the commission expressly bars as a ground of interpretation.

**Verdict: A.** Literal OS-level path-open accounting is non-substitutable under the frozen
law. A higher-level proxy does **not** preserve the intended non-collapse principle as an
*account* — it preserves a weaker, differently-named guarantee, and only if it is honestly
filed under its own account rather than relabelled as `path_opens`.
