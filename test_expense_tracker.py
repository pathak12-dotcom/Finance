#!/usr/bin/env python3
"""
Unit tests for the Expense Tracker application.
"""

import unittest
import os
import json
from datetime import datetime
from expense_tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    """Test cases for the ExpenseTracker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_file = "test_expenses.json"
        self.test_budget_file = "test_budgets.json"
        self.tracker = ExpenseTracker(self.test_data_file, self.test_budget_file)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.test_budget_file):
            os.remove(self.test_budget_file)

    def test_add_expense_success(self):
        """Test adding a valid expense."""
        success, message = self.tracker.add_expense("Lunch", 20.00)
        self.assertTrue(success)
        self.assertIn("Expense added successfully", message)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]['description'], "Lunch")
        self.assertEqual(self.tracker.expenses[0]['amount'], 20.00)

    def test_add_expense_with_category(self):
        """Test adding an expense with a category."""
        success, message = self.tracker.add_expense("Gas", 50.00, "Transport")
        self.assertTrue(success)
        self.assertEqual(self.tracker.expenses[0]['category'], "Transport")

    def test_add_expense_with_custom_date(self):
        """Test adding an expense with a custom date."""
        success, message = self.tracker.add_expense("Movie", 15.00, "Entertainment", "2026-05-10")
        self.assertTrue(success)
        self.assertEqual(self.tracker.expenses[0]['date'], "2026-05-10")

    def test_add_expense_empty_description(self):
        """Test that empty description is rejected."""
        success, message = self.tracker.add_expense("", 20.00)
        self.assertFalse(success)
        self.assertIn("Description cannot be empty", message)

    def test_add_expense_negative_amount(self):
        """Test that negative amounts are rejected."""
        success, message = self.tracker.add_expense("Lunch", -20.00)
        self.assertFalse(success)
        self.assertIn("Amount must be greater than 0", message)

    def test_add_expense_zero_amount(self):
        """Test that zero amount is rejected."""
        success, message = self.tracker.add_expense("Lunch", 0)
        self.assertFalse(success)
        self.assertIn("Amount must be greater than 0", message)

    def test_add_expense_invalid_date(self):
        """Test that invalid date format is rejected."""
        success, message = self.tracker.add_expense("Lunch", 20.00, date="05/15/2026")
        self.assertFalse(success)
        self.assertIn("Invalid date format", message)

    def test_update_expense_success(self):
        """Test updating an expense."""
        self.tracker.add_expense("Lunch", 20.00)
        success, message = self.tracker.update_expense(1, amount=25.00)
        self.assertTrue(success)
        self.assertEqual(self.tracker.expenses[0]['amount'], 25.00)

    def test_update_expense_not_found(self):
        """Test updating a non-existent expense."""
        success, message = self.tracker.update_expense(999, amount=25.00)
        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_update_expense_description(self):
        """Test updating expense description."""
        self.tracker.add_expense("Lunch", 20.00)
        success, message = self.tracker.update_expense(1, description="Dinner")
        self.assertTrue(success)
        self.assertEqual(self.tracker.expenses[0]['description'], "Dinner")

    def test_delete_expense_success(self):
        """Test deleting an expense."""
        self.tracker.add_expense("Lunch", 20.00)
        self.assertEqual(len(self.tracker.expenses), 1)
        success, message = self.tracker.delete_expense(1)
        self.assertTrue(success)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_delete_expense_not_found(self):
        """Test deleting a non-existent expense."""
        success, message = self.tracker.delete_expense(999)
        self.assertFalse(success)
        self.assertIn("not found", message)

    def test_list_expenses(self):
        """Test listing expenses."""
        self.tracker.add_expense("Lunch", 20.00)
        self.tracker.add_expense("Dinner", 30.00)
        output = self.tracker.list_expenses()
        self.assertIn("Lunch", output)
        self.assertIn("Dinner", output)
        self.assertIn("$20.00", output)
        self.assertIn("$30.00", output)

    def test_list_expenses_filter_by_category(self):
        """Test filtering expenses by category."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Gas", 50.00, "Transport")
        output = self.tracker.list_expenses(category="Food")
        self.assertIn("Lunch", output)
        self.assertNotIn("Gas", output)

    def test_list_expenses_filter_by_month(self):
        """Test filtering expenses by month."""
        self.tracker.add_expense("Lunch", 20.00, date="2026-05-10")
        self.tracker.add_expense("Dinner", 30.00, date="2026-04-10")
        output = self.tracker.list_expenses(month="2026-05")
        self.assertIn("Lunch", output)
        self.assertNotIn("Dinner", output)

    def test_summary_all_expenses(self):
        """Test generating summary for all expenses."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Gas", 30.00, "Transport")
        output = self.tracker.summary()
        self.assertIn("Total expenses: $50.00", output)
        self.assertIn("Food", output)
        self.assertIn("Transport", output)

    def test_summary_by_month(self):
        """Test generating summary for a specific month."""
        self.tracker.add_expense("Lunch", 20.00, date="2026-05-10")
        self.tracker.add_expense("Dinner", 30.00, date="2026-04-10")
        output = self.tracker.summary(month="2026-05")
        self.assertIn("Total expenses: $20.00", output)
        self.assertNotIn("Dinner", output)

    def test_summary_by_category(self):
        """Test generating summary for a specific category."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Dinner", 30.00, "Food")
        self.tracker.add_expense("Gas", 50.00, "Transport")
        output = self.tracker.summary(category="Food")
        self.assertIn("Total expenses: $50.00", output)
        self.assertNotIn("Transport", output)

    def test_summary_empty(self):
        """Test summary when no expenses exist."""
        output = self.tracker.summary()
        self.assertIn("No expenses found", output)

    def test_set_budget(self):
        """Test setting a budget."""
        success, message = self.tracker.set_budget("2026-05", 1000.00)
        self.assertTrue(success)
        self.assertIn("Budget set", message)
        self.assertEqual(self.tracker.budgets["2026-05"], 1000.00)

    def test_set_budget_negative_amount(self):
        """Test that negative budget is rejected."""
        success, message = self.tracker.set_budget("2026-05", -1000.00)
        self.assertFalse(success)
        self.assertIn("must be greater than 0", message)

    def test_set_budget_invalid_month(self):
        """Test that invalid month format is rejected."""
        success, message = self.tracker.set_budget("05-2026", 1000.00)
        self.assertFalse(success)
        self.assertIn("Invalid month format", message)

    def test_export_to_csv(self):
        """Test exporting expenses to CSV."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Dinner", 30.00, "Food")
        
        csv_file = "test_export.csv"
        success, message = self.tracker.export_to_csv(csv_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_file))
        
        # Verify CSV content
        with open(csv_file, 'r') as f:
            content = f.read()
            self.assertIn("Lunch", content)
            self.assertIn("Dinner", content)
            self.assertIn("20", content)
            self.assertIn("30", content)
        
        # Clean up
        os.remove(csv_file)

    def test_export_to_csv_filter_by_category(self):
        """Test exporting expenses filtered by category."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Gas", 50.00, "Transport")
        
        csv_file = "test_export.csv"
        success, message = self.tracker.export_to_csv(csv_file, category="Food")
        self.assertTrue(success)
        
        with open(csv_file, 'r') as f:
            content = f.read()
            self.assertIn("Lunch", content)
            self.assertNotIn("Gas", content)
        
        os.remove(csv_file)

    def test_persistence(self):
        """Test that expenses are persisted to disk."""
        self.tracker.add_expense("Lunch", 20.00, "Food")
        
        # Create a new tracker instance with the same data file
        new_tracker = ExpenseTracker(self.test_data_file, self.test_budget_file)
        self.assertEqual(len(new_tracker.expenses), 1)
        self.assertEqual(new_tracker.expenses[0]['description'], "Lunch")

    def test_multiple_operations(self):
        """Test multiple operations in sequence."""
        # Add expenses
        self.tracker.add_expense("Lunch", 20.00, "Food")
        self.tracker.add_expense("Dinner", 30.00, "Food")
        self.tracker.add_expense("Gas", 50.00, "Transport")
        
        # Verify total
        output = self.tracker.summary()
        self.assertIn("$100.00", output)
        
        # Delete one
        self.tracker.delete_expense(2)
        
        # Verify new total
        output = self.tracker.summary()
        self.assertIn("$70.00", output)
        
        # Update one
        self.tracker.update_expense(1, amount=25.00)
        
        # Verify final total
        output = self.tracker.summary()
        self.assertIn("$75.00", output)


if __name__ == '__main__':
    unittest.main()
