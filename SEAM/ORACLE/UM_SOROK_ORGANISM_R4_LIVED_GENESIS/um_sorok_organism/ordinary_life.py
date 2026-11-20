"""Low-cost historical density with **no fictitious microevent receipts**."""
from .types import stable_id, GRADE, copy
from .organism import mature


def passage(world,actors,days,processes=None):
    if not isinstance(days,int) or days<1 or days>3650:raise ValueError('UNSUPPORTED_TIME_PASSAGE')
    processes=copy(processes or [])
    start=world['clock']
    for a in actors.values():
        mature(a,days)
        # Coarse physiology with explicit modeling grade; one period cannot assert meals.
        b=a['body']
        b['nutrition']=round(max(.12,b['nutrition']-.0008*days),4)
        b['rest']=round(max(.15,b['rest']-.00035*days),4)
    world['clock']+=days
    period={'id':stable_id('period',{'world':world['id'],'start':start,'days':days,'processes':processes}),
       'start':start,'end':world['clock'],'resolution':'AGGREGATE_MODELED',
       'processes':processes,'cannot_warrant':'UNRECORDED_SPECIFIC_OCCURRENCE',
       'grade':GRADE}
    world['historical_periods'].append(period)
    return period
