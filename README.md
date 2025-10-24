# Advanced Calculator

This project implements an advanced calculator CLI with design patterns (Factory, Memento, Observer),
undo/redo, logging, autosave, CSV persistence using pandas, and unit tests.

## Setup

Create and activate a virtualenv:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add a `.env` file (an example is provided as `.env.example`) or copy `.env.example` to `.env`.

## Usage

Run the REPL:
```bash
python -m app.calculator
```

Commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff,
history, clear, undo, redo, save, load, help, exit

## Testing

Run tests with:
```bash
pytest --cov=app --cov-fail-under=90
```

## CI

A GitHub Actions workflow is included in `.github/workflows/python-app.yml`.
