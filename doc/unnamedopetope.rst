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

    from opetopy.UnnamedOpetope import *

    ar = Shift(Point())
    print(ar.eval())

    # Faster way
    ar = Arrow()

::

    ctx = {}
    src = ■
    tgt = ⧫


A classic
---------


.. code-block:: python

    from opetopy.UnnamedOpetope import *

    classic = Graft(
        Shift(OpetopicInteger(2)),
        OpetopicInteger(2),
        address([['*']])
    )
    print(classic.eval())

    # Faster way
    classic = OpetopicTree([None, [None, None]])

::

    ctx = {
        [[]] ↦ []
        [[*][]] ↦ [*]
        [[*][*]] ↦ [**]
    }
    src = {
        [] : {
            [] : ■
            [*] : ■
        }
        [[*]] : {
            [] : ■
            [*] : ■
        }
    }
    tgt = {
        [] : ■
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
        \UnaryInfC{$\frac{[*]}{*} \vdash \opetope{[] \sep \oneOpt} \longrightarrow \oneOpt$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$\frac{[[]]}{[]} \vdash \opetope{[] \sep \opetope{[] \sep \oneOpt}} \longrightarrow \opetope{[] \sep \oneOpt}$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \zeroOpt \longrightarrow \emptyset$}
        \RightLabel{\texttt{degen}}
        \UnaryInfC{$\frac{[]}{*} \vdash \degenopetope{\zeroOpt} \longrightarrow \oneOpt$}
        \RightLabel{\texttt{graft-}$[[]]$}
        \BinaryInfC{$ \vdash \opetope{[] \sep \opetope{[] \sep \oneOpt} \\ [[]] \sep \degenopetope{\zeroOpt}} \longrightarrow \degenopetope{\zeroOpt}$}
    \end{prooftree}


Opetopic integers
-----------------


Recall that for :math:`n \in \mathbb{N}`:

* if :math:`n = 0`, then :math:`\mathbf{n} = \{ \{ \blacklozenge`;
* if :math:`n = 1`, then :math:`\mathbf{n} = \{ [] \leftarrow \blacksquare`;
* otherwise, :math:`\mathbf{n} = \mathbf{(n-1)} \circ_{[* \cdots *]} \blacksquare`, where there is :math:`(n-1)` instances of :math:`*` in the grafting address.

This is exactly the implementation of :func:`UnnamedOpetope.OpetopicInteger`.

.. code-block:: python

    from UnnamedOpetope import OpetopicInteger

    oi5 = OpetopicInteger(5)
    print(oi5.eval())

::

    ctx = {
        [*****] ↦ *
    }
    src = {
        []: ■
        [*]: ■
        [**]: ■
        [***]: ■
        [****]: ■
    }
    tgt = ■


.. code-block:: python

    print(oi5.toTex())

.. code-block:: TeX

    \begin{prooftree}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \optZero \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \optOne \longrightarrow \optZero$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$\frac{[*]}{*} \vdash \opetope{[] \sep \optOne} \longrightarrow \optOne$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \optZero \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \optOne \longrightarrow \optZero$}
        \RightLabel{\texttt{graft-}$[*]$}
        \BinaryInfC{$\frac{[**]}{*} \vdash \opetope{[] \sep \optOne \\ [*] \sep \optOne} \longrightarrow \optOne$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \optZero \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \optOne \longrightarrow \optZero$}
        \RightLabel{\texttt{graft-}$[**]$}
        \BinaryInfC{$\frac{[***]}{*} \vdash \opetope{[] \sep \optOne \\ [*] \sep \optOne \\ [**] \sep \optOne} \longrightarrow \optOne$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \optZero \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \optOne \longrightarrow \optZero$}
        \RightLabel{\texttt{graft-}$[***]$}
        \BinaryInfC{$\frac{[****]}{*} \vdash \opetope{[] \sep \optOne \\ [*] \sep \optOne \\ [**] \sep \optOne \\ [***] \sep \optOne} \longrightarrow \optOne$}
        \AxiomC{}
        \RightLabel{\texttt{point}}
        \UnaryInfC{$ \vdash \optZero \longrightarrow \emptyset$}
        \RightLabel{\texttt{shift}}
        \UnaryInfC{$ \vdash \optOne \longrightarrow \optZero$}
        \RightLabel{\texttt{graft-}$[****]$}
        \BinaryInfC{$\frac{[*****]}{*} \vdash \opetope{[] \sep \optOne \\ [*] \sep \optOne \\ [**] \sep \optOne \\ [***] \sep \optOne \\ [****] \sep \optOne} \longrightarrow \optOne$}
    \end{prooftree}



Deciding opetopes
-----------------


The :func:`UnnamedOpetope.ProofTree` effectively decides opetopes among preopetopes. It takes as argument a preopetopes in "convenient form" (see examples), and returns its proof tree if it is an opetope, or raises an exception otherwise.


Here, we construct the proof tree of :math:`\mathsf{Y}_{\mathbf{2}} \circ_{[[*]]} \mathsf{Y}_{\mathbf{0}}`

.. code-block:: python

    from UnnamedOpetope import address, ProofTree

    p = ProofTree({
        address([], 2): {
            address([], 1): {
                address('*'): {}  # {} represents the point
            },
            address(['*']): {
                address('*'): {}
            }
        },
        address([['*']]): {
            None: {}  # indicates a degeneracy
        }})
    print(p)

::

    Graft(Shift(Graft(Shift(Shift(Point())), Shift(Point()), [*])), Degen(Point()), [[*]])


.. code-block:: python

    print(p.eval())

::

    ctx = {
        [[]] ↦ []
    }
    src = {
        []: {
            []: ■
            [*]: ■
        }
        [[*]]: degen(⧫)
    }
    tgt = {
        []: ■
        [*]: ■
    }


Here, we try to construct the proof tree of the invalid :math:`\mathsf{Y}_{\mathbf{1}} \circ_{[[***]]} \mathsf{Y}_{\mathbf{1}}`

.. code-block:: TeX

    ProofTree({
        address([], 2): {
            address([], 1): {
                address('*'): {}
            }
        },
        address([['*', '*', '*']]): {
            address([], 1): {
                address('*'): {}
            }
        }})

which raises an exception.


Documentation
=============


.. automodule:: UnnamedOpetope
    :members:
    :private-members:
    :special-members:
