"""SC0F3 entrypoint: native owner computation and active scope/use gates."""
import copy
import datetime
from .common import Hold, digest, require, semantic_selection
from . import producer,fixture_owner
from .gates import validate
from .receipts import build,verify


class TwoContractAdapter:
    def __init__(self,provider):
        self.provider=provider
        self._prior=None

    def _permission(self,selection):
        for atom in ('WORLD_READ','POSSIBILITY_QUERY'):
            self.provider.revoked_use(selection,atom)
            if selection:
                c=selection['world']['permission_ceiling']
                require(atom in c['use_atoms'] and atom not in c['revoked_atoms'], 'DENIED_USE','Selected ceiling denies '+atom)

    def run(self,demand=None):
        demand=copy.deepcopy({'scope':'fx:scope:town2008'} if demand is None else demand)
        self._permission(None)
        selection=copy.deepcopy(self.provider.resolve_world_selection(demand))
        self._permission(selection)
        selection=validate(selection,demand,self._prior)
        native=producer.produce(selection['empirical_variant'])
        self._permission(selection)
        require(native['query']['requested_projection']['target_role']=='ANSWER', 'HELD_AUTHORITY','Native target relabelled')
        support=native['support'];cells=support['cells'];denom=support['denominator']
        require(set(cells)=={'yes','no'}, 'INTEGRITY_FAILURE','Unrecognized native cells')
        common_support=dict(target_yes=cells['yes'],target_no=cells['no'],denominator=denom,
                            base_ratio=f"{cells['yes']}/{denom}",minority_ratio=f"{cells['no']}/{denom}",
                            risk_set=native['geometry']['denominator']['risk_set_ref'],
                            routing='EXACT_NATIVE_RESPONDENT_ROUTING',weight='UNIT_WEIGHT',uncertainty='EXACT_FIXTURE_NOT_POPULATION_INFERENCE')
        effects={}
        specs={
            'CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY':['fx:rule:public_access_2008','fx:rule:mutual_aid','fx:r:public','fx:r:mutual','fx:AH'],
            'NONPARENT_APPRENTICESHIP_ENTRY':['fx:rule:public_access_2008','fx:rule:mutual_aid','fx:r:public','fx:r:mutual'],
        }
        selected_values={**selection['world']['values'],**selection['world']['routes']}
        for cid,keys in specs.items():
            self._permission(selection)
            values=self.provider.read_values(selection,keys)['values']
            require(values=={k:selected_values[k] for k in keys}, 'REJECT_UNVERIFIABLE_CONSUMER_USE','Reader did not read selected values')
            routes=[dict(route=k,route_values=values[k]['values'],availability=values[k]['availability'],
                         rule=values[values[k]['rule_ref']]) for k in ('fx:r:public','fx:r:mutual')]
            if cid.startswith('CONCEPTION'):
                output=dict(eligible_scenario_constraints=routes,absolute_horizon=values['fx:AH'],
                            minority_alternatives=['no'],empirical_support=copy.deepcopy(common_support))
            else:
                output=dict(apprenticeship_access_routes=routes,empirical_support=copy.deepcopy(common_support))
            effects[cid]=dict(consumer_id=cid,output=output,values_read=values,person_generation='NONE')
        self._permission(selection)
        possibility=dict(universe=native['query']['source_universe_ref']['object_id'],
                         release=native['query']['release_ref']['object_id'],target='ANSWER',direction='FORWARD_CONDITIONAL',
                         sampling_unit='RESPONDENT',support=common_support,
                         cells=[dict(value=c['cell'],n=c['raw_numerator_support']) for c in native['geometry']['cells']],
                         # One actual conditioned native query. Do not pretend
                         # the old unrelated 60->30->12 hints were executed.
                         ordered_condition_chain=[dict(index=0,ref=native['query']['conditioner_bindings'][0]['binding_id'],n=denom)],
                         minority='no',routing='EXACT_NATIVE_RESPONDENT_ROUTING',risk_set='R_ALL_100',
                         weight='UNIT_WEIGHT',model_use='TEST_ONLY',uncertainty='EXACT_FIXTURE_NOT_POPULATION_INFERENCE')
        bundle=build(selection,native,effects,possibility)
        self._permission(selection)
        self._prior=copy.deepcopy(selection)
        return bundle

    def request_role_reversal(self,grant=None):
        self._permission(None)
        selection=self.provider.resolve_world_selection({'scope':'fx:scope:town2008'})
        self._permission(selection)
        validate(selection,selection['demand'],self._prior)
        expected=fixture_owner.check_reversal(grant,selection['world'],selection['empirical_variant'],
                                              datetime.date.today().isoformat())
        native=producer.produce(selection['empirical_variant'],'reverse')
        self._permission(selection)
        require(native['support']['denominator']==expected['denominator'] and native['query']['requested_projection']['target_role']==expected['target'],
                'HELD_AUTHORITY','Reverse geometry differs from closed fixture warrant')
        require(native['query']['source_universe_ref']==expected['native_source']
                and native['query']['release_ref']==expected['native_release']
                and native['query']['target_ref']==expected['native_target']
                and native['geometry']['denominator']['risk_set_ref']==expected['native_risk'],
                'HELD_AUTHORITY','Reverse native source/release/target/risk differs from warrant')
        return dict(state='TEST_ONLY_NATIVE_REVERSE_QUERY_COMPUTED',issuer_fixture=expected,
                    computed_from_forward=False,native_computation=native)

    def request_actor_weld(self,*args,**kwargs):
        raise Hold('REFUSE_UNGRANTED_ACTOR_USE','No actor operation authorized')


def provider_equivalence_report(a,b):
    verify(a);verify(b)
    # Complete receipt/carrier/effect content is included. Physical fields occur
    # only in the normalized selection snapshot; they are already excluded there.
    return dict(equivalent_except_physical_lineage=a==b)
