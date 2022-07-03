APP_BIN := .venv/bin/django-admin
PIP_BIN := .venv/bin/pip
PYTHON_BIN := .venv/bin/python

.PHONY:	test build check clean
.DEFAULT: test

test: ${APP_BIN}
	${PYTHON_BIN} -m tests.example -v 2

$(PIP_BIN):
	python3 -m venv .venv

${APP_BIN}: $(PIP_BIN)
	${PIP_BIN} install -e .

build: $(PIP_BIN)
	${PYTHON_BIN} setup.py sdist

clean:
	rm -rf .venv dist
