PYTHON = python3
VPYTHON = .venv/bin/python
VENV = .venv

install: $(VENV)
	@echo "Installing dependencies..."
	$(VPYTHON) -m pip install --upgrade pip
	$(VPYTHON) -m pip install -e ".[dev]"

$(VENV):
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created in $(VENV)"
	@echo "Activate it in terminal with: source $(VENV)/bin/activate"

venv: $(VENV)

run: install
	@echo "Generating the maze and finding the shortest path..."
	$(VPYTHON) a_maze_ing.py config.txt

debug: install
	@echo "Enable debug mode..."
	$(VPYTHON) -m pdb a_maze_ing.py config.txt

clean:
	@echo "Cleaning files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info $(VENV)

lint: install
	$(VPYTHON) -m flake8 mazegen a_maze_ing.py
	$(VPYTHON) -m mypy mazegen a_maze_ing.py --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	$(VPYTHON) -m flake8 mazegen a_maze_ing.py
	$(VPYTHON) -m mypy mazegen a_maze_ing.py --strict

build: install
	@echo "Building packages..."
	$(VPYTHON) -m build

.PHONY: install venv run debug clean lint lint-strict build
