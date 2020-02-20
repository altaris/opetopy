PYTHON 			= python3.8

DIR_DOCS		= docs
DIR_OPETOPY		= opetopy
DIR_OUT     	= out
DIR_OUT_DOCS	= $(DIR_OUT)/docs
DIR_OUT_TEST	= $(DIR_OUT)/tests

TESTS			= 							\
	test_namedopetope_classic 				\
	test_namedopetope_point 				\
	test_namedopetopicset_example 			\
	test_namedopetopicsetm_example 			\
	test_unnamedopetope_arrow 				\
	test_unnamedopetope_classic 			\
	test_unnamedopetope_decision_valid 		\
	test_unnamedopetope_opetopicinteger 	\
	test_unnamedopetopiccategory_suniv 		\
	test_unnamedopetopiccategory_tclose 	\
	test_unnamedopetopiccategory_tfill 		\
	test_unnamedopetopiccategory_tuniv 		\
	test_unnamedopetopicset_arrow		 	\
	test_unnamedopetopicset_classic

all: typecheck unittest

.PHONY: docs
docs: tests
	sphinx-build -b html $(DIR_DOCS)/ $(DIR_OUT_DOCS)/html/
	-@xdg-open $(DIR_OUT_DOCS)/html/index.html

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 --verbose $(DIR_OPETOPY)

test_%:
	@mkdir -p $(DIR_OUT_TEST)
	$(PYTHON) -m tests.$@ > $(DIR_OUT_TEST)/$@.out

tests: $(TESTS)

.PHONY: typecheck
typecheck:
	mypy opetopy/*.py

.PHONY: unittest
unittest:
	@$(PYTHON) -m unittest discover --start-directory tests \
		--pattern "unittest*.py" --verbose
