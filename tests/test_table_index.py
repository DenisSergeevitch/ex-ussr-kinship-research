import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import table_index

try:
    import openpyxl
    import defusedxml
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
        self.assertEqual(r["source"]["sha256"], hashlib.sha256(self.path.read_bytes()).hexdigest())

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

    def test_private_output_and_existing_symlinks(self):
        output = self.path.with_suffix(".json")
        table_index.write_new_result(output, b'{"ok":true}\n')
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        self.assertEqual(list(output.parent.glob(".table-*")), [])
        dangling = output.parent / "dangling.json"
        target = output.parent / "absent.json"
        dangling.symlink_to(target)
        with self.assertRaises(FileExistsError):
            table_index.write_new_result(dangling, b"{}")
        self.assertFalse(target.exists())
        self.assertTrue(dangling.is_symlink())
        self.assertEqual(list(output.parent.glob(".table-*")), [])

    def test_output_inside_skill_rejected_before_creation(self):
        destination = Path(table_index.__file__).resolve().parent / "table-result.json"
        with self.assertRaises(table_index.SourceError):
            table_index.write_new_result(destination, b"{}")
        self.assertFalse(destination.exists())

    def test_input_budget_and_table_width_fail_without_output(self):
        self.write_csv([["имя", "поле"], ["Анна", "=1+1"]])
        with mock.patch.object(table_index, "MAX_INPUT_BYTES", 2):
            with self.assertRaisesRegex(ValueError, "файл превышает"):
                table_index.analyze(self.path, None, ["имя"], ["Анна"], [])
        with mock.patch.object(table_index, "MAX_COLUMNS", 1):
            with self.assertRaisesRegex(ValueError, "столбцов"):
                table_index.analyze(self.path, None, ["имя"], ["Анна"], [])
        result = table_index.analyze(self.path, None, ["имя"], ["Анна"], [])
        self.assertEqual(result["ungrouped_matches"][0]["values"]["поле"], "=1+1")

    def test_source_symlink_and_non_regular_file(self):
        self.write_csv([["имя"], ["Анна"]])
        link = self.path.parent / "linked.csv"
        link.symlink_to(self.path)
        result = table_index.analyze(link, None, ["имя"], ["Анна"], [])
        self.assertEqual(result["source"]["sha256"], hashlib.sha256(self.path.read_bytes()).hexdigest())
        with self.assertRaises(ValueError):
            table_index.read_payload(self.path.parent)

    @unittest.skipIf(openpyxl is None, "optional openpyxl/defusedxml unavailable")
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

    @unittest.skipIf(openpyxl is None, "optional openpyxl/defusedxml unavailable")
    def test_xlsx_formula_header_and_disabled_xml_protection(self):
        path = self.path.with_suffix(".xlsx")
        book = openpyxl.Workbook()
        book.active.append(["=1+1"])
        book.active.append(["Анна"])
        book.save(path)
        book.close()
        with self.assertRaisesRegex(ValueError, "формула в строке 1"):
            table_index.analyze(path, None, ["=1+1"], ["Анна"], [])
        with mock.patch.object(openpyxl, "DEFUSEDXML", False):
            with self.assertRaisesRegex(ValueError, "defusedxml"):
                table_index.analyze(path, None, ["=1+1"], ["Анна"], [])

    @unittest.skipIf(openpyxl is None, "optional openpyxl/defusedxml unavailable")
    def test_xlsx_dimensions_are_not_coverage_and_resource_limits_fail(self):
        path = self.path.with_suffix(".xlsx")
        book = openpyxl.Workbook()
        book.active.append(["имя"])
        book.active.append(["Анна"])
        book.active.append(["Мария"])
        book.save(path)
        book.close()
        payload = path.read_bytes()
        for dimensions in [b"A1:A1", b"A1:XFD1048576"]:
            buffer = io.BytesIO()
            with zipfile.ZipFile(io.BytesIO(payload)) as original, zipfile.ZipFile(buffer, "w") as altered:
                for item in original.infolist():
                    content = original.read(item)
                    if item.filename == "xl/worksheets/sheet1.xml":
                        content = content.replace(b'A1:A3', dimensions)
                    altered.writestr(item, content)
            path.write_bytes(buffer.getvalue())
            result = table_index.analyze(path, None, ["имя"], ["Мария"], [])
            self.assertEqual(result["rows_examined"], 2)
            self.assertEqual(result["ungrouped_matches"][0]["row"], 3)
        with mock.patch.object(table_index, "MAX_ROWS", 2):
            with self.assertRaisesRegex(ValueError, "лимит строк"):
                table_index.analyze(path, None, ["имя"], ["Анна"], [])
        with mock.patch.object(table_index, "MAX_EXPANDED_BYTES", 1):
            with self.assertRaisesRegex(ValueError, "лимит распаковки"):
                table_index.analyze(path, None, ["имя"], ["Анна"], [])

    @unittest.skipIf(openpyxl is None, "optional openpyxl/defusedxml unavailable")
    def test_malformed_xlsx_fails_before_output(self):
        path = self.path.with_suffix(".xlsx")
        book = openpyxl.Workbook()
        book.active.append(["имя"])
        book.save(path)
        book.close()
        buffer = io.BytesIO()
        with zipfile.ZipFile(path) as original, zipfile.ZipFile(buffer, "w") as altered:
            for item in original.infolist():
                content = b"<broken" if item.filename == "xl/workbook.xml" else original.read(item)
                altered.writestr(item, content)
        path.write_bytes(buffer.getvalue())
        output = path.with_suffix(".json")
        proc = subprocess.run([sys.executable, table_index.__file__, str(path), "--name-column", "имя", "--variant", "Анна", "--out", str(output)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
