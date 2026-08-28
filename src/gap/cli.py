import argparse
import subprocess
import time
from collections import Counter

from gap.config import (
    load_config,
    set_collection_enabled,
)
from gap.history import remember_quote
from gap.repository import load_all_quotes, load_quotes
from gap.scheduler import regular_delay, startup_delay
from gap.selector import select_quote
from gap.state import (
    clear_pending_quote,
    get_pending_quote,
    set_pending_quote,
)


def print_quote(quote: dict) -> None:
    print()
    print(f"“{quote['text']}”")

    source = f"— {quote['author']}"

    if quote.get("work"):
        source += f", {quote['work']}"

    if quote.get("reference"):
        source += f", {quote['reference']}"

    print(f"    {source}")
    print()


def command_now() -> None:
    """
    Sélectionne et affiche immédiatement une citation.
    """
    quotes = load_quotes()

    quote = select_quote(quotes)

    if quote is None:
        print("Aucune citation disponible.")
        return

    print_quote(quote)

    remember_quote(quote["id"])


def command_queue() -> None:
    """
    Sélectionne une citation et la met en attente.
    """
    if get_pending_quote() is not None:
        return

    quotes = load_quotes()

    quote = select_quote(quotes)

    if quote is None:
        return

    set_pending_quote(quote)


def command_hook() -> None:
    """
    Affiche la citation actuellement en attente.
    """
    quote = get_pending_quote()

    if quote is None:
        return

    print_quote(quote)

    remember_quote(quote["id"])

    clear_pending_quote()


def command_daemon() -> None:
    """
    Lance le scheduler de GAP.
    """
    quotes = load_quotes()

    if not quotes:
        return

    time.sleep(startup_delay())

    while True:
        if get_pending_quote() is None:
            quotes = load_quotes()

            quote = select_quote(quotes)

            if quote is not None:
                set_pending_quote(quote)

        time.sleep(regular_delay())


def command_on() -> None:
    """
    Démarre le service systemd de GAP.
    """
    subprocess.run(
        ["systemctl", "--user", "start", "gap.service"],
        check=True,
    )


def command_off() -> None:
    """
    Arrête le service systemd de GAP.
    """
    subprocess.run(
        ["systemctl", "--user", "stop", "gap.service"],
        check=True,
    )


def command_status() -> None:
    """
    Affiche l'état du service systemd de GAP.
    """
    subprocess.run(
        ["systemctl", "--user", "status", "gap.service"],
    )


def command_list() -> None:
    """
    Affiche les collections disponibles et leur état.
    """
    quotes = load_all_quotes()

    if not quotes:
        print("Aucune collection disponible.")
        return

    counts = Counter(
        quote["collection"]
        for quote in quotes
    )

    config = load_config()
    configured = config.get("collections", {})

    print("GAP collections")
    print()

    for name, count in sorted(counts.items()):
        enabled = configured.get(name, True)

        status = "ON " if enabled else "OFF"

        print(
            f"  {status}  "
            f"{name:<20} "
            f"{count:>4} citations"
        )


def command_enable(name: str) -> None:
    """
    Active une collection.
    """
    quotes = load_all_quotes()

    collections = {
        quote["collection"]
        for quote in quotes
    }

    if name not in collections:
        print(f"Collection inconnue : {name}")
        return

    set_collection_enabled(name, True)

    print(f"Collection '{name}' activée.")


def command_disable(name: str) -> None:
    """
    Désactive une collection.
    """
    quotes = load_all_quotes()

    collections = {
        quote["collection"]
        for quote in quotes
    }

    if name not in collections:
        print(f"Collection inconnue : {name}")
        return

    set_collection_enabled(name, False)

    print(f"Collection '{name}' désactivée.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gap",
        description="Terminal quotes.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # --------------------------------------------------
    # Citations
    # --------------------------------------------------

    subparsers.add_parser(
        "now",
        help="affiche immédiatement une citation",
    )

    subparsers.add_parser(
        "queue",
        help="met une citation en attente",
    )

    subparsers.add_parser(
        "hook",
        help="affiche la citation en attente",
    )

    subparsers.add_parser(
        "daemon",
        help="lance le scheduler",
    )

    # --------------------------------------------------
    # Service GAP
    # --------------------------------------------------

    subparsers.add_parser(
        "on",
        help="démarre GAP",
    )

    subparsers.add_parser(
        "off",
        help="arrête GAP",
    )

    subparsers.add_parser(
        "status",
        help="affiche l'état de GAP",
    )

    # --------------------------------------------------
    # Collections
    # --------------------------------------------------

    subparsers.add_parser(
        "list",
        help="liste les collections",
    )

    enable_parser = subparsers.add_parser(
        "enable",
        help="active une collection",
    )

    enable_parser.add_argument(
        "collection",
        help="nom de la collection",
    )

    disable_parser = subparsers.add_parser(
        "disable",
        help="désactive une collection",
    )

    disable_parser.add_argument(
        "collection",
        help="nom de la collection",
    )

    # --------------------------------------------------
    # Parse
    # --------------------------------------------------

    args = parser.parse_args()

    match args.command:

        case "now":
            command_now()

        case "queue":
            command_queue()

        case "hook":
            command_hook()

        case "daemon":
            command_daemon()

        case "on":
            command_on()

        case "off":
            command_off()

        case "status":
            command_status()

        case "list":
            command_list()

        case "enable":
            command_enable(args.collection)

        case "disable":
            command_disable(args.collection)


if __name__ == "__main__":
    main()
