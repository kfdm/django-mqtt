.PHONY:	test build clean format
.DEFAULT: test

test:
	uv run -m tests.example -v 2

build:
	uv build

clean:
	rm -rf dist

################################################################################
# Formatting
################################################################################
format:
	uvx ruff check
	uvx ruff format
