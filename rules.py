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


def find_product(products: list, product_id: str):
    """Находит средство по id. Если такого нет, возвращает None."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def are_compatible(first: dict, second: dict) -> bool:
    """Проверяет, можно ли два средства использовать в один приём."""
    if second["id"] in first["incompatible"]:
        return False
    if first["id"] in second["incompatible"]:
        return False
    return True


def resolve_conflicts(candidates: list) -> tuple:
    """Убирает несовместимые средства: при конфликте остаётся то, у кого приоритет выше."""
    by_priority = sorted(candidates, key=lambda p: p["priority"], reverse=True)
    accepted = []
    skipped = []
    for product in by_priority:
        conflict = None
        for chosen in accepted:
            if not are_compatible(product, chosen):
                conflict = chosen
                break
        if conflict is None:
            accepted.append(product)
        else:
            skipped.append((product, conflict))
    accepted.sort(key=lambda p: p["order"])
    return accepted, skipped


def build_plan(products: list, records: list, today: date, time_of_day: str) -> list:
    """Собирает план на утро или вечер: подходящие средства по порядку нанесения."""
    plan = []
    for product in products:
        if not product["in_use"]:
            continue
        if not product["standalone"]:
            continue
        if time_of_day not in product["time"]:
            continue
        last = last_used(records, product["id"])
        if is_due(product, last, today):
            plan.append(product)
    return resolve_conflicts(plan)



def expand_steps(plan: list, products: list) -> list:
    """Превращает план в список шагов. Средство с сэндвичем даёт несколько шагов."""
    steps = []
    for product in plan:
        if "sandwich" not in product:
            steps.append(product["name"])
            continue
        cream = find_product(products, product["sandwich"]["cream"])
        if cream is None:
            steps.append(product["name"])
            continue
        wait = product["sandwich"]["wait_minutes"]
        steps.append(cream["name"])
        steps.append(f"подождать {wait} минут")
        steps.append(product["name"])
        steps.append(cream["name"])
    return steps

if __name__ == "__main__":
    products = load_products(Path.cwd() / "products.json")
    records = load_history(Path.cwd() / "history.json")
    for today in [date(2026, 10, 20), date(2026, 10, 22)]:
        print(f"Сегодня {today}")
        for time_of_day in ["morning", "evening"]:
            accepted, skipped = build_plan(products, records, today, time_of_day)
            print(f"{time_of_day}:")
            for number, step in enumerate(expand_steps(accepted, products), start=1):
                print(f"  {number}. {step}")
            for product, winner in skipped:
                print(f"  Не сегодня: {product['name']} (нельзя вместе с {winner['name']})")