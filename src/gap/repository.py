import json
from importlib.resources import files


def load_quotes() -> list[dict]:
    quotes = []

    data_dir = files("gap").joinpath("data")

    for resource in data_dir.iterdir():
        if resource.name.endswith(".json"):
            with resource.open("r", encoding="utf-8") as file:
                quotes.extend(json.load(file))

    return quotes
