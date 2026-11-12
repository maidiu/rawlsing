# C-2 — Agent A counterconstruction R2: semantic range closure with a real bounded witness model

**Status:** SOURCEFREE MODEL CONSTRUCTION PASS; original #919 engineering completion **HOLD**.  
**Adversary received:** PR #923 exact challenge HEAD fc6b75ec83795931df5d8f47d7a31553198ca05a; the six-test proof model blob 6c2321bfcb211383ad4123536d878a30ba620803 and independent findings blob 6804a53b7c13c8ec05683ae2a03bfd1f625346a9.  
**Starting incumbent:** Agent A @ 4616a1f411550c26914faf31a21d4444382a9b99.  
**Frozen source:** protected PRE-MAIN @ 6a5c12f04323d74001f9632063ec907f4fc4468e.  
**R2 branch:** agent/pyat-c2-counterconstruction-semantic-range-r2 created **from the exact #923 HEAD**, not from an older rival or protected branch. R2 preserves both earlier returns and adds one tested sourcefree construction plus a corrected original ABI. No protected or native PYAT source, #910, #923, W03/W04 paused HQ, original source data, scientific/host issuer or other worker's return was modified. Immutable final HEAD to be verified after the final commit.

## 1. Adjudication of the opponent's actual return

| Category | Judgment grounded in exact source and tests |
|---|---|
| **Genuine victory** | PR #923 demonstrates a missing invariant: authenticated complete **object/ref inventory** is insufficient to guarantee **semantic selector range completeness** at _pre553_query_predicate._select_respondent_events. It also identifies the O(N)-memory inventory_refs() signature. Both defects are valid, accepted, and corrected in the R2 inherited original artifact. |
| **False accusation corrected by opponent** | An earlier claim that Agent A had a duty under #919 to implement production code was false: the commission expressly limited this research cut to sourcefree/read-only, without restarting paused W03/W04 or changing protected code. The challenge was right to reject that accusation. |
| **Incomplete victory** | Their six tests are an honest in-memory independent **model**, but SemanticRangeStore recomputes a complete selector_root over all postings **on every select**. It offers neither a bounded authenticated inclusion/exclusion proof nor a verifiable empty range with predecessor/successor adjacency. The new sourcefree test goes beyond that model. |
| **New defect in their model, not an allegation against production** | Their expected_selector_bindings emits native/canonical/component aliases but does not exercise the native_only override, include_component flag, state-filter select, deduplicating one event matching several aliases, native exact output ordering, or a complete respondent/target scope attestation. Its U2/R2 nonexistent scope select returns empty rather than refusing without an admitted respondent/domain. None establishes the actual native I03 contract; their own report correctly labels model-only evidence. |
| **New defect in my initial R2 model, discovered and repaired** | R2 initially used caller-supplied known_respondents / allowed_targets, which could turn an invented scope into apparent certified emptiness. Replaced by a separately anchored Scope root bound to exact release; hostile attempted scope/target forgery now fails. Initial per-event global occurrence uniqueness used an in-memory set: replaced by disk-backed SQLite primary-key enforcement, with staging tables dropped after sealing. |
| **Missed opportunity** | The necessary successor interface is an **I02-committed derived semantic index** with verified complete ranges and authenticated adjacent boundaries; it can be built without preserving a second full canonical event-body corpus. Bounded verification is possible at model scope with SHA-256 Merkle paths, while native source and current-use authority remain separate. |

**Critique of rhetoric:** The opponent's "fully implementation-ready" criticism of the old ABI was earned. Their 6/6 success does not show a native engine vulnerability, a 6 GiB compliant reader, or production S2. R2's 19/19 also does not. Both parties owe #919 the complete eventual sourcefree vertical slice; neither is now entitled to claim it exists.

## 2. Actual constructed correction: sourcefree disk-backed SHA-256 range witness

**Artifact:** [tests/test_verified_range.py](tests/test_verified_range.py), a single standalone Python unittest module using only Python stdlib, SQLite, tempfile, SHA-256, heapq and dataclasses. Tested locally; exact Git blob pinned in the R2 execution receipt below. It is a **testable reference construction**, not native PYAT I02/I03 code and not a qualified publisher.

The construction has an actual external-sort-compatible SQLite staging table (PRAGMA temp_store=FILE), a disk-backed PRIMARY KEY over full event occurrence keys, one sorted leaf table and persisted SHA-256 Merkle node levels. All insertions come from the *source-event fixture stream*, not from untrusted index rows. The builder emits native, authorized-in-fixture canonical and component selector aliases with exact occurrence identity and typed state, uses deterministic source-native-event ref ordering, checks uniqueness, and anchors a versioned tuple of **source, release, replay, proof count, semantic root, qualified respondent/target scope root**. It then drops the staging posting table and occurrence uniqueness ledger; only locator and hash levels remain live for saved reads.

For a requested semantic selector, verify **each** selected posting's inclusion against the independently held root, assert consecutive exact leaf ordinals and inspect authenticated adjacent predecessor/successor leaves. Empty selection requires the neighboring leaves to be consecutive and bracket the requested prefix; absence of a SQL hit is not proof. State filtering happens **after** complete exact selector proof. The native selector semantics are a union over native plus authorized canonical and (only if requested) component identities; native_only overrides alias selection; duplicate alias matches yield one event/occurrence, still preserving multiple distinct events; every event's typed state participates in the committed leaf. The final caller-visible tuple is constructed **only after every included semantic range and boundary has been verified**, so a late failure does not release a partially proved result in this model. A future streaming production reader needs equivalent atomic read/serve and concurrent-file snapshot semantics.

This is a *rooted range proof model*, not a complete source-corpus cryptographic certification. The external expected anchor must be produced at **original I02 full event-corpus qualification**, not minted from an attacker-supplied local tree. The model's test fixture creates that expected anchor from known events, retains it outside subsequent mutations, and demonstrates that a second internally coherent but truncated tree cannot substitute for the issued one. Real signature/custody issuers, original source equivalence, replay closure and host/current authorization remain unimplemented. **Merkle inclusion proves commitment to the posted key/value, not that the publisher originally derived all postings from authoritative C11 events**; the latter needs a whole-corpus streaming bijection checked under one I02 proof transaction.

### Actual executed sourcefree regression receipt

Run command on the locally constructed file:

~~~
python3 -B -Werror::ResourceWarning -m unittest -q /mnt/data/c2_round2/test_verified_range.py
~~~

**Result:** 19 tests, 19 PASS; no skipped tests, approximately 0.4 seconds on the available Python runner (time varies). The exact local Git blob was recomputed with git hash-object and matched the committed test blob byte-for-byte. Tests cover: intact content ref inventory with damaged derived selector; entire-range deletion; missing interior/boundary; forged canonical alias; hostile extra leaf; changed typed state; native/canonical/component union and duplicate suppression; native_only and state filtering; correct ordering and repeated occurrences; global duplicate occurrence rejection; independently pinned release and self-rehash rejection; invented respondent and target-scope refusal; same-time permission-revoked stub; one valid empty range distinguished from unqualified routing and unknown scope; a new internally coherent but source-omitting tree rejected by a prior external expected root; and logarithmic witness siblings on the fixture.

Additional **1000-event / 3000-posting sourcefree engineering-only probe**:
- SQLite build 0.141 seconds, saved query 0.041 seconds in this runtime;
- complete selected occurrences 1000;
- SQLite file bytes 2,793,472;
- maximum Merkle proof siblings 12;
- process ru_maxrss 100,376 KiB (includes runtime and imports, not isolated C11 measurement).

This is **not** a 100,000-row test, 6 GiB process-tree proof, native I03/I05/Batch execution or original35 result. The probe was executed on the earlier 17-test model; later additions preserve its structure but the numeric timing/bytes were not rerun at the final SHA. No 6 GiB savings extrapolated.

### Executable command for a separate agent's clean checkout

~~~
git checkout agent/pyat-c2-counterconstruction-semantic-range-r2
git rev-parse HEAD
python3 -B -Werror::ResourceWarning -m unittest -v WORKER_RETURNS/PYAT_C2_COUNTERCONSTRUCTION_R2/tests/test_verified_range.py
git hash-object WORKER_RETURNS/PYAT_C2_COUNTERCONSTRUCTION_R2/tests/test_verified_range.py
~~~

The standalone script does not require pyarrow, Rawlsing data, source grants or other package imports. A competent reviewer must re-run it at the **immutable R2 HEAD** and independently inspect its source and assumptions before accepting even this model grade.

## 3. Corrected actual owner ABI and source-owner derivation

The inherited Agent A document's C11ReadStore declaration has been **edited on this R2 branch**: full_ref_keyspace_root alone is no longer enough. CertifiedReleaseHandle now includes semantic_selector_range_root, respondent_domain_root, routing_range_root, coordinate_range_root, weight_range_root and selector_codec_version. Its all-at-once inventory_refs() was replaced by bounded iter_refs_bounded(), and event selection now advertises native_only/include_component/states, an assert_complete_range receipt and the separate routing/coordinate/weight range proof. The original R1 immutable artifact remains unchanged at commit 4616a1f411550c26914faf31a21d4444382a9b99; the new R2 branch carries an explicit supersession note, not a stealth rewrite of history.

**Binding algorithm to authorize before publication (not yet implemented in native PYAT):**

1. The original complete I02-owner event stream is authoritative. Validate source snapshot SHA, source universe, respondent, exact native question, component, event group, occurrence ID and type/state; preserve the original stable ref.key order, not an inferred time/frequency sort. Complete external sort of exact event occurrence keys and reject any duplicate globally.
2. For *every event* emit one native semantic posting, one authorized canonical posting where the event carries authorized canonical question, and one component posting where applicable; keep exact ref, occurrence identity, typed state, semantic/topology authority and version. When native/canonical/component targets coincide, postings still have distinct selector-kind keys; a consumer union deduplicates the event **once**. No silent canonicalization from labels. Compare the full derived posting multiset against the separately generated candidate index **in both directions**: no omitted bindings, no invented ones. This is the obligation the original ref-only ABI lacked.
3. Externally merge/sort canonical postings. Reproduce a deterministic semantic selector-index root and complete family/member totals in the **same I02 accepted release transaction** as replay semantic root, exact ref closure, M01–M18, respondent domain and source/authority snapshot set. The independent original owner holds the expected roots, selector code/version and accepted hash before any saved read can use them. This does not grant P05 equivalence or current host permission.
4. Persist an authenticated complete sorted keyspace. A genuine SELECT result supplies source/release/replay/index version, universe/respondent/selector kind/ref, exact event/occurrence/state and an inclusion proof for every row plus authenticated preceding/following leaves. Verify adjacency, range boundary strictness and full set against the accepted external root. An **empty range** needs explicit neighboring exclusion proof and a separately certified respondent/target domain. A missing SQL/Parquet row, unsupported canonical mapping or unissued domain means UNKNOWN/REFUSE; no semantic observed-zero claims.
5. Independently verify routing, risk eligibility, coordinates/weights, exact native per-query authority, source retention and current use before deriving denominator or typed negative. Event absence is neither no respondent nor routing inapplicability. Sourcefree compiled semantic locator does not replace original I03 mathematics.
6. Execute native _select_respondent_events and I03 exact fact/replay, all I05 query roles, Batch and normal issued/joined resume through existing owners. Comparison requires changed input→changed exact full fact/receipt or refusal→restore parity. No model PASS can stand in for those calls.

**Why a new source-bodies copy is unnecessary:** persisted semantic posting rows store exact selector/occurrence/ref/state and Merkle proof material, not entire event raw/canonical response bodies. Native object reconstruction comes from the one source-authoritative canonical Parquet estate and must verify each selected exact event body/ref. The index is derived/regenerable, version-keyed, not a second C11 source of truth. On incompatible source/replay/currentness, discard/rebuild under qualified owner rather than rehash and bless the index.

**Cost boundary:** a certified semantic index is additional derived storage and has O(events×number_of_authorized_aliases) postings. Sorted ref range indexes, Merkle nodes and original exact fact risk/denominator vectors cost bytes and memory. The model proves only O(log posting count) *path depth* per inclusion witness, not O(log N) total query RAM: full native membership lists, result material and the final model tuple may be O(K), and production original I03 may loop O(all respondents). The 6 GiB accepted source-native engineering requirement remains an honest HOLD.

## 4. Remaining native first-reader and security debt

The following **are unchanged and unproved** by this R2 sourcefree work:
- actual PRE553 _ReleaseIndex uses a sealed C11LogicalRelease and private cache attestation; it needs a genuine owner-provided certified read/index adapter, not a Protocol accepted from an arbitrary caller;
- _select_respondent_events matches native/canonical/component and optional states; consumer groups then reconstruct routing/risk/weights, full denominator member refs, exact cells and provenance. Our miniature Event/Scope is NOT an ExactRef or a runtime AuthorityRegistry;
- complete I02 source↔semantic/full replay closure and independent P05 P01–P20/T01–T18 source equivalence;
- the physical Parquet/Zstd saved reader, crash/CAS recovery, immutable inode/page proof and 6 GiB full native sourcefree 100k build/read;
- authentic current issuer for joined COMPLETED/PARTIAL/ABSENT (source shows stale historical _resolver_for), independently pinned B5 checkpoint/event publisher and M1/M2 full closure, and actual learned/world first reader;
- scoped original35 source, structural/causal/actor and N11/Sorok authority. The W03/W04 user pause is still not released.

**Additional R2 attack surfaces:** SQLite's local post-build row locator, Merkle levels and Scope witness are untrusted in production; a real full-run builder must prove the index was derived from certified **actual** PRE553 canonical events (not just an independently coherent alternate set), must enforce authorization for canonical aliases, prove full family and domain count/absence across restart, protect a cursor from mutation between verifying boundary and returning it, and prevent emission of a partially verified cursor. Our internal generator yields rows before its final boundary check; only the **public model select()** buffers and withholds results until all proofs finish. Exposing the generator directly as a production streaming API would be UNSAFE without a proof-first phase or immutable pinned snapshot. Real concurrency, external issuer signature, exact native deterministic order and crash-safe publication are deliberately not claimed.

## 5. Rejected alternatives and eight-part adversarial handoff

**Rejected by demonstrated or source-grounded reason:** leaving the R1 ref-keyspace-only selector as proof of query completeness (PR #923 counterexample); whole selector_root recomputed over all postings on every saved read (unbounded per query); accepting unqualified caller-supplied known respondent/question domains (R2's self-discovered defect and corrective test); treating every index hit or empty hit as scientific fact (routing/authority and absent-domain contradiction); keeping a second object-body corpus merely to support alias lookup (unnecessary source duplication); changing I03 mathematics/Batch science or inventing B5 issuer to make a test pass (outside commission); silencing the challenge by insulting the reviewer.

1. **Exact artifact:** This R2 branch adds this correction and tests/test_verified_range.py; modifies only inherited Agent A S1 Markdown ABI; preserves both predecessor and independent adversary artifact. Obtain final immutable HEAD from branch and confirm three-file diff vs #923 before receiving.
2. **Governing contract:** #919 under #909, Oct28 one-hybrid selected physical estate, frozen original35/P05 and MCR-lite/full-MCR boundaries, W03/W04 paused; one bounded differential and independent receiving.
3. **Strongest achieved:** genuine sourcefree disk-backed indexed Merkle inclusion, adjacent range exclusion and alias/domain semantic matching with 19/19 locally executed tests, exact blob identity, model-only 1000-event performance observation; corrected original read-store interface in the inherited return.
4. **Genuine opponent advances:** explicit object-inventory≠semantic-range proof and unbounded inventory method; retained with no attempt to relitigate.
5. **Newly repaired defects:** R1 incomplete read-store signature, R2 unbounded Python occurrence set, R2 caller-claimed scope, redundant proof-path reread, index staging retention. Demonstrated test outcomes are sourcefree **not native**.
6. **Unresolved:** independently issued I02 semantic root and full source-derived multiset, real C11 disk adapter and native I03/I05/Batch, current issuer and native economics under cap, S05/B5 independent custody, original35 source/science.
7. **Likely hostile targets:** self-attested scope, unverifiable preissuance index derivation, empty-range boundary, alias union duplicates, state filtering, concurrent modification before serve, real native risk-set and replay identity, actual memory retained by facts.
8. **Proof boundaries:** no production code changes, no original-source or actor grants, no native runtime PYAT tests, no actual 100k/6 GiB qualification, no external signer, no protected merge, no independent acceptance. Honest status remains SOURCEFREE MODEL / C-2 OPEN.

**Disposition:** Carry forward the opponent's valid correction, make it executable at a stronger sourcefree data-structure level, and require a genuinely superior native I02/index/reader implementation before #919 can claim a complete vertical cut. One independent adversarial receiving of this immutable R2 HEAD is the appropriate next act—not another reconnaissance fleet.
