Named Opetopic Sets
*******************


Example
========


.. code-block:: python

    alpha = Fill(Fill(Point(Variable("a", 0)),
                      Variable("f", 1)),
                 Variable("α", 2))
    g = Fill(Point(Variable("c", 0)), Variable("g", 1))
    h = Fill(Point(Variable("b", 0)), Variable("h", 1))
    unfolded = Sum(Sum(Repr(alpha), Repr(g)), Repr(h))
    example = Fold(Fold(Fold(Fold(Fold(unfolded,
                                       Variable("a", 0),
                                       Variable("c", 0)),
                                  Variable("b", 0),
                                  Variable("tf", 0)),
                             Variable("b", 0),
                             Variable("tg", 0)),
                        Variable("a", 0),
                        Variable("th", 0)),
                   Variable("g", 1),
                   Variable("tα", 1))
    print(example.eval())

::

    {tf, b, ttα, tg}, {th, a, c}, {g, tα} ▷ th : ∅, h : b → ∅, g : c → ∅, ttα : ∅, b : ∅, tg : ∅, α : f → a → ∅, a : ∅, f : a → ∅, c : ∅, tα : a → ∅, tf : ∅

.. code-block:: python

    print(example.toTex())

.. code-block:: TeX

    \begin{prooftree}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \smalltriangleright a : \emptyset \vdash_{0} a : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \smalltriangleright a : \emptyset, f : a \rightarrow \emptyset \vdash_{1} f : a \rightarrow \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \smalltriangleright a : \emptyset, α : f \rightarrow a \rightarrow \emptyset, f : a \rightarrow \emptyset \vdash_{2} α : f \rightarrow a \rightarrow \emptyset$}
    \RightLabel{\texttt{repr}}
    \UnaryInfC{$\left\{ttα, tf\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, tα : a \rightarrow \emptyset, ttα : \emptyset, a : \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \smalltriangleright c : \emptyset \vdash_{0} c : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \smalltriangleright g : c \rightarrow \emptyset, c : \emptyset \vdash_{1} g : c \rightarrow \emptyset$}
    \RightLabel{\texttt{repr}}
    \UnaryInfC{$ \smalltriangleright g : c \rightarrow \emptyset, c : \emptyset, tg : \emptyset$}
    \RightLabel{\texttt{sum}}
    \BinaryInfC{$\left\{ttα, tf\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, tα : a \rightarrow \emptyset, tg : \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \smalltriangleright b : \emptyset \vdash_{0} b : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \smalltriangleright b : \emptyset, h : b \rightarrow \emptyset \vdash_{1} h : b \rightarrow \emptyset$}
    \RightLabel{\texttt{repr}}
    \UnaryInfC{$ \smalltriangleright b : \emptyset, th : \emptyset, h : b \rightarrow \emptyset$}
    \RightLabel{\texttt{sum}}
    \BinaryInfC{$\left\{ttα, tf\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tα : a \rightarrow \emptyset, tg : \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \RightLabel{\texttt{fold-}$(a = c)$}
    \UnaryInfC{$\left\{ttα, tf\right\}, \left\{a, c\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tg : \emptyset, tα : a \rightarrow \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \RightLabel{\texttt{fold-}$(b = tf)$}
    \UnaryInfC{$\left\{ttα, tf, b\right\}, \left\{a, c\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tα : a \rightarrow \emptyset, tg : \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \RightLabel{\texttt{fold-}$(b = tg)$}
    \UnaryInfC{$\left\{ttα, tf, tg, b\right\}, \left\{a, c\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tg : \emptyset, tα : a \rightarrow \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \RightLabel{\texttt{fold-}$(a = th)$}
    \UnaryInfC{$\left\{ttα, tf, tg, b\right\}, \left\{a, c, th\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tα : a \rightarrow \emptyset, tg : \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \RightLabel{\texttt{fold-}$(g = tα)$}
    \UnaryInfC{$\left\{ttα, tf, tg, b\right\}, \left\{a, c, th\right\}, \left\{tα, g\right\} \smalltriangleright α : f \rightarrow a \rightarrow \emptyset, g : c \rightarrow \emptyset, th : \emptyset, tg : \emptyset, tα : a \rightarrow \emptyset, c : \emptyset, ttα : \emptyset, a : \emptyset, b : \emptyset, h : b \rightarrow \emptyset, f : a \rightarrow \emptyset, tf : \emptyset$}
    \end{prooftree}


Documentation
=============

.. automodule:: NamedOpetopicSet
    :members:
    :private-members:
    :special-members:

