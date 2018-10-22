Named Opetopes
**************


Examples
========


The point
---------


.. code-block:: python

    pt = Point(Variable("x", 0))
    print(pt.eval())

::

     ▷ x : ∅ ⊢ x : ∅


A classic
---------


.. code-block:: python

    beta = Fill(Graft(
        Fill(Point(Variable("c", 0)), Variable("h", 1)),
        Fill(Point(Variable("a", 0)), Variable("i", 1)),
        Variable("c", 0)),
        Variable("β", 2))
    alpha = Fill(Graft(
        Fill(Point(Variable("b", 0)), Variable("g", 1)),
        Fill(Point(Variable("a", 0)), Variable("f", 1)),
        Variable("b", 0)),
        Variable("α", 2))
    classic = Fill(Graft(beta, alpha, Variable("i", 1)),
        Variable("A", 3))
    print(classic.eval())

::

     ▷ A : β(i ← α) → h(c ← g(b ← f)) → a → ∅, f : a → ∅, α : g(b ← f) → a → ∅, a : ∅, h : c → ∅, c : ∅, β : h(c ← i) → a → ∅, g : b → ∅, i : a → ∅, b : ∅ ⊢ A : β(i ← α) → h(c ← g(b ← f)) → a → ∅

.. code-block:: python

    print(classic.toTex())

.. code-block:: TeX

    \begin{prooftree}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \vdash_{0} c : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{1} h : c \rightarrow \emptyset$}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \vdash_{0} a : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{1} i : a \rightarrow \emptyset$}
    \RightLabel{\texttt{graft-}$c$}
    \BinaryInfC{$ \vdash_{1} h(c \leftarrow i) : a \rightarrow \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{2} β : h(c \leftarrow i) \rightarrow a \rightarrow \emptyset$}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \vdash_{0} b : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{1} g : b \rightarrow \emptyset$}
    \AxiomC{}
    \RightLabel{\texttt{point}}
    \UnaryInfC{$ \vdash_{0} a : \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{1} f : a \rightarrow \emptyset$}
    \RightLabel{\texttt{graft-}$b$}
    \BinaryInfC{$ \vdash_{1} g(b \leftarrow f) : a \rightarrow \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{2} α : g(b \leftarrow f) \rightarrow a \rightarrow \emptyset$}
    \RightLabel{\texttt{graft-}$i$}
    \BinaryInfC{$ \vdash_{2} β(i \leftarrow α) : h(c \leftarrow g(b \leftarrow f)) \rightarrow a \rightarrow \emptyset$}
    \RightLabel{\texttt{fill}}
    \UnaryInfC{$ \vdash_{3} A : β(i \leftarrow α) \rightarrow h(c \leftarrow g(b \leftarrow f)) \rightarrow a \rightarrow \emptyset$}
    \end{prooftree}


Documentation
=============


.. automodule:: NamedOpetope
    :members:
    :private-members:
    :special-members:
