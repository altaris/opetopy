RUN 		= python3
TYPECHECK	= mypy

all: typecheck unittests

.PHONY: coverage
coverage:
	coverage run UnitTests.py > /dev/null
	coverage html
	-xdg-open htmlcov/index.html

.PHONY: doc
doc:
	cd doc && make html
	-xdg-open doc/build/html/index.html

.PHONY: unittests
unittests:
	$(RUN) UnitTests.py

.PHONY: typecheck
typecheck:
	$(TYPECHECK) NamedOpetope.py
	$(TYPECHECK) NamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetope.py
	$(TYPECHECK) UnnamedOpetopicSet.py
	$(TYPECHECK) UnitTests.py