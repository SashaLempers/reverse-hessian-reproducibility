#!/usr/bin/env python3
"""Run all certificate builders, compare independent engines, and hash outputs.

Runtime metadata is written only under runtime_logs/. JSON certificates and
logs/full_run.log are deterministic.
"""
from __future__ import annotations
import argparse, concurrent.futures, datetime, hashlib, json, subprocess, sys, time
from pathlib import Path

SCRIPT_DIR=Path(__file__).resolve().parent
PACKAGE_ROOT=SCRIPT_DIR.parent

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def execute(name,cmd,cwd,runtime_dir):
    start=time.time(); p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    text=(f'name={name}\nstarted_utc={datetime.datetime.now(datetime.timezone.utc).isoformat()}\n'
          f'command={" ".join(map(str,cmd))}\nreturncode={p.returncode}\nelapsed_seconds={time.time()-start:.6f}\n\n{p.stdout}')
    (runtime_dir/f'{name}.log').write_text(text,encoding='utf-8')
    if p.returncode: raise subprocess.CalledProcessError(p.returncode,cmd,p.stdout)
    return name,p.stdout

def compare_engines(cert:Path):
    primary=json.loads((cert/'catalecticant_ranks.json').read_text())
    indep=json.loads((cert/'independent_catalecticant_check.json').read_text())
    if primary['polynomial_hashes']!=indep['polynomial_hashes']:
        raise AssertionError('independent polynomial hashes disagree')
    for a,row in enumerate(indep['checks']):
        prow=primary['catalecticants'][a]
        for form,rank_key,matrix_key in (('Ddet','rank_Ddet','matrix_sha256_Ddet'),('Dper','rank_Dperm','matrix_sha256_Dperm')):
            f=row['forms'][form]; expected=int(prow[rank_key])
            if any(int(v)!=expected for v in f['ranks_mod_p'].values()):
                raise AssertionError(f'rank mismatch a={a} {form}')
            if matrix_key in prow and f['matrix_sha256']!=prow[matrix_key]:
                raise AssertionError(f'matrix mismatch a={a} {form}')
            f['expected_rank_Q_from_primary']=expected
    indep['comparison_to_primary']={
        'polynomial_hashes_equal':True,
        'direct_matrix_hashes_equal_where_available':True,
        'all_modular_ranks_equal_exact_Q_ranks':True,
    }
    indep['result']='all independently reconstructed modular ranks equal the primary exact-Q ranks'
    (cert/'independent_catalecticant_check.json').write_text(json.dumps(indep,indent=2,sort_keys=True)+'\n')
    modular={'schema':'reverse_hessian.modular_crosscheck.v2','deterministic':True,'primes':indep['primes'],'polynomial_hashes':indep['polynomial_hashes'],'checks':indep['checks'],'comparison_to_primary':indep['comparison_to_primary'],'result':indep['result']}
    (cert/'modular_crosscheck.json').write_text(json.dumps(modular,indent=2,sort_keys=True)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-root',type=Path,default=PACKAGE_ROOT); ap.add_argument('--skip-exploratory',action='store_true'); a=ap.parse_args()
    root=a.output_root.resolve(); cert=root/'certificates'; runtime=root/'runtime_logs'; logs=root/'logs'
    cert.mkdir(parents=True,exist_ok=True); runtime.mkdir(parents=True,exist_ok=True); logs.mkdir(parents=True,exist_ok=True)
    py=sys.executable
    jobs={
      'primary_catalecticants':[py,SCRIPT_DIR/'certify_catalecticant_ranks.py','--out',cert/'catalecticant_ranks.json'],
      'independent_catalecticants':[py,SCRIPT_DIR/'independent_catalecticant_check.py','--out',cert/'independent_catalecticant_check.json'],
      'squarefree':[py,SCRIPT_DIR/'certify_squarefree_Dper3.py','--out',cert/'squarefree_Dper3.json'],
      'uniform_formulas':[py,SCRIPT_DIR/'verify_uniform_formulas.py','--out',cert/'uniform_formulas.json'],
      'transverse_hessian':[py,SCRIPT_DIR/'transverse_hessian_experiments.py','--out',cert/'transverse_hessian_experiments.json'],
    }
    if not a.skip_exploratory:
        jobs['exploratory_flattenings']=[py,SCRIPT_DIR/'exploratory_flattenings.py','--out',cert/'exploratory_flattenings.json']
    outputs={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        futs={ex.submit(execute,n,c,root,runtime):n for n,c in jobs.items()}
        for fut in concurrent.futures.as_completed(futs):
            name,out=fut.result(); outputs[name]=out
    compare_engines(cert)
    subprocess.run([py,SCRIPT_DIR/'normalize_certificates.py',cert],cwd=root,check=True,stdout=subprocess.PIPE,text=True)
    files=sorted(p for p in cert.glob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    (cert/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  certificates/{p.name}\n' for p in files),encoding='utf-8')
    stable=[]
    for p in files: stable.append(f'OK {p.name} {sha(p)}')
    (logs/'full_run.log').write_text('\n'.join(stable)+'\n',encoding='utf-8')
    (runtime/'run_all_runtime.log').write_text('completed_jobs='+','.join(sorted(outputs))+'\n',encoding='utf-8')
    print('all certificates generated and cross-checked')
    return 0
if __name__=='__main__': raise SystemExit(main())
