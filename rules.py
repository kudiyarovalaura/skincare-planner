from datetime import date
from pathlib import Path
from storage import load_products, load_history

def days_since(last_date: str, today: date) -> int:
    """Считает, сколько дней прошло с last_date до today."""
    last = date.fromisoformat(last_date)
    difference = today - last
    return difference.days


def is_due(product: dict, last_date, today: date) -> bool:
    """Проверяет, можно ли сегодня использовать средство по его интервалу."""
    interval = product["interval_days"]
    if interval is None:
        return True
    if last_date is None:
        return True
    return days_since(last_date, today) >= interval


def last_used(records: list, product_id: str):
    """Находит дату последнего применения средства. Если не применялось, None."""
    last = None
    for record in records:
        if record["product"] == product_id:
            if last is None or record["date"] > last:
                last = record["date"]
    return last

if __name__ == "__main__":
    today = date.today()
    products = load_products(Path.cwd() / "products.json")
    records = load_history(Path.cwd() / "history.json")
    for product in products:
        if product["in_use"]:
            last = last_used(records, product["id"])
            print(f"{product['name']}: последний раз {last}, сегодня можно: {is_due(product, last, today)}")
