.PHONY: test flake build install clean

test:
	python -m unittest tests/*.py

flake:
	flake8 --max-line-length 100 src/*.py tests/*.py

build:
	python -m build --sdist --wheel

install: build
	python -m pip install --force-reinstall dist/strava_cli-0.1-py3-none-any.whl

clean:
	rm -rf build/ dist/ strava-cli.egg-info
