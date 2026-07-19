#!/usr/bin/env python3
r"""Schur/Young-symmetrizer block ranks for Cat_{r=2,k=2}(C_2 Hess f).

The target after polarizing the residual quadratic is embedded in V^{*\otimes 6}:
  Sym^2(Λ^2 V*) ⊗ Sym^2(V*).
For each partition λ of 6 occurring by Pieri, a fixed row-major Young
symmetrizer is applied.  Its rank on the catalecticant image is a GL(V)-invariant
determinantal closed-locus rank test.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

# Import exact sparse construction from sibling module.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch  # type: ignore

TensorKey = Tuple[int, int, int, int, int, int]
PRIMES = (1009, 10007, 32003)
PARTITIONS = ((4,2),(3,2,1),(2,2,2),(3,1,1,1),(2,1,1,1,1))


def parity(p: Sequence[int]) -> int:
    return -1 if sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p))) & 1 else 1


def compose_perm(a: Tuple[int,...], b: Tuple[int,...]) -> Tuple[int,...]:
    """Slot permutation composition: apply b then a."""
    return tuple(b[a[i]] for i in range(len(a)))


def subgroup_permutations(blocks: List[List[int]]) -> List[Tuple[Tuple[int,...], int]]:
    """Permutations independently permuting entries within each block.

    Returns (slot map, sign), where slot map sends output position to input
    position under tensor action t -> tuple(t[perm[i]]).
    """
    d = sum(len(b) for b in blocks)
    # d here assumes blocks partition 0..d-1.
    out = []
    choices = [list(itertools.permutations(b)) for b in blocks]
    for selected in itertools.product(*choices):
        perm = list(range(d))
        sgn = 1
        for block, image in zip(blocks, selected):
            # map positions in block to selected original positions
            for pos, src in zip(block, image):
                perm[pos] = src
            # sign of permutation restricted to ordered block
            idx = [block.index(x) for x in image]
            sgn *= parity(idx)
        out.append((tuple(perm), sgn))
    return out


ADAPTED_ROWS = {
    (4,2): [[0,2,4,5],[1,3]],
    (3,2,1): [[0,2,4],[1,3],[5]],
    (2,2,2): [[0,2],[1,3],[4,5]],
    (3,1,1,1): [[0,4,5],[1],[2],[3]],
    (2,1,1,1,1): [[0,4],[1],[2],[3],[5]],
}

def tableau_groups(lam: Tuple[int,...]):
    # LR-adapted tableau: slots (0,1) and (2,3) are the two exterior
    # pairs, while (4,5) is the residual symmetric pair.
    rows=[list(r) for r in ADAPTED_ROWS[lam]]
    cols=[]
    for j in range(max(lam)):
        col=[rows[i][j] for i in range(len(rows)) if j < len(rows[i])]
        cols.append(col)
    row_group = subgroup_permutations(rows)
    col_group = subgroup_permutations(cols)
    # Young symmetrizer a_T b_T: first column antisymmetrizer b, then row sym a.
    # Combine duplicate permutations and integer coefficients.
    terms: Dict[Tuple[int,...],int]={}
    for rp,_ in row_group:
        for cp,cs in col_group:
            # action rho(rp) rho(cp) = rho(comp) under our convention
            comp=compose_perm(rp,cp)
            terms[comp]=terms.get(comp,0)+cs
    return rows, cols, [(p,c) for p,c in sorted(terms.items()) if c]


def full_tensor_row(labels, components, alpha: Tuple[int,int]) -> Dict[TensorKey,int]:
    """Polarized ordered-slot tensor for one second derivative direction."""
    row: Dict[TensorKey,int]={}
    for (I,K), comp in zip(labels,components):
        q=ch.derivative(comp,alpha)
        if not q:
            continue
        pair_orders=[]
        i,j=I; k,l=K
        first=[((i,j),1),((j,i),-1)]
        second=[((k,l),1),((l,k),-1)]
        for A,sa in first:
            for B,sb in second:
                pair_orders.append((A+B,sa*sb))
        if I != K:
            # symmetry swapping the two Λ^2 factors
            for B,sb in second:
                for A,sa in first:
                    pair_orders.append((B+A,sb*sa))
        for mon,c in q.items():
            if len(mon)!=2: raise AssertionError(mon)
            a,b=mon
            tails=[((a,a),2*c)] if a==b else [((a,b),c),((b,a),c)]
            for head,sgn in pair_orders:
                for tail,cc in tails:
                    key=head+tail
                    row[key]=row.get(key,0)+sgn*cc
    return {k:v for k,v in row.items() if v}


def apply_permutation(row: Dict[TensorKey,int], perm: Tuple[int,...], coeff: int, out: Dict[TensorKey,int], p:int):
    for key,val in row.items():
        nk=tuple(key[perm[i]] for i in range(6))
        z=(out.get(nk,0)+coeff*val)%p
        if z: out[nk]=z
        elif nk in out: del out[nk]


def apply_young(row: Dict[TensorKey,int], terms, p:int) -> Dict[TensorKey,int]:
    out: Dict[TensorKey,int]={}
    for perm,c in terms:
        apply_permutation(row,perm,c,out,p)
    return out


def sparse_rank(rows: Iterable[Dict[TensorKey,int]],p:int)->int:
    piv: Dict[TensorKey,Dict[TensorKey,int]]={}
    for raw in rows:
        row={k:v%p for k,v in raw.items() if v%p}
        while row:
            lead=min(row)
            if lead not in piv:
                inv=pow(row[lead],-1,p)
                row={k:(v*inv)%p for k,v in row.items() if (v*inv)%p}
                piv[lead]=row
                break
            f=row[lead]
            base=piv[lead]
            for k,v in base.items():
                z=(row.get(k,0)-f*v)%p
                if z: row[k]=z
                elif k in row: del row[k]
    return len(piv)


def run_form(name,f,prime_count:int,partitions) -> dict:
    t0=time.time(); H=ch.hessian(f); labels,components=ch.compound2_symmetric(H)
    active=ch.active_variables(f)
    alphas=list(itertools.combinations_with_replacement(range(ch.N),2))
    base_rows=[]
    for idx,a in enumerate(alphas):
        r=full_tensor_row(labels,components,a)
        base_rows.append(r)
    rec={
      'form':name,'active_variable_count':len(active),'base_row_count':len(base_rows),
      'base_nonzero_rows':sum(bool(r) for r in base_rows),
      'base_total_nnz':sum(len(r) for r in base_rows),
      'base_max_row_nnz':max(map(len,base_rows)),
      'blocks':[]
    }
    for lam in partitions:
        rows,cols,terms=tableau_groups(lam)
        br={'partition':list(lam),'row_blocks':rows,'column_blocks':cols,'young_terms':len(terms),'ranks_mod_p':{}}
        for p in PRIMES[:prime_count]:
            projected=(apply_young(r,terms,p) for r in base_rows)
            br['ranks_mod_p'][str(p)]=sparse_rank(projected,p)
        rec['blocks'].append(br)
        print(name,lam,br['ranks_mod_p'],flush=True)
    rec['elapsed_seconds']=round(time.time()-t0,3)
    return rec


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--forms',choices=('both','det4','z_per3'),default='both')
    ap.add_argument('--prime-count',type=int,choices=(1,2,3),default=1)
    ap.add_argument('--partition',default='all',help='all or comma-separated e.g. 4-2,3-2-1')
    a=ap.parse_args()
    if a.partition=='all': parts=PARTITIONS
    else:
        parts=tuple(tuple(map(int,x.split('-'))) for x in a.partition.split(','))
    forms=[('det4',ch.det4_terms()),('z_per3',ch.padded_per3_terms())]
    if a.forms!='both': forms=[x for x in forms if x[0]==a.forms]
    out={'schema':'reverse_hessian.schur_block_r2_k2.v1',
         'status':'EXPLORATORY-COMP; fixed Young-symmetrizer projected flattening ranks over finite fields',
         'mathematical_target':'Cat_{2,2}(f) projected in V^tensor6 by row-major Young symmetrizers',
         'partitions_by_pieri':[list(x) for x in PARTITIONS],
         'primes':list(PRIMES[:a.prime_count]),'forms':[]}
    for name,f in forms: out['forms'].append(run_form(name,f,a.prime_count,parts))
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
