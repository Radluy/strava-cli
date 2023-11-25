test:
	python -m unittest tests/*.py

flake:
	flake8 --max-line-length 100 src/*.py tests/*.py

build:
	python -m build

install: build
	python -m pip install --force-reinstall dist/strava_cli-0.1-py3-none-any.whl
