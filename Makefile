install:
	pip install -U pip
	pip install -r requirements.txt

test:
	pytest -q

lint:
	flake8 src tests

fmt:
	black src tests
	isort src tests

run:
	python -m audio2text $(ARGS)
