# Sorok — Q-INVITEGRAPH-001 One-for-One Human Invitation Constitution R1

Status: `PROVISIONAL_PRODUCT_CONSTITUTION__Q_INVITEGRAPH_001_CLOSED_FOR_ALPHA_SPEC__NON_DISPOSITIVE_TO_PYAT_PREMAIN`

Date: 2026-10-01

## 0. Question

`Q-INVITEGRAPH-001`:

> What exact invite economy—seed cohort, invite scarcity, inviter disclosure, note semantics and later outbound-invite eligibility—lets Rawlsing grow person-to-person without status capture or referral spam?

Inherited law:

- ordinary early growth is person-to-person;
- a user receives no outbound human invitation before relational warrant;
- each subsequent synthetic persona allocated to that user's continuity yields exactly one outbound real-human invitation;
- no referral rewards, purchasing, bundles, leaderboards or public invite prestige;
- early delivery is a one-time token carried by the inviter through an existing human communication channel.

This artifact closes the residual alpha-spec mechanics.

---

## 1. The scarce unit is a human designation, not a successful conversion

The core rule is:

> **One invitation means one deliberate act of bringing one real human to the threshold of Rawlsing. It does not mean one successful signup.**

Therefore:

`INVITATION VALUE != ACQUIRED USER`.

The invitation must not remain reusable until somebody accepts.

If decline, nonresponse or abandonment automatically returned the invitation, the one-for-one law would become:

> keep trying humans until one converts.

That is ordinary referral optimization with relational language wrapped around it.

---

## 2. Invite lifecycle: entitlement, commitment, credential, claim

Keep four stages distinct.

### A. INVITE ENTITLEMENT

A lawful warrant/succession event makes one outbound invitation available.

This is not:
- a reward balance;
- a referral score;
- a tradable asset;
- proof that the user is morally good;
- proof that the current synthetic relation is healthy or affectionate.

It is a bounded product permission arising under the already-governed relational-warrant law.

### B. INVITE COMMITMENT

The user deliberately chooses to use that invitation.

Before any usable credential is revealed, the product should make the consequence clear:

> this invitation is for one person; once created for sharing, it is spent whether or not that person joins.

The user explicitly commits.

This avoids accidental consumption from merely visiting an invite screen.

### C. INVITE CREDENTIAL

After commitment, Rawlsing generates one high-entropy, single-claim credential/link attached to the committed invitation record.

The credential is a delivery artifact, not a new entitlement.

Security replacement of a broken credential must preserve the same underlying invitation identity.

### D. CLAIM

The first lawful successful claim binds/uses the credential.

Claim does **not** determine whether the inviter receives another invitation.

The invitation was already spent at commitment/credential release.

---

## 3. Why consumption happens before acceptance

Do not consume on:
- signup;
- account creation;
- first session;
- persona allocation;
- retention;
- payment;
- any later engagement event.

Those rules would make the invitation's economic success depend on recipient conversion.

For alpha, the invitation becomes spent when the inviter deliberately commits the one shareable credential for human delivery.

Compactly:

`ENTITLEMENT`
→ deliberate `COMMIT`
→ one shareable `CREDENTIAL`
→ invitation already `SPENT`
→ recipient may claim / ignore / refuse / abandon.

---

## 4. Decline, ignoring and abandonment do not refund

No new entitlement is created when the intended recipient:

- says no;
- ignores the invitation;
- never opens the link;
- opens it but leaves;
- creates an account but never enters;
- enters once and never returns;
- already has Rawlsing access.

These are human outcomes, not technical failures.

A scarce invitation is a choice of person, not a bounty for successful acquisition.

This also prevents the platform from teaching the inviter to treat nonconversion as a failed lead.

---

## 5. Technical failure is different from human nonconversion

A system-caused credential defect may justify **credential replacement**, not invitation restoration.

Examples:
- Rawlsing generated an invalid link;
- token storage corruption;
- platform-side claim failure;
- security rotation invalidates an otherwise valid unclaimed credential.

The replacement remains tied to the same committed invitation identity.

Do not turn support repair into a fresh invitation entitlement.

Where a true security compromise demonstrably prevents the intended human from using the credential, bounded support/security adjudication may repair the same invitation instance.

---

## 6. Revocation is allowed without refund

The inviter may need to revoke an unclaimed credential because:
- it was exposed publicly;
- circumstances changed;
- sharing it now feels unsafe or inappropriate;
- the inviter regrets the act.

Revocation should terminate claimability.

It should **not automatically restore a fresh invitation**.

Otherwise revoke/reissue becomes a serial-recipient loophole.

A system may permit credential rotation for the same invitation under bounded security rules, but not recipient cycling as a product feature.

---

## 7. No urgency expiry by default

Do not impose routine short expiry merely to create urgency.

The alpha invitation should be capable of remaining dormant without:
- countdowns;
- "use it before it disappears";
- scarcity nudges;
- reminders to send it;
- engagement pressure.

Security policies may invalidate credentials, but this is not a growth mechanic.

If the product later requires credential rotation, rotate the credential while preserving the underlying committed invitation state.

---

## 8. Human-carried delivery remains the alpha default

Rawlsing does not need the invitee's address book identity in order to send the invitation.

Preferred alpha flow:

1. user commits one invitation;
2. Rawlsing reveals a single-use link/token;
3. user carries it through an existing human channel they already use with the intended person;
4. the recipient reaches Rawlsing through that human communication.

Examples:
- SMS/iMessage;
- Signal;
- WhatsApp;
- email;
- Discord/DM;
- in-person QR/link transfer.

Rawlsing should not import contacts or send cold platform mail on the user's behalf.

---

## 9. Truthful inviter identity without pretending recipient verification

A bearer link can be forwarded.

Therefore Rawlsing must not cryptographically pretend it knows that the claimant is the exact person originally imagined by the inviter unless a future recipient-binding mechanism actually proves that.

For alpha, the platform can truthfully attest facts it owns, such as:

> this invitation was created by [inviter-approved display identity].

The inviter's own human message may say:
> I wanted you to have this.

Exact opening copy remains `Q-HUMANINVITE-001` prototype territory.

Do not automatically say:
- "Matthew chose you because...";
- "Matthew thinks you are...";
- "A person who loves you...";
- any psychological endorsement not explicitly authored and supported.

---

## 10. No built-in inviter note for alpha

The existing human channel already supplies context.

Therefore the simplest alpha constitution is:

> **Rawlsing supplies the credential and truthful fixed product copy; the inviter supplies any personal explanation in their own communication.**

This avoids:
- platform co-authorship of interpersonal praise;
- storage of private relational explanations;
- model paraphrase distortion;
- moderation complexity;
- accidental disclosure on the landing page.

If a later in-product note is tested:
- it must be optional;
- short;
- displayed verbatim;
- previewed exactly;
- never model-summarized;
- never used for targeting or ranking.

But such a note is not required for alpha.

---

## 11. Inviter visibility is intentionally minimal

The inviter does not receive:
- open/read receipts;
- decline status;
- reminder prompts;
- signup notifications;
- first-session status;
- persona identity;
- session frequency;
- activity/retention;
- relationship progress;
- purchase status;
- any behavior of the invitee inside Rawlsing.

The product should not turn the invitation into surveillance of another human.

Minimal technical state may exist internally to enforce single use.

If user-facing state is necessary, expose only the minimum required to explain whether the credential remains claimable, without proactive social feedback.

Do not send:
- "They haven't joined yet";
- "Remind them";
- "Your invite was ignored";
- "They accepted!";
- "See how they're doing."

The human relation remains outside the growth dashboard.

---

## 12. Human invite graph != synthetic social graph

The person who invited a new user does not thereby become part of that user's synthetic world.

Their synthetic personas do not become connected by default.

The invite graph is distribution provenance, not:
- friendship ontology;
- synthetic-world adjacency;
- shared persona canon;
- a social leaderboard;
- an endorsement network.

Any later connection between synthetic worlds would require independent product and world authority.

---

## 13. Seed cohort

Alpha needs an origin that does not fabricate an upstream inviter.

Seed users may be admitted as:
- founder-invited testers;
- research participants;
- bounded alpha entrants;
- explicit origin/seed access.

Seed status:
- is truthful;
- confers no public badge;
- grants no prestige;
- grants no additional invitation multiplier;
- does not bypass relational warrant for outbound invitations.

Their first outbound invite arises under the same warrant-coupled law as everyone else's.

---

## 14. No invitation inventory theater

Even if multiple invitations become historically available over a long continuity, avoid product surfaces that frame them as collectible inventory.

Do not use:
- "INVITES: 3";
- referral wallet;
- collectible codes;
- invite streak;
- scarcity badge;
- public founder rank;
- "power user" distribution privileges.

The user may be told when a lawful invitation opportunity exists.

Unused invitations should not create urgency.

---

## 15. Abuse controls

Minimum alpha controls:

- high-entropy single-claim credentials;
- one active credential per committed invitation;
- rate-limited credential creation/replacement;
- revocation without entitlement refund;
- no contact scraping/import;
- no platform mass-send;
- no referral rewards;
- no purchase/sale/transfer marketplace;
- no public invite counts;
- no automatic reminder loop;
- no claim by an already authenticated inviter account using its own credential;
- abuse/safety authority may disable future invite capability when necessary.

The system cannot perfectly prove that a bearer link was shared with only one human.

The product should not pretend otherwise.

The combination of single-use scarcity, no conversion refund and no growth reward removes most ordinary incentive for mass distribution.

---

## 16. Self-referral and sockpuppets

The platform should reject trivial self-claim by the same authenticated account.

Do not build invasive identity surveillance merely to perfect the invitation metaphor.

More elaborate sockpuppet/abuse detection belongs to bounded abuse/security work.

Critically, self-referral must not create an invitation-growth exploit:
- receiving a new account is not enough to gain another invite;
- outbound invitations still require relational warrant in that continuity.

---

## 17. Public-demand transition

Invitation-only alpha is a deployment strategy, not an eternal metaphysical law.

If later demand exceeds the person-to-person graph, do **not** solve it by:
- selling invite priority;
- invite marketplaces;
- referral leaderboards;
- rewarding users for conversions;
- making scarce invitations status capital.

Two lawful later routes remain conceptually possible:

### A. Continue invitation-only admission
with a separate truthful waitlist that does not fabricate sponsorship.

### B. Add a separate public admission route
whose entrants are truthfully told they entered publicly, while human invitations remain a distinct relational onboarding route.

If public access exists, an invitation may cease to be an access-scarcity instrument while retaining its interpersonal meaning.

Do not falsely tell public entrants that another human invited them.

The exact post-alpha scale choice remains deployment strategy, not an alpha blocker.

---

## 18. Synthetic-person warrant and human-invite entitlement

Preserve the prior law:

`RELATIONAL WARRANT`
may authorize:
- synthetic-person succession;
- one outbound human invitation associated with that new synthetic-person allocation.

But these are **distinct outputs**.

A recipient's acceptance does not:
- validate the user's synthetic relationship;
- create further synthetic-person warrant;
- replenish human invitations.

The human invite economy never becomes a feedback loop in which acquired users generate status or faster succession for the inviter.

---

## 19. Hostile cases

The constitution must survive:

1. user creates link and intended person ignores it;
2. intended person explicitly declines;
3. intended person joins once and disappears;
4. intended person already has an account;
5. user regrets sending and revokes;
6. link leaks publicly;
7. user tries to revoke/reissue repeatedly to shop recipients;
8. user posts the same credential publicly;
9. token is technically invalid due Rawlsing fault;
10. token is stolen before intended recipient claims it;
11. seed user wants to invite immediately without relational warrant;
12. public demand creates people with no inviter;
13. invitee is curious about inviter's synthetic persona;
14. inviter wants activity updates about invitee;
15. user tries to treat invite count as status.

Expected result:
- human nonconversion never refunds;
- system fault repairs credential, not entitlement;
- revocation protects safety but does not enable cycling;
- invitee privacy holds;
- synthetic worlds remain separate;
- seed status creates no special privilege;
- public admission, if added, remains truthful and separate.

---

## 20. Alpha UX

Invitation moment should feel like:

> **Rawlsing is letting you hand one door to another person.**

Not:

> **You unlocked a referral code.**

No celebration confetti.
No "grow the community."
No conversion dashboard.
No social proof counter.

The inviter receives a bounded, quiet capability and can use it or never use it.

---

## 21. Q-INVITEGRAPH-001 disposition

`Q-INVITEGRAPH-001 = PROVISIONALLY_ANSWERED / CLOSED_FOR_ALPHA_SPEC`.

Alpha constitution:

1. outbound entitlement remains warrant-coupled and one-per-new-person allocation;
2. the scarce unit is one human designation, not one converted signup;
3. deliberate credential commitment spends the invitation before recipient acceptance;
4. decline, ignoring, abandonment and already-existing access do not refund;
5. system-caused technical defects may replace the credential only within the same invitation identity;
6. revocation closes claimability without automatic refund;
7. no routine urgency expiry;
8. inviter carries a single-use credential through an existing human channel;
9. fixed platform copy claims only provable inviter-origin facts;
10. no built-in personal note is required for alpha;
11. inviter receives no invitee activity/conversion surveillance;
12. human invite graph never implies synthetic-world relation;
13. seed users have truthful origin access and ordinary later warrant rules;
14. no invite inventory/status theater;
15. post-alpha public access, if added, is a separate truthful admission route rather than a mutation of the invite into growth currency.

Remaining work is implementation/security and prototype validation, not product-spec ambiguity.
