import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import pandas as pd
import numpy as np

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
        self.goals = []
        self.budgets = {}
        self.load_expenses()
        self.load_goals()
        self.load_budgets()

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
            month = e.date[:7]
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

    def set_budget(self, category, amount):
        self.budgets[category] = amount
        self.save_budgets()
        print(f"Budget set for {category}: {amount}")

    def check_budget_status(self):
        if not self.budgets:
            print("No budgets set")
            return

        current_month = datetime.now().strftime('%Y-%m')
        monthly_expenses = [e for e in self.expenses if e.date.startswith(current_month)]

        for category, budget in self.budgets.items():
            spent = sum(e.amount for e in monthly_expenses if e.category == category)
            percent = (spent / budget) * 100 if budget > 0 else 0
            status = "Over budget!" if spent > budget else f"✅ {percent:.1f}% of budget"
            print(f"{category}: Spent {spent} of {budget} - {status}")

    def save_budgets(self):
        with open('budgets.json', 'w') as f:
            json.dump(self.budgets, f, indent=2)

    def load_budgets(self):
        try:
            with open('budgets.json', 'r') as f:
                self.budgets = json.load(f)
        except FileNotFoundError:
            self.budgets = {}

    def add_financial_goal(self, name, target_amount, deadline=None):
        goal = {
            'name': name,
            'target': target_amount,
            'current': 0,
            'deadline': deadline,
            'date_created': datetime.now().strftime('%Y-%m-%d')
        }
        self.goals.append(goal)
        self.save_goals()
        print(f"Goal added: {name} ({target_amount})")

    def update_goal_progress(self, goal_name, amount):
        for goal in self.goals:
            if goal['name'].lower() == goal_name.lower():
                goal['current'] = min(goal['current'] + amount, goal['target'])
                self.save_goals()
                progress = (goal['current'] / goal['target']) * 100
                print(f"Updated {goal_name}: {progress:.1f}% complete")
                if goal['current'] >= goal['target']:
                    print(f"🎉 Goal '{goal_name}' achieved!")
                return
        print(f"Goal '{goal_name}' not found")

    def show_goals(self):
        if not self.goals:
            print("No financial goals set")
            return
        for goal in self.goals:
            progress = (goal['current'] / goal['target']) * 100
            print(f"\n{goal['name']}:")
            print(f"  Progress: {goal['current']}/{goal['target']} ({progress:.1f}%)")
            if goal['deadline']:
                print(f"  Deadline: {goal['deadline']}")
            remaining = goal['target'] - goal['current']
            if remaining > 0:
                print(f"  Remaining: {remaining}")

    def save_goals(self):
        with open('financial_goals.json', 'w') as f:
            json.dump(self.goals, f, indent=2)

    def load_goals(self):
        try:
            with open('financial_goals.json', 'r') as f:
                self.goals = json.load(f)
        except FileNotFoundError:
            self.goals = []

    def spending_trends(self, months=6):
        monthly_data = defaultdict(lambda: defaultdict(float))

        today = datetime.now()
        start_date = (today - timedelta(days=30*months)).strftime('%Y-%m-%d')

        for expense in self.expenses:
            if expense.date >= start_date:
                month = expense.date[:7]
                monthly_data[month][expense.category] += expense.amount

        months_list = sorted(monthly_data.keys())
        categories = list(set(cat for month in monthly_data.values() for cat in month.keys()))

        plt.figure(figsize=(12,6))
        for category in categories:
            amounts = [monthly_data[month].get(category, 0) for month in months_list]
            plt.plot(months_list, amounts, marker='o', label=category)
        plt.title("Monthly Spending Trends by Category")
        plt.xlabel("Month")
        plt.ylabel("Amount Spent")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def category_comparison(self, category1, category2, period="monthly"):
        if period == "monthly":
            current_month = datetime.now().strftime('%Y-%m')
            expenses = [e for e in self.expenses if e.date.startswith(current_month)]
        else:
            expenses = self.expenses

        total1 = sum(e.amount for e in expenses if e.category == category1)
        total2 = sum(e.amount for e in expenses if e.category == category2)

        print(f"Comparison: {category1} vs {category2}")
        print(f"{category1}: {total1}")
        print(f"{category2}: {total2}")
        if total2 > 0:
            ratio = total1 / total2
            print(f"Ratio ({category1}/{category2}): {ratio:.2f}")

        plt.figure(figsize=(8,6))
        plt.bar([category1, category2], [total1, total2], color=['skyblue', 'lightcoral'])
        plt.title(f"Spending Comparison: {category1} vs {category2}")
        plt.ylabel("Amount Spent")
        for i, v in enumerate([total1, total2]):
            plt.text(i, v + max([total1, total2])*0.01, f"{v}", ha='center', va='bottom')
        plt.show()

    def predict_next_month_spending(self):
        if len(self.expenses) < 30:
            print("Not enough data for prediction")
            return

        monthly_sums = defaultdict(lambda: defaultdict(float))
        for expense in self.expenses:
            month = expense.date[:7]
            monthly_sums[month][expense.category] += expense.amount

        categories = set(cat for month_data in monthly_sums.values() for cat in month_data.keys())
        predictions = {}

        for category in categories:
            amounts = [monthly_sums[month][category] for month in sorted(monthly_sums.keys()) if category in monthly_sums[month]]
            if len(amounts) >= 3:
                x = np.array(range(len(amounts)))
                y = np.array(amounts)
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                predicted = max(0, p(len(amounts)))
                predictions[category] = predicted

        print("Predicted spending for next month:")
        total = 0
        for category, amount in predictions.items():
            print(f"  {category}: {amount:.2f}")
            total += amount
        print(f"  Total predicted: {total:.2f}")
        return predictions

    def get_spending_insights(self):
        if not self.expenses:
            print("No expenses recorded yet")
            return

        cat_totals = {}
        for e in self.expenses:
            cat_totals[e.category] = cat_totals.get(e.category, 0) + e.amount

        top_cat = max(cat_totals, key=cat_totals.get)
        top_amount = cat_totals[top_cat]
        dates = [datetime.strptime(e.date, '%Y-%m-%d') for e in self.expenses]
        months = len(set((d.year, d.month) for d in dates))
        monthly_avg = sum(e.amount for e in self.expenses) / max(1, months)
        print("Spending Insights:")
        print(f"• Your top spending category is {top_cat} ({top_amount})")
        print(f"• Average monthly spending: {monthly_avg:.2f}")

        current_month = datetime.now().strftime('%Y-%m')
        current_total = sum(e.amount for e in self.expenses if e.date.startswith(current_month))
        if months > 1:
            previous_months_avg = (sum(e.amount for e in self.expenses) - current_total) / max(1, months-1)
            if current_total > previous_months_avg * 1.5:
                print(f" Current month spending ({current_total}) is significantly higher than average")
            elif current_total < previous_months_avg * 0.5:
                print(f" Current month spending ({current_total}) is significantly lower than average")
    def export_to_google_sheets(self, sheet_name="Expense Tracker"):
        print("Google Sheets integration requires Google API setup and authentication.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.add_expense(100, "Food", "Cash")
    tracker.add_expense(250, "Bills", "Card")
    tracker.show_summary()
    tracker.set_budget("Food", 600)
    tracker.check_budget_status()
