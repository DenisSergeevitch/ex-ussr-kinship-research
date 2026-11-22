"""Поиск по машинному распознаванию: нормализация, форматы страниц, ранжирование."""

from __future__ import annotations

import contextlib
import argparse
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.htr_search import (
    default_edits,
    main,
    normalize,
    parse_terms,
    read_lines,
    search_page,
    searchable,
    stem,
    substring_distance,
)

PAGE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15">
  <Page imageFilename="0007.jpg" imageWidth="100" imageHeight="100">
    <TextRegion id="r1">
      <TextLine id="l1"><TextEquiv><Unicode>Мѣщанинъ Иванъ Пе-</Unicode></TextEquiv></TextLine>
      <TextLine id="l2"><TextEquiv><Unicode>тровъ Сидорчукъ</Unicode></TextEquiv></TextLine>
      <TextEquiv><Unicode>Мѣщанинъ Иванъ Петровъ Сидорчукъ</Unicode></TextEquiv>
    </TextRegion>
  </Page>
</PcGts>
"""

ALTO_XML = """<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v4#"><Layout><Page><PrintSpace>
  <TextBlock><TextLine><String CONTENT="Сынъ"/><String CONTENT="Ѳеодоръ"/></TextLine></TextBlock>
</PrintSpace></Page></Layout></alto>
"""


class Normalization(unittest.TestCase):
    def test_folds_prereform_ukrainian_and_latin_lookalikes(self):
        self.assertEqual(normalize("Ѳеодоръ"), "феодор")
        self.assertEqual(normalize("Мѣщанинъ"), "мещанин")
        self.assertEqual(normalize("Гончарук-Лисенко"), "гончаруклисенко")
        self.assertEqual(normalize("Сидорчукова Ганна Їжакова"), "сидорчуковаганнаижакова")
        self.assertEqual(normalize("Iванъ"), "иван")  # латинская I вместо кириллической
        self.assertEqual(normalize("Сидоровскій"), normalize("Сидоровский"))

    def test_stem_removes_adjective_surname_endings(self):
        self.assertEqual(stem(normalize("Сидоровская")), "сидоровск")
        self.assertEqual(stem(normalize("Сидоровскаго")), "сидоровск")
        self.assertEqual(stem(normalize("Сидоровська")), "сидоровск")
        self.assertEqual(stem(normalize("Петрова")), "петров")
        self.assertEqual(stem(normalize("Хая")), "хая")

    def test_default_edits_are_strict_for_short_stems(self):
        self.assertEqual(default_edits("хана"), 0)
        self.assertEqual(default_edits("петров"), 1)
        self.assertEqual(default_edits("сидорчук"), 2)

    def test_substring_distance(self):
        self.assertEqual(substring_distance("петров", "иванпетровсидорчук"), 0)
        self.assertEqual(substring_distance("сидорчук", "иванпетровсидарчук"), 1)
        self.assertEqual(substring_distance("", "что угодно"), 0)


class Formats(unittest.TestCase):
    def write(self, tmp: str, name: str, text: str) -> Path:
        path = Path(tmp) / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_page_xml_reads_lines_not_region_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = read_lines(self.write(tmp, "0007.xml", PAGE_XML), ["text"])
        self.assertEqual(lines, [["Мѣщанинъ Иванъ Пе-"], ["тровъ Сидорчукъ"]])

    def test_alto(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = read_lines(self.write(tmp, "p1.xml", ALTO_XML), ["text"])
        self.assertEqual(lines, [["Сынъ Ѳеодоръ"]])

    def test_json_with_several_reading_variants(self):
        data = [{"text": "Ивань Петрав", "alt": "Иванъ Петровъ"}, {"text": ""}, "Сидорчукъ"]
        with tempfile.TemporaryDirectory() as tmp:
            lines = read_lines(self.write(tmp, "p.json", json.dumps(data, ensure_ascii=False)), ["text", "alt"])
        self.assertEqual(lines, [["Ивань Петрав", "Иванъ Петровъ"], ["Сидорчукъ"]])

    def test_xml_with_doctype_is_rejected(self):
        hostile = '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]><PcGts/>'
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ET.ParseError):
                read_lines(self.write(tmp, "bad.xml", hostile), ["text"])

    def test_utf16_xml_doctype_is_rejected_before_entity_expansion(self):
        hostile = '<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE PcGts [<!ENTITY a "Петров">]><PcGts><Page><TextLine><TextEquiv><Unicode>&a;</Unicode></TextEquiv></TextLine></Page></PcGts>'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.xml"
            path.write_bytes(hostile.encode("utf-16"))
            with self.assertRaisesRegex(ET.ParseError, "DOCTYPE/ENTITY"):
                read_lines(path, ["text"])

    def test_json_wrong_shapes_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for data in [None, 17, "Петров", {"lines": "Петров"}, [17],
                         {"pages": []}, [{"text": ["Петров"]}], [{"other": "Петров"}]]:
                with self.subTest(data=data):
                    path = self.write(tmp, "bad.json", json.dumps(data, ensure_ascii=False))
                    with self.assertRaises(ValueError):
                        read_lines(path, ["text"])
            self.assertEqual(read_lines(self.write(tmp, "empty.json", '["", {"text": ""}]'), ["text"]), [])

    def test_page_xml_keeps_alternate_line_readings(self):
        xml = PAGE_XML.replace('<Unicode>Мѣщанинъ Иванъ Пе-</Unicode></TextEquiv>',
                               '<Unicode>Мѣщанинъ Иванъ Пе-</Unicode></TextEquiv><TextEquiv><Unicode>Сынъ Пе-</Unicode></TextEquiv>')
        with tempfile.TemporaryDirectory() as tmp:
            lines = read_lines(self.write(tmp, "alternates.xml", xml), ["text"])
        self.assertEqual(lines[0], ["Мѣщанинъ Иванъ Пе-", "Сынъ Пе-"])

    def test_xml_does_not_combine_multiple_pages(self):
        xml = '<alto><Layout><Page/><Page/></Layout></alto>'
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "одну страницу"):
                read_lines(self.write(tmp, "pages.xml", xml), ["text"])


class Search(unittest.TestCase):
    def test_hyphenated_name_is_joined_across_lines(self):
        texts = [n for n, _ in searchable([["Иванъ Пе-"], ["тровъ"]])]
        self.assertIn("иванпе" + "тров", texts)

    def test_hyphenated_reading_can_join_an_alternate_next_line(self):
        terms = parse_terms(["Сидорчук"])
        result = search_page("p1", [["Сидор-"], ["тьк", "чук"]], terms, 0)
        self.assertIn("Сидорчук", result.terms)

    def test_terms_with_variants_and_ranking(self):
        terms = parse_terms(["Сидорчук|Сидорчик", "Петров", "Марфа"])
        full = search_page("a", [["Мѣщанинъ Иванъ Пе-"], ["тровъ Сидарчукъ"]], terms, None)
        partial = search_page("b", [["Марѳа Кузьмина"]], terms, None)
        self.assertEqual(set(full.terms), {"Сидорчук", "Петров"})
        self.assertEqual(full.terms["Сидорчук"][0], 1)
        self.assertGreater(full.score, partial.score)

    def test_short_terms_are_rejected(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_terms(["Ия"])

    def test_duplicate_labels_or_normalized_terms_are_rejected(self):
        for values in [["Петров", "Петровъ"], ["Иван|Пётр", "Иван|Егор"]]:
            with self.subTest(values=values), self.assertRaises(argparse.ArgumentTypeError):
                parse_terms(values)

    def test_cli_reports_pages_without_text_and_min_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "0001.txt").write_text("Сынъ Петръ\nотецъ Иванъ Сидорчукъ\n", encoding="utf-8")
            (root / "0002.txt").write_text("Дочь Марія\n", encoding="utf-8")
            (root / "0003.txt").write_text("", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                main([str(root), "--term", "Сидорчук", "--term", "Петр", "--min-terms", "2", "--json"])
            result = json.loads(out.getvalue())
        self.assertEqual(result["pages_total"], 3)
        self.assertEqual(result["pages_without_text"], [str(root / "0003.txt")])
        self.assertEqual([m["page"] for m in result["matches"]], ["0001"])

    def test_cli_reports_partial_failure_and_preserves_valid_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.txt"
            good.write_text("Петров", encoding="utf-8")
            (root / "bad.json").write_text('{"lines": 17}', encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main([str(root), str(root / "missing.txt"), "--term", "Петров", "--json"])
            result = json.loads(out.getvalue())
        self.assertEqual(status, 1)
        self.assertEqual(result["pages_with_text"], 1)
        self.assertEqual(len(result["pages_failed"]), 1)
        self.assertEqual(len(result["input_errors"]), 1)
        self.assertEqual(result["matches"][0]["source_file"], str(good))

    def test_cli_rejects_unpaired_surrogates_and_keeps_other_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "good.txt").write_text("Петров", encoding="utf-8")
            for name, data in [("string.json", {"lines": ["Петров" + chr(0xd800)]}),
                               ("field.json", {"lines": [{"text": "Петров" + chr(0xd800)}]})]:
                (root / name).write_text(json.dumps(data), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main([str(root), "--term", "Петров", "--json"])
            out.getvalue().encode("utf-8")
            result = json.loads(out.getvalue())
        self.assertEqual(status, 1)
        self.assertEqual(result["pages_with_text"], 1)
        self.assertEqual(len(result["pages_failed"]), 2)
        self.assertEqual(result["pages_matched"], 1)

    def test_cli_deduplicates_files_and_distinguishes_matching_basenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for name in ["a", "b"]:
                folder = Path(tmp) / name
                folder.mkdir()
                path = folder / "0001.txt"
                path.write_text("Петров", encoding="utf-8")
                paths.append(path)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = main([str(paths[0].parent), str(paths[0]), str(paths[1]), "--term", "Петров", "--top", "1", "--json"])
            result = json.loads(out.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(result["pages_total"], 2)
        self.assertEqual(set(result["files_with_text"]), set(map(str, paths)))
        self.assertEqual(result["pages_matched"], 2)
        self.assertEqual(result["matches_shown"], 1)

    def test_cli_rejects_invalid_numeric_options(self):
        for flags in [["--top", "-1"], ["--min-terms", "0"], ["--min-terms", "2"], ["--max-edits", "-1"]]:
            with self.subTest(flags=flags), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    main(["unused.txt", "--term", "Петров", *flags])
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
