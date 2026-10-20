from datetime import date
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


if __name__ == "__main__":
    today = date.today()
    print(f"Сегодня: {today}")
    print(days_since("2026-10-17", today))

    retinol = {"interval_days": 3}
    print(is_due(retinol, "2026-10-17", today))
    print(is_due(retinol, "2026-10-19", today))
