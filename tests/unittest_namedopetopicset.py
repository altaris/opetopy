import unittest

import sys
sys.path.insert(0, "../")

from opetopy.common import DerivationError

from opetopy import NamedOpetope
from opetopy import NamedOpetopicSet


class Test_NamedOpetopicSet_InferenceRules(unittest.TestCase):

    def setUp(self):
        pass

    def test_repres(self):
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.repres(
                NamedOpetope.Degen(NamedOpetope.Point("x")).eval())
        aseq = NamedOpetopicSet.repres(NamedOpetope.Arrow().eval())
        self.assertEqual(len(aseq.context), 3)
        self.assertEqual(len(aseq.theory.classes), 0)
        self.assertIn(NamedOpetope.Variable("a", 0), aseq.context)
        self.assertIn(NamedOpetope.Variable("tf", 0), aseq.context)
        self.assertIn(NamedOpetope.Variable("f", 1), aseq.context)
        i3seq = NamedOpetopicSet.repres(NamedOpetope.OpetopicInteger(3).eval())
        self.assertEqual(len(i3seq.context), 12)
        self.assertEqual(len(i3seq.theory.classes), 3)
        self.assertIn(NamedOpetope.Variable("a_1", 0), i3seq.context)
        self.assertIn(NamedOpetope.Variable("a_2", 0), i3seq.context)
        self.assertIn(NamedOpetope.Variable("a_3", 0), i3seq.context)
        self.assertIn(NamedOpetope.Variable("f_1", 1), i3seq.context)
        self.assertIn(NamedOpetope.Variable("f_2", 1), i3seq.context)
        self.assertIn(NamedOpetope.Variable("f_3", 1), i3seq.context)
        self.assertIn(NamedOpetope.Variable("A", 2), i3seq.context)
        self.assertTrue(i3seq.theory.equal(
            NamedOpetope.Variable("a_1", 0),
            NamedOpetope.Variable("tf_2", 0)))
        self.assertTrue(i3seq.theory.equal(
            NamedOpetope.Variable("a_2", 0),
            NamedOpetope.Variable("tf_3", 0)))
        self.assertTrue(i3seq.theory.equal(
            NamedOpetope.Variable("tf_1", 0),
            NamedOpetope.Variable("ttA", 0)))

    def test_sum(self):
        a = NamedOpetopicSet.Repr(
            NamedOpetope.OpetopicInteger(3, "a", "f", "A")).eval()
        b = NamedOpetopicSet.Repr(
            NamedOpetope.OpetopicInteger(4, "a", "f", "B")).eval()
        c = NamedOpetopicSet.Repr(
            NamedOpetope.OpetopicInteger(4, "b", "g", "B")).eval()
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.sum(a, b)
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.sum(b, c)
        d = NamedOpetopicSet.sum(a, c)
        self.assertEqual(len(d.context), len(a.context) + len(c.context))
        self.assertEqual(len(d.theory.classes),
                         len(a.theory.classes) + len(c.theory.classes))

    def test_glue(self):
        a = NamedOpetopicSet.Repr(NamedOpetope.OpetopicInteger(3)).eval()
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.glue(a, "a_1", "f_1")
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.glue(a, "f_1", "f_2")
        a = NamedOpetopicSet.glue(a, "a_1", "a_2")
        a = NamedOpetopicSet.glue(a, "a_1", "a_3")
        a = NamedOpetopicSet.glue(a, "a_1", "ttA")
        a = NamedOpetopicSet.glue(a, "f_1", "f_2")
        a = NamedOpetopicSet.glue(a, "f_1", "f_3")
        a = NamedOpetopicSet.glue(a, "f_1", "tA")
        self.assertEqual(len(a.theory.classes), 2)

    def test_zero(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity = 2)
