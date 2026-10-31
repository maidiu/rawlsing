def derive_alienation(state, derived, config):
    """Derive alienation vector from domain A/S/V mismatches, not independently mutated.

    distant_others: weighted by domains where awareness=unknown/distorted AND
                    solidarity=none AND viscerality=distant
    near_others:    weighted by domains where solidarity=none AND
                    viscerality=proximate/identified + buffer relational costs
    self:           from inner_load + (number of forsworn commitments * 10)
    moral_totality: from (100-coherence) * (100-religiosity) / 100 * buffer_presence_factor
    """
    from v3.core.enums import DOMAIN_NAMES

    distant = 0.0
    near = 0.0
    weight_total = 0.0

    for name in DOMAIN_NAMES:
        if name not in state.domains:
            continue
        d = state.domains[name]
        a_val = float(getattr(d, "A", 0))
        s_val = float(getattr(d, "S", 0))
        v_val = float(getattr(d, "V", 0))
        buf = str(getattr(d, "buffer_type", "")) if hasattr(d, "buffer_type") else ""
        # Weight by domain importance (empire/nation highest)
        domain_weight = {"empire_occupation": 0.25, "nation_state": 0.25,
                         "sect_class_ethnicity": 0.20, "family_household": 0.15,
                         "body_self": 0.15}.get(name, 0.20)
        weight_total += domain_weight

        # distant_others: don't know, don't care, don't feel it
        if a_val < 50 and s_val < 33 and v_val < 50:
            distant += 100.0 * domain_weight
        elif a_val < 50 or s_val < 33:
            distant += 50.0 * domain_weight

        # near_others: don't care about people close to them
        if s_val < 33 and v_val >= 50:
            near += 80.0 * domain_weight
        # Buffer costs add to near_others alienation
        if buf in ("guilt", "colonial_justification"):
            near += 15.0 * domain_weight

    # Normalize
    if weight_total > 0:
        distant = distant / weight_total
        near = near / weight_total

    # self alienation
    inner_load = float(getattr(state.registers, "inner_load", 50) or 50)
    self_axis = inner_load * 0.7

    # moral_totality: how disconnected from larger meaning
    coherence = float(getattr(state.peak_routing, "coherence", 50) or 50)
    ps = getattr(state, "practice_stack", None)
    religiosity = float(getattr(ps, "spiritual", 0) or 0) if ps else 0.0
    buffer_presence = 0.3 if any(
        getattr(d, "buffer_type", "") in ("not_my_concern", "liberal_utopian_blur", "colonial_justification")
        for d in state.domains.values() if hasattr(d, "buffer_type")
    ) else 0.1
    moral = (100.0 - coherence) * (100.0 - religiosity) / 100.0 * buffer_presence

    # Set alienation vector
    av = state.alienation_vector
    av.distant_others = max(0.0, min(100.0, round(distant, 1)))
    av.near_others = max(0.0, min(100.0, round(near, 1)))
    av.self = max(0.0, min(100.0, round(self_axis, 1)))
    av.moral_totality = max(0.0, min(100.0, round(moral, 1)))

    # Keep scalar in sync
    state.alienation = (av.distant_others + av.near_others + av.self + av.moral_totality) / 4.0


def update_alienation(state, derived, config):
    return derive_alienation(state, derived, config)
