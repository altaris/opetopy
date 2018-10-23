Unnamed Opetopic Sets
*********************


Examples
========


The arrow
---------


.. code-block:: python

    from UnnamedOpetopicSet import *
    import UnnamedOpetope

    ar = Point("a")
    ar = Point("b", ar)
    ar = Graft(
        PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.Arrow(),
            {UnnamedOpetope.Address.epsilon(0): "a"}),
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

We start by deriving in :math:`\textbf{Opt${}^?$}` (see :mod:`UnnamedOpetope`) the opetope :math:`\omega = \mathsf{Y}_{\underline{2}} \circ_{[[*]]} \mathsf{Y}_{\underline{2}}` describing the shape of the maximal cell :math:`A`. We then proceed to derive the opetopic set in :math:`\textbf{OptSet${}^?$}`.

.. code-block:: python
    
    # Derivation of ω
    omega = UnnamedOpetope.Graft(
        UnnamedOpetope.Shift(UnnamedOpetope.OpetopicInteger(2)),
        UnnamedOpetope.OpetopicInteger(2),
        UnnamedOpetope.Address.epsilon(0).shift(2))

    # Derivation of a
    classic = Point("a")

    # Derivation of f
    classic = Graft(
        PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.Arrow(),
            {
                UnnamedOpetope.Address.epsilon(0): "a"
            }),
        classic)
    classic = Fill("a", "f", classic)

    # Derivation of α
    classic = Graft(
        PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(2),
            {
                UnnamedOpetope.Address.fromList([], 1): "f",
                UnnamedOpetope.Address.fromList(['*'], 1): "f"
            }),
        classic)
    classic = Fill("f", "α", classic)

    # Derivation of β
    classic = Graft(
        PastingDiagram.nonDegeneratePastingDiagram(
            UnnamedOpetope.OpetopicInteger(3),
            {
                UnnamedOpetope.Address.fromList([], 1): "f",
                UnnamedOpetope.Address.fromList(['*'], 1): "f",
                UnnamedOpetope.Address.fromList(['*', '*'], 1): "f"
            }),
        classic)
    classic = Fill("f", "β", classic)

    # Derivation of A
    classic = Graft(
        PastingDiagram.nonDegeneratePastingDiagram(
            omega,
            {
                UnnamedOpetope.Address.epsilon(2): "α",
                UnnamedOpetope.Address.epsilon(0).shift(2): "α"
            }),
        classic)
    classic = Fill("β", "A", classic)

    print(classic.eval())

::

    A : PastingDiagram([ε] ← α, [[*]] ← α) → β, β : PastingDiagram([ε] ← f, [*] ← f, [**] ← f) → f, f : PastingDiagram(* ← a) → a, α : PastingDiagram([ε] ← f, [*] ← f) → f, a : ⧫ ⊢ 

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
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, a : \optZero \vdash \opetope{[\epsilon] \sep f \\ [*] \sep f}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, α : \opetope{[\epsilon] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$α : \opetope{[\epsilon] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero, f : \opetope{* \sep a} \longrightarrow a \vdash \opetope{[\epsilon] \sep f \\ [*] \sep f \\ [**] \sep f}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$f : \opetope{* \sep a} \longrightarrow a, β : \opetope{[\epsilon] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, α : \opetope{[\epsilon] \sep f \\ [*] \sep f} \longrightarrow f, a : \optZero \vdash $}
        \RightLabel{\texttt{graft}}
        \UnaryInfC{$a : \optZero, β : \opetope{[\epsilon] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, α : \opetope{[\epsilon] \sep f \\ [*] \sep f} \longrightarrow f, f : \opetope{* \sep a} \longrightarrow a \vdash \opetope{[\epsilon] \sep α \\ [[*]] \sep α}$}
        \RightLabel{\texttt{fill}}
        \UnaryInfC{$a : \optZero, α : \opetope{[\epsilon] \sep f \\ [*] \sep f} \longrightarrow f, β : \opetope{[\epsilon] \sep f \\ [*] \sep f \\ [**] \sep f} \longrightarrow f, f : \opetope{* \sep a} \longrightarrow a, A : \opetope{[\epsilon] \sep α \\ [[*]] \sep α} \longrightarrow β \vdash $}
    \end{prooftree}


Documentation
=============

.. automodule:: UnnamedOpetopicSet
    :members:
    :private-members:
    :special-members:
