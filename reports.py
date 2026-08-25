from datetime import date, timedelta


def get_today_expenses(expenses):
    today = date.today()
    today_expenses = []

    for expense in expenses:
        if expense["date"] == today.strftime("%Y-%m-%d"):
            today_expenses.append(expense)

    return today_expenses


def get_weekly_expenses(expenses):
    weekly_expenses = []
    today = date.today()
    week_ago = today - timedelta(days=6)

    for expense in expenses:
        expense_date = date.fromisoformat(expense["date"])

        if week_ago <= expense_date <= today:
            weekly_expenses.append(expense)

    return weekly_expenses


def get_monthly_expenses(expenses):
    monthly_expenses = []
    today = date.today()

    for expense in expenses:
        expense_date = date.fromisoformat(expense["date"])

        if expense_date.year == today.year and expense_date.month == today.month:
            monthly_expenses.append(expense)

    return monthly_expenses


def get_yearly_expenses(expenses):
    yearly_expenses = []
    today = date.today()

    for expense in expenses:
        expense_date = date.fromisoformat(expense["date"])

        if expense_date.year == today.year:
            yearly_expenses.append(expense)

    return yearly_expenses


def get_category_totals(expenses):
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals


def get_total_expenses(expenses):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total