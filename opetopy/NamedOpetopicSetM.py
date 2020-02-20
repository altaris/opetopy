# -*- coding: utf-8 -*-

"""
.. module:: NamedOpetopicSet
   :synopsis: Implementation of the mixed named approach
              for opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import Union

from opetopy.common import *
from opetopy import NamedOpetope
from opetopy import NamedOpetopicSet


def point(name: str) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{point}` rule.
    Introduces a :math:`0`-variable with name ``x``.
    """
    t = NamedOpetope.Typing(
        NamedOpetope.Term(NamedOpetope.Variable(name, 0)),
        NamedOpetope.Type([NamedOpetope.Term()]))
    return NamedOpetope.OCMT(
        NamedOpetope.EquationalTheory(),
        NamedOpetope.Context() + t)


def degen(ocmt: NamedOpetope.OCMT, name: str) -> NamedOpetope.Sequent:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{degen}` rule.
    Introduces the degenerate pasting diagram on a given variable.
    """
    var = ocmt.context[name]
    type = ocmt.context.typeOf(var)
    t = NamedOpetope.Typing(
        NamedOpetope.Term(var, True),
        NamedOpetope.Type([NamedOpetope.Term(var)] + type.terms))
    return NamedOpetope.Sequent(deepcopy(ocmt.theory),
                                deepcopy(ocmt.context), t)


def pd(ocmt: NamedOpetope.OCMT, name: str) -> NamedOpetope.Sequent:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{pd}` rule.
    Introduces the trivial non degenerate pasting diagram on a given variable.
    """
    var = ocmt.context[name]
    t = NamedOpetope.Typing(NamedOpetope.Term(var), ocmt.context.typeOf(var))
    return NamedOpetope.Sequent(deepcopy(ocmt.theory),
                                deepcopy(ocmt.context), t)


def graft(seqt: NamedOpetope.Sequent, seqx: NamedOpetope.Sequent,
          name: str) -> NamedOpetope.Sequent:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{graft}` rule, which is
    the same as system :math:`\\textbf{Opt${}^!$}`'s :math:`\\texttt{graft}`
    rule.
    """
    return NamedOpetope.graft(seqt, seqx, name)


def shift(seq: NamedOpetope.Sequent, name: str) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{shift}` rule.
    Takes a sequent ``seq`` typing a term ``t`` and introduces
    a new variable ``x`` having ``t`` as :math:`1`-source.
    """
    n = seq.typing.term.dimension
    var = NamedOpetope.Variable(name, n + 1)
    if var in seq.context:
        raise DerivationError(
            "shift rule",
            "NamedOpetope.Variable {var} already typed in context",
            var=name)
    typing = NamedOpetope.Typing(
        NamedOpetope.Term(var),
        NamedOpetope.Type([seq.typing.term] + seq.typing.type.terms))
    res = NamedOpetope.OCMT(deepcopy(seq.theory),
                            deepcopy(seq.context) + typing)
    # targets of new variable
    for i in range(1, n + 2):
        res.context += NamedOpetope.Typing(
            NamedOpetope.Term(res.target(var, i)),
            NamedOpetope.Type(typing.type.terms[i:]))
    # additional theory
    termVar = seq.typing.term.variable
    if termVar is None:
        raise RuntimeError(
            "[shift rule] Premiss sequent types an invalid term. In valid "
            "proof trees, this should not happen")
    if seq.typing.term.degenerate:
        for i in range(n):
            res.theory += (res.target(var, i + 2), res.target(termVar, i))
    elif n >= 1:
        seq.theory += (res.target(var, 2), res.target(termVar))
        for gt in seq.typing.term.graftTuples():
            seq.theory += (res.target(gt[1]), gt[0])
    return res


def zero() -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{zero}` rule, which is
    the same as system :math:`\\textbf{Opt${}^!$}`'s :math:`\\texttt{zero}`
    rule.
    """
    return NamedOpetopicSet.zero()


def sum(ocmt1: NamedOpetope.OCMT,
        ocmt2: NamedOpetope.OCMT) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{sum}` rule, which is
    the same as system :math:`\\textbf{OptSet${}^!$}`'s :math:`\\texttt{sum}`
    rule.
    """
    return NamedOpetopicSet.sum(ocmt1, ocmt2)


def glue(ocmt: NamedOpetope.OCMT, aName: str, bName: str) -> NamedOpetope.OCMT:
    """
    The :math:`\\textbf{OptSet${}^!_m$}` :math:`\\texttt{glue}` rule, which is
    the same as system :math:`\\textbf{OptSet${}^!$}`'s :math:`\\texttt{glue}`
    rule.
    """
    return NamedOpetopicSet.glue(ocmt, aName, bName)


class RuleInstance(AbstractRuleInstance):
    """
    A rule instance of system :math:`\\textbf{OptSet${}^!_m$}`.
    """

    def eval(self) -> Union[NamedOpetope.OCMT, NamedOpetope.Sequent]:
        """
        Pure virtual method evaluating a proof tree and returning the final
        conclusion sequent, or raising an exception if the proof is invalid.
        """
        raise NotImplementedError()


class Point(RuleInstance):
    """
    A class representing an instance of the ``point`` rule in a proof tree.
    """

    variableName: str

    def __init__(self, name: str) -> None:
        self.variableName = name

    def __repr__(self) -> str:
        return "Point({})".format(self.variableName)

    def __str__(self) -> str:
        return "Point({})".format(self.variableName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return "\\AxiomC{}\n\t\\RightLabel{\\texttt{point}}\n\t" + \
            "\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        """
        Evaluates the proof tree, in this cases returns the point sequent by
        calling :func:`opetopy.NamedOpetopicSetM.point`.
        """
        return point(self.variableName)


class Degen(RuleInstance):
    """
    A class representing an instance of the ``degen`` rule in a proof tree.
    """

    proofTree: RuleInstance
    variableName: str

    def __init__(self, p: RuleInstance, name: str) -> None:
        """
        Creates an instance of the ``degen`` rule and plugs proof tree ``p``
        on the unique premise.
        """
        self.proofTree = p
        self.variableName = name

    def __repr__(self) -> str:
        return "Degen({})".format(repr(self.proofTree))

    def __str__(self) -> str:
        return "Degen({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{degen}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.Sequent:
        """
        Evaluates this instance of ``degen`` by first evaluating its premiss,
        and then applying :func:`opetopy.NamedOpetopicSetM.degen` on the
        resulting sequent.
        """
        ocmt = self.proofTree.eval()
        if not isinstance(ocmt, NamedOpetope.OCMT):
            raise DerivationError(
                "degen rule",
                "Premiss expected to be an OCMT")
        else:
            return degen(ocmt, self.variableName)


class Pd(RuleInstance):
    """
    A class representing an instance of the ``pd`` rule in a proof tree.
    """

    proofTree: RuleInstance
    variableName: str

    def __init__(self, p: RuleInstance, name: str) -> None:
        """
        Creates an instance of the ``pd`` rule and plugs proof tree ``p``
        on the unique premise.
        """
        self.proofTree = p
        self.variableName = name

    def __repr__(self) -> str:
        return "Pd({})".format(repr(self.proofTree))

    def __str__(self) -> str:
        return "Pd({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{pd}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.Sequent:
        """
        Evaluates this instance of ``degen`` by first evaluating its premiss,
        and then applying :func:`opetopy.NamedOpetopicSetM.pd` on the
        resulting sequent.
        """
        ocmt = self.proofTree.eval()
        if not isinstance(ocmt, NamedOpetope.OCMT):
            raise DerivationError(
                "pd rule",
                "Premiss expected to be an OCMT")
        else:
            return pd(ocmt, self.variableName)


class Graft(RuleInstance):
    """
    A class representing an instance of the ``graft`` rule in a proof tree.
    """

    proofTree1: RuleInstance
    proofTree2: RuleInstance
    variableName: str

    def __init__(self, p1: RuleInstance,
                 p2: RuleInstance, a: str) -> None:
        """
        Creates an instance of the ``graft`` rule at variable ``a``, and plugs
        proof tree ``p1`` on the first premise, and ``p2`` on the second.

        :see: :func:`opetopy.NamedOpetopicSetM.graft`.
        """
        self.proofTree1 = p1
        self.proofTree2 = p2
        self.variableName = a

    def __repr__(self) -> str:
        return "Graft({p1}, {p2}, {a})".format(p1=repr(self.proofTree1),
                                               p2=repr(self.proofTree2),
                                               a=self.variableName)

    def __str__(self) -> str:
        return "Graft({p1}, {p2}, {a})".format(p1=str(self.proofTree1),
                                               p2=str(self.proofTree2),
                                               a=self.variableName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree1._toTex() + "\n\t" + self.proofTree2._toTex() + \
            "\n\t\\RightLabel{\\texttt{graft-}$" + \
            self.variableName + "$}\n\t\\BinaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.Sequent:
        """
        Evaluates this instance of ``graft`` by first evaluating its premises,
        and then applying :func:`opetopy.NamedOpetopicSetM.graft` at variable
        ``self.variableName`` on the resulting sequents.
        """
        seq1 = self.proofTree1.eval()
        seq2 = self.proofTree2.eval()
        if not isinstance(seq1, NamedOpetope.Sequent):
            raise DerivationError(
                "graft rule",
                "First premiss expected to be a sequent")
        elif not isinstance(seq2, NamedOpetope.Sequent):
            raise DerivationError(
                "graft rule",
                "Second premiss expected to be a sequent")
        else:
            return graft(seq1, seq2, self.variableName)


class Shift(RuleInstance):
    """
    A class representing an instance of the ``shift`` rule in a proof tree.
    """

    proofTree: RuleInstance
    variableName: str

    def __init__(self, p: RuleInstance, name: str) -> None:
        self.proofTree = p
        self.variableName = name

    def __repr__(self) -> str:
        return "Shift({}, {})".format(repr(self.proofTree), self.variableName)

    def __str__(self) -> str:
        return "Shift({}, {})".format(str(self.proofTree), self.variableName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{shift}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        seq = self.proofTree.eval()
        if not isinstance(seq, NamedOpetope.Sequent):
            raise DerivationError(
                "shift rule",
                "Premiss expected to be an sequent")
        else:
            return shift(seq, self.variableName)


class Zero(RuleInstance):
    """
    A class representing an instance of the ``zero`` rule in a proof tree.
    """

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
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
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree1._toTex() + "\n\t" + self.proofTree2._toTex() + \
            "\n\t\\RightLabel{\\texttt{sum}" + \
            "}\n\t\\BinaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        ocmt1 = self.proofTree1.eval()
        ocmt2 = self.proofTree2.eval()
        if not isinstance(ocmt1, NamedOpetope.OCMT):
            raise DerivationError(
                "sum rule",
                "First premiss expected to be an OCMT")
        elif not isinstance(ocmt2, NamedOpetope.OCMT):
            raise DerivationError(
                "sum rule",
                "Second premiss expected to be an OCMT")
        else:
            return sum(ocmt1, ocmt2)


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
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{glue-}$(" + self.aName + \
            " = " + self.bName + ")$}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> NamedOpetope.OCMT:
        """
        Evaluates this instance of ``graft`` by first evaluating its premises,
        and then applying :func:`opetopy.NamedOpetopicSetM.graft` at variable
        `self.a` on the resulting sequents.
        """
        ocmt = self.proofTree.eval()
        if not isinstance(ocmt, NamedOpetope.OCMT):
            raise DerivationError(
                "pd rule",
                "Premiss expected to be an OCMT")
        else:
            return glue(ocmt, self.aName, self.bName)


class DegenFill(RuleInstance):
    """
    A convenient class chaining an instance of the ``degen`` rule with an
    instance of the ``shift`` rule.
    """

    proofTree: RuleInstance

    def __init__(self, p: RuleInstance, dname: str, fname: str) -> None:
        self.proofTree = Shift(Degen(p, dname), fname)

    def __repr__(self) -> str:
        return repr(self.proofTree)

    def __str__(self) -> str:
        return str(self.proofTree)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetopicSetM.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex()

    def eval(self) -> NamedOpetope.OCMT:
        return self.proofTree.eval()
