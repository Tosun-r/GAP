import argparse
import random

from gap.repository import load_quotes
from gap.state import (
    get_pending_quote,
    clear_pending_quote,
    set_pending_quote,
)


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


def command_hook() -> None:
    quote = get_pending_quote()

    if quote is None:
        return

    print_quote(quote)
    clear_pending_quote()


def command_queue() -> None:
    quotes = load_quotes()

    if not quotes:
        return

    quote = random.choice(quotes)
    set_pending_quote(quote)


def main() -> None:
    parser = argparse.ArgumentParser(prog="gap")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("now")
    subparsers.add_parser("hook")
    subparsers.add_parser("queue")

    args = parser.parse_args()

    match args.command:
        case "now":
            command_now()

        case "hook":
            command_hook()

        case "queue":
            command_queue()



if __name__ == "__main__":
    main()
