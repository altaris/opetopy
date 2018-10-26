# -*- coding: utf-8 -*-

"""
.. module:: opetopy.NamedOpetope
   :synopsis: Implementation of the named approach
              for opetopes

.. moduleauthor:: Cédric HT

"""

from copy import deepcopy
from typing import ClassVar, Dict, List, Optional, Set, Tuple, Union

from common import *


class Variable:
    """
    A variable is just a string representing its name, annotated by an integer
    representing its dimension.
    """

    dimension: int
    name: str

    def __eq__(self, other) -> bool:
        """
        Tests syntactic equality between two variables. Two variables are equal
        if they have the same dimension and the same name.
        """
        if not isinstance(other, Variable):
            raise NotImplementedError
        return self.name == other.name and self.dimension == other.dimension

    def __hash__(self):
        """
        Return a hash of the variable. This is for Python purposes.
        """
        return self.name.__hash__()

    def __init__(self, name: str, dim: int) -> None:
        if dim < 0 and name is not None:
            raise DerivationError(
                "Variable decrlaration",
                "Dimension of new variable {name} must be >= 0 (is {dim})",
                name = name, dim = dim)
        self.dimension = dim
        self.name = name

    def __ne__(self, other) -> bool:
        if not isinstance(other, Variable):
            raise NotImplementedError
        return not (self == other)

    def __repr__(self) -> str:
        return "{name}{dim}".format(name = self.name, dim = self.dimension)

    def __str__(self) -> str:
        return self.name

    def toTex(self) -> str:
        """
        Returns the string representation of the variable, which is really just
        the variable name.
        """
        return self.name


class Term(Dict[Variable, 'Term']):
    """
    An :math:`n`-term is represented as follows:

    * If it is degenerate, then the boolean attribute
      :py:attr:`NamedOpetope.Term.degenerate` is set to ``True``, and
      :py:attr:`NamedOpetope.Term.variable` is set to the variable name of
      which the current term is the degeneracy.
    * If it is non degenerate, then the boolean attribute
      :py:attr:`NamedOpetope.Term.degenerate` is set to ``False``,
      :py:attr:`NamedOpetope.Term.variable` is set to the variable name of
      the root node, and this class is otherwise used as a ``dict`` mapping
      :math:`(n-1)`-variables in the source to other :math:`n`-terms.
    """

    degenerate: bool
    variable: Optional[Variable]

    def __contains__(self, var) -> bool:
        """
        Checks if a variable is in the term.

        If the term is degenerate, always return ``False``. Otherwise, assume
        the term has dimension :math:`n`.

        * If the variable has dimension :math:`(n-1)`, then it checks against
          all keys in the underlying ``dict`` and if not found, calls the
          method recursively on all values of the underlying ``dict`` (which by
          construction are also :math:`n`-terms).
        * If the variable has :math:`n`, then it compares it to the root node
          (:py:attr:`NamedOpetope.Term.variable`), and if not equal, calls
          the method recursively on all values of the underlying ``dict``
          (which by construction are also :math:`n`-terms).
        """
        if not isinstance(var, Variable):
            raise NotImplementedError
        elif self.degenerate:
            return False
        elif var.dimension == self.dimension - 1:
            if var in self.keys():
                return True
            else:
                for t in self.values():
                    if var in t:
                        return True
                return False
        elif var.dimension == self.dimension:
            if var == self.variable:
                return True
            else:
                for t in self.values():
                    if var in t:
                        return True
                return False
        else:
            return False

    def __eq__(self, other) -> bool:
        """
        Tests if two terms are syntactically equal.
        """
        if not isinstance(other, Term):
            raise NotImplementedError
        elif self.variable is None and other.variable is None:
            return True
        elif self.variable != other.variable or \
                self.degenerate != other.degenerate:
            return False
        elif len(self.keys()) == len(other.keys()):
            for k in self.keys():
                if k not in other.keys() or self[k] != other[k]:
                    return False
            return True
        else:
            return False

    def __init__(self, var: Optional[Variable] = None,
                 degen: bool = False) -> None:
        """
        Creates a term from a :class:`NamedOpetope.Variable` ``var``.
        If it is ``None`` (default), then this term represents the unique
        :math:`(-1)`-term.
        """
        self.degenerate = degen
        self.variable = var

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.dimension == -1:
            return "∅"
        elif self.degenerate:
            return "_" + str(self.variable)
        elif len(self.keys()) == 0:
            return str(self.variable)
        else:
            grafts = [str(k) + " ← " + str(self[k])
                      for k in self.keys()]
            return str(self.variable) + "(" + ", ".join(grafts) + ")"

    @property
    def dimension(self) -> int:
        """
        Returns the dimension of the term. If its
        :py:attr:`NamedOpetope.Term.variable` is ``None``, then it is
        :math:`-1` by convention. If it is degenerate, then it is the dimension
        of :py:attr:`NamedOpetope.Term.variable` :math:`+1`, otherwise just
        the dimension of :py:attr:`NamedOpetope.Term.variable`.
        """
        if self.variable is None:
            return -1
        elif self.degenerate:
            return self.variable.dimension + 1
        else:
            return self.variable.dimension

    def graftTuples(self) -> Set[Tuple[Variable, Variable]]:
        """
        This helper function constructs the set of tuples (b, a) for all
        variables a and b such that the expression
        :math:`b \\leftarrow a (\\ldots)` occurs in the term.
        """
        res = set()  # type: Set[Tuple[Variable, Variable]]
        for k in self.keys():
            if not self[k].degenerate:
                a = self[k].variable
                if a is None:
                    raise RuntimeError(
                        "[Term, graftTuples] An invalid / null term has been "
                        "grafted at variable {var} in term {term}. In valid "
                        "proof trees, this should not happen"
                        .format(var = str(k), term = str(self)))
                res |= set({(k, a)}) | self[k].graftTuples()
        return res

    def isVariable(self) -> bool:
        """
        Tells wether this term is in fact just a variable.
        """
        return self.variable is not None and not self.degenerate \
            and len(self.keys()) == 0

    def toTex(self) -> str:
        """
        Converts the term to TeX code.
        """
        if self.dimension == -1 or self.variable is None:
            return "\\emptyset"
        elif self.degenerate:
            return "\\underline{" + self.variable.toTex() + "}"
        elif len(self.keys()) == 0:
            return self.variable.toTex()
        else:
            grafts = [k.toTex() + " \\leftarrow " + self[k].toTex()
                      for k in self.keys()]
            return self.variable.toTex() + "(" + ", ".join(grafts) + ")"

    def variables(self, k) -> Set[Variable]:
        """
        Returns the set of all :math:`k` variables contained in the term. Note
        that degenerate terms don't containe any variables.

        :see: :meth:`NamedOpetope.Term.__contains__`
        """
        if self.degenerate or self.variable is None:
            return set()
        else:
            res = set()  # type: Set[Variable]
            if self.variable.dimension == k:
                res |= {self.variable}
            for a in self.keys():
                if a.dimension == k:
                    res |= {a}
                res |= self[a].variables(k)
            return res


class Type:
    """
    An :math:`n`-type is a sequence of :math:`(n+1)` terms of dimension
    :math:`(n-1), (n-2), \\ldots, -1`.

    """

    dimension: int
    terms: List[Term]

    def __contains__(self, var) -> bool:
        """
        Checks wether a given variable appears in at least one term of the
        type.
        """
        if not isinstance(var, Variable):
            raise NotImplementedError
        for t in self.terms:
            if var in t:
                return True
        return False

    def __init__(self, terms: List[Term]) -> None:
        """
        Creates a new type from a list of term. The dimension is inferred from
        the length of the list, and the terms are checked to have the correct
        dimension.

        If the list has length :math:`(n+1)`, then the type's dimension will be
        :math:`n`, and the dimension of the :math:`i` th term in the list must
        be :math:`n - i - 1` (recall that Python index start at :math:`0`,
        whence the :math:`-1` correction factor).
        """
        if len(terms) < 1:
            raise DerivationError(
                "Type declaration",
                "A type requires at least one term")
        self.dimension = len(terms) - 1
        self.terms = terms
        for i in range(len(self.terms)):
            if self.terms[i].dimension != self.dimension - i - 1:
                raise DerivationError(
                    "Type declaration",
                    "Invalid dimensions in term list: {i}th term {term} has "
                    "dimension {dim}, sould have {should}",
                    i = i, term = str(self.terms[i]),
                    dim = self.terms[i].dimension,
                    should = self.dimension - i - 1)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return " ⊷ ".join([str(t) for t in self.terms])

    def toTex(self) -> str:
        """
        Converts the type to TeX code.
        """
        return " \\blackwhitespoon ".join([t.toTex() for t in self.terms])

    def variables(self, k: int) -> Set[Variable]:
        """
        Returns the set of all :math:`k` variables contained in the terms of
        the type. Note that degenerate terms don't containe any variables.

        :see: :meth:`NamedOpetope.Term.__contains__`
        :see: :meth:`NamedOpetope.Term.variables`
        """
        res = set()  # type: Set[Variable]
        for t in self.terms:
            res |= t.variables(k)
        return res


class Typing:
    """
    A typing is simply an :math:`n`-term (:class:`NamedOpetope.Term`)
     together with an :math:`n`-type (:class:`NamedOpetope.Type`).

    """

    term: Term
    type: Type

    def __hash__(self):
        return self.toTex().__hash__()

    def __init__(self, term, type) -> None:
        if term.dimension != type.dimension:
            raise DerivationError(
                "Typing declaration",
                "Dimension mismatch in typing: term has dimension {dterm}, "
                "type has dimension {dtype}",
                dterm = term.dimension, dtype = type.dimension)
        self.term = term
        self.type = type

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.term) + " : " + str(self.type)

    def toTex(self) -> str:
        return self.term.toTex() + " : " + self.type.toTex()


class Context(Set[Typing]):
    """
    A context is a set of tyings (see :class:`NamedOpetope.Typing`).
    """

    def __add__(self, typing: Typing) -> 'Context':
        """
        Adds a variable typing to a deep copy of the context context, if the
        typed  variable isn't already typed in the context.
        """
        if not typing.term.isVariable():
            raise DerivationError(
                "Context, new typing",
                "Context typings only type variables, and {term} is not one",
                term = str(typing.term))
        elif typing.term.variable in self:
            raise DerivationError(
                "Context, new typing",
                "Variable {var} is already yped in this context",
                var = str(typing.term.variable))
        else:
            res = deepcopy(self)
            res.add(typing)
            return res

    def __and__(self, other) -> 'Context':
        """
        Returns the intersection of two contexts, i.e. the set of typings of
        the first context whose typed variable is in the second
        """
        res = Context()
        for typing in self:
            if typing.term.variable in other:
                res += typing
        return res

    def __contains__(self, var) -> bool:
        """
        Tests wether the variable ``var`` is typed in this context.
        """
        if not isinstance(var, Variable):
            raise NotImplementedError
        for typing in self:
            if Term(var) == typing.term:
                return True
        return False

    def __getitem__(self, name: str) -> Variable:
        """
        Returns the varible term in current context whose name is ``name``.
        """
        for typing in self:
            if typing.term.isVariable and \
                    typing.term.variable is not None and \
                    typing.term.variable.name == name:
                return typing.term.variable
        raise DerivationError(
            "Context, get variable",
            "Context types no variable named {name}",
            name = name)

    def __or__(self, other):
        """
        Returns the union of two compatible contexts.
        """
        res = deepcopy(self)
        for t in other:
            if t.term.variable not in res:
                res += t
        return res

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ", ".join([str(t) for t in self])

    def graftTuples(self) -> Set[Tuple[Variable, Variable]]:
        """
        Returns all tuples (b, a) for :math:`b \\leftarrow a (\\ldots)` a
        grafting occurring in a term in a type in the context.

        :see: :meth:`NamedOpetope.Term.graftTuples`
        :see: :func:`NamedOpetopicSet.repres`
        """
        res = set()  # type: Set[Tuple[Variable, Variable]]
        for typing in self:
            for t in typing.type.terms:
                res |= t.graftTuples()
        return res

    def source(self, var: Variable, k: int = 1) -> Term:
        """
        Returns the :mathm``k``-source of a variable.
        """
        if k < 0 or k > var.dimension + 1:
            raise DerivationError(
                "Context, source computation",
                "Index out of bounds: dimension of variable {var} is {dim}, "
                "so index should be between 0 and {max} included "
                "(is {k})",
                var = str(var), dim = var.dimension,
                max = var.dimension + 1, k = k)
        elif var not in self:
            raise DerivationError(
                "Context, source computation",
                "Variable {var} with dimension {dim} is not typed in context, "
                "so computing its source is not possible",
                var = str(var), dim = var.dimension)
        elif k == 0:
            return Term(var)
        else:
            return self.typeOf(var).terms[k - 1]

    def toTex(self) -> str:
        """
        Converts the type to TeX code.
        """
        return ", ".join([t.toTex() for t in self])

    def typeOf(self, var: Variable) -> Type:
        """
        Returns the type of a variable.
        """
        for typing in self:
            if typing.term == Term(var):
                return typing.type
        raise DerivationError(
            "Context, type computation",
            "Variable {var} with dimension {dim} is not typed in context, so "
            "computing its type is not possible",
            var = str(var), dim = var.dimension)

    def variables(self) -> Set[Variable]:
        """
        Return the set of all variables typed in the context.
        """
        return set([typing.term.variable for typing in self
                    if typing.term.variable is not None])


class EquationalTheory:
    """
    An equational theory (among variables), is here represented as a partition
    of a subset of the set of all variables. Is is thus a list of sets of
    variables. (set of sets isn't possible as python ``set`` isn't hashable)
    """

    classes: List[Set[Variable]]

    def __add__(self, eq: Tuple[Variable, Variable]) -> 'EquationalTheory':
        """
        Adds an equality (represented by a tuple of two
        :class:`NamedOpetope.Variable`) to the theory.
        """
        a, b = eq
        if a.dimension != b.dimension:
            raise DerivationError(
                "Eq. th. extension",
                "Dimension mismatch in new equality {a} = {b}: respective "
                "dimensions are {da} and {db}",
                a = str(a), b = str(b), da = a.dimension, db = b.dimension)
        else:
            ia = self._index(a)
            ib = self._index(b)
            res = deepcopy(self)
            if ia == -1 and ib == -1:       # Neither a nor b are in a class
                res.classes += [set({a, b})]
            elif ia == -1 and ib != -1:     # b is in a class but not a
                res.classes[ib].add(a)
            elif ia != -1 and ib == -1:     # a is in a class but not b
                res.classes[ia].add(b)
            elif ia != ib:                  # a and b are in different classes
                res.classes[ia] |= res.classes[ib]
                del res.classes[ib]
            return res

    def __init__(self) -> None:
        self.classes = []

    def __or__(self, other: 'EquationalTheory') -> 'EquationalTheory':
        """
        Returns the union of two equational theories
        """
        res = deepcopy(self)
        for cls in other.classes:
            lcls = list(cls)
            for i in range(1, len(lcls)):
                res += (lcls[0], lcls[i])
        return res

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        cls = ["{" + ", ".join([str(x) for x in c]) + "}"
               for c in self.classes]
        return ", ".join(cls)

    def _index(self, a: Variable) -> int:
        """
        Returns the index (in
        :py:attr:`NamedOpetope.EquationalTheory.classes`)
        of the class of the variable ``a``, or `-1` of the class doesn't exist.
        """
        for i in range(len(self.classes)):
            if a in self.classes[i]:
                return i
        return -1

    def classOf(self, a: Variable) -> Set[Variable]:
        """
        Returns the class of a variable.
        """
        ia = self._index(a)
        if ia == -1:
            return set({a})
        else:
            return self.classes[ia]

    def equal(self, a: Variable, b: Variable) -> bool:
        """
        Tells wether variables (:class:`NamedOpetope.Variable`)
        ``a`` and ``b`` are equal modulo the equational theory.
        """
        ia = self._index(a)
        if ia == -1:
            return a == b
        else:
            return b in self.classes[ia]

    def isIn(self, var: Variable, term: Term) -> bool:
        """
        Tells wether a variable is in a term modulo the equational theory of
        the sequent.

        :see: :meth:`NamedOpetope.Term.__contains__`.
        """
        for v in self.classOf(var):
            if v in term:
                return True
        return False

    def toTex(self) -> str:
        cls = ["\\left\\{" + ", ".join([x.toTex() for x in c]) +
               "\\right\\}" for c in self.classes]
        return ", ".join(cls)


class OCMT:
    """
    Opetopic context modulo theory. Basically the same as a
    :class:`NamedOpetope.Sequent`, without the typing.
    """

    theory: EquationalTheory
    context: Context

    targetSymbol: str = "t"

    def __init__(self, theory: EquationalTheory, context: Context) -> None:
        self.context = context
        self.theory = theory

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "{th} ▷ {ctx}".format(th = str(self.theory),
                                     ctx = str(self.context))

    def equal(self, t: Term, u: Term) -> bool:
        """
        Tells wether two terms ``t`` and ``u`` are equal modulo the equational
        theory.

        :see: Similar method for variables only:
          :meth:`NamedOpetope.EquationalTheory.equal`
        """
        if t.variable is None or u.variable is None:
            if t.variable is not None or u.variable is not None:
                return False
            return True
        elif t.degenerate != u.degenerate:
            return False
        elif not self.theory.equal(t.variable, u.variable):
            return False
        elif len(t.keys()) != len(u.keys()):
            return False
        else:
            for kt in t.keys():
                ku = None
                for l in u.keys():
                    if self.theory.equal(kt, l):
                        ku = l
                        break
                if ku is None:
                    return False
                elif not self.equal(t[kt], u[ku]):
                    return False
            return True

    def isIn(self, var: Variable, term: Term) -> bool:
        """
        Tells wether a variable is in a term modulo the equational theory of
        the sequent.

        :see: :meth:`NamedOpetope.EquationalTheory.isIn`
        :see: :meth:`NamedOpetope.Term.__contains__`
        """
        return self.theory.isIn(var, term)

    def source(self, var: Variable, k: int = 1) -> Term:
        """
        Returns the :mathm``k``-source of a variable.

        :see: :meth:`NamedOpetope.Context.source`
        """
        return self.context.source(var, k)

    def target(self, var: Variable, k: int = 1) -> Variable:
        """
        Returns the :math:`k` target of a variable.
        """
        if var.dimension == 0:
            raise DerivationError(
                "OCMT, target computation",
                "Cannot compute target of 0-dimensional variable {var}",
                var = str(var))
        else:
            return Variable((OCMT.targetSymbol * k) + var.name,
                            var.dimension - k)

    def toTex(self) -> str:
        return self.theory.toTex() + " \\smalltriangleright " + \
            self.context.toTex()

    def typeOf(self, var: Variable) -> Type:
        """
        Returns the type of a variable.

        :see: :meth:`NamedOpetope.Context.typeOf`
        """
        return self.context.typeOf(var)


class Sequent(OCMT):
    """
    A sequent consists of an equational theory
    (:class:`NamedOpetope.EquationalTheory`), a context
    (:class:`NamedOpetope.Context`), and a typing
    (:class:`NamedOpetope.Typing`).
    """

    typing: Typing

    """
    This variable specifies if contexts should be displayed in
    :meth:`NamedOpetope.Sequent.toTex`
    """
    texContexts: ClassVar[bool] = True

    def __init__(self, theory: EquationalTheory, context: Context,
                 typing: Typing) -> None:
        super().__init__(theory, context)
        self.typing = typing

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "{th} ▷ {ctx} ⊢ {typ}".format(th = str(self.theory),
                                             ctx = str(self.context),
                                             typ = str(self.typing))

    def graft(self, t: Term, x: Variable, u: Term) -> Term:
        """
        Grafts term (:class:`NamedOpetope.Term`) u on term t via
        variable (:class:`NamedOpetope.Variable`) x. In other words,
        computes :math:`t(x \\leftarrow u)`.
        """
        for k in t.keys():
            if self.theory.equal(k, x):
                raise DerivationError(
                    "Sequent, grafting",
                    "Variable {var} in term {term} has already been used for "
                    "a grafting",
                    var = str(x), term = str(t))
        if t.variable is None:
            raise DerivationError(
                "Sequent, grafting",
                "Term to be grafted onto is empty")
        elif t.degenerate:
            if t.variable == x:
                return deepcopy(u)
            else:
                raise DerivationError(
                    "Sequent, grafting",
                    "Incompatible graft: term {term} is degenerate, so the "
                    "grafting variable must be {var} (is {x})",
                    term = str(t), var = str(t.variable), x = str(x))
        else:
            r = deepcopy(t)
            if self.isIn(x, self.source(t.variable, 1)):
                r[x] = u
            else:
                for k in r.keys():
                    r[k] = self.graft(r[k], x, u)
            return r

    def substitute(self, u: Term, s: Term, a: Variable) -> \
            Tuple[Term, Optional[Tuple[Variable, Variable]]]:
        """
        Substitute term (:class:`NamedOpetope.Term`) ``s`` for variable
        (:class:`NamedOpetope.Variable`) ``a`` in term ``u``. In other
        words, computes :math:`u[s/a]`.

        Returns a tuple containing

        1. the resulting substitution
        2. an new equality to add to the equational theory, or ``None``
        """
        if s.variable is None:
            raise DerivationError(
                "Sequent, substitute",
                "Cannot substitute in the null term")
        elif u.variable is None:
            raise DerivationError(
                "Sequent, substitute",
                "Cannot substitute with the null term")
        elif s.degenerate:
            if a in [v.variable for v in u.values()]:
                # a appears grafted on the root of u
                # ta = None  # Term grafted in the root of u whose root is a
                # ka = None  # Key of ta
                for k in u.keys():
                    if u[k].variable == a:
                        ta = u[k]
                        ka = k
                        break
                if len(ta.keys()) == 0:  # ta is just the variable a
                    r = deepcopy(u)
                    del r[ka]
                    return (r, (s.variable, ka))
                else:  # ta has graftings on its root a
                    if len(ta.values()) != 1:  # that grafting should be unique
                        assert RuntimeError("[Sequent, substitution] Term "
                                            "{term} was expected to be "
                                            "globular... In valid proof "
                                            "trees, this error shouldn't "
                                            "happen, so congratulations, "
                                            "you broke everything"
                                            .format(term = repr(ta)))
                    r = deepcopy(u)
                    r[ka] = list(ta.values())[0]
                    return (r, (s.variable, ka))
            else:
                r = deepcopy(u)
                e = None
                for k in r.keys():
                    r[k], f = self.substitute(r[k], s, a)
                    if f is not None:
                        e = f
                return (r, e)
        else:
            if self.theory.equal(u.variable, a):
                r = deepcopy(s)
                for k in u.keys():
                    r = self.graft(r, k, u[k])
                return (r, None)
            else:
                r = deepcopy(u)
                for k in r.keys():
                    r[k] = self.substitute(r[k], s, a)[0]
                return (r, None)

    def toTex(self) -> str:
        if Sequent.texContexts:
            return self.theory.toTex() + " \\smalltriangleright " + \
                self.context.toTex() + \
                " \\vdash_{" + str(self.typing.term.dimension) + "} " + \
                self.typing.toTex()
        else:
            return self.theory.toTex() + " \\vdash_{" + \
                str(self.typing.term.dimension) + "} " + self.typing.toTex()


def point(name: str) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^!$}` :math:`\\texttt{point}` rule.
    Introduces a :math:`0`-variable with name ``x``.
    """
    t = Typing(Term(Variable(name, 0)), Type([Term()]))
    return Sequent(EquationalTheory(), Context() + t, t)


def fill(seq: Sequent, name: str) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^!$}` :math:`\\texttt{fill}` rule.
    Takes a sequent ``seq`` typing a term ``t`` and introduces
    a new variable ``x`` having ``t`` as :math:`1`-source.
    """
    n = seq.typing.term.dimension
    res = deepcopy(seq)
    typing = Typing(
        Term(Variable(name, n + 1)),
        Type([seq.typing.term] + seq.typing.type.terms))
    res.context += typing
    res.typing = typing
    return res


def degen(seq: Sequent) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^!$}` :math:`\\texttt{degen}` rule.
    Takes a sequent typing a variable and produces a new
    sequent typing the degeneracy at that variable.
    """
    if not seq.typing.term.isVariable():
        raise DerivationError(
            "degen rule",
            "Term {term} typed in premiss sequent is expected to be a "
            "variable",
            term = str(seq.typing.term))
    res = deepcopy(seq)
    var = res.typing.term.variable
    res.typing = Typing(Term(var, True), Type([Term(var)] +
                                              res.typing.type.terms))
    return res


def degenfill(seq: Sequent, name: str) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^!$}` :math:`\\texttt{degen-fill}` rule.
    Applies the degen and the fill rule consecutively.
    """
    return fill(degen(seq), name)


def graft(seqt: Sequent, seqx: Sequent, name: str) -> Sequent:
    """
    The :math:`\\textbf{Opt${}^!$}` :math:`\\texttt{graft}` rule.
    Takes the following arguments:

    1. ``seqt`` typing an :math:`n` term  :math:`t`
    2. ``seqx`` second typing an :math:`n` variable :math:`x`
    3. an :math:`(n-1)` variable ``a`` onto which to operate the grafting,
       specified by its name ``name``

    such that the two sequents are compatible, and the intersection of their
    context is essentially the context typing ``a`` and its variables. It then
    produces the :math:`n` term :math:`t(a \\leftarrow x)`.

    The way the intersection condition is checked is by verifying that the only
    variables typed in both contexts (modulo both theories) are those appearing
    in the type of ``a`` or of course ``a`` itself.
    """
    if seqt.typing.term.variable is None:
        raise DerivationError(
            "graft rule",
            "First premiss sequent types an invalid / null term")
    elif seqx.typing.term.variable is None:
        raise DerivationError(
            "graft rule",
            "Second premiss sequent types an invalid / null term")
    a = Variable(name, seqt.typing.term.dimension - 1)
    # checking intersection
    inter = seqt.context & seqx.context
    typea = seqt.typeOf(a)
    if a not in seqt.context:  # a in the first sequent
        raise DerivationError(
            "graft rule",
            "Graft variable {var} not typed in first sequent",
            var = str(a))
    for i in range(0, a.dimension):   # all variables in the type of a are in
        for v in typea.variables(i):  # the context intersection
            if v not in inter:
                raise DerivationError(
                    "graft rule",
                    "Intersection of the two premiss contexts does not "
                    "type variable {v} necessary to define variable {a}",
                    v = str(v), a = str(a))
    for typing in inter:  # all variables in the intersection are in that of a
        w = typing.term.variable
        if w not in typea:
            raise DerivationError(
                "graft rule",
                "Intersection of the two premiss contexts, variable {v} "
                "is typed, but is not required to type variable {a}",
                v = str(w), a = a.toTex())
    # checking rule hypothesis
    if not seqx.typing.term.isVariable():
        raise DerivationError(
            "graft rule",
            "Second premiss sequent expected to type a variable (types "
            "{term})",
            term = str(seqx.typing.term))
    elif a not in seqt.typing.type.terms[0]:
        raise DerivationError(
            "graft rule",
            "Graft variable {a} does not occur in the source of the term"
            "{term} grafted upon",
            a = str(a), term = str(seqt.typing.term))
    elif a in seqt.typing.term:
        raise DerivationError(
            "graft rule",
            "Graft variable {a} occurs first premiss term {term}, meaning it "
            " has already been used for grafting",
            a = str(a), term = str(seqt.typing.term))
    elif not seqt.equal(seqt.source(a, 1),
                        seqx.source(seqx.typing.term.variable, 2)):
        raise DerivationError(
            "graft rule",
            "Variables {a} and {x} have incompatible shapes: s{a} = {sa}, "
            "while ss{x} = {ssx}",
            a = str(a), x = str(seqx.typing.term.variable),
            sa = str(seqt.source(a, 1)),
            ssx = str(seqx.source(seqx.typing.term.variable, 2)))
    # forming conclusion sequent
    theory = seqt.theory | seqx.theory     # union of both theories
    context = seqt.context | seqx.context  # union of both contexts
    term = seqt.graft(seqt.typing.term, a, seqx.typing.term)  # new term
    s1, eq = seqt.substitute(seqt.typing.type.terms[0],       # 1st source of
                             seqx.typing.type.terms[0], a)    # that new term
    type = deepcopy(seqt.typing.type)  # the type of the new term is that of t
    type.terms[0] = s1                 # except for the 1st source, which is s1
    if eq is not None:                 # add new equation on theory if needed
        theory += eq
    return Sequent(theory, context, Typing(term, type))


class RuleInstance(AbstractRuleInstance):
    """
    A rule instance of system :math:`\\textbf{Opt${}^!$}`.
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
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return "\\AxiomC{}\n\t\\RightLabel{\\texttt{point}}\n\t" + \
            "\\UnaryInfC{$" + self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates the proof tree, in this cases returns the point sequent by
        calling :func:`NamedOpetope.point`.
        """
        return point(self.variableName)


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

    def __repr__(self) -> str:
        return "Degen({})".format(repr(self.proofTree))

    def __str__(self) -> str:
        return "Degen({})".format(str(self.proofTree))

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{degen}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates this instance of ``degen`` by first evaluating its premise,
        and then applying :func:`NamedOpetope.degenerate` on the
        resulting sequent.
        """
        return degen(self.proofTree.eval())


class Fill(RuleInstance):
    """
    A class representing an instance of the ``fill`` rule in a proof tree.
    """

    proofTree: RuleInstance
    variableName: str

    def __init__(self, p: RuleInstance, name: str) -> None:
        self.proofTree = p
        self.variableName = name

    def __repr__(self) -> str:
        return "Fill({}, {})".format(repr(self.proofTree), self.variableName)

    def __str__(self) -> str:
        return "Fill({}, {})".format(str(self.proofTree), self.variableName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex() + \
            "\n\t\\RightLabel{\\texttt{fill}}\n\t\\UnaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        return fill(self.proofTree.eval(), self.variableName)


class DegenFill(RuleInstance):
    """
    A class representing an instance of the ``degen-fill`` rule in a proof
    tree.
    """

    proofTree: RuleInstance

    def __init__(self, p: RuleInstance, name: str) -> None:
        self.proofTree = Fill(Degen(p), name)
        self.eval()

    def __repr__(self) -> str:
        return repr(self.proofTree)

    def __str__(self) -> str:
        return str(self.proofTree)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree._toTex()

    def eval(self) -> Sequent:
        return self.proofTree.eval()


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

        :see: :func:`NamedOpetope.graft`.
        """
        self.proofTree1 = p1
        self.proofTree2 = p2
        self.variableName = a
        self.eval()

    def __repr__(self) -> str:
        return "Graft({p1}, {p2}, {a})".format(p1 = repr(self.proofTree1),
                                               p2 = repr(self.proofTree2),
                                               a = self.variableName)

    def __str__(self) -> str:
        return "Graft({p1}, {p2}, {a})".format(p1 = str(self.proofTree1),
                                               p2 = str(self.proofTree2),
                                               a = self.variableName)

    def _toTex(self) -> str:
        """
        Converts the proof tree in TeX code. This method should not be called
        directly, use :meth:`NamedOpetope.RuleInstance.toTex`
        instead.
        """
        return self.proofTree1._toTex() + "\n\t" + self.proofTree2._toTex() + \
            "\n\t\\RightLabel{\\texttt{graft-}$" + \
            self.variableName + "$}\n\t\\BinaryInfC{$" + \
            self.eval().toTex() + "$}"

    def eval(self) -> Sequent:
        """
        Evaluates this instance of ``graft`` by first evaluating its premises,
        and then applying :func:`NamedOpetope.graft` at variable
        ``self.variableName`` on the resulting sequents.
        """
        return graft(
            self.proofTree1.eval(), self.proofTree2.eval(), self.variableName)


def Arrow(pointName: str = "a", arrowName: str = "f") -> RuleInstance:
    """
    Returns the proof tree of the arrow, with cell names as specified in the
    arguments.
    """
    return Fill(Point(pointName), arrowName)


def OpetopicInteger(n: int, pointName: str = "a", arrowName: str = "f",
                    cellName: str = "A") -> RuleInstance:
    """
    Returns the proof tree of the :math:`n`-th opetopic integer.

    * if ``n`` is 0, then the unique point is named ``pointName`` (default
      ``a``), and the unique :math:`2`-cell is named ``cellName`` (default
      ``A``).
    * otherwise, the points are named ``a_1``, ``a_2``, ... ``a_n-1`` (with
      added braces if the index exceeds 10, so that it is :math:`\\TeX`
      friendly), arrows ``f_1``, ... ``f_n``. Those names can be changed
      by specifying the ``pointName`` and ``arrowName`` arguments. The
      unique :math:`2`-cell is named ``cellName`` (default ``A``).
    """
    if n < 0:
        raise DerivationError(
            "Opetopic integer",
            "Parameter n must be >=0 (is {n})",
            n = n)
    elif n == 0:
        return DegenFill(Point(pointName), cellName)
    else:
        def toTex(i: int) -> str:
            if 0 <= i and i < 10:
                return str(i)
            else:
                return "{" + str(i) + "}"
        pointNames = [pointName + "_" + toTex(i) for i in range(1, n + 1)]
        arrowNames = [arrowName + "_" + toTex(i) for i in range(1, n + 1)]
        arrows = [Fill(Point(pointNames[i - 1]), arrowNames[i - 1])
                  for i in range(1, n + 1)]
        res = arrows[0]  # type: Union[Fill, Graft]
        for i in range(1, n):
            res = Graft(res, arrows[i], pointNames[i - 1])
        return Fill(res, cellName)
