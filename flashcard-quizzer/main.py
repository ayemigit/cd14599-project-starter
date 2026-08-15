import argparse
import sys
from utils.file_handler import load_flashcards
from quiz_engine import quiz_mode_factory


def show_stats(cards):
    total = len(cards)
    print(f"\n--- Flashcard Stats ---")
    print(f"Total cards: {total}")
    categories = set(c.get("category", "uncategorized") for c in cards)
    print(f"Categories: {', '.join(sorted(categories))}")
    print(f"-----------------------\n")


def run_quiz(cards, mode_name):
    mode = quiz_mode_factory(mode_name, cards)
    print(f"\nStarting quiz in '{mode_name}' mode. Type 'q' to quit.\n")
    score = 0
    total = 0

    for card in mode:
        question = card.get("question", card.get("front", ""))
        answer = card.get("answer", card.get("back", ""))
        print(f"Q: {question}")
        user_input = input("Your answer: ").strip()
        if user_input.lower() == "q":
            break
        total += 1
        if user_input.lower() == answer.lower():
            print("Correct!\n")
            score += 1
            if hasattr(mode, "record_result"):
                mode.record_result(card, correct=True)
        else:
            print(f"Wrong. Correct answer: {answer}\n")
            if hasattr(mode, "record_result"):
                mode.record_result(card, correct=False)

    if total > 0:
        print(f"\nSession complete: {score}/{total} correct ({100*score//total}%)")
    else:
        print("\nNo questions answered.")


def main():
    parser = argparse.ArgumentParser(
        description="Flashcard Quizzer - CLI study tool"
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Path to flashcard JSON file"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["sequential", "random", "adaptive"],
        default="sequential",
        help="Quiz mode (default: sequential)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show flashcard stats and exit"
    )

    args = parser.parse_args()
    cards = load_flashcards(args.file)

    if args.stats:
        show_stats(cards)
        sys.exit(0)

    run_quiz(cards, args.mode)


if __name__ == "__main__":
    main()
