RUN 		= python3
TYPECHECK	= mypy

all: typecheck unittests

.PHONY: doc
doc:
	cd doc && make html
	-xdg-open doc/build/html/index.html

.PHONY: unittests
unittests:
	python3 -m unittest discover --start-directory tests --verbose

.PHONY: typecheck
typecheck:
	$(TYPECHECK) NamedOpetope.py
	$(TYPECHECK) NamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetope.py
	$(TYPECHECK) UnnamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetopicCategory.py
	$(TYPECHECK) tests/*.py
