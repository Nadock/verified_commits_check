.PHONY: black black-check pytest pylint mypy

setup:
	pipenv install --dev

black:
	pipenv run black ./src

black-check:
	pipenv run black --check ./src

pytest:
	pipenv run pytest

pylint:
	pipenv run pylint src

mypy:
	pipenv run mypy src

docker-build:
	docker build -t verified_commits_alert .
