.PHONY: format lint typecheck test coverage coverage-html all develop

VENV_DIR := .venv
REQ := requirements.txt requirements-dev.txt
STAMP := $(VENV_DIR)/.install-stamp

ifeq ($(OS),Windows_NT)
    PYTHON := $(VENV_DIR)\Scripts\python.exe
    PIP := $(VENV_DIR)\Scripts\pip.exe
    BLACK := $(VENV_DIR)\Scripts\black.exe
    ISORT := $(VENV_DIR)\Scripts\isort.exe
    FLAKE8 := $(VENV_DIR)\Scripts\flake8.exe
    MYPY := $(VENV_DIR)\Scripts\mypy.exe
    COVERAGE := $(VENV_DIR)\Scripts\coverage.exe
    PYTEST := $(VENV_DIR)\Scripts\pytest.exe
    MKDIR_P := if not exist $(VENV_DIR) mkdir $(VENV_DIR)
    TOUCH := type nul > $(STAMP)
else
    PYTHON := $(VENV_DIR)/bin/python
    PIP := $(VENV_DIR)/bin/pip
    BLACK := $(VENV_DIR)/bin/black
    ISORT := $(VENV_DIR)/bin/isort
    FLAKE8 := $(VENV_DIR)/bin/flake8
    MYPY := $(VENV_DIR)/bin/mypy
    COVERAGE := $(VENV_DIR)/bin/coverage
    PYTEST := $(VENV_DIR)/bin/pytest
    MKDIR_P := mkdir -p $(VENV_DIR)
    TOUCH := touch $(STAMP)
endif

$(STAMP): $(REQ)
	@echo Setting up virtual environment...
	@$(MKDIR_P)
	@python -m venv $(VENV_DIR)
	@$(PIP) install -r requirements.txt -r requirements-dev.txt
	@$(TOUCH)

develop: $(STAMP)

format: develop
	$(BLACK) goban tests
	$(ISORT) goban tests

lint: develop
	$(FLAKE8) goban tests
	$(ISORT) --check-only goban tests

typecheck: develop
	$(MYPY) goban

coverage: develop
	$(COVERAGE) run -m pytest  || @echo "Tests failed, coverage report will be incomplete"
	$(COVERAGE) report

coverage-html: develop
	$(COVERAGE) run -m pytest || @echo "Tests failed, coverage report will be incomplete"
	$(COVERAGE) html
	@echo HTML report at htmlcov/index.html

test: develop
	$(PYTEST)

all: format lint typecheck test coverage
