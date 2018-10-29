Unnamed Opetopes
****************


In addition to the :math:`\textbf{Opt${}^?$}` derivation rules and their proof tree node counterparts, the following two functions are present:

* :func:`UnnamedOpetope.Arrow`: returns the proof tree of the arrow;
* :func:`UnnamedOpetope.OpetopicInteger`: returns the proof tree of an opetopic integer (i.e. :math:`2`-opetope).


Examples
========


The arrow
---------


.. literalinclude:: ../tests/test_unnamedopetope_arrow.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetope_arrow.out
    :linenos:


A classic
---------


.. literalinclude:: ../tests/test_unnamedopetope_classic.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetope_classic.out
    :linenos:


Opetopic integers
-----------------


Recall that for :math:`n \in \mathbb{N}`:

* if :math:`n = 0`, then :math:`\mathbf{n} = \{ \{ \blacklozenge`;
* if :math:`n = 1`, then :math:`\mathbf{n} = \{ [] \leftarrow \blacksquare`;
* otherwise, :math:`\mathbf{n} = \mathbf{(n-1)} \circ_{[* \cdots *]} \blacksquare`, where there is :math:`(n-1)` instances of :math:`*` in the grafting address.

This is exactly the implementation of :func:`UnnamedOpetope.OpetopicInteger`.

.. literalinclude:: ../tests/test_unnamedopetope_opetopicinteger.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetope_opetopicinteger.out
    :linenos:


Deciding opetopes
-----------------


The :func:`UnnamedOpetope.ProofTree` effectively decides opetopes among preopetopes. It takes as argument a preopetopes in "convenient form" (see examples), and returns its proof tree if it is an opetope, or raises an exception otherwise.


Here, we construct the proof tree of :math:`\mathsf{Y}_{\mathbf{2}} \circ_{[[*]]} \mathsf{Y}_{\mathbf{0}}`

.. literalinclude:: ../tests/test_unnamedopetope_decision_valid.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetope_decision_valid.out
    :linenos:

Here, we try to construct the proof tree of the invalid :math:`\mathsf{Y}_{\mathbf{1}} \circ_{[[***]]} \mathsf{Y}_{\mathbf{1}}`

.. code-block:: python
    :linenos:

    from UnnamedOpetope import address, ProofTree

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
