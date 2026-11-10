#!/usr/bin/env python3
"""Lint selected GEDCOM UTF-8 export rules and, optionally, case-register links.

This is not a complete schema, calendar, evidence or importer validator.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

try:
    from .audit_evidence import duplicate_ids, read_csv
except ImportError:  # Direct CLI invocation, rather than a package import.
    from audit_evidence import duplicate_ids, read_csv

ESTABLISHED = {"single-source", "corroborated", "strongly-corroborated"}

POINTER_TARGETS = {
    "FAMC": "FAM", "FAMS": "FAM",
    "HUSB": "INDI", "WIFE": "INDI", "CHIL": "INDI", "ASSO": "INDI", "ALIA": "INDI",
    "SUBM": "SUBM", "ANCI": "SUBM", "DESI": "SUBM", "SUBN": "SUBN",
    "SOUR": "SOUR", "REPO": "REPO", "OBJE": "OBJE", "NOTE": "NOTE", "SNOTE": "SNOTE",
}

EVENT_TAGS = {
    "BIRT", "CHR", "BAPM", "DEAT", "BURI", "CREM", "ADOP", "CENS", "EMIG", "IMMI", "NATU",
    "RESI", "OCCU", "RELI", "EDUC", "EVEN", "MARR", "MARB", "ENGA", "DIV", "ANUL",
}

GREG = "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC"
HEB = "TSH|CSH|KSL|TVT|SHV|ADR|ADS|NSN|IYR|SVN|TMZ|AAV|ELL"
FREN = "VEND|BRUM|FRIM|NIVO|PLUV|VENT|GERM|FLOR|PRAI|MESS|THER|FRUC|COMP"
DAY_551 = r"(?:0?[1-9]|[12][0-9]|3[01])"


def _date_551() -> re.Pattern[str]:
    day = DAY_551
    year = r"[0-9]{3,4}"
    dual = year + r"(?:/[0-9]{2})?"
    greg = rf"(?:(?:{day} )?(?:{GREG}) {dual}|{dual}(?: B\.C\.)?)"
    julian = rf"(?:(?:{day} )?(?:{GREG}) {year}|{year}(?: B\.C\.)?)"
    hebrew = rf"(?:(?:{day} )?(?:{HEB}) {year}|{year}(?: B\.C\.)?)"
    french = rf"(?:(?:{day} )?(?:{FREN}) {year}|{year}(?: B\.C\.)?)"
    date = (rf"(?:(?:@#DGREGORIAN@ )?{greg}|@#DJULIAN@ {julian}|@#DHEBREW@ {hebrew}"
            rf"|@#DFRENCH R@ {french}|@#D(?:ROMAN|UNKNOWN)@ [^ ].*?)")
    value = (rf"{date}|FROM {date}(?: TO {date})?|TO {date}|BEF {date}|AFT {date}"
             rf"|BET {date} AND {date}|(?:ABT|CAL|EST) {date}|INT {date} \(.*\)|\(.*\)")
    return re.compile(rf"(?:{value})")


def _date_7() -> re.Pattern[str]:
    ext = r"_[A-Z0-9_]+"
    cal = rf"(?:GREGORIAN|JULIAN|FRENCH_R|HEBREW|{ext})"
    month = rf"(?:{GREG}|{HEB}|{FREN}|{ext})"
    date = rf"(?:{cal} )?(?:(?:[0-9]+ )?{month} )?[0-9]+(?: (?:BCE|{ext}))?"
    value = (rf"|{date}|TO {date}|FROM {date}(?: TO {date})?|BET {date} AND {date}"
             rf"|(?:BEF|AFT) {date}|(?:ABT|CAL|EST) {date}")
    return re.compile(rf"(?:{value})")


DATE_VALUE = {"5.5.1": _date_551(), "7": _date_7()}
DATE_EXACT = {
    "5.5.1": re.compile(rf"{DAY_551} (?:{GREG}) [0-9]+(?:/[0-9]{{2}})?"),
    "7": re.compile(rf"0*{DAY_551} (?:{GREG}) [0-9]+"),
}
LEVEL = {"5.5.1": re.compile(r"0|[1-9][0-9]?"), "7": re.compile(r"0|[1-9][0-9]*")}
XREF = {"5.5.1": re.compile(r"@[A-Za-z0-9][^@]{0,19}@"), "7": re.compile(r"@[A-Z0-9_]+@")}
TAG = {"5.5.1": re.compile(r"[A-Za-z0-9_]{1,31}"), "7": re.compile(r"_[A-Z0-9_]+|[A-Z][A-Z0-9_]*")}
LINE = re.compile(r"(?P<level>[0-9]+) (?:(?P<xref>@[^@ ]+@) )?(?P<tag>[^ ]+)(?: (?P<value>.*))?")
ANY_POINTER = re.compile(r"@[^@# ][^@ ]*@")


class Node:
    def __init__(self, line: int, raw_level: str, xref: str | None, tag: str, value: str | None) -> None:
        self.line, self.raw_level, self.level = line, raw_level, int(raw_level)
        self.xref, self.tag, self.value = xref, tag, value
        self.children: list[Node] = []
        self.parent: Node | None = None

    def first(self, tag: str) -> Node | None:
        return next((child for child in self.children if child.tag == tag), None)

    def values(self, tag: str) -> list[str]:
        return [child.value for child in self.children if child.tag == tag and child.value]


def split_lines(text: str) -> list[tuple[str, int]]:
    """Return (line, terminator length) pairs; GEDCOM allows CR, LF and CRLF."""
    pieces = re.findall(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$", text)
    return [(piece.rstrip("\r\n"), len(piece) - len(piece.rstrip("\r\n"))) for piece in pieces]


def detect_version(records: list[Node]) -> str | None:
    head = records[0] if records and records[0].tag == "HEAD" else None
    gedc = head.first("GEDC") if head else None
    vers = gedc.first("VERS") if gedc else None
    if vers is None or not vers.value:
        return None
    if vers.value == "5.5.1":
        return "5.5.1"
    if re.fullmatch(r"7\.[0-9]+(?:\.[0-9]+)?", vers.value):
        return "7"
    return vers.value


def parse(text: str, errors: list[str], warnings: list[str]) -> list[Node]:
    records: list[Node] = []
    stack: list[Node] = []
    for number, (line, _) in enumerate(split_lines(text), 1):
        if not line.strip():
            warnings.append(f"строка {number}: пустая строка")
            continue
        if line != line.lstrip():
            warnings.append(f"строка {number}: пробел или табуляция в начале строки")
            line = line.lstrip()
        match = LINE.fullmatch(line)
        if not match:
            errors.append(f"строка {number}: не разбирается как строка GEDCOM: {line[:60]!r}")
            continue
        try:
            node = Node(number, match["level"], match["xref"], match["tag"], match["value"])
        except ValueError:
            errors.append(f"строка {number}: номер уровня не может быть разобран")
            continue
        level = node.level
        while stack and stack[-1].level >= level:
            stack.pop()
        if level == 0:
            records.append(node)
        elif not stack:
            errors.append(f"строка {number}: уровень {level} без записи уровня 0")
            continue
        else:
            if level > stack[-1].level + 1:
                errors.append(f"строка {number}: уровень {level} после уровня {stack[-1].level}")
            node.parent = stack[-1]
            stack[-1].children.append(node)
        stack.append(node)
    return records


def walk(nodes: list[Node]):
    pending = list(reversed(nodes))
    while pending:
        node = pending.pop()
        yield node
        pending.extend(reversed(node.children))


def check_syntax(nodes: list[Node], lines: list[tuple[str, int]], version: str | None,
                 errors: list[str], warnings: list[str]) -> None:
    if version not in DATE_VALUE:
        return
    unchecked_dates: list[str] = []
    for node in nodes:
        where = f"строка {node.line}"
        if not LEVEL[version].fullmatch(node.raw_level):
            errors.append(f"{where}: недопустимый номер уровня {node.raw_level}")
        if not TAG[version].fullmatch(node.tag):
            errors.append(f"{where}: недопустимый тег {node.tag!r}")
        if node.xref and not XREF[version].fullmatch(node.xref):
            errors.append(f"{where}: недопустимый XREF {node.xref}")
        if version == "7" and node.xref == "@VOID@":
            errors.append(f"{where}: @VOID@ допустим как указатель, но не как XREF записи")
        if node.xref and node.level:
            errors.append(f"{where}: XREF {node.xref} допускается только у записи уровня 0")
        value = node.value or ""
        pointer = bool(value) and XREF[version].fullmatch(value) is not None
        if node.tag == "DATE":
            parent = node.parent
            event_date = (parent is not None and parent.tag in EVENT_TAGS
                          and parent.parent is not None and parent.parent.tag in {"INDI", "FAM"})
            exact_date = parent is not None and (parent.tag, parent.level) in {("HEAD", 0), ("CHAN", 1)}
            if exact_date:
                if not DATE_EXACT[version].fullmatch(value):
                    errors.append(f"{where}: {parent.tag}.DATE требует точную дату GEDCOM {version} "
                                  "в форме дня, месяца и года")
            elif not event_date:
                unchecked_dates.append(f"{node.line} ({parent.tag if parent else 'уровень 0'})")
            elif not DATE_VALUE[version].fullmatch(value):
                hint = "; текстовую дату заключите в скобки или используйте ABT, BEF, AFT, BET" if version == "5.5.1" else ""
                errors.append(f"{where}: дата {value!r} не соответствует проверяемому формату GEDCOM {version}{hint}")
        if version == "5.5.1" and not pointer and "@" in re.sub(r"@@|@#[^@]*@", "", value):
            warnings.append(f"{where}: одиночный @ в тексте; в 5.5.1 его удваивают (@@)")
        if version == "7" and value.startswith("@") and not pointer and not value.startswith("@@"):
            errors.append(f"{where}: значение начинается с @; в GEDCOM 7 начальный @ удваивают")
        if version == "7" and node.tag == "CONC":
            errors.append(f"{where}: CONC нет в GEDCOM 7; длинный текст пишут одной строкой")
        if version == "7" and node.tag == "NOTE" and (node.level == 0 or pointer):
            errors.append(f"{where}: в GEDCOM 7 общая заметка и ссылка на неё используют SNOTE, не NOTE")
        if version == "5.5.1" and node.tag == "SNOTE":
            errors.append(f"{where}: SNOTE относится к GEDCOM 7, не к 5.5.1")
    if unchecked_dates:
        locations = ", ".join(unchecked_dates[:20])
        more = f" и ещё {len(unchecked_dates) - 20}" if len(unchecked_dates) > 20 else ""
        warnings.append(f"Сверьте по спецификации DATE вне поддерживаемых контекстов. Строки {locations}{more}.")
    if version == "5.5.1":
        for number, (line, term) in enumerate(lines, 1):
            if len(line) + term > 255:
                errors.append(f"строка {number}: {len(line) + term} символов, в 5.5.1 не больше 255")
        values = {node.line: node.value or "" for node in nodes}
        for node in nodes:
            if node.tag == "CONC" and (values.get(node.line, "").startswith(" ")
                                        or values.get(node.line - 1, "").endswith(" ")):
                warnings.append(f"строка {node.line}: CONC разрывает текст на пробеле; часть программ его теряет")


def check_header(records: list[Node], version: str | None, text: str,
                 errors: list[str], warnings: list[str]) -> None:
    if not records:
        errors.append("файл не содержит записей")
        return
    if records[0].tag != "HEAD":
        errors.append(f"строка {records[0].line}: первая запись должна быть HEAD")
    if records[-1].tag != "TRLR":
        errors.append(f"строка {records[-1].line}: последняя запись должна быть TRLR")
    for tag in ("HEAD", "TRLR"):
        if sum(record.tag == tag for record in records) != 1:
            errors.append(f"в файле должна быть ровно одна запись {tag}")
    for record in records:
        if record.tag in ("HEAD", "TRLR") and (record.xref or record.value is not None):
            errors.append(f"строка {record.line}: {record.tag} не имеет XREF или значения")
        if record.tag == "TRLR" and record.children:
            errors.append(f"строка {record.line}: TRLR не имеет подструктур")
    for record in records[:-1]:
        if record.tag == "TRLR":
            errors.append(f"строка {record.line}: TRLR не в конце файла")
    if version is None:
        errors.append("в HEAD нет GEDC.VERS: версия файла не указана")
        return
    if version not in DATE_VALUE:
        errors.append(f"версия {version!r} не поддерживается проверкой; проверены только общие правила")
        return
    head = records[0] if records[0].tag == "HEAD" else None
    if version == "5.5.1" and head is not None:
        gedc = head.first("GEDC")
        for tag in ("SOUR", "SUBM", "CHAR"):
            if head.first(tag) is None:
                errors.append(f"в HEAD нет обязательного {tag} для 5.5.1")
        form = gedc.first("FORM") if gedc else None
        if form is None or form.value != "LINEAGE-LINKED":
            errors.append("в HEAD.GEDC нет FORM LINEAGE-LINKED, обязательного для 5.5.1")
        char = head.first("CHAR")
        if char is not None and char.value != "UTF-8" and not text.isascii():
            errors.append(f"HEAD.CHAR {char.value!r}, а файл содержит символы вне ASCII; укажите UTF-8")


def unasserted_famc(link: Node) -> bool:
    status = link.first("STAT")
    return bool(status and (status.value or "").upper() in {"CHALLENGED", "DISPROVEN"})


def check_links(records: list[Node], version: str | None, errors: list[str]) -> None:
    pointer_syntax = XREF.get(version or "", ANY_POINTER)
    defined: dict[str, Node] = {}
    for record in records:
        if record.xref:
            if record.xref in defined:
                errors.append(f"строка {record.line}: XREF {record.xref} уже объявлен в строке {defined[record.xref].line}")
            else:
                defined[record.xref] = record
    for node in walk(records):
        value = node.value or ""
        if not node.level or not pointer_syntax.fullmatch(value):
            continue
        if version == "7" and value == "@VOID@":
            continue
        target = defined.get(value)
        if target is None:
            errors.append(f"строка {node.line}: ссылка {node.tag} {value} не найдена")
            continue
        expected = POINTER_TARGETS.get(node.tag)
        if version == "7" and node.tag == "NOTE":
            expected = None  # Diagnosed as a version error by check_syntax.
        if expected and target.tag != expected:
            errors.append(f"строка {node.line}: {node.tag} {value} указывает на {target.tag}, ожидается {expected}")
    for record in records:
        if record.tag == "FAM" and record.xref:
            for role in ("HUSB", "WIFE", "CHIL"):
                back = "FAMC" if role == "CHIL" else "FAMS"
                for person in record.values(role):
                    target = defined.get(person)
                    if target is not None and target.tag == "INDI" and record.xref not in target.values(back):
                        errors.append(f"{record.xref} {role} {person}: у {person} нет {back} {record.xref}")
        if record.tag == "INDI" and record.xref:
            for back, roles in (("FAMS", ("HUSB", "WIFE")), ("FAMC", ("CHIL",))):
                for link in record.children:
                    if link.tag != back or not link.value or (back == "FAMC" and unasserted_famc(link)):
                        continue
                    family = link.value
                    target = defined.get(family)
                    if target is not None and target.tag == "FAM" and not any(
                            record.xref in target.values(role) for role in roles):
                        errors.append(f"{record.xref} {back} {family}: в {family} нет {record.xref} как {'/'.join(roles)}")


def read_register(path: Path, required: set[str], errors: list[str]) -> list[dict[str, str]]:
    try:
        rows, file_errors = read_csv(path, required)
    except (UnicodeError, csv.Error) as exc:
        errors.append(f"{path.name}: ошибка чтения CSV: {exc}")
        return []
    errors.extend(file_errors)
    return rows


def check_registers(records: list[Node], case_dir: Path, errors: list[str], warnings: list[str]) -> None:
    register_errors: list[str] = []
    person_rows = read_register(case_dir / "person-register.csv", {"person_id"}, register_errors)
    relations = read_register(case_dir / "relationship-register.csv",
                              {"relationship_id", "person_a_id", "relationship_type", "person_b_id", "status"},
                              register_errors)
    for name, rows_, key in (("person-register.csv", person_rows, "person_id"),
                             ("relationship-register.csv", relations, "relationship_id")):
        duplicates = duplicate_ids(rows_, key)
        if duplicates:
            register_errors.append(f"{name}: дублирующиеся {key}: {', '.join(duplicates)}")
    errors.extend(register_errors)
    if register_errors:
        return
    people = {row["person_id"]: row for row in person_rows if row.get("person_id")}
    indi_by_xref = {record.xref: record for record in records if record.tag == "INDI" and record.xref}
    person_of: dict[str, str] = {}
    unmatched = []
    for record in records:
        if record.tag != "INDI" or not record.xref:
            continue
        ids = sorted({value for value in record.values("REFN") if value in people})
        if len(ids) > 1:
            errors.append(f"{record.xref}: несколько REFN соответствуют разным person_id: {', '.join(ids)}")
            continue
        if not ids:
            unmatched.append(record.xref)
            continue
        if ids[0] in person_of.values():
            errors.append(f"{record.xref}: person_id {ids[0]} уже связан с другой INDI")
        person_of[record.xref] = ids[0]
    if not person_of:
        warnings.append("ни у одной INDI нет REFN с person_id из реестра; сверка с реестрами пропущена")
        return
    if unmatched:
        more = f" и ещё {len(unmatched) - 20}" if len(unmatched) > 20 else ""
        warnings.append(f"INDI без REFN с person_id из реестра, не сверены: {', '.join(unmatched[:20])}{more}")

    exported = set()
    for record in records:
        if record.tag != "FAM":
            continue
        parents = [person_of[x] for x in record.values("HUSB") + record.values("WIFE") if x in person_of]
        if len(parents) == 2:
            pair = set(parents)
            pair_rows = [r for r in relations if {r["person_a_id"], r["person_b_id"]} == pair]
            found = [r for r in pair_rows if r["relationship_type"] in {"spouse-of", "spouse"}]
            if not found:
                warning = (f"{record.xref}: для пары {parents[0]} и {parents[1]} нет строки "
                           "spouse-of или spouse в relationship-register.csv.")
                if pair_rows:
                    other_rows = ", ".join(f"{r['relationship_id'] or 'без ID'} ({r['relationship_type'] or 'без типа'})"
                                           for r in pair_rows)
                    warning += f" Строки других типов для этих лиц — {other_rows}."
                warnings.append(warning)
            elif not any(r["status"] in ESTABLISHED for r in found):
                errors.append(f"{record.xref}: пара {parents[0]} и {parents[1]} в реестре со статусом "
                              f"{', '.join(sorted({r['status'] for r in found}))}, ниже single-source")
        for child in record.values("CHIL"):
            if child not in person_of:
                continue
            child_record = indi_by_xref[child]
            links = [link for link in child_record.children
                     if link.tag == "FAMC" and link.value == record.xref]
            adoption = any(event.tag == "ADOP" and record.xref in event.values("FAMC")
                           for event in child_record.children)
            other_pedigree = any((detail.value or "").casefold() != "birth"
                                 for link in links for detail in link.children if detail.tag == "PEDI")
            qualified = adoption or other_pedigree or any(unasserted_famc(link) for link in links)
            if qualified:
                warnings.append(f"{record.xref} CHIL {child}: PEDI, спорный STAT или ADOP требуют проверки ролей. "
                                "Сверка родительских связей этого ребёнка пропущена. См. gedcom.md.")
                exported.update((parent, person_of[child]) for parent in parents)
                continue
            for parent in parents:
                exported.add((parent, person_of[child]))
                found = [r for r in relations if r["relationship_type"] == "parent-of"
                         and r["person_a_id"] == parent and r["person_b_id"] == person_of[child]]
                if not found:
                    errors.append(f"{record.xref}: {parent} parent-of {person_of[child]} нет в relationship-register.csv")
                elif not any(r["status"] in ESTABLISHED for r in found):
                    errors.append(f"{record.xref}: {parent} parent-of {person_of[child]} в реестре со статусом "
                                  f"{', '.join(sorted({r['status'] for r in found}))}, ниже single-source")
    in_tree = set(person_of.values())
    for r in relations:
        key = (r["person_a_id"], r["person_b_id"])
        if (r["relationship_type"] == "parent-of" and r["status"] in ESTABLISHED
                and set(key) <= in_tree and key not in exported):
            warnings.append(f"{r['relationship_id']}: {key[0]} parent-of {key[1]} ({r['status']}) не перенесена в древо")
    for xref, person_id in person_of.items():
        status = (people[person_id].get("living_status") or "").strip()
        if not status.lower().startswith("deceased"):
            warnings.append(f"{xref} ({person_id}): living_status {status or 'не указан'}; "
                            "перед передачей файла см. privacy-and-safety.md")
    for record in records:
        if record.tag in ("INDI", "FAM"):
            for event in record.children:
                states_fact = event.first("DATE") is not None or event.first("PLAC") is not None
                if event.tag in EVENT_TAGS and states_fact and event.first("SOUR") is None:
                    warnings.append(f"строка {event.line}: {record.xref} {event.tag} с датой или местом без SOUR")


def check_file(path: Path, case_dir: Path | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return {"file": str(path), "version": None, "counts": {}, "warnings": [],
                "errors": [f"не удалось прочитать файл: {exc}"]}
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {"file": str(path), "version": None, "counts": {}, "warnings": [],
                "errors": [f"файл не в UTF-8 (байт {exc.start}); проверка читает только UTF-8"]}
    if text and not text.endswith(("\n", "\r")):
        errors.append("после последней строки (0 TRLR) нет перевода строки")
    lines = split_lines(text)
    records = parse(text, errors, warnings)
    version = detect_version(records)
    nodes = list(walk(records))
    check_header(records, version, text, errors, warnings)
    check_syntax(nodes, lines, version, errors, warnings)
    check_links(records, version, errors)
    if case_dir is not None:
        check_registers(records, case_dir, errors, warnings)
    counts = {tag: sum(1 for r in records if r.tag == tag) for tag in ("INDI", "FAM", "SOUR")}
    return {"file": str(path), "version": version, "counts": counts, "errors": errors, "warnings": warnings}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет отдельные правила GEDCOM 5.5.1/7 в UTF-8 и, по желанию, связи по реестрам; не полная валидация.")
    parser.add_argument("path", help="Путь к файлу .ged")
    parser.add_argument("--case-dir", help="Директория дела: сверить людей (REFN = person_id) и связи с реестрами")
    parser.add_argument("--json", action="store_true", help="Вывести JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path).expanduser().resolve()
    if not path.is_file():
        print(f"Ошибка: файл не найден: {path}", file=sys.stderr)
        return 2
    case_dir = None
    if args.case_dir:
        case_dir = Path(args.case_dir).expanduser().resolve()
        for name in ("person-register.csv", "relationship-register.csv"):
            if not (case_dir / name).is_file():
                print(f"Ошибка: в деле нет {name}: {case_dir}", file=sys.stderr)
                return 2
    result = check_file(path, case_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        counts = result["counts"]
        print(f"Проверен файл: {result['file']}")
        print(f"Версия: {result['version'] or 'не указана'}; INDI {counts.get('INDI', 0)}, "
              f"FAM {counts.get('FAM', 0)}, SOUR {counts.get('SOUR', 0)}")
        for label, items in (("ОШИБКИ", result["errors"]), ("ПРЕДУПРЕЖДЕНИЯ", result["warnings"])):
            if items:
                print(f"\n{label}:")
                for item in items:
                    print(f"- {item}")
        if not result["errors"] and not result["warnings"]:
            print("Ошибок и предупреждений не найдено.")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from research_common import configure_utf8_stdio

    configure_utf8_stdio()
    raise SystemExit(main())
