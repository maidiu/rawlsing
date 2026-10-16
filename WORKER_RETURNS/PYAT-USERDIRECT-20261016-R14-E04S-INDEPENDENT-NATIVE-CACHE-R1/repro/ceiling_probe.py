from common import *
from rawlsing_next.objective_consumer_bounded_evidence import installation_manifest,OC05,evaluate_current_consumer,NotYetApplicableConsumer
m={x['policy_id']:x for x in installation_manifest()}
assert m[OC05]['current_applicability']=='NOT_YET_APPLICABLE' and m[OC05]['consumer_seam'] is None
try:evaluate_current_consumer(policy_id=OC05,operation_id='E04S_INDEPENDENT_COURT',inputs=(),requested_claim_ceiling='OBJECTIVE_FACT',partial_allowed=False)
except NotYetApplicableConsumer as e:refusal=dict(type=type(e).__name__,message=str(e))
else:raise AssertionError('OC05 unexpectedly operative')
dump('actual_OC05_ceiling.json',dict(manifest=m,direct_refusal=refusal,operative_OC05=False,adoption=False,real_source_rights=False));print('ACTUAL_OC05_NOT_YET_APPLICABLE__SEAM_NONE__DIRECT_REFUSAL')
