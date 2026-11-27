"""Research-only independent event and state owner. NEVER writes native P2/P3.
SQLite atomic world+actors transaction, version guards and append-only hash chain.
"""
import sqlite3, json, threading, hashlib
from contextlib import contextmanager
from pathlib import Path
from .types import canonical, digest, copy, GRADE

class Conflict(Exception): pass
class Missing(Exception): pass

def _canonical_event_hashes(envelope, raw, prior, eid):
    """Hash the already verified canonical envelope without reserializing it.

    The existing sorted JSON preimages are retained byte for byte.
    No memoization or trusted cached history: callers must first establish
    canonical(envelope) == raw. Envelope argument also permits matched legacy
    hashing in the economic court.
    """
    payload=raw.encode('utf-8')
    def hash_parts(*parts):
        h=hashlib.sha256()
        for part in parts:h.update(part)
        return h.hexdigest()
    previous=canonical(prior).encode('utf-8')
    identity=hash_parts(b'{"envelope":',payload,b',"prev":',previous,b'}')
    chain=hash_parts(b'{"eid":',canonical(eid).encode('utf-8'),
                     b',"envelope":',payload,b',"previous":',previous,b'}')
    return 'evt_'+identity[:20],chain


def _canonical_object_hash(value, raw):
    """Reuse bytes *after* the caller has proved canonical(value) == raw.

    Retain parsed value for the exact original hashing comparator. Never use
    this as a substitute for canonical byte or type/identity verification.
    """
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _canonical_seal_hash(category, value, raw):
    """Exact canonical source-seal wrapper; only validated content bytes."""
    h=hashlib.sha256()
    h.update(b'{"category":')
    h.update(canonical(category).encode('utf-8'))
    h.update(b',"content":')
    h.update(raw.encode('utf-8'))
    h.update(b'}')
    return h.hexdigest()


class ResearchLedger:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, isolation_level=None)
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.execute('PRAGMA foreign_keys=ON')
        self.lock = threading.RLock()
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS worlds(id TEXT PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS actors(id TEXT PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT, eid TEXT NOT NULL UNIQUE,
           world_id TEXT NOT NULL, clock INTEGER NOT NULL, actor_id TEXT, kind TEXT NOT NULL,
           payload TEXT NOT NULL, previous_hash TEXT NOT NULL, chain_hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS source_seals(id TEXT PRIMARY KEY, type TEXT NOT NULL, content TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS constraints(id TEXT PRIMARY KEY, description TEXT NOT NULL, status TEXT NOT NULL);
        ''')

    @contextmanager
    def tx(self):
        with self.lock:
            self.conn.execute('BEGIN IMMEDIATE')
            try:
                yield
                self.conn.execute('COMMIT')
            except Exception:
                self.conn.execute('ROLLBACK')
                raise

    def _verify_current_anchor_locked(self, wid):
        """Prevent a later valid receipt from laundering uncommitted state.

        The most recent event must still bind the *current persisted* world and
        complete actor roster before adding anything to that same history. This
        is deliberately O(actors), not a full historical chain scan on every
        life step. ``verify_chain`` remains the full independent audit.
        This method is called only inside the SQLite IMMEDIATE transaction.
        """
        self._verified_source_seals_locked()
        first=self.conn.execute('SELECT kind FROM events ORDER BY seq LIMIT 1').fetchone()
        last=self.conn.execute('SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash '
                               'FROM events ORDER BY seq DESC LIMIT 1').fetchone()
        if not first or first[0]!='INITIALIZATION' or not last:
            raise Conflict('MISSING_LEDGER_GENESIS')
        eid,event_world,event_clock,event_actor,kind,payload,prior,chain=last
        try:
            envelope=json.loads(payload)
            if (canonical(envelope)!=payload or event_world!=envelope['world'] or
                event_clock!=envelope['clock'] or event_actor!=envelope['actor'] or
                kind!=envelope['kind']):
                raise Conflict('UNCOMMITTED_LEDGER_RECORD')
            expected_id,expected_chain=_canonical_event_hashes(envelope,payload,prior,eid)
            if eid!=expected_id or chain!=expected_chain:
                raise Conflict('UNCOMMITTED_LEDGER_RECORD')
        except (ValueError,TypeError,KeyError) as exc:
            raise Conflict('UNCOMMITTED_LEDGER_RECORD') from exc
        if event_world!=wid:
            raise Conflict('UNCOMMITTED_WORLD_ROSTER')
        rows=self.conn.execute('SELECT id,body FROM worlds').fetchall()
        if len(rows)!=1 or rows[0][0]!=wid:
            raise Conflict('UNCOMMITTED_WORLD_ROSTER')
        try:
            world=json.loads(rows[0][1])
            if canonical(world)!=rows[0][1] or _canonical_object_hash(world,rows[0][1])!=envelope['world_digest'] or world['clock']!=event_clock:
                raise Conflict('UNCOMMITTED_WORLD_STATE')
        except (ValueError,TypeError,KeyError) as exc:
            raise Conflict('UNCOMMITTED_WORLD_STATE') from exc
        rows=self.conn.execute('SELECT id,body FROM actors').fetchall()
        if set(aid for aid,_ in rows)!=set(envelope['actor_digests']):
            raise Conflict('UNCOMMITTED_ACTOR_STATE')
        for aid,raw in rows:
            try:
                person=json.loads(raw)
                if (canonical(person)!=raw or person.get('id')!=aid or
                    _canonical_object_hash(person,raw)!=envelope['actor_digests'][aid]):
                    raise Conflict('UNCOMMITTED_ACTOR_STATE')
            except (ValueError,TypeError,KeyError) as exc:
                raise Conflict('UNCOMMITTED_ACTOR_STATE') from exc

    def _verified_source_seals_locked(self):
        """Audit every auxiliary source against its exact historical issuer event.

        The ledger's event digest is *not* a cryptographic credential. This
        checks source custody and refuses unanchored auxiliary state in this
        research DB; it does not authorize an external disclosure or native
        scientific issuer. Called before appends and source reads, not only
        when an analyst explicitly requests verify_chain().
        """
        if self.conn.execute('SELECT 1 FROM constraints LIMIT 1').fetchone():
            raise Conflict('UNANCHORED_CONSTRAINTS_STATE')
        anchored={}
        seen_genesis=False
        for kind, raw in self.conn.execute(
                "SELECT kind,payload FROM events WHERE kind IN ('INITIALIZATION','SOURCE_SEAL') ORDER BY seq"):
            try:
                env=json.loads(raw)
                seals=env.get('source_seal_digests')
                if type(seals) is not dict:
                    raise ValueError('MISSING_SEAL_MAP')
                if kind=='INITIALIZATION':
                    if seen_genesis:
                        raise ValueError('DUPLICATE_GENESIS_ANCHOR')
                    seen_genesis=True
                else:
                    detail=env.get('payload')
                    if (len(seals)!=1 or type(detail) is not dict or
                            env.get('actor') is not None):
                        raise ValueError('SOURCE_SEAL_EVENT_WRONG_SHAPE')
                    sid,hash_value=next(iter(seals.items()))
                    if (detail.get('source_id')!=sid or
                            detail.get('source_digest')!=hash_value):
                        raise ValueError('SOURCE_SEAL_EVENT_MISMATCH')
                for sid,sha in seals.items():
                    if (type(sid) is not str or type(sha) is not str or
                            not sid or not sha or sid in anchored):
                        raise ValueError('DUPLICATE_OR_INVALID_SOURCE_SEAL')
                    anchored[sid]=sha
            except (ValueError,TypeError,KeyError,StopIteration) as exc:
                raise Conflict('SOURCE_SEAL_EVENT_INVALID') from exc
        actual={}
        for sid,category,raw in self.conn.execute('SELECT id,type,content FROM source_seals'):
            try:
                content=json.loads(raw)
                if canonical(content)!=raw:
                    raise ValueError('NONCANONICAL_SOURCE_BYTES')
                actual[sid]=_canonical_seal_hash(category,content,raw)
            except (ValueError,TypeError) as exc:
                raise Conflict('SOURCE_SEAL_TABLE_NONCANONICAL') from exc
        if anchored!=actual:
            raise Conflict('SOURCE_SEAL_ANCHOR_MISMATCH_OR_UNANCHORED')
        return anchored

    def _require_valid_history_locked(self):
        """Full source/chain preflight for reads and appends, not only audits.

        The fast auxiliary check is insufficient for noncanonical historical
        envelopes or source maps on ordinary events. This bounded owner repair
        reuses the complete verifier under the existing lock/transaction.
        """
        try:
            self.verify_chain()
        except AssertionError as exc:
            message=str(exc)
            # Preserve inherited P045/P046 diagnostics while still refusing
            # every malformed/noncanonical or unauthorized source history.
            if message.startswith('LAST_WORLD_STATE_CHANGED_OUTSIDE_LEDGER'):
                raise Conflict('UNCOMMITTED_WORLD_STATE') from exc
            if message.startswith('LAST_ACTOR_STATE_CHANGED_OUTSIDE_LEDGER'):
                raise Conflict('UNCOMMITTED_ACTOR_STATE') from exc
            if message=='MISSING_OBJECTIVE_EVENT_HISTORY':
                raise Conflict('MISSING_LEDGER_GENESIS') from exc
            raise Conflict('SOURCE_HISTORY_INVALID: '+message) from exc
        except (KeyError,TypeError,ValueError,StopIteration) as exc:
            raise Conflict('SOURCE_HISTORY_INVALID: '+type(exc).__name__+': '+str(exc)) from exc

    @staticmethod
    def _validate_source_identity(sid, category):
        if (type(sid) is not str or not sid.strip() or
                type(category) is not str or not category.strip()):
            raise Conflict('INVALID_SOURCE_IDENTITY')

    def initialize(self, world, actors, source_seals=None):
        with self.tx():
            if self.conn.execute('SELECT 1 FROM worlds WHERE id=?',(world['id'],)).fetchone():
                raise Conflict('world already initialized')
            if self.conn.execute('SELECT 1 FROM worlds LIMIT 1').fetchone():
                # This research DB has one ordered objective world event chain.
                # A second genesis would create an unrelated world with a
                # misleading shared ancestry.
                raise Conflict('MULTIWORLD_RESEARCH_DB_UNSUPPORTED')
            if (self.conn.execute('SELECT 1 FROM source_seals LIMIT 1').fetchone() or
                    self.conn.execute('SELECT 1 FROM constraints LIMIT 1').fetchone()):
                raise Conflict('UNANCHORED_PREGENESIS_AUXILIARY_STATE')
            for a in actors:
                if a['id'] in world['positions']:
                    raise Conflict('duplicate actor')
                world['positions'][a['id']] = a['location']
                world.setdefault('accounts',{}).setdefault(a['id'],0.0)
                world.setdefault('holdings',{}).setdefault(a['id'],{'food':0})
            # Sealed conditioning is durable *inside* the initialization
            # transaction. Legacy unanchored seals cannot be treated as verified.
            seals={}
            for sid,category,content in (source_seals or []):
                self._validate_source_identity(sid,category)
                if sid in seals:raise Conflict('DUPLICATE_SOURCE_SEAL')
                seals[sid]=digest({'category':category,'content':content})
                self.conn.execute('INSERT INTO source_seals VALUES(?,?,?)',
                                  (sid,category,canonical(content)))
            self.conn.execute('INSERT INTO worlds VALUES(?,?,?)',(world['id'],0,canonical(world)))
            for a in actors:
                self.conn.execute('INSERT INTO actors VALUES(?,?,?)',(a['id'],0,canonical(a)))
            envelope={'world':world['id'],'clock':world['clock'],'kind':'INITIALIZATION',
              'actor':None,'payload':{'actor_ids':sorted(a['id'] for a in actors),
                                     'grade':'FICTIONAL_GENESIS'},
              'world_digest':digest(world),
              'actor_digests':{a['id']:digest(a) for a in sorted(actors,key=lambda x:x['id'])},
              'source_seal_digests':seals,
              'grade':GRADE}
            prior='GENESIS'
            eid='evt_'+digest({'prev':prior,'envelope':envelope})[:20]
            chain=digest({'previous':prior,'eid':eid,'envelope':envelope})
            self.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) VALUES(?,?,?,?,?,?,?,?)',
              (eid,world['id'],world['clock'],None,'INITIALIZATION',canonical(envelope),prior,chain))

    def world(self, wid='w1'):
        x=self.conn.execute('SELECT version,body FROM worlds WHERE id=?',(wid,)).fetchone()
        if not x: raise Missing('WORLD_NOT_INITIALIZED')
        return x[0],json.loads(x[1])

    def actor(self, aid):
        x=self.conn.execute('SELECT version,body FROM actors WHERE id=?',(aid,)).fetchone()
        if not x: raise Missing('ACTOR_NOT_FOUND:'+aid)
        return x[0],json.loads(x[1])

    def actors(self):
        return {a:json.loads(b) for a,b in self.conn.execute('SELECT id,body FROM actors')}

    def actors_with_versions(self):
        """One roster statement binds each decoded body to its own version.

        No trusted cache or cross-statement roster claim. The existing world
        version and per-actor CAS checks, full historical audit, and anchor
        verification remain authoritative at commit.
        """
        versions={};actors={}
        for aid,version,body in self.conn.execute('SELECT id,version,body FROM actors'):
            versions[aid]=version
            actors[aid]=json.loads(body)
        return versions,actors

    def seal_source(self, sid, category, content, *, expected_world=None):
        """Optional late source seal: chain-anchor atomically, never an orphan row.

        A source insertion is a historical data act, not psychology formation.
        It must be emitted through the same world-anchored research chain.
        """
        self._validate_source_identity(sid,category)
        with self.tx():
            if self.conn.execute('SELECT 1 FROM source_seals WHERE id=?',(sid,)).fetchone():
                raise Conflict('source seal immutable')
            row=self.conn.execute('SELECT id,body FROM worlds ORDER BY id LIMIT 1').fetchone()
            if not row:raise Conflict('SOURCE_SEAL_REQUIRES_INITIALIZED_WORLD')
            wid,body=row
            if expected_world is not None and self.conn.execute('SELECT version FROM worlds WHERE id=?',(wid,)).fetchone()[0]!=expected_world:
                raise Conflict('STALE_WORLD')
            self._require_valid_history_locked()
            self._verify_current_anchor_locked(wid)
            world=json.loads(body)
            sha=digest({'category':category,'content':content})
            prior=self.conn.execute('SELECT chain_hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
            prev=prior[0] if prior else 'GENESIS'
            actor_map={aid:json.loads(blob) for aid,blob in self.conn.execute('SELECT id,body FROM actors')}
            envelope={'world':wid,'clock':world['clock'],'kind':'SOURCE_SEAL',
                'actor':None,'payload':{'source_id':sid,'source_digest':sha},
                'world_digest':digest(world),
                'actor_digests':{aid:digest(actor) for aid,actor in sorted(actor_map.items())},
                'source_seal_digests':{sid:sha},'grade':GRADE}
            eid='evt_'+digest({'prev':prev,'envelope':envelope})[:20]
            chain=digest({'previous':prev,'eid':eid,'envelope':envelope})
            self.conn.execute('INSERT INTO source_seals VALUES(?,?,?)',(sid,category,canonical(content)))
            self.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) VALUES(?,?,?,?,?,?,?,?)',
                              (eid,wid,world['clock'],None,'SOURCE_SEAL',canonical(envelope),prev,chain))

    def source(self,sid):
        with self.lock:
            self._require_valid_history_locked()
            x=self.conn.execute('SELECT type,content FROM source_seals WHERE id=?',(sid,)).fetchone()
            return None if not x else {'category':x[0], 'content':json.loads(x[1])}

    def commit(self,wid,expected_world,world,actors,actor_versions,kind,actor_id,payload,*,_family_actor=None):
        """All research state is committed atomically with immutable objective receipt."""
        if world['id']!=wid: raise Conflict('wrong world')
        # Reserved source-identity events are issued only by seal_source()
        # alongside the actual source_seals table row in one transaction.
        if kind in ('INITIALIZATION','SOURCE_SEAL'):
            raise Conflict('RESERVED_SOURCE_EVENT_KIND')
        family_entry=kind in ('FAMILY_COUNTERPART_ADMITTED','FAMILY_CHILD_BORN')
        if family_entry!=(_family_actor is not None):raise Conflict('FAMILY_ROSTER_AUTHORITY_REQUIRED')
        with self.tx():
            v=self.conn.execute('SELECT version FROM worlds WHERE id=?',(wid,)).fetchone()
            if not v or v[0]!=expected_world: raise Conflict('STALE_WORLD')
            self._require_valid_history_locked()
            self._verify_current_anchor_locked(wid)
            for aid,a in actors.items():
                cur=self.conn.execute('SELECT version FROM actors WHERE id=?',(aid,)).fetchone()
                if not cur or cur[0]!=actor_versions[aid] or a['id']!=aid:
                    raise Conflict('STALE_ACTOR:'+aid)
            prior=self.conn.execute('SELECT chain_hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
            prev=prior[0] if prior else 'GENESIS'
            full_actors={aid:json.loads(blob) for aid,blob in self.conn.execute('SELECT id,body FROM actors')}
            full_actors.update(actors)
            prior_world=json.loads(self.conn.execute('SELECT body FROM worlds WHERE id=?',(wid,)).fetchone()[0])
            if family_entry:
                aid=_family_actor.get('id');loc=_family_actor.get('location')
                if (actors or actor_versions or aid!=actor_id or aid in full_actors
                        or aid in prior_world.get('accounts',{}) or aid in prior_world.get('holdings',{})
                        or aid in prior_world.get('neighbor_users',{})
                        or loc not in prior_world['sites'] or world['clock']!=prior_world['clock']
                        or payload.get('admitted_actor')!=aid):raise Conflict('FAMILY_INVALID_ROSTER_ADMISSION')
                source=self.conn.execute('SELECT type,content FROM source_seals WHERE id=?',(payload.get('source_seal_id'),)).fetchone()
                if (not source or source[0]!='FICTIONAL_FAMILY_PATHWAY_CANDIDATES'
                        or digest({'category':source[0],'content':json.loads(source[1])})!=payload.get('source_digest')):
                    raise Conflict('FAMILY_UNSEALED_PATHWAY')
                family=payload['family_genesis'];path=family['selected_pathway']
                content=json.loads(source[1]);matches=[x for x in content['candidates'] if x['id']==path['id']]
                if (len(matches)!=1 or content['mother']!=path['mother']
                        or family['source_seal_id']!=payload['source_seal_id']
                        or family['source_digest']!=payload['source_digest']):
                    raise Conflict('FAMILY_PATHWAY_SOURCE_MISMATCH')
                chosen=matches[0]
                if (any(path[k]!=chosen[k] for k in ('id','source_ref','intersection_clock','intersection_site','conception_clock','birth_clock','child_id','child_name'))
                        or path['counterpart']!=chosen['counterpart_id']):
                    raise Conflict('FAMILY_PATHWAY_SOURCE_MISMATCH')
                if kind=='FAMILY_COUNTERPART_ADMITTED':
                    if (family['stage']!='COUNTERPART_ADMITTED' or aid!=path['counterpart']
                            or loc!=path['intersection_site'] or world['clock']!=path['intersection_clock']
                            or prior_world['positions'].get(path['mother'])!=loc):
                        raise Conflict('FAMILY_COUNTERPART_BOUNDARY_MISMATCH')
                elif (family['stage']!='CHILD_BORN' or aid!=path['child_id']
                        or world['clock']!=path['birth_clock'] or loc!=prior_world['positions'].get(path['mother'])
                        or prior_world.get('family_genesis',{}).get('selected_pathway')!=path
                        or prior_world.get('family_genesis',{}).get('conception')!=family.get('conception')):
                    raise Conflict('FAMILY_BIRTH_BOUNDARY_MISMATCH')
                expected=copy(prior_world)
                expected['positions'][aid]=loc
                expected.setdefault('accounts',{})[aid]=0.0
                expected.setdefault('holdings',{})[aid]={'food':0}
                expected['family_genesis']=copy(payload['family_genesis'])
                if world!=expected:raise Conflict('FAMILY_ADMISSION_REWRITES_WORLD')
                if kind=='FAMILY_CHILD_BORN':
                    from .types import newborn
                    if (_family_actor!=newborn(aid,_family_actor.get('name'),loc)
                            or prior_world.get('family_genesis',{}).get('stage')!='CONCEPTION_ADMITTED'):
                        raise Conflict('FAMILY_CHILD_NOT_SPARSE_OR_NO_CONCEPTION')
                elif (_family_actor.get('role')!='adult' or prior_world.get('family_genesis')):
                    raise Conflict('FAMILY_COUNTERPART_NOT_INDEPENDENT_ADULT')
                full_actors[aid]=_family_actor
            prior_family=prior_world.get('family_genesis',{})
            if kind=='FAMILY_CONCEPTION':
                from .historical_parent_bridge import family_encounter_evidence, FAMILY_GRADE
                from .types import stable_id
                if (actors or actor_versions or actor_id is not None
                        or prior_family.get('stage')!='COUNTERPART_ADMITTED'):
                    raise Conflict('FAMILY_CONCEPTION_AUTHORITY_REQUIRED')
                path=prior_family['selected_pathway']
                encounters=family_encounter_evidence(prior_world,path)
                if (prior_world['clock']!=path['conception_clock'] or not encounters
                        or any(prior_world['positions'].get(a)!=path['intersection_site']
                               for a in (path['mother'],path['counterpart']))):
                    raise Conflict('FAMILY_CONCEPTION_UNQUALIFIED_HISTORY')
                expected_family=copy(prior_family)
                expected_family['stage']='CONCEPTION_ADMITTED'
                expected_family['conception']={'id':stable_id('conditional_conception',path),
                    'clock':prior_world['clock'],'encounter_evidence':encounters[-1],
                    'sourcefree_branch_premise_not_biological_or_consent_inference':True,
                    'no_child_actor_yet':True,'grade':FAMILY_GRADE}
                expected=copy(prior_world);expected['family_genesis']=expected_family
                if world!=expected or payload.get('family_genesis')!=expected_family:
                    raise Conflict('FAMILY_CONCEPTION_REWRITES_HISTORY')
            elif not family_entry and world.get('family_genesis',{})!=prior_family:
                raise Conflict('FAMILY_TRANSITION_REQUIRES_QUALIFIED_EVENT')
            if (prior_family.get('stage')=='CONCEPTION_ADMITTED' and not family_entry
                    and world['clock']>prior_family['selected_pathway']['birth_clock']):
                raise Conflict('FAMILY_BIRTH_BOUNDARY_REQUIRES_REALIZATION')
            if actor_id is not None and actor_id not in full_actors:
                raise Conflict('UNKNOWN_EVENT_ACTOR')
            # A fabricated position is a fabricated co-present Other. Actor IDs,
            # physical positions, and actor-owned location are one closed roster.
            if set(world.get('positions',{})) != set(full_actors):
                raise Conflict('UNREGISTERED_WORLD_POSITION')
            if any(a.get('location')!=world['positions'][aid] or a.get('id')!=aid
                   for aid,a in full_actors.items()):
                raise Conflict('ACTOR_WORLD_POSITION_DIVERGENCE')
            latest=self.conn.execute('SELECT payload FROM events ORDER BY seq DESC LIMIT 1').fetchone()
            if (type(world.get('clock')) is not int or world['clock']<0 or
                    (latest and world['clock']<json.loads(latest[0])['clock'])):
                raise Conflict('WORLD_CLOCK_REGRESSION')
            envelope={'world':wid, 'clock':world['clock'],'kind':kind,'actor':actor_id,
                      'payload':payload,'world_digest':digest(world),
                      'actor_digests':{k:digest(v) for k,v in sorted(full_actors.items())},
                      'grade':GRADE}
            eid='evt_'+digest({'prev':prev,'envelope':envelope})[:20]
            chain=digest({'previous':prev,'eid':eid,'envelope':envelope})
            self.conn.execute('UPDATE worlds SET version=?,body=? WHERE id=?',
                              (expected_world+1,canonical(world),wid))
            for aid,a in actors.items():
                self.conn.execute('UPDATE actors SET version=?,body=? WHERE id=?',
                                  (actor_versions[aid]+1,canonical(a),aid))
            if family_entry:
                self.conn.execute('INSERT INTO actors VALUES(?,?,?)',(_family_actor['id'],0,canonical(_family_actor)))
            self.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) VALUES(?,?,?,?,?,?,?,?)',
                              (eid,wid,world['clock'],actor_id,kind,canonical(envelope),prev,chain))
            return {'id':eid,'chain_hash':chain,'envelope':envelope}

    def _iter_events(self,limit=None):
        if limit is None:
            x=self.conn.execute('SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash FROM events ORDER BY seq')
        else:
            x=self.conn.execute('SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash FROM events ORDER BY seq LIMIT ?', (limit,))
        for e,wid,clock,aid,kind,p,prev,h in x:
            yield {'id':e,'world_id':wid,'clock':clock,'actor_id':aid,'kind':kind,
                   'envelope':json.loads(p),'envelope_bytes':p,
                   'previous_hash':prev,'chain_hash':h}

    def events(self,limit=None):
        # Retain the existing public materialized reader contract.
        return list(self._iter_events(limit))

    def latest_event(self):
        """Bounded read of the exact existing tail record, not a new cache.

        Same event envelope as events()[-1], without hydrating earlier life.
        The enclosing step still uses the existing CAS/chain verification.
        """
        row=self.conn.execute(
            'SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash '
            'FROM events ORDER BY seq DESC LIMIT 1').fetchone()
        if row is None:return None
        e,wid,clock,aid,kind,p,prev,h=row
        return {'id':e,'world_id':wid,'clock':clock,'actor_id':aid,'kind':kind,
                'envelope':json.loads(p),'envelope_bytes':p,
                'previous_hash':prev,'chain_hash':h}

    def verify_chain(self):
        """Fail closed in ordinary AND Python -O interpreters.

        The chain binds the *whole SQLite event record*, not only a JSON
        subdocument. Source custody requires exact canonical bytes for
        conditioning; semantically identical whitespace is still a changed
        source seal. This is local integrity, not native cryptographic issuer.
        """
        prior='GENESIS';count=0;anchored={};previous_roster=None;previous_actor_digests=None
        last=None
        # Complete verification still visits every row, in the existing order.
        # Only the current row and the predecessor metadata must remain live.
        for idx,r in enumerate(self._iter_events()):
            envelope=r['envelope']
            if (type(envelope) is not dict or
                    any(k not in envelope for k in ('world','clock','actor','kind'))):
                raise AssertionError('EVENT_ENVELOPE_MALFORMED')
            if canonical(envelope)!=r['envelope_bytes']:
                raise AssertionError('EVENT_ENVELOPE_NONCANONICAL_BYTES')
            if (r['world_id']!=envelope['world'] or r['clock']!=envelope['clock']
                or r['actor_id']!=envelope['actor'] or r['kind']!=envelope['kind']):
                raise AssertionError('EVENT_HEADER_ENVELOPE_MISMATCH')
            if idx==0 and (r['kind']!='INITIALIZATION' or r['actor_id'] is not None or
                           r['previous_hash']!='GENESIS'):
                raise AssertionError('NOT_INITIALIZATION_GENESIS')
            if idx>0 and r['kind']=='INITIALIZATION':
                raise AssertionError('DUPLICATE_INITIALIZATION_GENESIS')
            if r['previous_hash']!=prior:
                raise AssertionError('BROKEN_EVENT_ANCESTRY')
            expected_id,expected_chain=_canonical_event_hashes(
                envelope,r['envelope_bytes'],prior,r['id'])
            if r['id']!=expected_id:
                raise AssertionError('BAD_EVENT_ID')
            if r['chain_hash']!=expected_chain:
                raise AssertionError('BAD_EVENT_CHAIN_HASH')
            seals=envelope.get('source_seal_digests',{})
            if type(seals) is not dict:
                raise AssertionError('SOURCE_SEAL_EVENT_INVALID_MAP')
            if r['kind']=='SOURCE_SEAL':
                payload=envelope.get('payload')
                if (len(seals)!=1 or r['actor_id'] is not None or
                        type(payload) is not dict):
                    raise AssertionError('SOURCE_SEAL_EVENT_INVALID')
                sid,sha=next(iter(seals.items()))
                if (payload.get('source_id')!=sid or
                        payload.get('source_digest')!=sha):
                    raise AssertionError('SOURCE_SEAL_EVENT_MISMATCH')
            elif r['kind']!='INITIALIZATION' and seals:
                raise AssertionError('SOURCE_SEAL_EVENT_UNAUTHORIZED_ANCHOR')
            for sid,sha in seals.items():
                if (type(sid) is not str or type(sha) is not str or
                        not sid or not sha or sid in anchored):
                    raise AssertionError('SOURCE_SEAL_DUPLICATE_OR_INVALID_ANCHOR')
                anchored[sid]=sha
            roster=set(envelope['actor_digests'])
            if r['kind'] in ('FAMILY_COUNTERPART_ADMITTED','FAMILY_CHILD_BORN'):
                detail=envelope['payload'];aid=detail.get('admitted_actor')
                if (previous_roster is None or aid in previous_roster or aid!=r['actor_id']
                        or roster!=previous_roster|{aid}
                        or anchored.get(detail.get('source_seal_id'))!=detail.get('source_digest')
                        or any(envelope['actor_digests'][old]!=previous_actor_digests[old]
                               for old in previous_roster)):
                    raise AssertionError('FAMILY_ADMISSION_ANCESTRY_INVALID')
            elif previous_roster is not None and roster!=previous_roster:
                raise AssertionError('UNAUTHORIZED_HISTORICAL_ROSTER_CHANGE')
            if r['kind']=='FAMILY_CONCEPTION' and (envelope['actor_digests']!=previous_actor_digests
                    or anchored.get(envelope['payload']['family_genesis']['source_seal_id'])!=
                       envelope['payload']['family_genesis']['source_digest']):
                raise AssertionError('FAMILY_CONCEPTION_ANCESTRY_INVALID')
            previous_roster=roster
            previous_actor_digests=envelope['actor_digests']
            prior=r['chain_hash'];count+=1;last=envelope
        if last is None:
            raise AssertionError('MISSING_OBJECTIVE_EVENT_HISTORY')
        if self.conn.execute('SELECT 1 FROM constraints LIMIT 1').fetchone():
            raise AssertionError('UNANCHORED_CONSTRAINTS_STATE')
        actual={}
        for sid,cat,content in self.conn.execute('SELECT id,type,content FROM source_seals'):
            normalized=json.loads(content)
            if canonical(normalized)!=content:
                raise AssertionError('SOURCE_SEAL_NONCANONICAL_BYTES:'+sid)
            actual[sid]=_canonical_seal_hash(cat,normalized,content)
        if anchored!=actual:
            raise AssertionError('SOURCE_SEAL_ANCHOR_MISMATCH_OR_UNANCHORED_LEGACY')
        if last is not None:
            # Exact current REMONT P070: the *stored* state is committed,
            # not only the meaning of its parsed JSON. No extra world can be
            # present even if the primary world hash still matches.
            world_rows=self.conn.execute('SELECT id,body FROM worlds').fetchall()
            if len(world_rows)!=1 or world_rows[0][0]!=last['world']:
                raise AssertionError('UNCOMMITTED_WORLD_ROSTER')
            try:
                world_obj=json.loads(world_rows[0][1])
                if type(world_obj) is not dict:
                    raise AssertionError('WORLD_SNAPSHOT_NOT_OBJECT')
                if canonical(world_obj)!=world_rows[0][1]:
                    raise AssertionError('WORLD_SNAPSHOT_NONCANONICAL_BYTES')
            except (ValueError,TypeError) as exc:
                raise AssertionError('WORLD_SNAPSHOT_NONCANONICAL_BYTES') from exc
            if _canonical_object_hash(world_obj,world_rows[0][1])!=last['world_digest']:
                raise AssertionError('LAST_WORLD_STATE_CHANGED_OUTSIDE_LEDGER')
            actor_rows=self.conn.execute('SELECT id,body FROM actors').fetchall()
            if set(aid for aid,_ in actor_rows)!=set(last['actor_digests']):
                raise AssertionError('UNCOMMITTED_ACTOR_SET')
            for aid,raw in actor_rows:
                try:
                    person=json.loads(raw)
                    if type(person) is not dict:
                        raise AssertionError('ACTOR_SNAPSHOT_NOT_OBJECT:'+aid)
                    if canonical(person)!=raw:
                        raise AssertionError('ACTOR_SNAPSHOT_NONCANONICAL_BYTES:'+aid)
                except (ValueError,TypeError) as exc:
                    raise AssertionError('ACTOR_SNAPSHOT_NONCANONICAL_BYTES:'+aid) from exc
                if person.get('id')!=aid or _canonical_object_hash(person,raw)!=last['actor_digests'][aid]:
                    raise AssertionError('LAST_ACTOR_STATE_CHANGED_OUTSIDE_LEDGER:'+aid)
        return {'grade':GRADE,'events':count,'valid':True,'last_hash':prior,
                'source_seals_verified':len(anchored)}

    def close(self): self.conn.close()
