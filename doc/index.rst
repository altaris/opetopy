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
presented in [CHM18]_ and some other work in progress.

The :mod:`opetopy` module is decomposed as follow:

+---------------------------+------------------------+-------------------------------+
| Module                    | Syntactical construct  | Derivation system             |
+===========================+========================+===============================+
| :mod:`NamedOpetope`       | Named opetopes         | :math:`\textbf{Opt${}^!$}`    |
+---------------------------+------------------------+-------------------------------+
| :mod:`NamedOpetopicSet`   | Named opetopic sets    | :math:`\textbf{OptSet${}^!$}` |
+---------------------------+------------------------+-------------------------------+
| :mod:`UnnamedOpetope`     | Unnamed opetopes       | :math:`\textbf{Opt${}^?$}`    |
+---------------------------+------------------------+-------------------------------+
| :mod:`UnnamedOpetopicSet` | Unnamed opetopic sets  | :math:`\textbf{OptSet${}^?$}` |
+---------------------------+------------------------+-------------------------------+

Each implement the following:

1. the syntactical constructs required to describe opetopes / opetopic sets and their sequents;
2. the derivation rules of the relevant system;
3. wrappers of those rules to describe proof trees.

+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+
| Derivation system             | Rule                        | Implementation                         | Proof tree node                          |
+===============================+=============================+========================================+==========================================+
| :math:`\textbf{Opt${}^!$}`    | :math:`\texttt{point}`      | :func:`NamedOpetope.point`             | :class:`NamedOpetope.Point`              |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{degen}`      | :func:`NamedOpetope.degen`             | :class:`NamedOpetope.Degen`              |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{degen-fill}` | :func:`NamedOpetope.degenfill`         | :class:`NamedOpetope.DegenFill`          |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{fill}`       | :func:`NamedOpetope.fill`              | :class:`NamedOpetope.Fill`               |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{graft}`      | :func:`NamedOpetope.graft`             | :class:`NamedOpetope.Graft`              |
+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+
| :math:`\textbf{OptSet${}^!$}` | :math:`\texttt{repr}`       | :func:`NamedOpetopicSet.repres`        | :class:`NamedOpetopicSet.Repr`           |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{zero}`       | :func:`NamedOpetopicSet.zero`          | :class:`NamedOpetopicSet.Zero`           |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{sum}`        | :func:`NamedOpetopicSet.sum`           | :class:`NamedOpetopicSet.Sum`            |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{glue}`       | :func:`NamedOpetopicSet.glue`          | :class:`NamedOpetopicSet.Glue`           |
+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+
| :math:`\textbf{Opt${}^?$}`    | :math:`\texttt{point}`      | :func:`UnnamedOpetope.point`           | :class:`UnnamedOpetope.Point`            |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{degen}`      | :func:`UnnamedOpetope.degen`           | :class:`UnnamedOpetope.Degen`            |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{shift}`      | :func:`UnnamedOpetope.shift`           | :class:`UnnamedOpetope.Shift`            |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{graft}`      | :func:`UnnamedOpetope.graft`           | :class:`UnnamedOpetope.Graft`            |
+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+
| :math:`\textbf{OptSet${}^?$}` | :math:`\texttt{point}`      | :func:`UnnamedOpetopicSet.point`       | :class:`UnnamedOpetopicSet.Point`        |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{degen}`      | :func:`UnnamedOpetopicSet.degen`       | :class:`UnnamedOpetopicSet.Degen`        |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{graft}`      | :func:`UnnamedOpetopicSet.graft`       | :class:`UnnamedOpetopicSet.Graft`        |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{fill}`       | :func:`UnnamedOpetopicSet.fill`        | :class:`UnnamedOpetopicSet.Fill`         |
+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+
| :math:`\textbf{OptCat${}^?$}` | :math:`\texttt{tfill}`      | :func:`UnnamedOpetopicCategory.tfill`  | :class:`UnnamedOpetopicCategory.TFill`   |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{tuniv}`      | :func:`UnnamedOpetopicCategory.tuniv`  | :class:`UnnamedOpetopicCategory.TUniv`   |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{suniv}`      | :func:`UnnamedOpetopicCategory.suniv`  | :class:`UnnamedOpetopicCategory.SUniv`   |
+                               +-----------------------------+----------------------------------------+------------------------------------------+
|                               | :math:`\texttt{tclose}`     | :func:`UnnamedOpetopicCategory.tclose` | :class:`UnnamedOpetopicCategory.TClose`  |
+-------------------------------+-----------------------------+----------------------------------------+------------------------------------------+


Usage
=====


Derivations and proof trees
---------------------------

A derivation / proof tree in any of those system can then be written as a Python expression. If it evaluates without raising the :python:`ValueError` exceptions, it is considered correct.

For example, in system :math:`\textbf{Opt${}^?$}`, the unique :math:`1`-opetope has the following expression:

.. code-block:: python

    from UnnamedOpetope import *
    shift(point())


which indeed evaluates without raising exceptions.

The preferred way to construct proof trees is to use the proof tree node classes (see table above), who act as instances of those rules. They behave as their function counterparts, taking proof trees instead of sequents as constructor arguments. Then, a proof tree can be evaluated with the :func:`eval` method. For instance, the proof tree described above is written as:

.. code-block:: python

    from UnnamedOpetope import *
    proof = Shift(Point())


and evaluated as:

.. code-block:: python

    proof.eval()


which again evaluates without raising exceptions.


Exporting to :math:`\TeX`
-------------------------


:mod:`opetopy`'s main classes can be translated to :math:`\TeX` code using method :func:`toTeX`. Here is the minimal template to compile the returned code

.. code-block:: TeX

    \documentclass{article}

    \usepackage{amsmath}
    \usepackage{bussproofs}
    \usepackage{fdsymbol}
    \usepackage{MnSymbol}

    \newcommand{\degenopetope}[1]{\left\lbrace \!\! \opetope{#1} \right.}
    \newcommand{\opetope}[1]{\left\lbrace \begin{matrix*}[l] #1 \end{matrix*} \right.}
    \newcommand{\optOne}{\mbox{\raisebox{.01cm}{\tiny $\blacksquare$}}}
    \newcommand{\optZero}{\mbox{\raisebox{.01cm}{\scriptsize $\blacklozenge$}}}
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
    unnamedopetope
    unnamedopetopicset
    unnamedopetopiccategory


.. [CHM18] Pierre-Louis Curien, Cédric Ho Thanh, and Samuel Mimram. Type theoretical approaches to opetopes. In preparation.