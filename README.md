# Fruit and Vegetable Inventory

A small Python command-line application for managing stock with CSV persistence. I built the original project to practise functions, dictionaries, file handling and input validation. The current version extends it with explicit CSV validation, safer saving and automated regression tests.

**Public source code:** this repository contains the runnable application and its tests. It is a programming project, not a production inventory service.

## Run

Requires Python 3.10 or later. No third-party packages are needed.

```sh
git clone https://github.com/Arda-Sevgi/Fruit-Inventory-.git
cd Fruit-Inventory-
python Fruit.py
```

On systems where Python is named `python3`, use that command instead.

By default, the application reads `inventory.csv` beside `Fruit.py`. It creates a missing file with Apples, Bananas and Carrots at zero stock. It preserves an existing inventory. To try a separate file without changing the sample:

```sh
python Fruit.py --file demo_inventory.csv
```

## Features

- Add and remove positive whole-number quantities.
- Reject unknown items, invalid quantities and removal beyond available stock.
- Check stock and list items below the 10-unit threshold.
- Load selectable items from the CSV rather than a separate hard-coded menu list.
- Validate headers, duplicate names, missing fields and negative or non-integer stock.
- Write to a temporary file and replace the CSV only after a complete write.
- Report file errors without resetting the existing inventory.

## Example

With a new demo inventory, select **1**, choose **1 (Apples)** and add **15** units. Then select **2**, choose Apples and remove **3**. The application saves **12** Apples. Restart it with the same `--file` path and select **3** to check that the quantity persisted.

```text
Stock saved. Apples: 15 units
Stock saved. Apples: 12 units
Current stock for Apples: 12 units
```

## Data format

```csv
Item,Stock
Apples,0
Bananas,0
Carrots,0
```

Each item name must be non-empty, unique and have no surrounding whitespace. Stock must be a non-negative integer. Back up a file before editing it manually; malformed data is rejected rather than repaired automatically.

## Tests

```sh
python -m unittest discover -v
```

The 12 tests use temporary files. They cover persistence, invalid transactions, threshold boundaries, corrupt CSV input, failed saves, Unicode names and the command-line workflow, including execution from another directory. They do not modify the repository's sample inventory.

## Design and limitations

The stock rules are separate from the interactive menu so they can be tested without simulated terminal sessions. CSV keeps the example simple and inspectable. Replacement-based saving protects against incomplete writes, but there is no locking for concurrent users, database, authentication, audit history or guarantee against every storage failure. This application is intended for one local user.

## Author

Arda Sevgi — BSc Computing student at Nottingham Trent University.

[Portfolio](https://arda-sevgi.github.io/Portfolio/) · [LinkedIn](https://www.linkedin.com/in/arda-sevgi-561299389/)
