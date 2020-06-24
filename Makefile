.PHONY: black black-check pytest pylint mypy

black:
	black ./src

black-check:
	black --check ./src

pytest:
	cd ./src && pytest

pylint:
	pylint src

mypy:
	mypy ./src
