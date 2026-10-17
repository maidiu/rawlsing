"use strict";
// Pure synthetic boundary runner; NOT an accepted V3 event/effect engine.
const judge=function judge(p){
 const a=p.actor,w=p.world,c=p.candidate,F=(code)=>({decision:"REFUSED",code,mutations:0});
 if(!a||!w||!c)return F("MISSING_PACKET");
 if(a.phase!=="V3DP_DEVELOPMENT_ACTIVE"||(a.segments||[]).length)return F("UNGOVERNED_ADP008_PHASE");
 if(!w.events.includes(c.event))return F("UNADMITTED_EVENT");
 if(c.age_shortcut)return F("AGE_SHORTCUT_REFUSED");
 if(c.retrocausal||c.time>w.now)return F("TEMPORAL_INTEGRITY");
 if(c.other_private)return F("UNAUTHORIZED_PRIVATE_MIND");
 for(const r of c.access||[])if(!a.access.includes(r))return F("ACTOR_ACCESS_MISSING");
 for(const r of c.utterances||[])if(!w.utterances.includes(r))return F("UTTERANCE_NOT_ADMITTED");
 for(const id of c.requires||[]){
  const x=a.capabilities[id];
  if(!x||x.status==="CAPABILITY_UNKNOWN")return F("CAPABILITY_UNKNOWN");
  if(x.status==="CAPABILITY_ABSENT")return F("CAPABILITY_ABSENT");
  if(x.actor!==a.id||x.id!==id||!x.witness?.length||!x.scope)return F("WITNESS_OR_ACTOR_INVALID");
  if(x.status==="CAPABILITY_CONDITIONED"&&!x.conditions.every(t=>a.facts.includes(t)))return F("CONDITION_UNMET");
  if(!["CAPABILITY_PRESENT","CAPABILITY_CONDITIONED"].includes(x.status))return F("INVALID_STATUS");
  if(x.from>w.now||(x.until&&w.now>=x.until))return F("CAPABILITY_NOT_CURRENT");
 }
 if(c.other&&!w.independent_actors.includes(c.other))return F("OTHER_ACTOR_NOT_GENERATED");
 if(c.durable&&!c.registered_effect_rule)return {decision:"PROPOSABLE_ONLY",code:"EFFECT_OWNER_UNISSUED",mutations:0};
 return {decision:"PROPOSABLE_ONLY",code:"NO_ACTOR_MUTATION",mutations:0};
};
const tests=[
  {
    "name": "affect first",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "NO_ACTOR_MUTATION"
  },
  {
    "name": "explicit recall unknown",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C05"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "CAPABILITY_UNKNOWN"
  },
  {
    "name": "same age not grant recall",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 19,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C05"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "CAPABILITY_UNKNOWN"
  },
  {
    "name": "absence genuinely distinct",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_ABSENT",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C05"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "CAPABILITY_ABSENT"
  },
  {
    "name": "no abstract comparison by age",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C07"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "CONDITION_UNMET"
  },
  {
    "name": "comparison practice enables proposal",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [
          "two_voices_learned"
        ],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C07"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "NO_ACTOR_MUTATION"
  },
  {
    "name": "peer claim sourced",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [
          "two_voices_learned"
        ],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C07"
        ],
        "access": [
          "parent_quote",
          "peer_quote"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ]
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "NO_ACTOR_MUTATION"
  },
  {
    "name": "peer accusation invented",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ],
        "utterances": [
          "unsupported_quote"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "UTTERANCE_NOT_ADMITTED"
  },
  {
    "name": "child did not hear parent",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "unheard"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "ACTOR_ACCESS_MISSING"
  },
  {
    "name": "cannot read other private motives",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ],
        "other_private": true
      }
    },
    "decision": "REFUSED",
    "code": "UNAUTHORIZED_PRIVATE_MIND"
  },
  {
    "name": "partner genuinely independently generated",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "peer_meeting",
        "time": "2026-10-17",
        "requires": [
          "C12"
        ],
        "other": "other_P"
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "NO_ACTOR_MUTATION"
  },
  {
    "name": "invented crush target",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "peer_meeting",
        "time": "2026-10-17",
        "requires": [
          "C12"
        ],
        "other": "ghost"
      }
    },
    "decision": "REFUSED",
    "code": "OTHER_ACTOR_NOT_GENERATED"
  },
  {
    "name": "past immutable",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ],
        "retrocausal": true
      }
    },
    "decision": "REFUSED",
    "code": "TEMPORAL_INTEGRITY"
  },
  {
    "name": "future unavailable",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2029-01-01",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "TEMPORAL_INTEGRITY"
  },
  {
    "name": "reject age only",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ],
        "age_shortcut": true
      }
    },
    "decision": "REFUSED",
    "code": "AGE_SHORTCUT_REFUSED"
  },
  {
    "name": "reject fake adolescent phase",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [
          "V3DP_AGE12"
        ],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "UNGOVERNED_ADP008_PHASE"
  },
  {
    "name": "tampered provenance",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "other",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "WITNESS_OR_ACTOR_INVALID"
  },
  {
    "name": "missing witness",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "WITNESS_OR_ACTOR_INVALID"
  },
  {
    "name": "capability expired",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01",
            "until": "2026-09-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "CAPABILITY_NOT_CURRENT"
  },
  {
    "name": "green competence not effect authority",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ],
        "durable": true
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "EFFECT_OWNER_UNISSUED"
  },
  {
    "name": "unrelated explicit memory absence leaves affect",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_ABSENT",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "bike_theft",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "PROPOSABLE_ONLY",
    "code": "NO_ACTOR_MUTATION"
  },
  {
    "name": "unadmitted objective culprit",
    "packet": {
      "actor": {
        "id": "X",
        "phase": "V3DP_DEVELOPMENT_ACTIVE",
        "segments": [],
        "age": 12,
        "access": [
          "theft",
          "parent_quote",
          "peer_quote"
        ],
        "facts": [],
        "capabilities": {
          "C02": {
            "actor": "X",
            "id": "C02",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "cry_observed"
            ],
            "scope": "garage",
            "from": "2026-01-01"
          },
          "C05": {
            "actor": "X",
            "id": "C05",
            "status": "CAPABILITY_UNKNOWN",
            "witness": [],
            "scope": "memory",
            "from": "2026-01-01"
          },
          "C07": {
            "actor": "X",
            "id": "C07",
            "status": "CAPABILITY_CONDITIONED",
            "witness": [
              "comparison-practice"
            ],
            "scope": "school",
            "conditions": [
              "two_voices_learned"
            ],
            "from": "2026-01-01"
          },
          "C12": {
            "actor": "X",
            "id": "C12",
            "status": "CAPABILITY_PRESENT",
            "witness": [
              "interest_observed"
            ],
            "scope": "school",
            "from": "2026-01-01"
          }
        }
      },
      "world": {
        "events": [
          "bike_theft",
          "peer_meeting"
        ],
        "utterances": [
          "parent_quote",
          "peer_quote"
        ],
        "independent_actors": [
          "other_P"
        ],
        "now": "2026-10-17"
      },
      "candidate": {
        "event": "unknown_thief_identity",
        "time": "2026-10-17",
        "requires": [
          "C02"
        ],
        "access": [
          "theft"
        ]
      }
    },
    "decision": "REFUSED",
    "code": "UNADMITTED_EVENT"
  }
];
let passed=0;
for(const t of tests){const r=judge(t.packet);if(r.decision!==t.decision||r.code!==t.code||r.mutations!==0){console.error("RED",t.name,r);process.exitCode=1;}else{console.log("PASS",t.name);passed++;}}
console.log("D1",passed,"/",tests.length,"PASS");
