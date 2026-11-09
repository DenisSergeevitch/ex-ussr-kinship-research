"""Тесты audit_evidence.py на временных делах, созданных init_case.py.

Запуск: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.audit_evidence import artifact_groups, has_direct_record

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
CLI_SCRIPTS = ("audit_evidence.py", "build_pdf.py", "check_gedcom.py", "familysearch.py", "gwar.py",
               "hash_artifact.py", "init_case.py", "register_search.py")

ARTIFACT = "{id},,title,url,,,,,,,P-0001,,,,direct,image-of-original,{group},clear,,,{claims},,"
CLAIM = "{id},text,P-0001,birth,{artifacts},{groups},,{status},moderate,rationale,"
PERSON = "{id},,,,,,,,,,,,,,,"
RELATION = "{id},P-0001,parent-of,P-0002,biological,{claims},{artifacts},,{groups},{status},moderate,rationale"


class AuditCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.case = Path(self.tmp.name) / "case"
        subprocess.run(
            [sys.executable, str(SCRIPTS / "init_case.py"), "--case-dir", str(self.case),
             "--research-question", "q"],
            check=True, capture_output=True,
        )
        self.append("person-register.csv", PERSON.format(id="P-0001"), PERSON.format(id="P-0002"))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def append(self, name: str, *lines: str) -> None:
        with (self.case / name).open("a", encoding="utf-8") as handle:
            handle.write("".join(line + "\n" for line in lines))

    def audit(self) -> dict:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "audit_evidence.py"), "--case-dir", str(self.case), "--json"],
            capture_output=True, encoding="utf-8",
        )
        return json.loads(proc.stdout)

    def update_row(self, name: str, record_id: str, **changes: str) -> None:
        path = self.case / name
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        for row in rows:
            if row[fields[0]] == record_id:
                row.update(changes)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def two_artifacts(self, second_group: str = "G2") -> None:
        self.append(
            "artifact-register.csv",
            ARTIFACT.format(id="A-0001", group="G1", claims="C-0001"),
            ARTIFACT.format(id="A-0002", group=second_group, claims="C-0001"),
        )

    def test_row_with_extra_fields_is_reported_not_crash(self):
        self.append("person-register.csv", PERSON.format(id="P-0003") + ",лишнее, поле")
        result = self.audit()
        self.assertTrue(any("person-register.csv: строка 4 содержит больше полей" in e for e in result["errors"]))
        self.assertEqual(result["counts"]["persons"], 3)

    def test_row_with_missing_fields_is_reported(self):
        # Строка короче заголовка: URL попадает в captured_at и т. д. — раньше аудит это пропускал.
        self.append("artifact-register.csv", "A-0001,https://example.org,index,Title,2026-10-28,,index-copy,clear,G1")
        result = self.audit()
        self.assertTrue(any(
            "artifact-register.csv: строка 2 содержит меньше полей, чем заголовок (9 из 23)" in e
            for e in result["errors"]
        ))

    def test_fresh_case_is_clean(self):
        # Плейсхолдеры шаблона отчёта (A-...., R-0001 при пустых реестрах) не дают ошибок.
        result = self.audit()
        self.assertEqual(result["errors"], [])

    def test_cyrillic_output_survives_legacy_pipe_encoding(self):
        # На Windows вывод в pipe идёт в cp1252; PYTHONIOENCODING воспроизводит это на любой ОС.
        env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
        for script in CLI_SCRIPTS:
            with self.subTest(script=script):
                proc = subprocess.run([sys.executable, str(SCRIPTS / script), "--help"],
                                      capture_output=True, encoding="utf-8", env=env)
                self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = subprocess.run([sys.executable, str(SCRIPTS / "audit_evidence.py"), "--case-dir", str(self.case)],
                              capture_output=True, encoding="utf-8", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Проверено дело", proc.stdout)
        proc = subprocess.run([sys.executable, str(SCRIPTS / "hash_artifact.py"), str(self.case / "missing")],
                              capture_output=True, encoding="utf-8", env=env)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("Ошибка: файл не найден", proc.stderr)
        for script in ("audit_evidence.py", "build_pdf.py", "hash_artifact.py", "init_case.py"):
            with self.subTest(script=script, isolated=True):
                proc = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), "--help"],
                                      capture_output=True, encoding="utf-8")
                self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_init_creates_research_state(self):
        text = (self.case / "research-state.md").read_text(encoding="utf-8")
        self.assertIn("## Очередь проверок", text)

    def test_partial_report_without_claims_has_no_length_gate(self):
        self.append("final-report.md", *[f"Ограничение поиска {n}: источник недоступен." for n in range(15)])
        result = self.audit()
        self.assertEqual(result["errors"], [])
        self.assertFalse(any("реестр утверждений пуст" in w for w in result["warnings"]), result["warnings"])

    def test_found_search_without_artifact_warns(self):
        row = "S-0001,,,,q,,,,{status},{artifacts},,,"
        self.append("search-log.csv", row.format(status="found", artifacts=""))
        result = self.audit()
        self.assertEqual(result["counts"]["searches"], 1)
        self.assertTrue(
            any("S-0001" in w and "artifact_ids пуст" in w for w in result["warnings"]), result["warnings"]
        )

    def test_partial_search_unknown_artifact_warns(self):
        self.append("search-log.csv", "S-0001,,,,q,,,,partial,A-9999,,,")
        result = self.audit()
        self.assertTrue(any("S-0001" in w and "A-9999" in w for w in result["warnings"]), result["warnings"])

    def test_found_search_with_artifact_or_not_found_is_clean(self):
        row = "S-0001,,,,q,,,,{status},{artifacts},,,"
        self.two_artifacts()
        self.append("search-log.csv", row.format(status="found", artifacts="A-0001"),
                    row.replace("S-0001", "S-0002").format(status="not-found", artifacts=""))
        result = self.audit()
        self.assertFalse(any("artifact_ids пуст" in w for w in result["warnings"]), result["warnings"])

    def test_declared_group_without_artifact_is_error(self):
        self.append("artifact-register.csv", ARTIFACT.format(id="A-0001", group="G1", claims="C-0001"))
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001", groups="G1;G2", status="corroborated"))
        result = self.audit()
        self.assertTrue(any("C-0001: independence_group G2" in e for e in result["errors"]))
        self.assertTrue(any("C-0001: статус corroborated" in w for w in result["warnings"]))

    def test_backed_groups_corroborate(self):
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="G1;G2", status="corroborated"))
        result = self.audit()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_copies_share_group(self):
        self.two_artifacts(second_group="G1")
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="G1", status="corroborated"))
        result = self.audit()
        self.assertTrue(any("найдено независимых групп: 1" in w for w in result["warnings"]))

    def test_group_case_and_whitespace_do_not_create_independence(self):
        self.assertEqual(
            artifact_groups(["A-0001", "A-0002"], {
                "A-0001": {"independence_group": " G1 "},
                "A-0002": {"independence_group": "   "},
            }),
            {"g1"},
        )
        self.two_artifacts(second_group="  g1  ")
        self.append("artifact-register.csv", ARTIFACT.format(id="A-0003", group="   ", claims="C-0001"))
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002;A-0003", groups="G1;g1", status="corroborated"))
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="g1",
                                    status="corroborated"))
        result = self.audit()
        self.assertEqual(result["errors"], [])
        self.assertIn("A-0003: не указан independence_group", result["warnings"])
        self.assertTrue(any("C-0001: статус corroborated, но найдено независимых групп: 1" in w
                            for w in result["warnings"]))
        self.assertTrue(any("R-0001: статус corroborated, но указано независимых групп: 1" in w
                            for w in result["warnings"]))

    def test_strong_corroboration_needs_one_direct_original_record(self):
        self.two_artifacts()
        self.update_row("artifact-register.csv", "A-0001", originality="derivative", provenance_level="documented")
        self.update_row("artifact-register.csv", "A-0002", directness="indirect", provenance_level="documented")
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="", status="strongly-corroborated"))
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="",
                                    status="strongly-corroborated"))
        warnings = self.audit()["warnings"]
        for record_id in ("C-0001", "R-0001"):
            self.assertTrue(any(w.startswith(record_id + ": strongly-corroborated без единой прямой записи")
                                for w in warnings))

    def test_strong_corroboration_checks_provenance_and_locator(self):
        self.assertFalse(has_direct_record(["A-0001"], {
            "A-0001": {"directness": "direct", "originality": "original", "provenance_level": "documented",
                       "source_url_or_path": "   ", "archival_reference": "   "},
        }))
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="", status="strongly-corroborated"))
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="",
                                    status="strongly-corroborated"))
        self.update_row("artifact-register.csv", "A-0002", directness="indirect")
        for provenance, locator, qualifies in [
            ("", "url", False),
            ("unknown", "url", False),
            ("documented", "", False),
            ("documented", "   ", False),
            ("documented", "url", True),
        ]:
            with self.subTest(provenance=provenance, locator=locator):
                self.update_row("artifact-register.csv", "A-0001", provenance_level=provenance,
                                source_url_or_path=locator)
                result = self.audit()
                self.assertEqual(result["errors"], [])
                for record_id in ("C-0001", "R-0001"):
                    missing_record = any(w.startswith(record_id + ": strongly-corroborated без единой прямой записи")
                                         for w in result["warnings"])
                    self.assertEqual(missing_record, not qualifies)

    def test_corroborated_conflicts_warn_for_claims_and_relationships(self):
        self.two_artifacts()
        self.append("artifact-register.csv", ARTIFACT.format(id="A-0003", group="G3", claims=""))
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="", status="corroborated"))
        self.update_row("claims-register.csv", "C-0001", contradicting_artifact_ids="A-0003")
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="", status="corroborated"),
                    RELATION.format(id="R-0002", claims="", artifacts="A-0001;A-0002", groups="", status="corroborated"))
        self.update_row("relationship-register.csv", "R-0002", contradicting_artifact_ids="A-0003")
        result = self.audit()
        self.assertEqual(result["errors"], [])
        for record_id in ("C-0001", "R-0001", "R-0002"):
            self.assertTrue(any(w.startswith(record_id + ": статус corroborated, но указаны противоречащие артефакты")
                                for w in result["warnings"]))

    def test_person_references_and_relationship_status_are_checked(self):
        self.two_artifacts()
        self.update_row("artifact-register.csv", "A-0001", person_ids="P-9999")
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001", groups="", status="single-source"))
        self.update_row("claims-register.csv", "C-0001", subject_person_ids="P-9998")
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="", status="invented"))
        self.update_row("relationship-register.csv", "R-0001", person_b_id="P-9997")
        result = self.audit()
        for expected in ("A-0001: неизвестный person_id P-9999",
                         "C-0001: неизвестный subject_person_id P-9998",
                         "R-0001: неизвестный person_b_id P-9997"):
            self.assertIn(expected, result["errors"])
        self.assertIn("R-0001: неизвестный статус 'invented'", result["warnings"])

    def test_relationship_groups_come_from_claims(self):
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001;A-0002", groups="", status="corroborated"))
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="G1;G2",
                                    status="corroborated"),
                    RELATION.format(id="R-0002", claims="", artifacts="A-0001", groups="G1;G9",
                                    status="corroborated"))
        result = self.audit()
        self.assertFalse(any(e.startswith("R-0001") for e in result["errors"]))
        self.assertTrue(any("R-0002: independence_group G9" in e for e in result["errors"]))

    def test_report_unknown_ids_are_errors(self):
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001", groups="", status="single-source"))
        self.append("final-report.md", "", "Вывод [A-0001; A-0099], см. C-0042.")
        errors = self.audit()["errors"]
        self.assertTrue(any("A-0099" in e for e in errors))
        self.assertTrue(any("C-0042" in e for e in errors))
        self.assertFalse(any("A-0001" in e for e in errors))

    def test_report_unknown_ids_with_empty_registers(self):
        self.append("final-report.md", "", "Вывод [A-0099], см. C-0042 и R-0003.")
        errors = self.audit()["errors"]
        for cited in ("A-0099", "C-0042", "R-0003"):
            self.assertTrue(any(cited in error for error in errors), cited)

    def test_report_status_must_match_register(self):
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001", groups="", status="single-source"))
        self.append("relationship-register.csv",
                    RELATION.format(id="R-0001", claims="C-0001", artifacts="", groups="",
                                    status="single-source"))
        self.append("final-report.md", "", "### R-0001: P-0001 — отец — P-0002", "",
                    "**Статус:** `corroborated`", "",
                    "| C-0001 | текст | corroborated | A-0001 |  |  |")
        errors = self.audit()["errors"]
        self.assertTrue(any("R-0001 — в отчёте corroborated, в реестре single-source" in e for e in errors))
        self.assertTrue(any("C-0001 — в отчёте corroborated, в реестре single-source" in e for e in errors))

    def test_summary_counts_open_items(self):
        self.two_artifacts()
        self.append("claims-register.csv",
                    CLAIM.format(id="C-0001", artifacts="A-0001", groups="", status="hypothesis"))
        self.append("final-report.md", "Фамилия [неразборчиво], отец [предположительно: Пётр].")
        summary = self.audit()["summary"]
        self.assertEqual(summary["claims_by_status"], {"hypothesis": 1})
        self.assertEqual(summary["report_markers"], {"неразборчиво": 1, "предположительно": 1})


if __name__ == "__main__":
    unittest.main()
