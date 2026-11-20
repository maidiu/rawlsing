"""Low-cost historical density with **no fictitious microevent receipts**."""
from .types import stable_id, GRADE, copy
from .organism import mature
from .material_objects import advance_material_wear


def passage(world,actors,days,processes=None):
    if type(days) is not int or days<1 or days>3650:raise ValueError('UNSUPPORTED_TIME_PASSAGE')
    processes=copy(processes or [])
    start=world['clock']
    for a in actors.values():
        mature(a,days)
        # Coarse physiology with explicit modeling grade; one period cannot assert meals.
        b=a['body']
        b['nutrition']=round(max(.12,b['nutrition']-.0008*days),4)
        b['rest']=round(max(.15,b['rest']-.00035*days),4)
    # The world changes independently of narrated or actor-initiated
    # microevents. Do not manufacture a daily series of fictitious repairs.
    material_wear=advance_material_wear(world,days,start)
    world['clock']+=days
    period={'id':stable_id('period',{'world':world['id'],'start':start,'days':days,'processes':processes}),
       'start':start,'end':world['clock'],'resolution':'AGGREGATE_MODELED',
       'processes':processes,
       'material_object_condition_process_refs':[r['id'] for r in material_wear],
       'cannot_warrant':'UNRECORDED_SPECIFIC_OCCURRENCE',
       'grade':GRADE}
    world['historical_periods'].append(period)
    return period
