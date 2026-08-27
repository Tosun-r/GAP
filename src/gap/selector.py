import random

from gap.history import load_history


def select_quote(quotes: list[dict]) -> dict | None:
    if not quotes:
        return None

    recent = set(load_history())

    candidates = [
        quote
        for quote in quotes
        if quote["id"] not in recent
    ]

    # Si toutes les citations ont été vues récemment,
    # on autorise de nouveau l'ensemble.
    if not candidates:
        candidates = quotes

    return random.choice(candidates)
