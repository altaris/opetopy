import unittest

import sys
sys.path.insert(0, "../")

from opetopy.common import DerivationError

from opetopy import UnnamedOpetope


class Test_UnnamedOpetope_Address(unittest.TestCase):

    def setUp(self):
        self.a = UnnamedOpetope.Address.epsilon(0)
        self.b = UnnamedOpetope.Address.epsilon(1)
        self.c = UnnamedOpetope.Address.fromListOfAddresses([self.a])
        self.d = UnnamedOpetope.Address.fromListOfAddresses([self.a, self.a])
        self.e = UnnamedOpetope.Address.fromList([['*'], ['*', '*'], []], 2)

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
        self.assertEqual(UnnamedOpetope.Address.fromList([[]], 1), self.c)
        self.assertEqual(UnnamedOpetope.Address.fromList(['*'], 1), self.c)
        self.assertEqual(UnnamedOpetope.Address.fromList([[], []], 1),
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
                [['*'], ['*', '*'], [], ['*', '*'], []], 2)
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


if __name__ == "__main__":
    unittest.main(verbosity = 2)
