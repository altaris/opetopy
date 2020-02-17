# -*- coding: utf-8 -*-

"""
.. module:: UnnamedOpetopicSet
   :synopsis: Implementation of the unnamed approach for opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from operator import attrgetter
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from opetopy.common import *
from opetopy import UnnamedOpetope


class Variable:
    """
    A variable is just a string representing its name, annotated by an opetope
    (:class:`opetopy.UnnamedOpetope.Preopetope`) representing its shape. To construct
    a variable, however, not only does the shape need to be specified, but its
    whole proof tree.
    """

    name: str
    shapeProof: UnnamedOpetope.RuleInstance
    shapeSequent: UnnamedOpetope.Sequent  # For optimization purposes

    def __eq__(self, other) -> bool:
        """
        Tests syntactic equality between two variables. Two variables are equal
        if they have the same name and the same shape.
        """
        if not isinstance(other, Variable):
            raise NotImplementedError
        return self.name == other.name

    def __init__(self, name: str,
                 shapeProof: UnnamedOpetope.RuleInstance) -> None:
        self.name = name
        self.shapeProof = shapeProof
        self.shapeSequent = shapeProof.eval()

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return "{name} : {shape}".format(name=self.name,
                                         shape=repr(self.shape))

    def __str__(self) -> str:
        return self.name

    @property
    def dimension(self) -> int:
        """
        Convenience function that returns the dimension of a variable.
        """
        return self.shape.dimension

    @property
    def shape(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the actual shape (:class:`opetopy.UnnamedOpetope.Preopetope`) of the
        variable, from the proof tree
        (:class:`opetopy.UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.source

    def shapeTarget(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the shape target (:class:`opetopy.UnnamedOpetope.Preopetope`) of the
        variable, from the proof tree
        (:class:`opetopy.UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.target

    def toTex(self) -> str:
        """
        Returns the string representation of the variable, which is really just
        the variable name.
        """
        return self.name


class PastingDiagram:
    """
    A pasting diagram consist in a shape :math:`\\omega`
    (:class:`opetopy.UnnamedOpetope.Preopetope`) and

    * if :math:`\\omega` is not degenerate, a mapping
      :math:`f : \\omega^\\bullet \\longrightarrow \\mathbb{V}` such that
      :math:`f (\\mathsf{s}_{[p]} \\omega)^\\natural = f([p])^\\natural`, where
      :math:`\\mathbb{V}` is the set of variable
      (:class:`opetopy.UnnamedOpetopicSet.Variable`); this case is implemented in
      :class:`opetopy.UnnamedOpetopicSet.NonDegeneratePastingDiagram`;
    * if :math:`\\omega` is degenerate, say :math:`\\omega = \\{\\{\\phi`, a
      variable of shape :math:`\\phi`; this case is implemented in
      :class:`opetopy.UnnamedOpetopicSet.DegeneratePastingDiagram`.
    """

    degeneracy: Optional[str]
    nodes: Optional[Dict[UnnamedOpetope.Address, str]]
    shapeSequent: UnnamedOpetope.Sequent  # For optimization purposes
    shapeProof: UnnamedOpetope.RuleInstance

    def __eq__(self, other) -> bool:
        if not isinstance(other, PastingDiagram):
            raise NotImplementedError
        else:
            return self.shape == other.shape and \
                self.degeneracy == other.degeneracy and \
                self.nodes == other.nodes

    def __getitem__(self, addr: UnnamedOpetope.Address) -> str:
        """
        Returns the source variable at ``addr`` of a non degenerate pasting
        diagram.
        """
        if self.nodes is None:
            raise DerivationError(
                "Pasting diagram, source",
                "Cannot compute a source of a degenerate pasting diagram")
        elif addr not in self.nodes.keys():
            raise DerivationError(
                "Pasting diagram, source",
                "Address {addr} is not an address of the pasting diagram {pd}",
                addr=repr(addr), pd=repr(self))
        else:
            return self.nodes[addr]

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.degeneracy is None:
            if self.nodes is None:
                raise RuntimeError("[Pasting diagram, to string] Both the "
                                   "degeneracy and node dict of the pasting "
                                   "diagram are None. In valid derivations, "
                                   "this should not happen")
            if self.shape == UnnamedOpetope.point().source:
                return "⧫"
            else:
                lines = [str(addr) + " ← " + str(self.nodes[addr])
                         for addr in self.nodes.keys()]
                return "{" + ", ".join(lines) + "}"
        else:
            return "{{" + str(self.degeneracy) + "}}"

    def degeneracyVariable(self) -> str:
        """
        Returns the degeneracy variable, or raises an exception if the pasting
        diagram is not degenerate.
        """
        if self.degeneracy is None:
            raise DerivationError(
                "Degenerate pasting diagram, get degeneracy",
                "Pasting diagram is not degenerate")
        else:
            return self.degeneracy

    @staticmethod
    def degeneratePastingDiagram(
            shapeProof: UnnamedOpetope.RuleInstance,
            degeneracy: str) -> 'PastingDiagram':
        """
        Creates a degenerate pasting diagram.
        """
        res = PastingDiagram()
        res.nodes = None
        res.shapeProof = shapeProof
        res.shapeSequent = shapeProof.eval()
        if not res.shape.isDegenerate:
            raise DerivationError(
                "Degenerate pasting diagram, creation",
                "Provided shape is not degenerate")
        elif res.shape.degeneracy is None:
            raise RuntimeError("[Degenerate pasting diagram, creation] "
                               "Provided shape is degenerate but does not "
                               "have any degeneracy. In valid proof trees, "
                               "this should not happen")
        res.degeneracy = degeneracy
        return res

    @staticmethod
    def point():
        """
        Creates the trivial pasting diagram with shape the point
        """
        return PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.Point(), {})

    @staticmethod
    def nonDegeneratePastingDiagram(
            shapeProof: UnnamedOpetope.RuleInstance,
            nodes: Dict[UnnamedOpetope.Address, str]) -> 'PastingDiagram':
        """
        Creates a non degenerate pasting diagram.
        """
        res = PastingDiagram()
        res.degeneracy = None
        res.shapeProof = shapeProof
        res.shapeSequent = shapeProof.eval()
        if res.shape.isDegenerate:
            raise DerivationError(
                "Non degenerate pasting diagram, creation",
                "Provided shape is degenerate")
        elif set(res.shape.nodes.keys()) != set(nodes.keys()):
            raise DerivationError(
                "Non degenerate pasting diagram, creation",
                "Node mapping domain doesn't match with the set of addresses "
                "of the shape")
        res.nodes = nodes
        return res

    @property
    def shape(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the actual shape (:class:`opetopy.UnnamedOpetope.Preopetope`) of the
        pasting diagram, from the proof tree
        (:class:`opetopy.UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.source

    def shapeTarget(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the shape target (:class:`opetopy.UnnamedOpetope.Preopetope`) of the
        pasting diagram, from the proof tree
        (:class:`opetopy.UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.target

    def source(self, addr: UnnamedOpetope.Address) -> str:
        """
        Returns the variable name at address ``addr``, or raises an exception
        if the pasting diagram is degenerate
        """
        if self.nodes is None:
            raise DerivationError(
                "Non degenerate pasting diagram, get source",
                "Pasting diagram is degenerate")
        elif addr not in self.nodes.keys():
            raise DerivationError(
                "Non degenerate pasting diagram, get source",
                "Address {addr} not in pasting diagram {pd}",
                addr=addr, pd=self)
        else:
            return self.nodes[addr]

    def toTex(self) -> str:
        if self.degeneracy is None:
            if self.nodes is None:
                raise RuntimeError("[Pasting diagram, to TeX] Both the "
                                   "degeneracy and node dict of the pasting "
                                   "diagram are None. In valid derivations, "
                                   "this should not happen")
            if self.shape == UnnamedOpetope.point().source:
                return "\\optZero"
            else:
                lines = [addr.toTex() + " \\sep " + self.nodes[addr]
                         for addr in self.nodes.keys()]
                return "\\opetope{" + " \\\\ ".join(lines) + "}"
        else:
            return "\\degenopetope{" + self.degeneracy + "}"


class Type:
    """
    A type consist in

    * a source pasting diagram (:class:`opetopy.UnnamedOpetopicSet.PastingDiagram`),
      say :math:`\\mathbf{P}`,
    * a target variable (:class:`opetopy.UnnamedOpetopicSet.Variable`), say :math:`x`,

    such that :math:`\\mathsf{t} \\mathbf{P}^\\natural = x^\\natural`
    """

    source: PastingDiagram
    target: Optional[Variable]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Type):
            raise NotImplementedError
        else:
            return self.source == other.source and self.target == other.target

    def __init__(self, source: PastingDiagram,
                 target: Optional[Variable]) -> None:
        if target is None:
            if source.shape != UnnamedOpetope.Point().eval().source:
                raise DerivationError(
                    "Type, creation",
                    "Source pasting diagram is not a point, but target is "
                    "unspecified")
        elif source.shapeTarget() != target.shape:
            raise DerivationError(
                "Type, creation",
                "Target variable {var} has shape {shape}, should have "
                "{should}",
                var=str(target), shape=target.shape,
                should=source.shapeTarget())
        self.source = source
        self.target = target

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        if self.target is None:
            return repr(self.source)
        else:
            return "{src} → {tgt}".format(
                src=repr(self.source), tgt=repr(self.target))

    def __str__(self) -> str:
        if self.target is None:
            return str(self.source)
        else:
            return "{src} → {tgt}".format(
                src=str(self.source), tgt=str(self.target))

    def toTex(self) -> str:
        if self.target is None:
            return self.source.toTex()
        else:
            return "{src} \\longrightarrow {tgt}".format(
                src=self.source.toTex(), tgt=self.target.toTex())


class Typing:
    """
    A typing consists in

    * a variable :class:`opetopy.UnnamedOpetopicSet.Variable`, say :math:`v`,
    * a type :class:`opetopy.UnnamedOpetopicSet.Type`, say
      :math:`\\mathbf{P} \\longrightarrow t`

    such that :math:`x^\\natural = \\mathbf{P}^\\natural`.
    """

    type: Type
    variable: Variable

    def __init__(self, variable: Variable, type: Type) -> None:
        if variable.shape != type.source.shape:
            raise DerivationError(
                "Typing, creation",
                "Variable {var} cannot have type {type} as shapes do not "
                "match",
                var=str(variable), type=type)
        self.type = type
        self.variable = variable

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.variable) + " : " + str(self.type)

    def toTex(self) -> str:
        return "{var} : {type}".format(
            var=self.variable.toTex(), type=self.type.toTex())


class Context(Set[Typing]):
    """
    A context is a set of tyings (see :class:`opetopy.UnnamedOpetopicSet.Typing`).
    """

    def __add__(self, typing: Typing) -> 'Context':
        """
        Adds a variable typing to a deep copy of the context context, if the
        typed variable isn't already typed in the context.
        """
        if typing.variable in self:
            raise DerivationError(
                "Context, new typing",
                "Variable {var} is already typed in this context",
                var=str(typing.variable))
        else:
            res = deepcopy(self)
            res.add(typing)
            return res

    def __contains__(self, var) -> bool:
        """
        Tests wether the variable ``var`` is typed in this context.
        """
        if not isinstance(var, Variable):
            raise NotImplementedError
        for typing in self:
            if var == typing.variable:
                return True
        return False

    def __getitem__(self, name: str) -> Typing:
        """
        Returns typing whose variable name is ``name``.
        """
        for t in self:
            if t.variable.name == name:
                return t
        raise DerivationError(
            "Context, get typing",
            "Variable {name} not typed in context",
            name=name)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ", ".join([str(self[v]) for v in self.variableNames()])

    def source(self, name: str, addr: UnnamedOpetope.Address) -> str:
        """
        Returns the source at address ``addr`` of the variable whose name is
        ``name``.
        """
        return self[name].type.source[addr]

    def target(self, name: str) -> str:
        """
        Returns the target of the variable whose name is ``name``.
        """
        res = self[name].type.target
        if self[name].type.source.shape == \
                UnnamedOpetope.Point().eval().source:
            raise DerivationError(
                "Context, target of variable",
                "Variable {var} is a point, and do not have a target",
                var=name)
        elif res is None:
            raise RuntimeError("[Context, target of variable] Variable {var} "
                               "is not a point, but has no target. In valid "
                               "derivations, this should not happen".format(
                                   var=name))
        return res.name

    def toTex(self) -> str:
        return ", ".join([t.toTex() for t in self])

    def variableNames(self) -> List[str]:
        """
        Return a list containing all variable names typed in this context.
        """
        variables = []  # type: List[str]
        for t in sorted(self,
                key=attrgetter('variable.dimension', 'variable.name')):
            variables.append(t.variable.name)
        return variables


class Sequent:
    """
    A sequent is composed of

    * a context (:class:`opetopy.UnnamedOpetopicSet.Context`);
    * optionally, a pasting diagram
      (:class:`opetopy.UnnamedOpetopicSet`.PastingDiagram).
    """

    context: Context
    pastingDiagram: Optional[PastingDiagram]

    def __getitem__(self, name: str) -> Variable:
        """
        Returns the variable in the sequent's context whose name is ``name``.
        Note that unlike :func:`opetopy.UnnamedOpetopicSet.Context.__getitem__`, this
        function returns a :class:`opetopy.UnnamedOpetopicSet.Variable` (and not a
        :class:`opetopy.UnnamedOpetopicSet.Typing`)
        """
        return self.context[name].variable

    def __init__(self) -> None:
        """
        Creates a sequent with an empty context, and no pasting diagram.
        """
        self.context = Context()
        self.pastingDiagram = None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        pd = ""
        if self.pastingDiagram is not None:
            pd = str(self.pastingDiagram)
        res = "ctx ="
        for v in self.context.variableNames():
            res += "\n    " + str(self.context[v])
        res += "\npd =\n    " + pd
        return res

    def toTex(self) -> str:
        pd = ""
        if self.pastingDiagram is not None:
            pd = self.pastingDiagram.toTex()
        return "{ctx} \\vdash {pd}".format(
            ctx=self.context.toTex(), pd=pd)


def point(seq: Sequent, name: Union[str, List[str]]) -> Sequent:
    """
    The :math:`\\textbf{OptSet${}^?$}` :math:`\\texttt{point}` rule.

    * If argument ``name`` is a ``str``, creates a new point with that name
      (this is just the :math:`\\texttt{point}`);
    * if it is a list of ``str``, then creates as many points.

    """
    if isinstance(name, list):
        res = seq
        for n in name:
            res = point(res, n)
        return res
    elif isinstance(name, str):
        if seq.pastingDiagram is not None:
            raise DerivationError(
                "point rule",
                "Sequent cannot have a pasting diagram")
        var = Variable(name, UnnamedOpetope.Point())
        if var in seq.context:
            raise DerivationError(
                "point rule",
                "Point shaped variable {name} is already typed in context "
                "{ctx}",
                name=name, ctx=str(seq.context))
        res = deepcopy(seq)
        res.context = res.context + Typing(
            var, Type(PastingDiagram.point(), None))
        return res
    else:
        raise DerivationError(
            "point rule",
            "Argument name is expected to be a str or list of str")


def degen(seq: Sequent, name: str) -> Sequent:
    """
    The :math:`\\textbf{OptSet${}^?$}` :math:`\\texttt{degen}` rule.
    """
    if seq.pastingDiagram is not None:
        raise DerivationError(
            "degen rule",
            "Sequent cannot have a pasting diagram")
    res = deepcopy(seq)
    res.pastingDiagram = PastingDiagram.degeneratePastingDiagram(
        UnnamedOpetope.Degen(seq.context[name].variable.shapeProof), name)
    return res


def graft(seq: Sequent, pd: PastingDiagram) -> Sequent:
    """
    The :math:`\\textbf{OptSet${}^?$}` :math:`\\texttt{graft}` rule.
    """
    if pd.nodes is None:
        raise DerivationError(
            "graft rule",
            "Parameter pasting diagram cannot be degenerate")
    # Shape checking
    omega = pd.shape
    for addr in pd.nodes.keys():
        psi = seq[pd.nodes[addr]].shape
        if psi != omega.source(addr):
            raise DerivationError(
                "graft rule",
                "Variable {var} has incompatible shape {psi}, should have "
                "{should}",
                var=seq[pd.nodes[addr]].name, psi=repr(psi),
                should=repr(omega.source(addr)))
    # [Inner] axiom
    for pj in pd.nodes.keys():
        if not pj.isEpsilon():
            pi, q = pj.edgeDecomposition()
            xi = pd.nodes[pi]
            xj = pd.nodes[pj]
            if seq.context.target(xj) != seq.context.source(xi, q):
                raise DerivationError(
                    "graft rule",
                    "Parameter pasting diagram doesn't satisfy axiom [Inner]: "
                    "variables {xi} and {xj} don't agree on the decoration of "
                    "edge {edge}",
                    xi=repr(xi), xj=repr(xj), edge=repr(pj))
    res = deepcopy(seq)
    res.pastingDiagram = deepcopy(pd)
    return res


def shift(seq: Sequent, targetName: str, name: str) -> Sequent:
    """
    The :math:`\\textbf{OptSet${}^?$}` :math:`\\texttt{shift}` rule.
    """
    if seq.pastingDiagram is None:
        raise DerivationError(
            "shift rule",
            "Sequent must have a pasting diagram")
    P = seq.pastingDiagram
    omega = P.shape
    readdress = P.shapeProof.eval().context
    n = omega.dimension
    x = seq.context[targetName].variable
    a = seq.context[targetName].type.target
    Q = seq.context[targetName].type.source
    if x.shape != P.shapeTarget():
        raise DerivationError(
            "shift rule",
            "Target variable {var} has shape {shape} should have {should}",
            var=repr(x), shape=repr(x.shape),
            should=repr(P.shapeTarget()))
    if omega.isDegenerate:
        if a is None:  # x is a point
            raise RuntimeError("[shift rule] Variable {x} has a degenerate "
                               "shape but no target. In valid derivations, "
                               "this should not happen")
        # [Degen] axiom
        if Q.nodes != {UnnamedOpetope.Address.epsilon(n - 2): a.name}:
            raise DerivationError(
                "shift rule",
                "Target variable {var}'s source is expected to be globular at "
                "{var}'s target",
                var=repr(x))
    else:
        # [Glob1] axiom
        r = P[UnnamedOpetope.Address.epsilon(n - 1)]
        if a is None:  # x is a point
            if seq.context[r].type.target is not None:  # r must be a point
                raise DerivationError(
                    "shift rule",
                    "Axiom [Glob1] is not satisfied: variable {x} is a point, "
                    "should have target {should}",
                    x=repr(x), should=repr(seq.context[r].type.target))
        else:
            b = seq.context.target(r)
            if b != a.name:
                raise DerivationError(
                    "shift rule",
                    "Axiom [Glob1] is not satisfied: variable {x} has target "
                    "{a}, should have {should}",
                    x=repr(x), a=a.name, should=repr(b))
        # [Glob2] axiom
        for l in omega.leafAddresses():
            p, q = l.edgeDecomposition()
            sP = seq.context.source(P[p], q)
            sx = seq.context.source(x.name, readdress(l))
            if sP != sx:
                raise DerivationError(
                    "shift rule",
                    "Axiom [Glob2] is not satisfied: variable {x} has {addr} "
                    "source {sx}, should have {should}",
                    x=repr(x), addr=repr(readdress(l)),
                    sx=repr(sx), should=repr(sP))
    res = Sequent()
    res.context = seq.context + Typing(
        Variable(name, seq.pastingDiagram.shapeProof),
        Type(deepcopy(seq.pastingDiagram), x))
    return res


class RuleInstance(AbstractRuleInstance):
    """
    A rule instance of system :math:`\\textbf{OptSet${}^?$}`.
    """

    def eval(self) -> Sequent:
        """
        Pure virtual method evaluating a proof tree and returning the final
        conclusion sequent, or raising an exception if the proof is invalid.
        """
        raise NotImplementedError()


class Point(RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{point}` rule in a
    proof tree.
    """

    name: Union[str, List[str]]
    proofTree: Optional[RuleInstance]

    def __init__(self, p: Optional[RuleInstance],
                 name: Union[str, List[str]]) -> None:
        self.name = name
        self.proofTree = p

    def __repr__(self) -> str:
        if self.proofTree is None:
            prepr = ""
        else:
            prepr = repr(self.proofTree)
        return "Point(" + prepr + "," + str(self.name) + ")"

    def __str__(self) -> str:
        if self.proofTree is None:
            pstr = ""
        else:
            pstr = str(self.proofTree)
        return "Point(" + pstr + ", " + str(self.name) + ")"

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        if self.proofTree is None:
            ptex = "\\AxiomC{}"
        else:
            ptex = self.proofTree._toTex()
        if isinstance(self.name, str):
            namestr = self.name
        else:
            namestr = "(" + ", ".join(self.name) + ")"
        return ptex + "\n\t\\RightLabel{\\texttt{point-$" + namestr + \
            "$}}\n\t\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree.
        """
        if self.proofTree is None:
            return point(Sequent(), self.name)
        else:
            return point(self.proofTree.eval(), self.name)


class Degen(RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{degen}` rule in a
    proof tree.
    """

    name: str
    proofTree: RuleInstance

    def __init__(self, p: RuleInstance, name: str) -> None:
        self.name = name
        self.proofTree = p

    def __repr__(self) -> str:
        return "Degen(" + repr(self.proofTree) + "," + self.name + ")"

    def __str__(self) -> str:
        return "Degen(" + str(self.proofTree) + ", " + self.name + ")"

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{degen}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree.
        """
        return degen(self.proofTree.eval(), self.name)


class Graft(RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{graft}` rule in a
    proof tree.
    """

    pastingDiagram: PastingDiagram
    proofTree: RuleInstance

    def __init__(self, p: RuleInstance, pd: PastingDiagram) -> None:
        self.pastingDiagram = pd
        self.proofTree = p

    def __repr__(self) -> str:
        return "Graft({})".format(repr(self.proofTree))

    def __str__(self) -> str:
        return "Graft({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{graft}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree.
        """
        return graft(self.proofTree.eval(), self.pastingDiagram)


class Shift(RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{shift}` rule in a
    proof tree.
    """

    name: str
    proofTree: RuleInstance
    targetName: str

    def __init__(self, p: RuleInstance, targetName: str, name: str) -> None:
        self.name = name
        self.proofTree = p
        self.targetName = targetName

    def __repr__(self) -> str:
        return "Shift(" + repr(self.proofTree) + "," + self.name + ")"

    def __str__(self) -> str:
        return "Shift(" + str(self.proofTree) + ", " + self.name + ")"

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{shift}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree.
        """
        return shift(self.proofTree.eval(), self.targetName, self.name)


def pastingDiagram(shapeProof: UnnamedOpetope.RuleInstance,
                   args: Union[Dict[UnnamedOpetope.Address, str], str]) \
        -> PastingDiagram:
    """
    Convenient function that regroups
    :meth:`UnnamedOpetopicSet.PastingDiagram.degeneratePastingDiagram` and
    :meth:`UnnamedOpetopicSet.PastingDiagram.nonDegeneratePastingDiagram`.
    It calls either depending on the shape opetope.
    """
    shape = shapeProof.eval().source
    if shape.isDegenerate:
        if isinstance(args, str):
            return PastingDiagram.degeneratePastingDiagram(
                shapeProof, args)
        else:
            raise DerivationError(
                "Pasting diagram creation",
                "Second argument is expected to be a variable name, since "
                "shape is degenerate")
    else:
        if isinstance(args, dict):
            return PastingDiagram.nonDegeneratePastingDiagram(
                shapeProof, args)
        else:
            raise DerivationError(
                "Pasting diagram creation",
                "Second argument is expected to be a address-to-variable-name "
                "mapping, since shape is non degenerate")
