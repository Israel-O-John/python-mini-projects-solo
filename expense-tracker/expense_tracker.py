import csv
import secrets
from datetime import date
from tabulate import tabulate




def main():
    menu = input("Expense Menu: Add | View - ").strip().lower()
    if menu == "add":
        try:
            date = input("Expense date: Today | YYYY-MM-DD ").strip().lower()
            description = input("Expense Description: ").strip()
            amount = input("Expense Amount: ").strip()
            expense = create_expense(date, description, amount)
            save_expense(expense)
            print("✅")
        except (ValueError, KeyError) as err:
            print(f"❎ {err}")
    elif menu == "view":
        expenses = view_expenses()
        print(tabulate(expenses, headers="keys", tablefmt="fancy_grid"))



def create_expense(date_in, desc, amt):
        if date_in == 'today':
            actual_date = date.today()
        else:
            try:
                actual_date = date.fromisoformat(date_in)
            except (ValueError, TypeError):
                return ValueError("Invalid date format")

        
        if actual_date > date.today():
            raise ValueError("Future dates not allowed")
        
        if not desc:
            raise ValueError("Expense description can't be empty")
        
        try:
            amount = float(amt)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number only")
        
        if not amount > 0:
            raise ValueError("Expense amount can't be less than 0")
        
        expense_id = secrets.token_hex(4)
        
        return {
            "id": expense_id,
            "date": actual_date.isoformat(),
            "description": desc,
            "amount": f"#{amount}",
        }


def save_expense(expense):
    file_exists = False
    
    try:
        with open("expenses.csv", "r") as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    
    
    with open("expenses.csv", "a", newline="", encoding="utf-8") as expense_file:
        fieldnames = ["id", "date", "description", "amount"]
        writer = csv.DictWriter(expense_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)


def view_expenses():
    try:
        with open("expenses.csv", "r") as expense_file:
            reader = csv.DictReader(expense_file)
            expense_list = [
                {k: v for k, v in row.items() if k != "id"}
                for row in reader
            ]
            return expense_list
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    main()