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
    return len(pattern) // 4


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


def read_lines(path: Path, json_fields: list[str]) -> list[list[str]]:
    """Возвращает строки страницы; у строки может быть несколько вариантов чтения."""
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return [[line] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("lines", [])
        lines = []
        for item in data:
            if isinstance(item, str):
                variants = [item]
            elif isinstance(item, dict):
                variants = [str(item[key]) for key in json_fields if item.get(key)]
            else:
                variants = []
            if variants:
                lines.append(variants)
        return lines
    raw = path.read_bytes()
    if b"<!DOCTYPE" in raw or b"<!ENTITY" in raw:  # экспорт PAGE/ALTO не нуждается в DTD и сущностях
        raise ET.ParseError("DOCTYPE/ENTITY в XML не поддерживаются")
    root = ET.fromstring(raw)
    lines = []
    for element in root.iter():
        name = _local(element.tag)
        if name == "TextLine":
            text = None
            for child in element:
                if _local(child.tag) == "TextEquiv":
                    for unicode in child:
                        if _local(unicode.tag) == "Unicode" and unicode.text:
                            text = unicode.text
            if text is None:  # ALTO: TextLine/String@CONTENT
                words = [s.get("CONTENT", "") for s in element if _local(s.tag) == "String"]
                text = " ".join(w for w in words if w) or None
            if text:
                lines.append([text])
    return lines


def searchable(lines: list[list[str]]) -> list[tuple[str, str]]:
    """Пары (нормализованный текст, исходная строка), включая склейку переноса."""
    out = []
    count = max((len(v) for v in lines), default=0)
    for k in range(count):
        column = [v[k] if k < len(v) else "" for v in lines]
        for raw in column:
            if raw:
                out.append((normalize(raw), raw))
        for first, second in zip(column, column[1:]):
            if first.rstrip().endswith(HYPHENS) and second:
                out.append((normalize(first) + normalize(second), f"{first.strip()} | {second.strip()}"))
    return out


@dataclass
class Term:
    label: str
    patterns: list[str]


@dataclass
class PageResult:
    page: str
    terms: dict[str, tuple[int, str]] = field(default_factory=dict)
    lines: int = 0

    @property
    def score(self) -> tuple[int, int]:
        return (len(self.terms), -sum(d for d, _ in self.terms.values()))


def parse_terms(values: list[str]) -> list[Term]:
    terms = []
    for value in values:
        variants = [v.strip() for v in value.split("|") if v.strip()]
        patterns = sorted({stem(normalize(v)) for v in variants if len(normalize(v)) >= 3})
        if not patterns:
            raise argparse.ArgumentTypeError(f"слишком короткий термин: {value!r}")
        terms.append(Term(variants[0], patterns))
    return terms


def search_page(page: str, lines: list[list[str]], terms: list[Term], max_edits: int | None) -> PageResult:
    result = PageResult(page, lines=len(lines))
    texts = searchable(lines)
    for term in terms:
        best = None
        for pattern in term.patterns:
            limit = default_edits(pattern) if max_edits is None else max_edits
            for normalized, raw in texts:
                distance = substring_distance(pattern, normalized)
                if distance <= limit and (best is None or distance < best[0]):
                    best = (distance, raw)
        if best is not None:
            result.terms[term.label] = best
    return result


def collect(paths: list[Path]) -> list[Path]:
    files = []
    for path in paths:
        if path.is_dir():
            files.extend(p for p in sorted(path.iterdir()) if p.is_file() and p.suffix.lower() in SUFFIXES)
        elif path.is_file():
            files.append(path)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", type=Path, help="файлы или папки с распознанным текстом страниц")
    parser.add_argument("--term", action="append", required=True,
                        help="поисковый термин; варианты через «|». Повторяйте для нескольких людей или слов записи")
    parser.add_argument("--min-terms", type=int, default=1, help="сколько разных терминов должно совпасть на странице")
    parser.add_argument("--max-edits", type=int, help="допуск правок; по умолчанию длина основы // 4")
    parser.add_argument("--json-field", action="append", dest="json_fields",
                        help="поле строки в JSON (можно несколько); по умолчанию text")
    parser.add_argument("--top", type=int, default=50, help="сколько страниц показать")
    parser.add_argument("--json", action="store_true", help="вывести результат в JSON")
    args = parser.parse_args(argv)
    try:
        terms = parse_terms(args.term)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))
    files = collect(args.paths)
    if not files:
        parser.error("не найдено файлов распознавания (.xml, .json, .txt)")
    results, empty, failed = [], [], []
    for path in files:
        try:
            lines = read_lines(path, args.json_fields or ["text"])
        except (ET.ParseError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            failed.append(f"{path.name}: {exc}")
            continue
        if not lines:
            empty.append(path.name)
            continue
        results.append(search_page(path.stem, lines, terms, args.max_edits))
    hits = [r for r in results if len(r.terms) >= args.min_terms]
    hits.sort(key=lambda r: r.score, reverse=True)
    summary = {
        "pages_total": len(files), "pages_with_text": len(results),
        "pages_without_text": empty, "pages_failed": failed, "pages_matched": len(hits),
        "terms": [{"label": t.label, "patterns": t.patterns} for t in terms],
    }
    if args.json:
        summary["matches"] = [
            {"page": r.page, "terms": {k: {"edits": d, "line": raw} for k, (d, raw) in r.terms.items()}}
            for r in hits[: args.top]
        ]
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print(f"Страниц: {len(files)}, с текстом: {len(results)}, с совпадениями (≥{args.min_terms}): {len(hits)}")
    if empty:
        print(f"Без распознанного текста ({len(empty)}): {', '.join(empty[:20])}{' …' if len(empty) > 20 else ''}")
    for line in failed:
        print(f"Не прочитан файл: {line}")
    for r in hits[: args.top]:
        found = "; ".join(f"{k} [{d}] «{raw}»" for k, (d, raw) in r.terms.items())
        print(f"{r.page}\t{len(r.terms)}/{len(terms)}\t{found}")
    print("Найденные страницы проверьте по изображению. Отсутствие совпадений не доказывает отсутствия записи.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
