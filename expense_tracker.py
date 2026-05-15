#!/usr/bin/env python3
"""
Expense Tracker - A command-line application to manage personal finances.
Features:
- Add, update, delete expenses
- View all expenses with filtering by category
- View expense summary (all-time, monthly, by category)
- Set monthly budgets and get warnings
- Export expenses to CSV
"""

import argparse
import json
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Data file location
DATA_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"


class ExpenseTracker:
    """Main expense tracker class."""

    def __init__(self, data_file: str = DATA_FILE, budget_file: str = BUDGET_FILE):
        """Initialize the expense tracker."""
        self.data_file = data_file
        self.budget_file = budget_file
        self.expenses = self._load_expenses()
        self.budgets = self._load_budgets()
        self.next_id = self._get_next_id()

    def _load_expenses(self) -> List[Dict]:
        """Load expenses from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _load_budgets(self) -> Dict:
        """Load budgets from JSON file."""
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_expenses(self) -> None:
        """Save expenses to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)

    def _save_budgets(self) -> None:
        """Save budgets to JSON file."""
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f, indent=2)

    def _get_next_id(self) -> int:
        """Get the next expense ID."""
        if not self.expenses:
            return 1
        return max(exp['id'] for exp in self.expenses) + 1

    def add_expense(self, description: str, amount: float, 
                   category: str = "General", date: Optional[str] = None) -> Tuple[bool, str]:
        """Add a new expense.
        
        Args:
            description: Description of the expense
            amount: Amount of the expense
            category: Category of the expense (default: General)
            date: Date of the expense (YYYY-MM-DD format, default: today)
            
        Returns:
            Tuple of (success, message)
        """
        # Validation
        if not description or not description.strip():
            return False, "Error: Description cannot be empty"
        
        if amount <= 0:
            return False, "Error: Amount must be greater than 0"
        
        if not category or not category.strip():
            return False, "Error: Category cannot be empty"
        
        # Set default date to today if not provided
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return False, "Error: Invalid date format. Use YYYY-MM-DD"
        
        expense = {
            "id": self.next_id,
            "description": description.strip(),
            "amount": float(amount),
            "category": category.strip(),
            "date": date
        }
        
        self.expenses.append(expense)
        self.next_id += 1
        self._save_expenses()
        
        # Check budget
        month = date[:7]  # YYYY-MM
        self._check_budget(month)
        
        return True, f"Expense added successfully (ID: {expense['id']})"

    def update_expense(self, expense_id: int, description: Optional[str] = None,
                      amount: Optional[float] = None, category: Optional[str] = None,
                      date: Optional[str] = None) -> Tuple[bool, str]:
        """Update an existing expense.
        
        Args:
            expense_id: ID of the expense to update
            description: New description (optional)
            amount: New amount (optional)
            category: New category (optional)
            date: New date (optional)
            
        Returns:
            Tuple of (success, message)
        """
        expense = self._find_expense(expense_id)
        if not expense:
            return False, f"Error: Expense with ID {expense_id} not found"
        
        # Update fields if provided
        if description is not None:
            if not description.strip():
                return False, "Error: Description cannot be empty"
            expense["description"] = description.strip()
        
        if amount is not None:
            if amount <= 0:
                return False, "Error: Amount must be greater than 0"
            expense["amount"] = float(amount)
        
        if category is not None:
            if not category.strip():
                return False, "Error: Category cannot be empty"
            expense["category"] = category.strip()
        
        if date is not None:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                expense["date"] = date
            except ValueError:
                return False, "Error: Invalid date format. Use YYYY-MM-DD"
        
        self._save_expenses()
        return True, f"Expense {expense_id} updated successfully"

    def delete_expense(self, expense_id: int) -> Tuple[bool, str]:
        """Delete an expense.
        
        Args:
            expense_id: ID of the expense to delete
            
        Returns:
            Tuple of (success, message)
        """
        expense = self._find_expense(expense_id)
        if not expense:
            return False, f"Error: Expense with ID {expense_id} not found"
        
        self.expenses.remove(expense)
        self._save_expenses()
        return True, f"Expense deleted successfully"

    def list_expenses(self, category: Optional[str] = None, month: Optional[str] = None) -> str:
        """List all expenses, optionally filtered by category or month.
        
        Args:
            category: Filter by category (optional)
            month: Filter by month in YYYY-MM format (optional)
            
        Returns:
            Formatted string of expenses
        """
        filtered_expenses = self.expenses
        
        # Filter by category if provided
        if category:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['category'].lower() == category.lower()]
        
        # Filter by month if provided
        if month:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['date'].startswith(month)]
        
        if not filtered_expenses:
            return "No expenses found."
        
        # Sort by date (newest first)
        filtered_expenses = sorted(filtered_expenses, key=lambda x: x['date'], reverse=True)
        
        # Format output
        output = "ID  Date        Description              Amount    Category\n"
        output += "-" * 70 + "\n"
        
        for expense in filtered_expenses:
            output += f"{expense['id']:<3} {expense['date']} {expense['description']:<24} ${expense['amount']:<8.2f} {expense['category']}\n"
        
        return output

    def summary(self, month: Optional[str] = None, category: Optional[str] = None) -> str:
        """Get expense summary.
        
        Args:
            month: Filter by month in YYYY-MM format (optional)
            category: Filter by category (optional)
            
        Returns:
            Summary string
        """
        filtered_expenses = self.expenses
        
        # Filter by category if provided
        if category:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['category'].lower() == category.lower()]
        
        # Filter by month if provided
        if month:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['date'].startswith(month)]
        
        if not filtered_expenses:
            if month and category:
                return f"No expenses found for {category} in {month}."
            elif month:
                return f"No expenses found for {month}."
            elif category:
                return f"No expenses found for {category}."
            else:
                return "No expenses found."
        
        total = sum(e['amount'] for e in filtered_expenses)
        
        # Generate summary
        output = ""
        if month and category:
            output = f"Summary for {category} in {month}:\n"
        elif month:
            output = f"Summary for {month}:\n"
        elif category:
            output = f"Summary for {category}:\n"
        else:
            output = "Overall Summary:\n"
        
        output += "-" * 40 + "\n"
        
        # Category breakdown
        categories = {}
        for expense in filtered_expenses:
            cat = expense['category']
            categories[cat] = categories.get(cat, 0) + expense['amount']
        
        for cat in sorted(categories.keys()):
            output += f"{cat:<20} ${categories[cat]:>10.2f}\n"
        
        output += "-" * 40 + "\n"
        output += f"Total expenses: ${total:.2f}\n"
        
        return output

    def set_budget(self, month: str, amount: float) -> Tuple[bool, str]:
        """Set a monthly budget.
        
        Args:
            month: Month in YYYY-MM format
            amount: Budget amount
            
        Returns:
            Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Error: Budget amount must be greater than 0"
        
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            return False, "Error: Invalid month format. Use YYYY-MM"
        
        self.budgets[month] = float(amount)
        self._save_budgets()
        return True, f"Budget set for {month}: ${amount:.2f}"

    def _check_budget(self, month: str) -> None:
        """Check if budget is exceeded for a month and print warning if needed.
        
        Args:
            month: Month in YYYY-MM format
        """
        if month not in self.budgets:
            return
        
        budget = self.budgets[month]
        spent = sum(e['amount'] for e in self.expenses 
                   if e['date'].startswith(month))
        
        if spent > budget:
            percentage = (spent / budget) * 100
            print(f"⚠️  Warning: Budget exceeded for {month}!")
            print(f"   Budget: ${budget:.2f}, Spent: ${spent:.2f} ({percentage:.1f}%)")

    def export_to_csv(self, filename: str, category: Optional[str] = None,
                     month: Optional[str] = None) -> Tuple[bool, str]:
        """Export expenses to CSV file.
        
        Args:
            filename: Output filename
            category: Filter by category (optional)
            month: Filter by month (optional)
            
        Returns:
            Tuple of (success, message)
        """
        filtered_expenses = self.expenses
        
        # Filter by category if provided
        if category:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['category'].lower() == category.lower()]
        
        # Filter by month if provided
        if month:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['date'].startswith(month)]
        
        if not filtered_expenses:
            return False, "No expenses to export"
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'date', 'description', 'amount', 'category'])
                writer.writeheader()
                writer.writerows(filtered_expenses)
            
            return True, f"Expenses exported to {filename} ({len(filtered_expenses)} records)"
        except IOError as e:
            return False, f"Error: Could not write to file {filename}: {e}"

    def _find_expense(self, expense_id: int) -> Optional[Dict]:
        """Find an expense by ID.
        
        Args:
            expense_id: ID of the expense
            
        Returns:
            Expense dict or None if not found
        """
        for expense in self.expenses:
            if expense['id'] == expense_id:
                return expense
        return None


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Expense Tracker - Manage your personal finances",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  expense-tracker add --description "Lunch" --amount 20
  expense-tracker add --description "Gas" --amount 50 --category "Transport"
  expense-tracker list
  expense-tracker list --category "Food"
  expense-tracker summary
  expense-tracker summary --month 2026-05
  expense-tracker update --id 1 --amount 25
  expense-tracker delete --id 1
  expense-tracker set-budget --month 2026-05 --amount 1000
  expense-tracker export --filename expenses.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', type=float, required=True, help='Amount of the expense')
    add_parser.add_argument('--category', default='General', help='Category of the expense (default: General)')
    add_parser.add_argument('--date', help='Date of the expense (YYYY-MM-DD format, default: today)')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an expense')
    update_parser.add_argument('--id', type=int, required=True, help='ID of the expense to update')
    update_parser.add_argument('--description', help='New description')
    update_parser.add_argument('--amount', type=float, help='New amount')
    update_parser.add_argument('--category', help='New category')
    update_parser.add_argument('--date', help='New date (YYYY-MM-DD format)')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the expense to delete')

    # List command
    list_parser = subparsers.add_parser('list', help='List all expenses')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--month', help='Filter by month (YYYY-MM format)')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Get expense summary')
    summary_parser.add_argument('--month', help='Summary for a specific month (YYYY-MM format)')
    summary_parser.add_argument('--category', help='Summary for a specific category')

    # Set budget command
    budget_parser = subparsers.add_parser('set-budget', help='Set a monthly budget')
    budget_parser.add_argument('--month', required=True, help='Month (YYYY-MM format)')
    budget_parser.add_argument('--amount', type=float, required=True, help='Budget amount')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export expenses to CSV')
    export_parser.add_argument('--filename', required=True, help='Output filename')
    export_parser.add_argument('--category', help='Filter by category')
    export_parser.add_argument('--month', help='Filter by month (YYYY-MM format)')

    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Initialize tracker
    tracker = ExpenseTracker()

    # Process commands
    if args.command == 'add':
        success, message = tracker.add_expense(
            args.description,
            args.amount,
            args.category,
            args.date
        )
        print(message)
        sys.exit(0 if success else 1)

    elif args.command == 'update':
        success, message = tracker.update_expense(
            args.id,
            args.description,
            args.amount,
            args.category,
            args.date
        )
        print(message)
        sys.exit(0 if success else 1)

    elif args.command == 'delete':
        success, message = tracker.delete_expense(args.id)
        print(message)
        sys.exit(0 if success else 1)

    elif args.command == 'list':
        print(tracker.list_expenses(args.category, args.month))

    elif args.command == 'summary':
        print(tracker.summary(args.month, args.category))

    elif args.command == 'set-budget':
        success, message = tracker.set_budget(args.month, args.amount)
        print(message)
        sys.exit(0 if success else 1)

    elif args.command == 'export':
        success, message = tracker.export_to_csv(args.filename, args.category, args.month)
        print(message)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
