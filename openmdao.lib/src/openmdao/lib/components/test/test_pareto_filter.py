# pylint: disable-msg=C0111,C0103

import unittest

from openmdao.lib.components.pareto_filter import ParetoFilter


class ParetoFilterTests(unittest.TestCase):
    
    def test_1d(self):
        pf = ParetoFilter(params=('xin',), responses=('x',))
        pf.params.xin = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        pf.responses.x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pf.execute()
       
        self.assertEqual(1, pf.pareto_outputs[0, 0])
        self.assertEqual(3, pf.pareto_inputs[0, 0])
        
    def test_2d_1(self):
        pf = ParetoFilter(responses=('x', 'y'))
        pf.responses.x = [1,1,1,2,2,2,3,3,3]
        pf.responses.y = [1,2,3,1,2,3,1,2,3]
        pf.execute()

        self.assertEqual(1, pf.pareto_outputs[0, 0])
        self.assertEqual(1, pf.pareto_outputs[0, 1])
        self.assertTrue(pf.pareto_outputs.shape == (1, 2))

    def test_2d_2(self):
        pf = ParetoFilter(responses=('x', 'y'))
        pf.responses.x = [1,1,2,2,2,3,3,3,]
        pf.responses.y = [2,3,1,2,3,1,2,3]
        pf.execute()

        self.assertEqual(1, pf.pareto_outputs[0, 0])
        self.assertEqual(2, pf.pareto_outputs[0, 1])
        self.assertEqual(2, pf.pareto_outputs[1, 0])
        self.assertEqual(1, pf.pareto_outputs[1, 1])
        self.assertTrue(pf.pareto_outputs.shape == (2, 2))
        
        
if __name__ == "__main__":
    unittest.main()

