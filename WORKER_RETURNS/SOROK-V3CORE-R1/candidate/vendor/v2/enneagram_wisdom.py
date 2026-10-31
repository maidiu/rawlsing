"""
Enneagram Wisdom System

Synthesizes insights from Ichazo, Naranjo, Riso, Chestnut, and others
to guide Enneagram inference from life-course patterns.

This system is:
- **Data-responsive**: Patterns adapt to actual data distributions
- **Probabilistic**: Uses confluence of factors to create likelihoods, not absolutes
- **Context-aware**: Adapts to different countries, time periods, material circumstances
- **Parent-influenced**: Models how WVS parent values → parent behavior → child development
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Literal, Tuple, Union, Any
import numpy as np
import random


@dataclass
class PatternRange:
    """Probabilistic range for a pattern value (allows variance)"""
    mean: float
    std: float = 15.0  # Standard deviation (allows individual variation)
    min_val: float = 0.0
    max_val: float = 100.0
    
    def sample(self) -> float:
        """Sample a value from this range"""
        value = np.random.normal(self.mean, self.std)
        return max(self.min_val, min(self.max_val, value))
    
    def probability_density(self, value: float) -> float:
        """Probability density at a given value (for matching)"""
        # Normal distribution PDF, normalized
        z = (value - self.mean) / self.std if self.std > 0 else 0
        return np.exp(-0.5 * z**2) / (self.std * np.sqrt(2 * np.pi)) if self.std > 0 else 1.0


@dataclass
class EnneagramTypeWisdom:
    """
    Wisdom about a specific Enneagram type from the masters.
    
    Patterns are probabilistic ranges, not fixed values, allowing:
    - Individual variation
    - Data-responsive adaptation
    - Context-dependent outcomes
    """
    type_number: int
    name: str
    
    # Core psychology (from Ichazo/Naranjo)
    core_fear: str
    core_desire: str
    superego_message: str
    passion: str  # The "capital sin" / ruling passion
    fixation: str  # The cognitive fixation
    defense_mechanism: str
    center: Literal["gut", "heart", "head"]
    
    # Developmental trajectories (from Riso) - must come before default fields
    integration_line: int  # Type they move toward when healthy
    disintegration_line: int  # Type they move toward when stressed
    
    # Life-course patterns (PROBABILISTIC - ranges, not fixed values)
    # Each value can be a float (mean) or PatternRange (mean + variance)
    early_childhood_pattern: Dict[str, Union[float, PatternRange]] = field(default_factory=dict)  # Ages 0-7
    childhood_pattern: Dict[str, Union[float, PatternRange]] = field(default_factory=dict)  # Ages 7-14
    adulthood_pattern: Dict[str, Union[float, PatternRange]] = field(default_factory=dict)  # Ages 22+
    
    # Characteristic strategies (from Naranjo)
    primary_strategies: List[str] = field(default_factory=list)
    secondary_strategies: List[str] = field(default_factory=list)
    avoided_strategies: List[str] = field(default_factory=list)
    
    # Characteristic needs (which are chronically unmet/over-met)
    unmet_needs: List[str] = field(default_factory=list)
    overcompensated_needs: List[str] = field(default_factory=list)
    
    # Characteristic indices (probabilistic ranges)
    typical_indices: Dict[str, Union[float, PatternRange]] = field(default_factory=dict)
    
    # Wing patterns (probabilistic)
    wing_patterns: Dict[int, Dict[str, Union[float, PatternRange]]] = field(default_factory=dict)
    
    # Subtype patterns (from Chestnut, probabilistic)
    subtype_patterns: Dict[str, Dict[str, Union[float, PatternRange]]] = field(default_factory=dict)
    
    # Context modifiers (how material circumstances affect patterns)
    context_modifiers: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # e.g., {"high_conflict": {"needs.safety": -20, "strategies.aggression_outward": +15}}


# ============================================================================
# TYPE WISDOM KNOWLEDGE BASE
# ============================================================================

TYPE_1_WISDOM = EnneagramTypeWisdom(
    type_number=1,
    name="The Reformer / The Perfectionist",
    core_fear="Of being bad, corrupt, evil, or defective",
    core_desire="To be good, virtuous, in balance, to have integrity",
    superego_message="You are good or okay if you do what is right",
    passion="Anger (repressed as resentment)",
    fixation="Resentment / Perfectionism",
    defense_mechanism="Reaction formation (anger → perfectionism)",
    center="gut",
    
    # Early childhood: High need for safety through rules, repressed warmth
    # Using PatternRange to allow variance (individual variation)
    early_childhood_pattern={
        "needs.safety": PatternRange(60.0, std=15.0),  # Rules = safety (with variance)
        "needs.warmth_bonding": PatternRange(40.0, std=12.0),  # Repressed (anger blocks warmth)
        "needs.coherence_meaning": PatternRange(70.0, std=10.0),  # Need for order
        "strategies.compliance_obedience": PatternRange(50.0, std=15.0),
    },
    
    # Childhood: Developing perfectionism
    childhood_pattern={
        "strategies.perfectionism_control": PatternRange(60.0, std=15.0),
        "strategies.compliance_obedience": PatternRange(70.0, std=12.0),
        "strategies.aggression_inward": PatternRange(40.0, std=15.0),  # Self-criticism
        "needs.play_pleasure": PatternRange(30.0, std=12.0),  # Can't play if not perfect
    },
    
    # Adulthood: Full pattern
    adulthood_pattern={
        "strategies.perfectionism_control": PatternRange(70.0, std=12.0),
        "strategies.compliance_obedience": PatternRange(60.0, std=15.0),
        "strategies.aggression_inward": PatternRange(50.0, std=15.0),  # Repressed anger
        "strategies.aggression_outward": PatternRange(20.0, std=10.0),  # Low (repressed)
        "needs.play_pleasure": PatternRange(30.0, std=12.0),
        "needs.coherence_meaning": PatternRange(80.0, std=10.0),  # High (order = meaning)
    },
    
    # Context modifiers: How material circumstances affect Type 1 patterns
    context_modifiers={
        "high_conflict": {
            "needs.safety": -15.0,  # Conflict reduces safety
            "strategies.perfectionism_control": +10.0,  # More control needed
        },
        "high_authoritarian_culture": {
            "strategies.compliance_obedience": +15.0,
            "needs.autonomy_agency": -10.0,
        },
        "low_material_security": {
            "needs.safety": -20.0,
            "strategies.perfectionism_control": +5.0,  # Control as compensation
        },
        "high_parental_warmth": {
            "needs.warmth_bonding": +15.0,  # Can mitigate repression
            "strategies.aggression_inward": -10.0,
        },
    },
    
    primary_strategies=["perfectionism_control", "compliance_obedience"],
    secondary_strategies=["aggression_inward", "achievement_striving"],
    avoided_strategies=["aggression_outward", "play_pleasure", "substance_use"],
    
    unmet_needs=["warmth_bonding", "play_pleasure"],
    overcompensated_needs=["coherence_meaning", "safety"],
    
    typical_indices={
        "drts": PatternRange(40.0, std=15.0),  # Moderate (rules provide structure)
        "permeability_index": PatternRange(30.0, std=12.0),  # Low (rigid)
        "recursive_madness_threshold": PatternRange(50.0, std=15.0),  # Moderate
    },
    
    integration_line=7,  # Moves toward spontaneity, joy
    disintegration_line=4,  # Moves toward moodiness, self-criticism
    
    wing_patterns={
        9: {"strategies.withdrawal_avoidance": 50.0, "needs.coherence_meaning": 85.0},
        2: {"strategies.caretaking_rescue": 40.0, "needs.warmth_bonding": 45.0},
    },
    
    subtype_patterns={
        "sp": {"strategies.perfectionism_control": 80.0, "needs.bodily_comfort": 60.0},
        "so": {"strategies.compliance_obedience": 75.0, "needs.belonging_group": 55.0},
        "sx": {"strategies.aggression_outward": 35.0, "strategies.activism_justice": 50.0},
    }
)

TYPE_4_WISDOM = EnneagramTypeWisdom(
    type_number=4,
    name="The Individualist",
    core_fear="Of having no identity or personal significance",
    core_desire="To find themselves and their significance, to create an identity",
    superego_message="You are good or okay if you are true to yourself",
    passion="Envy",
    fixation="Melancholy / Introjection",
    defense_mechanism="Introjection (internalize rejection, feel deficient)",
    center="heart",
    
    # Early childhood: Feels different, low belonging
    early_childhood_pattern={
        "needs.belonging_group": 30.0,  # Feels different
        "needs.warmth_bonding": 40.0,  # Feels rejected
        "needs.coherence_meaning": 50.0,  # Searching for identity
        "strategies.fantasy_immersion": 50.0,  # Imagined belonging
    },
    
    # Childhood: Developing creativity, withdrawal
    childhood_pattern={
        "strategies.creative_expression": 60.0,
        "strategies.fantasy_immersion": 70.0,
        "strategies.withdrawal_avoidance": 50.0,
        "needs.recognition_status": 40.0,  # Feels unseen
    },
    
    # Adulthood: Full pattern
    adulthood_pattern={
        "strategies.creative_expression": 75.0,
        "strategies.fantasy_immersion": 70.0,
        "strategies.withdrawal_avoidance": 60.0,
        "strategies.aggression_inward": 50.0,  # Self-criticism
        "needs.belonging_group": 35.0,
        "needs.transcendence_sacred": 70.0,  # Aesthetic/artistic
    },
    
    primary_strategies=["creative_expression", "fantasy_immersion"],
    secondary_strategies=["withdrawal_avoidance", "aggression_inward"],
    avoided_strategies=["compliance_obedience", "people_pleasing"],
    
    unmet_needs=["belonging_group", "recognition_status"],
    overcompensated_needs=["transcendence_sacred", "coherence_meaning"],
    
    typical_indices={
        "drts": 50.0,  # Moderate
        "permeability_index": 70.0,  # High (aesthetic sensitivity)
        "aesthetic_amplification": 80.0,  # Very high
        "recursive_madness_threshold": 60.0,  # Higher (melancholy)
    },
    
    integration_line=1,  # Moves toward integrity, objectivity
    disintegration_line=2,  # Moves toward people-pleasing, losing self
    
    wing_patterns={
        3: {"strategies.achievement_striving": 50.0, "needs.recognition_status": 55.0},
        5: {"strategies.withdrawal_avoidance": 70.0, "indices.permeability_index": 80.0},
    },
    
    subtype_patterns={
        "sp": {"strategies.withdrawal_avoidance": 70.0, "needs.bodily_comfort": 40.0},
        "so": {"strategies.creative_expression": 80.0, "needs.belonging_group": 40.0},
        "sx": {"strategies.aggression_outward": 50.0, "strategies.intimacy_seeking": 60.0},
    }
)

TYPE_6_WISDOM = EnneagramTypeWisdom(
    type_number=6,
    name="The Loyalist",
    core_fear="Of being without support or guidance",
    core_desire="To have security and support",
    superego_message="You are good or okay if you do what is expected of you",
    passion="Fear",
    fixation="Cowardice / Projection",
    defense_mechanism="Projection (fear → external threat)",
    center="head",
    
    # Early childhood: Low safety, high need for belonging
    early_childhood_pattern={
        "needs.safety": 35.0,  # Anxious
        "needs.belonging_group": 60.0,  # Security through group
        "needs.warmth_bonding": 45.0,
        "strategies.compliance_obedience": 50.0,  # Phobic subtype
    },
    
    # Childhood: Developing loyalty or rebellion
    childhood_pattern={
        "strategies.compliance_obedience": 60.0,  # OR aggression_outward (counterphobic)
        "strategies.aggression_outward": 30.0,  # May be higher if counterphobic
        "needs.safety": 40.0,
        "indices.drts": 50.0,  # Can go either way
    },
    
    # Adulthood: Full pattern (phobic or counterphobic)
    adulthood_pattern={
        "strategies.compliance_obedience": 65.0,  # OR lower if counterphobic
        "strategies.aggression_outward": 40.0,  # Higher if counterphobic
        "strategies.activism_justice": 50.0,  # When authority fails
        "needs.safety": 40.0,
        "needs.belonging_group": 70.0,  # High (group = security)
    },
    
    primary_strategies=["compliance_obedience", "activism_justice"],  # Depends on subtype
    secondary_strategies=["aggression_outward", "people_pleasing"],
    avoided_strategies=["withdrawal_avoidance", "fantasy_immersion"],  # Need connection
    
    unmet_needs=["safety", "autonomy_agency"],
    overcompensated_needs=["belonging_group"],
    
    typical_indices={
        "drts": 60.0,  # Can be high (counterphobic) or moderate (phobic)
        "permeability_index": 40.0,  # Low (rigid, security-focused)
        "recursive_madness_threshold": 45.0,  # Lower (anxiety)
    },
    
    integration_line=9,  # Moves toward peace, trust
    disintegration_line=3,  # Moves toward frantic activity, losing self
    
    wing_patterns={
        5: {"strategies.withdrawal_avoidance": 50.0, "indices.permeability_index": 50.0},
        7: {"strategies.fantasy_immersion": 50.0, "needs.play_pleasure": 55.0},
    },
    
    subtype_patterns={
        "sp": {"strategies.compliance_obedience": 70.0, "needs.safety": 35.0},  # Phobic
        "so": {"strategies.activism_justice": 60.0, "needs.belonging_group": 75.0},
        "sx": {"strategies.aggression_outward": 60.0, "indices.drts": 70.0},  # Counterphobic
    }
)

# Add remaining types (2, 3, 5, 7, 8, 9) following same pattern
# For brevity, I'll create a function to build the full knowledge base

# Add remaining types
TYPE_2_WISDOM = EnneagramTypeWisdom(
    type_number=2,
    name="The Helper",
    core_fear="Of being unloved and unwanted for themselves alone",
    core_desire="To feel loved",
    superego_message="You are good or okay if you are loved by others and are close to them",
    passion="Pride (self-inflation through giving)",
    fixation="Flattery / Repression",
    defense_mechanism="Repression (own needs → focus on others)",
    center="heart",
    early_childhood_pattern={
        "needs.warmth_bonding": 35.0,  # Unmet, drives giving
        "needs.belonging_group": 50.0,
        "strategies.people_pleasing": 50.0,
    },
    childhood_pattern={
        "strategies.caretaking_rescue": 60.0,
        "strategies.people_pleasing": 70.0,
        "needs.recognition_status": 55.0,  # Need to be appreciated
    },
    adulthood_pattern={
        "strategies.caretaking_rescue": 75.0,
        "strategies.people_pleasing": 80.0,
        "strategies.aggression_inward": 40.0,  # Repressed needs
        "needs.warmth_bonding": 40.0,  # Still unmet
    },
    primary_strategies=["caretaking_rescue", "people_pleasing"],
    secondary_strategies=["intimacy_seeking", "piety_ideology"],
    avoided_strategies=["withdrawal_avoidance", "aggression_outward"],
    unmet_needs=["warmth_bonding"],
    overcompensated_needs=["recognition_status"],
    typical_indices={"drts": 30.0, "permeability_index": 50.0},
    integration_line=4,
    disintegration_line=8,
    wing_patterns={
        1: {"strategies.compliance_obedience": 50.0},
        3: {"strategies.achievement_striving": 50.0, "needs.recognition_status": 60.0},
    },
    subtype_patterns={
        "sp": {"strategies.people_pleasing": 85.0, "needs.bodily_comfort": 45.0},
        "so": {"strategies.caretaking_rescue": 80.0, "needs.belonging_group": 60.0},
        "sx": {"strategies.intimacy_seeking": 70.0, "strategies.aggression_outward": 35.0},
    }
)

TYPE_3_WISDOM = EnneagramTypeWisdom(
    type_number=3,
    name="The Achiever",
    core_fear="Of being worthless or without inherent value apart from achievements",
    core_desire="To feel valuable and worthwhile",
    superego_message="You are good or okay as long as you are successful and others think well of you",
    passion="Vanity / Fraudulence",
    fixation="Vanity / Identification",
    defense_mechanism="Identification (become the image)",
    center="heart",
    early_childhood_pattern={
        "needs.recognition_status": 60.0,
        "needs.warmth_bonding": 45.0,  # Performance-based love
        "strategies.achievement_striving": 50.0,
    },
    childhood_pattern={
        "strategies.achievement_striving": 70.0,
        "strategies.compliance_obedience": 60.0,
        "needs.recognition_status": 70.0,
    },
    adulthood_pattern={
        "strategies.achievement_striving": 80.0,
        "strategies.compliance_obedience": 50.0,
        "strategies.people_pleasing": 60.0,
        "needs.recognition_status": 75.0,
        "needs.warmth_bonding": 40.0,  # Avoids feelings
    },
    primary_strategies=["achievement_striving", "compliance_obedience"],
    secondary_strategies=["people_pleasing", "perfectionism_control"],
    avoided_strategies=["withdrawal_avoidance", "aggression_inward"],
    unmet_needs=["warmth_bonding", "coherence_meaning"],
    overcompensated_needs=["recognition_status", "competence_effectiveness"],
    typical_indices={"drts": 40.0, "permeability_index": 50.0},
    integration_line=6,
    disintegration_line=9,
    wing_patterns={
        2: {"strategies.caretaking_rescue": 50.0, "needs.warmth_bonding": 45.0},
        4: {"strategies.creative_expression": 50.0, "needs.coherence_meaning": 55.0},
    },
    subtype_patterns={
        "sp": {"strategies.achievement_striving": 85.0, "needs.bodily_comfort": 50.0},
        "so": {"strategies.people_pleasing": 70.0, "needs.belonging_group": 65.0},
        "sx": {"strategies.intimacy_seeking": 60.0, "strategies.aggression_outward": 40.0},
    }
)

TYPE_5_WISDOM = EnneagramTypeWisdom(
    type_number=5,
    name="The Investigator",
    core_fear="Of being helpless, useless, or incapable",
    core_desire="To be competent and capable",
    superego_message="You are good or okay if you have mastered something",
    passion="Avarice (hoarding energy, knowledge)",
    fixation="Stinginess / Isolation",
    defense_mechanism="Isolation (withdraw from feelings)",
    center="head",
    early_childhood_pattern={
        "needs.warmth_bonding": 35.0,  # Withdrawn
        "needs.competence_effectiveness": 60.0,
        "strategies.withdrawal_avoidance": 50.0,
    },
    childhood_pattern={
        "strategies.withdrawal_avoidance": 65.0,
        "strategies.fantasy_immersion": 60.0,
        "indices.permeability_index": 70.0,  # High curiosity
    },
    adulthood_pattern={
        "strategies.withdrawal_avoidance": 75.0,
        "strategies.fantasy_immersion": 70.0,
        "strategies.creative_expression": 50.0,
        "needs.warmth_bonding": 30.0,
        "indices.permeability_index": 80.0,
    },
    primary_strategies=["withdrawal_avoidance", "fantasy_immersion"],
    secondary_strategies=["creative_expression"],
    avoided_strategies=["people_pleasing", "intimacy_seeking", "caretaking_rescue"],
    unmet_needs=["warmth_bonding", "belonging_group"],
    overcompensated_needs=["competence_effectiveness"],
    typical_indices={"drts": 30.0, "permeability_index": 85.0, "recursive_madness_threshold": 60.0},
    integration_line=8,
    disintegration_line=7,
    wing_patterns={
        4: {"strategies.creative_expression": 60.0, "needs.transcendence_sacred": 65.0},
        6: {"strategies.compliance_obedience": 40.0, "needs.safety": 45.0},
    },
    subtype_patterns={
        "sp": {"strategies.withdrawal_avoidance": 80.0, "needs.bodily_comfort": 35.0},
        "so": {"strategies.creative_expression": 60.0, "needs.belonging_group": 40.0},
        "sx": {"strategies.intimacy_seeking": 50.0, "strategies.aggression_outward": 30.0},
    }
)

TYPE_7_WISDOM = EnneagramTypeWisdom(
    type_number=7,
    name="The Enthusiast",
    core_fear="Of being deprived or trapped in pain",
    core_desire="To be happy and satisfied",
    superego_message="You are good or okay if you get what you need",
    passion="Gluttony",
    fixation="Planning / Rationalization",
    defense_mechanism="Rationalization (avoid pain through planning)",
    center="head",
    early_childhood_pattern={
        "needs.play_pleasure": 70.0,
        "needs.bodily_comfort": 50.0,
        "strategies.fantasy_immersion": 60.0,
    },
    childhood_pattern={
        "strategies.fantasy_immersion": 70.0,
        "strategies.risk_seeking_thrill": 50.0,
        "needs.play_pleasure": 75.0,
        "indices.permeability_index": 70.0,
    },
    adulthood_pattern={
        "strategies.fantasy_immersion": 75.0,
        "strategies.risk_seeking_thrill": 65.0,
        "strategies.substance_use": 40.0,  # May use substances
        "needs.play_pleasure": 80.0,
        "needs.bodily_comfort": 60.0,  # Avoids pain
        "indices.permeability_index": 75.0,
    },
    primary_strategies=["fantasy_immersion", "risk_seeking_thrill"],
    secondary_strategies=["substance_use", "humor_play"],
    avoided_strategies=["withdrawal_avoidance", "aggression_inward"],
    unmet_needs=["coherence_meaning", "transcendence_sacred"],
    overcompensated_needs=["play_pleasure"],
    typical_indices={"drts": 50.0, "permeability_index": 75.0, "aesthetic_amplification": 60.0},
    integration_line=5,
    disintegration_line=1,
    wing_patterns={
        6: {"strategies.compliance_obedience": 40.0, "needs.safety": 50.0},
        8: {"strategies.aggression_outward": 50.0, "strategies.risk_seeking_thrill": 75.0},
    },
    subtype_patterns={
        "sp": {"needs.bodily_comfort": 70.0, "strategies.substance_use": 50.0},
        "so": {"strategies.people_pleasing": 60.0, "needs.belonging_group": 65.0},
        "sx": {"strategies.intimacy_seeking": 70.0, "strategies.risk_seeking_thrill": 80.0},
    }
)

TYPE_8_WISDOM = EnneagramTypeWisdom(
    type_number=8,
    name="The Challenger",
    core_fear="Of being harmed or controlled by others",
    core_desire="To protect themselves and determine their own path",
    superego_message="You are good or okay if you are strong and in control of your situation",
    passion="Lust (intensity, excess)",
    fixation="Vengeance / Denial",
    defense_mechanism="Denial (vulnerability doesn't exist)",
    center="gut",
    early_childhood_pattern={
        "needs.safety": 40.0,  # Learned to be strong
        "needs.autonomy_agency": 70.0,
        "strategies.aggression_outward": 50.0,
    },
    childhood_pattern={
        "strategies.aggression_outward": 65.0,
        "strategies.risk_seeking_thrill": 60.0,
        "needs.recognition_status": 60.0,
        "indices.drts": 70.0,
    },
    adulthood_pattern={
        "strategies.aggression_outward": 80.0,
        "strategies.activism_justice": 70.0,
        "strategies.risk_seeking_thrill": 65.0,
        "needs.autonomy_agency": 80.0,
        "needs.warmth_bonding": 30.0,  # Repressed vulnerability
        "indices.drts": 75.0,
    },
    primary_strategies=["aggression_outward", "activism_justice"],
    secondary_strategies=["risk_seeking_thrill"],
    avoided_strategies=["compliance_obedience", "people_pleasing", "withdrawal_avoidance"],
    unmet_needs=["warmth_bonding", "safety"],
    overcompensated_needs=["autonomy_agency", "recognition_status"],
    typical_indices={"drts": 80.0, "permeability_index": 40.0, "transgression_threshold": 30.0},
    integration_line=2,
    disintegration_line=5,
    wing_patterns={
        7: {"strategies.risk_seeking_thrill": 75.0, "needs.play_pleasure": 60.0},
        9: {"strategies.withdrawal_avoidance": 40.0, "needs.coherence_meaning": 50.0},
    },
    subtype_patterns={
        "sp": {"strategies.aggression_outward": 85.0, "needs.bodily_comfort": 50.0},
        "so": {"strategies.activism_justice": 80.0, "needs.belonging_group": 55.0},
        "sx": {"strategies.intimacy_seeking": 50.0, "strategies.aggression_outward": 85.0},
    }
)

TYPE_9_WISDOM = EnneagramTypeWisdom(
    type_number=9,
    name="The Peacemaker",
    core_fear="Of loss and separation",
    core_desire="To have inner stability and peace of mind",
    superego_message="You are good or okay as long as those around you are okay and at peace",
    passion="Sloth (psychospiritual inertia)",
    fixation="Indolence / Narcotization",
    defense_mechanism="Narcotization (numb out, avoid conflict)",
    center="gut",
    early_childhood_pattern={
        "needs.warmth_bonding": 50.0,
        "needs.belonging_group": 60.0,
        "strategies.withdrawal_avoidance": 50.0,  # Avoids conflict
    },
    childhood_pattern={
        "strategies.withdrawal_avoidance": 60.0,
        "strategies.fantasy_immersion": 65.0,
        "strategies.compliance_obedience": 50.0,
        "needs.coherence_meaning": 45.0,  # Numbed
    },
    adulthood_pattern={
        "strategies.withdrawal_avoidance": 70.0,
        "strategies.fantasy_immersion": 75.0,
        "strategies.compliance_obedience": 60.0,
        "strategies.aggression_outward": 20.0,  # Very low (repressed)
        "needs.autonomy_agency": 40.0,  # Low (avoids asserting)
        "needs.coherence_meaning": 50.0,  # Moderate (numbed)
    },
    primary_strategies=["withdrawal_avoidance", "fantasy_immersion"],
    secondary_strategies=["compliance_obedience"],
    avoided_strategies=["aggression_outward", "activism_justice"],
    unmet_needs=["autonomy_agency", "recognition_status"],
    overcompensated_needs=["belonging_group"],
    typical_indices={"drts": 30.0, "permeability_index": 50.0, "recursive_madness_threshold": 40.0},
    integration_line=3,
    disintegration_line=6,
    wing_patterns={
        8: {"strategies.aggression_outward": 35.0, "needs.autonomy_agency": 50.0},
        1: {"strategies.compliance_obedience": 70.0, "needs.coherence_meaning": 55.0},
    },
    subtype_patterns={
        "sp": {"strategies.withdrawal_avoidance": 75.0, "needs.bodily_comfort": 55.0},
        "so": {"strategies.compliance_obedience": 70.0, "needs.belonging_group": 70.0},
        "sx": {"strategies.intimacy_seeking": 60.0, "strategies.aggression_outward": 30.0},
    }
)

def build_enneagram_wisdom_base() -> Dict[int, EnneagramTypeWisdom]:
    """Build complete wisdom knowledge base for all 9 types"""
    return {
        1: TYPE_1_WISDOM,
        2: TYPE_2_WISDOM,
        3: TYPE_3_WISDOM,
        4: TYPE_4_WISDOM,
        5: TYPE_5_WISDOM,
        6: TYPE_6_WISDOM,
        7: TYPE_7_WISDOM,
        8: TYPE_8_WISDOM,
        9: TYPE_9_WISDOM,
    }


def match_life_course_to_type(
    states_over_time: List,
    type_wisdom: EnneagramTypeWisdom,
    context: Optional[Dict[str, Any]] = None
) -> float:
    """
    Score how well a life-course matches a type's wisdom pattern.
    
    PROBABILISTIC: Uses probability density functions, not fixed matching.
    DATA-RESPONSIVE: Adapts to context (material circumstances, parental values).
    
    Args:
        states_over_time: List of PersonaState objects
        type_wisdom: Type wisdom to match against
        context: Optional context dict with:
            - world_slice: World conditions
            - driver_vec: Parent cohort values (WVS)
            - local_modifiers: Local circumstances
            - parental_warmth: Average caregiver warmth
            - parental_authority: Average caregiver authority
    
    Returns:
        Probability score from 0-100 (likelihood this is the type)
    """
    if not states_over_time:
        return 0.0
    
    if context is None:
        context = {}
    
    # Extract life-course features
    early_states = [s for s in states_over_time if s.age <= 7]
    childhood_states = [s for s in states_over_time if 7 < s.age <= 14]
    adult_states = [s for s in states_over_time if s.age >= 22]
    
    scores = []
    
    # Apply context modifiers to patterns (data-responsive)
    early_pattern = _apply_context_modifiers(
        type_wisdom.early_childhood_pattern.copy(),
        type_wisdom.context_modifiers,
        context
    )
    child_pattern = _apply_context_modifiers(
        type_wisdom.childhood_pattern.copy(),
        type_wisdom.context_modifiers,
        context
    )
    adult_pattern = _apply_context_modifiers(
        type_wisdom.adulthood_pattern.copy(),
        type_wisdom.context_modifiers,
        context
    )
    
    # Match early childhood pattern (PROBABILISTIC)
    if early_states and early_pattern:
        early_score = _match_pattern_probabilistic(early_states, early_pattern)
        scores.append(early_score * 1.5)  # Weight early patterns more
    
    # Match childhood pattern
    if childhood_states and child_pattern:
        child_score = _match_pattern_probabilistic(childhood_states, child_pattern)
        scores.append(child_score * 1.2)
    
    # Match adulthood pattern
    if adult_states and adult_pattern:
        adult_score = _match_pattern_probabilistic(adult_states, adult_pattern)
        scores.append(adult_score * 1.0)
    
    # Match strategies (probabilistic)
    if adult_states:
        strategy_score = _match_strategies_probabilistic(adult_states, type_wisdom, context)
        scores.append(strategy_score * 0.8)
    
    # Match indices (probabilistic)
    if states_over_time:
        index_score = _match_indices_probabilistic(states_over_time, type_wisdom, context)
        scores.append(index_score * 0.7)
    
    # Average scores (confluence of factors)
    if scores:
        base_score = np.mean(scores)
        # Add some randomness (individual variation)
        variance = np.random.normal(0, 5.0)  # ±5 points of individual variation
        return max(0.0, min(100.0, base_score + variance))
    return 0.0


def _apply_context_modifiers(
    pattern: Dict[str, Union[float, PatternRange]],
    modifiers: Dict[str, Dict[str, float]],
    context: Dict[str, Any]
) -> Dict[str, Union[float, PatternRange]]:
    """
    Apply context modifiers to patterns (data-responsive adaptation).
    
    Modifies pattern means based on material circumstances:
    - High conflict → affects safety needs
    - Parental warmth → affects attachment patterns
    - Authoritarian culture → affects compliance
    """
    modified_pattern = pattern.copy()
    
    # Check context conditions and apply modifiers
    world_slice = context.get("world_slice")
    parental_warmth = context.get("parental_warmth", 50.0)
    parental_authority = context.get("parental_authority", 50.0)
    
    if world_slice:
        # High conflict
        if hasattr(world_slice, 'conflict_intensity') and world_slice.conflict_intensity > 60:
            for path, adjustment in modifiers.get("high_conflict", {}).items():
                if path in modified_pattern:
                    old_val = modified_pattern[path]
                    if isinstance(old_val, PatternRange):
                        modified_pattern[path] = PatternRange(
                            old_val.mean + adjustment,
                            old_val.std,
                            old_val.min_val,
                            old_val.max_val
                        )
                    else:
                        modified_pattern[path] = old_val + adjustment
        
        # Low material security
        if hasattr(world_slice, 'gdp_per_capita') and world_slice.gdp_per_capita < 5000:
            for path, adjustment in modifiers.get("low_material_security", {}).items():
                if path in modified_pattern:
                    old_val = modified_pattern[path]
                    if isinstance(old_val, PatternRange):
                        modified_pattern[path] = PatternRange(
                            old_val.mean + adjustment,
                            old_val.std,
                            old_val.min_val,
                            old_val.max_val
                        )
                    else:
                        modified_pattern[path] = old_val + adjustment
    
    # Parental warmth modifier
    if parental_warmth > 70:
        for path, adjustment in modifiers.get("high_parental_warmth", {}).items():
            if path in modified_pattern:
                old_val = modified_pattern[path]
                if isinstance(old_val, PatternRange):
                    modified_pattern[path] = PatternRange(
                        old_val.mean + adjustment,
                        old_val.std,
                        old_val.min_val,
                        old_val.max_val
                    )
                else:
                    modified_pattern[path] = old_val + adjustment
    
    # High parental authority
    if parental_authority > 70:
        for path, adjustment in modifiers.get("high_authoritarian_culture", {}).items():
            if path in modified_pattern:
                old_val = modified_pattern[path]
                if isinstance(old_val, PatternRange):
                    modified_pattern[path] = PatternRange(
                        old_val.mean + adjustment,
                        old_val.std,
                        old_val.min_val,
                        old_val.max_val
                    )
                else:
                    modified_pattern[path] = old_val + adjustment
    
    return modified_pattern


def _match_pattern_probabilistic(
    states: List,
    pattern: Dict[str, Union[float, PatternRange]]
) -> float:
    """
    Match states against a pattern dictionary using PROBABILITY DENSITY.
    
    Uses probability density functions instead of distance, allowing:
    - Variance in individual outcomes
    - Probabilistic matching (confluence of factors)
    - Not absolute determination
    """
    if not states or not pattern:
        return 0.0
    
    probabilities = []
    for path, pattern_value in pattern.items():
        # Get actual values from states
        values = []
        for state in states:
            # Handle paths like "needs.safety" or "strategies.perfectionism_control"
            if path.startswith("needs."):
                need_name = path.split('.', 1)[1]
                if hasattr(state, 'needs') and hasattr(state.needs, need_name):
                    values.append(getattr(state.needs, need_name))
            elif path.startswith("strategies."):
                strategy_name = path.split('.', 1)[1]
                if hasattr(state, 'strategies') and hasattr(state.strategies, strategy_name):
                    values.append(getattr(state.strategies, strategy_name))
            elif path.startswith("indices."):
                index_name = path.split('.', 1)[1]
                if hasattr(state, 'indices') and hasattr(state.indices, index_name):
                    values.append(getattr(state.indices, index_name))
            else:
                value = _evaluate_path(state, path)
                if value is not None:
                    values.append(value)
        
        if values:
            avg_value = np.mean(values)
            
            # Use probability density (probabilistic matching)
            if isinstance(pattern_value, PatternRange):
                # Get probability density at this value
                prob_density = pattern_value.probability_density(avg_value)
                # Convert to score (0-100)
                # Normalize: peak density (at mean) = 100, tails = lower
                max_density = pattern_value.probability_density(pattern_value.mean)
                if max_density > 0:
                    score = (prob_density / max_density) * 100
                else:
                    score = 0.0
            else:
                # Fallback: treat as PatternRange with default std
                pattern_range = PatternRange(pattern_value, std=15.0)
                prob_density = pattern_range.probability_density(avg_value)
                max_density = pattern_range.probability_density(pattern_range.mean)
                score = (prob_density / max_density) * 100 if max_density > 0 else 0.0
            
            probabilities.append(score)
    
    # Average probabilities (confluence of factors)
    return np.mean(probabilities) if probabilities else 0.0


def _match_strategies_probabilistic(
    states: List,
    wisdom: EnneagramTypeWisdom,
    context: Optional[Dict[str, Any]] = None
) -> float:
    """
    Match strategies against type wisdom (PROBABILISTIC).
    
    Primary strategies should be HIGH (but with variance),
    Avoided strategies should be LOW (but not necessarily zero).
    """
    if not states:
        return 0.0
    
    # Get average strategy values
    strategy_avgs = {}
    for state in states:
        for strategy_name in wisdom.primary_strategies + wisdom.secondary_strategies + wisdom.avoided_strategies:
            if hasattr(state.strategies, strategy_name):
                if strategy_name not in strategy_avgs:
                    strategy_avgs[strategy_name] = []
                strategy_avgs[strategy_name].append(getattr(state.strategies, strategy_name))
    
    # Probabilistic scoring: primary should be high (but allow variance)
    scores = []
    for strategy in wisdom.primary_strategies:
        if strategy in strategy_avgs:
            avg = np.mean(strategy_avgs[strategy])
            # Use probability density: high values (60-80) are most likely
            # But allow variance (some Type 1s might have lower perfectionism due to context)
            expected_range = PatternRange(70.0, std=20.0)  # Allow significant variance
            prob_density = expected_range.probability_density(avg)
            max_density = expected_range.probability_density(expected_range.mean)
            score = (prob_density / max_density) * 100 if max_density > 0 else 0.0
            scores.append(score)
    
    for strategy in wisdom.avoided_strategies:
        if strategy in strategy_avgs:
            avg = np.mean(strategy_avgs[strategy])
            # Avoided strategies should be LOW (but not necessarily zero)
            # Some variance allowed (context might force them)
            expected_range = PatternRange(20.0, std=15.0)  # Low, but with variance
            prob_density = expected_range.probability_density(avg)
            max_density = expected_range.probability_density(expected_range.mean)
            score = (prob_density / max_density) * 100 if max_density > 0 else 0.0
            scores.append(score)
    
    return np.mean(scores) if scores else 0.0


def _match_indices_probabilistic(
    states: List,
    wisdom: EnneagramTypeWisdom,
    context: Optional[Dict[str, Any]] = None
) -> float:
    """Match indices against type wisdom (PROBABILISTIC)"""
    if not states or not wisdom.typical_indices:
        return 0.0
    
    probabilities = []
    for index_name, pattern_value in wisdom.typical_indices.items():
        values = []
        for state in states:
            if hasattr(state.indices, index_name):
                values.append(getattr(state.indices, index_name))
        
        if values:
            avg_value = np.mean(values)
            
            # Use probability density
            if isinstance(pattern_value, PatternRange):
                prob_density = pattern_value.probability_density(avg_value)
                max_density = pattern_value.probability_density(pattern_value.mean)
                score = (prob_density / max_density) * 100 if max_density > 0 else 0.0
            else:
                # Fallback
                pattern_range = PatternRange(pattern_value, std=15.0)
                prob_density = pattern_range.probability_density(avg_value)
                max_density = pattern_range.probability_density(pattern_range.mean)
                score = (prob_density / max_density) * 100 if max_density > 0 else 0.0
            
            probabilities.append(score)
    
    return np.mean(probabilities) if probabilities else 0.0


def _evaluate_path(obj, path: str) -> Optional[float]:
    """Evaluate a dot-separated path on an object (PersonaState)"""
    parts = path.split('.')
    value = obj
    
    for part in parts:
        if hasattr(value, part):
            value = getattr(value, part)
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    
    # Handle nested attributes (e.g., "needs.safety" when obj is PersonaState)
    if isinstance(value, (int, float)):
        return float(value)
    return None

