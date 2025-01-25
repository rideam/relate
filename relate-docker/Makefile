start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker compose up

stop: ## Stop Containers
	@docker compose down -v

restart: stop start ## Restart Containers

start-bg:  ## Run containers in the background
	@docker compose up -d

build: ## Build Containers
	@docker compose build

ssh: ## SSH into running web container
	@docker compose exec web bash

superuser: ## Create super user
	@docker compose exec web poetry run python manage.py createsuperuser

migrations: ## Create DB migrations in the container
	@docker compose exec web poetry run python manage.py makemigrations

migrate: ## Run DB migrations in the container
	@docker compose exec web poetry run python manage.py migrate

shell: ## Get a Django shell
	@docker compose exec web poetry run python manage.py shell

static: ## Collect static
	@docker compose exec web sh collectstatic.sh

collectstatic: ## Collect static
	@docker compose exec web poetry run python manage.py collectstatic

dbshell: ## Get a Database shell
	@docker compose exec db psql -U postgres relate

test: ## Run Django tests
	@docker compose exec web poetry run python manage.py test

init: start-bg migrations migrate  ## Quickly get up and running (start containers and migrate DB)

black: ## Runs black on the codebase
	@docker compose exec web black --extend-exclude migrations --line-length 120 .

isort: ## Runs isort on the codebase
	@docker compose exec web isort -l 120 --profile black .

format: black isort ## Runs formatting (black and isort)n on the codebase

npm-install: ## Runs npm install in the container
	@docker compose exec web npm install

npm-build: ## Runs npm build in the container (for production assets)
	@docker compose exec web npm run build

npm-dev: ## Runs npm dev in the container
	@docker compose exec web npm run dev

npm-watch: ## Runs npm watch in the container (recommended for dev)
	@docker compose exec web npm run dev-watch

npm-type-check: ## Runs the type checker on the front end TypeScript code
	@docker compose exec web npm run type-check

upgrade: build start-bg migrations migrate npm-install

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
