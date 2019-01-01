import unittest

from common import DerivationError

import NamedOpetope


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

    def test_shift(self):
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

    def test_degenshift(self):
        pass

    def test_graft(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity = 2)
