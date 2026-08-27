import json
from pathlib import Path

from gap.state import get_state_dir


HISTORY_LIMIT = 10


def history_path() -> Path:
    return get_state_dir() / "history.json"


def load_history() -> list[str]:
    path = history_path()

    if not path.exists():
        return []

    with path.open(encoding="utf-8") as file:
        return json.load(file)


def save_history(history: list[str]) -> None:
    path = history_path()

    with path.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def remember_quote(quote_id: str) -> None:
    history = load_history()

    # Si elle existe déjà, on la retire avant de la remettre à la fin.
    if quote_id in history:
        history.remove(quote_id)

    history.append(quote_id)

    # On ne conserve que les N dernières.
    history = history[-HISTORY_LIMIT:]

    save_history(history)
