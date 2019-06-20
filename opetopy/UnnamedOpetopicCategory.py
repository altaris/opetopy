# -*- coding: utf-8 -*-

"""
.. module:: UnnamedOpetopicCategory
   :synopsis: Implementation of opetopic categories and groupoids using the
              unnamed approach to opetopes and opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import Dict, List, Optional, Set

from opetopy.common import *
from opetopy import UnnamedOpetope
from opetopy import UnnamedOpetopicSet


class Type(UnnamedOpetopicSet.Type):
    """
    Similar to :class:`UnnamedOpetopicSet.Type` except information about the
    universality of faces is also stored/
    """

    sourceUniversal: Set[UnnamedOpetope.Address]
    targetUniversal: bool

    def __init__(self, source: UnnamedOpetopicSet.PastingDiagram,
                 target: Optional[UnnamedOpetopicSet.Variable]) -> None:
        """
        Inits the type as in :class:`UnnamedOpetopicSet.Type.__init__`, and
        sets all faces (sources and target) as non universal.
        """
        super().__init__(source, target)
        self.sourceUniversal = set()
        self.targetUniversal = False

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        srcstr = str()
        if self.source.degeneracy is None:
            if self.source.nodes is None:
                raise RuntimeError("[Pasting diagram, to string] Both the "
                                   "degeneracy and node dict of the pasting "
                                   "diagram are None. In valid derivations, "
                                   "this should not happen")
            if self.source.shape == UnnamedOpetope.point().source:
                srcstr = "⧫"
            else:
                lines = []  # type: List[str]
                for addr in self.source.nodes.keys():
                    if self.isSourceUniversal(addr):
                        lines += [str(addr) + " ← ∀" +
                                  str(self.source.nodes[addr])]
                    else:
                        lines += [str(addr) + " ← " +
                                  str(self.source.nodes[addr])]
                srcstr = "{" + ", ".join(lines) + "}"
        else:
            srcstr = "{{" + str(self.source.degeneracy) + "}}"
        if self.isTargetUniversal():
            return srcstr + " → ∀" + str(self.target)
        else:
            return srcstr + " → " + str(self.target)

    def isSourceUniversal(self, addr: UnnamedOpetope.Address) -> bool:
        """
        Tells wether this type is source universal at source address ``addr``.
        """
        return (addr in self.sourceUniversal)

    def isTargetUniversal(self) -> bool:
        """
        Tells wether this type is target universal.
        """
        return self.targetUniversal


def isTargetUniversal(t: UnnamedOpetopicSet.Type) -> bool:
    """
    This convenient function allows to know if an instance of
    :class:`UnnamedOpetopicSet.Type` is target universal, regardless of wether
    or not it is an actual instance of :class:`UnnamedOpetopicCategory.Type`.
    """
    if isinstance(t, Type):
        return t.isTargetUniversal()
    else:
        return False


def isSourceUniversal(t: UnnamedOpetopicSet.Type,
                      addr: UnnamedOpetope.Address) -> bool:
    """
    This convenient function allows to know if an instance of
    :class:`UnnamedOpetopicSet.Type` is source universal at a given address,
    regardless of wether or not it is an actual instance of
    :class:`UnnamedOpetopicCategory.Type`.
    """
    if isinstance(t, Type):
        return t.isSourceUniversal(addr)
    else:
        return False


def tfill(seq: UnnamedOpetopicSet.Sequent, targetName: str,
          fillerName: str) -> UnnamedOpetopicSet.Sequent:
    """
    This function takes a :class:`UnnamedOpetopicSet.Sequent`, (recall that
    the context of a sequent derivable in :math:`\\textbf{OptSet${}^?$}` is
    a finite opetopic set) typing a pasting diagram :math:`\\mathbf{P}`, and
    solves the Kan filler problem by adding

    * a new cell :math:`t` with name ``targetName``;
    * a new cell :math:`\\alpha : \\mathbf{P} \\longrightarrow t` with name
      ``fillerName``.

    """
    if seq.pastingDiagram is None:
        raise DerivationError(
            "Kan filling, target",
            "Argument sequent expecting to type a pasting diagram")

    # Source of alpha
    P = seq.pastingDiagram
    tPshapeProof = UnnamedOpetope.ProofTree(P.shapeTarget().toDict())

    # Start deriving
    res = deepcopy(seq)
    res.pastingDiagram = None

    # Derive t
    if P.shape.dimension - 1 == 0:
        # t is a point
        res = UnnamedOpetopicSet.point(res, targetName)
    else:
        # Set u, target of t
        if P.shape.isDegenerate:
            u = P.degeneracyVariable()
        else:
            u = seq.context.target(
                P.source(UnnamedOpetope.address([], P.shape.dimension - 1)))
        # Derive Q, source of t
        if P.shapeTarget().isDegenerate:
            Q = UnnamedOpetopicSet.pastingDiagram(
                tPshapeProof, seq.context.target(u))
        else:
            nodes = {}  # type: Dict[UnnamedOpetope.Address, str]
            if P.shape.isDegenerate:
                nodes[UnnamedOpetope.address([], P.shape.dimension - 2)] = \
                    P.degeneracyVariable()
            else:
                readdress = P.shapeProof.eval().context
                for l in P.shape.leafAddresses():
                    p, q = l.edgeDecomposition()
                    nodes[readdress(l)] = seq.context.source(P[p], q)
            Q = UnnamedOpetopicSet.pastingDiagram(tPshapeProof, nodes)
        if Q.shape.isDegenerate:
            res = UnnamedOpetopicSet.degen(res, Q.degeneracyVariable())
        else:
            res = UnnamedOpetopicSet.graft(res, Q)
        # Derive t, target of alpha
        res = UnnamedOpetopicSet.shift(res, u, targetName)

    # Derive P, source of alpha
    if P.shape.isDegenerate:
        res = UnnamedOpetopicSet.degen(res, u)
    else:
        res = UnnamedOpetopicSet.graft(res, P)

    # Derive alpha
    res = UnnamedOpetopicSet.shift(res, targetName, fillerName)

    # Mark t as universal in the type of alpha
    rawFillerType = res.context[fillerName].type
    fillerType = Type(rawFillerType.source, rawFillerType.target)
    fillerType.targetUniversal = True
    res.context[fillerName].type = fillerType

    # Done
    return res


def tuniv(seq: UnnamedOpetopicSet.Sequent, tuCell: str, cell: str,
          factorizationName: str,
          fillerName: str) -> UnnamedOpetopicSet.Sequent:
    """
    From a target universal cell :math:`\\alpha : \\mathbf{P}
    \\longrightarrow t` (whose name is ``tuCell``), and another cell
    :math:`\\beta : \\mathbf{P} \\longrightarrow u`, creates the universal
    factorization.
    """
    # Inits
    typealpha = seq.context[tuCell].type
    typebeta = seq.context[cell].type
    P = typealpha.source
    targetalpha = typealpha.target
    targetbeta = typebeta.target

    # Checks
    if seq.pastingDiagram is not None:
        raise DerivationError(
            "Apply target univ. prop.",
            "Sequent cannot type a pasting diagram")
    elif not isTargetUniversal(typealpha):
        raise DerivationError(
            "Apply target univ. prop.",
            "First cell is expected to be target universal")
    elif typebeta.source != P:
        raise DerivationError(
            "Apply target univ. prop.",
            "Cells are expected to have the same source pasting diagram")
    elif targetalpha is None or targetbeta is None:
        raise RuntimeError(
            "[Apply target univ. prop.] Target universal cell is a point. In "
            "valid derivations, this should not happen")

    # Derive the factorization cell
    n = targetalpha.shape.dimension
    res = UnnamedOpetopicSet.graft(
        deepcopy(seq), UnnamedOpetopicSet.pastingDiagram(
            UnnamedOpetope.Shift(targetalpha.shapeProof),
            {
                UnnamedOpetope.address([], n): targetalpha.name
            }))
    res = UnnamedOpetopicSet.shift(res, targetbeta.name, factorizationName)

    # Derive the filler
    res = UnnamedOpetopicSet.graft(
        res, UnnamedOpetopicSet.pastingDiagram(
            UnnamedOpetope.Graft(
                UnnamedOpetope.Shift(
                    UnnamedOpetope.Shift(targetalpha.shapeProof)),
                P.shapeProof,
                UnnamedOpetope.address([[]], n + 1)),
            {
                UnnamedOpetope.address([], n + 1): factorizationName,
                UnnamedOpetope.address([[]], n + 1): tuCell
            }))
    res = UnnamedOpetopicSet.shift(res, cell, fillerName)

    # Mark the filler as target universal and source universal at the facto.
    rawFillerType = res.context[fillerName].type
    fillerType = Type(rawFillerType.source, rawFillerType.target)
    fillerType.targetUniversal = True
    fillerType.sourceUniversal.add(UnnamedOpetope.address([], n + 1))
    res.context[fillerName].type = fillerType

    # Done
    return res


def suniv(seq: UnnamedOpetopicSet.Sequent, suCellName: str, cellName: str,
          addr: UnnamedOpetope.Address, factorizationName: str,
          fillerName: str) -> UnnamedOpetopicSet.Sequent:
    """
    From

    * an address :math:`[p]` (argument ``addr``);
    * a cell :math:`\\alpha : \\forall_{[p]} \\mathbf{P} \\longrightarrow u`
      (with name ``suCellName``);
    * a cell :math:`\\beta : \\mathbf{P'} \\longrightarrow
      u` (with name ``cellName``), where :math:`\\mathbf{P'}` is
      :math:`\\mathbf{P}` except at address :math:`[p]` where it is :math:`s`;

    applies the source universal property of :math:`\\alpha` at :math:`[p]`
    over :math:`\\beta`, thus creating

    * a factorization cell :math:`\\xi : s \\longrightarrow \\mathsf{s}_{[p]}
      \\mathbf{P}`;
    * a filler :math:`A`, target universal, and source universal at
      :math:`\\xi`, i.e. at address :math:`[[p]]`.
    """

    # Inits
    alphatype = seq.context[suCellName].type
    betatype = seq.context[cellName].type
    P = alphatype.source
    Q = betatype.source
    u = alphatype.target

    # Checks & inits
    if seq.pastingDiagram is not None:
        raise DerivationError(
            "Apply source univ. prop.",
            "Sequent expected to not type a pasting diagram")
    elif u is None:
        raise RuntimeError("[Apply source univ. prop.] Source universal cell "
                           "{sucell} is a point. In valid derivations, this "
                           "should not happen".format(sucell=suCellName))
    elif P.nodes is None:
        raise DerivationError(
            "Apply source univ. prop.",
            "Source universal cell {sucell} cannot be degenerate",
            sucell=suCellName)
    elif Q.nodes is None:
        raise DerivationError(
            "Apply source univ. prop.",
            "Cell {cell} cannot be degenerate",
            cell=cellName)
    elif addr not in P.nodes.keys():
        raise DerivationError(
            "Apply source univ. prop.",
            "Address {addr} not in source of {sucell}",
            addr=addr, sucell=suCellName)
    elif betatype.target != u:
        raise DerivationError(
            "Apply source univ. prop.",
            "Cells {sucell} and {cell} are not compatible: targets differ",
            cell=cellName, sucell=suCellName)
    elif P.nodes.keys() != Q.nodes.keys():
        raise DerivationError(
            "Apply source univ. prop.",
            "Cells {sucell} and {cell} are not compatible: source pasting "
            "diagrams do not have the same addresses",
            cell=cellName, sucell=suCellName)
    for a in P.nodes.keys():
        if a != addr and P.nodes[a] != Q.nodes[a]:
            raise DerivationError(
                "Apply source univ. prop.",
                "Cells {sucell} and {cell} are not compatible: source pasting "
                "diagrams do not agree on address {a}",
                cell=cellName, sucell=suCellName, a=a)

    # Derive xi
    xishapeproof = seq.context[Q.source(addr)].type.source.shapeProof
    res = UnnamedOpetopicSet.graft(
        seq, UnnamedOpetopicSet.pastingDiagram(
            UnnamedOpetope.Shift(xishapeproof),
            {
                UnnamedOpetope.address([], Q.shape.dimension - 1):
                    Q.source(addr)
            }))
    res = UnnamedOpetopicSet.shift(res, P.source(addr), factorizationName)

    # Derive A
    omega = UnnamedOpetope.Graft(
        UnnamedOpetope.Shift(P.shapeProof),
        UnnamedOpetope.Shift(xishapeproof),
        addr.shift())
    res = UnnamedOpetopicSet.graft(
        res, UnnamedOpetopicSet.pastingDiagram(
            omega,
            {
                UnnamedOpetope.address([], P.shape.dimension): suCellName,
                addr.shift(): factorizationName
            }))
    res = UnnamedOpetopicSet.shift(res, cellName, fillerName)

    # Mark A as source universal at xi and target universal
    rawFillerType = res.context[fillerName].type
    fillerType = Type(rawFillerType.source, rawFillerType.target)
    fillerType.targetUniversal = True
    fillerType.sourceUniversal.add(addr.shift())
    res.context[fillerName].type = fillerType

    # Done
    return res


def tclose(seq: UnnamedOpetopicSet.Sequent,
           tuCell: str) -> UnnamedOpetopicSet.Sequent:
    """
    From a target universal cell :math:`A : \\mathbf{P} \\longrightarrow
    \\forall u` such that all its faces are target universal but one,
    turns that one target universal as well.
    """

    # Inits
    P = seq.context[tuCell].type.source
    u = seq.context[tuCell].type.target

    # Checks
    if seq.pastingDiagram is not None:
        raise DerivationError(
            "Apply target univ. closure",
            "Sequent expected to not type a pasting diagram")
    elif u is None:
        raise RuntimeError("[Apply target univ. closure] Target universal "
                           "cell {cell} is a point. In valid derivations, "
                           "this should not happen".format(cell=tuCell))

    # If P is degenerate, make u target universal
    if P.shape.isDegenerate:
        res = deepcopy(seq)
        rawTargetType = res.context[u.name].type
        targetType = Type(rawTargetType.source, rawTargetType.target)
        targetType.targetUniversal = True
        res.context[u.name].type = targetType
        return res

    # Get non target universal source address (if any)
    if P.nodes is None:
        raise RuntimeError("[Apply target univ. closure] Target universal "
                           "cell {cell} non degenerate, yet it source pasting "
                           "diagram has no nodes. In valid derivations, this "
                           "should not happen".format(cell=tuCell))
    else:
        nonTuSource = None  # type: Optional[UnnamedOpetope.Address]
        for addr in P.nodes.keys():
            if not isTargetUniversal(seq.context[P.source(addr)].type):
                if nonTuSource is None:
                    nonTuSource = addr
                else:
                    raise DerivationError(
                        "Apply target univ. closure",
                        "Source pasting diagram has at least two non target "
                        "universal sources: {addr1} and {addr2}"
                        .format(addr1=nonTuSource, addr2=addr))

    if isTargetUniversal(seq.context[u.name].type):
        if nonTuSource is None:
            raise DerivationError(
                "Apply target univ. closure",
                "All faces of source pasting diagram are already target "
                "universal. You can just remove this rule instance")
        # Make source at nonTuSource target universal
        res = deepcopy(seq)
        rawSourceType = res.context[P.source(nonTuSource)].type
        sourceType = Type(rawSourceType.source, rawSourceType.target)
        sourceType.targetUniversal = True
        res.context[P.source(nonTuSource)].type = sourceType
        return res
    else:
        if nonTuSource is not None:
            raise DerivationError(
                "Apply target univ. closure",
                "Source pasting diagram has at least two non target universal "
                "faces: target and {addr}".format(addr=nonTuSource))
        # Make u target universal
        res = deepcopy(seq)
        rawTargetType = res.context[u.name].type
        targetType = Type(rawTargetType.source, rawTargetType.target)
        targetType.targetUniversal = True
        res.context[u.name].type = targetType
        return res


class TFill(UnnamedOpetopicSet.RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{tfill}` rule in a
    proof tree.
    """

    fillerName: str
    proofTree: UnnamedOpetopicSet.RuleInstance
    targetName: str

    def __init__(self, p: UnnamedOpetopicSet.RuleInstance, targetName: str,
                 fillerName: str) -> None:
        self.fillerName = fillerName
        self.proofTree = p
        self.targetName = targetName

    def __str__(self) -> str:
        return "TFill({p}, {t}, {f})".format(
            p=str(self.proofTree), t=self.targetName, f=self.fillerName)

    def __repr__(self) -> str:
        return "TFill({p},{t},{f})".format(
            p=repr(self.proofTree), t=self.targetName, f=self.fillerName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{tfill}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> UnnamedOpetopicSet.Sequent:
        return tfill(self.proofTree.eval(), self.targetName, self.fillerName)


class TUniv(UnnamedOpetopicSet.RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{tuniv}` rule in a
    proof tree.
    """

    cellName: str
    factorizationName: str
    fillerName: str
    proofTree: UnnamedOpetopicSet.RuleInstance
    tuCellName: str

    def __init__(self, p: UnnamedOpetopicSet.RuleInstance, tuCell: str,
                 cell: str, factorizationName: str, fillerName: str) -> None:
        self.cellName = cell
        self.factorizationName = factorizationName
        self.fillerName = fillerName
        self.proofTree = p
        self.tuCellName = tuCell

    def __str__(self) -> str:
        return "TUniv({p}, {tu}, {c})".format(
            p=str(self.proofTree), tu=self.tuCellName, c=self.cellName)

    def __repr__(self) -> str:
        return "TUniv({p},{tu},{c})".format(
            p=repr(self.proofTree), tu=self.tuCellName, c=self.cellName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{tuniv-$" + self.tuCellName + "$/$" + \
            self.cellName + "$}}\n\t\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> UnnamedOpetopicSet.Sequent:
        return tuniv(self.proofTree.eval(), self.tuCellName, self.cellName,
                     self.factorizationName, self.fillerName)


class SUniv(UnnamedOpetopicSet.RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{suniv}` rule in a
    proof tree.
    """

    address: UnnamedOpetope.Address
    cellName: str
    factorizationName: str
    fillerName: str
    proofTree: UnnamedOpetopicSet.RuleInstance
    suCellName: str

    def __init__(self, p: UnnamedOpetopicSet.RuleInstance, suCellName: str,
                 cellName: str, addr: UnnamedOpetope.Address,
                 factorizationName: str, fillerName: str) -> None:
        self.address = addr
        self.cellName = cellName
        self.factorizationName = factorizationName
        self.fillerName = fillerName
        self.proofTree = p
        self.suCellName = suCellName

    def __str__(self) -> str:
        return "SUniv({p}, {su}, {c})".format(
            p=str(self.proofTree), su=self.suCellName, c=self.cellName)

    def __repr__(self) -> str:
        return "SUniv({p},{su},{c})".format(
            p=repr(self.proofTree), su=self.suCellName, c=self.cellName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{suniv-$" + self.suCellName + "$/$" + \
            self.cellName + "$}}\n\t\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> UnnamedOpetopicSet.Sequent:
        return suniv(self.proofTree.eval(), self.suCellName, self.cellName,
                     self.address, self.factorizationName, self.fillerName)


class TClose(UnnamedOpetopicSet.RuleInstance):
    """
    A class representing an instance of the :math:`\\texttt{tclose}` rule in a
    proof tree.
    """

    proofTree: UnnamedOpetopicSet.RuleInstance
    tuCellName: str

    def __init__(self, p: UnnamedOpetopicSet.RuleInstance,
                 tuCell: str) -> None:
        self.proofTree = p
        self.tuCellName = tuCell

    def __str__(self) -> str:
        return "TClose({p}, {tu})".format(
            p=str(self.proofTree), tu=self.tuCellName)

    def __repr__(self) -> str:
        return "TClose({p},{tu})".format(
            p=repr(self.proofTree), tu=self.tuCellName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetopicSet.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{tclose-$" + self.tuCellName + \
            "$}}\n\t\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> UnnamedOpetopicSet.Sequent:
        return tclose(self.proofTree.eval(), self.tuCellName)
