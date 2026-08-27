import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_quotes() -> list[dict]:
    quotes = []

    for path in DATA_DIR.glob("*.json"):
        with path.open(encoding="utf-8") as file:
            quotes.extend(json.load(file))

    return quotes
