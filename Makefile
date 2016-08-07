.PHONY: all clean build install uninstall test

all: clean

clean:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete
	find . -name \*~ -delete
	rm -rf dist sulley.egg-info

build:
	python setup.py sdist

install:
	pip install dist/sulley-*.tar.gz

uninstall:
	yes | pip uninstall sulley

pylint: ; @for py in sulley/*.py; do echo "Linting $$py"; pylint --list-msgs -rn $$py; done

test:
	python -m unittest discover -s ./tests -p 'test_*.py'

push:
	python setup.py sdist upload -r pypi
