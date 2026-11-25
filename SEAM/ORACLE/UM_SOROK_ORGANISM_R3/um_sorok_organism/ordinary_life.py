"""Low-cost historical density with **no fictitious microevent receipts**."""
from .types import stable_id, GRADE, copy
from .organism import mature
from .material_objects import advance_material_wear
from .mediated_efficacy import conserve_compressed_practice
from .historical_social_reproduction import (
    qualify_period_allocation, apply_period_allocation)


def passage(world,actors,days,processes=None):
    if type(days) is not int or days<1 or days>3650:raise ValueError('UNSUPPORTED_TIME_PASSAGE')
    processes=copy(processes or [])
    start=world['clock']
    # Explicitly 'QUALIFIED_*' material histories require an *entire-actor*
    # budget before any body, world or developmental mutation. Legacy
    # non-time scope-change processes remain governed by their prior reader.
    qualified=[p for p in processes if isinstance(p,dict)
               and type(p.get('kind')) is str and
               p['kind'].startswith('QUALIFIED_')]
    allocation=qualify_period_allocation(
        world,actors,qualified,start,days)
    effective_iter=iter(allocation['qualified'])
    held={p['input_index'] for p in allocation.get('structurally_withheld_processes',[])}
    effective_processes=[];qindex=0
    for p in processes:
        if isinstance(p,dict) and type(p.get('kind')) is str and p['kind'].startswith('QUALIFIED_'):
            if qindex not in held:effective_processes.append(next(effective_iter))
            qindex+=1
        else:effective_processes.append(p)
    practice_evidence=[]
    for a in actors.values():
        # Only a source-qualified ongoing routine can contribute compressed
        # training dose. Merely being alive, aging or having a project never
        # fabricates exercise or silently generates an adult capability.
        for process in effective_processes:
            receipt=conserve_compressed_practice(a,process,start,days)
            if receipt and not receipt.get('already_recorded'):
                practice_evidence.append(receipt['id'])
        mature(a,days)
        # Coarse physiology with explicit modeling grade; one period cannot assert meals.
        b=a['body']
        b['nutrition']=round(max(.12,b['nutrition']-.0008*days),4)
        b['rest']=round(max(.15,b['rest']-.00035*days),4)
    # Time, care, lost rest and received wages are objective parts of
    # historical reproduction. They are not actor self-accounts or thousands
    # of individually witnessed household scenes.
    allocation_receipt=apply_period_allocation(world,actors,allocation)
    # The world changes independently of narrated or actor-initiated
    # microevents. Do not manufacture a daily series of fictitious repairs.
    material_wear=advance_material_wear(world,days,start)
    world['clock']+=days
    period={'id':stable_id('period',{'world':world['id'],'start':start,'days':days,'processes':processes}),
       'start':start,'end':world['clock'],'resolution':'AGGREGATE_MODELED',
       'processes':effective_processes,
       **({'structurally_withheld_processes':copy(allocation_receipt['structurally_withheld_processes'])}
          if allocation_receipt.get('structurally_withheld_processes') else {}),
       'qualified_material_time_allocation_ref':allocation_receipt['id'],
       'care_period_refs':allocation_receipt['care_period_refs'],
       'wage_period_refs':allocation_receipt['wage_period_refs'],
       'material_feeding_period_refs':allocation_receipt[
           'material_feeding_period_refs'],
       'material_feeding_shortfall_refs':allocation_receipt[
           'material_feeding_shortfall_refs'],
       'actor_time_claims':allocation_receipt['actor_hour_claims_per_day'],
       'material_object_condition_process_refs':[r['id'] for r in material_wear],
       'qualified_aggregate_practice_refs':practice_evidence,
       'cannot_warrant':'UNRECORDED_SPECIFIC_OCCURRENCE',
       'grade':GRADE}
    world['historical_periods'].append(period)
    return period
