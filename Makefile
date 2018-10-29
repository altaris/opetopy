RUN 		= python3
TYPECHECK	= mypy

TESTOUT		= doc/build/tests

TESTS 		= \
	test_namedopetope_classic \
	test_namedopetope_point \
	test_namedopetopicset_example \
	test_unnamedopetope_arrow \
	test_unnamedopetope_classic \
	test_unnamedopetope_decision_valid \
	test_unnamedopetope_opetopicinteger \
	test_unnamedopetopicset_arrow \
	test_unnamedopetopicset_classic

all: typecheck unittests

.PHONY: doc
doc: $(TESTS)
	cd doc && make html
	-xdg-open doc/build/html/index.html

test_%:
	@mkdir -p $(TESTOUT)
	@echo 
	@echo "----------------------------------------"
	@echo $@
	@echo "----------------------------------------"
	@echo
	@$(RUN) -m tests.$@ | tee $(TESTOUT)/$@.out

tests: $(TESTS)

.PHONY: typecheck
typecheck:
	$(TYPECHECK) NamedOpetope.py
	$(TYPECHECK) NamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetope.py
	$(TYPECHECK) UnnamedOpetopicSet.py
	$(TYPECHECK) UnnamedOpetopicCategory.py
	$(TYPECHECK) tests/*.py

.PHONY: unittests
unittests:
	python3 -m unittest discover --start-directory tests --pattern "unittest*.py" --verbose
