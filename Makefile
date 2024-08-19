VENV_DIR := .venv
APP_BIN := $(VENV_DIR)/bin/django-admin
PIP_BIN := $(VENV_DIR)/bin/pip
PYTHON_BIN := $(VENV_DIR)/bin/python
SYSTEM_PYTHON ?= python3.9

.PHONY:	test build check clean format
.DEFAULT: test

test: $(APP_BIN)
	$(PYTHON_BIN) -m tests.example -v 2

$(PIP_BIN):
	$(SYSTEM_PYTHON) -m venv $(VENV_DIR)

$(APP_BIN): $(PIP_BIN)
	$(PIP_BIN) install -e .

build: $(PIP_BIN)
	$(PYTHON_BIN) setup.py sdist

clean:
	rm -rf $(VENV_DIR) dist

################################################################################
# Formatting
################################################################################
RUFF_BIN := $(VENV_DIR)/bin/ruff
$(RUFF_BIN): $(PIP_BIN)
	$(PIP_BIN) install ruff

format: $(RUFF_BIN)
	$(RUFF_BIN) check
	$(RUFF_BIN) format
