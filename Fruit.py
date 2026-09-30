"""Small CSV-backed inventory application. No third-party dependencies."""

import argparse
import csv
import os
from pathlib import Path
import tempfile

FILENAME = Path(__file__).resolve().with_name("inventory.csv")
LOW_STOCK_THRESHOLD = 10
DEFAULT_INVENTORY = {"Apples": 0, "Bananas": 0, "Carrots": 0}


def validate_inventory(inventory):
    if not inventory:
        raise ValueError("Inventory must contain at least one item.")
    for item, stock in inventory.items():
        if not isinstance(item, str) or not item.strip() or item != item.strip():
            raise ValueError("Item names must be non-empty and trimmed.")
        if type(stock) is not int or stock < 0:
            raise ValueError(f"Invalid stock for {item}: use a non-negative integer.")


def write_inventory(inventory, filename=FILENAME):
    """Replace the CSV only after a complete write; preserve it on failure."""
    validate_inventory(inventory)
    path = Path(filename)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8",
                                         dir=path.parent, delete=False) as file:
            temporary = Path(file.name)
            writer = csv.writer(file)
            writer.writerow(["Item", "Stock"])
            writer.writerows(inventory.items())
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def initialize_inventory(filename=FILENAME):
    if not Path(filename).exists():
        write_inventory(DEFAULT_INVENTORY, filename)


def read_inventory(filename=FILENAME):
    """Reject malformed data instead of silently resetting existing stock."""
    inventory = {}
    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, strict=True)
        if reader.fieldnames != ["Item", "Stock"]:
            raise ValueError("CSV header must be Item,Stock.")
        for row in reader:
            item, stock = row.get("Item"), row.get("Stock")
            if None in row or item is None or stock is None:
                raise ValueError(f"Malformed CSV row at line {reader.line_num}.")
            if item in inventory:
                raise ValueError(f"Duplicate item: {item}.")
            try:
                inventory[item] = int(stock)
            except ValueError as error:
                raise ValueError(f"Invalid stock at line {reader.line_num}.") from error
    validate_inventory(inventory)
    return inventory


def change_stock(inventory, item, quantity, *, remove=False):
    """Validate a transaction before mutating the in-memory inventory."""
    if item not in inventory:
        raise ValueError("Unknown inventory item.")
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive whole number.")
    if remove and quantity > inventory[item]:
        raise ValueError(f"Not enough stock. Current stock for {item}: {inventory[item]}")
    inventory[item] += -quantity if remove else quantity


def low_stock_items(inventory, threshold=LOW_STOCK_THRESHOLD):
    return {item: stock for item, stock in inventory.items() if stock < threshold}


def choose_item(inventory):
    items = list(inventory)
    print("\nSelect an item:")
    for number, item in enumerate(items, 1):
        print(f"{number}. {item}")
    try:
        choice = int(input(f"Enter your choice (1-{len(items)}): "))
        if 1 <= choice <= len(items):
            return items[choice - 1]
    except ValueError:
        pass
    print("Invalid selection. Enter an item number from the list.")
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=FILENAME,
                        help="CSV path (default: inventory.csv beside this script)")
    args = parser.parse_args(argv)
    print("Welcome to the Fruit & Vegetable Inventory Management System!")
    try:
        initialize_inventory(args.file)
        while True:
            inventory = read_inventory(args.file)
            print("\n1. Add Stock Items\n2. Remove Stock Items\n3. Check Stock"
                  "\n4. Low Stock Warning\n5. Exit")
            choice = input("Select an option (1-5): ").strip()
            if choice == "5":
                print("Exiting program. Goodbye!")
                return 0
            if choice in ("1", "2", "3"):
                item = choose_item(inventory)
                if item is None:
                    continue
                if choice == "3":
                    print(f"Current stock for {item}: {inventory[item]} units")
                    continue
                try:
                    quantity = int(input("Enter quantity: "))
                    change_stock(inventory, item, quantity, remove=choice == "2")
                except ValueError as error:
                    print(f"Invalid transaction: {error}")
                    continue
                write_inventory(inventory, args.file)
                print(f"Stock saved. {item}: {inventory[item]} units")
            elif choice == "4":
                low = low_stock_items(inventory)
                print(f"Low stock items (below {LOW_STOCK_THRESHOLD} units):")
                for item, stock in low.items():
                    print(f"- {item}: {stock} units")
                if not low:
                    print("All items have sufficient stock.")
            else:
                print("Invalid choice. Please select between 1 and 5.")
    except (OSError, ValueError, csv.Error) as error:
        print(f"Inventory error: {error}\nCheck the CSV and file permissions. Existing data was not reset.")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nExiting program.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
