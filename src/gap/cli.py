import argparse
#import random

import time

from gap.scheduler import startup_delay, regular_delay
from gap.selector import select_quote
from gap.history import remember_quote

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
    quote = select_quote(quotes)

    if quote is None:
        print("Aucune citation disponible.")
        return

    print_quote(quote)
    remember_quote(quote["id"])


def command_hook() -> None:
    quote = get_pending_quote()

    if quote is None:
        return

    print_quote(quote)
    clear_pending_quote()


def command_queue() -> None:
    quotes = load_quotes()
    quote = select_quote(quotes)

    if quote is None:
        return

    set_pending_quote(quote)


def command_daemon() -> None:
    quotes = load_quotes()

    if not quotes:
        return

    time.sleep(startup_delay())

    while True:
        if get_pending_quote() is None:
            quote = select_quote(quotes)

            if quote is not None:
                set_pending_quote(quote)

        time.sleep(regular_delay())


def main() -> None:
    parser = argparse.ArgumentParser(prog="gap")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("now")
    subparsers.add_parser("hook")
    subparsers.add_parser("queue")
    subparsers.add_parser("daemon")

    args = parser.parse_args()

    match args.command:
        case "now":
            command_now()

        case "hook":
            command_hook()

        case "queue":
            command_queue()

        case "daemon":
            command_daemon()



if __name__ == "__main__":
    main()
