"""Immutable source preimages for B3's noncausal M2 research boundary.

This guard does not repair or adopt frozen M2 durable Interpretation semantics.
It refuses rewritten historical sources before re-enumeration.
"""
from dataclasses import asdict
from sources import m2

def preimages(scene):
 records={}
 for a in scene.actors:
  for h in a.history:records['history:'+a.id+':'+h.id]=asdict(h)
 for name,items in [('event',scene.events),('speech',scene.speech),('history_witness',scene.history_witnesses),('speech_action',scene.speech_actions),('exposure',scene.exposures)]:
  for x in items:
   key=(getattr(x,'id',None) or getattr(x,'history_id',None) or getattr(x,'speech_id',None))
   key=name+':'+str(key)+':'+str(getattr(x,'actor',getattr(x,'listener','')))
   if key in records:raise m2.Refusal('SOURCE_IDENTITY_COLLISION')
   records[key]=asdict(x)
 return records

def check(earlier,scene):
 current=preimages(scene)
 for key,value in current.items():
  if key in earlier and m2.canonical(earlier[key])!=m2.canonical(value):raise m2.Refusal('SOURCE_PREIMAGE_IDENTITY_COLLISION')
 return current
