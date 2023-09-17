help:
	@echo Developer commands for Spacetraders
	@echo
	@grep -E '^[ .a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo

install:  ## Install requirements ready for development
	poetry install
	createdb space_traders

mypy: ## Run a static syntax check
	poetry run mypy src/ cli.py

lint: ## Format the code correctly
	poetry run black .
	poetry run ruff --fix .

clear-caches:  ## Clear any cache files
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache

shell:  ## Run an ipython shell
	poetry run ipython

dbpatch:  ## Generate a new database patch automatically. Usage: make dbpatch message="my patch message"
	alembic revision -m "$(message)" --autogenerate

rebuild:  ## rebuild database from scratch
	dropdb space_traders
	createdb space_traders
	alembic upgrade head

upgradedb:  ## Upgrade the database with the latest db patches
	alembic upgrade head

query:  ## Run various queries against the CLI file. Use like `make query q="me"`
	poetry run python cli.py $(q)

automate:  ## Run the automation loop
	poetry run python cli.py loop

mining_loop:  ## Set a specific ship on a mining loop
	poetry run python cli.py mining $(q)

contract_loop:  ## Set up a specific ship to fulfill a contract
	poetry run python cli.py contract-mining $(q)

web:  ## Run the server
	python server.py run
