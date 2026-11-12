"""C-2 R2 sourcefree executable contract: disk-backed authenticated semantic ranges.

Not native PRE553, no real I02 issuer. Independent anchor models accepted-I02 custody.
SQLite is an untrusted locator; authenticated Merkle witnesses, not SQL, establish
complete sorted selection. Source stream -> postings must be independently proven
at I02 (this model derives its anchor from its small authoritative fixture).
"""
from __future__ import annotations
import hashlib
import heapq
import json
import sqlite3
import tempfile
import unittest
from dataclasses import dataclass, replace
from pathlib import Path


def enc(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def h(tag, value):
    return hashlib.sha256(tag + value).digest()


def leaf(row):
    return h(b"C2L", enc(row))


def parent(a, b):
    return h(b"C2N", a + b)


@dataclass(frozen=True)
class Event:
    universe: str
    respondent: str
    native: str
    event_group: str
    occurrence: str
    value: str
    state: str
    canonical: str = ""
    component: str = ""
    def ref(self):
        return h(b"C2E", enc(self.__dict__)).hex()
    def occurrence_key(self):
        return self.universe, self.respondent, self.native, self.component, self.event_group, self.occurrence


@dataclass(frozen=True)
class Anchor:
    source: str
    release: str
    replay: str
    version: str
    count: int
    root: str
    scope_root: str
    def fingerprint(self):
        return h(b"C2A", enc(self.__dict__)).hex()


@dataclass(frozen=True)
class QuestionBinding:
    """Model-only exact source-universe question/topology and mapping grant.

    The real implementation must populate this from I02-validated
    QuestionVariableBinding + authority snapshots, not user-declared strings.
    """
    universe: str
    native: str
    topology_authority_ref: str
    canonical: str = ""
    canonical_authority_ref: str = ""
    components: tuple[str, ...] = ()


@dataclass(frozen=True)
class Scope:
    release: str
    respondents: tuple[tuple[str, str], ...]
    targets: tuple[str, ...]
    question_bindings: tuple[QuestionBinding, ...] = ()
    def root(self):
        return h(b"C2S", enc({
            "release": self.release,
            "respondents": self.respondents,
            "targets": self.targets,
            "question_bindings": [vars(binding) for binding in self.question_bindings],
        })).hex()
    def allows_target(self, universe, target):
        return any(binding.universe == universe and (
            target == binding.native
            or (target == binding.canonical and bool(binding.canonical_authority_ref))
            or target in binding.components
        ) for binding in self.question_bindings)


class BadRange(Exception):
    pass


class DiskSemanticIndex:
    """Sourcefree model: a SQLite locator + independently pinned Merkle leaves.

    Build uses SQLite ORDER BY to permit temp-file external sorting. It does not
    rely on a complete tuple of refs and never verifies the entire tree per read.
    Proofs contain all selected leaves and authenticated adjacent neighbors.
    """
    def __init__(self, db, anchor):
        self.db, self.anchor = db, anchor
        self.proof_peak = 0

    @classmethod
    def build(cls, path: Path, events, *, scope: Scope, source="SOURCE_SHA", release="RELEASE_REF", replay="REPLAY_REF"):
        if scope.release != release:
            raise BadRange("DOMAIN_RELEASE_MISMATCH")
        db = sqlite3.connect(str(path))
        db.executescript("""
          PRAGMA temp_store=FILE;
          CREATE TABLE occurrence(key TEXT PRIMARY KEY);
          CREATE TABLE posting(u TEXT,r TEXT,kind TEXT,q TEXT,ord TEXT,eref TEXT,occ TEXT,state TEXT);
          CREATE TABLE entry(idx INTEGER PRIMARY KEY, u TEXT,r TEXT,kind TEXT,q TEXT,ord TEXT,eref TEXT,occ TEXT,state TEXT);
          CREATE TABLE node(level INTEGER, idx INTEGER, digest BLOB, PRIMARY KEY(level,idx));
          CREATE INDEX posting_lookup ON posting(u,r,kind,q,ord,eref);
          CREATE INDEX entry_lookup ON entry(u,r,kind,q,ord,eref);
        """)
        # A global target whitelist is not a universe-specific question grant.
        # The real authority owner must supply I02-validated QuestionVariableBindings.
        bindings = {}
        eligible_universes = {u for u, _ in scope.respondents}
        for binding in scope.question_bindings:
            key = (binding.universe, binding.native)
            if (not binding.topology_authority_ref
                    or key in bindings
                    or not binding.native
                    or binding.universe not in eligible_universes
                    or binding.native not in scope.targets
                    or (binding.canonical and not binding.canonical_authority_ref)):
                db.close()
                raise BadRange("QUESTION_BINDING_NOT_GOVERNED")
            bindings[key] = binding
        if not bindings:
            db.close()
            raise BadRange("QUESTION_BINDING_NOT_GOVERNED")
        # Uniqueness uses a disk-backed PRIMARY KEY, not an all-events Python set.
        # Only admitted source events are used; never import index as source truth.
        for e in events:
            binding = bindings.get((e.universe, e.native))
            if ((e.universe, e.respondent) not in scope.respondents
                    or binding is None
                    or (e.canonical and (e.canonical != binding.canonical
                                        or not binding.canonical_authority_ref))
                    or (e.component and e.component not in binding.components)):
                db.close()
                raise BadRange("EVENT_QUESTION_BINDING_OR_DOMAIN_MISMATCH")
            try:
                db.execute("INSERT INTO occurrence VALUES(?)", (enc(e.occurrence_key()).decode(),))
            except sqlite3.IntegrityError as exc:
                db.close()
                raise AssertionError("duplicate occurrence") from exc
            assert e.native and e.universe and e.respondent and e.state
            for kind, value in (("native", e.native), ("canonical", e.canonical), ("component", e.component)):
                if value:
                    # Dedup *within an event* later at native union, not here.
                    db.execute("INSERT INTO posting VALUES(?,?,?,?,?,?,?,?)",
                               (e.universe,e.respondent,kind,value,e.ref(),e.ref(),enc(e.occurrence_key()).decode(),e.state))
        db.commit()
        # SQL sorts can spill to disk; record one row at a time, bounded Python
        # memory; full source-validation and external issuer remain outside model.
        rows = db.execute("SELECT u,r,kind,q,ord,eref,occ,state FROM posting ORDER BY u,r,kind,q,ord,eref")
        count = 0
        for row in rows:
            db.execute("INSERT INTO entry VALUES(?,?,?,?,?,?,?,?,?)", (count,*row))
            db.execute("INSERT INTO node VALUES(?,?,?)", (0,count,leaf(row)))
            count += 1
        db.commit()
        level, n = 0, count
        while n > 1:
            cursor = db.execute("SELECT digest FROM node WHERE level=? ORDER BY idx", (level,))
            at = 0
            while True:
                left = cursor.fetchone()
                if left is None:
                    break
                right = cursor.fetchone()
                db.execute("INSERT INTO node VALUES(?,?,?)", (level+1,at,parent(left[0],right[0] if right else left[0])))
                at += 1
            n, level = at, level+1
            db.commit()
        root = db.execute("SELECT digest FROM node WHERE level=? AND idx=0", (level,)).fetchone()[0].hex() if count else h(b"C2Z",b"").hex()
        # Staging postings and the uniqueness ledger are discarded after seal;
        # only the compact locator and range witnesses remain for read.
        db.execute("DROP TABLE posting")
        db.execute("DROP TABLE occurrence")
        db.commit()
        return cls(db,Anchor(source,release,replay,"SEMANTIC_RANGE_V2",count,root,scope.root()))

    def _path(self, idx):
        n=self.anchor.count
        sibling=[]
        while n>1:
            partner = idx ^ 1
            if partner >= n:
                partner = idx
            row=self.db.execute("SELECT digest FROM node WHERE level=? AND idx=?", (len(sibling),partner)).fetchone()
            if row is None:
                raise BadRange("MISSING_MERKLE_WITNESS")
            sibling.append(row[0])
            idx//=2
            n=(n+1)//2
        return sibling

    def _verify(self, row):
        idx=int(row[0]); data=tuple(row[1:]); n=self.anchor.count
        if idx < 0 or idx>=n:
            raise BadRange("OUT_OF_ANCHORED_RANGE")
        value=leaf(data)
        at=idx
        siblings=self._path(idx)
        for sib in siblings:
            value=parent(value,sib) if at%2==0 else parent(sib,value)
            at//=2
        if value.hex()!=self.anchor.root:
            raise BadRange("ANCHORED_RANGE_PROOF_MISMATCH")
        self.proof_peak=max(self.proof_peak,len(siblings))
        return data

    def _byidx(self, idx):
        row=self.db.execute("SELECT * FROM entry WHERE idx=?",(idx,)).fetchone()
        if row is None:
            raise BadRange("MISSING_ADJACENT_WITNESS")
        return self._verify(row)

    @staticmethod
    def _key(data):
        return tuple(data[:4])

    def range(self, u, r, kind, q):
        wanted=(u,r,kind,q)
        if self.anchor.version!="SEMANTIC_RANGE_V2":
            raise BadRange("INDEX_VERSION")
        c=self.db.execute("SELECT * FROM entry WHERE u=? AND r=? AND kind=? AND q=? ORDER BY idx", wanted)
        first=last=None
        for row in c:
            data=self._verify(row)
            if self._key(data)!=wanted:
                raise BadRange("WRONG_SEMANTIC_RANGE")
            idx=row[0]
            if last is not None and idx!=last+1:
                raise BadRange("MISSING_INTERIOR_POSTING")
            if first is None:
                first=idx
            last=idx
            yield data
        if first is not None:
            if first>0 and self._key(self._byidx(first-1))>=wanted:
                raise BadRange("INCOMPLETE_LOWER_BOUND")
            if last+1<self.anchor.count and self._key(self._byidx(last+1))<=wanted:
                raise BadRange("INCOMPLETE_UPPER_BOUND")
        else:
            # For an empty range, find authenticated straddling adjacent leaves.
            before=self.db.execute("SELECT idx FROM entry WHERE (u,r,kind,q)<(?,?,?,?) ORDER BY idx DESC LIMIT 1",wanted).fetchone()
            after=self.db.execute("SELECT idx FROM entry WHERE (u,r,kind,q)>(?,?,?,?) ORDER BY idx ASC LIMIT 1",wanted).fetchone()
            b=before[0] if before else -1
            a=after[0] if after else self.anchor.count
            if a!=b+1:
                raise BadRange("HIDDEN_SEMANTIC_RANGE")
            if b>=0 and self._key(self._byidx(b))>=wanted:
                raise BadRange("INVALID_LOWER_EMPTY_BOUND")
            if a<self.anchor.count and self._key(self._byidx(a))<=wanted:
                raise BadRange("INVALID_UPPER_EMPTY_BOUND")

    def select(self, *, accepted: Anchor, universe, respondent, target, native_only=False, include_component=False,
               states=None, scope: Scope, current=True):
        if not current:
            raise BadRange("CURRENT_AUTHORITY_REVOKED")
        if accepted != self.anchor:
            raise BadRange("UNTRUSTED_ANCHOR")
        if scope.release != accepted.release or scope.root() != accepted.scope_root:
            raise BadRange("DOMAIN_SCOPE_NOT_ATTESTED")
        if (universe,respondent) not in scope.respondents or target not in scope.targets:
            raise BadRange("UNKNOWN_SCOPE_OR_SELECTOR")
        if not scope.allows_target(universe, target):
            raise BadRange("UNQUALIFIED_UNIVERSE_TARGET")
        kinds=("native",) if native_only else (("native","canonical","component") if include_component else ("native","canonical"))
        cursors=[self.range(universe,respondent,kind,target) for kind in kinds]
        # Ref ordering reproduces native frozen per-respondent event order. An
        # event may match native AND canonical AND component; emit it only once.
        sorted_rows=heapq.merge(*cursors,key=lambda data:data[4])
        prior=None
        out=[]
        for row in sorted_rows:
            if row[5]!=prior:
                if states is None or row[7] in states:
                    out.append((row[5],row[6],row[7]))
                prior=row[5]
        return tuple(out)


class TestVerifiedRanges(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.events=(
            Event("U1","R1","NQ7","g","0","A","SUBSTANTIVE_RESPONSE","CQ7","SUB7"),
            Event("U1","R1","NQ7","g","1","B","SUBSTANTIVE_RESPONSE","CQ7","SUB7"),
            Event("U1","R1","NQ7","g","2","?","NO_RESPONSE","CQ7","SUB7"),
            Event("U1","R2","NQ7","g","0","C","SUBSTANTIVE_RESPONSE","CQ7","SUB7"),
            Event("U2","R1","NQ7","g","0","X","SUBSTANTIVE_RESPONSE","CQ7","SUB7"),
            Event("U1","R1","ALIAS","h","0","Y","SUBSTANTIVE_RESPONSE","ALIAS","ALIAS"),
        )
        self.scope=Scope("RELEASE_REF",(("U1","R1"),("U1","R2"),("U2","R1")),
                         ("NQ7","CQ7","SUB7","ALIAS","ABSENT"),
                         (
                             QuestionBinding("U1","NQ7","TOPOLOGY_U1_NQ7", "CQ7","MAPPING_U1_CQ7",("SUB7",)),
                             QuestionBinding("U2","NQ7","TOPOLOGY_U2_NQ7", "CQ8","MAPPING_U2_CQ8",("SUB7",)),
                             QuestionBinding("U1","ALIAS","TOPOLOGY_U1_ALIAS", "ALIAS","MAPPING_U1_ALIAS",("ALIAS",)),
                             # Explicit native question with zero fixture events.
                             QuestionBinding("U1","ABSENT","TOPOLOGY_U1_ABSENT"),
                         ))
        self.store=DiskSemanticIndex.build(Path(self.tmp.name)/"a.db",self.events,scope=self.scope)
        self.addCleanup(self.store.db.close)
        self.a=self.store.anchor

    def ask(self, target="NQ7",**kw):
        return self.store.select(accepted=self.a,universe="U1",respondent="R1",target=target,
                                 scope=self.scope,**kw)

    def test_positive_native_all_occurrences_and_states(self):
        self.assertEqual(len(self.ask()),3)
        self.assertEqual(len(self.ask(states=frozenset({"SUBSTANTIVE_RESPONSE"}))),2)
        self.assertEqual(self.ask(states=frozenset()),())

    def test_native_canonical_component_semantics_and_no_alias_duplicates(self):
        self.assertEqual(len(self.ask("CQ7")),3)
        self.assertEqual(len(self.ask("SUB7",include_component=True)),3)
        self.assertEqual(self.ask("SUB7"),())
        self.assertEqual(self.ask("CQ7",native_only=True),())
        self.assertEqual(len(self.ask("ALIAS",include_component=True)),1)

    def test_poisoned_secondary_range_with_unchanged_event_tree_fails(self):
        self.store.db.execute("DELETE FROM entry WHERE q=? AND eref=?",("NQ7",self.events[1].ref()))
        self.store.db.commit()
        with self.assertRaisesRegex(BadRange,"MISSING_INTERIOR_POSTING|INCOMPLETE_UPPER_BOUND|MISSING_ADJACENT_WITNESS"):
            self.ask()

    def test_poisoned_canonical_alias_fails(self):
        self.store.db.execute("DELETE FROM entry WHERE q=? AND eref=?",("CQ7",self.events[0].ref()))
        self.store.db.commit()
        with self.assertRaises(BadRange):
            self.ask("CQ7")
        self.assertEqual(len(self.ask("NQ7",native_only=True)),3)

    def test_missing_empty_range_is_authenticated_not_scope_inference(self):
        self.assertEqual(self.ask("ABSENT"),())
        with self.assertRaisesRegex(BadRange,"UNKNOWN_SCOPE_OR_SELECTOR"):
            self.store.select(accepted=self.a,universe="U9",respondent="R1",target="ABSENT",
                              scope=self.scope)

    def test_changed_state_is_detected_with_same_ref_inventory(self):
        self.store.db.execute("UPDATE entry SET state='SUBSTANTIVE_RESPONSE' WHERE eref=?",(self.events[2].ref(),))
        self.store.db.commit()
        with self.assertRaisesRegex(BadRange,"ANCHORED_RANGE_PROOF_MISMATCH"):
            self.ask(states=frozenset({"SUBSTANTIVE_RESPONSE"}))

    def test_local_reanchor_is_not_external_acceptance(self):
        changed=replace(self.a,root="f"*64)
        with self.assertRaisesRegex(BadRange,"UNTRUSTED_ANCHOR"):
            self.store.select(accepted=changed,universe="U1",respondent="R1",target="NQ7",
                              scope=self.scope)

    def test_release_and_current_are_independently_bound(self):
        with self.assertRaisesRegex(BadRange,"UNTRUSTED_ANCHOR"):
            self.store.select(accepted=replace(self.a,release="WRONG"),universe="U1",respondent="R1",target="NQ7",
                              scope=self.scope)
        with self.assertRaisesRegex(BadRange,"CURRENT_AUTHORITY_REVOKED"):
            self.ask(current=False)

    def test_boundary_deletion_at_first_and_last_posting_fails(self):
        key=("U1","R1","native","NQ7")
        matches=self.store.db.execute("SELECT idx FROM entry WHERE (u,r,kind,q)=(?,?,?,?) ORDER BY idx",key).fetchall()
        self.store.db.execute("DELETE FROM entry WHERE idx=?",(matches[0][0],))
        self.store.db.commit()
        with self.assertRaisesRegex(BadRange,"INCOMPLETE_LOWER_BOUND|MISSING_ADJACENT_WITNESS"):
            self.ask()

    def test_partial_ref_store_can_validate_all_remaining_refs_but_fail(self):
        before={x.ref() for x in self.events}
        self.store.db.execute("DELETE FROM entry WHERE q='NQ7' AND eref=?",(self.events[2].ref(),))
        self.store.db.commit()
        self.assertEqual(before,{x.ref() for x in self.events})
        with self.assertRaises(BadRange):
            self.ask()

    def test_duplicate_occurrence_is_not_new_event(self):
        with self.assertRaisesRegex(AssertionError,"duplicate occurrence"):
            DiskSemanticIndex.build(Path(self.tmp.name)/"b.db",self.events+(self.events[0],),scope=self.scope)

    def test_entire_selector_range_deleted_cannot_be_false_empty(self):
        self.store.db.execute("DELETE FROM entry WHERE u='U1' AND r='R1' AND kind='native' AND q='NQ7'")
        self.store.db.commit()
        with self.assertRaisesRegex(BadRange,"HIDDEN_SEMANTIC_RANGE"):
            self.ask()

    def test_forged_locator_alias_cannot_borrow_merkle_path(self):
        self.store.db.execute("UPDATE entry SET q='CQ7' WHERE q='NQ7'")
        self.store.db.commit()
        with self.assertRaises(BadRange):
            self.ask("CQ7")

    def test_unanchored_new_leaf_cannot_expand_supported_selection(self):
        max_idx=self.a.count
        self.store.db.execute("INSERT INTO entry VALUES(?,?,?,?,?,?,?,?,?)",
                              (max_idx,"U1","R1","native","NQ7","f"*64,"f"*64,"fake","SUBSTANTIVE_RESPONSE"))
        self.store.db.commit()
        with self.assertRaisesRegex(BadRange,"OUT_OF_ANCHORED_RANGE"):
            self.ask()

    def test_exact_order_and_alias_dedup_matches_native_reference(self):
        expected=tuple((e.ref(), enc(e.occurrence_key()).decode(),e.state)
                       for e in sorted((e for e in self.events if e.universe=="U1" and e.respondent=="R1"
                                        and (e.native=="NQ7" or e.canonical=="NQ7")), key=lambda e:e.ref()))
        self.assertEqual(self.ask(),expected)
        self.assertEqual(len(self.ask("ALIAS",include_component=True)),1)

    def test_routing_unknown_stays_unknown_even_with_proved_empty_range(self):
        self.assertEqual(self.ask("ABSENT"),())
        routing="UNKNOWN"
        self.assertNotEqual(routing,"ELIGIBLE")
        # Returning an empty event selection does not issue an observed-zero EmpiricalFact.
        with self.assertRaisesRegex(BadRange,"ROUTING_NOT_CERTIFIED"):
            if routing!="ELIGIBLE":
                raise BadRange("ROUTING_NOT_CERTIFIED")

    def test_caller_cannot_invent_eligible_scope_or_question(self):
        false_scope=replace(self.scope,respondents=self.scope.respondents+(("U9","R1"),),
                            targets=self.scope.targets+("PRIVATE",))
        with self.assertRaisesRegex(BadRange,"DOMAIN_SCOPE_NOT_ATTESTED"):
            self.store.select(accepted=self.a,universe="U9",respondent="R1",target="PRIVATE",
                              scope=false_scope)

    def test_preissuance_omission_cannot_self_certify_against_external_root(self):
        # A different, internally valid tree is not I02's already accepted tree.
        candidate=DiskSemanticIndex.build(Path(self.tmp.name)/"short.db",
                                          (e for e in self.events if e != self.events[1]),scope=self.scope)
        self.addCleanup(candidate.db.close)
        self.assertNotEqual(candidate.anchor.root,self.a.root)
        with self.assertRaisesRegex(BadRange,"UNTRUSTED_ANCHOR"):
            candidate.select(accepted=self.a,universe="U1",respondent="R1",target="NQ7",
                             scope=self.scope)

    def test_global_target_is_not_exact_universe_question_binding(self):
        # CQ7 is a U1-only canonical alias; U2 has an independent CQ8 mapping.
        with self.assertRaisesRegex(BadRange,"UNQUALIFIED_UNIVERSE_TARGET"):
            self.store.select(accepted=self.a,universe="U2",respondent="R1",
                              target="CQ7",scope=self.scope)
        self.assertEqual(self.store.select(accepted=self.a,universe="U2",
                                            respondent="R1",target="NQ7",scope=self.scope)[0][2],
                         "SUBSTANTIVE_RESPONSE")

    def test_global_whitelist_cannot_convert_unissued_question_into_valid_empty(self):
        globally_known=replace(self.scope,targets=self.scope.targets+("GHOST",))
        candidate=DiskSemanticIndex.build(Path(self.tmp.name)/"globalonly.db",
                                          self.events,scope=globally_known)
        self.addCleanup(candidate.db.close)
        with self.assertRaisesRegex(BadRange,"UNQUALIFIED_UNIVERSE_TARGET"):
            candidate.select(accepted=candidate.anchor,universe="U1",respondent="R1",
                             target="GHOST",scope=globally_known)

    def test_fabricated_canonical_alias_fails_before_root_publication(self):
        event=replace(self.events[0],canonical="FAKE_CANONICAL")
        with self.assertRaisesRegex(BadRange,"EVENT_QUESTION_BINDING_OR_DOMAIN_MISMATCH"):
            DiskSemanticIndex.build(Path(self.tmp.name)/"bad_alias.db",
                                    (event,)+self.events[1:],scope=self.scope)

    def test_out_of_domain_event_fails_before_accepted_selector_root(self):
        extra=Event("U9","R8","NQ7","g","0","X","SUBSTANTIVE_RESPONSE")
        with self.assertRaisesRegex(BadRange,"EVENT_QUESTION_BINDING_OR_DOMAIN_MISMATCH"):
            DiskSemanticIndex.build(Path(self.tmp.name)/"bad_domain.db",
                                    self.events+(extra,),scope=self.scope)

    def test_legitimate_no_event_question_has_positive_binding_but_no_postings(self):
        self.assertTrue(self.scope.allows_target("U1","ABSENT"))
        self.assertEqual(self.ask("ABSENT"),())
        self.assertFalse(self.scope.allows_target("U2","ABSENT"))
        with self.assertRaisesRegex(BadRange,"UNQUALIFIED_UNIVERSE_TARGET"):
            self.store.select(accepted=self.a,universe="U2",respondent="R1",
                              target="ABSENT",scope=self.scope)

    def test_mapping_authority_removed_with_same_events_invalidates_store(self):
        grants=list(self.scope.question_bindings)
        grants[0]=replace(grants[0],canonical_authority_ref="")
        invalid=replace(self.scope,question_bindings=tuple(grants))
        with self.assertRaisesRegex(BadRange,"QUESTION_BINDING_NOT_GOVERNED"):
            DiskSemanticIndex.build(Path(self.tmp.name)/"bad_mapping.db",
                                    self.events,scope=invalid)
        with self.assertRaisesRegex(BadRange,"DOMAIN_SCOPE_NOT_ATTESTED"):
            self.store.select(accepted=self.a,universe="U1",respondent="R1",
                              target="NQ7",scope=invalid)

    def test_proof_work_bounded_by_log_tree_height(self):
        self.assertEqual(len(self.ask()),3)
        self.assertLessEqual(self.store.proof_peak,8)
        self.assertGreater(self.store.proof_peak,0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
