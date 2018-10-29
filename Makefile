RUN 		= python3
TYPECHECK	= mypy

all: typecheck unittests

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
	$(TYPECHECK) UnnamedOpetopicCategory.py
	$(TYPECHECK) UnitTests.py