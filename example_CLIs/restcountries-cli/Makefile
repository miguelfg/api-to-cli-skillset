.PHONY: install test lint format run-help countries-help

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

lint:
	python -m py_compile src/*.py src/commands/*.py

format:
	@echo "No formatter configured."

run-help:
	python -m src.cli --help

countries-help:
	python -m src.cli countries --help
