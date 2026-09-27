# HOSTILE LIFECYCLE TEST PLAN

Purpose: prove that implementation cannot launder chronology, authority, release identity, semantic meaning, or consumer permission into currentness.

## H01 — latest wins attack

Fixture:
two M2 releases, newer chronological release not explicitly selected.

Expected:
older selected release remains current.

Forbidden:
automatic newest selection.

## H02 — highest version wins attack

Fixture:
release v9 exists; v3 is explicitly current.

Expected:
v3 remains current.

## H03 — repository presence attack

Fixture:
valid M2 release exists in repository with no CURRENT_SELECT.

Expected:
NO_CURRENT or UNKNOWN_BEFORE_SELECTION_HISTORY.

## H04 — implicit successor promotion

Fixture:
SUPERSEDES predecessor->successor, no CURRENT_SELECT.

Expected:
current pointer unchanged or NO_CURRENT according to explicit prior state.

## H05 — recertification auto-promotion

Fixture:
historical release RECERTIFIES while another release is current.

Expected:
historical release does not become current.

## H06 — correction auto-promotion

Fixture:
semantic correction creates new semantic product + M2 release.

Expected:
new release is not current until explicit CURRENT_SELECT.

## H07 — withdrawal deletes history

Fixture:
withdraw a formerly current release.

Expected:
historical exact release/event/selection remain replayable.
Affected current key must receive explicit NO_CURRENT or replacement selection.

## H08 — reopen means accept

Fixture:
REOPENS a blocked/withdrawn lifecycle subject.

Expected:
eligibility/court status only; no positive semantic truth/currentness.

## H09 — no-current fallback attack

Fixture:
explicit NO_CURRENT followed by a newer eligible release with no selection.

Expected:
NO_CURRENT persists.

## H10 — selection scope bleed

Fixture:
same family, scope A selects R1, scope B selects R2.

Expected:
each key resolves its exact release; no family-global overwrite.

## H11 — purpose bleed

Fixture:
same family/scope with two selection purposes.

Expected:
different current releases may coexist if exact distinct SelectionKeys.

## H12 — consumer partition becomes permission

Fixture:
consumer-context partition names Consumer X, but consumer permission authority absent.

Expected:
M3 can resolve currentness namespace but downstream use remains denied/fail-closed.

## H13 — semantic scope disguised as selection scope

Fixture:
attempt to change the semantic claim population by creating a new SelectionKey only.

Expected:
reject; semantic-scope change requires upstream new semantic product/release where constitutive.

## H14 — same-members recertification inference

Fixture:
two releases contain identical members but no recertification authority.

Expected:
no RECERTIFIES inference.

## H15 — new ref means correction inference

Fixture:
new release ref differs for publication metadata only.

Expected:
dependency graph does not infer semantic correction.
Exact event authority must classify RELEASE_PREIMAGE_CORRECTION or other lawful class.

## H16 — completeness supersession rewrites local truth

Fixture:
expanded ontology invalidates old completeness claim but local edge object is unchanged.

Expected:
completeness/absence dependents invalidate; local truth remains historical/valid if its determinants are unchanged.

## H17 — ontology expansion invalidates all products

Fixture:
family expansion with many unrelated product branches.

Expected:
only determinant-reachable completeness/family-bound dependents invalidate.

## H18 — dependency engine infers event type

Fixture:
changed determinant graph is supplied without lifecycle classification.

Expected:
engine refuses to classify CORRECTS/SUPERSEDES/RECERTIFIES.

## H19 — release-only correction forces new semantic product

Fixture:
same semantic product; replay/explanation binding corrected, therefore new M2 release.

Expected:
semantic product identity preserved; release identity changes; M3 records release correction.

## H20 — semantic correction keeps same product ref

Fixture:
event claims semantic correction while predecessor/successor releases cite same semantic-product ref.

Expected:
reject unless correction is explicitly lifecycle-record-only/release-only. Semantic correction requires new semantic product identity.

## H21 — current selection without exact receipt

Fixture:
caller supplies SelectionKey only.

Expected:
resolve_current_exact fails; no hidden pointer/default accepted.

## H22 — wrong current receipt

Fixture:
receipt belongs to another key or older selection.

Expected:
fail exact.

## H23 — historical replay reinterpreted by successor

Fixture:
select R1, later select R2, query current-as-of R1-selection event.

Expected:
R1.

## H24 — commit-time as-of attack

Fixture:
Git commit order disagrees with governed lifecycle event order.

Expected:
lifecycle event/checkpoint controls; Git time ignored.

## H25 — concurrent current conflict

Fixture:
two incomparable CURRENT_SELECT events for same SelectionKey.

Expected:
CONFLICTING_CURRENT_SELECTION until explicit reconciliation.

## H26 — rollback by old-looking release

Fixture:
caller requests rollback using a historical release ref that was never lawfully selected/eligible for that key.

Expected:
reject unless exact prior lawful selection/rollback authority is satisfied.

## H27 — selective invalidation

Fixture:
changed determinant D reaches products A and B transitively; C is same family but no dependency edge.

Expected:
A/B affected, C unaffected.

## H28 — rebuild fabrication

Fixture:
A invalidated, no producer rebuild exists.

Expected:
REBUILD_REQUIRED; no synthetic successor ref.

## H29 — current pointer change invalidates semantic truth

Fixture:
CURRENT_SELECT R2 replaces R1; semantic products remain unchanged.

Expected:
only current-dependent consumers invalidate. Historical semantic product descendants not automatically invalidated.

## H30 — AuthoritySnapshot alias attack

Fixture:
implementation passes AuthoritySnapshot ref where M2 release ref required.

Expected:
typed rejection.

## H31 — AuthorityReleaseReceipt alias attack

Fixture:
A03 authority release receipt passed as M3 current receipt.

Expected:
typed rejection.

## H32 — APPROVED authority means accepted product

Fixture:
semantic authority revision is APPROVED but learned product lacks M1/M2 state.

Expected:
M3 refuses learned-product lifecycle/current selection.

## H33 — physical carrier swap

Fixture:
M2 logical release unchanged while physical cache/carrier changes.

Expected:
no lifecycle/currentness change.

## H34 — virtual release rebuild

Fixture:
release payload is recomputable; physical payload absent; immutable M2 release preimage/replay closure intact.

Expected:
M3 historical/current resolution remains valid at logical release identity.

## H35 — withdrawal plus replacement atomicity

Fixture:
withdraw R1, select R2 for same key in one governed transition package.

Expected:
no observable half-state; final exact receipt selects R2 and history records both events according to transaction law.

## H36 — NO_CURRENT is semantic negation attack

Fixture:
NO_CURRENT for a selection key while historical semantic product remains positive.

Expected:
historical product remains unchanged.

## H37 — current means consumer authorized attack

Fixture:
R1 is current, consumer permission explicitly absent.

Expected:
M3 resolves R1; downstream authorization fails separately.

## H38 — stale OBL034 serialization attack

Fixture:
reader consumes central TSV CLOSED row but ignores HQD-117 correction and M3 authority chain.

Expected:
current project interpretation follows later HQD-117/M3 adoption chain; historical B5 law preserved without treating stale provider identity as current.

## H39 — economics leakage

Fixture:
lifecycle resolver is asked to choose architecture based on 34-row economics determinants.

Expected:
reject as outside M3.

## H40 — restart/replay identity

Fixture:
complex history with select, recertify, correction, no-current, reselect, invalidation, rebuild link.

Expected:
checkpoint restore reproduces identical event refs, selection refs, determinant graph and checkpoint hash.

## Pass condition

All attacks fail closed without:
- implicit currentness;
- semantic-product mutation;
- history deletion;
- consumer-permission widening;
- family-wide invalidation by heuristic;
- Authority42 type aliasing;
- architecture/economics overreach.
