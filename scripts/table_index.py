#!/usr/bin/env python3
"""Search a local CSV/XLSX index and group rows by explicitly selected fields."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from research_common import SourceError, outside_skill

# These bound this in-memory helper, not the coverage of an investigation.
MAX_INPUT_BYTES = 32 * 1024 * 1024
MAX_EXPANDED_BYTES = 128 * 1024 * 1024
MAX_ZIP_MEMBERS = 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 256
MAX_CELLS = 1_000_000


def read_payload(path: Path) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("источник должен быть обычным файлом")
    except BaseException:
        os.close(descriptor)
        raise
    with os.fdopen(descriptor, "rb") as source:
        payload = source.read(MAX_INPUT_BYTES + 1)
    if len(payload) > MAX_INPUT_BYTES:
        raise ValueError("файл превышает лимит локального помощника")
    return payload


def check_row_size(rows: int, columns: int, cells: int):
    if rows > MAX_ROWS or columns > MAX_COLUMNS or cells > MAX_CELLS:
        raise ValueError("таблица превышает лимит строк, столбцов или ячеек")


def check_package(payload: bytes):
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = archive.infolist()
        if (len(members) > MAX_ZIP_MEMBERS
                or sum(item.file_size for item in members) > MAX_EXPANDED_BYTES
                or len({item.filename for item in members}) != len(members)):
            raise ValueError("XLSX превышает лимит распаковки или содержит повторные части")
        if any(item.flag_bits & 1 for item in members):
            raise ValueError("зашифрованный XLSX не поддерживается")


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
            cells = len(header)
            check_row_size(1, len(header), cells)
            while True:
                start = reader.line_num + 1
                try:
                    row = next(reader)
                except StopIteration:
                    break
                cells += len(row)
                check_row_size(len(result) + 2, len(row), cells)
                result.append((start, row))
        return header, result, None
    if suffix != ".xlsx":
        raise ValueError("поддерживаются CSV и XLSX")
    check_package(payload)
    try:
        import openpyxl
        from defusedxml.common import DefusedXmlException
        from openpyxl.utils.exceptions import InvalidFileException
    except ImportError as exc:
        raise ValueError("для XLSX нужны openpyxl и defusedxml; CSV доступен без них") from exc
    if not openpyxl.DEFUSEDXML:
        raise ValueError("для XLSX требуется включённая защита defusedxml")
    book = None
    try:
        book = openpyxl.load_workbook(io.BytesIO(payload), read_only=True,
                                      data_only=False, keep_links=False, keep_vba=False)
        if sheet is None and len(book.sheetnames) != 1:
            raise ValueError("укажите --sheet: в книге несколько листов")
        name = sheet if sheet is not None else book.sheetnames[0]
        if name not in book.sheetnames:
            raise ValueError(f"лист {name!r} не найден")
        if not hasattr(book[name], "iter_rows"):
            raise ValueError("выберите лист таблицы, а не диаграммы")
        # Do not trust a producer's dimensions: they can hide cells or invent
        # millions of empty rows. Bound the actual stream, preserving row gaps.
        book[name].reset_dimensions()
        rows = book[name].iter_rows()
        header_row = next(rows, None)
        if header_row is None:
            raise ValueError("пустой лист")
        check_row_size(1, len(header_row), len(header_row))
        if any(cell.data_type == "f" for cell in header_row):
            raise ValueError("формула в строке 1: сохраните копию со значениями")
        header = [str(cell.value).strip() if cell.value is not None else "" for cell in header_row]
        result = []
        cells = len(header)
        for number, row in enumerate(rows, start=2):
            cells += len(row)
            check_row_size(number, len(row), cells)
            if any(cell.data_type == "f" for cell in row):
                raise ValueError(f"формула в строке {number}: сохраните копию со значениями")
            result.append((number, ["" if cell.value is None else str(cell.value) for cell in row]))
        return header, result, name
    except (ET.ParseError, SyntaxError, DefusedXmlException, InvalidFileException,
            KeyError, TypeError, IndexError, OverflowError, NotImplementedError) as exc:
        raise ValueError("некорректный или неподдерживаемый XLSX") from exc
    finally:
        if book is not None:
            book.close()


def analyze(path: Path, sheet: str | None, name_columns: list[str], variants: list[str], group_columns: list[str], contains: bool = False):
    payload = read_payload(path)
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
        search_values = [normalize(data[column]) for column in name_columns]
        found = [term for term in terms if any(
            (term in value if contains else term == value)
            for value in search_values)]
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


def write_new_result(path: Path, encoded: bytes):
    # Reuse the case-output boundary, but not the replacing writer: results
    # must never replace an existing source, output or dangling symlink.
    outside_skill(path)
    destination = path.expanduser().absolute()
    destination = destination.parent.resolve() / destination.name
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".table-", delete=False) as pending:
            temporary = Path(pending.name)
            pending.write(encoded)
            pending.flush()
            os.fsync(pending.fileno())
        os.link(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


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
            write_new_result(args.out, encoded.encode("utf-8"))
        else:
            print(encoded, end="")
    except (OSError, ValueError, SourceError, csv.Error, zipfile.BadZipFile) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
