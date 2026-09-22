from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent / "data"


def data_path(name: str) -> Path:
    return _DATA_DIR / name
