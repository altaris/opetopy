Named Opetopes
**************


Examples
========


The point
---------


.. code-block:: python

    from opetopy.NamedOpetope import *

    pt = Point("x")
    print(pt.eval())

::

     ▷ x : ∅ ⊢ x : ∅


A classic
---------


.. code-block:: python

    from opetopy.NamedOpetope import *

    beta = Fill(Graft(
        Fill(Point("c"), "h"),
        Fill(Point("a"), "i"),
        "c"),
        "β")
    alpha = Fill(Graft(
        Fill(Point("b"), "g"),
        Fill(Point("a"), "f"),
        "b"),
        "α")
    classic = Fill(Graft(beta, alpha, "i"), "A")
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
