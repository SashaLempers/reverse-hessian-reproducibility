#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,struct,sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import compound_hessian_r2 as ch
import schur_block_r2_k2 as sb

def pack_key(t):
    x=0
    for i,v in enumerate(t): x |= (v & 15) << (4*i)
    return x

def export(name,f,out):
    H=ch.hessian(f); labs,cs=ch.compound2_symmetric(H)
    alphas=list(itertools.combinations_with_replacement(range(16),2))
    h=hashlib.sha256(); total=0
    with out.open('wb') as fh:
        fh.write(b'RHT6v1\0\0'); fh.write(struct.pack('<II',16,len(alphas)))
        for a in alphas:
            row=sb.full_tensor_row(labs,cs,a)
            items=sorted((pack_key(k),v) for k,v in row.items())
            fh.write(struct.pack('<BBHI',a[0],a[1],0,len(items)))
            for k,v in items: fh.write(struct.pack('<Ii',k,v))
            total+=len(items)
    data=out.read_bytes(); sha=hashlib.sha256(data).hexdigest()
    return {'form':name,'rows':len(alphas),'total_nnz':total,'bytes':len(data),'sha256':sha,'path':str(out)}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--dir',type=Path,required=True);a=ap.parse_args(); a.dir.mkdir(parents=True,exist_ok=True)
 rec=[]
 for name,f in [('det4',ch.det4_terms()),('z_per3',ch.padded_per3_terms())]:
  out=a.dir/(name+'_cat22_tensor6.bin'); r=export(name,f,out); rec.append(r); print(r,flush=True)
 (a.dir/'manifest.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
