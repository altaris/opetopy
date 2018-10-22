RUN 		= python3
TYPECHECK	= mypy

all: typecheck unittests

.PHONY: doc
doc:
	cd doc && make html

.PHONY: unittests
unittests: typecheck
	$(RUN) UnitTests.py

.PHONY: typecheck
typecheck:
	$(TYPECHECK) NamedOpetope.py
	$(TYPECHECK) NamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetope.py
	$(TYPECHECK) UnnamedOpetopicSet.py