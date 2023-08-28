init:
	pip install -r requirements-dev.txt
	pip install -e .

all: format lint install test build

format:
	black src tests

lint:
	flake8 src tests

install:
	pip install -e .

test:
	pytest --cov=src tests/ --cov-branch --cov-fail-under=95 --cov-report term-missing

build:
	python -m build
	