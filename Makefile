test:
	python -m unittest tests/*.py
flake:
	flake8 --max-line-length 100 src/*.py tests/*.py
