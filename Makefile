.PHONY: help create-venv activate-venv install clean

help:
	@echo "  make docker-up      - Start API"
	@echo "  make run-test       - Run test"
	@echo "  make run-cov        - Run test and display coverage report"
	@echo "  make run-lint       - Run linters"
	@echo "  make run-mypy       - Run mypy tool"

docker-up:
	sudo docker-compose build --no-cache
	sudo docker-compose up -d

run-test:
	docker-compose run --rm chatgpt-feedback pytest $(FILE)

run-cov:
	docker-compose run --rm chatgpt-feedback pytest --cov=chatgpt-feedback app/

run-lint:
	docker-compose run --rm chatgpt-feedback flake8 $(FILE)

run-mypy:
	docker-compose run --rm chatgpt-feedback mypy $(FILE)
