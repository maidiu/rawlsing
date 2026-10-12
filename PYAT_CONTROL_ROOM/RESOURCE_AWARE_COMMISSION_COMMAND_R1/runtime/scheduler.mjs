export const DECISION_TYPES = Object.freeze({
  NO_ELIGIBLE_EXECUTION_RESOURCE: 'NO_ELIGIBLE_EXECUTION_RESOURCE',
  BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD: 'BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD',
  WAIT_FOR_RESET_OR_BUDGET_HOLD: 'WAIT_FOR_RESET_OR_BUDGET_HOLD',
  SHARED_POOL_EXHAUSTED: 'SHARED_POOL_EXHAUSTED',
  CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW: 'CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW',
  PRESERVE_ACTIVE_WORKTREE_AND_RESUME: 'PRESERVE_ACTIVE_WORKTREE_AND_RESUME',
  INTAKE_EXISTING_RETURN: 'INTAKE_EXISTING_RETURN',
  REVIEW_INELIGIBLE: 'REVIEW_INELIGIBLE',
  SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL: 'SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL',
  SCIENTIFIC_HOLD: 'SCIENTIFIC_HOLD',
  EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE: 'EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE',
  LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER: 'LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER',
  COUNT_SCIENTIFIC_PRODUCT: 'COUNT_SCIENTIFIC_PRODUCT',
  ADVISORY_ONLY_PUBLICATION_HOLD: 'ADVISORY_ONLY_PUBLICATION_HOLD',
  REQUIRE_FRESH_RESOURCE_EVIDENCE: 'REQUIRE_FRESH_RESOURCE_EVIDENCE',
  PROVIDER_PRIVACY_INELIGIBLE: 'PROVIDER_PRIVACY_INELIGIBLE',
  HALT_AND_PRESERVE_LOCAL_STATE: 'HALT_AND_PRESERVE_LOCAL_STATE',
  BLOCK_STARTUP_NO_CLONE_RESET: 'BLOCK_STARTUP_NO_CLONE_RESET',
  REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE: 'REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE',
  RESOURCE_INELIGIBLE_PROVIDER_POLICY: 'RESOURCE_INELIGIBLE_PROVIDER_POLICY',
  HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA: 'HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA',
  RUNTIME_UNPROVED: 'RUNTIME_UNPROVED',
  REQUIRES_RESOURCE_EVIDENCE: 'REQUIRES_RESOURCE_EVIDENCE',
  ADVISORY_ROUTE: 'ADVISORY_ROUTE',
  ELIGIBLE: 'ELIGIBLE',
  HOLD: 'HOLD'
});

const HARD_GATE_ORDER = Object.freeze([
  'source_privacy',
  'intelligence_risk',
  'host_runtime',
  'worktree_branch',
  'reviewer_independence',
  'scientific_authority',
  'budget_quota'
]);

function deepClone(obj) {
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(deepClone);
  const cloned = {};
  for (const key of Object.keys(obj)) {
    cloned[key] = deepClone(obj[key]);
  }
  return cloned;
}

function isNullish(value) {
  return value === null || value === undefined;
}

function isPositiveNumber(value) {
  return typeof value === 'number' && !Number.isNaN(value) && value > 0;
}

function isNonNegativeNumber(value) {
  return typeof value === 'number' && !Number.isNaN(value) && value >= 0;
}

function hasLocalExecutionCapability(resource) {
  if (resource.local_python === true) return true;
  if (resource.local_raw_custody === true) return true;
  if (resource.local_python === false) return false;
  if (resource.local_raw_custody === false) return false;
  if (resource.class === 'browser_github' || resource.class === 'browser') return false;
  return true;
}

function hasToolCapability(resource, tool) {
  if (!Array.isArray(resource.tools)) return null;
  return resource.tools.includes(tool);
}

function isBrowserOnly(resource) {
  return resource.class === 'browser_github' || resource.class === 'browser';
}

function isScienceRisk(risk) {
  return risk === 'issuer' || risk === 'security';
}

function isHighRisk(risk) {
  return risk === 'high';
}

function hasPrivacyViolation(context, resource) {
  if (context.provider_training === true && context.source_permission === false) {
    return true;
  }
  if (resource.source_privacy === 'TRAINING_ALLOWED' && context.source_permission === false) {
    return true;
  }
  return false;
}

function isLimitEvasionAttempt(context) {
  return context.secondary_go_account_intended_for_limit_evasion === true;
}

function hasSharedPoolExhausted(resource, quota) {
  if (resource.eligible_models && Array.isArray(resource.eligible_models)) {
    const totalFraction = resource.eligible_models.reduce((sum, m) => {
      return sum + (isNonNegativeNumber(m.fraction_used) ? m.fraction_used : 0);
    }, 0);
    if (totalFraction >= 1.0) return true;
  }
  if (isNonNegativeNumber(quota.normalized_remaining) && quota.normalized_remaining <= 0) {
    return true;
  }
  if (isNonNegativeNumber(resource.normalized_shared_remaining_fraction) &&
      resource.normalized_shared_remaining_fraction <= 0) {
    return true;
  }
  return false;
}

function hasActiveSession(task) {
  return task.status === 'EXISTING_ACTIVE_NOT_RETURNED';
}

function hasPushedReturn(task) {
  return task.status === 'PUSHED_READY_FOR_HQ_INTAKE';
}

function hasReviewerConflict(context) {
  return context.reviewer_same_as_implementer === true;
}

function hasWriteOverlap(context) {
  return context.write_overlap === true;
}

function hasMissingIssuer(context) {
  return context.issuer_credential === null;
}

function hasUnknownEstimates(context) {
  return context.cost_estimate === null && context.wall_estimate === null;
}

function hasStalePricing(context) {
  return context.pricing_freshness === 'STALE';
}

function hasRepeatedProviderFailure(context) {
  return context.provider_stream_failure_repeated === true;
}

function hasLocalCommittedWork(context) {
  return context.local_committed_work === true;
}

function hasUnknownRemote(context) {
  return context.remote_sha_unknown === true;
}

function hasMissingWorktree(context) {
  return context.worktree_missing === true;
}

function hasChangedCandidate(context) {
  if (isNullish(context.review_frozen_tip) || isNullish(context.candidate_tip)) return false;
  return context.review_frozen_tip !== context.candidate_tip;
}

function isAutoAstraEscalation(context) {
  return context.astra_only_because_two_retries === true && context.scientific_conflict !== true;
}

function isStaticOnlyEvidence(context) {
  return context.source_only_static_graph === true && context.executed_calls === 0;
}

function hasSlowBrowserWithLocalAlternative(context) {
  return context.browser_roundtrip_measured_slow === true && context.cheap_local_collector_available === true;
}

function isMeasuredNullWithConsumer(context) {
  return context.measured_supported_null === true && context.real_consumer === true;
}

function isUnqualifiedDispatcher(context) {
  return context.dispatcher_qualified === false;
}

function createDecision(type, provenance, recommendations = [], assumptions = [], counterfactuals = []) {
  return Object.freeze({
    decision: type,
    provenance: Object.freeze(provenance),
    recommendations: Object.freeze(recommendations),
    assumptions: Object.freeze(assumptions),
    counterfactuals: Object.freeze(counterfactuals)
  });
}

function evaluateHardGates(task, resources, quota, context) {
  const gates = [];
  const triggered = [];

  for (const resourceName of (context.available || [])) {
    const resource = resources.find(r => r.id === resourceName);
    if (!resource) {
      gates.push({ gate: 'resource_existence', resource: resourceName, pass: false, reason: 'Resource not found in snapshot' });
      triggered.push('resource_existence');
      continue;
    }
    gates.push({ gate: 'resource_existence', resource: resourceName, pass: true });
  }

  for (const resource of resources) {
    if (hasPrivacyViolation(context, resource)) {
      triggered.push('source_privacy');
      gates.push({ gate: 'source_privacy', resource: resource.id, pass: false, reason: 'Provider training with source permission denied' });
    }
  }
  if (resources.length > 0 && !triggered.includes('source_privacy')) {
    gates.push({ gate: 'source_privacy', pass: true });
  }

  if (isScienceRisk(task.risk) || isHighRisk(task.risk)) {
    const hasCompetentResource = resources.some(r =>
      r.class === 'browser_github' || r.class === 'strategic_oversight' ||
      (r.class === 'codex' && r.role && r.role.includes('premium'))
    );
    if (!hasCompetentResource && resources.length > 0) {
      triggered.push('intelligence_risk');
      gates.push({ gate: 'intelligence_risk', pass: false, reason: 'No high-competence resource for risk level' });
    } else {
      gates.push({ gate: 'intelligence_risk', pass: true });
    }
  } else {
    gates.push({ gate: 'intelligence_risk', pass: true });
  }

  const needsLocalExecution = task.needs.some(n =>
    n === 'python' || n === 'pytest' || n === 'sigkill' || n === 'native_c' || n === 'mac_fs'
  );

  if (needsLocalExecution) {
    const hasLocalCapability = resources.some(r => hasLocalExecutionCapability(r) === true);
    const onlyBrowser = resources.length > 0 && resources.every(r => isBrowserOnly(r));
    if (onlyBrowser || !hasLocalCapability) {
      triggered.push('host_runtime');
      gates.push({ gate: 'host_runtime', pass: false, reason: 'No local execution capability for required task needs' });
    } else {
      gates.push({ gate: 'host_runtime', pass: true });
    }
  } else {
    gates.push({ gate: 'host_runtime', pass: true });
  }

  if (hasUnknownRemote(context) || hasMissingWorktree(context)) {
    triggered.push('worktree_branch');
    gates.push({ gate: 'worktree_branch', pass: false, reason: 'Worktree or remote state unknown/missing' });
  } else {
    gates.push({ gate: 'worktree_branch', pass: true });
  }

  if (hasReviewerConflict(context)) {
    triggered.push('reviewer_independence');
    gates.push({ gate: 'reviewer_independence', pass: false, reason: 'Reviewer same as implementer' });
  } else {
    gates.push({ gate: 'reviewer_independence', pass: true });
  }

  if (hasMissingIssuer(context) && isScienceRisk(task.risk)) {
    triggered.push('scientific_authority');
    gates.push({ gate: 'scientific_authority', pass: false, reason: 'Missing scientific issuer credential' });
  } else {
    gates.push({ gate: 'scientific_authority', pass: true });
  }

  const budgetExhausted = isNonNegativeNumber(quota.normalized_remaining) && quota.normalized_remaining <= 0;
  const overflowDisabled = quota.overflow_enabled === false;
  if (budgetExhausted && overflowDisabled) {
    triggered.push('budget_quota');
    gates.push({ gate: 'budget_quota', pass: false, reason: 'Budget exhausted and overflow disabled' });
  } else {
    gates.push({ gate: 'budget_quota', pass: true });
  }

  return { gates, triggered };
}

function scoreResource(resource, task, quota) {
  let score = 0;
  const factors = [];

  if (resource.local_python === true) {
    score += 10;
    factors.push({ factor: 'local_execution', weight: 10 });
  }

  if (resource.local_raw_custody === true) {
    score += 5;
    factors.push({ factor: 'raw_custody', weight: 5 });
  }

  if (resource.class === 'codex' && isPositiveNumber(resource.remaining_usage)) {
    score += Math.min(resource.remaining_usage / 10, 10);
    factors.push({ factor: 'codex_remaining', weight: Math.min(resource.remaining_usage / 10, 10) });
  }

  if (resource.class === 'subscription_pool') {
    const remaining = isNonNegativeNumber(quota.normalized_remaining) ? quota.normalized_remaining : 0.5;
    score += remaining * 10;
    factors.push({ factor: 'pool_remaining', weight: remaining * 10 });
  }

  if (resource.class === 'metered_local' && isNonNegativeNumber(resource.cost_usd)) {
    score += Math.max(0, 10 - resource.cost_usd);
    factors.push({ factor: 'cost_efficiency', weight: Math.max(0, 10 - resource.cost_usd) });
  }

  if (resource.can_act_as_runtime_reviewer === true) {
    score += 3;
    factors.push({ factor: 'review_capability', weight: 3 });
  }

  if (task.critical_path === true && resource.class !== 'browser_github') {
    score += 2;
    factors.push({ factor: 'critical_path', weight: 2 });
  }

  const toolMatch = task.needs.filter(n => hasToolCapability(resource, n)).length;
  score += toolMatch * 3;
  if (toolMatch > 0) {
    factors.push({ factor: 'tool_match', weight: toolMatch * 3 });
  }

  return { score, factors };
}

export function createScheduler(config = {}) {
  const weights = config.weights || {};

  function advise(input) {
    if (input === null || input === undefined || typeof input !== 'object') {
      return createDecision(
        DECISION_TYPES.REQUIRES_RESOURCE_EVIDENCE,
        { hard_gates: ['input_validation'], triggered: ['invalid_input'] },
        [{ action: 'REJECT', reason: 'Invalid or missing input' }],
        ['Scheduler requires valid input object'],
        ['Re-submit with valid task, resources, and quota']
      );
    }
    const task = deepClone(input.task) || {};
    if (!Array.isArray(task.needs)) {
      task.needs = [];
    }
    const resources = Array.isArray(input.resources) ? deepClone(input.resources) : [];
    const quota = deepClone(input.quota) || {};
    const context = deepClone(input) || {};

    const available = context.available || resources.map(r => r.id);

    if (isLimitEvasionAttempt(context)) {
      return createDecision(
        DECISION_TYPES.RESOURCE_INELIGIBLE_PROVIDER_POLICY,
        { hard_gates: ['provider_policy'], triggered: ['limit_evasion'] },
        [{ action: 'REJECT', reason: 'Account intended for usage limit evasion' }],
        ['Provider policy forbids extra accounts for limit circumvention'],
        ['If legitimate separate subscription: re-submit with independent entitlement evidence']
      );
    }

    if (hasActiveSession(task)) {
      return createDecision(
        DECISION_TYPES.PRESERVE_ACTIVE_WORKTREE_AND_RESUME,
        { hard_gates: ['active_session'], triggered: ['existing_active'] },
        [{ action: 'RESUME', reason: 'Existing active session with unpushed work' }],
        ['Active session takes priority over new assignment'],
        ['If session is stale: require exact forensic attestation before reset']
      );
    }

    if (hasPushedReturn(task)) {
      return createDecision(
        DECISION_TYPES.INTAKE_EXISTING_RETURN,
        { hard_gates: ['return_state'], triggered: ['pushed_return'] },
        [{ action: 'INTAKE', reason: 'Pushed return ready for HQ review' }],
        ['Pushed return is not adopted; no reimplementation'],
        ['HQ may adopt through competent decision']
      );
    }

    if (hasReviewerConflict(context)) {
      return createDecision(
        DECISION_TYPES.REVIEW_INELIGIBLE,
        { hard_gates: ['reviewer_independence'], triggered: ['reviewer_conflict'] },
        [{ action: 'REJECT_REVIEW', reason: 'Reviewer same as implementer' }],
        ['Review independence cannot be waived by scheduling convenience'],
        ['Assign independent reviewer for valid review']
      );
    }

    if (hasWriteOverlap(context)) {
      const recommendations = [{ action: 'SERIALIZE', reason: 'Colliding write paths detected' }];
      if (context.otherwise_independent_lane_ready === true) {
        recommendations.push({ action: 'CONTINUE_ORTHOGONAL', reason: 'Non-overlapping work can proceed' });
      }
      return createDecision(
        DECISION_TYPES.SERIALIZE_COLLIDING_WRITES_CONTINUE_ORTHOGONAL,
        { hard_gates: ['write_collision'], triggered: ['write_overlap'] },
        recommendations,
        ['No fixed global two-slot cap; serialize only colliding paths'],
        ['If lanes diverge: both may proceed concurrently']
      );
    }

    if (hasChangedCandidate(context)) {
      return createDecision(
        DECISION_TYPES.REVIEW_INVALIDATED_BY_CHANGED_CANDIDATE,
        { hard_gates: ['review_binding'], triggered: ['candidate_changed'] },
        [{ action: 'REJECT_REVIEW', reason: 'Candidate changed after review' }],
        ['Independent review bound to exact candidate tip'],
        ['Re-review required on new candidate tip']
      );
    }

    if (hasRepeatedProviderFailure(context) && hasLocalCommittedWork(context)) {
      return createDecision(
        DECISION_TYPES.HALT_AND_PRESERVE_LOCAL_STATE,
        { hard_gates: ['provider_stability'], triggered: ['repeated_failure'] },
        [{ action: 'HALT', reason: 'Repeated provider failures with local state at risk' }],
        ['Avoid model loops and lost state'],
        ['After mechanism diagnosis: retry with fixed configuration']
      );
    }

    if (hasUnknownRemote(context) || hasMissingWorktree(context)) {
      return createDecision(
        DECISION_TYPES.BLOCK_STARTUP_NO_CLONE_RESET,
        { hard_gates: ['worktree_branch'], triggered: ['unknown_remote_or_missing_worktree'] },
        [{ action: 'BLOCK', reason: 'Worktree or remote state unknown' }],
        ['Explicit bootstrap owner required'],
        ['After HQ-authorized bootstrap: re-submit with verified worktree']
      );
    }

    if (isAutoAstraEscalation(context)) {
      return createDecision(
        DECISION_TYPES.HQ_ROOT_CAUSE_REVIEW_NOT_AUTO_ASTRA,
        { hard_gates: ['escalation_policy'], triggered: ['auto_astra'] },
        [{ action: 'ROOT_CAUSE', reason: 'Repetition alone is not strategic escalation' }],
        ['Astra reserved for constitutional/semantic conflict or explicit user direction'],
        ['If genuine scientific conflict: escalate to Astra with evidence']
      );
    }

    if (isStaticOnlyEvidence(context)) {
      return createDecision(
        DECISION_TYPES.RUNTIME_UNPROVED,
        { hard_gates: ['runtime_evidence'], triggered: ['static_only'] },
        [{ action: 'REQUIRE_RUNTIME', reason: 'Static repo text is not executed owner chain' }],
        ['No runtime execution evidence available'],
        ['Execute and collect runtime evidence before claiming product']
      );
    }

    if (isUnqualifiedDispatcher(context)) {
      return createDecision(
        DECISION_TYPES.ADVISORY_ONLY_PUBLICATION_HOLD,
        { hard_gates: ['dispatcher_qualification'], triggered: ['unqualified_dispatcher'] },
        [{ action: 'ADVISORY_ONLY', reason: 'Dispatcher not independently qualified' }],
        ['Unqualified Space Bunny candidate never launches/publishes'],
        ['After separate qualification: re-evaluate dispatch candidate']
      );
    }

    if (isMeasuredNullWithConsumer(context)) {
      return createDecision(
        DECISION_TYPES.COUNT_SCIENTIFIC_PRODUCT,
        { hard_gates: ['product_counting'], triggered: ['measured_null_with_consumer'] },
        [{ action: 'COUNT_PRODUCT', reason: 'Measured supported null with real consumer' }],
        ['Measured null differs from pipeline failure'],
        ['If no consumer: do not count as product']
      );
    }

    if (hasSlowBrowserWithLocalAlternative(context)) {
      return createDecision(
        DECISION_TYPES.LOCAL_EVIDENCE_COLLECTOR_WITH_BROWSER_HQ_OWNER,
        { hard_gates: ['latency_optimization'], triggered: ['slow_browser_fast_local'] },
        [
          { action: 'USE_LOCAL_COLLECTOR', reason: 'Cheap local evidence collection available' },
          { action: 'BROWSER_HQ_OWNER', reason: 'Browser retains scientific adjudication' }
        ],
        ['No compulsory free-first latency rule'],
        ['If local collector unavailable: use Browser with measured latency']
      );
    }

    if (hasMissingIssuer(context) && isScienceRisk(task.risk)) {
      return createDecision(
        DECISION_TYPES.SCIENTIFIC_HOLD,
        { hard_gates: ['scientific_authority'], triggered: ['missing_issuer'] },
        [{ action: 'HOLD', reason: 'No qualified source/operation/EE12/EE13/model-use issuer' }],
        ['No model can invent competent issuer'],
        ['After competent issuer appointed: re-evaluate']
      );
    }

    const needsLocalExecution = task.needs.some(n =>
      n === 'python' || n === 'pytest' || n === 'sigkill' || n === 'native_c' || n === 'mac_fs'
    );

    if (needsLocalExecution) {
      const onlyBrowser = resources.length > 0 && resources.every(r => isBrowserOnly(r));
      const hasLocalCapability = resources.some(r => hasLocalExecutionCapability(r) === true);

      if (onlyBrowser || !hasLocalCapability) {
        return createDecision(
          DECISION_TYPES.NO_ELIGIBLE_EXECUTION_RESOURCE,
          { hard_gates: ['host_runtime'], triggered: ['no_local_capability'] },
          [{ action: 'NO_ELIGIBLE', reason: 'No local execution capability for required task needs' }],
          ['Browser never manufactures runtime PASS'],
          ['If local executor qualified: pair with Browser scientific owner']
        );
      }
    }

    for (const resource of resources) {
      if (hasPrivacyViolation(context, resource)) {
        return createDecision(
          DECISION_TYPES.PROVIDER_PRIVACY_INELIGIBLE,
          { hard_gates: ['source_privacy'], triggered: ['privacy_violation'] },
          [{ action: 'REJECT', reason: 'Provider privacy terms violate custody requirements' }],
          ['No cost advantage defeats privacy'],
          ['If provider terms change: re-evaluate with evidence']
        );
      }
    }

    if (isScienceRisk(task.risk) && resources.length > 0) {
      const hasCompetentResource = resources.some(r =>
        r.class === 'browser_github' || r.class === 'strategic_oversight' ||
        (r.class === 'codex' && r.role && r.role.includes('premium'))
      );
      const hasCheapResource = resources.some(r =>
        r.class === 'metered_local' || r.class === 'subscription_pool'
      );

      if (hasCheapResource && !hasCompetentResource) {
        return createDecision(
          DECISION_TYPES.BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD,
          { hard_gates: ['intelligence_risk', 'scientific_authority'], triggered: ['science_risk_no_competent'] },
          [
            { action: 'BROWSER_OWNER', reason: 'Browser HQ as science owner' },
            { action: 'SCIENTIFIC_HOLD', reason: 'Cheap extractor cannot self-issue' }
          ],
          ['Cheap extractor never self-issues scientific authority'],
          ['After Browser qualification: re-evaluate']
        );
      }

      if (hasCheapResource && hasCompetentResource) {
        return createDecision(
          DECISION_TYPES.BROWSER_SCIENCE_OWNER_OR_SCIENTIFIC_HOLD,
          { hard_gates: ['intelligence_risk', 'scientific_authority'], triggered: ['science_risk_mixed_resources'] },
          [
            { action: 'BROWSER_OWNER', reason: 'Browser HQ as science owner' },
            { action: 'SCIENTIFIC_HOLD', reason: 'Cheap extractor cannot self-issue' }
          ],
          ['Cheap extractor never self-issues scientific authority'],
          ['After Browser qualification: re-evaluate']
        );
      }
    }

    if (resources.length > 0 && hasSharedPoolExhausted(resources[0], quota) && quota.overflow_enabled !== true) {
      const decisionType = resources[0] && resources[0].eligible_models && resources[0].eligible_models.length > 1
        ? DECISION_TYPES.SHARED_POOL_EXHAUSTED
        : DECISION_TYPES.WAIT_FOR_RESET_OR_BUDGET_HOLD;

      return createDecision(
        decisionType,
        { hard_gates: ['budget_quota'], triggered: ['pool_exhausted'] },
        [{ action: 'WAIT', reason: 'Shared pool exhausted, overflow disabled' }],
        ['No unapproved Zen spend', 'One Go pooled allowance not multiplied per model'],
        ['After reset or budget increase: re-evaluate']
      );
    }

    const hasCodexAExhausted = resources.some(r => r.id === 'CODEX_A' && isNonNegativeNumber(r.remaining_usage) && r.remaining_usage <= 0);
    const hasCodexBUsable = resources.some(r => r.id === 'CODEX_B' && (isPositiveNumber(r.remaining_usage) || r.remaining_usage === 'MEASURED_POSITIVE'));

    if (hasCodexAExhausted && hasCodexBUsable) {
      return createDecision(
        DECISION_TYPES.CONSIDER_CODEX_B_IF_INDEPENDENCE_AND_BUDGET_ALLOW,
        { hard_gates: ['budget_quota'], triggered: ['codex_a_exhausted_b_usable'] },
        [{ action: 'CONSIDER_CODEX_B', reason: 'Codex A exhausted, Codex B has remaining budget' }],
        ['B unobserved entitlement cannot be inferred from account name', 'Independence and budget must be verified'],
        ['If B quota or privacy cannot be verified: require fresh evidence']
      );
    }

    if (hasUnknownEstimates(context)) {
      return createDecision(
        DECISION_TYPES.EXPLICIT_ESTIMATE_UNKNOWN_OR_BOUNDED_PROBE,
        { hard_gates: ['estimation'], triggered: ['unknown_estimates'] },
        [{ action: 'BOUNDED_PROBE', reason: 'Cost and time estimates unknown' }],
        ['Unknown is not zero'],
        ['After bounded probe: use measured estimates']
      );
    }

    if (hasStalePricing(context) || (isNullish(quota.normalized_remaining) && resources.length > 0)) {
      return createDecision(
        DECISION_TYPES.REQUIRE_FRESH_RESOURCE_EVIDENCE,
        { hard_gates: ['budget_quota'], triggered: ['stale_pricing_or_unknown_quota'] },
        [{ action: 'REFRESH', reason: 'Stale pricing or unknown quota' }],
        ['No fictional usage balances'],
        ['After fresh evidence: re-evaluate eligibility']
      );
    }

    const { gates, triggered } = evaluateHardGates(task, resources, quota, context);

    const eligibleResources = [];
    for (const resource of resources) {
      const { score, factors } = scoreResource(resource, task, quota);
      eligibleResources.push({ resource, score, factors });
    }

    eligibleResources.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.resource.id.localeCompare(b.resource.id);
    });

    if (eligibleResources.length === 0) {
      return createDecision(
        DECISION_TYPES.NO_ELIGIBLE_EXECUTION_RESOURCE,
        { hard_gates: HARD_GATE_ORDER, triggered: ['no_eligible_after_gates'] },
        [{ action: 'NO_ELIGIBLE', reason: 'No resources passed hard gates' }],
        ['All resources ineligible after hard gate evaluation'],
        ['Re-submit with additional or refreshed resources']
      );
    }

    const topChoice = eligibleResources[0];
    const recommendations = [{
      action: 'ADVISORY_ROUTE',
      resource: topChoice.resource.id,
      score: topChoice.score,
      reason: `Highest scored eligible resource: ${topChoice.resource.id}`
    }];

    for (const alt of eligibleResources.slice(1)) {
      recommendations.push({
        action: 'ALTERNATIVE',
        resource: alt.resource.id,
        score: alt.score,
        reason: `Lower scored alternative: ${alt.resource.id}`
      });
    }

    const counterfactuals = eligibleResources.slice(1).map(alt => ({
      if: `If ${alt.resource.id} were selected instead`,
      tradeoff: `Score difference: ${(topChoice.score - alt.score).toFixed(2)}`
    }));

    return createDecision(
      DECISION_TYPES.ADVISORY_ROUTE,
      { hard_gates: HARD_GATE_ORDER, triggered: [] },
      recommendations,
      ['Estimates are explicitly observed or hypothetical, never 0 for missing', 'Configurable weights applied after hard gates', 'Deterministic tie-break by resource ID'],
      counterfactuals
    );
  }

  return Object.freeze({ advise });
}

export default { createScheduler, DECISION_TYPES };
