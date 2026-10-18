import json
from pathlib import Path


def load_products(path: Path) -> list:
    """Загружает список средств из JSON-файла."""
    if not path.exists():
        print(f"Файл {path.name} не найден")
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["products"]


if __name__ == "__main__":
    products = load_products(Path.cwd() / "products.json")
    print(f"Загружено средств: {len(products)}")
    for product in products:
        print(product["name"])