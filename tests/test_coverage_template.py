"""Exercise creation and preservation of a source coverage map."""

import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CoverageTemplateTest(unittest.TestCase):
    def test_new_case_has_editable_map_and_reinit_preserves_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "case"
            command = [sys.executable, str(ROOT / "scripts/init_case.py"),
                       "--case-dir", str(case), "--research-question", "Кто родители?"]
            subprocess.run(command, check=True, capture_output=True, text=True)
            coverage = case / "source-coverage.csv"
            with coverage.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                fields = reader.fieldnames
                self.assertEqual(list(reader), [])
            row = {field: "" for field in fields}
            row.update(source_id="S-1", catalog_extent="1890–1892",
                       reviewed_extent="кадры 1–20", review_status="partial",
                       limitations="кадр 12 нечитаем", search_ids="Q-1")
            with coverage.open("a", encoding="utf-8", newline="") as stream:
                csv.DictWriter(stream, fieldnames=fields).writerow(row)
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            with coverage.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream)), [row])


if __name__ == "__main__":
    unittest.main()
