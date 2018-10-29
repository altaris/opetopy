Opetopic categories: unnamed approach
*************************************


Examples
========

.. _uoptcat-ex-fill-tgt:

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


Source universal property
-------------------------


This example is a continuation of that presented in :ref:`uoptcat-ex-fill-tgt`. We derive the following additional cells:

* :math:`i`, parallel to :math:`h` (the composition of arrows :math:`f` and :math:`g`);
* :math:`\beta`, from the :math:`fg` horn to :math:`i`.

We then apply the target universal property of :math:`\alpha` over :math:`\beta` to obtain a factorization :math:`\xi : h \longrightarrow i` and a filler :math:`A`. We do it again, with a new factorization :math:`\zeta` and filler :math:`B`. Finally, we apply the source univerality of :math:`A` over :math:`B` to obtain a factorization :math:`C : \zeta \longrightarrow \xi`.

This hints that any two factorization in the application of the target universality of the composition :math:`h` over :math:`i` are homotopic, and in fact, equivalent. 

.. literalinclude:: ../tests/test_unnamedopetopiccategory_applysourceuniversalproperty.py
    :language: python
    :linenos:

.. literalinclude:: build/tests/test_unnamedopetopiccategory_applysourceuniversalproperty.out
    :linenos:


Documentation
=============


.. automodule:: UnnamedOpetopicCategory
    :members:
    :private-members:
    :special-members:
