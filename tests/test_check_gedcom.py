"""Тесты check_gedcom.py на синтетических файлах без семейных данных.

Запуск: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.check_gedcom import check_file

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

HEAD_551 = """0 HEAD
1 SOUR test
1 SUBM @U1@
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
0 @U1@ SUBM
1 NAME Тест
"""

FAMILY = """0 @I1@ INDI
1 NAME Иван /Тестов/
1 REFN P-0001
1 FAMS @F1@
0 @I2@ INDI
1 NAME Мария /Тестова/
1 REFN P-0002
1 FAMS @F1@
0 @I3@ INDI
1 NAME Пётр /Тестов/
1 REFN P-0003
1 BIRT
2 DATE ABT 1890
2 SOUR @S1@
1 FAMC @F1@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
0 @S1@ SOUR
1 TITL Синтетический источник
"""


def gedcom(body: str = FAMILY, head: str = HEAD_551) -> str:
    return head + body + "0 TRLR\n"


class GedcomCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def check(self, text: str, raw: bytes | None = None, case_dir: Path | None = None) -> dict:
        path = self.dir / "tree.ged"
        path.write_bytes(raw if raw is not None else text.encode("utf-8"))
        return check_file(path, case_dir)

    def assertClean(self, result: dict) -> None:
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])


class StructureTest(GedcomCase):
    def test_valid_551_with_any_line_ending_and_bom(self) -> None:
        text = gedcom()
        self.assertClean(self.check(text))
        self.assertClean(self.check("", b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8")))
        result = self.check(text)
        self.assertEqual(result["version"], "5.5.1")
        self.assertEqual(result["counts"], {"INDI": 3, "FAM": 1, "SOUR": 1})

    def test_missing_final_line_break(self) -> None:
        errors = self.check(gedcom().rstrip("\n"))["errors"]
        self.assertTrue(any("перевода строки" in e for e in errors), errors)

    def test_head_requirements_for_551(self) -> None:
        head = "0 HEAD\n1 GEDC\n2 VERS 5.5.1\n"
        errors = self.check(gedcom(head=head))["errors"]
        for tag in ("SOUR", "SUBM", "CHAR", "FORM"):
            self.assertTrue(any(tag in e for e in errors), (tag, errors))

    def test_missing_version_and_order_of_records(self) -> None:
        errors = self.check("0 @I1@ INDI\n0 HEAD\n")["errors"]
        self.assertTrue(any("HEAD" in e and "первая" in e for e in errors), errors)
        self.assertTrue(any("TRLR" in e for e in errors), errors)
        self.assertTrue(any("VERS" in e for e in errors), errors)

    def test_levels_and_blank_lines(self) -> None:
        result = self.check(gedcom(FAMILY.replace("1 TITL", "3 TITL") + "\n"))
        self.assertTrue(any("уровень 3 после уровня 0" in e for e in result["errors"]), result["errors"])
        self.assertTrue(any("пустая строка" in w for w in result["warnings"]), result["warnings"])

    def test_xref_rules(self) -> None:
        body = FAMILY + "0 @I1@ INDI\n1 NAME Дубль\n0 @1X@ NOTE начальная цифра допустима в 5.5.1\n"
        errors = self.check(gedcom(body))["errors"]
        self.assertTrue(any("@I1@ уже объявлен" in e for e in errors), errors)
        self.assertFalse(any("@1X@" in e for e in errors), errors)

    def test_unresolved_and_wrong_target(self) -> None:
        body = FAMILY.replace("2 SOUR @S1@", "2 SOUR @S9@").replace("1 FAMC @F1@", "1 FAMC @F1@\n1 FAMS @S1@")
        errors = self.check(gedcom(body))["errors"]
        self.assertTrue(any("@S9@ не найдена" in e for e in errors), errors)
        self.assertTrue(any("FAMS @S1@ указывает на SOUR" in e for e in errors), errors)

    def test_family_links_must_be_reciprocal(self) -> None:
        errors = self.check(gedcom(FAMILY.replace("1 FAMC @F1@\n", "")))["errors"]
        self.assertTrue(any("@F1@ CHIL @I3@" in e and "FAMC" in e for e in errors), errors)
        errors = self.check(gedcom(FAMILY.replace("1 CHIL @I3@\n", "")))["errors"]
        self.assertTrue(any("@I3@ FAMC @F1@" in e for e in errors), errors)

    def test_repeated_header_and_reserved_void_xref_are_errors(self) -> None:
        result = self.check(gedcom(FAMILY + "0 HEAD\n"))
        self.assertTrue(any("ровно одна запись HEAD" in e for e in result["errors"]), result)
        head = "0 HEAD\n1 GEDC\n2 VERS 7.0\n"
        result = self.check(gedcom("0 @VOID@ INDI\n", head))
        self.assertTrue(any("не как XREF" in e for e in result["errors"]), result)

    def test_deep_extension_tree_does_not_exhaust_python_recursion(self) -> None:
        body = "0 @I1@ INDI\n" + "".join(f"{level} _DETAIL x\n" for level in range(1, 1100))
        result = self.check(gedcom(body, "0 HEAD\n1 GEDC\n2 VERS 7.0\n"))
        self.assertEqual(result["errors"], [], result)

    def test_exact_header_and_change_dates(self) -> None:
        heads = (("5.5.1", HEAD_551.replace("1 SUBM", "1 DATE 1 JAN 2000\n1 SUBM", 1)),
                 ("7", "0 HEAD\n1 GEDC\n2 VERS 7.0\n1 DATE 1 JAN 2000\n"))
        body = FAMILY + "0 @I4@ INDI\n1 CHAN\n2 DATE 2 FEB 2000\n"
        for version, head in heads:
            with self.subTest(version=version):
                self.assertClean(self.check(gedcom(body, head)))
                partial_head = head.replace("1 DATE 1 JAN 2000", "1 DATE JAN 2000")
                approximate_change = body.replace("2 DATE 2 FEB 2000", "2 DATE ABT 2 FEB 2000")
                result = self.check(gedcom(approximate_change, partial_head))
                self.assertTrue(any("HEAD.DATE" in error for error in result["errors"]), result)
                self.assertTrue(any("CHAN.DATE" in error for error in result["errors"]), result)
                self.assertEqual(result["warnings"], [], result)
                dual_year_head = head.replace("1 DATE 1 JAN 2000", "1 DATE 15 FEB 1699/00")
                result = self.check(gedcom(body, dual_year_head))
                self.assertEqual(any("HEAD.DATE" in e for e in result["errors"]), version == "7", result)

    def test_other_date_contexts_share_one_manual_review_warning(self) -> None:
        body = FAMILY + ("0 @S2@ SOUR\n1 DATA\n2 EVEN BIRT\n3 DATE FROM 1800 TO 1900\n"
                         "2 EVEN DEAT\n3 DATE FROM 1900 TO 2000\n")
        result = self.check(gedcom(body))
        self.assertEqual(result["errors"], [], result)
        self.assertEqual(len(result["warnings"]), 1, result)
        self.assertEqual(result["warnings"][0].count("(EVEN)"), 2, result)


class Version551Test(GedcomCase):
    def date_errors(self, value: str) -> list[str]:
        return self.check(gedcom(FAMILY.replace("2 DATE ABT 1890", f"2 DATE {value}")))["errors"]

    def test_valid_dates(self) -> None:
        for value in ("1890", "MAR 1890", "12 MAR 1890", "@#DJULIAN@ 12 MAR 1890", "1699/00",
                      "BET 1890 AND 1895", "FROM 1890 TO 1895", "BEF 1900", "CAL 1890",
                      "(около 1850)", "INT 1850 (по словам семьи)", "850 B.C.",
                      "@#DHEBREW@ 850 B.C.", "@#DFRENCH R@ 850 B.C."):
            with self.subTest(value=value):
                self.assertEqual(self.date_errors(value), [])

    def test_invalid_dates(self) -> None:
        for value in ("около 1850", "1890-03-12", "12.03.1890", "32 MAR 1890", "ABT", "ABT 1850 г."):
            with self.subTest(value=value):
                errors = self.date_errors(value)
                self.assertTrue(any("дата" in e and "GEDCOM 5.5.1" in e for e in errors), errors)

    def test_line_length_and_at_sign(self) -> None:
        body = FAMILY + "0 @N1@ NOTE " + "x" * 260 + "\n1 CONT адрес a@b\n1 CONT a@@b @#DJULIAN@\n"
        result = self.check(gedcom(body))
        self.assertTrue(any("в 5.5.1 не больше 255" in e for e in result["errors"]), result["errors"])
        at_warnings = [w for w in result["warnings"] if "одиночный @" in w]
        self.assertEqual(len(at_warnings), 1, result["warnings"])

    def test_conc_split_at_space(self) -> None:
        body = FAMILY + "0 @N1@ NOTE начало \n1 CONC продолжение\n"
        warnings = self.check(gedcom(body))["warnings"]
        self.assertTrue(any("CONC разрывает текст на пробеле" in w for w in warnings), warnings)

    def test_non_ascii_needs_utf8_char(self) -> None:
        errors = self.check(gedcom(head=HEAD_551.replace("CHAR UTF-8", "CHAR ANSEL")))["errors"]
        self.assertTrue(any("HEAD.CHAR" in e for e in errors), errors)

    def test_not_utf8(self) -> None:
        errors = self.check("", gedcom().encode("cp1251"))["errors"]
        self.assertTrue(any("не в UTF-8" in e for e in errors), errors)


class Version7Test(GedcomCase):
    HEAD_7 = "0 HEAD\n1 GEDC\n2 VERS 7.0\n"

    def test_valid_7(self) -> None:
        body = FAMILY + "0 @I4@ INDI\n1 FAMC @VOID@\n"
        result = self.check(gedcom(body.replace("ABT 1890", "JULIAN 12 MAR 1890"), self.HEAD_7))
        self.assertEqual(result["version"], "7")
        self.assertClean(result)

    def test_rules_specific_to_7(self) -> None:
        body = (FAMILY.replace("ABT 1890", "(около 1890)")
                + "0 @N1@ SNOTE начало\n1 CONC конец\n0 @n2@ SNOTE @ в начале\n")
        errors = self.check(gedcom(body, self.HEAD_7))["errors"]
        self.assertTrue(any("дата" in e and "GEDCOM 7" in e for e in errors), errors)
        self.assertTrue(any("CONC нет в GEDCOM 7" in e for e in errors), errors)
        self.assertTrue(any("недопустимый XREF @n2@" in e for e in errors), errors)
        self.assertTrue(any("начальный @ удваивают" in e for e in errors), errors)

    def test_shared_note_uses_snote_in_7(self) -> None:
        body = "0 @I1@ INDI\n1 NOTE @N1@\n0 @N1@ NOTE общая заметка\n"
        errors = self.check(gedcom(body, self.HEAD_7))["errors"]
        self.assertTrue(any("используют SNOTE" in e for e in errors), errors)
        self.assertClean(self.check(gedcom(body.replace("NOTE", "SNOTE"), self.HEAD_7)))

    def test_disproven_child_link_needs_no_asserted_reverse_child(self) -> None:
        body = "0 @I1@ INDI\n1 FAMC @F1@\n2 STAT DISPROVEN\n0 @F1@ FAM\n"
        self.assertClean(self.check(gedcom(body, self.HEAD_7)))


class RegisterTest(GedcomCase):
    def setUp(self) -> None:
        super().setUp()
        self.case = self.dir / "case"
        subprocess.run([sys.executable, str(SCRIPTS / "init_case.py"), "--case-dir", str(self.case),
                        "--research-question", "q"], check=True, capture_output=True)
        for person_id, living in (("P-0001", "deceased"), ("P-0002", "deceased"), ("P-0003", "deceased")):
            self.add("person-register.csv", person_id=person_id, living_status=living)

    def add(self, name: str, **values: str) -> None:
        path = self.case / name
        with path.open(encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        with path.open("a", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, header, lineterminator="\n").writerow(values)

    def relation(self, rel_id: str, a: str, kind: str, b: str, status: str) -> None:
        self.add("relationship-register.csv", relationship_id=rel_id, person_a_id=a,
                 relationship_type=kind, person_b_id=b, status=status)

    def test_established_links_pass(self) -> None:
        self.relation("R-0001", "P-0001", "spouse-of", "P-0002", "single-source")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "corroborated")
        self.relation("R-0003", "P-0002", "parent-of", "P-0003", "single-source")
        self.assertClean(self.check(gedcom(), case_dir=self.case))

    def test_hypothesis_and_missing_links_are_errors(self) -> None:
        self.relation("R-0001", "P-0001", "spouse", "P-0002", "hypothesis")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "hypothesis")
        errors = self.check(gedcom(), case_dir=self.case)["errors"]
        self.assertTrue(any("пара P-0001 и P-0002" in e and "hypothesis" in e for e in errors), errors)
        self.assertTrue(any("P-0001 parent-of P-0003" in e and "hypothesis" in e for e in errors), errors)
        self.assertTrue(any("P-0002 parent-of P-0003 нет" in e for e in errors), errors)

    def test_existing_spouse_spelling_is_compared(self) -> None:
        self.relation("R-0001", "P-0002", "spouse", "P-0001", "single-source")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "single-source")
        self.relation("R-0003", "P-0002", "parent-of", "P-0003", "single-source")
        self.assertClean(self.check(gedcom(), case_dir=self.case))

    def test_sibling_row_cannot_establish_a_couple(self) -> None:
        self.relation("R-0001", "P-0001", "sibling-of", "P-0002", "corroborated")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "single-source")
        self.relation("R-0003", "P-0002", "parent-of", "P-0003", "single-source")
        result = self.check(gedcom(), case_dir=self.case)
        self.assertEqual(result["errors"], [], result)
        self.assertTrue(any("нет строки spouse-of или spouse" in w and "R-0001 (sibling-of)" in w
                            for w in result["warnings"]), result)

    def test_ambiguous_refn_and_duplicate_register_ids_are_diagnosed(self) -> None:
        body = FAMILY.replace("1 REFN P-0001", "1 REFN P-0001\n1 REFN P-0002")
        result = self.check(gedcom(body), case_dir=self.case)
        self.assertTrue(any("несколько REFN" in e for e in result["errors"]), result)
        self.add("person-register.csv", person_id="P-0001", living_status="deceased")
        result = self.check(gedcom(), case_dir=self.case)
        self.assertTrue(any("дублирующиеся person_id" in e for e in result["errors"]), result)

    def test_malformed_register_returns_diagnostics(self) -> None:
        path = self.case / "relationship-register.csv"
        path.write_text("relationship_id,status\nR-0001,single-source\n", encoding="utf-8")
        result = self.check(gedcom(), case_dir=self.case)
        self.assertTrue(any("отсутствуют колонки" in e for e in result["errors"]), result)
        path.write_text("relationship_id,person_a_id,relationship_type,person_b_id,status\n"
                        "R-0001,P-0001,parent-of,P-0003,single-source,extra\n", encoding="utf-8")
        result = self.check(gedcom(), case_dir=self.case)
        self.assertTrue(any("больше полей" in e for e in result["errors"]), result)

    def test_birth_pedigree_compares_parent_links_in_both_versions(self) -> None:
        self.relation("R-0001", "P-0001", "spouse-of", "P-0002", "single-source")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "single-source")
        for head, pedigree in ((HEAD_551, "birth"), (Version7Test.HEAD_7, "BIRTH")):
            with self.subTest(pedigree=pedigree):
                body = FAMILY.replace("1 FAMC @F1@\n", f"1 FAMC @F1@\n2 PEDI {pedigree}\n")
                result = self.check(gedcom(body, head), case_dir=self.case)
                self.assertTrue(any("P-0002 parent-of P-0003 нет" in e for e in result["errors"]), result)
                self.assertEqual(result["warnings"], [], result)

    def test_qualified_parent_link_requires_review_for_that_child(self) -> None:
        self.relation("R-0001", "P-0001", "spouse-of", "P-0002", "single-source")
        self.add("relationship-register.csv", relationship_id="R-0002", person_a_id="P-0001",
                 relationship_type="parent-of", person_b_id="P-0003", biological_legal_household="legal",
                 status="single-source")
        self.add("person-register.csv", person_id="P-0004", living_status="deceased")
        second_child = "0 @I4@ INDI\n1 REFN P-0004\n1 FAMC @F1@\n2 PEDI birth\n"
        for extra in ("1 FAMC @F1@\n2 PEDI adopted\n",
                      "1 FAMC @F1@\n2 PEDI birth\n2 STAT challenged\n",
                      "1 FAMC @F1@\n2 PEDI birth\n1 ADOP\n2 FAMC @F1@\n3 ADOP HUSB\n"):
            with self.subTest(extra=extra):
                body = FAMILY.replace("1 FAMC @F1@\n", extra)
                body = body.replace("1 CHIL @I3@\n", "1 CHIL @I3@\n1 CHIL @I4@\n")
                result = self.check(gedcom(body + second_child), case_dir=self.case)
                self.assertFalse(any("parent-of P-0003" in e for e in result["errors"]), result)
                self.assertTrue(any("parent-of P-0004 нет" in e for e in result["errors"]), result)
                self.assertTrue(any("CHIL @I3@" in w and "этого ребёнка пропущена" in w
                                    for w in result["warnings"]), result)

    def test_warnings(self) -> None:
        self.add("person-register.csv", person_id="P-0004", living_status="unknown")
        self.relation("R-0002", "P-0001", "parent-of", "P-0003", "single-source")
        self.relation("R-0003", "P-0002", "parent-of", "P-0003", "single-source")
        self.relation("R-0004", "P-0001", "parent-of", "P-0004", "single-source")
        body = (FAMILY.replace("2 SOUR @S1@\n", "") + "0 @I4@ INDI\n1 REFN P-0004\n0 @I5@ INDI\n")
        body = body.replace("1 REFN P-0001\n", "1 REFN P-0001\n1 DEAT Y\n2 NOTE дата не установлена\n")
        warnings = self.check(gedcom(body), case_dir=self.case)["warnings"]
        expected = ("для пары P-0001 и P-0002 нет строки spouse-of или spouse", "R-0004", "living_status unknown",
                    "@I3@ BIRT с датой или местом без SOUR", "не сверены: @I5@")
        for text in expected:
            self.assertTrue(any(text in w for w in warnings), (text, warnings))
        self.assertFalse(any("@I1@ DEAT" in w for w in warnings), warnings)

    def test_cli(self) -> None:
        path = self.dir / "tree.ged"
        path.write_text(gedcom(), encoding="utf-8")
        script = str(SCRIPTS / "check_gedcom.py")
        proc = subprocess.run([sys.executable, script, str(path)], capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Версия: 5.5.1", proc.stdout)
        path.write_text(gedcom(FAMILY.replace("@S1@\n1 FAMC", "@S9@\n1 FAMC")), encoding="utf-8")
        proc = subprocess.run([sys.executable, script, str(path), "--json"], capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        proc = subprocess.run([sys.executable, script, str(self.dir / "missing.ged")],
                              capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        proc = subprocess.run([sys.executable, script, str(path), "--case-dir", str(self.dir)],
                              capture_output=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 2, proc.stderr)


if __name__ == "__main__":
    unittest.main()
