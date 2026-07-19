import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name): return json.loads((ROOT/'certificates'/name).read_text())

class Certificates(unittest.TestCase):
    def test_rank_vectors(self):
        x=load('catalecticant_ranks.json')
        self.assertEqual(x['rank_vectors']['Ddet'],[1,9,45,165,270,270,165,45,9,1])
        self.assertEqual(x['rank_vectors']['Dper'],[1,9,45,165,414,414,165,45,9,1])
    def test_independent_modular(self):
        x=load('independent_catalecticant_check.json')
        for c in x['checks']:
            for form in ('Ddet','Dper'):
                d=c['forms'][form]
                self.assertTrue(all(v==d['expected_rank_Q_from_primary'] for v in d['ranks_mod_p'].values()))
    def test_squarefree(self):
        x=load('squarefree_Dper3.json')
        self.assertEqual(x['gcd_of_partial_derivatives_over_Q'],'1')
        self.assertEqual(x['gcd_total_degree_over_Q'],0)
    def test_padding_collapse(self):
        x=load('transverse_hessian_experiments.json')
        self.assertTrue(all(c['residual_zero'] for c in x['checks']))
        self.assertTrue(x['unused_variable_check']['full_hessian_determinant_zero'])
    def test_spd_results_are_not_overclaimed(self):
        x=load('exploratory_flattenings.json')
        self.assertTrue(all(not t['separates_reverse_direction'] for t in x['tests']))

if __name__=='__main__': unittest.main()
