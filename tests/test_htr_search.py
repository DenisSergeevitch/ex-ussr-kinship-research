"""Поиск по машинному распознаванию: нормализация, форматы страниц, ранжирование."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
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
            with self.assertRaises(Exception):
                read_lines(self.write(tmp, "bad.xml", hostile), ["text"])


class Search(unittest.TestCase):
    def test_hyphenated_name_is_joined_across_lines(self):
        texts = [n for n, _ in searchable([["Иванъ Пе-"], ["тровъ"]])]
        self.assertIn("иванпе" + "тров", texts)

    def test_terms_with_variants_and_ranking(self):
        terms = parse_terms(["Сидорчук|Сидорчик", "Петров", "Марфа"])
        full = search_page("a", [["Мѣщанинъ Иванъ Пе-"], ["тровъ Сидарчукъ"]], terms, None)
        partial = search_page("b", [["Марѳа Кузьмина"]], terms, None)
        self.assertEqual(set(full.terms), {"Сидорчук", "Петров"})
        self.assertEqual(full.terms["Сидорчук"][0], 1)
        self.assertGreater(full.score, partial.score)

    def test_short_terms_are_rejected(self):
        with self.assertRaises(Exception):
            parse_terms(["Ия"])

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
        self.assertEqual(result["pages_without_text"], ["0003.txt"])
        self.assertEqual([m["page"] for m in result["matches"]], ["0001"])


if __name__ == "__main__":
    unittest.main()
