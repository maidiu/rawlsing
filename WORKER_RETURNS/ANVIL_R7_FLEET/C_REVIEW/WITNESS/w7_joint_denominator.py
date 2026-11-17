#!/usr/bin/env python3
"""Independent arithmetic witness: one- and two-way marginals cannot distinguish
even/odd three-way support, and forward/reverse conditional denominators differ.
Not a project consumer; a minimal scientific distinction for the C review."""
import collections, json
even=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
odd=[(1,1,1),(0,0,1),(0,1,0),(1,0,0)]
def margins(rows):
    n=len(rows); uni=[collections.Counter(r[i] for r in rows) for i in range(3)]
    pair={(i,j):collections.Counter((r[i],r[j]) for r in rows) for i,j in ((0,1),(0,2),(1,2))}
    triple=collections.Counter(rows)
    return {'n':n,'univariate':[{str(k):v for k,v in x.items()} for x in uni],'pairwise':{f'{i}{j}':{str(k):v for k,v in c.items()} for (i,j),c in pair.items()},'p111':triple.get((1,1,1),0)/n}
# forward P(Y=1|D=1) and reverse P(D=1|Y=1) on a toy 2-way table
# rows: (Y,D) counts
table={(1,1):3,(1,0):2,(0,1):1,(0,0):4}
fwd=table[(1,1)]/sum(v for (y,d),v in table.items() if d==1)
rev=table[(1,1)]/sum(v for (y,d),v in table.items() if y==1)
report={
 'even':margins(even),'odd':margins(odd),
 'marginals_equal':margins(even)['univariate']==margins(odd)['univariate'] and margins(even)['pairwise']==margins(odd)['pairwise'],
 'p111_even':margins(even)['p111'],'p111_odd':margins(odd)['p111'],
 'forward_P_Y1_given_D1':fwd,'reverse_P_D1_given_Y1':rev,
 'forward_denominator_nD1':sum(v for (y,d),v in table.items() if d==1),
 'reverse_denominator_nY1':sum(v for (y,d),v in table.items() if y==1),
 'negative':'NOT_ASKED/UNKNOWN_ROUTING must not be coerced to zero; missing code 9 is not a substantive 0.'
}
print(json.dumps(report,indent=2))
