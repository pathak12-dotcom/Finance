# Expense Tracker

A powerful command-line application to manage your personal finances. Add, update, delete, and analyze your expenses with ease.

## Features

✅ **Core Features**
- Add expenses with description, amount, category, and date
- Update existing expenses
- Delete expenses
- View all expenses with optional filtering
- Get expense summaries (total, by category, by month)
- View expenses for specific months

✅ **Advanced Features**
- Filter expenses by category
- Set monthly budgets and receive warnings when exceeded
- Export expenses to CSV files
- Persistent storage using JSON
- Full error handling and input validation

## Installation

### Prerequisites
- Python 3.6 or higher

### Quick Setup

1. Clone or download the repository
2. Navigate to the project directory
3. Make the script executable:
   ```bash
   chmod +x expense_tracker.py
   ```

### Optional: Setup Command Alias

To use `expense-tracker` command directly:

```bash
chmod +x setup.sh
./setup.sh
```

Then add `~/.local/bin` to your PATH if not already there:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

### Basic Commands

#### Add an Expense

```bash
python3 expense_tracker.py add --description "Lunch" --amount 20
```

With category and date:
```bash
python3 expense_tracker.py add --description "Gas" --amount 50 --category "Transport" --date "2026-05-15"
```

**Output:**
```
Expense added successfully (ID: 1)
```

#### List All Expenses

```bash
python3 expense_tracker.py list
```

**Output:**
```
ID  Date        Description              Amount    Category
----------------------------------------------------------------------
2   2026-05-15  Dinner                   $10.00    Food
1   2026-05-15  Lunch                    $20.00    Food
```

#### List Expenses by Category

```bash
python3 expense_tracker.py list --category "Transport"
```

#### List Expenses for Specific Month

```bash
python3 expense_tracker.py list --month "2026-05"
```

#### View Expense Summary

```bash
python3 expense_tracker.py summary
```

**Output:**
```
Overall Summary:
----------------------------------------
Food                          $30.00
Transport                     $50.00
----------------------------------------
Total expenses: $80.00
```

#### View Summary for Specific Month

```bash
python3 expense_tracker.py summary --month "2026-05"
```

**Output:**
```
Summary for 2026-05:
----------------------------------------
Food                          $30.00
Transport                     $50.00
----------------------------------------
Total expenses: $80.00
```

#### View Summary for Specific Category

```bash
python3 expense_tracker.py summary --category "Food"
```

#### Update an Expense

```bash
python3 expense_tracker.py update --id 1 --amount 25
```

Update multiple fields:
```bash
python3 expense_tracker.py update --id 1 --description "Breakfast" --amount 15 --category "Food"
```

**Output:**
```
Expense 1 updated successfully
```

#### Delete an Expense

```bash
python3 expense_tracker.py delete --id 1
```

**Output:**
```
Expense deleted successfully
```

#### Set a Monthly Budget

```bash
python3 expense_tracker.py set-budget --month "2026-05" --amount 1000
```

**Output:**
```
Budget set for 2026-05: $1000.00
```

When you add expenses, the application will automatically check if you exceed the budget:

```
⚠️  Warning: Budget exceeded for 2026-05!
   Budget: $1000.00, Spent: $1050.00 (105.0%)
```

#### Export to CSV

```bash
python3 expense_tracker.py export --filename expenses.csv
```

Export filtered by category:
```bash
python3 expense_tracker.py export --filename food_expenses.csv --category "Food"
```

Export filtered by month:
```bash
python3 expense_tracker.py export --filename may_expenses.csv --month "2026-05"
```

**Output:**
```
Expenses exported to expenses.csv (10 records)
```

### Help

View all available commands:
```bash
python3 expense_tracker.py -h
```

View help for a specific command:
```bash
python3 expense_tracker.py add -h
python3 expense_tracker.py summary -h
```

## Data Storage

The application stores data in JSON files in the same directory:

- **expenses.json**: Contains all expense records
- **budgets.json**: Contains budget settings by month

### Example expenses.json

```json
[
  {
    "id": 1,
    "description": "Lunch",
    "amount": 20.0,
    "category": "Food",
    "date": "2026-05-15"
  },
  {
    "id": 2,
    "description": "Gas",
    "amount": 50.0,
    "category": "Transport",
    "date": "2026-05-15"
  }
]
```

### Example budgets.json

```json
{
  "2026-05": 1000.0,
  "2026-06": 1200.0
}
```

## Error Handling

The application includes comprehensive error handling:

- **Empty descriptions**: Error message displayed
- **Negative or zero amounts**: Error message displayed
- **Invalid date format**: Must use YYYY-MM-DD format
- **Non-existent expense ID**: Error message displayed
- **Invalid month format**: Must use YYYY-MM format
- **File write errors**: Graceful error handling

## Examples

### Complete Workflow Example

```bash
# Add some expenses
python3 expense_tracker.py add --description "Breakfast" --amount 10 --category "Food"
python3 expense_tracker.py add --description "Uber" --amount 15 --category "Transport"
python3 expense_tracker.py add --description "Movie" --amount 12 --category "Entertainment"

# View all expenses
python3 expense_tracker.py list

# Get overall summary
python3 expense_tracker.py summary

# Set a budget
python3 expense_tracker.py set-budget --month "2026-05" --amount 500

# View budget by category
python3 expense_tracker.py summary --category "Food"

# Export to CSV for analysis
python3 expense_tracker.py export --filename may_expenses.csv --month "2026-05"

# Update an expense
python3 expense_tracker.py update --id 1 --amount 12

# Delete an expense
python3 expense_tracker.py delete --id 3

# Final summary
python3 expense_tracker.py summary
```

## Testing

Run the test suite to verify all functionality:

```bash
python3 test_expense_tracker.py
```

**Output:**
```
...............................................................................
Ran 28 tests in 0.123s

OK
```

### Test Coverage

- Adding expenses (valid and invalid cases)
- Updating expenses
- Deleting expenses
- Listing and filtering expenses
- Summary generation
- Budget management
- CSV export
- Data persistence
- Error handling

## Categories

Default categories include:
- Food
- Transport
- Entertainment
- Utilities
- Health
- General (default)

You can use any custom category - the application is not limited to predefined categories.

## Tips & Best Practices

1. **Consistent date format**: Always use YYYY-MM-DD format for dates
2. **Consistent categories**: Use the same category names for better organization
3. **Regular summaries**: Check your summary monthly to monitor spending
4. **Set budgets**: Use set-budget to stay within your spending limits
5. **Regular backups**: Back up your expenses.json and budgets.json files regularly
6. **Export regularly**: Export expenses to CSV for archiving and analysis

## Troubleshooting

### Command not recognized

If you haven't run the setup script, use the full command:
```bash
python3 expense_tracker.py [command] [options]
```

### Invalid date format errors

Make sure dates follow YYYY-MM-DD format:
- ✅ Correct: 2026-05-15
- ❌ Wrong: 05/15/2026 or 15-05-2026

### Negative amount errors

Amounts must be positive numbers:
- ✅ Correct: 20, 20.00, 20.50
- ❌ Wrong: -20, 0, -20.00

## License

This project is open source and available for personal use.

## Contributing

Feel free to fork and submit pull requests with improvements!
