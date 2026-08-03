-- Rawlsing P3 logical validation queries v2. Read-only.
-- Run after loading a shadow P3 release.

-- Q01: exactly one runtime promotion pointer row.
SELECT CASE WHEN COUNT(*)=1 THEN 'PASS' ELSE 'FAIL' END AS q01_single_promotion_pointer FROM p3_runtime_promotion_pointer;

-- Q02: pointer release has a PROMOTED status event.
SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM p3_runtime_promotion_pointer p
  WHERE NOT EXISTS (SELECT 1 FROM p3_release_status_event e WHERE e.release_id=p.promoted_release_id AND e.status='PROMOTED')
) THEN 'PASS' ELSE 'FAIL' END AS q02_pointer_has_promoted_event;

-- Q03: all pair endpoints differ and resolve (foreign keys also enforce resolution).
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q03_no_reflexive_pairs FROM p3_pair_fact_bundle WHERE left_object_id=right_object_id;

-- Q04: only proposition relations create candidate connectivity.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q04_connectivity_types
FROM p3_pair_fact_bundle WHERE connectivity_allowed AND relation_type NOT IN ('PROPOSITION_RESPONSE_IDENTITY','PROPOSITION_IDENTITY_ONLY');

-- Q05: paths never create endpoint authority.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q05_no_path_authority
FROM p3_pair_fact_bundle WHERE creates_endpoint_authority;

-- Q06: every pair fact has exactly one governing P2 source authority.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q06_one_governing_source
FROM p3_pair_fact_bundle p LEFT JOIN (
 SELECT pair_fact_id,COUNT(*) FILTER (WHERE governing) n FROM p3_pair_fact_source_authority GROUP BY pair_fact_id
) s ON s.pair_fact_id=p.pair_fact_id WHERE COALESCE(s.n,0)<>1;

-- Q07: candidate internal-pair rows equal n(n-1)/2.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q07_complete_pair_matrix
FROM p3_candidate_revision r
JOIN (SELECT candidate_revision_id,COUNT(*) n FROM p3_candidate_membership GROUP BY candidate_revision_id) m USING(candidate_revision_id)
LEFT JOIN (SELECT candidate_revision_id,COUNT(*) n FROM p3_internal_pair_matrix GROUP BY candidate_revision_id) x USING(candidate_revision_id)
WHERE COALESCE(x.n,0) <> (m.n*(m.n-1))/2;

-- Q08: no clean candidate contains a direct collision, unresolved obligation, or signature conflict.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q08_clean_candidate_blockers
FROM p3_candidate_revision r
WHERE r.candidate_classification='CLEAN_FAMILY_CANDIDATE' AND EXISTS (
 SELECT 1 FROM p3_internal_pair_matrix x WHERE x.candidate_revision_id=r.candidate_revision_id AND x.pair_state IN ('DIRECT_COLLISION','SIGNATURE_CONFLICT')
 UNION ALL
 SELECT 1 FROM p3_closure_obligation o WHERE o.candidate_revision_id=r.candidate_revision_id AND o.status='OPEN'
);

-- Q09: every canonical-family revision has at least two members and a complete signature.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q09_family_revision_complete
FROM p3_canonical_family_revision f
JOIN p3_proposition_signature s ON s.signature_id=f.canonical_signature_id
LEFT JOIN (SELECT family_revision_id,COUNT(*) n FROM p3_canonical_family_membership GROUP BY family_revision_id) m USING(family_revision_id)
WHERE COALESCE(m.n,0)<2 OR s.signature_status<>'COMPLETE';

-- Q10: P3 never authorizes response transformations.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q10_no_measurement_leak
FROM p3_family_variant_revision WHERE value_portability_status<>'NOT_AUTHORIZED_BY_P3';

-- Q11: no canonical family points to an adjudication that names a different family.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q11_family_adjudication_consistency
FROM p3_canonical_family f JOIN p3_adjudication_decision a ON a.adjudication_id=f.created_by_adjudication_id
WHERE a.canonical_family_id IS DISTINCT FROM f.canonical_family_id;

-- Q12: current release snapshot is complete for all objects allocated in that release.
SELECT CASE WHEN COUNT(*)=0 THEN 'PASS' ELSE 'FAIL' END AS q12_release_snapshot_complete
FROM p3_object_registry o LEFT JOIN p3_release_object_snapshot s ON s.release_id=o.allocation_release_id AND s.object_id=o.object_id
WHERE s.object_id IS NULL;
