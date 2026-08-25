from expense import add_expense 
from storage import save_expenses, load_expenses
from reports import (
    get_today_expenses,
    get_weekly_expenses,
    get_monthly_expenses,
    get_yearly_expenses,
    get_category_totals,
    get_total_expenses
)

expenses = load_expenses()

def show_today_expenses():
    today_expenses = get_today_expenses(expenses)

    print("------ Today's Expenses ------")

    for expense in today_expenses:
        print(f"Amount: {expense['amount']} | Category: {expense['category']} | Date: {expense['date']}")

show_today_expenses()

while True : 
  
    print("\nWelcome to Expense Tracker")
    
    print("------Expense Tracker------")
    
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Weekly expenses")
    print("4. Monthly expenses")
    print("5. Yearly expenses")
    print("6. Category Summary")
    print("7. Total Spending")
    print("8. Exit")
    
    choice = input("Enter your choice : ")
    if choice == "1" : 
        expense = add_expense()
        expenses.append(expense)
        save_expenses(expenses)
    
    elif choice == "2" :
        print("____Your Expenses____")
        if not expenses:
            print("No expenses found.")
        else:
            for expense in expenses :
                print(f"Amount: {expense['amount']} | Category: {expense['category']} | Date: {expense['date']}")
    
    elif choice == "3":
        weekly_expenses = get_weekly_expenses(expenses)
        print("------ Weekly Expenses ------")
        if not weekly_expenses:
            print("No expenses found.")
        else :
            for expense in weekly_expenses:
                print(f"Amount: {expense['amount']} | Category: {expense['category']} | Date: {expense['date']}")
    
    elif choice == "4":
        monthly_expenses = get_monthly_expenses(expenses)
        print("------ Monthly Expenses ------")
        if not monthly_expenses:
            print("No expenses found.")
        else:
            for expense in monthly_expenses:
                print(f"Amount: {expense['amount']} | Category: {expense['category']} | Date: {expense['date']}")

    elif choice == "5":
        yearly_expenses = get_yearly_expenses(expenses)
        print("------ Yearly Expenses ------")
        if not yearly_expenses:
            print("No expenses found.")
        else:
            for expense in yearly_expenses:
                print(f"Amount: {expense['amount']} | Category: {expense['category']} | Date: {expense['date']}")

    elif choice == "6":
        category_totals = get_category_totals(expenses)
        print("------ Category Summary ------")
        if not category_totals:
            print("No expenses found.")
        else:
            for category in category_totals:
                print(f"{category}: {category_totals[category]}")

    elif choice == "7":
        total = get_total_expenses(expenses)
        print("------ Total Spending ------")
        if total == 0:
            print("No expenses found.")
        else:
            print(f"Total spent: {total}")

    elif choice == "8":
        print("Thank you for using Expense Tracker")
        break

    else:
        print("Invalid choice. Please try again.")