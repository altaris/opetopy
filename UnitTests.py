# -*- coding: utf-8 -*-

"""
.. module:: opetopy.UnitTests
   :synopsis: Unit tests

.. moduleauthor:: Cédric HT

"""

import unittest

from common import DerivationError

import UnnamedOpetope
import UnnamedOpetopicSet
import NamedOpetope
import NamedOpetopicSet


class Test_UnnamedOpetope_Address(unittest.TestCase):

    def setUp(self):
        self.a = UnnamedOpetope.Address.epsilon(0)
        self.b = UnnamedOpetope.Address.epsilon(1)
        self.c = UnnamedOpetope.Address.fromListOfAddresses([self.a])
        self.d = UnnamedOpetope.Address.fromListOfAddresses([self.a, self.a])
        self.e = UnnamedOpetope.Address.fromList([['*'], ['*', '*'], ['']], 2)

    def test___add__(self):
        with self.assertRaises(DerivationError):
            self.b + self.b
        with self.assertRaises(DerivationError):
            self.a + self.b
        self.assertEqual(
            UnnamedOpetope.Address.fromListOfAddresses([self.a, self.a]),
            UnnamedOpetope.Address.fromListOfAddresses([self.a]) + self.a
        )
        self.assertNotEqual(
            UnnamedOpetope.Address.fromListOfAddresses(
                [self.a, self.a, self.a]),
            UnnamedOpetope.Address.fromListOfAddresses([self.a]) + self.a
        )

    def test___eq__(self):
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.e, self.e)
        self.assertNotEqual(self.a, self.b)
        self.assertNotEqual(self.b, self.c)

    def test___init__(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address(-1)
        UnnamedOpetope.Address(0)

    def test___lt__(self):
        with self.assertRaises(DerivationError):
            self.a < self.b
        self.assertFalse(self.c < self.c)
        self.assertLess(self.c, self.d)
        self.assertFalse(self.d < self.c)
        self.assertLess(self.e, self.e + self.d)
        self.assertLess(self.e + self.c, self.e + self.d)

    def test___mul__(self):
        with self.assertRaises(DerivationError):
            self.a * self.c
        self.assertEqual(self.a * self.a, self.a)
        self.assertEqual(self.b * self.b, self.b)
        self.assertEqual(self.c * self.c, self.d)
        self.assertNotEqual(self.c * self.d, self.d)

    def test___str__(self):
        self.assertEqual(str(self.a), "*")
        self.assertEqual(str(self.b), "[]")
        self.assertEqual(str(self.c), "[*]")
        self.assertEqual(str(self.d), "[**]")
        self.assertEqual(str(self.e), "[[*][**][]]")

    def test_epsilon(self):
        self.assertEqual(UnnamedOpetope.Address.epsilon(1),
                         UnnamedOpetope.Address(1))

    def test_isEpsilon(self):
        self.assertTrue(self.a.isEpsilon())
        self.assertTrue(self.b.isEpsilon())
        self.assertFalse(self.c.isEpsilon())
        self.assertFalse(self.d.isEpsilon())
        self.assertFalse(self.e.isEpsilon())

    def test_edgeDecomposition(self):
        with self.assertRaises(DerivationError):
            self.a.edgeDecomposition()
        with self.assertRaises(DerivationError):
            self.b.edgeDecomposition()
        p, q = self.c.edgeDecomposition()
        self.assertEqual(p, self.b)
        self.assertEqual(q, self.a)
        p, q = self.d.edgeDecomposition()
        self.assertEqual(p, self.c)
        self.assertEqual(q, self.a)
        p, q = self.e.edgeDecomposition()
        self.assertEqual(
            p, UnnamedOpetope.Address.fromList([['*'], ['*', '*']], 2))
        self.assertEqual(q, self.b)

    def test_fromListOfAddresses(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address.fromListOfAddresses([self.a, self.b])
        self.assertEqual(
            self.e,
            UnnamedOpetope.Address.fromListOfAddresses(
                [self.c, self.d, UnnamedOpetope.Address.epsilon(1)])
        )

    def test_fromList(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address.fromList([], -1)
        self.assertEqual(UnnamedOpetope.Address.fromList([], 1), self.b)
        self.assertEqual(UnnamedOpetope.Address.fromList([['']], 1), self.c)
        self.assertEqual(UnnamedOpetope.Address.fromList(['*'], 1), self.c)
        self.assertEqual(UnnamedOpetope.Address.fromList([[''], ['']], 1),
                         self.d)

    def test_shift(self):
        with self.assertRaises(DerivationError):
            self.a.shift(-1)
        self.assertEqual(self.a.shift(0), self.a)
        self.assertEqual(self.b.shift(0), self.b)
        self.assertEqual(self.c.shift(0), self.c)
        self.assertEqual(self.d.shift(0), self.d)
        self.assertEqual(self.e.shift(0), self.e)
        self.assertEqual(self.a.shift(), self.c)
        self.assertEqual(self.a.shift(1), self.c)
        self.assertEqual(
            (self.a.shift(2) + (self.a.shift(1) + self.a)) *
            self.b.shift(1),
            self.e
        )

    def test_substitution(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address.substitution(self.d, self.a, self.c)
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address.substitution(self.d, self.c, self.a)
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Address.substitution(self.e, self.b, self.b)
        self.assertEqual(UnnamedOpetope.Address.substitution(
            self.e,
            UnnamedOpetope.Address.epsilon(1).shift(),
            UnnamedOpetope.Address.epsilon(1).shift() +
            UnnamedOpetope.Address.epsilon(1)),
            self.e
        )
        self.assertEqual(UnnamedOpetope.Address.substitution(self.d, self.c,
                                                             self.c),
                         self.d)
        self.assertEqual(UnnamedOpetope.Address.substitution(
            self.e,
            UnnamedOpetope.Address.epsilon(0).shift(2),
            self.e
        ),
            UnnamedOpetope.Address.fromList(
                [['*'], ['*', '*'], [''], ['*', '*'], ['']], 2)
        )


class Test_UnnamedOpetope_Context(unittest.TestCase):

    def setUp(self):
        self.a = UnnamedOpetope.Context(0)
        self.b = UnnamedOpetope.Context(2)
        self.c = UnnamedOpetope.Context(2) + \
            (UnnamedOpetope.Address.epsilon(1),
                UnnamedOpetope.Address.epsilon(0))
        self.d = UnnamedOpetope.Context(2) + \
            (UnnamedOpetope.Address.fromList(['*'], 1),
                UnnamedOpetope.Address.epsilon(0))
        self.e = UnnamedOpetope.Context(3) + \
            (UnnamedOpetope.Address.epsilon(2),
                UnnamedOpetope.Address.fromList(['*'], 1))
        self.f = UnnamedOpetope.Context(3) + \
            (UnnamedOpetope.Address.epsilon(1).shift(),
                UnnamedOpetope.Address.epsilon(1))

    def test___add__(self):
        # Dimension mismatch in tuple
        with self.assertRaises(DerivationError):
            self.b + (UnnamedOpetope.Address.epsilon(1),
                      UnnamedOpetope.Address.epsilon(1))
        # Dimension mismatch with UnnamedOpetope.context
        with self.assertRaises(DerivationError):
            self.b + (UnnamedOpetope.Address.epsilon(2),
                      UnnamedOpetope.Address.epsilon(1))
        # Leaf already present
        with self.assertRaises(DerivationError):
            self.e + (UnnamedOpetope.Address.epsilon(2),
                      UnnamedOpetope.Address.epsilon(1))
        # Node already present
        with self.assertRaises(DerivationError):
            self.e + (UnnamedOpetope.Address.epsilon(1).shift(),
                      UnnamedOpetope.Address.fromList(['*'], 1))
        self.assertEqual(
            self.b + (UnnamedOpetope.Address.epsilon(1),
                      UnnamedOpetope.Address.epsilon(0)),
            self.c
        )
        self.assertEqual(
            self.b + (UnnamedOpetope.Address.fromList(['*'], 1),
                      UnnamedOpetope.Address.epsilon(0)),
            self.d
        )
        self.assertEqual(
            self.e + (UnnamedOpetope.Address.epsilon(1).shift(),
                      UnnamedOpetope.Address.epsilon(1)),
            self.f + (UnnamedOpetope.Address.epsilon(2),
                      UnnamedOpetope.Address.fromList(['*'], 1))
        )

    def test___call__(self):
        with self.assertRaises(DerivationError):
            self.f(UnnamedOpetope.Address.epsilon(2))
        self.assertEqual(self.c(UnnamedOpetope.Address.epsilon(1)),
                         UnnamedOpetope.Address.epsilon(0))
        self.assertEqual(
            self.e(UnnamedOpetope.Address.epsilon(2)),
            UnnamedOpetope.Address.fromList(['*'], 1)
        )

    def test___eq__(self):
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.b, self.b)
        self.assertEqual(self.c, self.c)
        self.assertEqual(self.d, self.d)
        self.assertEqual(self.e, self.e)
        self.assertEqual(self.f, self.f)
        self.assertNotEqual(self.a, self.b)
        self.assertNotEqual(self.b, self.c)
        self.assertNotEqual(self.b, self.d)
        self.assertNotEqual(self.c, self.d)
        self.assertNotEqual(self.e, self.f)

    def test___init__(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Context(-1)
        self.assertEqual(len(self.b.keys()), 0)
        self.assertEqual(self.b.dimension, 2)

    def test___sub__(self):
        with self.assertRaises(DerivationError):
            self.b - UnnamedOpetope.Address.epsilon(1)
        with self.assertRaises(DerivationError):
            self.f - UnnamedOpetope.Address.epsilon(2)
        self.assertEqual(self.c - UnnamedOpetope.Address.epsilon(1), self.b)
        self.assertEqual(self.d - UnnamedOpetope.Address.fromList(['*'], 1),
                         self.b)
        self.assertEqual(self.e - UnnamedOpetope.Address.epsilon(2),
                         UnnamedOpetope.Context(3))
        self.assertEqual(
            self.f - UnnamedOpetope.Address.epsilon(1).shift(),
            UnnamedOpetope.Context(3))


class Test_UnnamedOpetope_Preopetope(unittest.TestCase):

    def setUp(self):
        self.a = UnnamedOpetope.Preopetope(-1)
        self.b = UnnamedOpetope.Preopetope(0)
        self.c = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(0): self.b
        })
        self.d = UnnamedOpetope.Preopetope.degenerate(self.b)
        self.e = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(1): self.c
        })
        self.f = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(1): self.c,
            UnnamedOpetope.Address.fromList(['*'], 1): self.c
        })

    def test___add__(self):
        # Adding to a degenerate
        with self.assertRaises(DerivationError):
            self.d + (UnnamedOpetope.Address.epsilon(1), self.c)
        # Dimension mismatch in the tuple
        with self.assertRaises(DerivationError):
            self.e + (UnnamedOpetope.Address.fromList(['*'], 1), self.a)
        # Dimension mismatch with the popt
        with self.assertRaises(DerivationError):
            self.e + (UnnamedOpetope.Address.epsilon(2), self.f)
        # UnnamedOpetope.Address already present
        with self.assertRaises(DerivationError):
            self.e + (UnnamedOpetope.Address.epsilon(1), self.c)
        self.assertEqual(self.e + (UnnamedOpetope.Address.fromList(['*'], 1),
                                   self.c),
                         self.f)

    def test___eq__(self):
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.b, self.b)
        self.assertEqual(self.c, self.c)
        self.assertEqual(self.b, self.b)
        self.assertEqual(self.e, self.e)
        self.assertEqual(self.f, self.f)
        self.assertNotEqual(self.a, self.b)
        self.assertNotEqual(self.b, self.c)
        self.assertNotEqual(self.c, self.d)
        self.assertNotEqual(self.c, self.e)
        self.assertNotEqual(self.e, self.f)

    def test___init__(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope(-2)
        UnnamedOpetope.Preopetope(-1)
        x = UnnamedOpetope.Preopetope(8)
        self.assertEqual(x.dimension, 8)
        self.assertFalse(x.isDegenerate)
        self.assertEqual(x.nodes, {})

    def test___sub__(self):
        with self.assertRaises(DerivationError):
            self.e - UnnamedOpetope.Address.fromList(['*'], 1)
        self.assertEqual(self.f - UnnamedOpetope.Address.fromList(['*'], 1),
                         self.e)

    def test_degenerate(self):
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.degenerate(self.a)
        self.assertEqual(self.d.degeneracy, self.b)
        self.assertEqual(self.d.dimension, self.b.dimension + 2)
        self.assertTrue(self.d.isDegenerate)
        self.assertEqual(self.d.nodes, {})

    def test_empty(self):
        x = UnnamedOpetope.Preopetope.empty()
        self.assertEqual(x.dimension, -1)

    def test_fromDictOfPreopetopes(self):
        # Empty dict
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.fromDictOfPreopetopes({})
        # Dimension mismatch in tuple
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
                UnnamedOpetope.Address.epsilon(1): self.a
            })
        # Dimension mismatch among tuples
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
                UnnamedOpetope.Address.epsilon(0): self.a,
                UnnamedOpetope.Address.epsilon(1): self.c
            })
        self.assertEqual(self.f.nodes[UnnamedOpetope.Address.epsilon(1)],
                         self.c)
        self.assertIn(UnnamedOpetope.Address.fromList(['*'], 1),
                      self.f.nodes.keys())
        self.assertNotIn(UnnamedOpetope.Address.epsilon(2),
                         self.f.nodes.keys())

    def test_grafting(self):
        # Dimension mismatch btw preopetopes
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.grafting(
                self.e,
                UnnamedOpetope.Address.epsilon(0), self.b)
        # Dim mismatch btw addr and UnnamedOpetope.preopetope
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.grafting(
                self.e,
                UnnamedOpetope.Address.epsilon(0), self.c)
        self.assertEqual(
            UnnamedOpetope.Preopetope.grafting(
                self.e,
                UnnamedOpetope.Address.fromList(['*'], 1),
                self.e),
            self.f
        )

    def test_improperGrafting(self):
        # Adding to a degenerate
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.improperGrafting(
                self.d,
                UnnamedOpetope.Address.epsilon(1),
                self.c
            )
        # Dimension mismatch in the tuple
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.improperGrafting(
                self.e,
                UnnamedOpetope.Address.fromList(['*'], 1),
                self.a
            )
        # Dimension mismatch with the popt
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.improperGrafting(
                self.e,
                UnnamedOpetope.Address.epsilon(2),
                self.f
            )
        # UnnamedOpetope.Address already present
        with self.assertRaises(DerivationError):
            UnnamedOpetope.Preopetope.improperGrafting(
                self.e,
                UnnamedOpetope.Address.epsilon(1),
                self.c
            )
        self.assertEqual(
            UnnamedOpetope.Preopetope.improperGrafting(
                self.e,
                UnnamedOpetope.Address.fromList(['*'], 1),
                self.c
            ),
            self.f
        )

    def test_leafAddresses(self):
        self.assertEqual(self.b.leafAddresses(), set())
        self.assertEqual(self.c.leafAddresses(), set())
        self.assertEqual(self.d.leafAddresses(), set())
        self.assertEqual(self.e.leafAddresses(),
                         set([UnnamedOpetope.Address.fromList(['*'], 1)])
                         )
        self.assertEqual(self.f.leafAddresses(),
                         set([UnnamedOpetope.Address.fromList(['*', '*'], 1)])
                         )

    def test_nodeAddresses(self):
        self.assertEqual(self.b.nodeAddresses(), set())
        self.assertEqual(self.c.nodeAddresses(),
                         set([UnnamedOpetope.Address.epsilon(0)]))
        self.assertEqual(self.d.nodeAddresses(), set())
        self.assertEqual(self.e.nodeAddresses(),
                         set([UnnamedOpetope.Address.epsilon(1)]))
        self.assertEqual(self.f.nodeAddresses(),
                         set([UnnamedOpetope.Address.epsilon(1),
                              UnnamedOpetope.Address.fromList(['*'], 1)]))

    def test_point(self):
        p = UnnamedOpetope.Preopetope.point()
        self.assertEqual(p, self.b)
        self.assertEqual(p.dimension, 0)
        self.assertFalse(p.isDegenerate)
        self.assertEqual(p.nodes, {})

    def test_source(self):
        with self.assertRaises(DerivationError):
            self.f.source(UnnamedOpetope.Address.fromList(['*', '*'], 1))
        self.assertEqual(self.c.source(UnnamedOpetope.Address.epsilon(0)),
                         self.b)
        self.assertEqual(self.f.source(UnnamedOpetope.Address.epsilon(1)),
                         self.c)
        self.assertEqual(
            self.f.source(UnnamedOpetope.Address.fromList(['*'], 1)),
            self.c)

    def test_substitution(self):
        i2 = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(1): self.c,
            UnnamedOpetope.Address.fromList(['*'], 1): self.c
        })
        i4 = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(1): self.c,
            UnnamedOpetope.Address.fromList(['*'], 1): self.c,
            UnnamedOpetope.Address.fromList(['*', '*'], 1): self.c,
            UnnamedOpetope.Address.fromList(['*', '*', '*'], 1): self.c
        })
        i5 = UnnamedOpetope.Preopetope.fromDictOfPreopetopes({
            UnnamedOpetope.Address.epsilon(1): self.c,
            UnnamedOpetope.Address.fromList(['*'], 1): self.c,
            UnnamedOpetope.Address.fromList(['*', '*'], 1): self.c,
            UnnamedOpetope.Address.fromList(['*', '*', '*'], 1): self.c,
            UnnamedOpetope.Address.fromList(['*', '*', '*', '*'], 1): self.c
        })
        ctx = UnnamedOpetope.Context(
            2) + (UnnamedOpetope.Address.fromList(['*', '*'], 1),
                  UnnamedOpetope.Address.epsilon(0))
        self.assertEqual(UnnamedOpetope.Preopetope.substitution(
            i4, UnnamedOpetope.Address.fromList(['*', '*'], 1), ctx, i2),
            i5)

    def test_toDict(self):
        for i in range(5):
            seq = UnnamedOpetope.OpetopicInteger(i).eval()
            self.assertEqual(
                seq,
                UnnamedOpetope.ProofTree(seq.source.toDict()).eval())


class Test_UnnamedOpetope_InferenceRules(unittest.TestCase):

    def setUp(self):
        pass

    def test_point(self):
        s = UnnamedOpetope.point()
        self.assertEqual(s.context, UnnamedOpetope.Context(0))
        self.assertEqual(s.source, UnnamedOpetope.Preopetope.point())
        self.assertEqual(s.target, UnnamedOpetope.Preopetope.empty())

    def test_degen(self):
        s = UnnamedOpetope.degen(UnnamedOpetope.point())
        self.assertEqual(
            s.context, UnnamedOpetope.Context(2) +
            (UnnamedOpetope.Address.epsilon(1),
             UnnamedOpetope.Address.epsilon(0)))
        self.assertEqual(
            s.source,
            UnnamedOpetope.Preopetope.degenerate(
                UnnamedOpetope.Preopetope.point()))
        self.assertEqual(
            s.target,
            UnnamedOpetope.shift(UnnamedOpetope.point()).source)

    def test_shift(self):
        s1 = UnnamedOpetope.shift(UnnamedOpetope.point())
        s2 = UnnamedOpetope.shift(s1)
        self.assertEqual(
            s2.context,
            UnnamedOpetope.Context(2) +
            (UnnamedOpetope.Address.epsilon(0).shift(),
             UnnamedOpetope.Address.epsilon(0)))
        p = UnnamedOpetope.Preopetope.point()
        a = UnnamedOpetope.Preopetope(1)
        a.nodes[UnnamedOpetope.Address.epsilon(0)] = p
        g = UnnamedOpetope.Preopetope(2)
        g.nodes[UnnamedOpetope.Address.epsilon(1)] = a
        self.assertEqual(s1.source, a)
        self.assertEqual(s1.target, p)
        self.assertEqual(s2.source, g)
        self.assertEqual(s2.target, a)

    def test_graft(self):
        i2 = UnnamedOpetope.OpetopicInteger(2).eval()
        i3 = UnnamedOpetope.OpetopicInteger(3).eval()
        s = UnnamedOpetope.shift(i3)
        s = UnnamedOpetope.graft(
            s, i2, UnnamedOpetope.Address.fromList([['*']], 2))
        s = UnnamedOpetope.graft(
            s, i2,
            UnnamedOpetope.Address.fromList([['*', '*']], 2))
        r = s.context
        self.assertEqual(
            r(UnnamedOpetope.Address.fromList([[]], 2)),
            UnnamedOpetope.Address.fromList([], 1))
        self.assertEqual(
            r(UnnamedOpetope.Address.fromList([['*'], []], 2)),
            UnnamedOpetope.Address.fromList(['*'], 1))
        self.assertEqual(
            r(UnnamedOpetope.Address.fromList([['*'], ['*']], 2)),
            UnnamedOpetope.Address.fromList(['*', '*'], 1))
        self.assertEqual(
            r(UnnamedOpetope.Address.fromList([['*', '*'], []], 2)),
            UnnamedOpetope.Address.fromList(['*', '*', '*'], 1))
        self.assertEqual(
            r(UnnamedOpetope.Address.fromList([['*', '*'], ['*']], 2)),
            UnnamedOpetope.Address.fromList(['*', '*', '*', '*'], 1))


class Test_UnnamedOpetope_Utils(unittest.TestCase):

    def setUp(self):
        pass

    def test_address(self):
        self.assertEqual(
            UnnamedOpetope.address('*'),
            UnnamedOpetope.Address.epsilon(0))
        self.assertEqual(
            UnnamedOpetope.address([['*'], [], ['*', '*']]),
            UnnamedOpetope.Address.fromList([['*'], [], ['*', '*']], 2))
        self.assertEqual(
            UnnamedOpetope.address([[], [], ['*', '*']]),
            UnnamedOpetope.Address.fromList([[], [], ['*', '*']], 2))
        with self.assertRaises(DerivationError):
            UnnamedOpetope.address([[[]]])
        with self.assertRaises(DerivationError):
            UnnamedOpetope.address([[[]]], 1)
        UnnamedOpetope.address([[[]]], 3)
        with self.assertRaises(DerivationError):
            UnnamedOpetope.address([[['*'], [['*']]]])

    def test_OpetopicTree(self):
        self.assertEqual(
            UnnamedOpetope.OpetopicTree(None).eval(),
            UnnamedOpetope.Degen(UnnamedOpetope.Arrow()).eval())
        for i in range(5):
            self.assertEqual(
                UnnamedOpetope.OpetopicTree([None] * i).eval(),
                UnnamedOpetope.Shift(UnnamedOpetope.OpetopicInteger(i)).eval())
        for i in range(5):
            tree = [None] * i + [[None]] + [None] * (4 - i)
            self.assertEqual(
                UnnamedOpetope.OpetopicTree(tree).eval(),
                UnnamedOpetope.Graft(
                    UnnamedOpetope.Shift(UnnamedOpetope.OpetopicInteger(5)),
                    UnnamedOpetope.OpetopicInteger(1),
                    UnnamedOpetope.address([['*'] * i], 2)).eval())

    def test_ProofTree(self):
        self.assertEqual(
            UnnamedOpetope.ProofTree({}).eval(),
            UnnamedOpetope.Point().eval())
        self.assertEqual(
            UnnamedOpetope.ProofTree({
                UnnamedOpetope.address('*'): {}
            }).eval(),
            UnnamedOpetope.Arrow().eval())
        self.assertEqual(
            UnnamedOpetope.ProofTree({
                None: {}
            }).eval(),
            UnnamedOpetope.OpetopicInteger(0).eval())
        self.assertEqual(
            UnnamedOpetope.ProofTree({
                UnnamedOpetope.address([], 1): {
                    UnnamedOpetope.address('*'): {}
                },
                UnnamedOpetope.address(['*']): {
                    UnnamedOpetope.address('*'): {}
                }
            }).eval(),
            UnnamedOpetope.OpetopicInteger(2).eval())
        with self.assertRaises(DerivationError):
            UnnamedOpetope.ProofTree({
                UnnamedOpetope.address(['*']): {
                    UnnamedOpetope.address('*'): {}
                }
            })
        with self.assertRaises(DerivationError):
            UnnamedOpetope.ProofTree({
                UnnamedOpetope.address([], 1): {
                    UnnamedOpetope.address('*'): {}
                },
                UnnamedOpetope.address(['*', '*']): {
                    UnnamedOpetope.address('*'): {}
                }
            }).eval()


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
            UnnamedOpetope.Shift(UnnamedOpetope.OpetopicInteger(2)),
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

    def test___getitem__(self):
        d = UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(0), "d")
        p = UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(2),
            {
                UnnamedOpetope.Address.epsilon(1): "a",
                UnnamedOpetope.Address.epsilon(0).shift(): "b"
            })
        with self.assertRaises(DerivationError):
            d[UnnamedOpetope.Address.epsilon(0)]
        self.assertEqual(p[UnnamedOpetope.Address.epsilon(1)], "a")
        self.assertEqual(p[UnnamedOpetope.Address.epsilon(0).shift()], "b")

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
                UnnamedOpetope.Address.epsilon(0).shift(): "b"
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
                UnnamedOpetope.Address.epsilon(0).shift(): "b"
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
                    UnnamedOpetope.Address.epsilon(0).shift(): "b"
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
                        UnnamedOpetope.Address.epsilon(0).shift(): "y"
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
            self.ctx.source("c", UnnamedOpetope.Address.epsilon(0).shift()),
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

    def test_fill(self):
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
                        UnnamedOpetope.Address.epsilon(0).shift(): "ab"
                    }))
        # Correct grafting: ab on top of bc
        UnnamedOpetopicSet.graft(
            self.seq,
            UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram(
                UnnamedOpetope.OpetopicInteger(2),
                {
                    UnnamedOpetope.Address.epsilon(1): "bc",
                    UnnamedOpetope.Address.epsilon(0).shift(): "ab"
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


class Test_NamedOpetope_Variable(unittest.TestCase):

    def setUp(self):
        self.a0 = NamedOpetope.Variable("a", 0)
        self.b0 = NamedOpetope.Variable("b", 0)
        self.c1 = NamedOpetope.Variable("c", 1)
        self.a1 = NamedOpetope.Variable("a", 1)

    def test___eq__(self):
        self.assertEqual(self.a0, self.a0)
        self.assertEqual(self.b0, self.b0)
        self.assertEqual(self.c1, self.c1)
        self.assertEqual(self.a1, self.a1)
        self.assertNotEqual(self.a0, self.b0)
        self.assertNotEqual(self.a0, self.c1)
        self.assertNotEqual(self.a0, self.a1)

    def test___init__(self):
        with self.assertRaises(DerivationError):
            NamedOpetope.Variable("x", -1)
        NamedOpetope.Variable("x", 0)


class Test_NamedOpetope_Term(unittest.TestCase):

    def setUp(self):
        self.w = NamedOpetope.Variable("w", 2)
        self.x = NamedOpetope.Variable("x", 2)
        self.y = NamedOpetope.Variable("y", 2)
        self.z = NamedOpetope.Variable("z", 2)
        self.a = NamedOpetope.Variable("a", 1)
        self.b = NamedOpetope.Variable("b", 1)
        self.c = NamedOpetope.Variable("c", 1)
        self.d = NamedOpetope.Variable("d", 1)
        self.e = NamedOpetope.Variable("e", 1)
        # t = w (a <- x, b <- y (c <- z, d <- _e_))
        self.tw = NamedOpetope.Term(self.w)
        self.tx = NamedOpetope.Term(self.x)
        self.ty = NamedOpetope.Term(self.y)
        self.tz = NamedOpetope.Term(self.z)
        self.ty[self.c] = self.tz
        self.ty[self.d] = NamedOpetope.Term(self.e, True)
        self.tw[self.a] = self.tx
        self.tw[self.b] = self.ty

    def test___contains__(self):
        self.assertIn(self.a, self.tw)
        self.assertIn(self.b, self.tw)
        self.assertIn(self.c, self.tw)
        self.assertIn(self.d, self.tw)
        self.assertNotIn(self.e, self.tw)
        self.assertIn(self.w, self.tw)
        self.assertIn(self.x, self.tw)
        self.assertIn(self.y, self.tw)
        self.assertIn(self.z, self.tw)
        self.assertNotIn(self.a, self.tx)
        self.assertNotIn(self.b, self.tx)
        self.assertNotIn(self.c, self.tx)
        self.assertNotIn(self.d, self.tx)
        self.assertNotIn(self.e, self.tx)
        self.assertNotIn(self.w, self.tx)
        self.assertIn(self.x, self.tx)
        self.assertNotIn(self.y, self.tx)
        self.assertNotIn(self.z, self.tx)
        self.assertNotIn(self.a, self.ty)
        self.assertNotIn(self.b, self.ty)
        self.assertIn(self.c, self.ty)
        self.assertIn(self.d, self.ty)
        self.assertNotIn(self.e, self.ty)
        self.assertNotIn(self.w, self.ty)
        self.assertNotIn(self.x, self.ty)
        self.assertIn(self.y, self.ty)
        self.assertIn(self.z, self.ty)
        self.assertNotIn(self.a, self.tz)
        self.assertNotIn(self.b, self.tz)
        self.assertNotIn(self.c, self.tz)
        self.assertNotIn(self.d, self.tz)
        self.assertNotIn(self.e, self.tz)
        self.assertNotIn(self.w, self.tz)
        self.assertNotIn(self.x, self.tz)
        self.assertNotIn(self.y, self.tz)
        self.assertIn(self.z, self.tz)

    def test___eq__(self):
        self.assertEqual(self.tw, self.tw)
        self.assertEqual(self.tx, self.tx)
        self.assertEqual(self.ty, self.ty)
        self.assertEqual(self.tz, self.tz)
        self.assertNotEqual(self.tx, self.tz)
        self.assertNotEqual(self.tw, NamedOpetope.Term(self.w))
        self.assertNotEqual(
            NamedOpetope.Term(NamedOpetope.Variable("x", 0)),
            NamedOpetope.Term(NamedOpetope.Variable("x", 1)))

    def test_dim(self):
        self.assertEqual(self.tw.dimension, 2)
        self.assertEqual(self.tx.dimension, 2)
        self.assertEqual(self.ty.dimension, 2)
        self.assertEqual(self.tz.dimension, 2)
        self.assertEqual(NamedOpetope.Term(self.e, True).dimension, 2)

    def test_graftTuples(self):
        self.assertEqual(self.tw.graftTuples(),
                         {(self.a, self.x), (self.b, self.y),
                          (self.c, self.z)})

    def test_isVariable(self):
        self.assertFalse(self.tw.isVariable())
        self.assertTrue(self.tx.isVariable())
        self.assertFalse(self.ty.isVariable())
        self.assertTrue(self.tz.isVariable())

    def test_variables(self):
        self.assertEqual(self.tw.variables(0), set())
        self.assertEqual(self.tw.variables(1),
                         {self.a, self.b, self.c, self.d})
        self.assertEqual(self.tw.variables(2),
                         {self.w, self.x, self.y, self.z})


class Test_NamedOpetope_Type(unittest.TestCase):

    def setUp(self):
        self.a = NamedOpetope.Variable("a", 0)
        self.f = NamedOpetope.Variable("f", 1)
        self.alpha = NamedOpetope.Variable("α", 2)
        self.t0 = NamedOpetope.Type([NamedOpetope.Term()])
        self.t1 = NamedOpetope.Type(
            [NamedOpetope.Term(self.a), NamedOpetope.Term()])
        self.t2 = NamedOpetope.Type(
            [NamedOpetope.Term(self.f), NamedOpetope.Term(self.a),
             NamedOpetope.Term()])
        self.t3 = NamedOpetope.Type(
            [NamedOpetope.Term(self.alpha), NamedOpetope.Term(self.f),
             NamedOpetope.Term(self.a), NamedOpetope.Term()])

    def test___contains__(self):
        self.assertNotIn(self.a, self.t0)
        self.assertNotIn(self.f, self.t0)
        self.assertNotIn(self.alpha, self.t0)
        self.assertIn(self.a, self.t1)
        self.assertNotIn(self.f, self.t1)
        self.assertNotIn(self.alpha, self.t1)
        self.assertIn(self.a, self.t2)
        self.assertIn(self.f, self.t2)
        self.assertNotIn(self.alpha, self.t2)
        self.assertIn(self.a, self.t3)
        self.assertIn(self.f, self.t3)
        self.assertIn(self.alpha, self.t3)
        self.assertNotIn(NamedOpetope.Variable("β", 2), self.t3)
        self.assertNotIn(NamedOpetope.Variable("a", 2), self.t3)

    def test___init__(self):
        with self.assertRaises(DerivationError):
            NamedOpetope.Type(
                [NamedOpetope.Term(NamedOpetope.Variable("α", 3)),
                 NamedOpetope.Term(self.f),
                 NamedOpetope.Term(self.a),
                 NamedOpetope.Term()])
        with self.assertRaises(DerivationError):
            NamedOpetope.Type(
                [NamedOpetope.Term(self.alpha),
                 NamedOpetope.Term(self.f),
                 NamedOpetope.Term(NamedOpetope.Variable("a", 1)),
                 NamedOpetope.Term()])
        with self.assertRaises(DerivationError):
            NamedOpetope.Type([])

    def test_variables(self):
        self.assertEqual(self.t3.variables(0), {self.a})
        self.assertEqual(self.t3.variables(1), {self.f})
        self.assertEqual(self.t3.variables(2), {self.alpha})
        self.assertEqual(self.t3.variables(3), set())


class Test_NamedOpetope_Typing(unittest.TestCase):

    def test___init__(self):
        NamedOpetope.Typing(
            NamedOpetope.Term(NamedOpetope.Variable("a", 0)),
            NamedOpetope.Type([NamedOpetope.Term()]))
        NamedOpetope.Typing(
            NamedOpetope.Term(NamedOpetope.Variable("f", 1)),
            NamedOpetope.Type(
                [NamedOpetope.Term(NamedOpetope.Variable("a", 0)),
                 NamedOpetope.Term()]))
        with self.assertRaises(DerivationError):
            NamedOpetope.Typing(
                NamedOpetope.Term(NamedOpetope.Variable("a", 1)),
                NamedOpetope.Type([NamedOpetope.Term()]))
        with self.assertRaises(DerivationError):
            NamedOpetope.Typing(
                NamedOpetope.Term(NamedOpetope.Variable("f", 2)),
                NamedOpetope.Type(
                    [NamedOpetope.Term(NamedOpetope.Variable("a", 0)),
                     NamedOpetope.Term()]))
        with self.assertRaises(DerivationError):
            NamedOpetope.Typing(
                NamedOpetope.Term(NamedOpetope.Variable("f", 0)),
                NamedOpetope.Type(
                    [NamedOpetope.Term(NamedOpetope.Variable("a", 0)),
                     NamedOpetope.Term()]))


class Test_NamedOpetope_Context(unittest.TestCase):

    def setUp(self):
        self.term1 = NamedOpetope.Term(NamedOpetope.Variable("a", 0))
        self.term2 = NamedOpetope.Term(NamedOpetope.Variable("f", 1))
        self.term3 = NamedOpetope.Term(NamedOpetope.Variable("α", 2))
        self.term4 = NamedOpetope.Term(NamedOpetope.Variable("A", 3))
        self.typing1 = NamedOpetope.Type([NamedOpetope.Term()])
        self.typing2 = NamedOpetope.Type([self.term1, NamedOpetope.Term()])
        self.typing3 = NamedOpetope.Type(
            [self.term2, self.term1, NamedOpetope.Term()])
        self.typing4 = NamedOpetope.Type(
            [self.term3, self.term2, self.term1, NamedOpetope.Term()])
        self.ctx1 = NamedOpetope.Context()
        self.ctx2 = self.ctx1 + NamedOpetope.Typing(self.term1, self.typing1)
        self.ctx3 = self.ctx2 + NamedOpetope.Typing(self.term2, self.typing2)
        self.ctx4 = self.ctx3 + NamedOpetope.Typing(self.term3, self.typing3)
        self.ctx5 = self.ctx4 + NamedOpetope.Typing(self.term4, self.typing4)

    def test___add__(self):
        with self.assertRaises(DerivationError):
            self.ctx5 + NamedOpetope.Typing(self.term1, self.typing1)
        with self.assertRaises(DerivationError):
            self.ctx5 + NamedOpetope.Typing(self.term2, self.typing2)
        with self.assertRaises(DerivationError):
            self.ctx5 + NamedOpetope.Typing(self.term3, self.typing3)
        with self.assertRaises(DerivationError):
            self.ctx5 + NamedOpetope.Typing(self.term4, self.typing4)
        term = NamedOpetope.Term(NamedOpetope.Variable("x", 2))
        term[NamedOpetope.Variable("a", 1)] = NamedOpetope.Term(
            NamedOpetope.Variable("y", 2))
        typing = NamedOpetope.Typing(term, self.typing3)
        with self.assertRaises(DerivationError):
            self.ctx5 + typing

    def test___contains__(self):
        self.assertNotIn(self.term1.variable, self.ctx1)
        self.assertIn(self.term1.variable, self.ctx2)
        self.assertIn(self.term1.variable, self.ctx3)
        self.assertIn(self.term1.variable, self.ctx4)
        self.assertIn(self.term1.variable, self.ctx5)
        self.assertNotIn(self.term2.variable, self.ctx1)
        self.assertNotIn(self.term2.variable, self.ctx2)
        self.assertIn(self.term2.variable, self.ctx3)
        self.assertIn(self.term2.variable, self.ctx4)
        self.assertIn(self.term2.variable, self.ctx5)
        self.assertNotIn(self.term3.variable, self.ctx1)
        self.assertNotIn(self.term3.variable, self.ctx2)
        self.assertNotIn(self.term3.variable, self.ctx3)
        self.assertIn(self.term3.variable, self.ctx4)
        self.assertIn(self.term3.variable, self.ctx5)
        self.assertNotIn(self.term4.variable, self.ctx1)
        self.assertNotIn(self.term4.variable, self.ctx2)
        self.assertNotIn(self.term4.variable, self.ctx3)
        self.assertNotIn(self.term4.variable, self.ctx4)
        self.assertIn(self.term4.variable, self.ctx5)

    def test_source(self):
        with self.assertRaises(DerivationError):
            self.ctx5.source(NamedOpetope.Variable("A", 3), -1)
        with self.assertRaises(DerivationError):
            self.ctx5.source(NamedOpetope.Variable("A", 3), 5)
        self.assertEqual(self.ctx5.source(NamedOpetope.Variable("A", 3), 0),
                         NamedOpetope.Term(NamedOpetope.Variable("A", 3)))
        self.assertEqual(self.ctx5.source(NamedOpetope.Variable("A", 3), 1),
                         NamedOpetope.Term(NamedOpetope.Variable("α", 2)))
        self.assertEqual(self.ctx5.source(NamedOpetope.Variable("A", 3), 2),
                         NamedOpetope.Term(NamedOpetope.Variable("f", 1)))
        self.assertEqual(self.ctx5.source(NamedOpetope.Variable("A", 3), 3),
                         NamedOpetope.Term(NamedOpetope.Variable("a", 0)))
        self.assertEqual(self.ctx5.source(NamedOpetope.Variable("A", 3), 4),
                         NamedOpetope.Term())

    def test_typeOf(self):
        with self.assertRaises(DerivationError):
            self.ctx1.typeOf(NamedOpetope.Variable("a", 0))
        with self.assertRaises(DerivationError):
            self.ctx2.typeOf(NamedOpetope.Variable("b", 0))
        self.assertEqual(self.ctx5.typeOf(NamedOpetope.Variable("a", 0)).terms,
                         self.typing1.terms)
        self.assertEqual(self.ctx5.typeOf(NamedOpetope.Variable("f", 1)).terms,
                         self.typing2.terms)
        self.assertEqual(self.ctx5.typeOf(NamedOpetope.Variable("α", 2)).terms,
                         self.typing3.terms)
        self.assertEqual(self.ctx5.typeOf(NamedOpetope.Variable("A", 3)).terms,
                         self.typing4.terms)


class Test_NamedOpetope_EquationalTheory(unittest.TestCase):

    def setUp(self):
        self.a0 = NamedOpetope.Variable("a", 0)
        self.b0 = NamedOpetope.Variable("b", 0)
        self.c0 = NamedOpetope.Variable("c", 0)
        self.d0 = NamedOpetope.Variable("d", 0)
        self.e0 = NamedOpetope.Variable("e", 0)
        self.a1 = NamedOpetope.Variable("a", 1)
        self.th1 = NamedOpetope.EquationalTheory()
        self.th2 = self.th1 + (self.a0, self.b0)
        self.th3 = self.th2 + (self.c0, self.d0)
        self.th4 = self.th3 + (self.c0, self.e0)
        self.th5 = self.th4 + (self.b0, self.a0)
        self.th6 = self.th5 + (self.a0, self.e0)

    def test___add__(self):
        with self.assertRaises(DerivationError):
            NamedOpetope.EquationalTheory() + (self.a0, self.a1)
        self.assertEqual(len(self.th2.classes), 1)
        self.assertEqual(self.th2.classes[0], {self.a0, self.b0})
        self.assertEqual(len(self.th3.classes), 2)
        self.assertEqual(self.th3.classes[0], {self.a0, self.b0})
        self.assertEqual(self.th3.classes[1], {self.c0, self.d0})
        self.assertEqual(len(self.th4.classes), 2)
        self.assertEqual(self.th4.classes[0], {self.a0, self.b0})
        self.assertEqual(self.th4.classes[1], {self.c0, self.d0, self.e0})
        self.assertEqual(len(self.th5.classes), 2)
        self.assertEqual(self.th5.classes[0], {self.a0, self.b0})
        self.assertEqual(self.th5.classes[1], {self.c0, self.d0, self.e0})
        self.assertEqual(len(self.th6.classes), 1)
        self.assertEqual(self.th6.classes[0],
                         {self.a0, self.b0, self.c0, self.d0, self.e0})

    def test___or__(self):
        self.assertFalse((self.th1 | self.th1).equal(self.a0, self.b0))
        self.assertFalse((self.th1 | self.th2).equal(self.a0, self.c0))
        self.assertTrue((self.th2 | self.th2).equal(self.a0, self.b0))
        self.assertTrue(
            (self.th2 | (NamedOpetope.EquationalTheory() + (self.b0, self.e0)))
            .equal(self.e0, self.a0))

    def test_classOf(self):
        self.assertEqual(self.th1.classOf(self.a0), set({self.a0}))
        self.assertEqual(self.th1.classOf(self.b0), set({self.b0}))
        self.assertEqual(self.th1.classOf(self.c0), set({self.c0}))
        self.assertEqual(self.th1.classOf(self.d0), set({self.d0}))
        self.assertEqual(self.th1.classOf(self.e0), set({self.e0}))
        self.assertEqual(self.th1.classOf(self.a1), set({self.a1}))
        self.assertEqual(self.th2.classOf(self.a0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th2.classOf(self.b0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th2.classOf(self.c0), set({self.c0}))
        self.assertEqual(self.th2.classOf(self.d0), set({self.d0}))
        self.assertEqual(self.th2.classOf(self.e0), set({self.e0}))
        self.assertEqual(self.th2.classOf(self.a1), set({self.a1}))
        self.assertEqual(self.th3.classOf(self.a0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th3.classOf(self.b0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th3.classOf(self.c0),
                         set({self.c0, self.d0}))
        self.assertEqual(self.th3.classOf(self.d0),
                         set({self.c0, self.d0}))
        self.assertEqual(self.th3.classOf(self.e0), set({self.e0}))
        self.assertEqual(self.th3.classOf(self.a1), set({self.a1}))
        self.assertEqual(self.th4.classOf(self.a0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th4.classOf(self.b0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th4.classOf(self.c0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th4.classOf(self.d0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th4.classOf(self.e0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th4.classOf(self.a1), set({self.a1}))
        self.assertEqual(self.th5.classOf(self.a0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th5.classOf(self.b0),
                         set({self.a0, self.b0}))
        self.assertEqual(self.th5.classOf(self.c0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th5.classOf(self.d0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th5.classOf(self.e0),
                         set({self.c0, self.d0, self.e0}))
        self.assertEqual(self.th5.classOf(self.a1), set({self.a1}))
        self.assertEqual(self.th6.classOf(self.a0),
                         set({self.a0, self.b0, self.c0, self.d0,
                              self.e0}))
        self.assertEqual(self.th6.classOf(self.b0),
                         set({self.a0, self.b0, self.c0, self.d0,
                              self.e0}))
        self.assertEqual(self.th6.classOf(self.c0),
                         set({self.a0, self.b0, self.c0, self.d0,
                              self.e0}))
        self.assertEqual(self.th6.classOf(self.d0),
                         set({self.a0, self.b0, self.c0, self.d0,
                              self.e0}))
        self.assertEqual(self.th6.classOf(self.e0),
                         set({self.a0, self.b0, self.c0, self.d0,
                              self.e0}))
        self.assertEqual(self.th6.classOf(self.a1), set({self.a1}))

    def test_equal(self):
        self.assertTrue(self.th2.equal(self.a0, self.b0))
        self.assertTrue(self.th2.equal(self.b0, self.a0))
        self.assertFalse(self.th2.equal(self.a0, self.a1))
        self.assertFalse(self.th2.equal(self.c0, self.d0))
        self.assertTrue(self.th3.equal(self.a0, self.b0))
        self.assertTrue(self.th3.equal(self.c0, self.d0))
        self.assertFalse(self.th3.equal(self.a0, self.c0))
        self.assertFalse(self.th3.equal(self.a0, self.d0))
        self.assertFalse(self.th4.equal(self.a0, self.e0))
        self.assertFalse(self.th4.equal(self.b0, self.e0))
        self.assertTrue(self.th6.equal(self.a0, self.b0))
        self.assertTrue(self.th6.equal(self.a0, self.c0))
        self.assertTrue(self.th6.equal(self.a0, self.d0))
        self.assertTrue(self.th6.equal(self.a0, self.e0))

    def test_isIn(self):
        self.assertTrue(self.th1.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th1.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th1.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th1.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th1.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th1.isIn(self.a1, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th2.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th2.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th2.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th2.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th2.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th2.isIn(self.a1, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th3.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th3.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th3.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th3.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th3.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th3.isIn(self.a1, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th4.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th4.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th4.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th4.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th4.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th4.isIn(self.a1, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th5.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th5.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th5.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th5.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th5.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th5.isIn(self.a1, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th6.isIn(self.a0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th6.isIn(self.b0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th6.isIn(self.c0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th6.isIn(self.d0, NamedOpetope.Term(self.a0)))
        self.assertTrue(self.th6.isIn(self.e0, NamedOpetope.Term(self.a0)))
        self.assertFalse(self.th6.isIn(self.a1, NamedOpetope.Term(self.a0)))


class Test_NamedOpetope_Sequent(unittest.TestCase):

    def setUp(self):
        self.a1 = NamedOpetope.Variable("a1", 0)
        self.b1 = NamedOpetope.Variable("b1", 0)
        self.c1 = NamedOpetope.Variable("c1", 0)
        self.a2 = NamedOpetope.Variable("a2", 0)
        self.b2 = NamedOpetope.Variable("b2", 0)
        self.c2 = NamedOpetope.Variable("c2", 0)
        self.f = NamedOpetope.Variable("f", 1)
        self.g = NamedOpetope.Variable("g", 1)
        self.h = NamedOpetope.Variable("h", 1)
        self.i = NamedOpetope.Variable("h", 1)
        ctx = NamedOpetope.Context() + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.a1),
                NamedOpetope.Type([NamedOpetope.Term()])) + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.b1),
                NamedOpetope.Type([NamedOpetope.Term()])) + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.c1),
                NamedOpetope.Type([NamedOpetope.Term()])) + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.f),
                NamedOpetope.Type(
                    [NamedOpetope.Term(self.a2),
                     NamedOpetope.Term()])) + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.g),
                NamedOpetope.Type(
                    [NamedOpetope.Term(self.b2), NamedOpetope.Term()])) + \
            NamedOpetope.Typing(
                NamedOpetope.Term(self.h),
                NamedOpetope.Type(
                    [NamedOpetope.Term(self.c2), NamedOpetope.Term()]))
        eqth = NamedOpetope.EquationalTheory() + \
            (self.b1, self.b2) + \
            (self.c1, self.c2) + \
            (self.h, self.i)
        self.sequent = NamedOpetope.Sequent(eqth, ctx, None)
        self.fg = self.sequent.graft(
            NamedOpetope.Term(self.g), self.b2, NamedOpetope.Term(self.f))
        self.gh = self.sequent.graft(
            NamedOpetope.Term(self.h), self.c2, NamedOpetope.Term(self.g))
        self.fgh1 = self.sequent.graft(
            self.gh, self.b2, NamedOpetope.Term(self.f))
        self.fgh2 = self.sequent.graft(
            NamedOpetope.Term(self.h), self.c2, self.fg)

    def test_equal(self):
        self.assertTrue(self.sequent.equal(self.fgh1, self.fgh2))
        self.assertTrue(self.sequent.equal(
            NamedOpetope.Term(self.h), NamedOpetope.Term(self.i)))
        self.assertTrue(self.sequent.equal(
            self.sequent.graft(NamedOpetope.Term(self.i), self.c1, self.fg),
            self.fgh1))
        self.assertTrue(self.sequent.equal(
            self.sequent.graft(NamedOpetope.Term(self.i), self.c1, self.fg),
            self.fgh2))
        self.assertFalse(self.sequent.equal(
            self.gh, NamedOpetope.Term(self.h)))
        self.assertFalse(self.sequent.equal(
            self.gh, NamedOpetope.Term(self.g)))
        self.assertFalse(self.sequent.equal(self.gh, self.fg))

    def test_graft(self):
        """
        :todo: Test degenerate grafting
        """
        self.assertEqual(NamedOpetope.Term(self.g),
                         self.sequent.graft(NamedOpetope.Term(self.g), self.c1,
                                            NamedOpetope.Term(self.f)))
        self.assertEqual(self.fgh1, self.fgh2)
        self.assertEqual(len(self.fgh1.keys()), 1)
        self.assertTrue(self.sequent.theory.equal(
            list(self.fgh1.keys())[0], self.c1))
        t = list(self.fgh1.values())[0]
        self.assertTrue(self.sequent.theory.equal(t.variable, self.g))
        self.assertEqual(len(t.keys()), 1)
        self.assertTrue(self.sequent.theory.equal(
            list(t.keys())[0], self.b1))
        self.assertTrue(self.sequent.theory.equal(
            list(t.values())[0].variable, self.f))
        with self.assertRaises(DerivationError):
            self.sequent.graft(self.fg, self.b1, NamedOpetope.Term(self.f))

    def test_substitute(self):
        res = self.sequent.substitute(self.fg, self.gh, self.g)
        self.assertIs(res[1], None)
        self.assertEqual(res[0], self.fgh1)
        res = self.sequent.substitute(self.gh, self.fg, self.g)
        self.assertEqual(res[0], self.fgh1)
        self.assertIs(res[1], None)
        res = self.sequent.substitute(
            NamedOpetope.Term(self.f), NamedOpetope.Term(self.f), self.f)
        self.assertEqual(res[0], NamedOpetope.Term(self.f))
        self.assertIs(res[1], None)
        res = self.sequent.substitute(
            NamedOpetope.Term(self.f), NamedOpetope.Term(self.fg), self.f)
        self.assertEqual(res[0], NamedOpetope.Term(self.fg))
        self.assertIs(res[1], None)
        res = self.sequent.substitute(
            NamedOpetope.Term(self.f), NamedOpetope.Term(self.fg), self.g)
        self.assertEqual(res[0], NamedOpetope.Term(self.f))
        self.assertIs(res[1], None)
        res = self.sequent.substitute(
            NamedOpetope.Term(self.f), NamedOpetope.Term(self.fgh1), self.f)
        self.assertEqual(res[0], NamedOpetope.Term(self.fgh1))
        self.assertIs(res[1], None)
        res = self.sequent.substitute(
            self.fgh1, NamedOpetope.Term(self.c1, True), self.g)
        self.assertEqual(
            res[0], self.sequent.graft(NamedOpetope.Term(self.h), self.c2,
                                       NamedOpetope.Term(self.f)))
        res = self.sequent.substitute(
            self.fgh1, NamedOpetope.Term(self.b1, True), self.f)
        self.assertTrue(self.sequent.equal(res[0], self.gh))


class Test_NamedOpetope_InferenceRules(unittest.TestCase):

    def setUp(self):
        pass

    def test_point(self):
        s = NamedOpetope.point("x")
        self.assertEqual(
            s.typing.term, NamedOpetope.Term(NamedOpetope.Variable("x", 0)))
        self.assertEqual(len(s.context), 1)

    def test_fill(self):
        pass

    def test_degen(self):
        s = NamedOpetope.point("x")
        s = NamedOpetope.degen(s)
        self.assertEqual(
            s.typing.term, NamedOpetope.Term(
                NamedOpetope.Variable("x", 0), True))
        self.assertEqual(len(s.context), 1)
        with self.assertRaises(DerivationError):
            NamedOpetope.degen(s)

    def test_degenfill(self):
        pass

    def test_graft(self):
        pass


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

    def test_fold(self):
        a = NamedOpetopicSet.Repr(NamedOpetope.OpetopicInteger(3)).eval()
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.fold(a, "a_1", "f_1")
        with self.assertRaises(DerivationError):
            NamedOpetopicSet.fold(a, "f_1", "f_2")
        a = NamedOpetopicSet.fold(a, "a_1", "a_2")
        a = NamedOpetopicSet.fold(a, "a_1", "a_3")
        a = NamedOpetopicSet.fold(a, "a_1", "ttA")
        a = NamedOpetopicSet.fold(a, "f_1", "f_2")
        a = NamedOpetopicSet.fold(a, "f_1", "f_3")
        a = NamedOpetopicSet.fold(a, "f_1", "tA")
        self.assertEqual(len(a.theory.classes), 2)

    def test_zero(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity = 2)
