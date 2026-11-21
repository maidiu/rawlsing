from um_sorok_organism.types import adult, blank_world
from um_sorok_organism.constitution import compose, materialize, actor_access
from um_sorok_organism.world import add_cue
a=adult('amy','Amy')
for n in ('a','b','c'):
    a['forms'][n]={'id':n,'actor':'amy','kind':'PRACTICE','origin':['e_'+n],
        'cues':['encounter'],'enables':['SING'],'strength':.6,'body_min':0,
        'lifecycle':'ACTIVE','scope':{}}
a['links']=[{'source':'a','target':'b','relation':'INHIBITS','contexts':[]},
            {'source':'b','target':'c','relation':'INHIBITS','contexts':[]},
            {'source':'c','target':'a','relation':'INHIBITS','contexts':[]}]
w=blank_world(); w['positions']={'amy':'home'}; add_cue(w,'bell',['encounter'],location='home')
s=compose(materialize(a,w),actor_access(a,w))
print('recruited',[f['id'] for f in s.recruited])
print('inhibited',s.inhibited)
print('actions',[x['action'] for x in s.candidate_actions])
