# CURRENT-SELECTION LAW

## 1. Central theorem

CURRENTNESS_IS_EXPLICIT

CURRENT != LATEST
CURRENT != NEWEST
CURRENT != HIGHEST_VERSION
CURRENT != MOST_RECENT_COMMIT
CURRENT != REPOSITORY_PRESENCE
CURRENT != CONSUMER_PERMISSION

The only positive currentness fact is an exact CURRENT_SELECT event and its exact CurrentSelectionReceipt.

The only explicit empty currentness fact is an exact NO_CURRENT event and its exact NoCurrentReceipt.

## 2. Selection jurisdiction

A current-selection claim is meaningless without an exact SelectionKey.

SelectionKey fields:

1. product_family_ref
2. selection_scope_ref
3. selection_purpose_ref
4. optional consumer_context_partition_ref

The key is content-addressed.

A CURRENT_SELECT binds only that exact key.

It cannot widen:
- semantic product scope;
- M2 release publication scope;
- downstream consumer permission;
- structural admission permission;
- source/comparability/composition authority.

## 3. Purpose

selection_purpose_ref is required because the same product family may lawfully have different current releases for different governed selection purposes.

Examples of purpose classes may include operational serving, audit replay, evaluation, or named downstream composition, but the exact allowed purpose vocabulary belongs to separately adopted authority.

M3 accepts the purpose ref as an exact governed partition.

M3 does not invent purpose semantics.

## 4. Consumer-context partition

consumer_context_partition_ref is optional.

It exists only to permit lawful coexistence where currentness is intentionally consumer-context specific.

It is not an authorization token.

Freeze:

CONSUMER_PARTITION_IN_SELECTION_KEY != CONSUMER_PERMISSION

A downstream consumer must separately prove permission to dereference/use the selected product.

## 5. Cardinality

For one exact SelectionKey:

- zero current releases is lawful only as explicit NO_CURRENT or UNKNOWN_BEFORE_SELECTION_HISTORY;
- one current release is lawful;
- two unresolved current releases are unlawful and produce CONFLICTING_CURRENT_SELECTION.

Across different SelectionKeys, multiple releases may simultaneously be current.

Thus there is no universal singleton CURRENT product for a product family unless a separate authority explicitly defines one global SelectionKey.

## 6. CURRENT_SELECT preconditions

Before CURRENT_SELECT:

- target M2 release ref resolves exactly;
- target release is lifecycle-eligible at the event scope;
- selection key resolves exactly;
- exact selection authority/attestation refs resolve;
- no forbidden selector token or heuristic is used;
- any predecessor current receipt is cited exactly;
- any required invalidation consequence is derivable/recorded.

If the release is withdrawn at the same scope, CURRENT_SELECT fails closed unless a later exact event explicitly restores eligibility.

REOPENS alone does not restore positive current eligibility.

## 7. NO_CURRENT

NO_CURRENT is first-class, not absence.

Use it when:
- no release is currently authorized for a SelectionKey;
- current release is withdrawn with no lawful replacement;
- correction/supersession requires a gap before replacement;
- a conflict is resolved by clearing currentness.

NO_CURRENT does not:
- delete releases;
- negate semantic product truth;
- imply no historical release existed;
- imply the family is retired;
- block historical replay.

## 8. Supersession and currentness

SUPERSEDES does not auto-select the successor.

A successor release can exist and supersede a predecessor historically while the predecessor remains current for a separate key, or while the key is NO_CURRENT.

Changing currentness requires a separate CURRENT_SELECT.

This enforces:

SUCCESSION_RELATION != CURRENT_SELECTION

## 9. Withdrawal and currentness

Withdrawal marks a release ineligible at exact scope.

If that release is current for affected SelectionKeys, M3 must require explicit selection-state follow-up:
- CURRENT_SELECT replacement; or
- NO_CURRENT.

No replacement is inferred.

Historical replay remains intact.

## 10. Recertification and currentness

RECERTIFIES never implies current selection.

A recertified historical release remains historical unless selected explicitly.

A current release that is recertified remains current only because its existing current receipt remains valid under the exact rules; recertification itself does not create another selection receipt.

If recertification changes the M2 release preimage, the result is a new M2 release and requires explicit CURRENT_SELECT to become current.

## 11. Correction and currentness

CORRECTS never auto-promotes the corrected release.

A semantic correction may require:
- new semantic product;
- new M2 release;
- invalidation;
- NO_CURRENT at affected keys until an explicit successor selection.

A release-only correction may preserve semantic product identity but still creates a new M2 release if M2 preimage changes.

The prior release remains historically resolvable.

## 12. Scope change

Selection-scope change is governed by distinct SelectionKeys.

A release can be current for scope A and NO_CURRENT for scope B.

Changing semantic-product scope is upstream and normally requires a new semantic product and release.

M3 must not simulate semantic scope change by merely changing the SelectionKey.

## 13. Historical replay / current-as-of

An exact current-as-of query uses:
- exact SelectionKey; plus
- exact lifecycle event ref or exact lifecycle checkpoint ref.

The resolver deterministically replays the append-only event chain to that exact point.

No Git commit date, filesystem mtime, release timestamp, semantic version, or newest object participates.

If governed effective-time evidence exists, a time-based view may be built only over that explicit evidence.

Absent such evidence, wall-clock current-as-of is UNKNOWN rather than inferred.

## 14. Rollback

Rollback is represented as explicit CURRENT_SELECT of an exact prior lawful M2 release under exact rollback/selection authority.

The prior release must already exist exactly and remain lifecycle-eligible.

Rollback:
- does not delete the newer release;
- does not rewrite history;
- does not imply the newer release was semantically false;
- may trigger selective invalidation for current-dependent consumers.

## 15. Resolver contract

Minimal read API:

resolve_current_exact(selection_key_ref, current_receipt_ref) -> exact release OR NO_CURRENT

resolve_current_as_of(selection_key_ref, as_of_event_or_checkpoint_ref) -> typed historical result

list_historical_selections(selection_key_ref) -> immutable exact receipts in governed event order

No API named latest(), default(), nearest(), newest(), best_version(), fallback(), or resolve_without_receipt() is lawful.

## 16. Fail-closed states

Required nonpositive states:

NO_CURRENT
UNKNOWN_BEFORE_SELECTION_HISTORY
CONFLICTING_CURRENT_SELECTION
MISSING_SELECTION_AUTHORITY
MISSING_RELEASE
WITHDRAWN_AT_SCOPE
SELECTION_SCOPE_MISMATCH
SELECTION_PURPOSE_MISMATCH
SELECTION_RECEIPT_MISMATCH
HISTORICAL_REPLAY_MISMATCH

None may be coerced into a current release.
