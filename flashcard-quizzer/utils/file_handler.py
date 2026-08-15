import json
import sys


def load_flashcards(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filepath}': {e}")
        sys.exit(1)

    if isinstance(data, list):
        cards = data
    elif isinstance(data, dict) and "cards" in data:
        cards = data["cards"]
    else:
        print(
            "Error: JSON must be an array of cards or an object with a 'cards' key."
        )
        sys.exit(1)

    if not isinstance(cards, list):
        print("Error: 'cards' must be a list.")
        sys.exit(1)

    required_fields = {"question", "answer"}
    alt_fields = {"front", "back"}

    for i, card in enumerate(cards):
        if not isinstance(card, dict):
            print(f"Error: Card at index {i} is not an object.")
            sys.exit(1)
        has_required = required_fields.issubset(card.keys())
        has_alt = alt_fields.issubset(card.keys())
        if not has_required and not has_alt:
            print(
                f"Error: Card at index {i} is missing required fields "
                f"('question'+'answer' or 'front'+'back')."
            )
            sys.exit(1)

    return cards
