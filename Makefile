.PHONY: test flake build install clean

test:
	python -m unittest tests/*.py

flake:
	flake8 --max-line-length 100 src/*.py tests/*.py

build:
	python -m build --sdist --wheel

install: build
	python -m pip install --no-binary :all: dist/strava-cli-0.1.tar.gz

binary:
	pyinstaller --noconfirm src/parse.py
	mv dist/parse/parse dist/parse/strava-cli
	mv dist/parse dist/binary

clean:
	rm -rf build/ dist/ strava-cli.egg-info
