/**
 * SEAM/11: Tiny executable reference for the SEAM/10 discriminator matrix.
 * Run: node SEAM/11_SOROK_SOURCEFREE_PRACTICAL_PREMISE_PROBE_R1.mjs
 *
 * GRADE: SOURCEFREE TOY / ZERO measured respondents / ZERO psych science /
 *        ZERO CAN-P3-PFF product integration / ZERO original35 proof.
 * Values for WVS7 Q8/Q17 are HYPOTHETICAL and never sourced from a respondent.
 * Toy ages are scenario eligibility gates, NOT empirical child-development laws.
 */
import assert from "node:assert/strict";

const D = { Q8_independence_mentioned: true, Q17_obedience_mentioned: true };
const world = { employer_sanctions_shift_request: true };
function state() {
  return {
    anticipated: Object.create(null),
    practiced: Object.create(null),
    heard: [],
    inferred_hidden_cause: [],
    endorsed: [],
  };
}
function kExpressive({ age = 8, present = true } = {}) {
  return {
    id: "K-E:spoken-principle",
    context: "home",
    kind: "speech",
    report: D.Q8_independence_mentioned ? "Try deciding for yourself" : "ordinary talk",
    result: "none",
    age, seen: present, participated: false, causeVisible: true,
  };
}
function kPractical({ age = 8, present = true, sanction = world.employer_sanctions_shift_request } = {}) {
  return {
    id: "K-P:shift-request",
    context: "work",
    kind: "request_change",
    report: "caregiver asks supervisor for a shift accommodation",
    result: sanction ? "sanction" : "accepted",
    age, seen: present, participated: false, causeVisible: false,
  };
}
function childPractice({ age = 11, participated = true, present = true } = {}) {
  return {
    id: "CHILD:peer-organization",
    context: "peer",
    kind: "organize",
    report: "child organizes a work-sharing task",
    result: "accepted",
    age, seen: present, participated, causeVisible: true,
  };
}
function uptakePredictive(h, e) {
  if (!e.seen) return h; // no child event
  if (e.kind === "speech") {
    if (e.age >= 3) h.heard.push(e.id);
    return h; // spoken expectation is not a sanction or endorsement
  }
  if (e.age >= 6) {
    const key = e.context + ":" + e.kind;
    (h.anticipated[key] ??= []).push(e.result);
    if (!e.causeVisible) h.inferred_hidden_cause.push("UNKNOWN@" + e.id);
  }
  return h;
}
function uptakeParticipatory(h, e) {
  if (!e.seen) return h;
  if (e.kind === "speech") {
    if (e.age >= 3) h.heard.push(e.id);
    return h;
  }
  if (e.age >= 6 && e.participated && e.result === "accepted") {
    const key = e.context + ":" + e.kind;
    (h.practiced[key] ??= []).push(e.id);
  }
  return h;
}
const tests = [];
function check(label, callback) {
  callback();
  tests.push(label);
}
const witnessed = uptakePredictive(state(), kPractical());
check("witnessed institutional sanction => predicted cost, not endorsement", () => {
  assert.deepEqual(witnessed.anticipated["work:request_change"], ["sanction"]);
  assert.deepEqual(witnessed.endorsed, []);
});
check("unseen underlying cause remains UNKNOWN", () => {
  assert.deepEqual(witnessed.inferred_hidden_cause, ["UNKNOWN@K-P:shift-request"]);
});
check("unseen adult act => no child normative learning", () => {
  assert.equal(Object.keys(uptakePredictive(state(), kPractical({ present: false })).anticipated).length, 0);
});
check("spoken norm => heard only, not enacted sanction or internalization", () => {
  const h = uptakePredictive(state(), kExpressive());
  assert.equal(h.heard.length, 1);
  assert.equal(Object.keys(h.anticipated).length, 0);
  assert.deepEqual(h.endorsed, []);
});
const coordinated = uptakeParticipatory(uptakeParticipatory(state(), kPractical()), childPractice());
check("child's actual participation yields a bounded practiced competence", () => {
  assert.deepEqual(coordinated.practiced["peer:organize"], ["CHILD:peer-organization"]);
  assert.equal(Object.keys(coordinated.anticipated).length, 0);
});
check("mere observation of a practice is not actual practiced skill", () => {
  assert.equal(Object.keys(uptakeParticipatory(state(), childPractice({ participated: false })).practiced).length, 0);
});
check("same D, changed real institution => changed anticipated cost", () => {
  const h = uptakePredictive(state(), kPractical({ sanction: false }));
  assert.deepEqual(h.anticipated["work:request_change"], ["accepted"]);
});
check("infant does not acquire propositional norm merely from speech", () => {
  assert.equal(uptakePredictive(state(), kExpressive({ age: 1 })).heard.length, 0);
});
check("work-risk premise and peer competence remain jointly possible", () => {
  const h = uptakeParticipatory(uptakePredictive(state(), kPractical()), childPractice());
  assert.deepEqual(h.anticipated["work:request_change"], ["sanction"]);
  assert.deepEqual(h.practiced["peer:organize"], ["CHILD:peer-organization"]);
});
check("same adult D; alter K or U => distinguishable later actor evidence", () => {
  const speech = uptakePredictive(state(), kExpressive());
  assert.notDeepEqual(speech.anticipated, witnessed.anticipated);
  assert.notDeepEqual(coordinated.practiced, witnessed.practiced);
});
console.log(JSON.stringify({
  test_grade: "SOURCEFREE_TOY_NOT_PRODUCT",
  pass: tests.length,
  total: 10,
  checks: tests,
  sample_count: 0,
  source_native_persons: 0,
  native_psych_authority: false,
}, null, 2));
