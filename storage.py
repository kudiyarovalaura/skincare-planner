import json
from pathlib import Path


def load_products(path: Path) -> list:
    """Загружает список средств из JSON-файла. При проблеме возвращает пустой список."""
    if not path.exists():
        print(f"Файл {path.name} не найден")
        return []
    if path.read_text(encoding="utf-8").strip() == "":
        print(f"Файл {path.name} пустой")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["products"]


def load_history(path: Path) -> list:
    """Загружает историю применений. Если файла нет или он пустой, история пустая."""
    if not path.exists():
        return []
    if path.read_text(encoding="utf-8").strip() == "":
        print(f"Файл {path.name} пустой, начинаю историю заново")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["records"]


def save_history(path: Path, records: list) -> None:
    """Сохраняет историю применений в JSON-файл."""
    data = {"records": records}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascil=False, indent=4)