import csv
import os

FILENAME = "inventory.csv"
LOW_STOCK_THRESHOLD = 10

print(" Welcome to the Fruit & Vegetable Inventory Management System!")

# === Main Menu ===
menu_text = """
=== Main Menu ===
1. Add Stock Items
2. Remove Stock Items
3. Check Stock
4. Low Stock Warning
5. Exit
"""

def initialize_inventory():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item', 'Stock'])
            writer.writerow(['Apples', 0])
            writer.writerow(['Bananas', 0])
            writer.writerow(['Carrots', 0])


def read_inventory():
    inventory = {}
    with open(FILENAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory[row['Item']] = int(row['Stock'])
    return inventory


def write_inventory(inventory):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item', 'Stock'])
        for item, stock in inventory.items():
            writer.writerow([item, stock])


def choose_item():
    items = ['Apples', 'Bananas', 'Carrots']
    print("\nSelect an item:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    try:
        choice = int(input("Enter your choice (1-3): "))
        if 1 <= choice <= 3:
            return items[choice - 1]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# 1. Add Stock Items
def add_stock(inventory):
    item = choose_item()
    if item:
        try:
            qty = int(input(f"Enter quantity to add for {item}: "))
            if qty > 0:
                inventory[item] += qty
                print(f"{qty} units of {item} added successfully.")
            else:
                print("Quantity must be positive.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# 2. Remove Stock Items
def remove_stock(inventory):
    item = choose_item()
    if item:
        try:
            qty = int(input(f"Enter quantity to remove for {item}: "))
            if qty > 0:
                if qty <= inventory[item]:
                    inventory[item] -= qty
                    print(f"{qty} units of {item} removed successfully.")
                else:
                    print(f"Not enough stock. Current stock for {item}: {inventory[item]}")
            else:
                print("Quantity must be positive.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# 3. Check Stock
def check_stock(inventory):
    item = choose_item()
    if item:
        print(f"Current stock for {item}: {inventory[item]} units")

# 4. Low Stock Warning
def low_stock_warning(inventory):
    print("\n Low Stock Items (below threshold of 10 units):")
    low_items = {item: qty for item, qty in inventory.items() if qty < LOW_STOCK_THRESHOLD}
    if low_items:
        for item, qty in low_items.items():
            print(f"- {item}: {qty} units")
    else:
        print(" All items have sufficient stock.")

# 5. Exit
def exit_program():
    print(" Exiting program. Goodbye!")

# Main Program Loop
def main():
    initialize_inventory()
    while True:
        inventory = read_inventory()
        print(menu_text)
        try:
            choice = int(input("Select an option (1-5): "))
            if choice == 1:
                add_stock(inventory)
            elif choice == 2:
                remove_stock(inventory)
            elif choice == 3:
                check_stock(inventory)
            elif choice == 4:
                low_stock_warning(inventory)
            elif choice == 5:
                exit_program()
                break
            else:
                print("Invalid choice. Please select between 1 and 5.")
            write_inventory(inventory)

            again = input("\nWould you like to perform another task? (yes/no): ").strip().lower()
            if again != "yes":
                exit_program()
                break

        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
