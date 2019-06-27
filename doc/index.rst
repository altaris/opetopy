.. role:: python(code)
    :language: python

opetopy
*******

.. image:: https://travis-ci.com/altaris/opetopy.svg?branch=master
    :target: https://travis-ci.com/altaris/opetopy
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/altaris/opetopy/badge.svg?branch=master
    :target: https://coveralls.io/github/altaris/opetopy?branch=master
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/opetopy/badge/?version=latest
    :target: https://opetopy.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://badgen.net/badge//GitHub/green?icon=github
    :target: https://github.com/altaris/opetopy
    :alt: GitHub

.. image:: https://badgen.net/badge/Python/3/blue
    :alt: Python 3

.. image:: https://badgen.net/badge/license/MIT/blue
    :target: https://choosealicense.com/licenses/mit/
    :alt: MIT License

.. contents:: Contents


Introduction
============


This project is the Python implementation of the opetope derivation systems
presented in [CHM19]_ and some other work in progress.

The :mod:`opetopy` module is decomposed as follow:

+--------------------------------+------------------------------+-------------------------------+
| Module                         | Syntactical construct        | Derivation system             |
+================================+==============================+===============================+
| :mod:`NamedOpetope`            | Named opetopes               | :math:`\textbf{Opt${}^!$}`    |
+--------------------------------+------------------------------+-------------------------------+
| :mod:`NamedOpetopicSet`        | Named opetopic sets          | :math:`\textbf{OptSet${}^!$}` |
+--------------------------------+------------------------------+-------------------------------+
| :mod:`UnnamedOpetope`          | Unnamed opetopes             | :math:`\textbf{Opt${}^?$}`    |
+--------------------------------+------------------------------+-------------------------------+
| :mod:`UnnamedOpetopicSet`      | Unnamed opetopic sets        | :math:`\textbf{OptSet${}^?$}` |
+--------------------------------+------------------------------+-------------------------------+
| :mod:`UnnamedOpetopicCategory` | Unnamed opetopic categories  | :math:`\textbf{OptCat${}^?$}` |
+--------------------------------+------------------------------+-------------------------------+

Each implement the following:

1. the syntactic constructs required to describe opetopes / opetopic sets and their sequents;
2. the derivation rules of the relevant system;
3. wrappers of those rules to describe proof trees.

+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| Derivation system               | Rule                         | Implementation                                 | Proof tree node                                 |
+=================================+==============================+================================================+=================================================+
| :math:`\textbf{Opt${}^!$}`      | :math:`\texttt{point}`       | :func:`opetopy.NamedOpetope.point`             | :class:`opetopy.NamedOpetope.Point`             |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{degen}`       | :func:`opetopy.NamedOpetope.degen`             | :class:`opetopy.NamedOpetope.Degen`             |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{degen-fill}`  | :func:`opetopy.NamedOpetope.degenfill`         | :class:`opetopy.NamedOpetope.DegenFill`         |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{fill}`        | :func:`opetopy.NamedOpetope.fill`              | :class:`opetopy.NamedOpetope.Fill`              |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{graft}`       | :func:`opetopy.NamedOpetope.graft`             | :class:`opetopy.NamedOpetope.Graft`             |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| :math:`\textbf{OptSet${}^!$}`   | :math:`\texttt{repr}`        | :func:`opetopy.NamedOpetopicSet.repres`        | :class:`opetopy.NamedOpetopicSet.Repr`          |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{zero}`        | :func:`opetopy.NamedOpetopicSet.zero`          | :class:`opetopy.NamedOpetopicSet.Zero`          |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{sum}`         | :func:`opetopy.NamedOpetopicSet.sum`           | :class:`opetopy.NamedOpetopicSet.Sum`           |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{glue}`        | :func:`opetopy.NamedOpetopicSet.glue`          | :class:`opetopy.NamedOpetopicSet.Glue`          |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| :math:`\textbf{OptSet${}^!_m$}` | :math:`\texttt{point}`       | :func:`opetopy.NamedOpetopicSetM.point`        | :class:`opetopy.NamedOpetopicSetM.Point`        |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{degen}`       | :func:`opetopy.NamedOpetopicSetM.degen`        | :class:`opetopy.NamedOpetopicSetM.Degen`        |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{pd}`          | :func:`opetopy.NamedOpetopicSetM.pd`           | :class:`opetopy.NamedOpetopicSetM.Pd`           |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{graft}`       | :func:`opetopy.NamedOpetopicSetM.graft`        | :class:`opetopy.NamedOpetopicSetM.Graft`        |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{fill}`        | :func:`opetopy.NamedOpetopicSetM.fill`         | :class:`opetopy.NamedOpetopicSetM.Fill`         |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{zero}`        | :func:`opetopy.NamedOpetopicSetM.zero`         | :class:`opetopy.NamedOpetopicSetM.Zero`         |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{sum}`         | :func:`opetopy.NamedOpetopicSetM.sum`          | :class:`opetopy.NamedOpetopicSetM.Sum`          |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{glue}`        | :func:`opetopy.NamedOpetopicSetM.glue`         | :class:`opetopy.NamedOpetopicSetM.Glue`         |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| :math:`\textbf{Opt${}^?$}`      | :math:`\texttt{point}`       | :func:`opetopy.UnnamedOpetope.point`           | :class:`opetopy.UnnamedOpetope.Point`           |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{degen}`       | :func:`opetopy.UnnamedOpetope.degen`           | :class:`opetopy.UnnamedOpetope.Degen`           |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{shift}`       | :func:`opetopy.UnnamedOpetope.shift`           | :class:`opetopy.UnnamedOpetope.Shift`           |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{graft}`       | :func:`opetopy.UnnamedOpetope.graft`           | :class:`opetopy.UnnamedOpetope.Graft`           |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| :math:`\textbf{OptSet${}^?$}`   | :math:`\texttt{point}`       | :func:`opetopy.UnnamedOpetopicSet.point`       | :class:`opetopy.UnnamedOpetopicSet.Point`       |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{degen}`       | :func:`opetopy.UnnamedOpetopicSet.degen`       | :class:`opetopy.UnnamedOpetopicSet.Degen`       |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{graft}`       | :func:`opetopy.UnnamedOpetopicSet.graft`       | :class:`opetopy.UnnamedOpetopicSet.Graft`       |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{shift}`       | :func:`opetopy.UnnamedOpetopicSet.shift`       | :class:`opetopy.UnnamedOpetopicSet.Shift`       |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+
| :math:`\textbf{OptCat${}^?$}`   | :math:`\texttt{tfill}`       | :func:`opetopy.UnnamedOpetopicCategory.tfill`  | :class:`opetopy.UnnamedOpetopicCategory.TFill`  |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{tuniv}`       | :func:`opetopy.UnnamedOpetopicCategory.tuniv`  | :class:`opetopy.UnnamedOpetopicCategory.TUniv`  |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{suniv}`       | :func:`opetopy.UnnamedOpetopicCategory.suniv`  | :class:`opetopy.UnnamedOpetopicCategory.SUniv`  |
+                                 +------------------------------+------------------------------------------------+-------------------------------------------------+
|                                 | :math:`\texttt{tclose}`      | :func:`opetopy.UnnamedOpetopicCategory.tclose` | :class:`opetopy.UnnamedOpetopicCategory.TClose` |
+---------------------------------+------------------------------+------------------------------------------------+-------------------------------------------------+


Usage
=====


Derivations and proof trees
---------------------------

A derivation / proof tree in any of those system can then be written as a Python
expression. If it evaluates without raising any exception, it is considered
valid.

For example, in system :math:`\textbf{Opt${}^?$}`, the unique :math:`1`-opetope
has the following expression:

.. code-block:: python

    from opetopy.UnnamedOpetope import *
    shift(point())


which indeed evaluates without raising exceptions.

The preferred way to construct proof trees is to use the proof tree node
classes (see table above), who act as instances of those rules. They behave as
their function counterparts, taking proof trees instead of sequents as
constructor arguments. Then, a proof tree can be evaluated with the
:func:`opetopy.common.AbstractRuleInstance.eval` method. For instance, the
proof tree described above is written as:

.. code-block:: python

    from opetopy.UnnamedOpetope import *
    proof = Shift(Point())


and evaluated as:

.. code-block:: python

    proof.eval()


which again evaluates without raising exceptions.


Exporting to :math:`\TeX`
-------------------------


`opetopy`'s main classes can be translated to :math:`\TeX` code using method
:func:`opetopy.common.AbstractRuleInstance.toTeX`. Here is the minimal template
to compile the returned code

.. code-block:: TeX

    \documentclass{article}

    \usepackage{amsmath}
    \usepackage{bussproofs}
    \usepackage{fdsymbol}
    \usepackage{MnSymbol}

    \newcommand{\degenopetope}[1]{\left\lbrace \!\! \opetope{#1} \right.}
    \newcommand{\opetope}[1]{\left\lbrace \begin{matrix*}[l] #1 \end{matrix*} \right.}
    \newcommand{\optOne}{\filledsquare}
    \newcommand{\optZero}{\filledlozenge}
    \newcommand{\sep}{\leftarrow}

    \begin{document}

    Your code here.

    \end{document}


Documentation
=============


.. toctree::

    common
    namedopetope
    namedopetopicset
    namedopetopicsetm
    unnamedopetope
    unnamedopetopicset
    unnamedopetopiccategory


.. [CHM19] Pierre-Louis Curien, Cédric Ho Thanh, and Samuel Mimram. Syntactic
    approaches to opetopes. arXiv:1903.05848
