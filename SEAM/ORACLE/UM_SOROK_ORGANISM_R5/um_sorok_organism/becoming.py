"""TCO R4: replaceable, actor-specific lived-difference and relational genesis.

No scalar psychological conservation, fixed ends, clinical theories or invented
past events. A single experience is an open trace; repeated *contrasts* may
qualify an orientation, not an explanation, diagnosis or completed competence.
Historical proposals remain provisional and source-bound. Independent Others'
world histories never become actor memories through this module.
"""
from .types import stable_id,copy,GRADE

MECHANISM='TCO_R4_LIVED_DIFFERENCE@1'


class LivedDifferenceKernel:
    version=MECHANISM

    def mark_attention(self,actor,cues):
        """Only annotate already accessible cues, never manufacture or expose them."""
        out=copy(cues)
        for cue in out:
            tags={str(t).lower() for t in cue.get('tags',[])+[cue.get('kind','')]}
            refs=[v['id'] for v in actor.get('nonconceptual_orientations',{}).values()
                  if tags & set(v['cue_terms'])]
            if refs:cue['actor_attention_refs']=sorted(refs)
        return out

    def register_preconceptual(self,actor,experience,clock):
        """Finite-body, pre-verbal co-regulatory pattern, no adult emotion installed.

        Repeated independently supported care *with actor's own somatic
        settling* may change which coactor-present cues later draw attention.
        Neither attachment nor consent nor a caregiver's love is inferred.
        """
        if experience.get('actor')!=actor['id']:
            raise ValueError('PRECONCEPTUAL_ACTOR_MISMATCH')
        partner=experience.get('reciprocated_partner')
        bodily=experience.get('interoceptive_change') or []
        if not partner or 'SETTLING_PROXY' not in bodily:
            return []
        history=actor.setdefault('nonconceptual_events',[])
        row={'event':experience['ref'],'clock':clock,'coactor':partner,
             'somatic_signature':'SETTLING_PROXY',
             'actor_access':'NONDECLARATIVE_BODILY_PROXY'}
        if any(e['event']==row['event'] for e in history):
            raise ValueError('PRECONCEPTUAL_DUPLICATE_EXPERIENCE')
        history.append(row)
        qualified=[e for e in history if e['coactor']==partner]
        if len(qualified)<2:return []
        ident=stable_id('orientation',{'actor':actor['id'],'other':partner,
                                        'kind':'SOMATIC_CONTINGENCY'})
        orientation={'id':ident,'actor':actor['id'],'other':partner,
            'cue_terms':['coactor',partner.lower()],
            'source_experience_refs':[e['event'] for e in qualified],
            'function':'NONCONCEPTUAL_ATTENTION_ORIENTATION',
            'not_attachment_or_other_intention':True,
            'version':self.version,'grade':GRADE}
        old=actor.setdefault('nonconceptual_orientations',{}).get(ident)
        actor['nonconceptual_orientations'][ident]=orientation
        return [] if old==orientation else [{'kind':'NONCONCEPTUAL_SOMATIC_CUE_ORIENTATION',
                'orientation':ident,'source_experience_refs':orientation['source_experience_refs']}]

    def register(self,actor,experience,lived,clock):
        """Actor's actual experienced participation differentiates future salience.

        Keep source episodes append-only, form contrast hypotheses only when
        two distinct actor-experienced courses exist for SAME project/operation.
        A contrast is not an inferred frustration, inhibition or causation.
        """
        if actor['id']!=experience.get('actor'):
            raise ValueError('BECOMING_ACTOR_IDENTITY_MISMATCH')
        changes=[]
        for row in lived:
            if row.get('actor')!=actor['id'] or row.get('experience_ref')!=experience['ref']:
                raise ValueError('BECOMING_FOREIGN_EXPERIENCE')
            key=stable_id('course',{'actor':actor['id'],'project':row['project'],
                                     'action':row['attempted_operation']})
            cluster=actor.setdefault('lived_course_series',{}).setdefault(key,{
                'id':key,'project':row['project'],'operation':row['attempted_operation'],
                'actor':actor['id'],'episodes':[],'grade':GRADE})
            if any(x['event']==row['event'] for x in cluster['episodes']):
                raise ValueError('BECOMING_DUPLICATE_EVIDENCE')
            episode={'event':row['event'],'experience_ref':row['experience_ref'],
                     'clock':clock,'somatic_course':row['somatic_course'],
                     'accessible_cue_tags':copy(row['accessible_cue_tags']),
                     'actor':actor['id']}
            cluster['episodes'].append(episode)
            kinds={e['somatic_course'] for e in cluster['episodes']}
            # Both episodes actually lived by this actor; no omniscient cause.
            if len(kinds)>=2:
                evidence=cluster['episodes']
                ref=stable_id('difference',{'actor':actor['id'],'series':key})
                # A contrast exists across multiple episodes, but its content
                # is deliberately undetermined rather than an LLM's motive.
                acquired=actor.setdefault('acquired_discriminations',{})
                old=acquired.get(ref)
                new={'id':ref,'actor':actor['id'],'series':key,'project':row['project'],
                     'operation':row['attempted_operation'],
                     'courses':sorted(kinds),'origin_events':[e['event'] for e in evidence],
                     'accessible_cue_tags':sorted({tag for e in evidence
                                                  for tag in e['accessible_cue_tags']}),
                     'function':'DIFFERENTIATE_PRACTICAL_EXPECTATION',
                     'interpretation':'OPEN_NOT_CAUSALLY_EXPLAINED',
                     'acquired_not_preinstalled':True,'version':self.version,'grade':GRADE}
                acquired[ref]=new
                if old!=new:
                    changes.append({'kind':'ACQUIRED_DIFFERENCE_IN_ENACTMENT',
                                    'discrimination':ref,'origin_events':new['origin_events'],
                                    'no_inferred_motive':True})
        return changes

    def orient(self,const,access):
        """Actor-conditional orientation derived from *accessible* cue tags.

        Perceivability remains world/sensor-owned; attention is differentiated
        after access but before form matching and action prospect formation.
        """
        observed={str(t).lower() for c in access.cues
                  for t in c.get('tags',[])+[c.get('kind','')]}
        currents=[];matching=[]
        for orient in const.nonconceptual_orientations.values():
            if orient['actor']!=const.actor:continue
            hits=sorted(set(orient['cue_terms'])&observed)
            if hits and any(orient['id'] in c.get('actor_attention_refs',[]) for c in access.cues):
                currents.append({'kind':'NONCONCEPTUAL_ACQUIRED_ORIENTATION',
                     'ref':orient['id'],'matched_accessible_tags':hits,
                     'origin_experiences':copy(orient['source_experience_refs']),
                     'not_conscious_named_affect':True,'version':self.version})
        for d in const.acquired_discriminations.values():
            if d['actor']!=const.actor:continue
            hits=sorted(set(d['accessible_cue_tags'])&observed)
            if hits:
                entry={'kind':'HISTORY_CONDITIONED_ATTENTION','ref':d['id'],
                       'project':d['project'],'operation':d['operation'],
                       'matched_accessible_tags':hits,'origin_events':copy(d['origin_events']),
                       'not_a_conscious_explanation':True,'version':self.version}
                currents.append(entry);matching.append(d)
        return currents,matching

    def propose_second_order(self,actor,experience,participations):
        """Generate a practice hypothesis from an actor's *own* event sequence.

        A triplet INTERRUPTED(A)->CONTINUED(B)->CONTINUED(A) in one project
        is sufficient for a *candidate organizing method* only, never a causal
        inference that B enabled A. Two independent triplets are required to
        admit the practice as an executable method. No mature fixed ontology.
        """
        changes=[]
        for row in participations:
            if row['somatic_course']!='CONTINUED':continue
            project=row['project'];action=row['attempted_operation']
            episodes=[e for e in actor.get('lived_activity_history',[])
                      if e['project']==project and e['actor']==actor['id']]
            if len(episodes)<3:continue
            last=episodes[-1]
            if last['experience_ref']!=experience['ref']:continue
            # A, B, A is a historically observed sequence, not arbitrary opcode pair.
            first,mid=episodes[-3:-1]
            if (first['attempted_operation']!=action or
                first['somatic_course']!='INTERRUPTED' or
                mid['attempted_operation']==action or
                mid['somatic_course']!='CONTINUED'):
                continue
            pair=(mid['attempted_operation'],action)
            p=next((x for x in actor['projects'] if x['id']==project),None)
            if not p or not set(pair).issubset(p.get('means',[])):continue
            # The original R4 association would also learn SING-before-REPAIR
            # when an unseen fixture replenished stock between the actions.
            # Confront the world-owner feasibility record: a blocked material
            # requirement, a distinct operation that actually improved it,
            # and a subsequently feasible retry in the SAME material field.
            # This checks objective support, NOT subjective recognition or a
            # scientific causal law of why the organism selected its practice.
            audits=actor.get('activity_history',[])
            def objective_life(episode):
                return next((h for h in audits if h['event']==episode['event']
                     and h['project']==project and
                     h['operation']==episode['attempted_operation']),None)
            f,m,l=(objective_life(e) for e in (first,mid,last))
            if not (f and m and l):continue
            failure=[r for r in f.get('object_transformation',{}).get('affordance_requirements',[])
                     if not r['satisfied']]
            intermediate=m.get('object_transformation',{}).get('affordance_changes',[])
            recovered=l.get('object_transformation',{}).get('affordance_requirements',[])
            materially_supported=any(
                effect['path']==needed['path'] and effect['delta']>0 and
                effect['after']>=needed['required_at_least'] and
                any(r['path']==needed['path'] and r['satisfied'] for r in recovered)
                for needed in failure for effect in intermediate)
            if not materially_supported:continue
            if not all(e.get('accessible_cue_tags') for e in (first,mid,last)):
                # No fictional acquisition from an inaccessible material chain.
                continue
            ident=stable_id('provisional_method',{'actor':actor['id'],
                         'project':project,'steps':pair})
            record=actor.setdefault('historical_method_candidates',{}).setdefault(ident,{
                    'id':ident,'actor':actor['id'],'project':project,
                    'operations':list(pair),'triplets':[],
                    'claim':'REPEATED_LIVED_SEQUENCE_WITH_WORLD_AFFORDANCE_SUPPORT_NOT_CAUSAL_CERTAINTY',
                    'version':self.version})
            triplet=[e['event'] for e in (first,mid,last)]
            if triplet not in record['triplets']:record['triplets'].append(triplet)
            # Distinct triplets must not recycle one event as proof twice.
            flat=[a for seq in record['triplets'] for a in seq]
            disjoint_evidence=len(record['triplets'])>=2 and len(flat)==len(set(flat))
            if disjoint_evidence and ident not in actor.setdefault('historical_composition_methods',{}):
                method={'id':ident,'actor':actor['id'],'project':project,
                    'operations':list(pair),'source_events':copy(record['triplets']),
                    'hypothesized_end':'try an encountered alternative before retrying '+action,
                    'status':'ACTIVE','meaning':'ACQUIRED_PROCEDURAL_ASSOCIATION_NOT_CAUSAL_CERTAINTY',
                    'origin_grade':'HISTORICALLY_REPEATED_LIVED_AND_WORLD_SUPPORTED_PRACTICE',
                    'version':self.version,'grade':GRADE}
                actor['historical_composition_methods'][ident]=method
                changes.append({'kind':'HISTORY_GENERATED_COMPOSITION_METHOD','method':ident,
                                'source_events':copy(record['triplets']),
                                'not_inferred_universal_learning_law':True})
        return changes
