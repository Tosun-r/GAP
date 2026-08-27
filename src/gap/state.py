import json
import os
from pathlib import Path


def get_state_dir() -> Path:
    base = Path(
        os.environ.get(
            "XDG_STATE_HOME",
            Path.home() / ".local" / "state"
        )
    )

    path = base / "gap"
    path.mkdir(parents=True, exist_ok=True)

    return path


def pending_path() -> Path:
    return get_state_dir() / "pending.json"


def set_pending_quote(quote: dict) -> None:
    path = pending_path()

    with path.open("w", encoding="utf-8") as file:
        json.dump(quote, file, ensure_ascii=False)


def get_pending_quote() -> dict | None:
    path = pending_path()

    if not path.exists():
        return None

    with path.open(encoding="utf-8") as file:
        return json.load(file)


def clear_pending_quote() -> None:
    path = pending_path()

    if path.exists():
        path.unlink()
