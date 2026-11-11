
from datetime import date, timedelta
from collections import defaultdict

def get_today_expenses(expenses):
    today = date.today().isoformat()
    return [e for e in expenses if e["date"] == today]

def get_week_expenses(expenses):
    start = (date.today() - timedelta(days=6)).isoformat()
    return [e for e in expenses if e["date"] >= start]

def get_month_expenses(expenses):
    month = date.today().strftime("%Y-%m")
    return [e for e in expenses if e["date"].startswith(month)]

def get_year_expenses(expenses):
    year = str(date.today().year)
    return [e for e in expenses if e["date"].startswith(year)]

def get_category_totals(expenses):
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(totals)

def get_total_expenses(expenses):
    return sum(e["amount"] for e in expenses)

def get_top_category(expenses):
    totals = get_category_totals(expenses)
    return max(totals, key=totals.get) if totals else "None"

def get_average_expense(expenses):
    return get_total_expenses(expenses) / len(expenses) if expenses else 0
