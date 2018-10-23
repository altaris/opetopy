Unnamed Opetopes
****************


In addition to the :math:`\textbf{Opt${}^?$}` derivation rules and their proof tree node counterparts, the following two functions are present:

* :func:`UnnamedOpetope.Arrow`: returns the proof tree of the arrow;
* :func:`UnnamedOpetope.OpetopicInteger`: returns the proof tree of an opetopic integer (i.e. :math:`2`-opetope).


Examples
========


The arrow
---------


.. code-block:: python

    ar = Shift(Point())
    print(ar.eval())

::

    ctx = {
        
    }
    src = ■
    tgt = ⧫


A classic
---------


.. code-block:: python

    classic = Graft(
        Shift(OpetopicInteger(2)),
        OpetopicInteger(2),
        Address.epsilon(0).shift(2)
    )
    print(classic.eval())

::

    ctx = {
        [[ε]] → [ε]
        [[*][ε]] → [*]
        [[*][*]] → [**]
    }
    src = {
        [ε] : {
            [ε] : ■
            [*] : ■
        }
        [[*]] : {
            [ε] : ■
            [*] : ■
        }
    }
    tgt = {
        [ε] : ■
        [*] : ■
        [**] : ■
    }

.. code-block:: python

    print(classic.toTex())

.. code-block:: TeX

    \begin{prooftree}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \zeroOpt \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \oneOpt \longrightarrow \zeroOpt$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$\frac{[*]}{*} \vdash \opetope{[\epsilon] \sep \oneOpt} \longrightarrow \oneOpt$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$\frac{[[\epsilon]]}{[\epsilon]} \vdash \opetope{[\epsilon] \sep \opetope{[\epsilon] \sep \oneOpt}} \longrightarrow \opetope{[\epsilon] \sep \oneOpt}$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \zeroOpt \longrightarrow \emptyset$}
        \RightLabel{\texttt{degen}}
        \UnaryInfC{$\frac{[\epsilon]}{*} \vdash \degenopetope{\zeroOpt} \longrightarrow \oneOpt$}
        \RightLabel{\texttt{graft-}$[[\epsilon]]$}
        \BinaryInfC{$ \vdash \opetope{[\epsilon] \sep \opetope{[\epsilon] \sep \oneOpt} \\ [[\epsilon]] \sep \degenopetope{\zeroOpt}} \longrightarrow \degenopetope{\zeroOpt}$}
    \end{prooftree}


Documentation
=============


.. automodule:: UnnamedOpetope
    :members:
    :private-members:
    :special-members:
