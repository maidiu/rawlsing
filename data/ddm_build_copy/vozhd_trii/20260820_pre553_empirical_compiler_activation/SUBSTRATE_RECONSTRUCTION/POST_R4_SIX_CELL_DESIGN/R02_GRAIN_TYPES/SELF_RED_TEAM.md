# SELF RED TEAM — R02 GRAIN / TYPES

Status: `NON_DISPOSITIVE__SELF_ATTACK`

## Attack 1 — “Question metadata is obviously constant”

No. A decoder usually presents labels, missing declarations, formats and type as variable metadata, but R02 cannot convert an implementation convention into an unlimited theorem. The safe scope is **per sealed release-variable under the frozen decoder contract**. If a source family or future decoder exposes event-varying metadata, that field leaves question grain or gains an exact exception lane.

**Defeat condition:** two source-native events with the same declared release-variable determinant but distinct dependent metadata.

**Response:** revoke the FD for that scope; store the field directly or block publication.

## Attack 2 — Selected labels and host-language equality

A tempting reconstruction is `selected_label = labels[raw_value]`. That is unsafe if lookup identity is a Python/SQL equality relation: `True`, `1`, and `1.0` can collide; signed zero compares equal; NaNs have hostile equality; cross-type dictionary keys can be coerced.

**Required repair:** typed-key identity is `(type_tag, exact_payload_bytes)`. If the source dictionary cannot be represented as a total unambiguous mapping on that key, selected label remains event-grain/direct.

## Attack 3 — Float textual round trip

Accepted R4 terrain uses `repr(float)` then `float(text)`. That is not an adequate physical identity contract for NaN payload/signaling bits and is not the standard R02 should inherit.

**Required repair:** persist decoder-observed IEEE bit pattern for float32/64. This preserves `-0.0`, infinities and NaN payload bits that survive the frozen decoder. Do not overclaim recovery of raw file bits already lost by the decoder.

## Attack 4 — Integer narrowing by current corpus

CLOSED_35 maxima are evidence about CLOSED_35, not the legal value domain of a native type and not future authority.

**Required repair:** width selection comes from immutable native storage/type/cardinality metadata. Every write is range-checked. Out-of-range means deterministic widening, exact escape, or pre-publication failure.

## Attack 5 — Strings are not “just UTF-8”

UTF-8 is safe only as an exact encoding of the decoder-observed Unicode sequence. A serializer can still destroy identity by NFC/NFKC normalization, trim, case fold, embedded-NUL truncation, invalid-codepoint replacement, or empty-string/null conflation.

**Required repair:** test exact sequence round trip, preserve embedded NUL and empty string, and provide a native-special/opaque escape if the decoder exposes non-Unicode bytes.

## Attack 6 — Date/time coercion

Source numeric values can have date/time-looking formats. Converting them to epoch timestamps can alter range, calendar, unit, timezone or even invent semantics not authorized by the source.

**Required repair:** default is native numeric/string raw payload + exact source format metadata. Use a date/time lane only if the frozen decoder/source contract exposes an exact native date/time type and the carrier round trip is total.

## Attack 7 — Missing declarations imply event state

They do not. A variable-level declaration tells how the source describes special values/ranges; the event still has a physical state that must distinguish observed, system missing, user-missing declarations, extended missing and other physical states under the governing contract. LiTS/EVS/Afro accepted evidence defeats label/raw-code shortcuts.

**Required repair:** keep event physical state directly in R02. A later source-specific classifier must be proved separately before removal.

## Attack 8 — Rectangular source means physical row position is identity

Even when source geometry is rectangular, Parquet row position is mutable. Repartitioning, compression, filtering during a buggy rewrite, or a different sort can change physical position.

**Required repair:** implicit identity is a logical arithmetic locator derived from sealed source coordinates and variable count, never the current storage row index. If exact traversal is not certified, keep explicit coordinates/map.

## Attack 9 — Repeated/ranked/MR compaction erases topology

A geometric cell locator does not authorize collapsing physical variables. WVS ordered-slot examples and overlapping MR metadata show why. A conceptual-question merge can change order, multiplicity and ExactRef.

**Required repair:** source variable ordinal remains physical identity; topology is additional metadata. All MR memberships are preserved, including overlaps/reentry.

## Attack 10 — Hot/cold creates an archival second class

If “cold” becomes optional, the hot incidence file silently becomes a weaker second authority that cannot reconstruct provenance, labels, missing declarations or topology.

**Required repair:** hot and cold are members of one sealed canonical release. Missing cold material is corruption/incompleteness, not a degraded-but-valid positive state.

## Attack 11 — Sparse defaults become a hidden frequency heuristic

A sparse override format can tempt the compiler to select the most frequent value or first observed value as the default. That turns corpus coincidence into authority and creates brittle rare-exception behavior.

**Required repair:** default values come only from an explicit determinant. Observed equality may validate a dependency already authorized; it cannot create one.

## Attack 12 — C13/C19 complexity outruns the benefit

If a field is tiny, if the determinant requires an elaborate exception hierarchy, or if a hot/cold split forces many synchronized manifests and opens, direct event storage may be cheaper and safer.

**Rejection rule:** where proof/maintenance complexity is disproportionate to the repeated bytes removed, store directly. Minimality outranks clever compaction.

## Attack 13 — Source-family generalization from CLOSED_35

Even a complete 35-file scan cannot prove future values/types. It can prove concrete counterexamples and current source geometry; it cannot establish “NaN never occurs,” “ordinals always fit uint16,” or “IDs are globally unique.”

**Required repair:** design the lane/overflow/failure law over the declared representable domain, not over observed values.

## Attack 14 — Semantic leakage

It is easy to mistake a physical lane tag such as `NATIVE_MISSING_TAG` for C11 semantic absence, or to treat a label dictionary code as canonical response meaning.

**Required repair:** R02 tags are source-physical only. C11/upstream semantic authority continues to own semantic response/absence. Downstream code cannot branch on R02 physical tags.

## Final self-red-team verdict

The proposal survives only in its narrow form: authority-proven grain, exact tagged physical identity, explicit event physical state, conditional typed-label derivation, conditional logical geometry, and fail-before-publication on violation.

Any attempt to broaden it with frequency defaults, semantic codebook inference, physical-row identity, text-float identity, or source-family/global respondent-ID assumptions should be rejected.
