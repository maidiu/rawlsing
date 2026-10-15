"""Active, candidate-owned gates; no frozen oracle outcome is returned as law."""
import copy
import re
from collections.abc import Mapping
from .common import require, digest
from .fixture_owner import fixture_world, source_catalog, check_earlier_knowledge


def calendar_cut(value):
    require(isinstance(value,str) and re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?',value),
            'NO_CURRENT_OR_NOT_KNOWN_ASOF', 'Unrecognized clock')
    import datetime
    parts=[int(x) for x in value.split('-')]
    try:
        return datetime.date(*(parts+[1]*(3-len(parts))))
    except ValueError:
        require(False, 'NO_CURRENT_OR_NOT_KNOWN_ASOF', 'Invalid calendar date')


def validate(selection,demand,prior=None):
    require(selection.get('selection_state') == 'COMPLETE', 'INCOMPLETE_SELECTION_NOT_POSITIVE', 'Explicit COMPLETE required')
    w=selection['world'];base=fixture_world()
    require(all(k in w for k in base), 'REJECT_SEMANTIC_LOSS', 'Required source world field absent')
    known={'scope','source','release','native_unit','strata','as_of','mode','temporal_operation','sampling_unit','target'}
    require(set(demand)<=known, 'DEMAND_CLOSURE_INCOMPLETE', 'Unrecognized demand criterion')
    catalog=[row for row in source_catalog() if row[:2]==(w['source_ref'],w['source_release_ref'])]
    require(len(catalog)==1, 'DEMAND_CLOSURE_INCOMPLETE', 'Unissued source/release catalog')
    source,release,scope,unit,strata=catalog[0]
    require(demand.get('scope',scope)==scope and demand.get('source',source)==source
            and demand.get('release',release)==release and demand.get('native_unit',unit)==unit,
            'DEMAND_CLOSURE_INCOMPLETE', 'Demand source/release/scope/unit unavailable')
    require(w['native_unit']==unit and set(w['native_strata'])==set(strata),
            'DEMAND_CLOSURE_INCOMPLETE', 'Native strata incomplete')
    requested=demand.get('strata',list(strata))
    require(isinstance(requested,list) and requested and set(requested)<=set(strata),
            'DEMAND_CLOSURE_INCOMPLETE', 'Requested strata unavailable')
    require(all(s in w['values'] and isinstance(w['values'][s],Mapping) and w['values'][s].get('label') for s in strata),
            'DEMAND_CLOSURE_INCOMPLETE', 'Native strata not dereferenceable')
    require(len({w['values'][s]['label'] for s in strata})==len(strata),
            'REJECT_NONINJECTIVE_COORDINATE', 'Stratum mapping collapsed')
    require(w['absolute_horizon'] in w['values'], 'REJECT_SEMANTIC_LOSS', 'Absolute horizon absent')
    require(w['epistemic_grade']=='TEST_FIXTURE_ONLY', 'REJECT_EPISTEMIC_PROMOTION', 'Sourcefree ceiling')
    from port.contracts import PSYCHIC_TOKENS
    forbidden=(*PSYCHIC_TOKENS,'ACTOR_STATE','PARENT_OBJECT','PARTNER_SELECTION','LEARNER_PSYCHE')
    require(not any(t in repr(w).upper() for t in forbidden),
            'REJECT_ACTOR_JURISDICTION', 'Actor/person fields outside this interface')
    require(demand.get('temporal_operation') is None, 'HELD_AUTHORITY', 'No temporal interpolation grant')
    require(demand.get('sampling_unit',unit)==unit, 'REFUSE_SAMPLING_UNIT_JOINT', 'No cross-unit pooling')
    require(demand.get('target','ANSWER')=='ANSWER', 'HELD_AUTHORITY', 'Forward target not authorized')
    axes=w['time_axes']
    require(set(axes)==set(base['time_axes']), 'NO_CURRENT_OR_NOT_KNOWN_ASOF', 'Four clock families required')
    for v in axes.values():calendar_cut(v)
    asof=demand.get('as_of',axes['as_of']);calendar_cut(asof)
    require(demand.get('mode',w['clock_mode'])==w['clock_mode']=='KNOWLEDGE_AS_OF',
            'NO_CURRENT_OR_NOT_KNOWN_ASOF','Unsupported clock mode')
    if calendar_cut(axes['published'])>calendar_cut(asof):
        check_earlier_knowledge(w,w.get('earlier_knowledge_evidence_ref'),asof)
    # The actual requested knowledge cut, not a provider label, is carried out.
    w['time_axes']['as_of']=asof
    n=w['nary'];f2=w['f2']
    require(n==base['nary'], 'REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS', 'Native F1 roles/cardinality/order changed')
    require(f2==base['f2'] and w['f1_refs']==base['f1_refs'] and w['f2_requirement_ref']==base['f2_requirement_ref'],
            'REJECT_F2_PREREQUISITE_LOSS', 'F2 prerequisite/deferral changed or replaced by F1')
    require(w['public_categories']==base['public_categories'] and w['public_sanctions']==base['public_sanctions'],
            'REJECT_PUBLIC_RULE_AND_OWNER_LOSS', 'Public category/sanction erased')
    require(set(w['routes'])==set(base['routes']), 'REJECT_PUBLIC_RULE_AND_OWNER_LOSS', 'Native route lost')
    for key,route in w['routes'].items():
        require(route.get('epistemic_grade') in (None,'TEST_FIXTURE_ONLY'),
                'REJECT_EPISTEMIC_PROMOTION', 'Route fixture promoted to observation')
        require(route.get('sanction_refs')==base['routes'][key]['sanction_refs']
                and route.get('category_refs')==base['routes'][key]['category_refs']
                and route.get('rule_ref')==base['routes'][key]['rule_ref'],
                'REJECT_PUBLIC_RULE_AND_OWNER_LOSS', 'Native route rule/category/sanction owner lost')
        require(isinstance(w['values'].get(route['rule_ref']),Mapping),
                'REJECT_UNVERIFIABLE_CONSUMER_USE', 'Readable public rule absent')
    require(w['contradictory_alternatives']==base['contradictory_alternatives'],
            'REJECT_ALTERNATIVE_ERASURE', 'Contradictory alternative erased')
    # The structural world's support remains independent of empirical results.
    require(w['support']==base['support'], 'REJECT_SUPPORT_ERASURE', 'Structural fixture support mutated')
    require(w['negative_states']==base['negative_states'], 'REJECT_NEGATIVE_ALGEBRA_LOSS', '12 native negatives changed')
    echo=w['generated_binding_echo']
    require(echo.get('channel')=='H3_GENERATED_BINDING_ECHO_FILTER_ONLY' and echo.get('upstream_authorship') is False,
            'REJECT_GENERATED_FACT_PROMOTION','H3 is filter echo only')
    if prior is not None:
        old=prior['world']
        if old['generated_binding_echo']!=echo:
            require(selection['binding_generation']>prior['binding_generation'], 'REJECT_STALE_BINDING_CONTEXT', 'Unmarked binding drift')
        changed=(old['source_release_ref'],old['time_axes']['published'])!=(w['source_release_ref'],axes['published'])
        require(changed==(selection['publication_generation']>prior['publication_generation']),
                'REJECT_STALE_REPOSITORY_CONTEXT', 'Publication counter/boundary drift')
    return selection
