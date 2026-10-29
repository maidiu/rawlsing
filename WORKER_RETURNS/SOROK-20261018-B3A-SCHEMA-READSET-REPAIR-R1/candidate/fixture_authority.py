"""Closed synthetic fixture registrar, deliberately outside the response engine.

A trusted test author can register observations. Hashes authenticate no real world,
user, actor or production issuer. The responder cannot register its own proposal.
"""
from copy import deepcopy
from sources import m2
class FixtureAuthority:
 def __init__(self):self._frames=set()
 def register_observed(self,frame):
  # Exclude analyst requests, keep exact evidence/speaker/exposure source bytes.
  self._frames.add(self.binding(frame))
 @staticmethod
 def binding(frame):
  return m2.digest(dict(source={k:deepcopy(frame[k]) for k in ('event','actors','evidence','utterances','exposures')},origin_event_id=frame.get('origin_event_id')))
 def permits(self,frame):return self.binding(frame) in self._frames
