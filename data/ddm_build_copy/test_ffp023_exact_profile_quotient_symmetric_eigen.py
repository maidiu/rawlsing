from __future__ import annotations
import math
import numpy as np
from data.ddm_build_copy import ffx002_r2_local_geometry_exact_profile_quotient_symmetric_eigen as q


def _jacobi_eigh(matrix, tol=1e-14):
    a=[list(map(float,row)) for row in matrix]; n=len(a)
    v=[[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max(1,100*n*n)):
        p=qq=0; largest=0.0
        for i in range(n):
            for j in range(i+1,n):
                x=abs(a[i][j])
                if x>largest: largest=x; p=i; qq=j
        if largest<=tol: break
        app,aqq,apq=a[p][p],a[qq][qq],a[p][qq]
        phi=.5*math.atan2(2*apq,aqq-app); c,s=math.cos(phi),math.sin(phi)
        for k in range(n):
            if k in (p,qq): continue
            akp,akq=a[k][p],a[k][qq]
            a[k][p]=a[p][k]=c*akp-s*akq; a[k][qq]=a[qq][k]=s*akp+c*akq
        a[p][p]=c*c*app-2*s*c*apq+s*s*aqq
        a[qq][qq]=s*s*app+2*s*c*apq+c*c*aqq; a[p][qq]=a[qq][p]=0.0
        for k in range(n):
            vkp,vkq=v[k][p],v[k][qq]; v[k][p]=c*vkp-s*vkq; v[k][qq]=s*vkp+c*vkq
    pairs=sorted(((a[i][i],[v[r][i] for r in range(n)]) for i in range(n)),reverse=True,key=lambda x:x[0])
    return np.array([x[0] for x in pairs]),np.array([x[1] for x in pairs]).T


def _fixture(weighted=False):
    mids=['M1','M2','M3','M4']
    profiles=[('A','A','A','A'),('A','A','A','B'),('A','B','B','A'),('B','A','B','A'),('B','B','A','B'),('B','B','B','B')]
    counts=[2,2,1,1,2,1] if not weighted else [2,1,2,1,1,2]
    rows=[]; z=0
    for p,c in zip(profiles,counts):
        for _ in range(c):
            z+=1; rows.append({'respondent_id':f'R{z:02d}','state_by_measurement':dict(zip(mids,p))})
    return rows,mids,(dict(zip(mids,[1.,2.,3.,5.])) if weighted else None)


def _dense_distance(rows,mids,weights):
    n=len(rows); out=np.zeros((n,n)); ws=[1.]*len(mids) if weights is None else [weights[m] for m in mids]
    for i in range(n):
        for j in range(i+1,n):
            d=sum(w for w,m in zip(ws,mids) if rows[i]['state_by_measurement'][m]!=rows[j]['state_by_measurement'][m])/sum(ws)
            out[i,j]=out[j,i]=d
    return out


def _check(weighted):
    rows,mids,weights=_fixture(weighted); rows=sorted(rows,key=lambda r:r['respondent_id'])
    quotient=q.build_exact_profile_quotient(rows,mids); delta=q.exact_profile_distance_matrix(quotient,weights)
    gram=q.quotient_classical_mds_gram(delta,quotient.multiplicities); evq,vecq=q.symmetric_eigensystem(gram)
    dense=_dense_distance(rows,mids,weights); d2=dense*dense; rm=d2.mean(1); gd=-.5*(d2-rm[:,None]-rm[None,:]+d2.mean())
    evd,vecd=_jacobi_eigh(gd); posd=evd[evd>q.POSITIVE_EIGEN_EPS]; posq=evq[evq>q.POSITIVE_EIGEN_EPS]
    assert np.max(np.abs(posd-posq)) < 1e-10
    assert np.max(np.abs(q.expanded_gram_from_quotient(gram,quotient)-gd)) < 1e-10
    for retained in [1,2,min(3,len(posq))]:
        idx=np.where(evd>q.POSITIVE_EIGEN_EPS)[0][:retained]; cd=vecd[:,idx]*np.sqrt(evd[idx])
        cq=q.retained_profile_coordinates(evq,vecq,quotient.multiplicities,retained)
        ce=np.array([cq[i] for i in quotient.respondent_profile_index])
        assert np.max(np.abs(np.linalg.norm(cd[:,None]-cd[None,:],axis=2)-np.linalg.norm(ce[:,None]-ce[None,:],axis=2))) < 1e-10
    for i,row in enumerate(rows):
        exact=sorted((float(dense[i,j]),rows[j]['respondent_id']) for j in range(len(rows)) if i!=j)
        for k in [1,3,len(rows)-1]:
            assert q.exact_neighbors_for_respondent(quotient,delta,row['respondent_id'],k)==[(rid,d) for d,rid in exact[:k]]
    retained=min(2,len(posq)); cq=q.retained_profile_coordinates(evq,vecq,quotient.multiplicities,retained)
    ep=q.embedded_profile_distances(cq); ce=np.array([cq[i] for i in quotient.respondent_profile_index]); ed=np.linalg.norm(ce[:,None]-ce[None,:],axis=2)
    dense_stress=math.sqrt(np.sum(np.triu((dense-ed)**2,1))/np.sum(np.triu(dense*dense,1)))
    assert abs(dense_stress-q.normalized_stress_exact(delta,ep,quotient.multiplicities)) < 1e-10


def test_unweighted_dense_jacobi_equivalence(): _check(False)
def test_weighted_dense_jacobi_equivalence(): _check(True)
