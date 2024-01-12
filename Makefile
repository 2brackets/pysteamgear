.PHONY: install install-dev test lint clean venv

install:
	pip install .

install-dev:
	pip install .[dev]
	pip install -r requirements-dev.txt

test:
	python -m unittest discover tests/  # Adjust 'tests/' if your tests are in a different directory

lint:
	pylint pysteamgear/  # Replace 'pysteamgear/' with the path to your Python package or module

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

venv:
	python -m venv venv
	. venv/bin/activate

docs:
	cd docs && make html