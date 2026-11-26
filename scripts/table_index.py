#!/usr/bin/env python3
"""Search a local CSV/XLSX index and group rows by explicitly selected fields."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def read_table(path: Path, payload: bytes, sheet: str | None):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        if sheet is not None:
            raise ValueError("--sheet применяется только к XLSX")
        with io.StringIO(payload.decode("utf-8-sig"), newline="") as source:
            reader = csv.reader(source, strict=True)
            header = next(reader, None)
            if header is None:
                raise ValueError("пустой CSV")
            result = []
            while True:
                start = reader.line_num + 1
                try:
                    row = next(reader)
                except StopIteration:
                    break
                result.append((start, row))
        return header, result, None
    if suffix != ".xlsx":
        raise ValueError("поддерживаются CSV и XLSX")
    try:
        import openpyxl
    except ImportError as exc:
        raise ValueError("для XLSX установите openpyxl; CSV доступен без него") from exc
    book = openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=False)
    try:
        if sheet is None and len(book.sheetnames) != 1:
            raise ValueError("укажите --sheet: в книге несколько листов")
        name = sheet if sheet is not None else book.sheetnames[0]
        if name not in book.sheetnames:
            raise ValueError(f"лист {name!r} не найден")
        rows = book[name].iter_rows()
        header_row = next(rows, None)
        if header_row is None:
            raise ValueError("пустой лист")
        header = [str(cell.value).strip() if cell.value is not None else "" for cell in header_row]
        result = []
        for number, row in enumerate(rows, start=2):
            if any(cell.data_type == "f" for cell in row):
                raise ValueError(f"формула в строке {number}: сохраните копию со значениями")
            result.append((number, ["" if cell.value is None else str(cell.value) for cell in row]))
        return header, result, name
    finally:
        book.close()


def analyze(path: Path, sheet: str | None, name_columns: list[str], variants: list[str], group_columns: list[str], contains: bool = False):
    payload = path.read_bytes()
    header, source_rows, sheet = read_table(path, payload, sheet)
    header = [name.strip() for name in header]
    if any(not name for name in header) or len(set(header)) != len(header):
        raise ValueError("заголовки должны быть непустыми и уникальными")
    columns = name_columns + group_columns
    if len(set(name_columns)) != len(name_columns) or len(set(group_columns)) != len(group_columns):
        raise ValueError("столбец повторяется")
    missing = [name for name in columns if name not in header]
    if missing:
        raise ValueError("нет столбцов: " + ", ".join(missing))
    terms = list(dict.fromkeys(normalize(v) for v in variants))
    if not terms or "" in terms:
        raise ValueError("укажите непустые варианты поиска")
    rows = []
    for number, values in source_rows:
        if not any(str(value).strip() for value in values):
            continue
        if len(values) > len(header):
            raise ValueError(f"строка {number}: полей больше, чем заголовков")
        values += [""] * (len(header) - len(values))
        data = dict(zip(header, values))
        found = [term for term in terms if any(
            (term in normalize(data[column]) if contains else term == normalize(data[column]))
            for column in name_columns)]
        key = tuple(normalize(data[column]) for column in group_columns)
        rows.append({"row": number, "values": data, "matched_variants": found, "key": key})
    buckets = defaultdict(list)
    ungrouped = []
    for row in rows:
        key = row.pop("key")
        if group_columns and all(key):
            buckets[key].append(row)
        elif row["matched_variants"]:
            ungrouped.append(row)
    groups = [{"key": dict(zip(group_columns, key)), "rows": entries}
              for key, entries in buckets.items() if any(r["matched_variants"] for r in entries)]
    return {
        "source": {"file": str(path), "sha256": hashlib.sha256(payload).hexdigest(), "sheet": sheet},
        "search": {"columns": name_columns, "variants": variants, "mode": "contains" if contains else "exact", "group_by": group_columns},
        "rows_examined": len(rows), "groups": groups, "ungrouped_matches": ungrouped,
        "notice": "Группы — совпадения полей, а не установленные личности или родство. Проверьте исходные записи и охват.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--sheet", help="имя листа XLSX")
    parser.add_argument("--name-column", action="append", required=True, help="столбец поиска; можно повторить")
    parser.add_argument("--variant", action="append", required=True, help="вариант написания; можно повторить")
    parser.add_argument("--group-by", action="append", default=[], help="поле группировки; можно повторить")
    parser.add_argument("--contains", action="store_true", help="искать подстроку вместо полного совпадения поля")
    parser.add_argument("--out", type=Path, help="новый JSON-файл; существующие файлы не перезаписываются")
    args = parser.parse_args(argv)
    try:
        result = analyze(args.file, args.sheet, args.name_column, args.variant, args.group_by, args.contains)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            with args.out.open("x", encoding="utf-8") as output:
                output.write(encoded)
        else:
            print(encoded, end="")
    except (OSError, ValueError, csv.Error, zipfile.BadZipFile) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
