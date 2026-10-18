# Enneagram Type Emergence System

## Overview

The Enneagram type **emerges** from the life course simulation - it is NOT predetermined or assigned at birth. The type develops naturally from:
- Early childhood imprinting (ages 0-7)
- Unmet needs that develop
- Compensation patterns that activate
- Strategies that emerge
- World conditions and experiences

## How Type Emergence Works

### 1. Birth: No Type Assigned

At birth, the persona has:
- **No Enneagram type** - type doesn't exist yet
- **Temperament** (`EnneagramLatentVector`) - just biases (reactivity, idealism, shame/fear/anger)
- **Initial needs** - sampled from birth conditions
- **No strategies** - strategies develop in response to needs

### 2. Early Childhood (Ages 0-7): The Imprint Period

During early childhood, the **imprint** occurs:

**What Happens:**
- Unmet needs develop (e.g., low warmth, low safety, low belonging)
- Compensation patterns activate (general Enneagram-aligned patterns)
- Strategies begin to develop in response to unmet needs
- Patterns start to form

**Compensation During Imprint:**
- Uses **general Enneagram-aligned patterns** (type not known yet)
- Examples:
  - Low warmth → overcompensate with coherence/safety (Type 1 pattern)
  - Low warmth → overcompensate with recognition (Type 2 pattern)
  - Low safety → overcompensate with belonging (Type 6 pattern)
- Compensation is **1.5x stronger** during imprint (creates lasting patterns)

**Key Point:** The compensation patterns are Enneagram-aligned but **don't require knowing the type**. They're general patterns that could lead to any type, depending on what develops.

### 3. Life Continues: Patterns Deepen

As life continues:
- Patterns established during imprint persist
- New patterns develop in response to experiences
- Strategies become more sophisticated
- Needs and compensation create feedback loops
- World conditions influence development

**Compensation Continues:**
- Still uses general Enneagram-aligned patterns (type still not known)
- Patterns deepen and become more characteristic
- The psychological structure develops

### 4. End of Simulation: Type Emerges

At the end of the life course simulation:

```python
# Infer Enneagram from life-course
enneagram_profile = infer_enneagram_from_life(yearly_states)

# Attach Enneagram to final state
final_state.enneagram = enneagram_profile
```

**How Inference Works:**
1. **Extract patterns** from the full life course:
   - Early childhood patterns (ages 0-7)
   - Childhood patterns (ages 7-14)
   - Adult patterns (ages 22+)
   - Characteristic strategies
   - Characteristic needs
   - Indices (DRTS, PI, RMT, etc.)

2. **Match to type wisdom**:
   - Compare life course patterns to each type's `early_childhood_pattern`
   - Compare to `childhood_pattern` and `adulthood_pattern`
   - Compare to `primary_strategies`, `unmet_needs`, `overcompensated_needs`
   - Use probabilistic matching (not fixed)

3. **Score each type**:
   - Each type gets a probability score
   - Based on how well life course matches type wisdom
   - Early childhood patterns weighted 1.5x more (imprint period)

4. **Type emerges**:
   - Highest scoring type becomes `primary_type`
   - Wing determined from adjacent type scores
   - Health level computed from RMT and buffers

**Key Point:** The type is **inferred from the patterns that developed**, not predetermined.

## Why This Works

### Compensation Doesn't Require Type

The compensation system uses **general Enneagram-aligned patterns** that don't require knowing the type:

```python
# General Enneagram-aligned compensation patterns (when type unknown or as fallback)
# These patterns align with common Enneagram overcompensation patterns

# Type 1 pattern: Low warmth/play → overcompensate with coherence/safety
if need_name == "coherence_meaning":
    warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
    play_value = getattr(prev_needs, "play_pleasure", 50.0)
    if warmth_value < 40.0 or play_value < 40.0:
        deficit = max(40.0 - warmth_value, 40.0 - play_value, 0)
        compensation += deficit * 0.12  # Up to 4.8 points
```

These patterns are **Enneagram-aligned** (they match what types do) but **general** (they could lead to any type depending on what else develops).

### Patterns Develop Naturally

The patterns that develop are a result of:
1. **Early imprinting**: What unmet needs developed during ages 0-7
2. **Compensation**: How the persona compensated for unmet needs
3. **Strategies**: What strategies activated in response
4. **World conditions**: Material circumstances, parental values, etc.
5. **Feedback loops**: Needs → strategies → needs → compensation

All of this happens **without knowing the type**. The type emerges from what developed.

### Type Matches What Developed

The inference system matches the **actual patterns that developed** to type wisdom:

- If early childhood had low warmth and high coherence → matches Type 1 pattern
- If early childhood had low belonging and high transcendence → matches Type 4 pattern
- If early childhood had low safety and high belonging → matches Type 6 pattern

The type **emerges** from the patterns, not the other way around.

## Example: Type 1 Emergence

### Birth (Age 0)
- No Enneagram type
- Temperament: Some reactivity, idealism
- Initial needs: Sampled from conditions

### Early Childhood (Ages 0-7)
- **Imprint develops**:
  - Low warmth (parental values, world conditions)
  - Low play (repressed, can't play if not perfect)
  - Compensation activates: coherence/safety increases
  - Strategies develop: compliance, perfectionism
- **Pattern forms**: High need for order, low warmth, repressed anger

### Life Continues (Ages 8-40)
- Patterns deepen
- Strategies become more sophisticated
- Compensation continues (maintains pattern)
- World conditions influence development

### End of Simulation (Age 40)
- **Type inferred**:
  - Early pattern: Low warmth, high coherence → matches Type 1
  - Strategies: Perfectionism, compliance → matches Type 1
  - Needs: Low warmth/play, high coherence → matches Type 1
  - **Type 1 emerges** from the patterns that developed

## Verification

✅ **Type NOT assigned at birth**: No Enneagram type exists at birth
✅ **Type NOT used during simulation**: Compensation doesn't use type (it's not known)
✅ **Patterns develop naturally**: From imprinting, unmet needs, compensation, strategies
✅ **Type emerges at end**: Inferred from the patterns that developed
✅ **Type matches patterns**: The type that emerges matches what actually developed

## Conclusion

The Enneagram type **fully emerges** from the life course simulation. It is:
- **NOT predetermined** - not assigned at birth
- **NOT used during simulation** - compensation uses general patterns
- **Emerges from patterns** - inferred from what developed
- **Matches what developed** - the type reflects the actual life course

The system creates psychologically realistic development where:
1. Early childhood imprinting creates patterns
2. Compensation and strategies develop naturally
3. Patterns deepen throughout life
4. Type emerges from the patterns at the end

This aligns with Enneagram theory: the type develops from life experiences, not from predetermined assignment.

