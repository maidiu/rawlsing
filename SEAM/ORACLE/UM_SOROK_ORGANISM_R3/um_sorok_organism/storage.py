"""Research-only independent event and state owner. NEVER writes native P2/P3.
SQLite atomic world+actors transaction, version guards and append-only hash chain.
"""
import sqlite3, json, threading
from contextlib import contextmanager
from pathlib import Path
from .types import canonical, digest, copy, GRADE

class Conflict(Exception): pass
class Missing(Exception): pass

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

    def initialize(self, world, actors, source_seals=None):
        with self.tx():
            if self.conn.execute('SELECT 1 FROM worlds WHERE id=?',(world['id'],)).fetchone():
                raise Conflict('world already initialized')
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

    def seal_source(self, sid, category, content):
        """Optional late source seal: chain-anchor atomically, never an orphan row.

        A source insertion is a historical data act, not psychology formation.
        It must be emitted through the same world-anchored research chain.
        """
        with self.tx():
            if self.conn.execute('SELECT 1 FROM source_seals WHERE id=?',(sid,)).fetchone():
                raise Conflict('source seal immutable')
            row=self.conn.execute('SELECT id,body FROM worlds ORDER BY id LIMIT 1').fetchone()
            if not row:raise Conflict('SOURCE_SEAL_REQUIRES_INITIALIZED_WORLD')
            wid,body=row;world=json.loads(body)
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
        x=self.conn.execute('SELECT type,content FROM source_seals WHERE id=?',(sid,)).fetchone()
        return None if not x else {'category':x[0], 'content':json.loads(x[1])}

    def commit(self,wid,expected_world,world,actors,actor_versions,kind,actor_id,payload):
        """All research state is committed atomically with immutable objective receipt."""
        if world['id']!=wid: raise Conflict('wrong world')
        with self.tx():
            v=self.conn.execute('SELECT version FROM worlds WHERE id=?',(wid,)).fetchone()
            if not v or v[0]!=expected_world: raise Conflict('STALE_WORLD')
            for aid,a in actors.items():
                cur=self.conn.execute('SELECT version FROM actors WHERE id=?',(aid,)).fetchone()
                if not cur or cur[0]!=actor_versions[aid] or a['id']!=aid:
                    raise Conflict('STALE_ACTOR:'+aid)
            prior=self.conn.execute('SELECT chain_hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
            prev=prior[0] if prior else 'GENESIS'
            full_actors={aid:json.loads(blob) for aid,blob in self.conn.execute('SELECT id,body FROM actors')}
            full_actors.update(actors)
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
            self.conn.execute('INSERT INTO events(eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash) VALUES(?,?,?,?,?,?,?,?)',
                              (eid,wid,world['clock'],actor_id,kind,canonical(envelope),prev,chain))
            return {'id':eid,'chain_hash':chain,'envelope':envelope}

    def events(self,limit=None):
        if limit is None:
            x=self.conn.execute('SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash FROM events ORDER BY seq')
        else:
            x=self.conn.execute('SELECT eid,world_id,clock,actor_id,kind,payload,previous_hash,chain_hash FROM events ORDER BY seq LIMIT ?', (limit,))
        return [{'id':e,'world_id':wid,'clock':clock,'actor_id':aid,'kind':kind,
                 'envelope':json.loads(p),'envelope_bytes':p,
                 'previous_hash':prev,'chain_hash':h}
                for e,wid,clock,aid,kind,p,prev,h in x]

    def verify_chain(self):
        """Fail closed in ordinary AND Python -O interpreters.

        The chain binds the *whole SQLite event record*, not only a JSON
        subdocument. Source custody requires exact canonical bytes for
        conditioning; semantically identical whitespace is still a changed
        source seal. This is local integrity, not native cryptographic issuer.
        """
        prior='GENESIS';count=0;anchored={}
        records=self.events()
        if not records:
            raise AssertionError('MISSING_OBJECTIVE_EVENT_HISTORY')
        for r in records:
            envelope=r['envelope']
            if canonical(envelope)!=r['envelope_bytes']:
                raise AssertionError('EVENT_ENVELOPE_NONCANONICAL_BYTES')
            if (r['world_id']!=envelope['world'] or r['clock']!=envelope['clock']
                or r['actor_id']!=envelope['actor'] or r['kind']!=envelope['kind']):
                raise AssertionError('EVENT_HEADER_ENVELOPE_MISMATCH')
            if r['previous_hash']!=prior:
                raise AssertionError('BROKEN_EVENT_ANCESTRY')
            if r['id']!='evt_'+digest({'prev':prior,'envelope':envelope})[:20]:
                raise AssertionError('BAD_EVENT_ID')
            if r['chain_hash']!=digest({'previous':prior,'eid':r['id'],'envelope':envelope}):
                raise AssertionError('BAD_EVENT_CHAIN_HASH')
            for sid,sha in envelope.get('source_seal_digests',{}).items():
                if sid in anchored:
                    raise AssertionError('SOURCE_SEAL_DUPLICATE_ANCHOR:'+sid)
                anchored[sid]=sha
            prior=r['chain_hash'];count+=1
        actual={}
        for sid,cat,content in self.conn.execute('SELECT id,type,content FROM source_seals'):
            normalized=json.loads(content)
            if canonical(normalized)!=content:
                raise AssertionError('SOURCE_SEAL_NONCANONICAL_BYTES:'+sid)
            actual[sid]=digest({'category':cat,'content':normalized})
        if anchored!=actual:
            raise AssertionError('SOURCE_SEAL_ANCHOR_MISMATCH_OR_UNANCHORED_LEGACY')
        if records:
            last=records[-1]['envelope']
            if digest(self.world(last['world'])[1])!=last['world_digest']:
                raise AssertionError('LAST_WORLD_STATE_CHANGED_OUTSIDE_LEDGER')
            actors=self.actors()
            if set(actors)!=set(last['actor_digests']):
                raise AssertionError('UNCOMMITTED_ACTOR_SET')
            for aid,ahash in last['actor_digests'].items():
                if aid not in actors or digest(actors[aid])!=ahash:
                    raise AssertionError('LAST_ACTOR_STATE_CHANGED_OUTSIDE_LEDGER:'+aid)
        return {'grade':GRADE,'events':count,'valid':True,'last_hash':prior,
                'source_seals_verified':len(anchored)}

    def close(self): self.conn.close()
