Opetopic categories: unnamed approach
*************************************


Examples
========


Filler of target horn
---------------------


In this simple example, we use the target filling of a pasting diagram of shape :math:`\mathbf{2}`, effectively composing arrow cells :math:`f` and :math:`g`. The result is the arrow :math:`h`, and the compositor is :math:`\alpha`.


.. literalinclude:: ../tests/test_unnamedopetopiccategory_filltargethorn.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetopiccategory_filltargethorn.out
    :linenos:


Target universal property
-------------------------


In this example, we have two cells of shape :math:`\mathbf{0}`:

* :math:`\delta`, degenerate at :math:`a` with target :math:`f`, constructed via rules :math:`\texttt{degen}` and :math:`\texttt{fill}` of system :math:`\textsc{OptSet${}^?$}`;
* :math:`\gamma`, constructed by filling the empty pasting diagram at :math:`a`, with universal target :math:`g`.

We then apply the target universal property of :math:`\gamma` over :math:`\delta` to get a factorization cell :math:`\xi` and a filler :math:`A`.

.. literalinclude:: ../tests/test_unnamedopetopiccategory_applytargetuniversalproperty.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetopiccategory_applytargetuniversalproperty.out
    :linenos:


Documentation
=============


.. automodule:: UnnamedOpetopicCategory
    :members:
    :private-members:
    :special-members:
