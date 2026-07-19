#!/usr/bin/env python3
"""Export order-6 tensors obtained by contracting two slots of Phi_2(f).

Phi_2(f) is fully polarized as an order-8 tensor with slot convention
  [wedge I:0,1] [wedge J:2,3] [quartic polynomial:4,5,6,7].
For fixed source slots we contract either Sym^2 V or Lambda^2 V and retain the
remaining six ordered tensor slots for Young-symmetrizer projections.
"""
from __future__ import annotations
import argparse,itertools,struct,sys,json,hashlib,math,time
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch

COMBOS=[
 ('poly_poly_sym',(6,7),'sym'),
 ('wedge_same_alt',(0,1),'alt'),
 ('wedge_cross_sym',(0,2),'sym'),
 ('wedge_cross_alt',(0,2),'alt'),
 ('wedge_poly_sym',(0,4),'sym'),
 ('wedge_poly_alt',(0,4),'alt'),
]

def unique_perms(t):return sorted(set(itertools.permutations(t)))
def pack6(t):
 x=0
 for i,v in enumerate(t):x|=(v&15)<<(4*i)
 return x

def source_basis(kind):
 return list(itertools.combinations_with_replacement(range(16),2)) if kind=='sym' else list(itertools.combinations(range(16),2))

def build_rows(labels,components,slots,kind):
 basis=source_basis(kind);bi={x:i for i,x in enumerate(basis)};rows=[{} for _ in basis]
 remain=[i for i in range(8) if i not in slots]
 for (I,K),comp in zip(labels,components):
  if not comp:continue
  i,j=I;k,l=K
  first=[((i,j),1),((j,i),-1)];second=[((k,l),1),((l,k),-1)]
  heads=[]
  for A,sa in first:
   for B,sb in second:heads.append((A+B,sa*sb))
  if I!=K:
   for B,sb in second:
    for A,sa in first:heads.append((B+A,sb*sa))
  for mon,c in comp.items():
   fac=1
   for n in Counter(mon).values():fac*=math.factorial(n)
   for tail in unique_perms(mon):
    for head,sgn in heads:
     key=head+tail;u,v=key[slots[0]],key[slots[1]]
     if kind=='alt':
      if u==v:continue
      b=(u,v) if u<v else (v,u);ss=1 if u<v else -1
     else:
      b=(u,v) if u<=v else (v,u);ss=1
     target=tuple(key[q] for q in remain);r=rows[bi[b]]
     val=sgn*ss*c*fac
     r[target]=r.get(target,0)+val
 # remove zero cancellations
 return basis,[{k:v for k,v in r.items() if v} for r in rows]

def write_bin(out,basis,rows):
 with out.open('wb') as fh:
  fh.write(b'RHT6v1\0\0');fh.write(struct.pack('<II',16,len(rows)))
  total=0
  for b,row in zip(basis,rows):
   items=sorted((pack6(k),v) for k,v in row.items());total+=len(items)
   fh.write(struct.pack('<BBHI',b[0],b[1],0,len(items)))
   for k,v in items:fh.write(struct.pack('<Ii',k,v))
 return total

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--forms',choices=('both','det4','z_per3'),default='both');ap.add_argument('--combo',default='all');a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
 forms=[('det4',ch.det4_terms()),('z_per3',ch.padded_per3_terms())]
 if a.forms!='both':forms=[x for x in forms if x[0]==a.forms]
 combos=COMBOS if a.combo=='all' else [x for x in COMBOS if x[0]==a.combo]
 manifest=[]
 for name,f in forms:
  t=time.time();H=ch.hessian(f);labels,components=ch.compound2_symmetric(H);print(name,'compound ready',time.time()-t,flush=True)
  for cname,slots,kind in combos:
   t=time.time();basis,rows=build_rows(labels,components,slots,kind);out=a.outdir/f'{name}_{cname}.bin';total=write_bin(out,basis,rows);sha=hashlib.sha256(out.read_bytes()).hexdigest()
   rec={'form':name,'contraction':cname,'source_slots':list(slots),'source_type':kind,'rows':len(rows),'nonzero_rows':sum(bool(r) for r in rows),'total_nnz':total,'max_row_nnz':max(map(len,rows)),'bytes':out.stat().st_size,'sha256':sha,'file':out.name}
   manifest.append(rec);print(rec,flush=True)
 (a.outdir/'young_contractions_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
