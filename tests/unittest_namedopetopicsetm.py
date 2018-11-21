import unittest

from common import DerivationError

import NamedOpetope
import NamedOpetopicSet
import NamedOpetopicSetM


class Test_NamedOpetopicSetM_InferenceRules(unittest.TestCase):

    def setUp(self):
        pass

    def test_point(self):
        s = NamedOpetopicSetM.point("x")
        self.assertTrue(isinstance(s, NamedOpetope.OCMT))
        self.assertEqual(len(s.context), 1)
        self.assertEqual(len(s.theory.classes), 0)

    def test_degen(self):
        s = NamedOpetopicSetM.point("x")
        with self.assertRaises(DerivationError):
            NamedOpetopicSetM.degen(s, "y")
        s = NamedOpetopicSetM.degen(s, "x")
        self.assertTrue(isinstance(s, NamedOpetope.Sequent))
        self.assertEqual(len(s.context), 1)
        self.assertEqual(len(s.theory.classes), 0)
        self.assertEqual(
            s.typing.term, NamedOpetope.Term(
                NamedOpetope.Variable("x", 0), True))

    def test_pd(self):
        s = NamedOpetopicSetM.point("x")
        with self.assertRaises(DerivationError):
            NamedOpetopicSetM.pd(s, "y")
        s = NamedOpetopicSetM.pd(s, "x")
        self.assertTrue(isinstance(s, NamedOpetope.Sequent))
        self.assertEqual(len(s.context), 1)
        self.assertEqual(len(s.theory.classes), 0)
        self.assertEqual(
            s.typing.term, NamedOpetope.Term(
                NamedOpetope.Variable("x", 0), False))

    def test_graft(self):
        pass

    def test_fill(self):
        s = NamedOpetopicSetM.Fill(
            NamedOpetopicSetM.Pd(
                NamedOpetopicSetM.Point("x"),
                "x"),
            "f").eval()
        self.assertTrue(isinstance(s, NamedOpetope.OCMT))
        self.assertEqual(len(s.context), 3)
        self.assertEqual(len(s.theory.classes), 0)

    def test_zero(self):
        pass

    def test_sum(self):
        pass

    def test_glue(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity = 2)
