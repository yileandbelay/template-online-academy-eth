.PHONY: setup check test lint fmt new-block
setup:      ## install everything
	uv sync --all-packages
test:       ## run all tests
	uv run pytest
lint:       ## lint, types, import boundaries
	uv run ruff check . && uv run ruff format --check . && uv run mypy backend/kernel/hulu_kernel backend/contracts/hulu_contracts tools/new_block/new_block $(wildcard backend/blocks/*/*/hulu_*) && uv run lint-imports
fmt:        ## format code
	uv run ruff format . && uv run ruff check . --fix
check: lint test   ## what CI runs
new-block:  ## make new-block ID=business.lms
	uv run new-block $(ID)
