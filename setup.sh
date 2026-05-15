#!/usr/bin/env bash
# Setup script for Expense Tracker

# Create a symbolic link to make the script executable as a command
if [ ! -d "$HOME/.local/bin" ]; then
    mkdir -p "$HOME/.local/bin"
fi

# Make the expense tracker executable
chmod +x expense_tracker.py

# Create a wrapper script
cat > "$HOME/.local/bin/expense-tracker" << 'EOF'
#!/usr/bin/env python3
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the script directory to Python path
sys.path.insert(0, script_dir)

# Import and run the main function
from expense_tracker import main
main()
EOF

chmod +x "$HOME/.local/bin/expense-tracker"

echo "✓ Expense Tracker setup complete!"
echo "✓ You can now use 'expense-tracker' command"
echo ""
echo "Usage examples:"
echo "  expense-tracker add --description 'Lunch' --amount 20"
echo "  expense-tracker list"
echo "  expense-tracker summary"
echo "  expense-tracker summary --month 2026-05"
echo ""
echo "For more help, run: expense-tracker -h"
