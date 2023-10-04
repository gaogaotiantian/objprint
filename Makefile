refresh: clean build install lint

build:
	python -m build	

install: 
	pip install .	

build_dist:
	make clean
	python -m build
	pip install dist/*.whl
	make test

release:
	python -m twine upload dist/*

lint:
	flake8 --exclude src/objprint/executing src/ tests/ --count --max-line-length=127 --ignore=W503
	mypy src/ --exclude src/objprint/executing --follow-imports=skip

test:
	python -m unittest

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf src/objprint/__pycache__
	rm -rf build
	rm -rf dist
	rm -rf objprint.egg-info 
	rm -rf src/objprint.egg-info
	pip uninstall -y objprint || true
