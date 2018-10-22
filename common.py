# -*- coding: utf-8 -*-

"""
.. module:: opetopy.common
   :synopsis: Some utilities and global definitions

.. moduleauthor:: Cédric HT

"""

from typing import Any


class AbstractRuleInstance:
    """
    Abstract class representing a rule instance in a proof tree.
    """

    def _toTex(self) -> str:
        raise NotImplementedError()

    def eval(self) -> Any:
        """
        Pure virtual method evaluating a proof tree and returning the final
        conclusion sequent, or raising an exception if the proof is invalid.
        """
        raise NotImplementedError()

    def toTex(self) -> str:
        """
        Converts the proof tree in TeX code.
        """
        return "\\begin{prooftree}\n\t" + self._toTex() + "\n\\end{prooftree}"
