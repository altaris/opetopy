Unnamed Opetopic Sets
*********************


Examples
========


The arrow
---------


.. code-block:: python

    from opetopy.UnnamedOpetopicSet import *
    from opetopy.UnnamedOpetope import address, Arrow

    ar = Point("a")
    ar = Point("b", ar)
    ar = Graft(
        pastingDiagram(
            Arrow(),
            {
                address([], 0): "a"
            }),
        ar)
    ar = Fill("b", "f", ar)
    print(ar.eval())

::
    
    b : ⧫, f : PastingDiagram(* ← a) → b, a : ⧫ ⊢ 

.. code-block:: python

    print(ar.toTex())

.. code-block:: TeX

    \begin{prooftree}
        \AxiomC{}
        \RightLabel{\texttt{point-$a$}}
        \UnaryInfC{$a : \optZero \vdash $}
        \RightLabel{\texttt{point-$b$}}
        \UnaryInfC{$a : \optZero, b : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$a : \optZero, b : \optZero \vdash \opetope{* \sep a}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$a : \optZero, f : \opetope{* \sep a} \longrightarrow b, b : \optZero \vdash $}
    \end{prooftree}


A classic, maximally folded
---------------------------

We start by deriving in :math:`\textbf{Opt${}^?$}` (see :mod:`UnnamedOpetope`) the opetope :math:`\omega = \mathsf{Y}_{\mathbf{2}} \circ_{[[*]]} \mathsf{Y}_{\mathbf{2}}` describing the shape of the maximal cell :math:`A`. We then proceed to derive the opetopic set in :math:`\textbf{OptSet${}^?$}`.

.. code-block:: python

    from opetopy.UnnamedOpetopicSet import *
    from opetopy.UnnamedOpetope import address, Arrow, OpetopicInteger
    from opetopy.UnnamedOpetope import Graft as OptGraft
    from opetopy.UnnamedOpetope import Shift as OptShift

    # Derivation of ω
    omega = OptGraft(
        OptShift(OpetopicInteger(2)),
        OpetopicInteger(2),
        address([['*']]))

    # Derivation of a
    classic = Point("a")

    # Derivation of f
    classic = Graft(
        pastingDiagram(
            Arrow(),
            {
                address([], 0): "a"
            }),
        classic)
    classic = Fill("a", "f", classic)

    # Derivation of α
    classic = Graft(
        pastingDiagram(
            OpetopicInteger(2),
            {
                address([], 1): "f",
                address(['*']): "f"
            }),
        classic)
    classic = Fill("f", "α", classic)

    # Derivation of β
    classic = Graft(
        pastingDiagram(
            OpetopicInteger(3),
            {
                address([], 1): "f",
                address(['*']): "f",
                address(['*', '*']): "f"
            }),
        classic)
    classic = Fill("f", "β", classic)

    # Derivation of A
    classic = Graft(
        pastingDiagram(
            omega,
            {
                address([], 2): "α",
                address([['*']]): "α"
            }),
        classic)
    classic = Fill("β", "A", classic)

    print(classic.eval())

::

    A : PastingDiagram([] ← α, [[*]] ← α) → β, β : PastingDiagram([] ← f, [*] ← f, [**] ← f) → f, f : PastingDiagram(* ← a) → a, α : PastingDiagram([] ← f, [*] ← f) → f, a : ⧫ ⊢ 

.. code-block:: python

    print(classic.toTex())

.. code-block:: TeX

    \begin{prooftree}
        \AxiomC{}
        \RightLabel{\texttt{point-$a$}}
        \UnaryInfC{$a : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$a : \optZero \vdash \opetope{* \sep a}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$a : \optZero, f : \opetope{* \sep a} \longrightarrow a \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, a : \optZero \vdash \opetope{[] \sep f \\ [*] \sep f}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, α : \opetope{[] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$α : \opetope{[] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero, f : \opetope{* \sep a} \longrightarrow a \vdash \opetope{[] \sep f \\ [*] \sep f \\ [**] \sep f}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, β : \opetope{[] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, α : \opetope{[] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$a : \optZero, β : \opetope{[] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, α : \opetope{[] \sep f \\ [*] \sep f} \longrightarrow f, f : \opetope{* \sep a} \longrightarrow a \vdash \opetope{[] \sep α \\ [[*]] \sep α}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$a : \optZero, α : \opetope{[] \sep f \\ [*] \sep f} \longrightarrow f, β : \opetope{[] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, f : \opetope{* \sep a} \longrightarrow a, A : \opetope{[] \sep α \\ [[*]] \sep α} \longrightarrow β \vdash $}
    \end{prooftree}


Documentation
=============

.. automodule:: UnnamedOpetopicSet
    :members:
    :private-members:
    :special-members:
