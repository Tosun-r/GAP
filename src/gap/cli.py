import argparse
import random

from gap.repository import load_quotes


def print_quote(quote: dict) -> None:
    print()
    print(f"“{quote['text']}”")

    source = f"— {quote['author']}"

    if quote.get("reference"):
        source += f", {quote['reference']}"

    print(f"    {source}")
    print()


def command_now() -> None:
    quotes = load_quotes()

    if not quotes:
        print("Aucune citation disponible.")
        return

    print_quote(random.choice(quotes))


def main() -> None:
    parser = argparse.ArgumentParser(prog="gap")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("now")

    args = parser.parse_args()

    match args.command:
        case "now":
            command_now()


if __name__ == "__main__":
    main()
