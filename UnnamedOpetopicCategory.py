# -*- coding: utf-8 -*-

"""
.. module:: opetopy.UnnamedOpetopicCategory
   :synopsis: Implementation of opetopic categories and groupoids using the
              unnamed approach to opetopes and opetopic sets

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import Dict, List, Optional, Set

from common import *

import UnnamedOpetope
import UnnamedOpetopicSet


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
                        lines += [repr(addr) + "←!" +
                                  repr(self.source.nodes[addr])]
                    else:
                        lines += [repr(addr) + "←" +
                                  repr(self.source.nodes[addr])]
                srcstr = "PD({})".format(",".join(lines))
        else:
            srcstr = "DPD({})".format(repr(self.source.degeneracy))
        if self.isTargetUniversal():
            return srcstr + "→!" + repr(self.target)
        else:
            return srcstr + "→" + repr(self.target)

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
                        lines += [str(addr) + " ← !" +
                                  str(self.source.nodes[addr])]
                    else:
                        lines += [str(addr) + " ← " +
                                  str(self.source.nodes[addr])]
                srcstr = "PastingDiagram({})".format(", ".join(lines))
        else:
            srcstr = "DegeneratePastingDiagram({})".format(
                str(self.source.degeneracy))
        if self.isTargetUniversal():
            return srcstr + " → !" + str(self.target)
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


def fillTargetHorn(seq: UnnamedOpetopicSet.Sequent,
                   targetName: str,
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
    shapeProof = P.shapeProof
    targetShapeProof = UnnamedOpetope.ProofTree(P.shapeTarget().toDict())

    # Target of t
    u = str()
    if P.shape.isDegenerate:
        u = P.degeneracyVariable()
    else:
        u = seq.context.target(
            P.source(UnnamedOpetope.address([], P.shape.dimension - 1)))

    # Source of t
    Q = UnnamedOpetopicSet.PastingDiagram()
    if P.shapeTarget().isDegenerate:
        Q = UnnamedOpetopicSet.pastingDiagram(targetShapeProof, u)
    else:
        nodes = {}  # type: Dict[UnnamedOpetope.Address, str]
        readdress = P.shapeProof.eval().context
        for l in P.shape.leafAddresses():
            p, q = l.edgeDecomposition()
            nodes[readdress(l)] = seq.context.source(P[p], q)
        Q = UnnamedOpetopicSet.pastingDiagram(targetShapeProof, nodes)

    # Derive Q
    res = deepcopy(seq)
    res.pastingDiagram = None
    if Q.shape.isDegenerate:
        res = UnnamedOpetopicSet.degen(res, Q.degeneracyVariable())
    else:
        res = UnnamedOpetopicSet.graft(res, Q)

    # Derive t
    res = UnnamedOpetopicSet.fill(res, u, targetName)

    # Derive P
    if P.shape.isDegenerate:
        res = UnnamedOpetopicSet.degen(res, P.degeneracyVariable())
    else:
        res = UnnamedOpetopicSet.graft(res, P)

    # Derive alpha
    res = UnnamedOpetopicSet.fill(res, targetName, fillerName)

    # Mark t as universal in the type of alpha
    rawFillerType = res.context[fillerName].type
    fillerType = Type(rawFillerType.source, rawFillerType.target)
    fillerType.targetUniversal = True
    res.context[fillerName].type = fillerType

    # Done
    return res
