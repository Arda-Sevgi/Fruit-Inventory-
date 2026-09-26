# Fruit & Vegetable Inventory Management System

A simple Python-based inventory management system for tracking fruit and vegetable stock. The program uses a CSV file to store inventory data and provides a menu-driven interface for adding, removing, and checking stock levels.

## 📌 Features

- Add stock items
- Remove stock items
- Check the current stock of an item
- Automatically identify low-stock items
- Store inventory data in a CSV file
- Validate user input
- Prevent removing more stock than is currently available
- Automatically initialise the inventory file when the program is first run

## 🛠️ Technologies Used

- **Python 3**
- **CSV** – Used for storing and updating inventory data
- **OS module** – Used to check whether the inventory file exists

## 📂 Inventory

The system starts with three inventory items:

- Apples
- Bananas
- Carrots

A low-stock warning is displayed when an item's stock falls below **10 units**.

## 🚀 Getting Started

### Prerequisites

Make sure Python 3 is installed on your computer.

### Clone the Repository

```bash
git clone https://github.com/Arda-Sevgi/Fruit-Inventory-.git
```

Navigate to the project directory:

```bash
cd Fruit-Inventory-
```

### Run the Program

```bash
python main.py
```

> Replace `main.py` with the actual Python filename if the file has a different name.

## 💻 Main Menu

When the program starts, users can choose from the following options:

```text
1. Add Stock Items
2. Remove Stock Items
3. Check Stock
4. Low Stock Warning
5. Exit
```

### Add Stock

Select an item and enter the quantity you want to add. The inventory is updated and saved to the CSV file.

### Remove Stock

Select an item and enter the quantity to remove. The system checks that enough stock is available before making the change.

### Check Stock

Displays the current quantity of a selected item.

### Low Stock Warning

Checks all inventory items and displays items with fewer than 10 units remaining.

## 💾 Data Storage

Inventory data is stored in `inventory.csv`.

The program automatically creates the file if it does not already exist and initialises it with the default inventory:

```csv
Item,Stock
Apples,0
Bananas,0
Carrots,0
```

Changes made through the program are written back to the CSV file, allowing inventory data to persist between program runs.

## 🎯 Learning Objectives

This project was created to practise Python programming fundamentals and basic data management.

Through this project, I practised:

- Functions and modular programming
- File handling
- Reading and writing CSV files
- Dictionaries
- Loops and conditional statements
- Exception handling
- User input validation
- Basic inventory management logic
- Persistent data storage

## 👤 Author

**Arda Sevgi**

GitHub: [Arda-Sevgi](https://github.com/Arda-Sevgi)
