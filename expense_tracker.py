import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import pandas as pd

class Expense:
    def __init__(self, amount, category, date, payment):
        self.amount = amount
        self.category = category
        self.date = date
        self.payment = payment

class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def add_expense(self, amount, category, payment):
        date = datetime.now().strftime('%Y-%m-%d')
        expense = Expense(amount, category, date, payment)
        self.expenses.append(expense)
        self.save_expenses()

    def save_expenses(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amount', 'Category', 'Date', 'Payment'])
            for exp in self.expenses:
                writer.writerow([exp.amount, exp.category, exp.date, exp.payment])

    def load_expenses(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    exp = Expense(float(row['Amount']), row['Category'], row['Date'], row['Payment'])
                    self.expenses.append(exp)
        except FileNotFoundError:
            pass

    def show_summary(self):
        total = sum(exp.amount for exp in self.expenses)
        print(f"Total expenses: {total}")
        cat_summary = {}
        for exp in self.expenses:
            cat_summary[exp.category] = cat_summary.get(exp.category, 0) + exp.amount
        print("Category-wise summary:", cat_summary)

    def edit_expense(self, idx, new_amount=None, new_category=None, new_payment=None):
        if 0 <= idx < len(self.expenses):
            if new_amount: self.expenses[idx].amount = new_amount
            if new_category: self.expenses[idx].category = new_category
            if new_payment: self.expenses[idx].payment = new_payment
            self.save_expenses()

    def delete_expense(self, idx):
        if 0 <= idx < len(self.expenses):
            self.expenses.pop(idx)
            self.save_expenses()

    def search_expenses(self, category=None, payment=None, date=None):
        results = self.expenses
        if category: results = [e for e in results if e.category == category]
        if payment: results = [e for e in results if e.payment == payment]
        if date: results = [e for e in results if e.date == date]
        return results

    def monthly_summary(self):
        month = datetime.now().strftime('%Y-%m')
        filtered = [e for e in self.expenses if e.date.startswith(month)]
        total = sum(e.amount for e in filtered)
        cat_summary = {}
        for e in filtered:
            cat_summary[e.category] = cat_summary.get(e.category, 0) + e.amount
        print(f"Total for {month}: {total}")
        print("Breakdown:", cat_summary)

    def recent_expenses(self, n=5):
        return self.expenses[-n:]

    def visualize_category_summary(self):
        summary = {}
        for e in self.expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
        plt.pie(summary.values(), labels=summary.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Spending by Category")
        plt.axis('equal')
        plt.show()

    # New functions:
    def export_to_excel(self, filename='expenses.xlsx'):
        data = [{'Amount': e.amount, 'Category': e.category, 'Date': e.date, 'Payment': e.payment} for e in self.expenses]
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Exported expenses to {filename}")

    def expenses_in_date_range(self, start_date, end_date):
        results = [e for e in self.expenses if start_date <= e.date <= end_date]
        return results

    def top_categories(self, n=3):
        cat_summary = {}
        for exp in self.expenses:
            cat_summary[exp.category] = cat_summary.get(exp.category, 0) + exp.amount
        sorted_cats = sorted(cat_summary.items(), key=lambda x: x[1], reverse=True)
        return sorted_cats[:n]

    def visualize_monthly_trend(self):
        month_expense = defaultdict(float)
        for e in self.expenses:
            month = e.date[:7]  # 'YYYY-MM'
            month_expense[month] += e.amount
        months = sorted(month_expense.keys())
        amounts = [month_expense[m] for m in months]
        plt.plot(months, amounts, marker='o')
        plt.title("Monthly Expense Trend")
        plt.xlabel("Month")
        plt.ylabel("Amount Spent")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def filter_by_amount(self, min_amount=0, max_amount=float('inf')):
        return [e for e in self.expenses if min_amount <= e.amount <= max_amount]

    def save_as_json(self, filename='expenses.json'):
        data = [{'Amount': e.amount, 'Category': e.category, 'Date': e.date, 'Payment': e.payment} for e in self.expenses]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved expenses to {filename}")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.add_expense(100, "Food", "Cash")
    tracker.add_expense(250, "Bills", "Card")
    tracker.show_summary()
