import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import table_index

try:
    import openpyxl
except ImportError:
    openpyxl = None


class TableIndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "index.csv"

    def write_csv(self, rows):
        with self.path.open("w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f).writerows(rows)

    def test_search_variants_groups_and_missing_keys(self):
        self.write_csv([
            ["имя", "отец", "мать", "запись"],
            ["Петров", "Иван", "Анна", "10"],
            ["ПЕТРОВА", "ИВАН", "Анна", "11"],
            ["Другая", "Иван", "Анна", "12"],
            ["Петров", "Иван", "", "13"],
            ["Петровский", "Фёдор", "Мария", "14"],
        ])
        r = table_index.analyze(self.path, None, ["имя"], ["петров", "петрова"], ["отец", "мать"])
        self.assertEqual(r["rows_examined"], 5)
        self.assertEqual([row["row"] for row in r["groups"][0]["rows"]], [2, 3, 4])
        self.assertEqual(r["groups"][0]["rows"][2]["matched_variants"], [])
        self.assertEqual(r["ungrouped_matches"][0]["row"], 5)
        self.assertNotIn("Петровский", json.dumps(r, ensure_ascii=False))
        self.assertEqual(len(r["source"]["sha256"]), 64)

    def test_contains_and_multiline_csv_row_locator(self):
        self.write_csv([["имя", "пометка"], ["Другая", "первая\nвторая"], ["Петровский", ""]])
        r = table_index.analyze(self.path, None, ["имя"], ["петров"], [], True)
        self.assertEqual(r["ungrouped_matches"][0]["row"], 4)

    def test_bad_input_fails_without_partial_output(self):
        self.write_csv([["имя", "имя"], ["А", "Б"]])
        proc = subprocess.run([sys.executable, table_index.__file__, str(self.path), "--name-column", "имя", "--variant", "А"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertIn("уникальными", proc.stderr)

    def test_missing_field_and_empty_variant_rejected(self):
        self.write_csv([["имя"], ["Анна"]])
        with self.assertRaisesRegex(ValueError, "нет столбцов"):
            table_index.analyze(self.path, None, ["нет"], ["Анна"], [])
        with self.assertRaisesRegex(ValueError, "непустые варианты"):
            table_index.analyze(self.path, None, ["имя"], ["  "], [])

    def test_output_never_overwrites_existing_file_or_source(self):
        self.write_csv([["имя"], ["Анна"]])
        original = self.path.read_bytes()
        cmd = [sys.executable, table_index.__file__, str(self.path), "--name-column", "имя", "--variant", "Анна", "--out"]
        proc = subprocess.run(cmd + [str(self.path)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(self.path.read_bytes(), original)
        output = self.path.with_suffix(".json")
        self.assertEqual(subprocess.run(cmd + [str(output)], capture_output=True).returncode, 0)
        saved = output.read_bytes()
        self.assertEqual(subprocess.run(cmd + [str(output)], capture_output=True).returncode, 2)
        self.assertEqual(output.read_bytes(), saved)

    @unittest.skipIf(openpyxl is None, "optional openpyxl unavailable")
    def test_xlsx_sheet_selection_rows_and_formula(self):
        path = self.path.with_suffix(".xlsx")
        book = openpyxl.Workbook()
        one = book.active
        one.title = "Другой"
        sheet = book.create_sheet("Рождения")
        sheet.append(["имя", "родитель"])
        sheet.append(["Анна", "Иван"])
        sheet.append(["Мария", "Иван"])
        book.save(path)
        book.close()
        with self.assertRaisesRegex(ValueError, "укажите --sheet"):
            table_index.analyze(path, None, ["имя"], ["Анна"], ["родитель"])
        r = table_index.analyze(path, "Рождения", ["имя"], ["анна"], ["родитель"])
        self.assertEqual([row["row"] for row in r["groups"][0]["rows"]], [2, 3])
        book = openpyxl.load_workbook(path)
        book["Рождения"]["A3"] = "=1+1"
        book.save(path)
        book.close()
        with self.assertRaisesRegex(ValueError, "формула в строке 3"):
            table_index.analyze(path, "Рождения", ["имя"], ["анна"], ["родитель"])


if __name__ == "__main__":
    unittest.main()
