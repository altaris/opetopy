# -*- coding: utf-8 -*-

"""
.. module:: opetopy.UnnamedOpetopicSet
   :synopsis: Implementation of the unnamed approach for opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

import UnnamedOpetope


class Variable:
    """
    A variable is just a string representing its name, annotated by an opetope
    (:class:`UnnamedOpetope.Preopetope`) representing its shape. To construct
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
        return self.name == other.name and self.shape == other.shape

    def __init__(self, name: str,
                 shapeProof: UnnamedOpetope.RuleInstance) -> None:
        self.name = name
        self.shapeProof = shapeProof
        self.shapeSequent = shapeProof.eval()

    def __ne__(self, other) -> bool:
        if not isinstance(other, Variable):
            raise NotImplementedError
        return not (self == other)

    def __repr__(self) -> str:
        return "{name} : {shape}".format(name = self.name,
                                         shape = repr(self.shape))

    def __str__(self) -> str:
        return self.name

    @property
    def shape(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the actual shape (:class:`UnnamedOpetope.Preopetope`) of the
        variable, from the proof tree
        (:class:`UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.source

    def shapeTarget(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the shape target (:class:`UnnamedOpetope.Preopetope`) of the
        variable, from the proof tree
        (:class:`UnnamedOpetope.RuleInstance`) that was provided
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
    A pasting diagram consist in a shape :math:`\omega`
    (:class:`UnnamedOpetope.Preopetope`) and

    * if :math:`\omega` is not degenerate, a mapping
      :math:`f : \omega^\\bullet \longrightarrow \mathbb{V}` such that
      :math:`f (\mathsf{s}_{[p]} \omega)^\\natural = f([p])^\\natural`, where
      :math:`\mathbb{V}` is the set of variable
      (:class:`UnnamedOpetopicSet.Variable`); this case is implemented in
      :class:`UnnamedOpetopicSet.NonDegeneratePastingDiagram`;
    * if :math:`\omega` is degenerate, say :math:`\omega = \{\{\phi`, a
      variable of shape :math:`\phi`; this case is implemented in
      :class:`UnnamedOpetopicSet.DegeneratePastingDiagram`.
    """

    degeneracy: Optional[Variable]
    nodes: Optional[Dict[UnnamedOpetope.Address, Variable]]
    shapeSequent: UnnamedOpetope.Sequent  # For optimization purposes
    shapeProof: UnnamedOpetope.RuleInstance

    def __getitem__(self, addr: UnnamedOpetope.Address) -> Variable:
        """
        Returns the source variable at `addr` of a non degenerate pasting
        diagram.
        """
        if self.nodes is None:
            raise ValueError("[Pasting diagram, source] Cannot compute a "
                             "source of a degenerate pasting diagram")
        elif addr not in self.nodes.keys():
            raise ValueError("[Pasting diagram, source] Address {addr} is "
                             "not an address of the pasting diagram {pd}"
                             .format(addr = repr(addr), pd = repr(self)))
        else:
            return self.nodes[addr]

    @staticmethod
    def degeneratePastingDiagram(
            shapeProof: UnnamedOpetope.RuleInstance,
            degeneracy: Variable) -> 'PastingDiagram':
        """
        Creates a degenerate pasting diagram.
        """
        res = PastingDiagram()
        res.nodes = None
        res.shapeProof = shapeProof
        res.shapeSequent = shapeProof.eval()
        if not res.shape.isDegenerate:
            raise ValueError("[Degenerate pasting diagram, creation] Provided "
                             "shape is not degenerate")
        elif res.shape.degeneracy is None:
            raise ValueError("[Degenerate pasting diagram, creation] Provided "
                             "shape is degenerate but does not have any "
                             "degeneracy. In valid proof trees, this should "
                             "not happen")
        elif res.shape.degeneracy != degeneracy.shape:
            raise ValueError("[Degenerate pasting diagram, creation] Provided "
                             "degeneracy variable {var} has shape {shape}, "
                             "should have {should}".format(
                                 var = str(degeneracy),
                                 shape = degeneracy.shape,
                                 should = res.shape.degeneracy))
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
            nodes: Dict[UnnamedOpetope.Address, Variable]) -> 'PastingDiagram':
        """
        Creates a non degenerate pasting diagram.
        """
        res = PastingDiagram()
        res.degeneracy = None
        res.shapeProof = shapeProof
        res.shapeSequent = shapeProof.eval()
        if res.shape.isDegenerate:
            raise ValueError("[Non degenerate pasting diagram, creation] "
                             "Provided shape is degenerate")
        elif set(res.shape.nodes.keys()) != set(nodes.keys()):
            raise ValueError("[Non degenerate pasting diagram, creation] "
                             "Node mapping domain doesn't match with the "
                             "set of addresses of the shape")
        for a in nodes.keys():
            if nodes[a].shape != res.shape.source(a):
                raise ValueError("[Non degenerate pasting diagram, creation] "
                                 "Variable {var} at address {addr} has shape "
                                 "{shape}, should have {should}".format(
                                     var = str(nodes[a]),
                                     addr = a,
                                     shape = nodes[a].shape,
                                     should = res.shape.source(a)))
        res.nodes = nodes
        return res

    @property
    def shape(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the actual shape (:class:`UnnamedOpetope.Preopetope`) of the
        pasting diagram, from the proof tree
        (:class:`UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.source

    def shapeTarget(self) -> UnnamedOpetope.Preopetope:
        """
        Returns the shape target (:class:`UnnamedOpetope.Preopetope`) of the
        pasting diagram, from the proof tree
        (:class:`UnnamedOpetope.RuleInstance`) that was provided
        at its creation.
        """
        return self.shapeSequent.target

    def __repr__(self) -> str:
        if self.degeneracy is None:
            if self.nodes is None:
                raise RuntimeError("[Pasting diagram, repr] Both the "
                                   "degeneracy and node dict of the pasting "
                                   "diagram are None. In valid derivations, "
                                   "this should not happen")
            if self.shape == UnnamedOpetope.point().source:
                return "⧫"
            else:
                lines = [repr(addr) + " ← " + self.nodes[addr].name
                         for addr in self.nodes.keys()]
                return "PD({})".format(", ".join(lines))
        else:
            return "DPD({})".format(self.degeneracy.name)

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
                return "PastingDiagram({})".format(", ".join(lines))
        else:
            return "DegeneratePastingDiagram({})".format(str(self.degeneracy))

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
                lines = [addr.toTex() + " \\sep " + self.nodes[addr].toTex()
                         for addr in self.nodes.keys()]
                return "\\opetope{" + " \\\\ ".join(lines) + "}"
        else:
            return "\\degenopetope{" + self.degeneracy.toTex() + "}"


class Type:
    """
    A type consist in

    * a source pasting diagram (:class:`UnnamedOpetopicSet.PastingDiagram`),
      say :math:`\mathbf{P}`,
    * a target variable (:class:`UnnamedOpetopicSet.Variable`), say :math:`x`,

    such that :math:`\mathsf{t} \mathbf{P}^\\natural = x^\\natural`
    """

    source: PastingDiagram
    target: Optional[Variable]

    def __init__(self, source: PastingDiagram,
                 target: Optional[Variable]) -> None:
        if target is None:
            if source.shape != UnnamedOpetope.Point().eval().source:
                raise ValueError("[Type, creation] Source pasting diagram is "
                                 "not a point, but target is unspecified")
        elif source.shapeTarget() != target.shape:
            raise ValueError("[Type, creation] Target variable {var} has "
                             "shape {shape}, should have {should}".format(
                                 var = str(target),
                                 shape = target.shape,
                                 should = source.shapeTarget()))
        self.source = source
        self.target = target

    def __repr__(self) -> str:
        if self.target is None:
            return repr(self.source)
        else:
            return "{src} → {tgt}".format(
                src = repr(self.source), tgt = repr(self.target))

    def __str__(self) -> str:
        if self.target is None:
            return str(self.source)
        else:
            return "{src} → {tgt}".format(
                src = str(self.source), tgt = str(self.target))

    def toTex(self) -> str:
        if self.target is None:
            return self.source.toTex()
        else:
            return "{src} \\longrightarrow {tgt}".format(
                src = self.source.toTex(), tgt = self.target.toTex())


class Typing:
    """
    A typing consists in

    * a variable :class:`UnnamedOpetopicSet.Variable`, say :math:`v`,
    * a type :class:`UnnamedOpetopicSet.Type`, say
      :math:`\mathbf{P} \longrightarrow t`

    such that :math:`x^\\natural = \mathbf{P}^\\natural`.
    """

    type: Type
    variable: Variable

    def __init__(self, variable: Variable, type: Type) -> None:
        if variable.shape != type.source.shape:
            raise ValueError("[Typing, creation] Variable {var} cannot have "
                             "type {type} as shapes do not match".format(
                                 var = str(variable),
                                 type = type))
        self.type = type
        self.variable = variable

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.variable) + " : " + str(self.type)

    def toTex(self) -> str:
        return "{var} : {type}".format(
            var = self.variable.toTex(), type = self.type.toTex())


class Context(Set[Typing]):
    """
    A context is a set of tyings (see :class:`UnnamedOpetopicSet.Typing`).
    """

    def __add__(self, typing: Typing) -> 'Context':
        """
        Adds a variable typing to a deep copy of the context context, if the
        typed variable isn't already typed in the context.
        """
        if typing.variable in self:
            raise ValueError("[Context, new typing] Variable {var} is already "
                             "typed in this context".format(
                                 var = str(typing.variable)))
        else:
            res = deepcopy(self)
            res.add(typing)
            return res

    def __contains__(self, var) -> bool:
        """
        Tests wether the variable `var` is typed in this context.
        """
        if not isinstance(var, Variable):
            raise NotImplementedError
        for typing in self:
            if var == typing.variable:
                return True
        return False

    def __getitem__(self, name: str) -> Typing:
        """
        Returns typing whose variable name is `name`.
        """
        for t in self:
            if t.variable.name == name:
                return t
        raise ValueError("[Context, get typing] Variable {name} not typed in "
                         "context".format(name = name))

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ", ".join([str(t) for t in self])

    def source(self, name: str, addr: UnnamedOpetope.Address) -> Variable:
        """
        Returns the source at address `addr` of the variable whose name is
        `name`.
        """
        return self[name].type.source[addr]

    def target(self, name: str) -> Variable:
        """
        Returns the target of the variable whose name is `name`.
        """
        res = self[name].type.target
        if self[name].type.source.shape == \
                UnnamedOpetope.Point().eval().source:
            raise ValueError("[Context, target of variable] Variable {var} is "
                             "a point, and do not have a target".format(
                                 var = name))
        elif res is None:
            raise RuntimeError("[Context, target of variable] Variable {var} "
                               "is not a point, but has no target. In valid "
                               "derivations, this should not happen".format(
                                   var = name))
        return res

    def toTex(self) -> str:
        return ", ".join([t.toTex() for t in self])


class Sequent:
    """
    A sequent is composed of

    * a context (:class:`UnnamedOpetopicSet.Context`);
    * optionally, a pasting diagram
      (:class:`UnnamedOpetopicSet`.PastingDiagram).
    """

    context: Context
    pastingDiagram: Optional[PastingDiagram]

    def __init__(self) -> None:
        """
        Creates a sequent with an empty context, and no pasting diagram.
        """
        self.context = Context()
        self.pastingDiagram = None

    def __repr__(self) -> str:
        pd = ""
        if self.pastingDiagram is not None:
            pd = repr(self.pastingDiagram)
        return "{ctx} ⊢ {pd}".format(ctx = repr(self.context), pd = pd)

    def __str__(self) -> str:
        pd = ""
        if self.pastingDiagram is not None:
            pd = str(self.pastingDiagram)
        return "{ctx} ⊢ {pd}".format(ctx = str(self.context), pd = pd)

    def toTex(self) -> str:
        pd = ""
        if self.pastingDiagram is not None:
            pd = self.pastingDiagram.toTex()
        return "{ctx} \\vdash {pd}".format(
            ctx = self.context.toTex(), pd = pd)


def point(seq: Sequent, name: str) -> Sequent:
    if seq.pastingDiagram is not None:
        raise ValueError("[point rule] Sequent cannot have a pasting diagram")
    var = Variable(name, UnnamedOpetope.Point())
    if var in seq.context:
        raise ValueError("[point rule] Point shaped variable {name} is "
                         "already typed in context {ctx}".format(
                             name = name, ctx = str(seq.context)))
    res = deepcopy(seq)
    res.context = res.context + Typing(
        var, Type(PastingDiagram.point(), None))
    return res


def degen(seq: Sequent, name: str) -> Sequent:
    if seq.pastingDiagram is not None:
        raise ValueError("[degen rule] Sequent cannot have a pasting diagram")
    var = seq.context[name].variable
    res = deepcopy(seq)
    res.pastingDiagram = PastingDiagram.degeneratePastingDiagram(
        UnnamedOpetope.Degen(var.shapeProof), var)
    return res


def graft(seq: Sequent, pd: PastingDiagram) -> Sequent:
    if pd.nodes is None:
        raise ValueError("[graft rule] Parameter pasting diagram cannot be "
                         "degenerate")
    for var in pd.nodes.values():
        if var not in seq.context:
            raise ValueError("[graft rule] Variable {var} in parameter "
                             "pasting diagram is not typed in context"
                             .format(var = var))
    for pj in pd.nodes.keys():
        if not pj.isEpsilon():
            pi, q = pj.innerEdgeDecomposition()
            xi = pd.nodes[pi]
            xj = pd.nodes[pj]
            if seq.context.target(xj.name) != seq.context.source(xi.name, q):
                raise ValueError("[graft rule] Parameter pasting diagram "
                                 "doesn't satisfy axiom [Inner]: variables "
                                 "{xi} and {xj} don't agree on the "
                                 "decoration of edge {edge}".format(
                                     xi = repr(xi),
                                     xj = repr(xj),
                                     edge = repr(pj)))
    res = deepcopy(seq)
    res.pastingDiagram = deepcopy(pd)
    return res
