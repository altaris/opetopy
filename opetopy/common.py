# -*- coding: utf-8 -*-

"""
.. module:: common
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


class DerivationError(Exception):
    """
    This exception is raised whenever an illegal operation on syntactical
    constructs relevant to opetopes is performed.
    """

    def __init__(self, scope: str, message: str, **kwargs) -> None:
        self.message = message.format(**kwargs)
        self.scope = scope
        super().__init__(self, message)

    def __str__(self):
        return "[{scope}] {msg}".format(scope=self.scope, msg=self.message)
