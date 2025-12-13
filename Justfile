_help:
    @just --list

test:
    uv run -m tests.example -v 2

build:
    uv build --clear

format:
    uvx ruff check --fix
    uvx ruff format
