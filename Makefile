RUN 		= python3
TYPECHECK	= mypy

TESTOUTDIR	= doc/build/tests

TESTFILES	= \
	test_namedopetope_classic \
	test_namedopetope_point \
	test_namedopetopicset_example \
	test_namedopetopicsetm_example \
	test_unnamedopetope_arrow \
	test_unnamedopetope_classic \
	test_unnamedopetope_decision_valid \
	test_unnamedopetope_opetopicinteger \
	test_unnamedopetopiccategory_suniv \
	test_unnamedopetopiccategory_tclose \
	test_unnamedopetopiccategory_tfill \
	test_unnamedopetopiccategory_tuniv \
	test_unnamedopetopicset_arrow \
	test_unnamedopetopicset_classic

all: typecheck unittest

.PHONY: doc
doc: $(TESTFILES)
	cd doc && make html
	-xdg-open doc/build/html/index.html

test_%:
	@mkdir -p $(TESTOUTDIR)
	@echo
	@echo "----------------------------------------"
	@echo $@
	@echo "----------------------------------------"
	@echo
	@$(RUN) -m tests.$@ | tee $(TESTOUTDIR)/$@.out

test: $(TESTFILES)

.PHONY: typecheck
typecheck:
	$(TYPECHECK) opetopy/NamedOpetope.py
	$(TYPECHECK) opetopy/NamedOpetopicSet.py
	$(TYPECHECK) opetopy/NamedOpetopicSetM.py
	$(TYPECHECK) opetopy/UnnamedOpetope.py
	$(TYPECHECK) opetopy/UnnamedOpetopicSet.py
	$(TYPECHECK) opetopy/UnnamedOpetopicCategory.py

.PHONY: unittest
unittest:
	@$(RUN) -m unittest discover --start-directory tests --pattern "unittest*.py" --verbose
