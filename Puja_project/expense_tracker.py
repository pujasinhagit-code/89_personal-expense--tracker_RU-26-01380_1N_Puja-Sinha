import csv
import os
from collections import defaultdict
from datetime import datetime


FILE_NAME = "expenses.csv"
HEADERS = ["Date", "Category", "Description", "Amount"]


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense(expenses):
    date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return expenses

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    try:
        amount = float(input("Amount: ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Amount must be a positive number.")
        return expenses

    expenses.append({
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": str(amount),
    })
    save_expenses(expenses)
    print(f"Expense saved. Total records: {len(expenses)}")
    return expenses


def show_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print(
            f"{expense['Date']} | {expense['Category']} | "
            f"{expense['Description']} | {float(expense['Amount']):.2f}"
        )


def show_category_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    totals = defaultdict(float)
    for expense in expenses:
        totals[expense["Category"]] += float(expense["Amount"])

    for category, amount in totals.items():
        print(f"{category}: {amount:.2f}")
    print(f"Total: {sum(totals.values()):.2f}")


def show_monthly_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    totals = defaultdict(float)
    for expense in expenses:
        totals[expense["Date"][:7]] += float(expense["Amount"])

    for month, amount in totals.items():
        print(f"{month}: {amount:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Category summary")
        print("4. Monthly summary")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            expenses = add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_category_summary(expenses)
        elif choice == "4":
            show_monthly_summary(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 1-5.")


if __name__ == "__main__":
    main()