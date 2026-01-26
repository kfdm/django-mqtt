_help:
    @just --list

# Format code with ruff
[group('dev')]
format:
    uvx ruff check --fix
    uvx ruff format

# Run Django management commands against example project
[group('dev')]
manage *args:
    uv run -m tests.example {{ args }}

# Run Django tests
[group('django')]
test *args:
    @just manage test {{ args }}

build:
    uv build --clear
