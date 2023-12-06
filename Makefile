.PHONY: test flake build install clean

test:
	python -m unittest tests/*.py

flake:
	flake8 --max-line-length 100 src/*.py tests/*.py

build:
	python -m build --sdist --wheel

install: build
	python -m pip install --no-binary :all: dist/strava-cli-0.1.tar.gz

clean:
	rm -rf build/ dist/ strava-cli.egg-info
