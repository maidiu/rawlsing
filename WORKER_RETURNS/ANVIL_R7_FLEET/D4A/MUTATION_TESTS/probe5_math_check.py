#!/usr/bin/env python3
"""Constructed probe-5 witness. Not historical/native execution."""
from itertools import product
from collections import Counter

# Same univariate/pairwise margins, different 3-way tables (parity-even vs parity-odd).
A = {(0,0,0):10,(0,1,1):10,(1,0,1):10,(1,1,0):10}
B = {(0,0,1):10,(0,1,0):10,(1,0,0):10,(1,1,1):10}
def table(d): return {k:d.get(k,0) for k in product((0,1),repeat=3)}
def margins(d):
    out={}
    for i in range(3):
        for v in (0,1):
            out[f'X{i+1}={v}']=sum(c for k,c in d.items() if k[i]==v)
    for i,j in ((0,1),(0,2),(1,2)):
        for a,b in product((0,1),repeat=2):
            out[f'X{i+1}{j+1}={a}{b}']=sum(c for k,c in d.items() if k[i]==a and k[j]==b)
    return out
TA,TB=table(A),table(B)
print('A cells',TA)
print('B cells',TB)
print('A margins',margins(TA))
print('B margins',margins(TB))
print('margins_equal',margins(TA)==margins(TB))
print('cell_tables_equal',TA==TB)
# Equal numeric denominator sizes with different population definitions.
# Universe U: 8 respondents; D=A members {r1..r4}; Y=1 members {r1,r2,r5,r6}.
U=['r1','r2','r3','r4','r5','r6','r7','r8']
D_A={'r1','r2','r3','r4'}
Y1={'r1','r2','r5','r6'}
p_y_given_da=len(D_A & Y1)/len(D_A)
p_da_given_y=len(D_A & Y1)/len(Y1)
print('denominator P(Y=1|D=A)=',len(D_A),'P(D=A|Y=1)=',len(Y1),
      'numerators=',len(D_A & Y1),'values=',p_y_given_da,p_da_given_y,
      'numeric_equal=',p_y_given_da==p_da_given_y,'same_denominator_membership=',D_A==Y1)
