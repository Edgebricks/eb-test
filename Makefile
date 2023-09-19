# Copyright (c) 2021-2023 Edgebricks Inc.
#
# Targets:
#   clean: clean generated files
#   codechecks: runs fmt, lint, staticchecks and vet targets/tools.
#   run-tests: runs ebapi and ebui tests
#   print-[VARIABLE]: good for debugging and testing variables.

SHELL := /bin/bash

# Figure out git repository details.
export GITREPO = $(shell git rev-parse --show-toplevel)
GITCOMMIT = $(shell git rev-parse HEAD)
GITBRANCH = $(shell git symbolic-ref --short HEAD)

export CURR_TIME_STAMP = $(shell date +%m.%d.%G:%T)

ifndef WORKSPACE
# WORKSPACE will have a / at the end
export WORKSPACE = $(dir $(abspath $(CURDIR)))
endif

# With this you can print the value of any makefile variable by doing
# make print-VARIABLENAME
print-%  : ; @echo $* = $($*)

# check and install dependencies
check-flake8:
	(which flake8) >/dev/null || (pip3 install flake8) >/dev/null
check-black:
	(which black) >/dev/null || (pip3 install black) >/dev/null
check-pylint:
	(which pylint) >/dev/null || (pip3 install pylint) >/dev/null

# We use black for fixing flake8 issues.
# Black is a PEP 8 compliant opinionated formatter.
fix-flake8-errors: check-black
	@echo -e "* \e[0;34mFixing obvious flake8 issues...\e[m"
	black doc/
	black ebapi/
	black ebui/
	@echo -e "* \e[0;34mFixed obvious flake8 issues\e[m"

# Flake8 is a Python linting tool that checks your Python codebase for
# errors, styling issues and complexity.
flake8: check-flake8
	@echo -e "* \e[0;32mRunning flake8\e[m"
	flake8 .
	@$(MAKE) -s fix-flake8-errors
	@echo -e "* \e[0;32mFinished flake8\e[m"

# Pylint is a static code analysis tool for the Python programming language.
# It is named following a common convention in Python of a "py" prefix, and
# a nod to the C programming lint program. It follows the style recommended
# by PEP 8, the Python style guide. It is similar to Pychecker and Pyflakes,
# but includes the following features:
# -> Checking the length of each line
# -> Checking that variable names are well-formed according to the project's
#    coding standard
# -> Checking that declared interfaces are truly implemented.[5]
pylint: check-pylint
	@echo -e "* \e[0;32mRunning pylint\e[m"
	pylint --recursive=y .
	@echo -e "* \e[0;32mFinished pylint\e[m"

# checks code formatting and linting issues
codechecks:
	@echo -e "* \e[0;33mRunning codechecks\e[m"
	@$(MAKE) -s flake8
	@$(MAKE) -s pylint
	@echo -e "* Finished \e[0;33mRunning codechecks\e[m"

clean-ui-pytest:
	(find ebui/ -type d -name assets -exec rm -rf {} +) >/dev/null
	(find ebui/ -type d -name .pytest_cache -exec rm -rf {} +) >/dev/null
	@echo -e "* \e[0;33mRemoved ui pytest cache files\e[m"

clean-api-pytest:
	(find ebapi/ -type d -name assets -exec rm -rf {} +) >/dev/null
	(find ebapi/ -type d -name .pytest_cache -exec rm -rf {} +) >/dev/null
	@echo -e "* \e[0;33mRemoved api pytest cache files\e[m"

clean-ui-pycache:
	(find ebui/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete) >/dev/null
	@echo -e "* \e[0;33mRemoved ui python cache files\e[m"

clean-api-pycache:
	(find ebapi/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete) >/dev/null
	@echo -e "* \e[0;33mRemoved api python cache files\e[m"

clean-ui:
	@$(MAKE) -s clean-ui-pytest
	@$(MAKE) -s clean-ui-pycache

clean-api:
	@$(MAKE) -s clean-api-pytest
	@$(MAKE) -s clean-api-pycache

clean:
	@$(MAKE) -s clean-api
	@$(MAKE) -s clean-ui

run-api-tests:
	@$(MAKE) -s clean-api
	@echo -e "* \e[0;33mRunning api tests\e[m"
	python3 -m pytest ebapi/tests/bu
	python3 -m pytest ebapi/tests/project
	python3 -m pytest ebapi/tests/vm

run-ui-tests:
	@$(MAKE) -s clean-api
	@echo -e "* \e[0;33mRunning ui tests\e[m"
	python3 -m pytest ebapi/tests -s

run-tests:
	@$(MAKE) -s run-api-tests
	@$(MAKE) -s run-ui-tests