"""Operator-only sourcefree mode coordination, not another organism or scheduler.

All state changes remain with the existing native owner, P2 recursion and
NEIGHBOR. This sidecar only conserves epoch boundaries and attempt custody.
It is serialized and does not authenticate a human, authorize remote export,
or coordinate uncooperative native writers. Ambiguous operations HOLD.
"""
from contextlib import contextmanager
import fcntl
import json
from pathlib import Path
import sqlite3

from modern_generation_port_r28 import (
    ModernDevelopmentOwner, ModernGeneration, link_actual_live_interval,
    require, canonical, detached, digest, text)
from live_turn_port_r38 import LiveTurnSession

GRADE="SOURCEFREE_CONTINUING_LIFE_OPERATOR_NOT_PRODUCTION_AUTHORITY"

class ContinuingLife:
    def __init__(self,runtime,directory,actor,*,historical_provider,live_provider,
                 sourcefree_attested=False,period_catalog=None,family_sources=(),
                 selective_memory_context=False,mii_module=None):
        require(sourcefree_attested is True,"LIFE_EXPLICIT_SOURCEFREE_ONLY")
        require(hasattr(historical_provider,"call") and hasattr(live_provider,"call"),
                "LIFE_EXPLICIT_PROVIDERS")
        require(type(selective_memory_context) is bool,"LIFE_CONTEXT_PROFILE")
        self.rt=runtime;self.historical_provider=historical_provider
        self.live_provider=live_provider;self.mii=mii_module
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.actor=actor;self.config=detached({"period_catalog":period_catalog or {},
            "family_sources":sorted(set(family_sources)),
            "selective_memory_context":selective_memory_context})
        self.db=sqlite3.connect(self.directory/"operator.sqlite")
        try:
            with self.lock():
                self.db.execute("CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY CHECK(id=1),body TEXT NOT NULL)")
                self.db.execute("CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY,body TEXT NOT NULL)")
                root=runtime.ledger.events(limit=1)[0]["chain_hash"]
                runtime.ledger.actor(actor)
                head=self.native()
                binding={"root":root,"actor":actor,"world":runtime.world_id,
                         "config_digest":digest(self.config),"grade":GRADE}
                row=self.db.execute("SELECT body FROM session WHERE id=1").fetchone()
                if row is None:
                    require(not any(self.directory.glob("epoch-*")) and
                            not (self.directory/"live.sqlite").exists(),
                            "LIFE_ORPHAN_CUSTODY")
                    require(not self.present(),"LIFE_INITIAL_VISITOR_PRESENT")
                    self.db.execute("INSERT INTO session VALUES (1,?)",(canonical({
                        "binding":binding,"mode":"READY","epoch":0,"expected":head,
                        "pending":None,"terminal":None,"link":None}),))
                    self.db.commit()
                else:
                    require(json.loads(row[0])["binding"]==binding,"LIFE_FOREIGN_BINDING")
        except BaseException:
            self.db.close();raise

    @contextmanager
    def lock(self):
        with (self.directory/"operator.lock").open("a") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            yield

    def native(self):
        v=self.rt.verify()
        require(v.get("valid") is True,"LIFE_NATIVE_CHAIN_INVALID")
        return v["last_hash"]

    def present(self):
        return any(v.get("present") is True for v in
                   self.rt.ledger.world(self.rt.world_id)[1].get("neighbor_users",{}).values())

    def load(self):
        row=self.db.execute("SELECT body FROM session WHERE id=1").fetchone()
        require(row is not None,"LIFE_MISSING_SESSION")
        return json.loads(row[0])

    def save(self,state):
        self.db.execute("UPDATE session SET body=? WHERE id=1",(canonical(state),))

    def ready(self,*modes):
        s=self.load()
        require(s["pending"] is None,"LIFE_AMBIGUOUS_OPERATION_REQUIRES_DISPOSITION")
        require(s["mode"] in modes,"LIFE_WRONG_MODE")
        require(self.native()==s["expected"],"LIFE_UNRECONCILED_NATIVE_TRANSITION")
        return s

    def reserve(self,s,operation):
        row={"operation":operation,"before":s["expected"],"epoch":s["epoch"],
             "mode":s["mode"],"status":"RESERVED"}
        cur=self.db.execute("INSERT INTO attempts(body) VALUES (?)",(canonical(row),))
        s["pending"]=cur.lastrowid;self.save(s);self.db.commit()
        return row

    def execute(self,s,operation,fn,*,next_mode=None,refusal_is_local=False):
        row=self.reserve(s,operation);attempt=s["pending"]
        try:
            result=fn(s)
            after=self.native()
        except BaseException as exc:
            try:after=self.native()
            except BaseException:after=None
            # Only operations with no provider call may clear a native
            # unchanged refusal. For model calls a zero event delta proves
            # nothing about expenditure or whether a response was received.
            local=refusal_is_local and after==row["before"] and isinstance(exc,ValueError)
            row.update(status="REFUSED_UNCHANGED" if local else "HELD",
                       after=after,error=type(exc).__name__)
            if local:s["pending"]=None;self.save(s)
            self.db.execute("UPDATE attempts SET body=? WHERE id=?",(canonical(row),attempt))
            self.db.commit();raise
        s["expected"]=after;s["pending"]=None
        if next_mode is not None:s["mode"]=next_mode
        row.update(status="RETURNED",after=after,result_digest=digest(result))
        self.db.execute("UPDATE attempts SET body=? WHERE id=?",(canonical(row),attempt))
        self.save(s);self.db.commit()
        return result

    def epoch_path(self,n):
        return self.directory/("epoch-%06d"%n)

    @contextmanager
    def generation(self,s):
        path=self.epoch_path(s["epoch"]);path.mkdir(exist_ok=True)
        owner=ModernDevelopmentOwner(self.rt,self.actor,path/"ops.sqlite",
            sourcefree_attested=True,qualified_interval_cuts=True,
            period_catalog=self.config["period_catalog"],family_sources=self.config["family_sources"],
            selective_memory_context=self.config["selective_memory_context"],continuity_link=s["link"])
        g=None
        try:
            g=ModernGeneration(owner,self.historical_provider,path/"batch.sqlite",path/"cycle.json")
            yield g
        finally:
            if g is not None:g.close()
            else:owner.close()

    def historical_checkpoint(self):
        with self.lock():
            s=self.ready("READY","HISTORY")
            require(not self.present(),"LIFE_HISTORY_PRESENT_VISITOR")
            def work(state):
                with self.generation(state) as g:
                    return g.bootstrap() if state["mode"]=="READY" else g.advance()
            return self.execute(s,"HISTORICAL_CHECKPOINT",work,next_mode="HISTORY")

    def finish_history(self):
        with self.lock():
            s=self.ready("HISTORY")
            require(not self.present(),"LIFE_HISTORY_PRESENT_VISITOR")
            def work(state):
                with self.generation(state) as g:
                    g.finish();state["terminal"]=g.terminal_handoff()
                    return {"terminal_digest":digest(state["terminal"])}
            return self.execute(s,"HISTORICAL_TERMINAL",work,next_mode="LIVE")

    @contextmanager
    def live(self,visitor=None):
        session=LiveTurnSession(self.rt,self.live_provider,self.directory/"live.sqlite",
                                sourcefree_attested=True)
        try:
            yield session if visitor is None else session.bind_neighbor(visitor,mii_module=self.mii)
        finally:session.close()

    def configure_encounter(self,visitor,conditions,*,request_id):
        # Research operator only; never a human-facing grant of access.
        with self.lock():
            s=self.ready("LIVE")
            def work(_):
                with self.live(visitor) as n:
                    return n.install_sourcefree_conditions(conditions,request_id=request_id)
            return self.execute(s,"SOURCEFREE_ENCOUNTER_CONDITIONS",work,refusal_is_local=True)

    def contribute(self,visitor,request_id,operation,**kwargs):
        with self.lock():
            s=self.ready("LIVE")
            def work(_):
                with self.live(visitor) as n:
                    return n.contribute(request_id,operation,**kwargs)
            return self.execute(s,"ACTUAL_VISITOR_CONTRIBUTION",work,refusal_is_local=True)

    def profile_path(self,visitor):
        require(text(visitor,120),"LIFE_VISITOR_ID")
        return self.directory/("mii-"+digest(visitor)+".json")

    def present_until(self,visitor,occasion_ref,target_clock,*,max_beats=24):
        with self.lock():
            s=self.ready("LIVE")
            require(self.present(),"LIFE_NO_PRESENT_VISITOR")
            def work(_):
                with self.live(visitor) as n:
                    path=self.profile_path(visitor)
                    profile=n.load_private_profile(path)
                    out=n.continue_present_life_until(occasion_ref,target_clock,
                            max_beats=max_beats,profile=profile)
                    n.save_private_profile(path,profile)
                    return out
            return self.execute(s,"PRESENT_INDEPENDENT_LIFE",work)

    def private_surface(self,visitor,*,command=None,target=None):
        # Same finite MII sidecar and native reader; no actor history returned.
        with self.lock():
            s=self.ready("LIVE")
            with self.live(visitor) as n:
                out=n.private_surface_stored(self.profile_path(visitor),command=command,target=target)
            require(self.native()==s["expected"],"LIFE_SURFACE_MUTATED_NATIVE")
            return out

    def independent_absent_beat(self):
        with self.lock():
            s=self.ready("LIVE")
            require(not self.present(),"LIFE_USE_PRESENT_OWNER")
            # Persist no second scheduler. The live epoch already has a
            # qualified terminal boundary; an actual later departure opens
            # a new absent interval. Recover counts from the native ledger.
            require(s["terminal"] is not None,"LIFE_MISSING_TERMINAL")
            origin=s["terminal"]["state"]["clock"]
            w=self.rt.ledger.world(self.rt.world_id)[1]
            departures=[e["clock"] for e in w.get("neighbor_user_events",[])
                        if e.get("operation")=="LEAVE" and e.get("status")=="PERFORMED"
                        and type(e.get("clock")) is int and origin<=e["clock"]<=w["clock"]]
            origin=max([origin,*departures])
            def work(_):
                with self.live() as session:
                    return session.continue_independent(interval_origin=origin)
            return self.execute(s,"ABSENT_INDEPENDENT_BEAT",work)

    def resume_history(self):
        with self.lock():
            s=self.ready("LIVE")
            require(not self.present(),"LIFE_VISITOR_STILL_PRESENT")
            require(s["terminal"] is not None,"LIFE_MISSING_TERMINAL")
            link=link_actual_live_interval(self.rt,s["terminal"],self.epoch_path(s["epoch"])/"cycle.json")
            def work(state):
                state["epoch"]+=1;state["link"]=link;state["terminal"]=None
                with self.generation(state) as g:return g.bootstrap()
            return self.execute(s,"RESUMED_HISTORICAL_BOOTSTRAP",work,next_mode="HISTORY")

    def status(self):
        with self.lock():
            s=self.load();actual=self.native()
            return {"grade":GRADE,"mode":s["mode"],"epoch":s["epoch"],
                    "expected":s["expected"],"actual":actual,
                    "pending":s["pending"],"held":s["pending"] is not None or actual!=s["expected"]}

    def receipts(self):
        with self.lock():
            return [{"id":i,**json.loads(r)} for i,r in self.db.execute("SELECT id,body FROM attempts ORDER BY id")]

    def close(self):self.db.close()
