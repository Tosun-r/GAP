import json
import os
from pathlib import Path


def get_config_dir() -> Path:
    base = Path(
        os.environ.get(
            "XDG_CONFIG_HOME",
            Path.home() / ".config",
        )
    )

    path = base / "gap"
    path.mkdir(parents=True, exist_ok=True)

    return path


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load_config() -> dict:
    path = get_config_path()

    if not path.exists():
        return {
            "collections": {}
        }

    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {
            "collections": {}
        }


def save_config(config: dict) -> None:
    path = get_config_path()

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            ensure_ascii=False,
            indent=2,
        )


def is_collection_enabled(name: str) -> bool:
    config = load_config()

    return config.get("collections", {}).get(name, True)


def set_collection_enabled(name: str, enabled: bool) -> None:
    config = load_config()

    collections = config.setdefault("collections", {})

    collections[name] = enabled

    save_config(config)
