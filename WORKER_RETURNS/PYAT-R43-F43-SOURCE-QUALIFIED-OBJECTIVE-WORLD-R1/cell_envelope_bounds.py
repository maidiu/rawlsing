"""Conservative conditional envelopes over native marginal cell intervals.

This consumes already supplied F6M uncertainty; it neither estimates mapping
bias nor grants transport. It relaxes correlations among source-specific cell
bounds, so it is an OUTER set, not generally a sharp source-model region.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from bounded_methods import MethodError, q


def conditional_envelope(cell_bounds, axes, conditions, outcome):
    if not axes or len(set(axes)) != len(axes) or outcome not in axes:
        raise MethodError('INVALID_ENVELOPE_TOPOLOGY')
    if outcome in conditions or any(k not in axes for k in conditions):
        raise MethodError('INVALID_ENVELOPE_CONDITION')
    cells = {}
    for row in cell_bounds:
        key = tuple(row['categories'])
        if key in cells or len(key) != len(axes):
            raise MethodError('INVALID_ENVELOPE_CELL')
        lo, hi = q(row['lower'], unit=True), q(row['upper'], unit=True)
        if lo > hi:
            raise MethodError('INVERTED_CELL_ENVELOPE')
        cells[key] = (lo, hi)
    if (not cells or sum(v[0] for v in cells.values()) > 1
            or sum(v[1] for v in cells.values()) < 1):
        raise MethodError('INFEASIBLE_CELL_ENVELOPE')
    for axis, value in conditions.items():
        if value not in {key[axes.index(axis)] for key in cells}:
            raise MethodError('CATEGORY_OUTSIDE_SUPPORT')
    out = {}
    for label in sorted({key[axes.index(outcome)] for key in cells}):
        # Three exhaustive, disjoint events: Y=label,C ; Y!=label,C ; not C.
        groups = [[Q(0), Q(0)] for _ in range(3)]
        for key, interval in cells.items():
            matches = all(key[axes.index(k)] == v for k, v in conditions.items())
            group = (0 if key[axes.index(outcome)] == label else 1) if matches else 2
            for i in (0, 1):
                groups[group][i] += interval[i]
        for interval in groups:
            interval[1] = min(Q(1), interval[1])
        vertices = []
        for fixed in combinations(range(3), 2):
            free = next(i for i in range(3) if i not in fixed)
            for endpoints in product((0, 1), repeat=2):
                v = [Q(0)] * 3
                for i, endpoint in zip(fixed, endpoints):
                    v[i] = groups[i][endpoint]
                v[free] = 1-sum(v)
                if all(lo <= value <= hi for value, (lo, hi) in zip(v, groups)) and v[0]+v[1] > 0:
                    vertices.append((v[0]/(v[0]+v[1]), v))
        if not vertices:
            out[label] = dict(lower=None, upper=None, state='UNDEFINED_ZERO_CONDITION_MASS')
            continue
        lower = min(vertices, key=lambda x: x[0]); upper = max(vertices, key=lambda x: x[0])
        out[label] = dict(lower=str(lower[0]), upper=str(upper[0]),
                          lower_outer_witness=[str(v) for v in lower[1]],
                          upper_outer_witness=[str(v) for v in upper[1]])
    return dict(bounds=out, state='CONSERVATIVE_CELL_ENVELOPE_CONDITIONAL',
                uncertainty='SUPPLIED_SOURCE_OR_BIAS_ENVELOPE_NOT_SAMPLING_CI',
                dependence='RELAXED_CELL_BOX_PLUS_NORMALIZATION_OUTER_SET',
                point=None, real_use_authorized=False, route_probability=None)
