"""Behavioural tests using isolated temporary files, never the real inventory."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import Fruit


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "inventory.csv"

    def test_initialization_preserves_existing_data(self):
        Fruit.initialize_inventory(self.path)
        self.assertEqual(Fruit.read_inventory(self.path), Fruit.DEFAULT_INVENTORY)
        Fruit.write_inventory({"Apples": 17}, self.path)
        Fruit.initialize_inventory(self.path)
        self.assertEqual(Fruit.read_inventory(self.path), {"Apples": 17})

    def test_transaction_persists_after_reload(self):
        stock = {"Apples": 10}
        Fruit.change_stock(stock, "Apples", 5)
        Fruit.change_stock(stock, "Apples", 3, remove=True)
        Fruit.write_inventory(stock, self.path)
        self.assertEqual(Fruit.read_inventory(self.path), {"Apples": 12})

    def test_invalid_transactions_leave_stock_unchanged(self):
        for item, qty, remove in [("Apples", 0, False), ("Apples", -1, False),
                                  ("Apples", 1.5, False), ("Apples", True, False),
                                  ("Apples", 11, True), ("Unknown", 1, False)]:
            with self.subTest(item=item, qty=qty, remove=remove):
                stock = {"Apples": 10}
                with self.assertRaises(ValueError):
                    Fruit.change_stock(stock, item, qty, remove=remove)
                self.assertEqual(stock, {"Apples": 10})

    def test_removing_all_stock_is_valid(self):
        stock = {"Apples": 10}
        Fruit.change_stock(stock, "Apples", 10, remove=True)
        self.assertEqual(stock["Apples"], 0)

    def test_low_stock_threshold_boundary(self):
        self.assertEqual(Fruit.low_stock_items({"A": 9, "B": 10, "C": 11}), {"A": 9})

    def test_corrupt_csv_is_rejected_without_modification(self):
        for data in ["Name,Count\nApples,1\n", "Item,Stock\nApples,-1\n",
                     "Item,Stock\nApples,x\n", "Item,Stock\nApples,1\nApples,2\n",
                     "Item,Stock\nApples\n", "Item,Stock\nApples,1,extra\n",
                     "Item,Stock\n,1\n", "Item,Stock\n"]:
            with self.subTest(data=data):
                self.path.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    Fruit.read_inventory(self.path)
                self.assertEqual(self.path.read_text(encoding="utf-8"), data)

    def test_failed_save_preserves_csv_and_removes_temp_file(self):
        Fruit.write_inventory({"Apples": 10}, self.path)
        before = self.path.read_bytes()
        with patch("Fruit.os.replace", side_effect=PermissionError("blocked")):
            with self.assertRaises(PermissionError):
                Fruit.write_inventory({"Apples": 99}, self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_save_does_not_replace_existing_csv(self):
        Fruit.write_inventory({"Apples": 10}, self.path)
        with self.assertRaises(ValueError):
            Fruit.write_inventory({"Apples": -1}, self.path)
        self.assertEqual(Fruit.read_inventory(self.path), {"Apples": 10})

    def test_csv_round_trip_with_unicode_and_comma(self):
        stock = {"Green apples, large": 3, "Çilek": 5}
        Fruit.write_inventory(stock, self.path)
        self.assertEqual(Fruit.read_inventory(self.path), stock)

    def test_cli_add_remove_and_exit(self):
        with patch("builtins.input", side_effect=["1", "1", "15", "2", "1", "3", "5"]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(Fruit.main(["--file", str(self.path)]), 0)
        self.assertEqual(Fruit.read_inventory(self.path)["Apples"], 12)
        self.assertIn("Stock saved", output.getvalue())

    def test_cli_corrupt_file_reports_error(self):
        self.path.write_text("broken\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(Fruit.main(["--file", str(self.path)]), 1)
        self.assertEqual(self.path.read_text(), "broken\n")

    def test_cli_runs_from_another_directory(self):
        result = subprocess.run([sys.executable, str(Path(Fruit.__file__).resolve()),
                                 "--file", str(self.path)], input="5\n", text=True,
                                capture_output=True, cwd=self.directory.name)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(self.path.exists())


if __name__ == "__main__":
    unittest.main()
