_help:
    @just --list

# Format code with ruff
[group('dev')]
format:
    just --fmt
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

# Build for release
[group('dev')]
build:
    uv build --clear

# Review checks for release
[group('dev')]
review *args:
    uv run repo-review {{ args }}
