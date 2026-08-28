import json
import os
from importlib.resources import files
from pathlib import Path

from gap.config import is_collection_enabled


def get_user_data_dir() -> Path:
    base = Path(
        os.environ.get(
            "XDG_CONFIG_HOME",
            Path.home() / ".config",
        )
    )

    return base / "gap"


def get_user_quotes_dir() -> Path:
    path = get_user_data_dir() / "quotes"
    path.mkdir(parents=True, exist_ok=True)

    return path


def load_json_file(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def load_default_quotes() -> list[dict]:
    quotes = []

    data_dir = files("gap").joinpath("data", "default")

    for resource in data_dir.iterdir():
        if resource.name.endswith(".json"):
            with resource.open("r", encoding="utf-8") as file:
                quotes.extend(json.load(file))

    return quotes


def load_user_quotes() -> list[dict]:
    quotes = []

    data_dir = get_user_quotes_dir()

    for path in data_dir.glob("*.json"):
        quotes.extend(load_json_file(path))

    return quotes


def load_all_quotes() -> list[dict]:
    """
    Charge toutes les citations, activées ou désactivées.
    """
    return load_default_quotes() + load_user_quotes()


def load_quotes() -> list[dict]:
    """
    Charge uniquement les citations des collections activées.
    """
    return [
        quote
        for quote in load_all_quotes()
        if is_collection_enabled(quote["collection"])
    ]
