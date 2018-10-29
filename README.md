opetopy
=======

[![Build status](https://travis-ci.com/altaris/opetopy.svg?branch=master)](https://travis-ci.com/altaris/opetopy)
[![Coverage Status](https://coveralls.io/repos/github/altaris/opetopy/badge.svg?branch=master)](https://coveralls.io/github/altaris/opetopy?branch=master)
[![Documentation](https://readthedocs.org/projects/opetopy/badge/?version=latest)](https://opetopy.readthedocs.io/en/latest/)
![Python 3](https://badgen.net/badge/Python/3/blue)
[![MIT License](https://badgen.net/badge/license/MIT/blue)](https://choosealicense.com/licenses/mit/)

# Introduction

This project is the Python implementation of the opetope derivation systems
presented in **Type theoretical approaches to opetopes**, by [Pierre-Louis Curien](https://www.irif.fr/~curien/), [Cédric Ho Thanh](https://chothanh.wordpress.com/), and [Samuel Mimram](http://www.lix.polytechnique.fr/Labo/Samuel.Mimram/), and some other work in progress.

# Documentation

Available at [readthedocs.io](https://readthedocs.io/en/latest/?badge=latest).

Generating the documentation requires [Sphinx](http://www.sphinx-doc.org/en/stable/). After running

```sh
    make doc
```

the HTML documentation should be located at `doc/build/html/index.html`.

# Tests

Unit tests are written in [UnitTests.py](UnitTests.py), and can executed by running

```sh
    make unittests
```

Additionaly, the code can be typechecked with [mypy](http://mypy-lang.org/) (according to [PEP484](https://www.python.org/dev/peps/pep-0484/)) by running

```sh
    make typecheck
```
