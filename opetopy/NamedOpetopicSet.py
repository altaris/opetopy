# -*- coding: utf-8 -*-

"""
.. module:: NamedOpetopicSet
   :synopsis: Implementation of the named approach
              for opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy

from opetopy.common import *
from opetopy import NamedOpetope


def repres(seq: NamedOpetope.Sequent) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!$}` :math:`\\texttt{repr}` rule.
    """
    if not seq.typing.term.isVariable():
        raise DerivationError(
            "repr rule",
            "Opt! sequent expected to type a variable, typing {term}",
            term=repr(seq.typing.term))
    res = NamedOpetope.OCMT(deepcopy(seq.theory), deepcopy(seq.context))
    # new context
    for typing in seq.context:
        v = typing.term.variable
        if v is None:
            raise RuntimeError("[repres rule] The premiss context types an "
                               "invalid / null term. In valid proof trees, "
                               "this should not happen")
        for i in range(1, v.dimension + 1):
            res.context += NamedOpetope.Typing(
                NamedOpetope.Term(res.target(v, i)),
                NamedOpetope.Type(typing.type.terms[i:]))
    # new theory
    for tup in seq.context.graftTuples():
        b, a = tup
        res.theory += (res.target(a), b)
    for a in res.context.variables():
        if a.dimension >= 2 and not res.source(a).degenerate:
            s = res.source(a).variable
            if s is None:
                raise RuntimeError("[repres rule] The premiss context types "
                                   "the variable {a} of dimension {dim}, "
                                   "whose first source is invalid / null. In "
                                   "valid proof trees, this should not happen"
                                   .format(a=str(a), dim=a.dimension))
            res.theory += (res.target(a, 2), res.target(s))
    for a in seq.context.variables():
        for k in range(0, a.dimension - 1):
            if res.source(res.target(a, k)).degenerate:
                c = res.source(res.target(a, k)).variable
                if c is None:
                    raise RuntimeError("[repres rule] The premiss context "
                                       "types the variable {var} of dimension "
                                       "{dim}, whose first source is invalid "
                                       "/ null. In valid proof trees, this "
                                       "should not happen".format(
                                           var=str(res.target(a, k)),
                                           dim=res.target(a, k).dimension))
                res.theory += (res.target(a, k + 2), c)
    # identification of targets
    tmp = deepcopy(res.theory)
    for cls in tmp.classes:
        elems = list(cls)
        dim = elems[0].dimension
        for i in range(1, len(cls)):
            for k in range(1, dim + 1):
                res.theory += (res.target(elems[0], k),
                               res.target(elems[i], k))
    return res


def sum(ocmt1: NamedOpetope.OCMT,
        ocmt2: NamedOpetope.OCMT) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!$}` :math:`\\texttt{sum}` rule.
    """
    if len(ocmt1.context.variables() & ocmt2.context.variables()) != 0:
        raise DerivationError(
            "sum rule",
            "The two premiss OCTM are expected to have disjoint contexts, "
            "but intersection types the following variables {inter}",
            inter=ocmt1.context.variables() & ocmt2.context.variables())
    return NamedOpetope.OCMT(
        ocmt1.theory | ocmt2.theory, ocmt1.context | ocmt2.context)


def glue(ocmt: NamedOpetope.OCMT, aName: str, bName: str) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!$}` :math:`\\texttt{glue}` rule.
    """
    a = ocmt.context[aName]
    b = ocmt.context[bName]
    if a.dimension != b.dimension:
        raise DerivationError(
            "glue rule",
            "NamedOpetope.Variables {a} and {b} cannot be identified as they "
            "do not have the same dimension (have respectively {da} and {db})",
            a=str(a), b=str(b), da=a.dimension, db=b.dimension)
    elif a.dimension != 0 and not \
        (ocmt.equal(ocmt.source(a), ocmt.source(b)) and
         ocmt.theory.equal(ocmt.target(a), ocmt.target(b))):
        raise DerivationError(
            "glue rule",
            "NamedOpetope.Variables {a} and {b} cannot be identified as they "
            "are not parallel: sa = {sa}, sb = {sb}, ta = {ta}, tb = {tb}",
            a=str(a), b=str(b), sa=str(ocmt.source(a)),
            sb=str(ocmt.source(b)), ta=str(ocmt.target(a)),
            tb=str(ocmt.target(b)))
    res = deepcopy(ocmt)
    res.theory += (a, b)
    return res


def zero() -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!$}` :math:`\\texttt{zero}` rule.
    """
    return NamedOpetope.OCMT(
        NamedOpetope.EquationalTheory(), NamedOpetope.Context())


class RuleInstance(AbstractRuleInstance):
    """
    A rule instance of system :math:`\\textbf{OptSet${}^!$}`.
    """

    def eval(self) -> NamedOpetope.OCMT:
        """
        Pure virtual method evaluating a proof tree and returning the final
        conclusion sequent, or raising an exception if the proof is invalid.
        """
        raise NotImplementedError()


class Repr(RuleInstance):
    """
    A class representing an instance of the ``repr`` rule in a proof tree.
    """

    proofTree: NamedOpetope.RuleInstance

    def __init__(self, p: NamedOpetope.RuleInstance) -> None:
        self.proofTree = p

    def __repr__(self) -> str:
        return "Repr({})".format(repr(self.proofTree))

    def __str__(self) -> str:
        return "Repr({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{repr}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        return repres(self.proofTree.eval())


class Sum(RuleInstance):
    """
    A class representing an instance of the ``sum`` rule in a proof tree.
    """

    proofTree1: RuleInstance
    proofTree2: RuleInstance

    def __init__(self, p1: RuleInstance, p2: RuleInstance) -> None:
        """
        Creates an instance of the ``graft`` rule at variable ``a``, and plugs
        proof tree ``p1`` on the first premise, and ``p2`` on the second.

        :see: :func:`opetopy.NamedOpetope.graft`.
        """
        self.proofTree1 = p1
        self.proofTree2 = p2

    def __repr__(self) -> str:
        return "Sum({p1}, {p2})".format(
            p1=repr(self.proofTree1), p2=repr(self.proofTree2))

    def __str__(self) -> str:
        return "Sum({p1}, {p2})".format(
            p1=str(self.proofTree1), p2=str(self.proofTree2))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree1._toTex() + "\n\t" + self.proofTree2._toTex() + \
            "\n\t\\RightLabel{\\texttt{sum}" + \
            "}\n\t\\BinaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        return sum(self.proofTree1.eval(), self.proofTree2.eval())


class Glue(RuleInstance):
    """
    A class representing an instance of the ``glue`` rule in a proof tree.
    """

    proofTree: RuleInstance
    aName: str
    bName: str

    def __init__(self, p: RuleInstance, a: str, b: str) -> None:
        self.proofTree = p
        self.aName = a
        self.bName = b

    def __repr__(self) -> str:
        return "Glue({p}, {a}, {b})".format(p=repr(self.proofTree),
                                            a=repr(self.aName),
                                            b=repr(self.bName))

    def __str__(self) -> str:
        return "Glue({p}, {a}, {b})".format(p=str(self.proofTree),
                                            a=str(self.aName),
                                            b=str(self.bName))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{glue-}$(" + self.aName + \
            " = " + self.bName + ")$}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        """
        Evaluates this instance of ``graft`` by first evaluating its premises,
        and then applying :func:`opetopy.NamedOpetope.graft` at variable
        `self.a` on the resulting sequents.
        """
        return glue(self.proofTree.eval(), self.aName, self.bName)


class Zero(RuleInstance):
    """
    A class representing an instance of the ``zero`` rule in a proof tree.
    """

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return "\\AxiomC{}\n\t\\RightLabel{\\texttt{zero}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

        def __repr__(self) -> str:
            return "Zero()"

        def __str__(self) -> str:
            return "Zero()"

    def eval(self) -> NamedOpetope.OCMT:
        return zero()
