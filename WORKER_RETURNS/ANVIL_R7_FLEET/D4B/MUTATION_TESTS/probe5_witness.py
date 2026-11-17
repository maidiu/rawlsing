#!/usr/bin/env python3
"""Correct two-distribution witness for GROK probe 5.

A = fully independent X,Y,Z ~ Bernoulli(1/2).
B = X,Y iid Bernoulli(1/2), Z = X XOR Y.
Univariate and every pairwise marginal are identical; the true 3-way joint is
different. All arithmetic is exact (fractions), no sampling.
"""
from fractions import Fraction as F
import itertools

KEYS = list(itertools.product((0, 1), repeat=3))
A = {k: F(1, 8) for k in KEYS}
B = {(0, 0, 0): F(1, 4), (0, 1, 1): F(1, 4),
     (1, 0, 1): F(1, 4), (1, 1, 0): F(1, 4)}
B.update({k: F(0) for k in KEYS if k not in B})

def marg(t, keep):
    out = {}
    for k, p in t.items():
        key = tuple(k[i] for i in keep)
        out[key] = out.get(key, F(0)) + p
    return out

def cond(t, fixed, target):
    num = sum(p for k, p in t.items()
              if all(k[i] == v for i, v in fixed.items()) and k[target] == 1)
    den = sum(p for k, p in t.items() if all(k[i] == v for i, v in fixed.items()))
    return num, den

assert sum(A.values()) == 1 and sum(B.values()) == 1
for i in range(3):
    assert marg(A, [i]) == marg(B, [i]), ("univariate", i)
for pair in ((0, 1), (0, 2), (1, 2)):
    assert marg(A, pair) == marg(B, pair), ("pairwise", pair)
assert A != B
print("UNIVARIATE_AND_ALL_PAIRWISE_MARGINALS_IDENTICAL: PASS")
print("TRUE_3WAY_JOINT_DIFFERS: PASS")
print("A_3WAY", {''.join(map(str, k)): str(v) for k, v in A.items() if v})
print("B_3WAY", {''.join(map(str, k)): str(v) for k, v in B.items() if v})
print("A_000", A[(0, 0, 0)], "B_000", B[(0, 0, 0)])
print("A_111", A[(1, 1, 1)], "B_111", B[(1, 1, 1)])

# Forward: P(Z=1 | X=0,Y=0); denominator = respondents with X,Y answered.
fa = cond(A, {0: 0, 1: 0}, 2)
fb = cond(B, {0: 0, 1: 0}, 2)
print("FORWARD P(Z=1|X=0,Y=0) A", fa[0], "/", fa[1], "=", fa[0] / fa[1])
print("FORWARD P(Z=1|X=0,Y=0) B", fb[0], "/", fb[1], "=", fb[0] / fb[1])
assert fa != fb

# Reverse: P(Y=1 | X=1,Z=1); denominator = respondents with X=1,Z=1.
ra = cond(A, {0: 1, 2: 1}, 1)
rb = cond(B, {0: 1, 2: 1}, 1)
print("REVERSE P(Y=1|X=1,Z=1) A", ra[0], "/", ra[1], "=", ra[0] / ra[1])
print("REVERSE P(Y=1|X=1,Z=1) B", rb[0], "/", rb[1], "=", rb[0] / rb[1])
assert ra != rb

# Denominator contrast: P(Y=1|Z=1) vs P(Y=1|X=1,Z=1) use different risk sets.
zy = cond(B, {2: 1}, 1)
print("B P(Y=1|Z=1)", zy[0], "/", zy[1], "=", zy[0] / zy[1])
print("B P(Y=1|X=1,Z=1)", rb[0], "/", rb[1], "=", rb[0] / rb[1])
assert zy != rb
print("DENOMINATORS_DIFFER_BY_RISK_SET: PASS")
print("STATUS=PASS_EXACT_TABLES")
