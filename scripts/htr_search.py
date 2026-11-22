#!/usr/bin/env python3
"""Нечёткий поиск имён по машинному распознаванию серии сканов.

Читает построчный результат распознавания рукописи или печати (PAGE XML,
ALTO, JSON или TXT по одному файлу на страницу) и ранжирует страницы по числу
найденных поисковых терминов. Каждый термин может иметь варианты через «|»:
`--term "Сидорчук|Сидорчик" --term "Марфа|Марѳа"`. Сравнение терпит ошибки
распознавания: учитываются дореформенные буквы, украинские формы, латинские
двойники кириллицы, перенос слова на следующую строку и окончания
прилагательных фамилий.

Результат — список страниц для проверки по изображению, а не чтение записи.
Отсутствие совпадений не доказывает отсутствия записи: машинное
распознавание пропускает часть слов, особенно редкие фамилии.
Скрипт использует только стандартную библиотеку Python.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

SUFFIXES = {".xml", ".json", ".txt"}
HYPHENS = ("-", "‐", "—", "–", "¬", "=")
LATIN_HOMOGLYPHS = str.maketrans({
    "a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х", "y": "у",
    "k": "к", "m": "м", "t": "т", "h": "н", "b": "в", "i": "и", "u": "и", "n": "п",
})
FOLD = (("ѣ", "е"), ("і", "и"), ("ї", "и"), ("є", "е"), ("ѳ", "ф"), ("ё", "е"),
        ("й", "и"), ("ґ", "г"), ("ы", "и"), ("ъ", ""), ("ь", ""))
ADJ_ENDING = re.compile(r"(ск|цк)(ии|ая|ого|аго|ои|ою|ую|ие|их|ими|ому|ее|еи|а|и|е|о)$")


def normalize(text: str) -> str:
    """Сводит написание к сравнимому виду: строчные, без ъ/ь, ѣ→е, і→и и т. п."""
    text = text.lower().translate(LATIN_HOMOGLYPHS)
    for old, new in FOLD:
        text = text.replace(old, new)
    return re.sub(r"[^а-я]", "", text)


def stem(normalized: str) -> str:
    """Отбрасывает окончание прилагательной фамилии или одну конечную гласную."""
    stemmed = ADJ_ENDING.sub(r"\1", normalized)
    if stemmed == normalized and len(normalized) >= 6:
        stemmed = re.sub(r"[аеиоуя]$", "", normalized)
    return stemmed


def default_edits(pattern: str) -> int:
    """Допуск правок: четырёхбуквенная основа — точно, длиннее — примерно 1 на 4 буквы."""
    return 0 if len(pattern) <= 4 else len(pattern) // 4


def substring_distance(pattern: str, text: str) -> int:
    """Наименьшее редакционное расстояние от pattern до любого фрагмента text."""
    if not pattern:
        return 0
    previous = [0] * (len(text) + 1)
    for i, pc in enumerate(pattern, 1):
        current = [i] + [0] * len(text)
        for j, tc in enumerate(text, 1):
            current[j] = min(previous[j - 1] + (pc != tc), previous[j] + 1, current[j - 1] + 1)
        previous = current
    return min(previous)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class NoDoctypeTreeBuilder(ET.TreeBuilder):
    def doctype(self, name, public_id, system_id):
        raise ET.ParseError("DOCTYPE/ENTITY в XML не поддерживаются")


def read_lines(path: Path, json_fields: list[str]) -> list[list[str]]:
    """Возвращает строки страницы; у строки может быть несколько вариантов чтения."""
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return [[line] for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            if "lines" not in data:
                raise ValueError("JSON-страница должна содержать массив lines")
            data = data["lines"]
        if not isinstance(data, list):
            raise ValueError("JSON-строки должны быть массивом")
        lines = []
        # Escaped unpaired surrogates in JSON cannot be emitted as UTF-8 text.
        for item in data:
            if isinstance(item, str):
                item.encode("utf-8")
                variants = [item] if item.strip() else []
            elif isinstance(item, dict):
                if not any(key in item for key in json_fields):
                    raise ValueError("в JSON-строке нет указанных текстовых полей")
                variants = []
                for key in dict.fromkeys(json_fields):
                    value = item.get(key)
                    if value is None:
                        continue
                    if not isinstance(value, str):
                        raise ValueError(f"поле JSON-строки {key!r} должно быть текстом")
                    value.encode("utf-8")
                    if value.strip():
                        variants.append(value)
            else:
                raise ValueError("JSON-строка должна быть текстом или объектом")
            if variants:
                lines.append(variants)
        return lines
    if suffix != ".xml":
        raise ValueError("поддерживаются только .xml, .json и .txt")
    parser = ET.XMLParser(target=NoDoctypeTreeBuilder())
    root = ET.fromstring(path.read_bytes(), parser=parser)
    if _local(root.tag) not in {"PcGts", "alto"}:
        raise ValueError("ожидается PAGE XML или ALTO")
    pages = [element for element in root.iter() if _local(element.tag) == "Page"]
    if len(pages) != 1:
        raise ValueError("XML-файл должен описывать ровно одну страницу")
    lines = []
    for element in root.iter():
        name = _local(element.tag)
        if name == "TextLine":
            variants = []
            for child in element:
                if _local(child.tag) == "TextEquiv":
                    for unicode in child:
                        if _local(unicode.tag) == "Unicode" and unicode.text and unicode.text.strip():
                            variants.append(unicode.text)
            if not variants:  # ALTO: TextLine/String@CONTENT
                words = [s.get("CONTENT", "") for s in element if _local(s.tag) in {"String", "HYP"}]
                text = " ".join(w for w in words if w)
                if text.strip():
                    variants.append(text)
            if variants:
                lines.append(list(dict.fromkeys(variants)))
    return lines


def searchable(lines: list[list[str]]) -> list[tuple[str, str]]:
    """Пары (нормализованный текст, исходная строка), включая склейку переноса."""
    out = []
    for variants in lines:
        for raw in variants:
            if raw:
                out.append((normalize(raw), raw))
    for first_line, second_line in zip(lines, lines[1:]):
        for first in first_line:
            if first.rstrip().endswith(HYPHENS):
                for second in second_line:
                    if second:
                        out.append((normalize(first) + normalize(second), f"{first.strip()} | {second.strip()}"))
    return out


@dataclass
class Term:
    label: str
    patterns: list[str]


@dataclass
class PageResult:
    page: str
    source_file: str = ""
    terms: dict[str, tuple[int, str]] = field(default_factory=dict)

    @property
    def score(self) -> tuple[int, int]:
        return (len(self.terms), -sum(d for d, _ in self.terms.values()))


def parse_terms(values: list[str]) -> list[Term]:
    terms = []
    labels = set()
    pattern_groups = set()
    for value in values:
        variants = [v.strip() for v in value.split("|") if v.strip()]
        patterns = sorted({stem(normalize(v)) for v in variants if len(normalize(v)) >= 3})
        if not patterns:
            raise argparse.ArgumentTypeError(f"слишком короткий термин: {value!r}")
        if variants[0] in labels or tuple(patterns) in pattern_groups:
            raise argparse.ArgumentTypeError(f"повтор поискового термина: {value!r}")
        labels.add(variants[0])
        pattern_groups.add(tuple(patterns))
        terms.append(Term(variants[0], patterns))
    return terms


def search_page(page: str, lines: list[list[str]], terms: list[Term], max_edits: int | None) -> PageResult:
    result = PageResult(page)
    texts = searchable(lines)
    for term in terms:
        best = None
        for pattern in term.patterns:
            limit = default_edits(pattern) if max_edits is None else max_edits
            for normalized, raw in texts:
                if len(pattern) > len(normalized) + limit:
                    continue
                if pattern in normalized:
                    distance = 0
                elif limit == 0:
                    continue
                else:
                    distance = substring_distance(pattern, normalized)
                if distance <= limit and (best is None or distance < best[0]):
                    best = (distance, raw)
                if best is not None and best[0] == 0:
                    break
            if best is not None and best[0] == 0:
                break
        if best is not None:
            result.terms[term.label] = best
    return result


def collect(paths: list[Path]) -> tuple[list[Path], list[str]]:
    files = []
    errors = []
    seen = set()
    for path in paths:
        try:
            if path.is_dir():
                candidates = [p for p in sorted(path.iterdir()) if p.is_file() and p.suffix.lower() in SUFFIXES]
            elif path.is_file() and path.suffix.lower() in SUFFIXES:
                candidates = [path]
            else:
                errors.append(f"{path}: файл отсутствует или формат не поддерживается")
                continue
            for candidate in candidates:
                identity = candidate.resolve()
                if identity not in seen:
                    files.append(candidate)
                    seen.add(identity)
        except OSError as exc:
            errors.append(f"{path}: {exc}")
    return files, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path, help="файлы или папки с распознанным текстом страниц")
    parser.add_argument("--term", action="append", required=True,
                        help="поисковый термин; варианты через «|». Повторяйте для нескольких людей или слов записи")
    parser.add_argument("--min-terms", type=int, default=1, help="сколько разных терминов должно совпасть на странице")
    parser.add_argument("--max-edits", type=int, help="допуск правок; по умолчанию 0 для основы до 4 букв, иначе длина // 4")
    parser.add_argument("--json-field", action="append", dest="json_fields",
                        help="поле строки в JSON (можно несколько); по умолчанию text")
    parser.add_argument("--top", type=int, default=50, help="сколько страниц показать")
    parser.add_argument("--json", action="store_true", help="вывести результат в JSON")
    args = parser.parse_args(argv)
    try:
        terms = parse_terms(args.term)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))
    if args.min_terms < 1 or args.min_terms > len(terms):
        parser.error("--min-terms должен быть от 1 до числа разных терминов")
    if args.max_edits is not None and args.max_edits < 0:
        parser.error("--max-edits должен быть неотрицательным")
    if args.top < 0:
        parser.error("--top должен быть неотрицательным")
    files, input_errors = collect(args.paths)
    if not files and not input_errors:
        parser.error("не найдено файлов распознавания (.xml, .json, .txt)")
    results, empty, failed = [], [], []
    for path in files:
        try:
            lines = read_lines(path, args.json_fields or ["text"])
        except (ET.ParseError, ValueError, OSError) as exc:
            failed.append(f"{path}: {exc}")
            continue
        if not lines:
            empty.append(str(path))
            continue
        result = search_page(path.stem, lines, terms, args.max_edits)
        result.source_file = str(path)
        results.append(result)
    hits = [r for r in results if len(r.terms) >= args.min_terms]
    hits.sort(key=lambda r: r.score, reverse=True)
    summary = {
        "pages_total": len(files), "pages_with_text": len(results),
        "files_with_text": [r.source_file for r in results], "input_errors": input_errors,
        "pages_without_text": empty, "pages_failed": failed, "pages_matched": len(hits),
        "matches_shown": min(args.top, len(hits)), "min_terms": args.min_terms,
        "terms": [{"label": t.label, "patterns": t.patterns,
                   "edit_limits": {p: default_edits(p) if args.max_edits is None else args.max_edits
                                   for p in t.patterns}} for t in terms],
    }
    if args.json:
        summary["matches"] = [
            {"page": r.page, "source_file": r.source_file,
             "terms": {k: {"edits": d, "line": raw} for k, (d, raw) in r.terms.items()}}
            for r in hits[: args.top]
        ]
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 1 if failed or input_errors else 0
    print(f"Страниц: {len(files)}, с текстом: {len(results)}, с совпадениями (≥{args.min_terms}): {len(hits)}")
    if empty:
        print(f"Без распознанного текста ({len(empty)}): {', '.join(empty[:20])}{' …' if len(empty) > 20 else ''}")
    for line in input_errors + failed:
        print(f"Не прочитан файл: {line}")
    for r in hits[: args.top]:
        found = "; ".join(f"{k} [{d}] «{raw}»" for k, (d, raw) in r.terms.items())
        print(f"{r.source_file}\t{len(r.terms)}/{len(terms)}\t{found}")
    print("Найденные страницы проверьте по изображению. Отсутствие совпадений не доказывает отсутствия записи.")
    return 1 if failed or input_errors else 0


if __name__ == "__main__":
    sys.exit(main())
