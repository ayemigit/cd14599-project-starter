# Flashcard Quizzer

A CLI flashcard study tool supporting sequential, random, and adaptive quiz modes.

## Setup

```bash
cd flashcard-quizzer
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py -f <path-to-json> [-m <mode>] [--stats]
```

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-f FILE` | Path to flashcard JSON file (required) | — |
| `-m MODE` | Quiz mode: `sequential`, `random`, `adaptive` | `sequential` |
| `--stats` | Show card stats and exit | — |

### Examples

```bash
# Sequential quiz with python basics
python main.py -f data/python_basics.json

# Random mode with server acronyms
python main.py -f data/server_acronyms.json -m random

# Adaptive mode
python main.py -f data/python_basics.json -m adaptive

# Show stats only
python main.py -f data/python_basics.json --stats
```

## Flashcard JSON Formats

**Array format:**
```json
[
  { "question": "What is X?", "answer": "Y" }
]
```

**Object format:**
```json
{
  "cards": [
    { "question": "What is X?", "answer": "Y" }
  ]
}
```

Cards may also use `"front"` / `"back"` instead of `"question"` / `"answer"`.

## Quiz Modes

- **sequential** — Cards in file order
- **random** — Cards in shuffled order
- **adaptive** — Weights cards by difficulty; missed cards appear more often

## Running Tests

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=term-missing
```

## Code Quality

```bash
black .
flake8 .
mypy main.py quiz_engine.py utils/file_handler.py
```

## Project Structure

```
flashcard-quizzer/
├── main.py
├── quiz_engine.py
├── requirements.txt
├── READme.md
├── utils/
│   ├── __init__.py
│   └── file_handler.py
├── tests/
│   ├── __init__.py
│   ├── test_flashcard_loader.py
│   ├── test_quiz_modes.py
│   └── test_integration.py
├── data/
│   ├── python_basics.json
│   └── server_acronyms.json
└── docs/
    └── ai_edit_log.md
```
