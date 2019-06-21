import unittest

import sys
sys.path.insert(0, "../")

from opetopy.common import DerivationError

from opetopy import UnnamedOpetope
from opetopy import UnnamedOpetopicSet


class Test_UnnamedOpetopicSet_Variable(unittest.TestCase):

    def setUp(self):
        self.a = UnnamedOpetopicSet.Variable("a", UnnamedOpetope.Arrow())
        self.b = UnnamedOpetopicSet.Variable("b", UnnamedOpetope.Arrow())
        self.i1 = UnnamedOpetopicSet.Variable(
            "i1", UnnamedOpetope.OpetopicInteger(1))
        self.i2 = UnnamedOpetopicSet.Variable(
            "i2", UnnamedOpetope.OpetopicInteger(2))
        self.i3 = UnnamedOpetopicSet.Variable(
            "i3", UnnamedOpetope.OpetopicInteger(3))
        self.c = UnnamedOpetopicSet.Variable("c", UnnamedOpetope.Graft(
            UnnamedOpetope.Fill(UnnamedOpetope.OpetopicInteger(2)),
            UnnamedOpetope.OpetopicInteger(2),
            UnnamedOpetope.Address.fromList([['*']], 2)))

    def test___eq__(self):
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.b, self.b)
        self.assertEqual(self.i1, self.i1)
        self.assertEqual(self.i2, self.i2)
        self.assertNotEqual(self.a, self.b)
        self.assertNotEqual(self.a, self.i1)
        self.assertNotEqual(self.i1, self.i2)
        self.assertNotEqual(self.i2, self.i3)
        self.assertNotEqual(self.i3, self.c)

    def test_shape(self):
        self.assertEqual(self.a.shape,
                         UnnamedOpetope.Arrow().eval().source)
        self.assertEqual(self.b.shape,
                         UnnamedOpetope.Arrow().eval().source)
        self.assertEqual(self.i1.shape,
                         UnnamedOpetope.OpetopicInteger(1).eval().source)
        self.assertEqual(self.i2.shape,
                         UnnamedOpetope.OpetopicInteger(2).eval().source)
        self.assertEqual(self.i3.shape,
                         UnnamedOpetope.OpetopicInteger(3).eval().source)

    def test_shapeTarget(self):
        self.assertEqual(self.a.shapeTarget(),
                         UnnamedOpetope.Point().eval().source)
        self.assertEqual(self.b.shapeTarget(),
                         UnnamedOpetope.Point().eval().source)
        self.assertEqual(self.i1.shapeTarget(),
                         UnnamedOpetope.Arrow().eval().source)
        self.assertEqual(self.i2.shapeTarget(),
                         UnnamedOpetope.Arrow().eval().source)
        self.assertEqual(self.i3.shapeTarget(),
                         UnnamedOpetope.Arrow().eval().source)
        self.assertEqual(self.c.shapeTarget(),
                         UnnamedOpetope.OpetopicInteger(3).eval().source)


class Test_UnnamedOpetopicSet_PastingDiagram(unittest.TestCase):

    def setUp(self):
        pass

    def test___eq__(self):
        self.assertEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), "a"),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), "a"))
        self.assertNotEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), "a"),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), "b"))
        self.assertNotEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), "a"),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.Degen(UnnamedOpetope.Arrow()), "a"))
        self.assertNotEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(1),
                {UnnamedOpetope.address([], 1): "a"}),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(1),
                {UnnamedOpetope.address([], 1): "b"}))
        self.assertNotEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(1),
                {UnnamedOpetope.address([], 1): "a"}),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.address([], 1): "a",
                    UnnamedOpetope.address(['*']): "a"
                }))
        self.assertEqual(
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.address([], 1): "a",
                    UnnamedOpetope.address(['*']): "b"
                }),
            UnnamedOpetopicSet.pastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.address(['*']): "b",
                    UnnamedOpetope.address([], 1): "a"
                }))

    def test___getitem__(self):
        d = UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(0), "d")
        p = UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(2),
            {
                UnnamedOpetope.Address.epsilon(1): "a",
                UnnamedOpetope.Address.epsilon(0).fill(): "b"
            })
        with self.assertRaises(DerivationError):
            d[UnnamedOpetope.Address.epsilon(0)]
        self.assertEqual(p[UnnamedOpetope.Address.epsilon(1)], "a")
        self.assertEqual(p[UnnamedOpetope.Address.epsilon(0).fill()], "b")

    def test_degeneratePastingDiagram(self):
        UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(0), "d")
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(1), "d")

    def test_point(self):
        UnnamedOpetopicSet.PastingDiagram.point()

    def test_nonDegeneratePastingDiagram(self):
        UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(2),
            {
                UnnamedOpetope.Address.epsilon(1): "a",
                UnnamedOpetope.Address.epsilon(0).fill(): "b"
            })
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(0), {})
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.Address.epsilon(1): "a"
                })


class Test_UnnamedOpetopicSet_Type(unittest.TestCase):

    def setUp(self):
        self.s = UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(2),
            {
                UnnamedOpetope.Address.epsilon(1): "a",
                UnnamedOpetope.Address.epsilon(0).fill(): "b"
            })

    def test___init__(self):
        UnnamedOpetopicSet.Type(
            self.s, UnnamedOpetopicSet.Variable("t", UnnamedOpetope.Arrow()))
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.Type(
                self.s, UnnamedOpetopicSet.Variable(
                    "t", UnnamedOpetope.Point()))
        UnnamedOpetopicSet.Type(
            UnnamedOpetopicSet.PastingDiagram.point(), None)
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.Type(self.s, None)


class Test_UnnamedOpetopicSet_Typing(unittest.TestCase):

    def setUp(self):
        self.t = UnnamedOpetopicSet.Type(
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.Address.epsilon(1): "a",
                    UnnamedOpetope.Address.epsilon(0).fill(): "b"
                }),
            UnnamedOpetopicSet.Variable("t", UnnamedOpetope.Arrow()))

    def test___init__(self):
        UnnamedOpetopicSet.Typing(
            UnnamedOpetopicSet.Variable(
                "x", UnnamedOpetope.OpetopicInteger(2)), self.t)
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.Typing(
                UnnamedOpetopicSet.Variable(
                    "x", UnnamedOpetope.OpetopicInteger(3)),
                self.t)


class Test_UnnamedOpetopicSet_Context(unittest.TestCase):

    def setUp(self):
        self.p = UnnamedOpetopicSet.Typing(
            UnnamedOpetopicSet.Variable("p", UnnamedOpetope.Point()),
            UnnamedOpetopicSet.Type(
                UnnamedOpetopicSet.PastingDiagram.point(), None))
        self.a = UnnamedOpetopicSet.Typing(
            UnnamedOpetopicSet.Variable(
                "a", UnnamedOpetope.OpetopicInteger(0)),
            UnnamedOpetopicSet.Type(
                UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
                    UnnamedOpetope.OpetopicInteger(0), "p"),
                UnnamedOpetopicSet.Variable("p", UnnamedOpetope.Arrow())))
        self.b = UnnamedOpetopicSet.Typing(
            UnnamedOpetopicSet.Variable(
                "b", UnnamedOpetope.OpetopicInteger(0)),
            UnnamedOpetopicSet.Type(
                UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
                    UnnamedOpetope.OpetopicInteger(0), "p"),
                UnnamedOpetopicSet.Variable("p", UnnamedOpetope.Arrow())))
        self.c = UnnamedOpetopicSet.Typing(
            UnnamedOpetopicSet.Variable(
                "c", UnnamedOpetope.OpetopicInteger(2)),
            UnnamedOpetopicSet.Type(
                UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                    UnnamedOpetope.OpetopicInteger(2),
                    {
                        UnnamedOpetope.Address.epsilon(1): "x",
                        UnnamedOpetope.Address.epsilon(0).fill(): "y"
                    }),
                UnnamedOpetopicSet.Variable("z", UnnamedOpetope.Arrow())))
        self.ctx = UnnamedOpetopicSet.Context() + self.p + self.a + self.c

    def test___add__(self):
        with self.assertRaises(DerivationError):
            self.ctx + self.a
        self.ctx + self.b
        with self.assertRaises(DerivationError):
            self.ctx + self.c

    def test___contains__(self):
        self.assertIn(self.a.variable, self.ctx)
        self.assertNotIn(self.b.variable, self.ctx)
        self.assertIn(self.c.variable, self.ctx)

    def test___getitem__(self):
        self.assertEqual(self.ctx["a"].variable, self.a.variable)
        with self.assertRaises(DerivationError):
            self.ctx["b"]
        self.assertEqual(self.ctx["c"].variable, self.c.variable)

    def test_source(self):
        self.assertEqual(
            self.ctx.source("c", UnnamedOpetope.Address.epsilon(1)),
            "x")
        self.assertEqual(
            self.ctx.source("c", UnnamedOpetope.Address.epsilon(0).fill()),
            "y")

    def test_target(self):
        self.assertEqual(self.ctx.target("c"), "z")
        with self.assertRaises(DerivationError):
            self.ctx.target("p")


class Test_UnnamedOpetopicSet_InferenceRules(unittest.TestCase):

    def setUp(self):
        self.type_point = UnnamedOpetopicSet.Type(
            UnnamedOpetopicSet.PastingDiagram.point(), None)
        self.a = UnnamedOpetopicSet.Variable("a", UnnamedOpetope.Point())
        self.b = UnnamedOpetopicSet.Variable("b", UnnamedOpetope.Point())
        self.c = UnnamedOpetopicSet.Variable("c", UnnamedOpetope.Point())
        self.d = UnnamedOpetopicSet.Variable("d", UnnamedOpetope.Point())
        self.ab = UnnamedOpetopicSet.Variable("ab", UnnamedOpetope.Arrow())
        self.ac = UnnamedOpetopicSet.Variable("ac", UnnamedOpetope.Arrow())
        self.bc = UnnamedOpetopicSet.Variable("bc", UnnamedOpetope.Arrow())
        self.cd = UnnamedOpetopicSet.Variable("cd", UnnamedOpetope.Arrow())
        self.seq = UnnamedOpetopicSet.Sequent()
        self.seq.context = UnnamedOpetopicSet.Context() + \
            UnnamedOpetopicSet.Typing(self.a, self.type_point) + \
            UnnamedOpetopicSet.Typing(self.b, self.type_point) + \
            UnnamedOpetopicSet.Typing(self.c, self.type_point) + \
            UnnamedOpetopicSet.Typing(self.d, self.type_point) + \
            UnnamedOpetopicSet.Typing(
                self.ab, self.type_arrow("a", self.b)) + \
            UnnamedOpetopicSet.Typing(
                self.ac, self.type_arrow("a", self.c)) + \
            UnnamedOpetopicSet.Typing(
                self.bc, self.type_arrow("b", self.c)) + \
            UnnamedOpetopicSet.Typing(
                self.cd, self.type_arrow("c", self.d))

    def type_arrow(
            self, src: str,
            tgt: UnnamedOpetopicSet.Variable) -> UnnamedOpetopicSet.Type:
        """
        Convenient function to define the type of an arrow shaped cell
        """
        return UnnamedOpetopicSet.Type(
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.Arrow(),
                {UnnamedOpetope.Address.epsilon(0): src}),
            tgt)

    def test_degen(self):
        s = UnnamedOpetopicSet.point(UnnamedOpetopicSet.Sequent(), "x")
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.degen(s, "y")
        s = UnnamedOpetopicSet.degen(s, "x")
        self.assertIsNotNone(s.pastingDiagram.degeneracy)
        self.assertEqual(s.pastingDiagram.degeneracy, "x")
        self.assertIsNone(s.pastingDiagram.nodes)
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.degen(s, "x")

    def test_shift(self):
        s = UnnamedOpetopicSet.graft(
            self.seq,
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(1),
                {
                    UnnamedOpetope.Address.epsilon(1): "ac"
                }))
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.fill(s, "ab", "A")
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.fill(s, "bc", "A")
        UnnamedOpetopicSet.fill(s, "ac", "A")

    def test_graft(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.graft(
                UnnamedOpetopicSet.Sequent(),
                UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
                    UnnamedOpetope.OpetopicInteger(0), "x"))
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.graft(
                UnnamedOpetopicSet.Sequent(),
                UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                    UnnamedOpetope.Arrow(),
                    {
                        UnnamedOpetope.Address.epsilon(0): "x"
                    }))
        # Incorrect grafting: ab on top of cd
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.graft(
                self.seq,
                UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                    UnnamedOpetope.OpetopicInteger(2),
                    {
                        UnnamedOpetope.Address.epsilon(1): "cd",
                        UnnamedOpetope.Address.epsilon(0).fill(): "ab"
                    }))
        # Correct grafting: ab on top of bc
        UnnamedOpetopicSet.graft(
            self.seq,
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.Address.epsilon(1): "bc",
                    UnnamedOpetope.Address.epsilon(0).fill(): "ab"
                }))

    def test_point(self):
        s = UnnamedOpetopicSet.point(UnnamedOpetopicSet.Sequent(), "x")
        s = UnnamedOpetopicSet.point(s, "y")
        self.assertEqual(len(s.context), 2)
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.point(s, "x")
        s.pastingDiagram = UnnamedOpetopicSet.PastingDiagram.point()
        with self.assertRaises(DerivationError):
            UnnamedOpetopicSet.point(s, "z")


if __name__ == "__main__":
    unittest.main(verbosity = 2)
