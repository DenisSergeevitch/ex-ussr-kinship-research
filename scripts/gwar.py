#!/usr/bin/env python3
"""Find WWI source records and locality clusters without inferring kinship."""

from __future__ import annotations

import argparse
import difflib
import re
import ssl
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # `python -I` omits the script folder

from research_common import (configure_utf8_stdio, SourceClient, SourceError, fingerprint, outside_skill, output_json,
                             read_json, save_json, state_lock, timestamp)

BASE = "https://gwar.mil.ru"
KINDS = {"reports": "chelovek_donesenie", "hospitals": "chelovek_gospital", "awards": "chelovek_nagrazhdenie", "pows": "chelovek_plen"}


def source_client():
    # Extra certificates apply only to this client, never to the system trust store.
    context = ssl.create_default_context()
    for name in ("russian_trusted_root_ca.pem", "russian_trusted_sub_ca.pem"):
        path = Path(__file__).resolve().parent / "ca" / name
        if not path.is_file():
            raise SourceError("Отсутствует сертификат GWAR из scripts/ca; проверка TLS не отключается.")
        context.load_verify_locations(cafile=str(path))
    return SourceClient(BASE, context=context, referer=BASE + "/heroes/")


def query_body(fields, offset, size, entities, builder="Heroes"):
    return {"indices": ["gwar"], "entities": entities, "queryFields": fields,
            "filterFields": {}, "facetField": None, "from": offset, "size": size, "builderType": builder}


def fetch_page(client, fields, offset, size, entities, builder="Heroes"):
    data = client.request("/gt_data/?builder=" + builder, query_body(fields, offset, size, entities, builder))
    if isinstance(data, dict) and "response" in data:
        data = data["response"]
    box = data.get("hits") if isinstance(data, dict) else None
    if not isinstance(box, dict) or not isinstance(box.get("hits"), list):
        raise SourceError("GWAR: неожиданный формат выдачи.")
    total = box.get("total")
    if isinstance(total, dict):
        if total.get("relation", "eq") != "eq":
            raise SourceError("GWAR не сообщил точное число результатов; полнота неизвестна.")
        total = total.get("value")
    if type(total) is not int or total < 0:
        raise SourceError("GWAR: отсутствует точный счётчик записей.")
    for hit in box["hits"]:
        if not isinstance(hit, dict) or not hit.get("_id") or not isinstance(hit.get("_source"), dict):
            raise SourceError("GWAR: карточка без ID или исходных полей.")
    return box["hits"], total


def hit_key(hit):
    return "|".join(str(hit.get(field, "")) for field in ("_index", "_type", "_id"))


def collect(client, fields, entities, limit, checkpoint=None):
    identity = {"source": "gwar", "query": fields, "entities": entities}
    state = {**identity, "fingerprint": fingerprint(identity), "total": None, "hits": [],
             "next_offset": 0, "started_at": timestamp(), "captured_at": timestamp(), "coverage": {"complete": False}}
    if checkpoint and Path(checkpoint).exists():
        state = read_json(checkpoint)
        if state.get("fingerprint") != fingerprint(identity):
            raise SourceError("Сохранённая выдача GWAR относится к другому запросу.")
        if not isinstance(state.get("hits"), list) or type(state.get("next_offset")) is not int:
            raise SourceError("Некорректное состояние выдачи GWAR.")
        if limit < len(state["hits"]):
            raise SourceError("Лимит меньше уже сохранённой выдачи; выберите другой файл или прежний лимит.")
    hits = {hit_key(hit): hit for hit in state["hits"]}
    if len(hits) != len(state["hits"]):
        raise SourceError("В контрольной точке GWAR есть повторные ID.")
    blocked, incomplete_reason = None, ""
    try:
        if state["total"] is None or state["next_offset"] < state["total"]:
            client.request("/heroes/", as_json=False)
        while len(hits) < limit and (state["total"] is None or state["next_offset"] < state["total"]):
            requested_size = min(1000, limit - len(hits))
            page, total = fetch_page(client, fields, state["next_offset"], requested_size, entities)
            if len(page) > requested_size:
                raise SourceError("GWAR вернул больше запрошенного объёма; проверьте формат API.")
            if state["total"] is not None and state["total"] != total:
                raise SourceError("Число результатов GWAR изменилось; проверьте выдачу новым запросом.")
            state["total"] = total
            state["captured_at"] = timestamp()
            previous_count = len(hits)
            for hit in page:
                key = hit_key(hit)
                if key in hits and hits[key] != hit:
                    raise SourceError("Содержимое карточки GWAR изменилось во время получения выдачи.")
                hits[key] = hit
            state["next_offset"] += len(page)
            state["hits"] = list(hits.values())
            if not page or len(hits) == previous_count:
                if len(hits) < total:
                    incomplete_reason = "empty-or-repeated-page-before-total"
                break
            if checkpoint:
                save_json(checkpoint, state)
    except SourceError as exc:
        blocked = {"status": exc.status, "message": str(exc)}
    finally:
        complete = state["total"] is not None and len(hits) == state["total"] and not blocked and not incomplete_reason
        state.update({"hits": list(hits.values()), "updated_at": timestamp(), "blocked": blocked,
                      "coverage": {"complete": complete, "retrieved_records": len(hits), "reported_total": state["total"],
                                   "limit": limit, "reason": incomplete_reason or (("limit-reached" if len(hits) >= limit else "source-window-incomplete") if not complete and not blocked else ""),
                                   "scope": "returned-source-records-not-population-census"}})
        if checkpoint:
            save_json(checkpoint, state)
    return state


def parse_scan(xml):
    xml = str(xml or "")
    image = re.search(r"[A-Za-z0-9_\-/]+\.(?:jpe?g|png|tiff?)", xml, flags=re.IGNORECASE)
    path = image.group(0) if image else None
    zones = []
    try:
        root = ET.fromstring(xml)
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] == "s":
                zones.append(dict(element.attrib))
    except ET.ParseError:
        # Some source payloads are XML fragments rather than a full document.
        for match in re.finditer(r"<s\s+([^>]+?)/?>", xml):
            zones.append(dict(re.findall(r'([\w:]+)\s*=\s*"([^"]*)"', match.group(1))))
    return {"image_path": path, "image_url": BASE + "/cdn/imagesfww/" + path.lstrip("/") if path else None,
            "zones": zones, "raw": xml}


def pages(client, page_ids):
    client.request("/heroes/", as_json=False)
    result = []
    for page_id in dict.fromkeys(page_ids):
        hits, total = fetch_page(client, {"linkedPages": [int(page_id)]}, 0, 100, ["stranitsa"], "HeroesStranitsa")
        result.append({"pages_id": page_id, "total": total, "complete": len(hits) == total,
                       "records": [{"id": hit["_id"], "source": hit["_source"],
                                    **parse_scan(hit["_source"].get("obraz_s_oblastyami", ""))} for hit in hits]})
    return {"source": "gwar-pages", "captured_at": timestamp(), "pages": result,
            "coverage": {"complete": all(item["complete"] for item in result), "scope": "selected-pages"}}


PLACE_UNITS = (("gubernia", re.compile(r"\b(?:губ(?:ерния)?|обл(?:асть)?)\.?$")),
               ("uezd", re.compile(r"\b(?:уезд|у)\.?$")),
               ("volost", re.compile(r"\bвол(?:ость)?\.?$")))
SETTLEMENT_TYPE = re.compile(r"^(?:селение|село|деревня|дер|хутор|местечко|колония|слобода|н\.\s?п|с|д|х|м|к|сл)\.?\s+")


def place_parts(source):
    """Split the card's place into units and the settlement, keeping each string as written."""
    parts = {unit: str(source.get("birth_place_" + unit) or "").strip() for unit, _ in PLACE_UNITS}
    rest = []
    for token in (item.strip() for item in str(source.get("birth_place") or "").split(",")):
        if not token:
            continue
        unit = next((name for name, pattern in PLACE_UNITS if pattern.search(token.lower())), None)
        if unit and not parts[unit]:
            parts[unit] = token
        elif not unit:
            rest.append(token)
    parts["settlement"] = ", ".join(rest)
    return parts


def name_key(name):
    return "".join(char for char in unicodedata.normalize("NFC", name).lower().replace("ё", "е")
                   if char.isalpha())


def place_key(name):
    name = SETTLEMENT_TYPE.sub("", name.lower().replace("ё", "е").strip())
    return re.sub(r"[^a-zа-яіїєґăâîșțş]", "", name)


def similarity(left, right, key=place_key, vowels="аеиоуыэюяіїєйăâîьъ"):
    left, right = key(left), key(right)
    if not left or not right:
        return 0.0
    skeleton = ["".join(char for char in value if char not in vowels) for value in (left, right)]
    scores = [difflib.SequenceMatcher(None, left, right).ratio()]
    if all(skeleton):
        scores.append(difflib.SequenceMatcher(None, *skeleton).ratio())
    return round(max(scores), 2)


def saved_cards(states):
    """Merge cards of saved search/volost files by full key; refuse conflicting snapshots."""
    cards, inputs = {}, []
    for name, state in states:
        if (not isinstance(state, dict) or state.get("source", "gwar") != "gwar"
                or not isinstance(state.get("hits"), list)):
            raise SourceError(f"{name}: это не выдача gwar.py search/volost.")
        coverage = state.get("coverage")
        if not isinstance(coverage, dict):
            raise SourceError(f"{name}: отсутствуют сведения о полноте выдачи GWAR.")
        inputs.append({"file": name, "query": state.get("query"),
                       "complete": coverage.get("complete") is True})
        for hit in state["hits"]:
            if (not isinstance(hit, dict) or not hit.get("_id")
                    or not isinstance(hit.get("_source"), dict)):
                raise SourceError(f"{name}: карточка GWAR без ID или исходных полей.")
            key = hit_key(hit)
            if key in cards and cards[key]["_source"] != hit["_source"]:
                raise SourceError(f"{name}: версии одной карточки GWAR различаются; сравните исходные файлы.")
            cards.setdefault(key, hit)
    if not inputs:
        raise SourceError("Укажите хотя бы одну сохранённую выдачу GWAR.")
    return cards, inputs


def places(states, target=None):
    """Group settlement spellings of saved cards by gubernia, uezd and volost; no network access."""
    cards, inputs = saved_cards(states)
    groups = {}
    for hit in cards.values():
        parts = place_parts(hit.get("_source") or {})
        group = groups.setdefault((parts["gubernia"], parts["uezd"], parts["volost"]), {})
        entry = group.setdefault(parts["settlement"], {"as_written": parts["settlement"], "cards": 0, "card_ids": [], "card_keys": []})
        entry["cards"] += 1
        entry["card_ids"].append(hit["_id"])
        entry["card_keys"].append(hit_key(hit))
    result = []
    for (gubernia, uezd, volost), settlements in groups.items():
        items = list(settlements.values())
        for item in items:
            if target:
                item["similarity"] = similarity(target, item["as_written"])
        items.sort(key=lambda item: (-item.get("similarity", 0), -item["cards"], item["as_written"]))
        result.append({"gubernia": gubernia, "uezd": uezd, "volost": volost, "settlements": items})
    result.sort(key=lambda group: (-max((item.get("similarity", 0) for item in group["settlements"]), default=0),
                                   group["gubernia"], group["uezd"], group["volost"]))
    return {"source": "gwar-places", "captured_at": timestamp(), "target": target, "inputs": inputs,
            "cards": len(cards), "groups": result,
            "coverage": {"complete": all(item["complete"] for item in inputs),
                         "scope": "spellings-in-saved-cards-not-settlement-list"}}


def surnames(states, target=None):
    """Group surname spellings of saved cards and rank them against a target; no network access."""
    cards, inputs = saved_cards(states)
    spellings = {}
    fields = ("first_name", "middle_name", "birth_place", "birth_place_volost",
              "birth_place_uezd", "birth_place_gubernia")
    for key, hit in cards.items():
        source = hit["_source"]
        written = str(source.get("last_name") or "")
        card = {"card_id": hit["_id"], "card_key": key}
        card.update({field: source[field] for field in fields if source.get(field)})
        spellings.setdefault(written if written.strip() else "", []).append(card)
    items = [{"as_written": written, "cards": len(rows), "card_context": rows}
             for written, rows in spellings.items()]
    target_key = name_key(target) if target else ""
    if target_key:
        for item in items:
            item["similarity"] = similarity(target, item["as_written"], key=name_key,
                                            vowels="аеиоуыэюяіїєйăâîьъaeiouy")
    items.sort(key=lambda item: (not item["as_written"], -item.get("similarity", 0),
                                 bool(target_key) and name_key(item["as_written"]) != target_key,
                                 -item["cards"], item["as_written"]))
    return {"source": "gwar-surnames", "captured_at": timestamp(), "target": target, "inputs": inputs,
            "cards": len(cards), "surnames": items,
            "coverage": {"complete": all(item["complete"] for item in inputs),
                         "scope": "surname-spellings-in-saved-cards-not-kinship"}}


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Нужно положительное число.")
    return number


def parser():
    root = argparse.ArgumentParser(description="Документы Первой мировой: поиск человека и сбор по местности.")
    commands = root.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search", help="Поиск по имени, месту или части")
    for flag in ("surname", "given", "patronymic", "event-place", "regiment", "birth-place", "gubernia"):
        help_text = ("Населённый пункт в поле birth_place сайта (место жительства / призыва; не доказанное место рождения)"
                     if flag == "birth-place" else None)
        search.add_argument("--" + flag, help=help_text)
    volost = commands.add_parser("volost", help="Собрать найденные записи по волости и губернии")
    volost.add_argument("--volost", required=True, help="Волость в поле birth_place_volost сайта")
    volost.add_argument("--gubernia", required=True)
    for command in (search, volost):
        command.add_argument("--kind", nargs="+", choices=("all", *KINDS), default=["all"])
        command.add_argument("--max-records", type=positive, default=1000)
        command.add_argument("--out", required=True, help="JSON вне папки навыка; также контрольная точка")
    spellings = commands.add_parser("places", help="Сравнить написания местностей в сохранённых выдачах (без сети)")
    spellings.add_argument("--input", nargs="+", required=True, help="JSON-выдачи search/volost")
    spellings.add_argument("--target", help="Неопознанное название, с которым сравнить написания")
    spellings.add_argument("--out", help="JSON вне папки навыка; без него вывод в консоль")
    names = commands.add_parser("surnames", help="Сравнить написания фамилий в сохранённых выдачах (без сети)")
    names.add_argument("--input", nargs="+", required=True, help="JSON-выдачи search/volost")
    names.add_argument("--target", help="Фамилия, с которой сравнить написания")
    names.add_argument("--out", help="JSON вне папки навыка; без него вывод в консоль")
    page = commands.add_parser("page", help="Найти скан и координаты строк по pages_id")
    page.add_argument("--pages", nargs="+", type=positive, required=True)
    page.add_argument("--out", required=True)
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command in ("places", "surnames"):
            path = outside_skill(args.out) if args.out else None
            if path is not None:
                for name in args.input:
                    source = Path(name).expanduser().resolve()
                    if path == source or (path.exists() and source.exists() and path.samefile(source)):
                        raise SourceError("Выходной файл не должен заменять исходную выдачу GWAR.")
            compare = places if args.command == "places" else surnames
            result = compare([(name, read_json(name)) for name in args.input], args.target)
            output_json(result, path)
            return 0 if result["coverage"]["complete"] else 1
        path = outside_skill(args.out)
        if args.command == "page":
            result = pages(source_client(), args.pages)
            output_json(result, path)
        else:
            if args.command == "volost":
                fields = {"birth_place_volost": args.volost, "birth_place_gubernia": args.gubernia}
            else:
                mapping = {"surname": "last_name", "given": "first_name", "patronymic": "middle_name",
                           "event_place": "event_place", "regiment": "military_unit_name",
                           "birth_place": "birth_place", "gubernia": "birth_place_gubernia"}
                fields = {field: getattr(args, key) for key, field in mapping.items() if getattr(args, key)}
                if not fields:
                    raise SourceError("Укажите имя, местность или воинскую часть.")
            kinds = list(KINDS) if "all" in args.kind else list(dict.fromkeys(args.kind))
            with state_lock(str(path) + ".lock"):
                result = collect(source_client(), fields, [KINDS[kind] for kind in kinds], args.max_records, path)
        return 0 if result["coverage"]["complete"] else 1
    except (SourceError, OSError, ValueError, TypeError, KeyError) as exc:
        print("Ошибка: " + (str(exc) if isinstance(exc, SourceError) else "Некорректный файл или ошибка локального ввода/вывода."), file=sys.stderr)
        return 1


if __name__ == "__main__":
    configure_utf8_stdio()
    raise SystemExit(main())
