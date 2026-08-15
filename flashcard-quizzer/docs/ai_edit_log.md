# AI Edit Log

## Entry 1 — 2026-08-15
**Action:** Project scaffolding  
**Prompt:** Create complete flashcard quizzer CLI application structure  
**Changes:** Created directory structure: `utils/`, `tests/`, `data/`, `docs/`  
**Outcome:** All directories created successfully

## Entry 2 — 2026-08-15
**Action:** CLI entry point created  
**Prompt:** Implement `main.py` with argparse flags `-f`, `-m`, `--stats`  
**Changes:** Created `main.py` with argument parsing, `show_stats()`, and `run_quiz()` functions  
**Outcome:** CLI supports sequential, random, and adaptive quiz modes with optional stats display

## Entry 3 — 2026-08-15
**Action:** File handler utility created  
**Prompt:** Implement `utils/file_handler.py` with `load_flashcards()` supporting array and object JSON formats  
**Changes:** Created `utils/file_handler.py` with dual-format support and `sys.exit()` error handling  
**Outcome:** Handles both `[{...}]` and `{"cards":[...]}` formats; exits cleanly on errors

## Entry 4 — 2026-08-15
**Action:** Quiz engine implemented  
**Prompt:** Implement `quiz_engine.py` using Strategy Pattern (ABC subclasses) and Factory Pattern (dict registry)  
**Changes:** Created `QuizMode` ABC with `SequentialMode`, `RandomMode`, `AdaptiveMode` subclasses and `quiz_mode_factory()`  
**Outcome:** All three modes functional; adaptive mode uses weight-based card selection with result feedback

## Entry 5 — 2026-08-15
**Action:** Test suite created  
**Prompt:** Write pytest tests for file loader, quiz modes, and integration  
**Changes:** Created `tests/test_flashcard_loader.py`, `tests/test_quiz_modes.py`, `tests/test_integration.py`  
**Outcome:** 18 tests covering valid/invalid JSON loading, all quiz modes, adaptive weight behavior, and end-to-end sessions

## Entry 6 — 2026-08-15
**Action:** Sample data and documentation added  
**Prompt:** Create sample flashcard JSON files, README, and requirements  
**Changes:** Created `data/python_basics.json` (8 cards, array format), `data/server_acronyms.json` (5 cards, object format), `README.md`, `requirements.txt`  
**Outcome:** Project is fully functional and ready for use
