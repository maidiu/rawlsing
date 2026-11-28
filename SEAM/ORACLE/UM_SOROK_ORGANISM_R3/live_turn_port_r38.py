"""One-response sourcefree live turn over the existing CO and NEIGHBOR owners.

No new world writer or visitor surface. The owner chooses the principal and
calls its normal actor-attempt interface. One actual provider response supplies
conditional actor-local policies; subsequent native semantic suboperations
bind fresh offers through the existing generation compiler. This is NOT the
historical developmental checkpoint cadence, native scientific authorization,
or an assertion of actual model adequacy.
"""
from collections import Counter
import fcntl
import json
from pathlib import Path
import sqlite3
from time import perf_counter_ns

from modern_generation_port_r28 import ConditionalPolicy, policy_check, require, canonical, digest, detached, exact_keys, text
from um_sorok_organism.semantics import ValidatingSemanticService

GRADE="SOURCEFREE_CONDITIONAL_LIVE_TURN_NOT_MODEL_ADEQUACY"
MAX_PEERS=8
MAX_PACKET=512*1024

class LiveAttemptCustody:
    """Operational metadata only; native ledger remains the state authority.

    An ambiguous/rejected reservation is not silently retried at the same
    exact native state. A subsequent independently committed native event may
    qualify a new turn; no replay of the old proposal or actor action.
    """
    def __init__(self,path,root):
        self.path=Path(path);self.db=sqlite3.connect(self.path)
        self.db.execute("CREATE TABLE IF NOT EXISTS binding (root TEXT PRIMARY KEY)")
        rows=self.db.execute("SELECT root FROM binding").fetchall()
        if not rows:self.db.execute("INSERT INTO binding VALUES (?)",(root,))
        else:require(rows==[(root,)],"LIVE_CUSTODY_FOREIGN_ROOT")
        self.db.execute("CREATE TABLE IF NOT EXISTS turns (source TEXT PRIMARY KEY,receipt TEXT NOT NULL)")
        self.db.commit()
    def reserve(self,source,row):
        require(not self.db.execute("SELECT 1 FROM turns WHERE source=?",(source,)).fetchone(),
                "LIVE_PREVIOUS_ATTEMPT_REQUIRES_DISPOSITION")
        self.db.execute("INSERT INTO turns VALUES (?,?)",(source,canonical(row)));self.db.commit()
    def update(self,source,**changes):
        row=self.db.execute("SELECT receipt FROM turns WHERE source=?",(source,)).fetchone()
        require(row is not None,"LIVE_UNKNOWN_RESERVATION")
        old=json.loads(row[0]);old.update(detached(changes))
        self.db.execute("UPDATE turns SET receipt=? WHERE source=?",(canonical(old),source));self.db.commit()
    def receipts(self):
        return [json.loads(r) for (r,) in self.db.execute("SELECT receipt FROM turns ORDER BY rowid")]
    def close(self):self.db.close()


class OneTurnPolicy:
    """Lazy call at the actual principal selection boundary, not on a user cue.

    Peer tips are separately conditioned current reads, not shared knowledge.
    Only co-present or specifically offered actor targets are included, capped.
    Unrepresented observers may still develop via the existing local policy.
    All subsequent tasks use the existing ConditionalPolicy compiler against
    fresh actual packets. No inference call in the post-settlement phases.
    """
    def __init__(self,runtime,provider,custody,source):
        self.rt=runtime;self.provider=provider;self.custody=custody;self.source=source
        self.policy=None;self.started=False;self.principal=None
        self.grade=GRADE
    def peer_tips(self,principal,packet):
        people=self.rt.ledger.actors()
        w=self.rt.ledger.world(self.rt.world_id)[1]
        loc=w["positions"].get(principal)
        relevant={a for a in people if a!=principal and w["positions"].get(a)==loc}
        for pool in ("practical_options","addressed_lexical_options"):
            for q in packet.get(pool,[]):
                peer=q.get("world_request",{}).get("addressed_party_ref")
                if peer in people and peer!=principal:relevant.add(peer)
        require(len(relevant)<=MAX_PEERS,"LIVE_PEER_SCOPE_REQUIRES_EXPLICIT_QUALIFICATION")
        out={}
        for a in sorted(relevant):
            tip=self.rt.situated(a);own=self.rt.see(a)
            out[a]={"actor":{"id":a,"role":people[a]["role"],"body":people[a]["body"]},
                    "accessible":{k:v for k,v in own.items() if k!="inaccessible_count"},
                    "candidate_actions":tip["candidate_actions"],"recruited":tip["recruited"],
                    "currents":tip["currents"],"inhibited":tip["inhibited"],
                    "antagonisms":tip["antagonisms"],
                    "not_principal_access_or_coactor_consent":True}
        return detached(out)
    def propose(self,task,packet):
        if self.policy is None:
            require(not self.started,"LIVE_REENTRANT_PROVIDER_CALL")
            require(task=="actor_attempt" and packet.get("requesting_actor") is None,
                    "LIVE_NO_PRINCIPAL_SELECTION")
            self.principal=packet.get("actor",{}).get("id")
            require(self.principal in self.rt.ledger.actors(),"LIVE_UNKNOWN_PRINCIPAL")
            # Reserve before any paid call; on invalid context still conserve
            # the held selection occasion. No raw private packet in receipts.
            self.custody.reserve(self.source,{"source":self.source,"principal":self.principal,
                "outcome":"RESERVED","provider_called":False,"grade":GRADE})
            self.started=True;start=perf_counter_ns()
            usage=getattr(self.provider,"usage_snapshot",None)
            before=usage()["total"] if usage else None
            try:
                tips=self.peer_tips(self.principal,packet)
                req={"grade":GRADE,"source":self.source,"principal":self.principal,
                     "principal_packet":detached(packet),"peer_tips":tips}
                n=len(canonical(req).encode("utf-8"))
                self.custody.update(self.source,request_digest=digest(req),request_bytes=n,
                                    peer_count=len(tips))
                require(n<=MAX_PACKET,"LIVE_CONTEXT_BUDGET_HOLD")
                self.custody.update(self.source,provider_called=True)
                result=detached(self.provider.call(req))
                require(self.rt.ledger.latest_event()["chain_hash"]==self.source,"LIVE_PROVIDER_MUTATED_OWNER")
                require(exact_keys(result,("policies",),("private_rehearsal",)) and
                        isinstance(result["policies"],dict),"LIVE_BAD_POLICY_RESPONSE")
                policies=result["policies"]
                require(self.principal in policies and set(policies)<={self.principal,*tips},
                        "LIVE_POLICY_FOREIGN_ACTOR")
                for p in policies.values():policy_check(p)
                rehearsal=None
                if "private_rehearsal" in result:
                    r=result["private_rehearsal"]
                    require(exact_keys(r,("objective_ref","meaning")) and text(r["objective_ref"])
                            and text(r["meaning"]),"LIVE_REHEARSAL_SCHEMA")
                    rows=[q for q in packet.get("private_rehearsal_options",[])
                          if q.get("memory_event_ref")==r["objective_ref"] and q.get("affect_ref") is None]
                    require(len(rows)==1,"LIVE_REHEARSAL_NOT_CURRENTLY_OFFERED")
                    rehearsal={"actor":self.principal,**detached(r)}
                # Only actor-local hypotheses, no generated actual result.
                # Reuse the qualified R61 current private rehearsal carrier.
                self.policy=ConditionalPolicy(policies,rehearsal=rehearsal)
                self.custody.update(self.source,outcome="POLICY_RETURNED",response_bytes=len(canonical(result).encode("utf-8")),
                                    response_digest=digest(result),policy_actor_count=len(policies))
            except BaseException as exc:
                self.custody.update(self.source,outcome="HELD_PROVIDER_OR_POLICY",error_type=type(exc).__name__)
                raise
            finally:
                row={"elapsed_ns":perf_counter_ns()-start}
                if usage:
                    snap=usage()
                    if snap["total"]==before+1 and snap["receipts"]:
                        row["transport_receipt"]={k:detached(v) for k,v in snap["receipts"][-1].items()
                            if k in ("task","transport","attempts","outcome","instruction_bytes",
                                     "packet_bytes","request_bytes","response_content_bytes","usage","elapsed_ns",
                                     "budget_attempt","budget_disposition","wire_packet_bytes","packet_variant",
                                     "alias_count","structured_field_count")}
                self.custody.update(self.source,**row)
        return self.policy.propose(task,packet)


class LiveTurnSession:
    """One ordinary live turn; reuse native independent scheduler and MII.

    Calls to owner_actor_beat are researcher/owner-side, never a user-facing
    target actor selection API. after_user_contribution is the actual visitor
    path. No state cache across turns. Sourcefree serialized operation only;
    lock coordinates this port, not unrelated external native owner writers.
    """
    def __init__(self,runtime,provider,custody_path,*,sourcefree_attested=False):
        require(sourcefree_attested is True,"LIVE_SOURCEFREE_ATTESTATION_REQUIRED")
        require(hasattr(provider,"call"),"LIVE_EXPLICIT_CALL_PROVIDER")
        self.rt=runtime;self.provider=provider
        require(runtime.verify()["valid"],"LIVE_NATIVE_CHAIN_INVALID")
        root=runtime.ledger.events(limit=1)[0]["chain_hash"]
        self.custody=LiveAttemptCustody(custody_path,root)
    def _run(self,operation):
        with self.custody.path.with_suffix(self.custody.path.suffix+".lock").open("a") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            before=self.rt.verify()
            require(before["valid"],"LIVE_NATIVE_CHAIN_INVALID")
            source=before["last_hash"]
            p=OneTurnPolicy(self.rt,self.provider,self.custody,source)
            old=self.rt.semantic;self.rt.semantic=ValidatingSemanticService(p)
            try:
                result=operation()
                after=self.rt.verify()
                require(after["valid"],"LIVE_NATIVE_CHAIN_INVALID")
                count=after["events"]-before["events"]
                require(count in (0,1),"LIVE_MULTIPLE_NATIVE_EVENTS")
                if count==1:
                    require(p.started and p.policy is not None,"LIVE_NATIVE_EVENT_WITHOUT_POLICY")
                    evt=self.rt.ledger.latest_event()
                    require(evt["kind"]=="ACTOR_LIFE_TRANSITION" and evt["actor_id"]==p.principal,
                            "LIVE_NATIVE_EVENT_MISMATCH")
                    self.custody.update(source,outcome="ACTUAL_TURN_COMMITTED",
                        native_receipt=evt["id"],after_hash=after["last_hash"],
                        local_semantic_tasks=dict(p.policy.counts),conditional_routes=dict(p.policy.routes),
                        local_packet_bytes=p.policy.packet_bytes)
                else:require(not p.started,"LIVE_POLICY_WITHOUT_NATIVE_EVENT")
                return result
            except BaseException as exc:
                if p.started:
                    after=self.rt.verify()
                    self.custody.update(source,outcome="HELD_OWNER_OR_PROVIDER",
                        native_events_delta=after["events"]-before["events"],
                        after_hash=after["last_hash"],error_type=type(exc).__name__)
                raise
            finally:self.rt.semantic=old
    def after_user_contribution(self,encounter,*,profile=None):
        require(encounter.runtime is self.rt,"LIVE_FOREIGN_ENCOUNTER")
        if getattr(encounter,"_live_session",None) is self:
            return encounter.continue_independent_life_during_visit(profile=profile)
        return self._run(lambda:encounter.continue_independent_life_during_visit(profile=profile))
    def owner_actor_beat(self,encounter,actor):
        require(encounter.runtime is self.rt,"LIVE_FOREIGN_ENCOUNTER")
        if getattr(encounter,"_live_session",None) is self:return encounter.independent_actor_beat(actor)
        return self._run(lambda:encounter.independent_actor_beat(actor))
    def continue_independent(self):
        return self._run(lambda:self.rt.continue_without_user(beats=1))
    def bind_neighbor(self,user_id,*,mii_module=None):
        """Attach to the existing multi-beat owner without a second scheduler.

        The inherited present-occasion reader decides WHO and when to stop.
        Each native independent beat gets a fresh one-response reservation.
        The inherited MII reader produces actual per-beat surfaces and refuses
        replay; no generation policy or user-supplied actor selection.
        """
        from neighbor_runtime import NeighborEncounter
        session=self
        class BoundNeighbor(NeighborEncounter):
            _live_session=session
            def independent_actor_beat(self,actor_id):
                return session._run(lambda:super(BoundNeighbor,self).independent_actor_beat(actor_id))
        return BoundNeighbor(self.rt,user_id,mii_module=mii_module)

    def close(self):self.custody.close()
