from common import *
from rawlsing_next.pre553_empirical_objects import ExactRef
s,ss,a,b=full();s.provider.world['source']['risk_refs']['R']=ExactRef('RISK_SET','urn:e04t:foreign-risk','b'*64)
for label,call in [('nonparent',lambda:consume(s,ss)),('scenario',lambda:evaluate(s,ss,PROPOSALS)),('provider',lambda:s.provider.step('Y',(('A',1),)))]:
 try:call()
 except ValueError as e:print(label,repr(str(e)))
 else:raise AssertionError('risk rekey unexpectedly permitted')
