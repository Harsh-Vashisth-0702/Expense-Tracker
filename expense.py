from datetime import date

def add_expense():
    while True:
        try:
            amount = float(input("Enter Amount : "))

            if amount < 0:
                print("Amount cannot be negative.")
                continue

            break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    while True:
        category = input("Enter Category : ")

        if category.strip() == "":
            print("Category cannot be empty.")
            continue

        break

    today = date.today().strftime("%Y-%m-%d")

    expense = {
        "amount": amount,
        "category": category,
        "date": today
    }

    return expense