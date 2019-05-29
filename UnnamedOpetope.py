# -*- coding: utf-8 -*-

"""
.. module:: UnnamedOpetope
   :synopsis: Implementation of the unnamed approach for opetopes

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .common import *


class Address:
    """
    The :math:`0`-address :math:`*` is construced as::

      Address.epsilon(0)

    More generally, the empty address is construced as::

      Address.epsilon(n)

    Recall that an :math:`n`-address is by definition a sequence of
    :math:`(n-1)`-addresses. To append an :math:`(n-1)`-address to a
    :math:`n`-address, use the :meth:`Address.__add__`
    method. For instance, the following yields the :math:`1`-address
    :math:`[**]`::

      Address.epsilon(1) + Address.epsilon(0) + Address.epsilon(0)

    Given two :math:`n`-addresses, it is possible to concatenate them using
    the :meth:`Address.__mul__` method. Following up
    on the previous examples, the following expression yields the address
    :math:`[****]`::

      x = Address.epsilon(1) + Address.epsilon(0) + Address.epsilon(0)
      x * x

    """

    dimension: int
    edges: List['Address']

    def __add__(self, other) -> 'Address':
        """
        Adds the :math:`(n-1)`-address ``other`` at the end of the sequence of
        :math:`(n-1)`-addresses that make up the :math:`n`-address ``self``.

        :warning: This is **not** concatenation (see
          :meth:`Address.__mul__`).
        """
        if (self.dimension != other.dimension + 1):
            raise DerivationError(
                "Address extension",
                "Dimension mismatch: address {this} is {sdim} dimensional "
                "and cannot be extended by {other} which is {odim} "
                "dimensional",
                this = str(self), sdim = self.dimension, other = str(other),
                odim = other.dimension)
        result = deepcopy(self)
        result.edges += [other]
        return result

    def __eq__(self, other) -> bool:
        """
        Compares two addresses. Two addresses are equal if they have the same
        dimension and the same underlying list of addresses.
        """
        if not isinstance(other, Address):
            raise NotImplementedError
        elif self.dimension == other.dimension and \
                len(self.edges) == len(other.edges):
            for i in range(len(self.edges)):
                if self.edges[i] != other.edges[i]:
                    return False
            return True
        else:
            return False

    def __hash__(self):
        return hash(str(self))

    def __init__(self, dim: int) -> None:
        """
        Creates an empty address of dimension ``dim``
        :math:`\\geq 0`.
        """
        if (dim < 0):
            raise DerivationError(
                "Address creation",
                "New address must have dimension >= 0 (is {dim})",
                dim = dim)
        self.dimension = dim
        self.edges = []  # type: List[Address]

    def __lt__(self, other: 'Address') -> bool:
        """
        Compares two addresses with respect to the lexicographical order.
        """
        if self.dimension != other.dimension:
            raise DerivationError(
                "Address comparison",
                "Cannot compare addresses {this} and {other} as dimensions do "
                "not match (are respectively {sdim} and {odim})",
                this = str(self), other = str(other), sdim = self.dimension,
                odim = other.dimension)
        for i in range(min(len(self.edges), len(other.edges))):
            if self.edges[i] < other.edges[i]:
                return True
            elif self.edges[i] > other.edges[i]:
                return False
        return len(self.edges) < len(other.edges)

    def __mul__(self, other: 'Address') -> 'Address':
        """
        Concatenates two :math:`n`-addresses by concatenating the underlying
        lists of :math:`(n-1)`-addresses.
        """
        if (self.dimension != other.dimension):
            raise DerivationError(
                "Address concatenation",
                "Cannot concatenate addresses {this} and {other} as "
                "dimensions do not match (are respectively {sdim} and {odim})",
                this = str(self), other = str(other), sdim = self.dimension,
                odim = other.dimension)
        result = deepcopy(self)
        result.edges += other.edges
        return result

    def __repr__(self) -> str:
        return "Address({str}, {dim})".format(
            str = str(self),
            dim = str(self.dimension))

    def __str__(self) -> str:
        """
        Converts an address to a human readable string. The
        :math:`0`-dimensional empty address is represented by the
        symbol ``*``.
        """
        if self == Address.epsilon(0):
            return '*'
        else:
            return '[' + ''.join(map(str, self.edges)) + ']'

    @staticmethod
    def epsilon(dim: int) -> 'Address':
        """
        Creates an empty address of dimension ``dim``
        :math:`\\geq 0`. Internally just calls
        :meth:`Address.__init__`.
        """
        return Address(dim)

    def edgeDecomposition(self) -> Tuple['Address', 'Address']:
        """
        If the current address is of the form :math:`[p[q]]` (or equivalently,
        not an epsilon address), returns the tuple :math:`([p], [q])`.
        """
        if self.isEpsilon():
            raise DerivationError(
                "Address, inner edge decomposition",
                "Current is not an epsilon address")
        p = Address(self.dimension)
        p.edges = self.edges[:-1]
        q = self.edges[-1]
        return (p, q)

    def isEpsilon(self) -> bool:
        """
        Simply tells wither the current address is of the form
        :math:`[]`.
        """
        return len(self.edges) == 0

    @staticmethod
    def fromList(l: List[Any], dim: int) -> 'Address':
        """
        Recursibely create an address of dimension ``dim`` from a list of lists
        that themselves represent addresses. The empty address is
        represented by ``[]``, and ``'*'`` represents the
        :math:`0`-dimensional empty address.
        """
        if (dim < 0):
            raise DerivationError(
                "Address creation",
                "New address must have dimension >= 0 (is {dim})",
                dim = dim)
        if len(l) == 0:
            return Address.epsilon(dim)
        la = []  # type: List[Address]
        for x in l:
            if x == []:
                la += [Address.epsilon(dim - 1)]
            elif x == '*':
                la += [Address.epsilon(0)]
            else:
                la += [Address.fromList(x, dim - 1)]
        return Address.fromListOfAddresses(la)

    @staticmethod
    def fromListOfAddresses(l: List['Address']) -> 'Address':
        """
        Creates an address from a non empty list of addresses.
        """
        if len(l) == 0:
            raise DerivationError(
                "Address creation",
                "Cannot create address from an empty list of addresses")
        else:
            a = l[0].shift()
            for b in l[1:]:
                a += b
            return a

    def shift(self, n: int = 1) -> 'Address':
        """
        Returns the curent address shifted by :math:`n` dimensions.

        Example:
          :math:`[[][*]]` ``.shift(2)`` is
          :math:`[[[[][*]]]]`
        """
        if n < 0:
            raise DerivationError(
                "Address shift",
                "Shift exponent must be >= 0 (is {dim})",
                dim = n)
        elif n == 0:
            return self
        else:
            return Address.epsilon(self.dimension + n) + self.shift(n - 1)

    @staticmethod
    def substitution(a: 'Address', b: 'Address', c: 'Address') -> 'Address':
        """
        If the underlying sequence of ``b`` is a prefix of that of ``a``, then
        replaces this prefix by the underlying sequence of ``c``.

        Example:
          ``substitution(`` :math:`[[*][**]]` ``,`` :math:`[[*]]` ``,``
          :math:`[[][]]` ``)`` is
          :math:`[[][][**]]`
        """
        if not (a.dimension == b.dimension and b.dimension == c.dimension):
            raise DerivationError(
                "Address substitution",
                "Cannot substitute prefix {a} of {b} by {c} as dimensions do "
                "not match (are respectively {ad}, {bd}, and {cd})",
                a = str(a), b = str(b), c = str(c), ad = str(a.dimension),
                bd = str(b.dimension), cd = str(c.dimension))
        if a.edges[0:len(b.edges)] == b.edges:
            r = deepcopy(a)
            r.edges[0:len(b.edges)] = c.edges
            return r
        else:
            return a

    def toTex(self) -> str:
        """
        Converts the address to TeX code.
        """
        if self == Address.epsilon(0):
            return '*'
        elif len(self.edges) == 0:
            return '[]'
        else:
            return '[' + ''.join(map(Address.toTex, self.edges)) + ']'


class Context(Dict[Address, Address]):
    """
    A :math:`(n+1)`-context can be seen as a partial injective function from
    the set :math:`\\mathbb{A}_n` of :math:`n`-addresses to the set
    :math:`\\mathbb{A}_{n-1}` of :math:`(n-1)`-addresses.
    """

    dimension: int

    def __add__(self, other: Tuple[Address, Address]) -> 'Context':
        """
        Adds a tuple of the form (math:`n`-address, :math:`(n-1)`-address) to
        the :math:`(n+1)`-context ``self``.
        """
        if other[0].dimension != other[1].dimension + 1:
            raise DerivationError(
                "Context extension",
                "New mapping {a} -> {b} is ill-formed as dimensions do not "
                "match (are respectively {ad} and {bd}",
                a = str(other[0]), b = str(other[1]),
                ad = str(other[0].dimension), bd = str(other[1].dimension))
        elif other[0].dimension + 1 != self.dimension:
            raise DerivationError(
                "Context extension",
                "New mapping {a} -> {b} cannot be added to context {this} as "
                "dimension do not match (context has dimension {sdim}, "
                "first address has dimension {ad}, should have dimension "
                "{should}",
                a = str(other[0]), b = str(other[1]), this = str(self),
                sdim = self.dimension, ad = str(other[0].dimension),
                should = str(self.dimension - 1))
        elif other[0] in self.keys():
            raise DerivationError(
                "Context extension",
                "New mapping {a} -> {b} cannot be added to context {this} as "
                "first address is already present in context",
                a = str(other[0]), b = str(other[1]), this = str(self))
        elif other[1] in self.values():
            raise DerivationError(
                "Context extension",
                "New mapping {a} -> {b} cannot be added to context {this} as "
                "second address is already present in context",
                a = str(other[0]), b = str(other[1]), this = str(self))
        r = deepcopy(self)
        r[other[0]] = other[1]
        return r

    def __call__(self, addr: Address) -> Address:
        """
        If ``self`` is an `(n+1)`-context, returns the node
        :math:`(n-1)`-address associated to the given leaf
        :math:`n`-address ``addr``. Raises an exception if not defined.
        """
        if not self.definedOnLeaf(addr):
            raise DerivationError(
                "Context call",
                "Context {this} is not defined on leaf {addr}",
                this = str(self), addr = str(addr))
        return self[addr]

    def __eq__(self, other) -> bool:
        """
        Tests equality between two contexts. Two contexts are equal if they
        have the same dimension and if the partial mapping
        :math:`\\mathbb{A}_n \\longrightarrow \\mathbb{A}_{n-1}` they represent
        are (extentionally) equal.
        """
        if not isinstance(other, Context):
            raise NotImplementedError
        return self.dimension == other.dimension and dict.__eq__(self, other)

    def __init__(self, dim: int) -> None:
        """
        Creates an empty context of dimension :math:`\\geq 0`.
        """
        if (dim < 0):
            raise DerivationError(
                "Context creation",
                "Context must have dimension >= 0 (is {dim})",
                dim = dim)
        self.dimension = dim

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Converts a context to a human readable string.
        """
        if len(self) == 0:
            return "{}"
        else:
            res = [str(x) + " ↦ " + str(self[x])
                   for x in sorted(list(self.keys()))]
            return "{\n    " + "\n    ".join(res) + "\n}"

    def __sub__(self, addr: Address) -> 'Context':
        """
        Removes a address ``addr`` from the domain of definition of the
        context.
        """
        if not self.definedOnLeaf(addr):
            raise DerivationError(
                "Context restriction",
                "Context {this} does not contain leaf {addr}",
                this = str(self), addr = str(addr))
        r = deepcopy(self)
        del r[addr]
        return r

    def definedOnLeaf(self, addr: Address) -> bool:
        """
        Returns wether the context is defined on address ``addr``.
        """
        return addr in self.keys()

    def leaves(self) -> Set[Address]:
        """
        Returns the set of addresses on which the context is defined.
        """
        return set(self.keys())

    def toTex(self) -> str:
        res = ["\\frac{" + x.toTex() + "}{" + self(x).toTex() + "}"
               for x in sorted(self.leaves())]
        return ", ".join(res)


class Preopetope:
    """
    Main class of the module.
    """

    dimension: int
    degeneracy: Optional['Preopetope']
    isDegenerate: bool
    nodes: Dict[Address, 'Preopetope']

    def __add__(self, t: Tuple[Address, 'Preopetope']) -> 'Preopetope':
        """
        Adds a (:math:`(n-1)`-address, :math:`(n-1)`-preopetope) tuple ``t`` to
        the non degenerate ``self`` :math:`n`-preopetope. The
        :math:`(n-1)`-address must not be present.
        """
        if self.isDegenerate:
            raise DerivationError(
                "Preopetope extension",
                "Cannot add an address to a degenerate preopetope")
        elif t[0].dimension != t[1].dimension:
            raise DerivationError(
                "Preopetope extension",
                "Cannot add address {addr} to preopetope {this} as dimension "
                "do not match (are respectively {adim} and {sdim})",
                addr = str(t[0]), this = str(self), adim = t[0].dimension,
                sdim = self.dimension)
        elif t[0].dimension + 1 != self.dimension:
            raise DerivationError(
                "Preopetope extension",
                "Specified extension {addr} : {p} cannot be added to "
                "preopetope as dimension don't match (address dimension is "
                "{adim}, should be {should})",
                addr = str(t[0]), p = str(t[1]), adim = t[0].dimension,
                should = self.dimension - 1)
        elif t[0] in self.nodes.keys():
            raise DerivationError(
                "Preopetope extension",
                "Address {addr} already present in preopetope {this}",
                addr = str(t[0]), this = str(self))
        else:
            u = deepcopy(self)
            u.nodes[t[0]] = t[1]
            return u

    def __eq__(self, other):
        """
        Tests equality between two preopetopes. Two preopetopes are equal if
        they have the same dimension, and if either

        * they are both degenerate on the same preopetope;
        * they are both non degenerate, have the same (address, preopetope)
          tuples.
        """
        if not isinstance(other, Preopetope):
            raise NotImplementedError
        elif self.dimension != other.dimension:
            return False
        elif self.isDegenerate ^ other.isDegenerate:
            return False
        elif set(self.nodes.keys()) != set(other.nodes.keys()):
            return False
        else:
            for k in self.nodes.keys():
                if self.nodes[k] != other.nodes[k]:
                    return False
            return True

    def __init__(self, dim: int) -> None:
        """
        Inits an **invalid** preopetope of dimension ``dim``. This method
        should not be called directly.
        """
        if (dim < -1):
            raise DerivationError(
                "Preopetope creation",
                "Preopetope must have dimension >= -1 (is {dim})",
                dim = dim)
        self.dimension = dim
        self.isDegenerate = False
        self.nodes = {}

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Converts a preopetope to a human readable string. The
        :math:`(-1)`-preopetope is represented by ``"∅"``, the
        :math:`0`-preopetope by ``"⧫"``, and the unique
        :math:`1`-preopetope by ``"■"``.
        """
        if self.dimension == -1:
            return "∅"
        elif self.dimension == 0:
            return "⧫"
        elif self == Preopetope.fromDictOfPreopetopes({
                Address.epsilon(0): Preopetope.point()}):
            return "■"
        elif self.isDegenerate:
            return "degen({d})".format(d = str(self.degeneracy))
        else:
            res = [str(x) + ": " + str(self.nodes[x]).replace("\n", "\n    ")
                   for x in sorted(self.nodes)]
            return "{\n    " + "\n    ".join(res) + "\n}"

    def __sub__(self, addr: Address) -> 'Preopetope':
        """
        Removes source at address ``addr``.
        """
        if addr not in self.nodeAddresses():
            raise DerivationError(
                "Preopetope restriction",
                "Cannot remove address {addr} from preopetope {this} as it is "
                "not present",
                addr = str(addr), this = str(self))
        r = deepcopy(self)
        del r.nodes[addr]
        return r

    @staticmethod
    def degenerate(q: 'Preopetope') -> 'Preopetope':
        """
        Constructs the degenerate preopetope at ``q``.
        """
        if q.dimension < 0:
            raise DerivationError(
                "Preopetope degeneration",
                "Cannot degenerate the (-1)-preopetope")
        p = Preopetope(q.dimension + 2)
        p.degeneracy = q
        p.isDegenerate = True
        return p

    @staticmethod
    def empty() -> 'Preopetope':
        """
        Constructs the unique :math:`(-1)`-preopetope.
        """
        return Preopetope(-1)

    @staticmethod
    def fromDictOfPreopetopes(d: Dict[Address, 'Preopetope']) -> 'Preopetope':
        """
        Creates a non degenerate preopetope from a ``dict`` of preopetopes
        indexed by their addresses.
        """
        if len(d) == 0:
            raise DerivationError(
                "Preopetope creation",
                "Cannot create preopetope from an empty dictionnary")
        items = list(d.items())
        p = Preopetope(items[0][0].dimension + 1) + items[0]
        for t in items[1:]:
            p += t
        return p

    @staticmethod
    def grafting(p: 'Preopetope', addr: Address,
                 q: 'Preopetope') -> 'Preopetope':
        """
        Grafts the :math:`n`-preopetope ``q`` on the :math:`n`-preopetope
        ``p`` at address ``addr``.
        For improper grafting, see
        :meth:`UnnamedOpetope.Preopetope.improperGrafting`
        """
        if p.dimension != q.dimension:
            raise DerivationError(
                "Preopetope grafting",
                "Cannot graft preopetope {q} on {p} as dimensions do not "
                "match (are respectively {qd} and {pd}",
                p = str(p), q = str(q), pd = p.dimension, qd = q.dimension)
        elif p.dimension != addr.dimension + 1:
            raise DerivationError(
                "Preopetope grafting",
                "Cannot graft preopetope {q} on {p} at address {addr} as "
                "dimensions of address do not match that of the preopetopes "
                "(preopetopes have dimension {d}, address has dimension {ad}, "
                "should have {should}",
                p = str(p), q = str(q), d = p.dimension, ad = addr.dimension,
                should = p.dimension - 1)
        else:
            r = p
            for t in list(q.nodes.items()):
                r += (addr * t[0], t[1])
            return r

    @staticmethod
    def improperGrafting(p: 'Preopetope', addr: Address, q: 'Preopetope'):
        """
        Performs the improper grafting of the :math:`(n-1)`-preopetope ``q`` on
        the :math:`n`-preopetope ``p`` at address ``addr``.
        For proper grafting, see
        :meth:`UnnamedOpetope.Preopetope.grafting`
        """
        return p + (addr, q)

    def leafAddresses(self) -> Set[Address]:
        """
        Returnst the set of leaf addresses of the preopetope.
        """
        res = []  # type: List[Address]
        for p in self.nodeAddresses():
            for q in self.source(p).nodeAddresses():
                if p + q not in self.nodeAddresses():
                    res += [p + q]
        return set(res)

    def nodeAddresses(self) -> Set[Address]:
        """
        Returns the set of node addresses of the preopetope.
        """
        return set(self.nodes.keys())

    @staticmethod
    def point() -> 'Preopetope':
        """
        Constructs the unique :math:`0`-preopetope.
        """
        return Preopetope(0)

    def source(self, addr: Address) -> 'Preopetope':
        if addr not in self.nodes.keys():
            raise DerivationError(
                "Preopetope source",
                "Address {addr} not in preopetope {this}",
                addr = str(addr), this = str(self))
        return self.nodes[addr]

    @staticmethod
    def substitution(p: 'Preopetope', addr: Address, ctx: Context,
                     q: 'Preopetope'):
        """
        In the :math:`n`-preopetope ``p``, substitute the source at address
        ``addr`` by the :math:`(n-1)`-preopetope ``q``. The context ``ctx``
        must be defined on all leaves of ``q`` (see
        :meth:`UnnamedOpetope.Context.__call__`).
        """
        for leaf in q.leafAddresses():
            if not ctx.definedOnLeaf(leaf):
                raise DerivationError(
                    "Preopetope substitution",
                    "Cannot substitute with {q} in {p} as ambient context "
                    "{ctx} is not defined on leaf {leaf}",
                    p = str(p), q = str(q), ctx = str(ctx), leaf = str(leaf))
        if addr not in p.nodeAddresses():
            raise DerivationError(
                "Preopetope substitution",
                "Cannot substitute in {p} at address {addr} as it is not in "
                "the preopetope",
                p = str(p), addr = str(addr))
        elif addr.dimension + 1 != q.dimension:
            raise DerivationError(
                "Preopetope substitution",
                "Cannot substitute with {q} in {p} as dimensions mismatch "
                "(the former has dimension {qd}, should have {pd}",
                p = str(p), q = str(q), pd = p.dimension, qd = q.dimension)

        if q.isDegenerate:

            if len(p.nodeAddresses()) == 1:  # if p has only one node
                return q
            else:  # otherwise, the node at addr must be globular
                r = Preopetope(p.dimension)
                for a in p.nodeAddresses():
                    r += (
                        Address.substitution(
                            a,
                            addr + Address.epsilon(p.dimension - 2),
                            addr
                        ),
                        p.source(a)
                    )
                return r

        else:

            r = Preopetope(p.dimension)
            for a in q.nodeAddresses():  # adding nodes of q
                r += (addr * a, q.source(a))
            for a in (p - addr).nodeAddresses():  # adding nodes of p
                b = a
                for l in ctx.leaves():
                    c = Address.substitution(a, addr + ctx(l), addr * l)
                    if c != a:
                        b = c
                        break
                r += (b, p.source(a))
            return r

    def toDict(self) -> Dict[Optional[Address], Dict]:
        """
        Transforms the current preopetope into a ``dict``.
        """
        if self.isDegenerate:
            if self.degeneracy is None:
                raise RuntimeError(
                    "Preopetope, to dict",
                    "Preopetope is degenerate but doesn't have any "
                    "degeneracy. In valid derivations, this should not happen")
            return {None: self.degeneracy.toDict()}
        else:
            if self.nodes is None:
                raise RuntimeError(
                    "Preopetope, to dict",
                    "Preopetope is not degenerate but doesn't have any "
                    "node dict. In valid derivations, this should not happen")
            res = {}  # type: Dict[Optional[Address], Dict]
            for addr in self.nodes.keys():
                res[addr] = self.nodes[addr].toDict()
            return res

    def toTex(self) -> str:
        """
        Converts the preopetope to TeX code.
        """
        if self.dimension == -1:
            return "\\emptyset"
        elif self.dimension == 0:
            return "\\optZero"
        elif self == Preopetope.fromDictOfPreopetopes({
                Address.epsilon(0): Preopetope.point()}):
            return "\\optOne"
        elif self.isDegenerate:
            if self.degeneracy is None:
                raise RuntimeError("[Preopetope, toTex] Preopetope marked "
                                   "degenerate but the underlying preopetope "
                                   "is undefined. In valid proof trees, this "
                                   "should not happen")
            return "\\degenopetope{" + self.degeneracy.toTex() + "}"
        else:
            res = [x.toTex() + " \\sep " + self.nodes[x].toTex()
                   for x in sorted(self.nodes)]
            return "\\opetope{" + " \\\\ ".join(res) + "}"


class Sequent:
    """
    A sequent is a triple consisting of an :math:`n`-context, a source
    :math:`n`-preopetope, and a target :math:`(n-1)`-preopetope.
    """

    context: Context
    source: Preopetope
    target: Preopetope

    def __init__(self, ctx: Context, s: Preopetope, t: Preopetope) -> None:
        """
        Creates a sequent from an :math:`n`-context ``ctx``, an
        :math:`n`-preopetope ``s``, and an :math:`(n-1)`-preopetope ``t``.
        """
        if not (ctx.dimension == s.dimension and
                s.dimension == t.dimension + 1):
            raise DerivationError(
                "Sequent creation",
                "Dimension mismatch between the context, source, and target "
                "(are respectively {cd}, {sd}, and {td}): the context and "
                "should have the same dimension, while the target should have "
                "1 less",
                cd = ctx.dimension, sd = s.dimension, td = t.dimension)
        self.context = ctx
        self.source = s
        self.target = t

    def __eq__(self, other) -> bool:
        if not isinstance(other, Sequent):
            raise NotImplementedError
        else:
            return self.context == other.context and \
                self.source == other.source and \
                self.target == other.target

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Converts a sequent to a human readable string.
        """
        return "ctx = {ctx}\nsrc = {src}\ntgt = {tgt}".format(
            ctx = self.context,
            src = self.source,
            tgt = self.target
        )

    def toTex(self) -> str:
        return self.context.toTex() + " \\vdash " + self.source.toTex() + \
            " \\longrightarrow " + self.target.toTex()


def point() -> Sequent:
    """
    The :math:`\\textbf{Opt${}^?$}` :math:`\\texttt{point}` rule.
    Create the unique :math:`0`-opetope with no premises.
    """
    return Sequent(Context(0), Preopetope.point(), Preopetope.empty())


def degen(seq: Sequent) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^?$}` :math:`\\texttt{degen}` rule.
    From an :math:`n`-opetope :math:`\\omega`, creates the
    degenerate :math:`(n+2)`-opetope :math:`\\lbrace \\lbrace \\omega`.
    """
    n = seq.source.dimension
    return Sequent(
        Context(n + 2) + (Address.epsilon(n + 1), Address.epsilon(n)),
        Preopetope.degenerate(seq.source),
        Preopetope.fromDictOfPreopetopes({
            Address.epsilon(n): seq.source
        })
    )


def shift(seq: Sequent) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^?$}` :math:`\\texttt{shift}` rule.
    From an :math:`n`-opetope :math:`\\omega`, creates the
    globular :math:`(n+1)`-opetope
    :math:`\\lbrace []: \\omega`.
    """
    n = seq.source.dimension
    ctx = Context(n + 1)
    for a in seq.source.nodeAddresses():
        ctx += (a.shift(), a)

    return Sequent(
        ctx,
        Preopetope.fromDictOfPreopetopes({
            Address.epsilon(n): seq.source
        }),
        seq.source
    )


def graft(seq1: Sequent, seq2: Sequent, addr: Address) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^?$}` :math:`\\texttt{graft}` rule.
    From an :math:`n`-opetope :math:`\\omega` (in sequent
    ``seq1``), an :math:`(n-1)`-opetope :math:`\\psi` (in sequent ``seq2``),
    and a leaf of :math:`\\omega`, creates the opetope
    :math:`\\omega \\circ_{\\mathrm{addr}} \\mathsf{Y}_{\\psi}`.
    """
    r = seq1.context(addr)

    ctx = Context(seq1.context.dimension)
    for a in seq2.source.nodeAddresses():
        ctx += (addr + a, r * a)
    for a in (seq1.context - addr).leaves():
        b = seq1.context(a)
        for x in seq2.context.leaves():
            y = seq2.context(x)
            c = Address.substitution(b, r + y, r * x)
            if b != c:
                b = c
                break
        ctx += (a, b)

    return Sequent(
        ctx,
        Preopetope.improperGrafting(seq1.source, addr, seq2.source),
        Preopetope.substitution(
            seq1.target,
            r,
            seq2.context,
            seq2.source
        )
    )


class RuleInstance(AbstractRuleInstance):
    """
    A rule instance of system :math:`\\textbf{Opt${}^?$}`.
    """

    def eval(self) -> Sequent:
        """
        Pure virtual method evaluating a proof tree and returning the final
        conclusion sequent, or raising an exception if the proof is invalid.
        """
        raise NotImplementedError()


class Point(RuleInstance):
    """
    A class representing an instance of the ``point`` rule in a proof tree.
    """

    def __repr__(self):
        return "Point()"

    def __str__(self):
        return "Point()"

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetope.RuleInstance.toTex`
        instead.
        """
        return "\\AxiomC{}\n\t\\RightLabel{\\texttt{point}}\n\t" + \
            "\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree, in this cases returns the point sequent by
        calling :func:`UnnamedOpetope.point`.
        """
        return point()


class Degen(RuleInstance):
    """
    A class representing an instance of the ``degen`` rule in a proof tree.
    """

    proofTree: RuleInstance

    def __init__(self, p: RuleInstance) -> None:
        """
        Creates an instance of the ``degen`` rule and plugs proof tree ``p``
        on the unique premise.
        """
        self.proofTree = p

    def __repr__(self):
        return "Degen({})".format(repr(self.proofTree))

    def __str__(self):
        return "Degen({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{degen}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates this instance of ``degen`` by first evaluating its premise,
        and then applying :func:`UnnamedOpetope.degen` on the resulting
        sequent.
        """
        return degen(self.proofTree.eval())


class Shift(RuleInstance):
    """
    A class representing an instance of the ``shift`` rule in a proof tree.
    """

    proofTree: RuleInstance

    def __init__(self, p: RuleInstance) -> None:
        """
        Creates an instance of the ``shift`` rule and plugs proof tree ``p``
        on the unique premise.
        """
        self.proofTree = p

    def __repr__(self):
        return "Shift({})".format(repr(self.proofTree))

    def __str__(self):
        return "Shift({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{shift}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates this instance of ``shift`` by first evaluating its premise,
        and then applying :func:`UnnamedOpetope.shift` on the resulting
        sequent.
        """
        return shift(self.proofTree.eval())


class Graft(RuleInstance):
    """
    A class representing an instance of the ``graft`` rule in a proof tree.
    """

    proofTree1: RuleInstance
    proofTree2: RuleInstance

    def __init__(self, p1: RuleInstance, p2: RuleInstance,
                 addr: Address) -> None:
        """
        Creates an instance of the ``graft`` rule at address ``addr``, and
        plugs proof tree ``p1`` on the first premise, and ``p2`` on the second.
        Recall that the opetope described in the second premise will be
        impropely grafted on that of the first. See
        :func:`UnnamedOpetope.graft`.
        """
        self.proofTree1 = p1
        self.proofTree2 = p2
        self.addr = addr

    def __repr__(self):
        return "Graft({p1}, {p2}, {addr})".format(p1 = repr(self.proofTree1),
                                                  p2 = repr(self.proofTree2),
                                                  addr = repr(self.addr))

    def __str__(self):
        return "Graft({p1}, {p2}, {addr})".format(p1 = str(self.proofTree1),
                                                  p2 = str(self.proofTree2),
                                                  addr = str(self.addr))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`UnnamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree1._toTex() + "\n\t" + self.proofTree2._toTex() + \
            "\n\t\\RightLabel{\\texttt{graft-}$" + self.addr.toTex() + \
            "$}\n\t\\BinaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates this instance of ``graft`` by first evaluating its premises,
        and then applying :func:`UnnamedOpetope.graft` at address
        `self.addr` on the resulting sequents.
        """
        return graft(self.proofTree1.eval(), self.proofTree2.eval(),
                     self.addr)


def address(lst: Union[List[Any], str], dim: Optional[int] = None) -> Address:
    """
    Similar to :meth:`Address.fromList`, except the name is shorter, and
    the dimension is inferred if possible. Otherwise, an exception is thrown.
    Here are some examples:

    >>> address('*')
    Address(*, 0)

    >>> address([['*'], [], ['*', '*']])
    Address([[*][][**]], 2)

    """
    def dimension(k: Any) -> Optional[int]:
        """
        Tries to infer the dimension.
        """
        if k == []:
            return None
        elif k == '*':
            return 0
        elif isinstance(k, list):
            i = None  # type: Optional[int]
            for a in k:
                j = dimension(a)
                if i is None:
                    i = j
                elif j is not None and i != j:  # Contradictory dim inferrences
                    return None
            if i is None:
                return None
            else:
                return i + 1
        else:
            raise NotImplementedError("[Address from list] Incompatible type: "
                                      "a list representation of an address "
                                      "(LA) for short, is either the string "
                                      "'*', or a list of LA")
    if isinstance(lst, str):
        if lst == '*':
            return Address.epsilon(0)
        else:
            raise DerivationError(
                "Address from list",
                "The following expression does not represent an address: "
                "{lst}",
                lst = lst)
    elif dim is not None:
        return Address.fromList(lst, dim)
    d = dimension(lst)
    if d is None:
        raise DerivationError(
            "Address from list",
            "Cannot infer dimension of list {lst}",
            lst = lst)
    else:
        return Address.fromList(lst, d)


def Arrow() -> RuleInstance:
    """
    Returns the proof tree of the arrow.
    """
    return Shift(Point())


def OpetopicInteger(n: int) -> RuleInstance:
    """
    Returns the sequent nth opetopic integer.
    """
    if n < 0:
        raise DerivationError(
            "Opetopic integer",
            "Argument is expected to be >= 0")
    elif n == 0:
        return Degen(Point())
    elif n == 1:
        return Shift(Arrow())
    else:
        return Graft(OpetopicInteger(n - 1), Arrow(), address(['*'] * (n - 1)))


def OpetopicTree(tree: Optional[List[Any]]) -> RuleInstance:
    """
    Returns the proof tree of the :math:`3`-opetope corresponding to a tree.
    The tree is expressed as a recursive list. For instance,
    ``[None, [[None], None], None, None]`` corresponds to
    :math:`\\mathsf{Y}_{\\mathbf{4}} \\circ_{[[*]]} \\left(
    \\mathsf{Y}_{\\mathbf{2}} \\circ_{[]} \\mathsf{Y}_{\\mathbf{1}} \\right)`
    while ``None`` corresponds to the degenerate opetope at the arrow.
    """
    def toDict(lst: Optional[List[Any]]) -> Dict[Address, RuleInstance]:
        if lst is None:
            return {}
        else:
            res = {
                address([], 2): OpetopicInteger(len(lst))
            }  # type: Dict[Address, RuleInstance]
            for i in range(len(lst)):
                if lst[i] is not None and not isinstance(lst[i], list):
                    raise DerivationError(
                        "Opetopic tree",
                        "A tree is expected to be either none or a list of "
                        "trees")
                d = toDict(lst[i])
                for a in d.keys():
                    res[address([['*'] * i], 2) * a] = d[a]
            return res
    if tree is None:
        return Degen(Arrow())
    else:
        d = toDict(tree)
        sa = sorted(d.keys())
        res = Shift(d[address([], 2)])  # type: RuleInstance
        for i in range(1, len(sa)):
            res = Graft(res, d[sa[i]], sa[i])
        return res


def ProofTree(p: Dict[Optional[Address], Dict]) -> RuleInstance:
    """
    Returns the proof tree of a preopetope described as a dict, or raises a
    :class:`common.DerivationError` if the preopetope is not an opetope. For
    ``T`` the type of the argument, ``T`` is a ``dict`` mapping
    :class:`UnnamedOpetope.Address` or ``None`` to instances of ``T``.
    For example,

    .. code-block:: python

        {
            address([], 1): {
                address('*'): {}
            },
            address(['*']): {
                address('*'): {}
            },
            address(['*', '*']): {
                address('*'): {}
            }
        }

    corresponds to the opetopic integer :math:`\\mathbf{3}`, while

    .. code-block:: python

        {
            None: {
                address('*'): {}
            }
        }

    is the :math:`3`-opetope degenerate at the arrow (the ``None`` indicates a
    degeneracy).
    """
    if p == {}:
        return Point()
    a = list(p.keys())[0]
    if a is None:
        if len(p.keys()) != 1:
            raise DerivationError(
                "Proof tree of a preopetope",
                "Argument is not an opetope: containes address None "
                "indicating it is degenerate, but also other addresses. {p}",
                p = p)
        else:
            return Degen(ProofTree(p[None]))
    else:
        sa = sorted([x for x in p.keys() if x is not None])  # for typechecker
        if sa[0] != Address.epsilon(a.dimension):
            raise DerivationError(
                "Proof tree of a preopetope",
                "Argument is not an opetope: doesn't contain address {e}. {p}",
                e = Address.epsilon(a.dimension), p = p)
        res = Shift(ProofTree(p[sa[0]]))  # type: RuleInstance
        for i in range(1, len(sa)):
            res = Graft(res, ProofTree(p[sa[i]]), sa[i])
        res.eval()
        return res
