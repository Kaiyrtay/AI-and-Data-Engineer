# ─────────────────────────────────────────────
#  main.py
# ─────────────────────────────────────────────

import sys
from manager import FinanceManager
from storage import JSONStorage
from utils import (
    parse_float,
    format_amount,
    format_date,
    validate_str,
    validate_id,
    validate_transaction_type
)


class FinanceTrackerCLI:

    def __init__(self):
        self.manager = FinanceManager()
        self.storage = JSONStorage()
        self.running = True
        self.load_data()

    def load_data(self):
        try:
            transactions, budgets = self.storage.load()
            self.manager._FinanceManager__transactions = transactions
            self.manager._FinanceManager__budgets = budgets

            if transactions:
                max_id = max(t.id for t in transactions)
                self.manager._FinanceManager__current_id = max_id + 1

            print(
                f"Loaded {len(transactions)} transactions and {len(budgets)} budgets")
        except Exception as e:
            print(f"Error loading data: {e}")

    def save_data(self):
        try:
            self.storage.save(
                self.manager.transactions,
                self.manager.budgets
            )
            print("Data saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")

    def display_header(self):
        """Display welcome header"""
        print("\n" + "=" * 60)
        print(" PERSONAL FINANCE TRACKER CLI ".center(60))
        print("=" * 60)

    def display_menu(self):
        """Display main menu options"""
        menu = """
                Commands:
                add        - Add a new transaction
                remove     - Remove a transaction
                list       - List transactions (with optional filters)
                recurring  - Mark a transaction as recurring
                balance    - View current balance
                budget     - Manage budgets
                report     - Generate financial report
                help       - Show this menu
                exit       - Save and exit

                Type 'help' for more information on any command.
            """
        print(menu)

    def display_help(self, command=None):
        """Display help for a specific command"""
        help_text = {
            "add": """
            ADD - Add a new transaction
            Usage: add
            You will be prompted for:
                - Title: Brief description of the transaction
                - Type: 'income' or 'expense'
                - Amount: Numerical amount (must be positive)
                - Category: Category name (e.g., 'groceries', 'salary', 'utilities')
                - Recurring: Whether it repeats regularly (y/n)
            """,
            "remove": """
            REMOVE - Remove a transaction
            Usage: remove
            You will be prompted for the transaction ID to remove.
            View IDs using the 'list' command.
            """,
            "list": """
            LIST - List transactions with optional filters
            Usage: list
            Shows all transactions by default.
            Options:
                - Filter by type (income/expense)
                - Filter by category
                - View all with no filters
            """,
            "recurring": """
            RECURRING - Mark a transaction as recurring
            Usage: recurring
            Prompts for transaction ID.
            Marks the transaction as recurring=True.
            """,
            "balance": """
            BALANCE - View your financial balance
            Usage: balance
            Shows:
                - Overall balance (income - expenses)
                - Balance by category
            """,
            "budget": """
            BUDGET - Manage category budgets
            Usage: budget
            Options:
                - Add a new budget limit for a category
                - Update budget spent amount
                - View all budgets
            """,
            "report": """
            REPORT - Generate financial reports
            Usage: report
            Shows:
                - Summary by category (income, expense, balance, count)
                - Transaction details
            """,
            "exit": """
            EXIT - Save and close the application
            Usage: exit
            Saves all data to storage and exits the program.
            """
        }

        if command and command.lower() in help_text:
            print(help_text[command.lower()])
        else:
            print("\n" + "=" * 60)
            print("HELP - Available Commands".center(60))
            print("=" * 60)
            for cmd, text in help_text.items():
                print(f"\n{cmd.upper()}")
                print("-" * 40)
                print(text.strip())

    # ─────────────────────────────────────────────
    #  Transaction Commands
    # ─────────────────────────────────────────────

    def cmd_add_transaction(self):
        try:
            print("\n--- Add Transaction ---")

            title = input("Title: ").strip()
            validate_str(title, "Title")

            print("Type (income/expense): ", end="")
            trans_type = input().strip().lower()
            trans_type = validate_transaction_type(trans_type)

            amount_str = input("Amount: $").strip()
            amount = parse_float(amount_str)

            category = input("Category: ").strip().lower()
            category = validate_str(category, "Category")

            recurring_input = input("Recurring? (y/n): ").strip().lower()
            recurring = recurring_input == "y"

            transaction = self.manager.add_transaction(
                title=title,
                transaction_type=trans_type,
                amount=amount,
                category=category,
                recurring=recurring
            )

            print(f"Transaction added: {transaction}")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def cmd_remove_transaction(self):
        try:
            print("\n--- Remove Transaction ---")

            self.cmd_list_transactions()

            trans_id_str = input("\nEnter transaction ID to remove: ").strip()
            trans_id = int(trans_id_str)

            if self.manager.remove_transaction(trans_id):
                print(f"Transaction {trans_id} removed")
            else:
                print(f"Transaction {trans_id} not found")

        except ValueError:
            print("Invalid transaction ID (must be a number)")
        except Exception as e:
            print(f"Error: {e}")

    def cmd_list_transactions(self):
        try:
            print("\n--- List Transactions ---")

            print("\nFilter options:")
            print("  1. Show all")
            print("  2. Filter by type (income/expense)")
            print("  3. Filter by category")

            choice = input("\nChoose option (1-3): ").strip()

            filter_type = None
            filter_category = None

            if choice == "2":
                trans_type = input("Type (income/expense): ").strip().lower()
                filter_type = validate_transaction_type(trans_type)

            elif choice == "3":
                filter_category = input("Category: ").strip().lower()

            transactions = list(self.manager.list_transactions(
                filter_type=filter_type,
                category=filter_category
            ))

            if not transactions:
                print("No transactions found.")
                return

            print("\n" + "-" * 100)
            print(
                f"{'ID':<5} {'Title':<20} {'Type':<10} {'Amount':<15} {'Category':<15} {'Date':<20} {'Recurring':<10}")
            print("-" * 100)

            for trans in transactions:
                recurring_str = "Yes" if trans.recurring else "No"
                date_str = format_date(trans.date)
                amount_str = format_amount(trans.amount)

                print(
                    f"{trans.id:<5} "
                    f"{trans.title:<20} "
                    f"{trans.type:<10} "
                    f"{amount_str:<15} "
                    f"{trans.category:<15} "
                    f"{date_str:<20} "
                    f"{recurring_str:<10}"
                )

            print("-" * 100)
            print(f"Total: {len(transactions)} transaction(s)")

        except Exception as e:
            print(f"Error: {e}")

    def cmd_mark_recurring(self):
        try:
            print("\n--- Mark as Recurring ---")

            self.cmd_list_transactions()

            trans_id_str = input(
                "\nEnter transaction ID to mark as recurring: ").strip()
            trans_id = int(trans_id_str)

            transaction = self.manager.mark_recurring(trans_id)
            if transaction:
                print(f"Transaction {trans_id} marked as recurring")
            else:
                print(f"Transaction {trans_id} not found")

        except ValueError:
            print("Invalid transaction ID (must be a number)")
        except Exception as e:
            print(f"Error: {e}")

    # ─────────────────────────────────────────────
    #  Balance Commands
    # ─────────────────────────────────────────────

    def cmd_get_balance(self):
        try:
            print("\n--- Balance ---")

            overall_balance = self.manager.get_balance()

            print(f"\nOverall Balance: {format_amount(overall_balance)}")

            categories = set()
            for trans in self.manager.transactions:
                categories.add(trans.category)

            if categories:
                print("\nBalance by Category:")
                print("-" * 60)
                print(
                    f"{'Category':<20} {'Income':<15} {'Expenses':<15} {'Balance':<10}")
                print("-" * 60)

                for category in sorted(categories):
                    balance_info = self.manager.get_balance_by_category(
                        category)
                    print(
                        f"{balance_info['category'].title():<20} "
                        f"{format_amount(balance_info['income']):<15} "
                        f"{format_amount(balance_info['expenses']):<15} "
                        f"{format_amount(balance_info['net']):<10}"
                    )

                print("-" * 60)

        except Exception as e:
            print(f"Error: {e}")

    # ─────────────────────────────────────────────
    #  Budget Commands
    # ─────────────────────────────────────────────

    def cmd_budget(self):
        try:
            print("\n--- Budget Management ---")

            print("\nOptions:")
            print("  1. Add budget")
            print("  2. Update budget spent amount")
            print("  3. View all budgets")

            choice = input("\nChoose option (1-3): ").strip()

            if choice == "1":
                self._budget_add()
            elif choice == "2":
                self._budget_update()
            elif choice == "3":
                self._budget_view()
            else:
                print("Invalid option")

        except Exception as e:
            print(f"Error: {e}")

    def _budget_add(self):
        try:
            category = input("Category: ").strip().lower()
            validate_str(category, "Category")

            limit_str = input("Budget limit ($): ").strip()
            limit = parse_float(limit_str)

            budget = self.manager.add_budget(category, limit)
            print(f"Budget added: {budget}")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def _budget_update(self):
        try:
            self._budget_view()

            category = input("\nCategory to update: ").strip().lower()
            amount_str = input("Amount spent ($): ").strip()
            amount = parse_float(amount_str)

            if self.manager.update_budget_spent(category, amount):
                print(f"Budget updated for '{category}'")
            else:
                print(f"Budget not found for '{category}'")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def _budget_view(self):
        budgets = self.manager.budgets

        if not budgets:
            print("No budgets created yet.")
            return

        print("\n" + "-" * 70)
        print(
            f"{'Category':<20} {'Limit':<15} {'Spent':<15} {'Remaining':<15} {'Usage':<10}")
        print("-" * 70)

        for category, budget in sorted(budgets.items()):
            remaining = budget.limit - budget.spent
            usage_pct = (budget.spent / budget.limit *
                         100) if budget.limit > 0 else 0

            print(
                f"{budget.category.title():<20} "
                f"{format_amount(budget.limit):<15} "
                f"{format_amount(budget.spent):<15} "
                f"{format_amount(remaining):<15} "
                f"{usage_pct:>6.1f}%"
            )

        print("-" * 70)

    # ─────────────────────────────────────────────
    #  Report Command
    # ─────────────────────────────────────────────

    def cmd_generate_report(self):
        try:
            print("\n--- Financial Report ---\n")
            self.manager.generate_report()

        except Exception as e:
            print(f"Error: {e}")

    # ─────────────────────────────────────────────
    #  Main Loop
    # ─────────────────────────────────────────────

    def run(self):
        self.display_header()
        # self.display_menu()
        print("Type 'help' for available commands\n")

        while self.running:
            try:
                user_input = input("\n> ").strip().lower()

                if not user_input:
                    continue

                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else None

                if command == "add":
                    self.cmd_add_transaction()
                elif command == "remove":
                    self.cmd_remove_transaction()
                elif command == "list":
                    self.cmd_list_transactions()
                elif command == "recurring":
                    self.cmd_mark_recurring()
                elif command == "balance":
                    self.cmd_get_balance()
                elif command == "budget":
                    self.cmd_budget()
                elif command == "report":
                    self.cmd_generate_report()
                elif command == "help":
                    self.display_help(args)
                elif command == "exit" or command == "quit":
                    self.exit_program()
                else:
                    print(
                        f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                self.exit_program()
            except Exception as e:
                print(f"Unexpected error: {e}")

    def exit_program(self):
        print("\n" + "=" * 60)
        print("Saving and exiting...".center(60))
        self.save_data()
        print("=" * 60)
        print("Goodbye!\n")
        self.running = False


def main():
    try:
        cli = FinanceTrackerCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
