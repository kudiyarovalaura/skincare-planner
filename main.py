from datetime import date
from pathlib import Path


from storage import load_products, load_history, save_history
from rules import build_plan, expand_steps


PRODUCTS_PATH = Path.cwd() / "products.json"
HISTORY_PATH = Path.cwd() / "history.json"


def show_plan(products: list, records: list, today: date, time_of_day: str) -> list:
    """Печатает план на утро или вечер и возвращает сресдтва из плана."""
    accepted, skipped = build_plan(products, records, today, time_of_day)
    steps = expand_steps(accepted, products)
    for number, step in enumerate(steps, start=1):
        print(f" {number}. {step}")
    for product, winner in skipped:
        print(f" Не сегодня: {product["name"]} (нельзя вместе с {winner['name']})")
    return accepted


def mark_done(records: list, plan: list, today: date) -> None:
    """Добавляет в историю запись о каждом средстве из плана."""
    for product in plan:
        record = {"date": today.isoformat(), "product": product["id"]}
        if record not in records:
            records.append(record)


def main() -> None:
    """Главное меню программы."""
    products = load_products(PRODUCTS_PATH)
    records = load_history(HISTORY_PATH)
    today = date.today()
    print(f"Сегодня {today}")

    while True:
        print()
        print("1 - план на утро")
        print("2 - план на вечер")
        print("3 - выход")
        choice = input("Выберите: ").strip()

        match choice:
            case "1":
                time_of_day = "morning"
            case "2":
                time_of_day = "evening"
            case "3":
                print("До встречи!")
                break
            case _:
                print("Нужно ввести 1, 2 или 3")
                continue

        plan = show_plan(products, records, today, time_of_day)
        answer = input("Сделала? (да/нет): ").strip().lower()
        if answer == "да":
            mark_done(records, plan, today)
            save_history(HISTORY_PATH, records)
            print("Записала в историю")
        else:
            print("Ничего не записываю. Пропущенное перенесётся само.")


if __name__ == "__main__":
    main()