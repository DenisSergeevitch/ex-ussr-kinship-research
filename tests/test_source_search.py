"""Synthetic source-search tests; no live accounts, network or private case data."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import familysearch as fs
import gwar
import register_search
import research_common as common
from familysearch import compile_patterns


def sample_fragment():
    return {
        "url": "https://www.familysearch.org/en/search/record/results",
        "captured_at": "2026-10-26T12:00:00Z",
        "scope": {"dgs": "000000001", "description": "one relevant result"},
        "rows": [{"url": "https://www.familysearch.org/ark:/61903/1:1:TEST-ROW",
                  "name": "Иван Иванов",
                  "text": "Иван Иванов. Parent: Мария Петрова. Witness: Пётр Сидоров / Petr Sidorov.",
                  "people": [{"name": "Иван Иванов", "label": "Primary"},
                             {"name": "Мария Петрова", "label": "Parent"},
                             {"name": "Пётр Сидоров / Petr Sidorov", "label": "Witness"}]}]
    }


class FakeClient:
    def __init__(self, handler):
        self.handler = handler
        self.calls = []

    def request(self, path, body=None, as_json=True):
        self.calls.append((path, body, as_json))
        return self.handler(path, body, as_json)


def hit(number):
    return {"_index": "gwar", "_type": "chelovek_donesenie", "_id": str(number),
            "_source": {"last_name": "Иванов", "first_name": "Пётр", "birth_place": "Условное село",
                        "documents_pages": {"pages_id": [1000 + number]}}}


class GwarTests(unittest.TestCase):
    def test_pow_cli_selects_card_index_and_default_all(self):
        cases = (
            (["--kind", "pows"], ["chelovek_plen"]),
            ([], ["chelovek_donesenie", "chelovek_gospital", "chelovek_nagrazhdenie", "chelovek_plen"]),
        )
        for flags, expected in cases:
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as tmp:
                client = FakeClient(lambda path, body, as_json:
                                    "public page" if not as_json else {"hits": {"total": 0, "hits": []}})
                with patch.object(gwar, "source_client", return_value=client):
                    result = gwar.main(["search", "--surname", "Условный", "--out", str(Path(tmp) / "gwar.json"), *flags])
                self.assertEqual(result, 0)
                self.assertEqual(client.calls[-1][1]["entities"], expected)

    def test_completed_cache_keeps_capture_time_without_new_requests(self):
        def handler(path, body, as_json):
            return "public page" if not as_json else {"hits": {"total": 1, "hits": [hit(1)]}}
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = Path(tmp) / "gwar.json"
            first = gwar.collect(FakeClient(handler), {"last_name": "Иванов"}, list(gwar.KINDS.values()), 1, checkpoint)
            first["captured_at"] = "2000-01-01T00:00:00+00:00"
            common.save_json(checkpoint, first)
            def unexpected(*args):
                self.fail("A completed cache must not make a new source request")
            cached = gwar.collect(FakeClient(unexpected), {"last_name": "Иванов"}, list(gwar.KINDS.values()), 1, checkpoint)
            self.assertEqual(cached["captured_at"], first["captured_at"])
            self.assertEqual(cached["hits"], first["hits"])

    def test_limit_and_resume_preserve_all_entity_kinds_and_offsets(self):
        def handler(path, body, as_json):
            if not as_json:
                return "public page"
            start, size = body["from"], body["size"]
            return {"hits": {"total": {"value": 3, "relation": "eq"}, "hits": [hit(i) for i in range(start, min(3, start + size))]}}
        client = FakeClient(handler)
        entities = list(gwar.KINDS.values())
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = Path(tmp) / "gwar.json"
            first = gwar.collect(client, {"birth_place": "Условное село"}, entities, 2, checkpoint)
            self.assertFalse(first["coverage"]["complete"])
            self.assertEqual(first["coverage"]["reason"], "limit-reached")
            second = gwar.collect(client, {"birth_place": "Условное село"}, entities, 3, checkpoint)
            self.assertTrue(second["coverage"]["complete"])
            self.assertEqual(len(second["hits"]), 3)
            self.assertEqual(client.calls[-1][1]["from"], 2)
            self.assertEqual(client.calls[-1][1]["entities"], entities)
            with self.assertRaises(common.SourceError):
                gwar.collect(client, {"birth_place": "Другая волость"}, entities, 3, checkpoint)

    def test_repeated_pages_and_access_failures_are_not_complete(self):
        client = FakeClient(lambda path, body, as_json: "page" if not as_json else {"hits": {"total": 3, "hits": [hit(0)]}})
        self.assertFalse(gwar.collect(client, {"last_name": "Иванов"}, list(gwar.KINDS.values()), 3)["coverage"]["complete"])
        def denied(*args):
            raise common.SourceError("limit", 429)
        blocked = gwar.collect(FakeClient(denied), {}, [], 3)
        self.assertEqual(blocked["blocked"]["status"], 429)

    def test_scan_locator_and_scoped_certificates(self):
        parsed = gwar.parse_scan('<page image="folder/test.jpg"><s id="row" c="1,2,3,4"/></page>')
        self.assertEqual(parsed["zones"][0]["c"], "1,2,3,4")
        self.assertEqual(parsed["image_url"], "https://gwar.mil.ru/cdn/imagesfww/folder/test.jpg")
        self.assertEqual(gwar.source_client().base, gwar.BASE)

    def test_places_group_spellings_by_volost_and_rank_by_target(self):
        def card(number, place, **fields):
            return {"_index": "gwar", "_type": "chelovek_donesenie", "_id": str(number),
                    "_source": {"birth_place": place, **fields}}
        state = {"query": {"last_name": "Иванов"}, "coverage": {"complete": True}, "hits": [
            card(1, "Условная губ., Северный уезд, селение Новоберезицы"),
            card(2, "Условная губ., Северный уезд, Заречная вол., д. Новобережка"),
            card(3, "Условная губ., Северный уезд, Заречная вол., с. Новобережка"),
            card(4, "с. Каменка", birth_place_gubernia="Условная губ.", birth_place_uezd="Северный уезд",
                 birth_place_volost="Заречная вол.")]}
        result = gwar.places([("first.json", state), ("copy.json", state)], "Новоберезицы")
        self.assertEqual(result["cards"], 4)
        self.assertTrue(result["coverage"]["complete"])
        volost = next(group for group in result["groups"] if group["volost"] == "Заречная вол.")
        self.assertEqual(volost["uezd"], "Северный уезд")
        first, last = volost["settlements"][0], volost["settlements"][-1]
        self.assertEqual(first["as_written"], "д. Новобережка")
        self.assertGreater(first["similarity"], last["similarity"])
        self.assertEqual(last["as_written"], "с. Каменка")
        self.assertEqual(gwar.place_key("с. Новобережка"), gwar.place_key("д. Новобережка"))

    def test_places_keep_incomplete_input_visible(self):
        state = {"query": {}, "coverage": {"complete": False}, "hits": [hit(1)]}
        result = gwar.places([("partial.json", state)])
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["groups"][0]["settlements"][0]["as_written"], "Условное село")
        with self.assertRaises(common.SourceError):
            gwar.places([("other.json", {"rows": []})])


    def test_places_preserve_settlements_named_like_administrative_units(self):
        for name in ("Волково", "Губино", "с. Волково"):
            parts = gwar.place_parts({"birth_place": "Тестовая губ., Северный уезд, Заречная вол., " + name})
            self.assertEqual(parts["settlement"], name)
            self.assertEqual(parts["volost"], "Заречная вол.")
        self.assertEqual(gwar.similarity("Ая", "Уя"), 0.5)

    def test_places_keep_namespaces_and_reject_conflicting_snapshots(self):
        first, second = hit(1), hit(1)
        second["_type"] = "chelovek_gospital"
        state = {"hits": [first, second], "coverage": {"complete": True}}
        result = gwar.places([("a.json", state)])
        entry = result["groups"][0]["settlements"][0]
        self.assertEqual(result["cards"], 2)
        self.assertEqual(len(set(entry["card_keys"])), 2)
        changed = hit(1)
        changed["_source"]["birth_place"] = "Иное село"
        with self.assertRaises(common.SourceError):
            gwar.places([("a.json", state), ("b.json", {"hits": [changed], "coverage": {"complete": True}})])

    def test_places_reject_malformed_cards_and_nonboolean_coverage(self):
        for bad in (None, {}, {"_id": "1", "_source": []}):
            with self.assertRaises(common.SourceError):
                gwar.places([("bad.json", {"hits": [bad], "coverage": {"complete": True}})])
        result = gwar.places([("bad-coverage.json", {"hits": [], "coverage": {"complete": "false"}})])
        self.assertFalse(result["coverage"]["complete"])
        with self.assertRaises(common.SourceError):
            gwar.places([])

    def test_offline_comparisons_never_overwrite_an_input_or_contact_the_site(self):
        for command in ("places", "surnames"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "source.json"
                common.save_json(source, {"source": "gwar", "hits": [hit(1)], "coverage": {"complete": True}})
                original = source.read_bytes()
                with patch.object(gwar, "source_client", side_effect=AssertionError("offline command")):
                    self.assertEqual(gwar.main([command, "--input", str(source), "--out", str(source)]), 1)
                    self.assertEqual(source.read_bytes(), original)
                    output = Path(tmp) / "out.json"
                    self.assertEqual(gwar.main([command, "--input", str(source), "--out", str(output)]), 0)
                    for alias_name in ("symlink.json", "hardlink.json"):
                        alias = Path(tmp) / alias_name
                        if alias_name == "symlink.json":
                            alias.symlink_to(source)
                        else:
                            alias.hardlink_to(source)
                        self.assertEqual(gwar.main([command, "--input", str(source), "--out", str(alias)]), 1)
                        self.assertTrue(alias.samefile(source))
                    self.assertEqual(source.read_bytes(), original)

    def test_surnames_rank_spellings_by_target_and_keep_card_context(self):
        def card(number, surname, given="", kind="chelovek_donesenie", **fields):
            return {"_index": "gwar", "_type": kind, "_id": str(number),
                    "_source": {"last_name": surname, "first_name": given, **fields}}
        complete = {"coverage": {"complete": True}, "hits": [
            card(1, "Тестенко", "Иван", middle_name="Первый", birth_place="Условное село"),
            card(1, "Тестенко", "Пётр", kind="chelovek_gospital", birth_place_volost="Условная волость"),
            card(2, "Тэстенко", "Пётр"), card(3, "Дестенко"), card(4, "Условный"), card(5, "")]}
        partial = {"coverage": {"complete": False}, "hits": [{**card(2, "Тэстенко", "Пётр"), "_score": 4}]}
        result = gwar.surnames([("volost.json", complete), ("person.json", partial)], "Тестенко")
        order = [item["as_written"] for item in result["surnames"]]
        self.assertEqual(order, ["Тестенко", "Тэстенко", "Дестенко", "Условный", ""])
        first = result["surnames"][0]
        self.assertEqual(first["cards"], 2)
        contexts = {row["card_key"]: row for row in first["card_context"]}
        self.assertEqual(contexts, {
            "gwar|chelovek_donesenie|1": {"card_id": "1", "card_key": "gwar|chelovek_donesenie|1",
                                         "first_name": "Иван", "middle_name": "Первый", "birth_place": "Условное село"},
            "gwar|chelovek_gospital|1": {"card_id": "1", "card_key": "gwar|chelovek_gospital|1",
                                        "first_name": "Пётр", "birth_place_volost": "Условная волость"},
        })
        self.assertEqual(result["surnames"][1]["cards"], 1)
        self.assertEqual(result["surnames"][1]["similarity"], 1.0)
        self.assertGreater(result["surnames"][2]["similarity"], result["surnames"][3]["similarity"])
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["coverage"]["scope"], "surname-spellings-in-saved-cards-not-kinship")
        with self.assertRaises(common.SourceError):
            gwar.surnames([("other.json", {"rows": []})])

    def test_surnames_cli_writes_partial_result_and_returns_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "partial.json"
            output = Path(tmp) / "out.json"
            common.save_json(source, {"source": "gwar", "hits": [hit(1)], "coverage": {"complete": False}})
            with patch.object(gwar, "source_client", side_effect=AssertionError("offline command")):
                self.assertEqual(gwar.main(["surnames", "--input", str(source), "--out", str(output)]), 1)
            result = common.read_json(output)
            self.assertFalse(result["coverage"]["complete"])
            self.assertEqual(result["cards"], 1)


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.case = self.directory / "case"
        subprocess.run([sys.executable, str(SCRIPTS / "init_case.py"), "--case-dir", str(self.case),
                        "--research-question", "Кто родители условного человека?"], check=True, capture_output=True)

    def rows(self, name):
        with (self.case / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def result(self):
        source = self.directory / "fragment.json"
        common.save_json(source, sample_fragment())
        return fs.browser_import([source], compile_patterns(surnames=["Петрова"]))

    def test_end_to_end_preserves_evidence_boundary_and_is_idempotent(self):
        path = self.directory / "analysis.json"
        common.save_json(path, self.result())
        untouched = {name: (self.case / name).read_bytes() for name in ("claims-register.csv", "person-register.csv", "relationship-register.csv")}
        first = register_search.register(self.case, path, "Найти родителей")
        second = register_search.register(self.case, path, "Найти родителей")
        self.assertEqual(first["added_artifacts"], 1)
        self.assertEqual(second["added_artifacts"], 0)
        self.assertFalse(second["added_search_log"])
        artifact = self.rows("artifact-register.csv")[0]
        self.assertEqual(artifact["originality"], "index")
        self.assertEqual(artifact["directness"], "lead-only")
        self.assertEqual(artifact["independence_group"], "")
        self.assertEqual(artifact["person_ids"], "")
        self.assertIn("DGS", artifact["archival_reference"].upper())
        snapshot = next((self.case / "sources" / "familysearch").glob("*.json"))
        self.assertEqual(hashlib.sha256(snapshot.read_bytes()).hexdigest(), artifact["sha256"])
        for name, content in untouched.items():
            self.assertEqual((self.case / name).read_bytes(), content)
        audit = subprocess.run([sys.executable, str(SCRIPTS / "audit_evidence.py"), "--case-dir", str(self.case), "--json"], capture_output=True, encoding="utf-8")
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        self.assertIn("independence_group", audit.stdout)

    def test_preserves_manual_evaluation_and_source_revisions(self):
        path = self.directory / "analysis.json"
        result = self.result()
        common.save_json(path, result)
        register_search.register(self.case, path, "goal")
        fields, rows = register_search.read_register(self.case / "artifact-register.csv", "artifact_id")
        rows[0]["independence_group"] = "ORIGINAL-ACT-1"
        register_search.save_register(self.case / "artifact-register.csv", fields, rows)
        register_search.register(self.case, path, "goal")
        self.assertEqual(self.rows("artifact-register.csv")[0]["independence_group"], "ORIGINAL-ACT-1")
        result["candidates"][0]["record"]["persons"]["observed-1"]["name"] = "Исправленное имя"
        common.save_json(path, result)
        self.assertEqual(register_search.register(self.case, path, "goal")["added_artifacts"], 1)
        self.assertEqual(len(self.rows("artifact-register.csv")), 2)

    def test_partial_empty_result_is_not_negative_evidence(self):
        result = self.result()
        result["candidates"] = []
        result["coverage"]["complete"] = False
        path = self.directory / "partial.json"
        common.save_json(path, result)
        report = register_search.register(self.case, path, "goal")
        self.assertEqual(report["result_status"], "partial")
        self.assertEqual(self.rows("artifact-register.csv"), [])
        self.assertEqual(self.rows("search-log.csv")[0]["result_status"], "partial")

    def manual_input(self, **changes):
        data = {"source": "manual", "source_or_domain": "archive.org", "query": {"surname": "Иванов", "place": "Условный уезд"},
                "coverage": {"complete": True},
                "items": [{"id": "https://archive.org/details/directory-1900#page=12", "source_title": "Адрес-календарь 1900, с. 12",
                           "source_url_or_path": "https://archive.org/details/directory-1900", "names_as_written": "Иванов Пётр, мещанин",
                           "snapshot": {"line": "Иванов Пётр, мещанин, Садовая, 5"}},
                          {"id": "directory-1900:p13:l4", "source_title": "Адрес-календарь 1900, с. 13",
                           "source_url_or_path": "https://archive.org/details/directory-1900", "names_as_written": "Иванова Анна",
                           "language_script": "ru, кириллица"}]}
        data.update(changes)
        return data

    def register_manual(self, data, name="manual.json"):
        path = self.directory / name
        common.save_json(path, data)
        return register_search.register(self.case, path, "Найти адреса")

    def test_manual_source_registers_leads_and_is_idempotent(self):
        untouched = {name: (self.case / name).read_bytes() for name in ("claims-register.csv", "person-register.csv", "relationship-register.csv")}
        data = self.manual_input()
        first = self.register_manual(data)
        second = self.register_manual(data)
        self.assertEqual(first["added_artifacts"], 2)
        self.assertEqual(first["artifact_ids"], ["A-0001", "A-0002"])
        self.assertEqual(second["added_artifacts"], 0)
        self.assertFalse(second["added_search_log"])
        artifacts = self.rows("artifact-register.csv")
        self.assertEqual(len(artifacts), 2)
        for artifact in artifacts:
            self.assertEqual(artifact["status"], "lead-only")
            self.assertEqual(artifact["directness"], "lead-only")
            self.assertTrue(artifact["source_url_or_path"].startswith("https://archive.org/"))
            self.assertTrue(artifact["names_as_written"])
            self.assertEqual(artifact["repository_or_archive"], "уточнить по источнику")
        self.assertEqual(artifacts[1]["language_script"], "ru, кириллица")
        snapshots = sorted((self.case / "sources" / "manual").glob("*.json"))
        self.assertEqual(len(snapshots), 2)
        saved = json.loads(snapshots[0].read_text(encoding="utf-8"))
        self.assertIn(saved["record"]["id"], {item["id"] for item in data["items"]})
        logs = self.rows("search-log.csv")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["source_or_domain"], "archive.org")
        self.assertEqual(logs[0]["result_status"], "found")
        self.assertEqual(logs[0]["artifact_ids"], "A-0001;A-0002")
        for name, content in untouched.items():
            self.assertEqual((self.case / name).read_bytes(), content)

    def test_manual_sources_with_same_local_record_id_stay_separate(self):
        item = {"id": "page-1", "source_title": "Локальная заметка", "snapshot": {"line": "Условный текст"}}
        self.register_manual(self.manual_input(source_or_domain="Источник A", items=[item]))
        second = self.register_manual(self.manual_input(source_or_domain="Источник B", items=[item]), "other.json")
        self.assertEqual(second["added_artifacts"], 1)
        self.assertEqual(len(self.rows("artifact-register.csv")), 2)
        snapshots = [json.loads(path.read_text(encoding="utf-8")) for path in (self.case / "sources" / "manual").glob("*.json")]
        self.assertEqual({item["record"]["source_or_domain"] for item in snapshots}, {"Источник A", "Источник B"})

    def test_manual_unknown_coverage_stays_partial_and_originality_unknown(self):
        data = self.manual_input()
        del data["coverage"]
        result = self.register_manual(data)
        self.assertEqual(result["result_status"], "partial")
        for artifact in self.rows("artifact-register.csv"):
            self.assertEqual(artifact["originality"], "unknown")
            self.assertEqual(artifact["source_type"], "unknown")
            self.assertNotIn("установлен", artifact["provenance_level"])
            self.assertEqual(artifact["independence_group"], "")
        empty = self.register_manual({**data, "items": []}, "unknown-empty.json")
        self.assertEqual(empty["result_status"], "partial")

    def test_manual_source_empty_items_is_not_found(self):
        report = self.register_manual(self.manual_input(items=[]))
        self.assertEqual(report["result_status"], "not-found")
        self.assertEqual(self.rows("artifact-register.csv"), [])
        report = self.register_manual(self.manual_input(items=[], coverage={"complete": False}), "partial.json")
        self.assertEqual(report["result_status"], "partial")
        self.assertEqual([row["result_status"] for row in self.rows("search-log.csv")], ["not-found", "partial"])

    def test_manual_source_rejects_bad_input(self):
        item = self.manual_input()["items"][0]
        def without(key):
            data = self.manual_input()
            del data[key]
            return data
        cases = {
            "no domain": without("source_or_domain"),
            "no items": without("items"),
            "items not a list": self.manual_input(items={"id": "x"}),
            "no id": self.manual_input(items=[{k: v for k, v in item.items() if k != "id"}]),
            "unknown key": self.manual_input(items=[{**item, "foo": "bar"}]),
            "no title": self.manual_input(items=[{k: v for k, v in item.items() if k != "source_title"}]),
            "snapshot not dict": self.manual_input(items=[{**item, "snapshot": "text"}]),
        }
        for label, data in cases.items():
            with self.subTest(label), self.assertRaises(common.SourceError):
                self.register_manual(data, "bad.json")
        self.assertEqual(self.rows("artifact-register.csv"), [])
        self.assertEqual(self.rows("search-log.csv"), [])

    def test_manual_source_changed_snapshot_for_same_id_is_rejected(self):
        self.register_manual(self.manual_input())
        snapshot = next((self.case / "sources" / "manual").glob("*.json"))
        saved = json.loads(snapshot.read_text(encoding="utf-8"))
        saved["record"]["snapshot"] = {"line": "подменённая строка"}
        snapshot.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
        fields, rows = register_search.read_register(self.case / "artifact-register.csv", "artifact_id")
        register_search.save_register(self.case / "artifact-register.csv", fields, [])
        with self.assertRaises(common.SourceError) as caught:
            self.register_manual(self.manual_input(), "again.json")
        self.assertIn("не соответствует", str(caught.exception))

    def test_gwar_import_and_restart_between_register_writes(self):
        path = self.directory / "gwar.json"
        common.save_json(path, {"source": "gwar", "hits": [hit(1), hit(2)], "query": {"birth_place": "Условное село"},
                                "coverage": {"complete": True}, "captured_at": common.timestamp()})
        original_save = register_search.save_register
        def fail_log(path, fields, rows):
            if path.name == "search-log.csv":
                raise OSError("simulated interruption")
            original_save(path, fields, rows)
        with patch.object(register_search, "save_register", side_effect=fail_log):
            with self.assertRaises(OSError):
                register_search.register(self.case, path, "goal")
        report = register_search.register(self.case, path, "goal")
        self.assertEqual(report["added_artifacts"], 0)
        self.assertEqual(len(self.rows("artifact-register.csv")), 2)
        self.assertEqual(len(self.rows("search-log.csv")), 1)
        self.assertEqual(self.rows("artifact-register.csv")[0]["source_url_or_path"],
                         "https://gwar.mil.ru/heroes/chelovek_donesenie1/")

    def test_gwar_card_locators_keep_unknown_routes_in_snapshot(self):
        for kind, identifier, suffix in (
            ("chelovek_donesenie", "12", "chelovek_donesenie12/"),
            ("chelovek_gospital", "34", "chelovek_gospital34/"),
            ("chelovek_plen", "78", "chelovek_plen78/"),
            ("unknown", "56", ""),
            ("chelovek_donesenie", "1/../../elsewhere", ""),
            ("chelovek_gospital", "１２", ""),
        ):
            with self.subTest(kind=kind, identifier=identifier):
                record = {**hit(1), "_type": kind, "_id": identifier}
                item, = register_search.gwar_items({"hits": [record]})
                self.assertEqual(item["source_url_or_path"], "https://gwar.mil.ru/heroes/" + suffix)
                self.assertEqual(item["snapshot"], record)

    def test_gwar_import_keeps_volost_uezd_and_gubernia(self):
        path = self.directory / "gwar.json"
        record = hit(1)
        record["_source"].update({"birth_place": None, "birth_place_volost": "Условная вол.",
                                  "birth_place_uezd": "Условный у.", "birth_place_gubernia": "Условная губ."})
        common.save_json(path, {"source": "gwar", "hits": [record], "coverage": {"complete": True},
                                "query": {"last_name": "Иванов"}})
        register_search.register(self.case, path, "goal")
        self.assertEqual(self.rows("artifact-register.csv")[0]["place_as_written"],
                         "Условная вол., Условный у., Условная губ.")

    def test_gwar_search_score_changes_do_not_duplicate_source_cards(self):
        path = self.directory / "gwar.json"
        record = {**hit(1), "_score": 150.0}
        data = {"source": "gwar", "hits": [record], "coverage": {"complete": True}, "query": {"birth_place": "Условное село"}}
        common.save_json(path, data)
        register_search.register(self.case, path, "goal")
        fields, rows = register_search.read_register(self.case / "artifact-register.csv", "artifact_id")
        rows[0]["independence_group"] = "REVIEWED-DOCUMENT"
        register_search.save_register(self.case / "artifact-register.csv", fields, rows)
        record["_score"] = 95.0
        data["query"] = {"last_name": "Иванов"}
        common.save_json(path, data)
        second = register_search.register(self.case, path, "goal")
        self.assertEqual(second["added_artifacts"], 0)
        self.assertTrue(second["added_search_log"])
        self.assertEqual(len(self.rows("artifact-register.csv")), 1)
        self.assertEqual(self.rows("artifact-register.csv")[0]["independence_group"], "REVIEWED-DOCUMENT")
        record["_source"]["first_name"] = "Исправленное имя"
        common.save_json(path, data)
        self.assertEqual(register_search.register(self.case, path, "goal")["added_artifacts"], 1)

    def test_browser_index_text_uses_same_registers_without_inventing_parent_role(self):
        page = self.directory / "browser.json"
        snapshot = {"url": "https://www.familysearch.org/en/search/record/results?q.surname=test",
                    "scope": {"description": "one observed result", "page": 1},
                    "rows": [{"name": "Иван Иванов", "url": "https://www.familysearch.org/ark:/61903/1:1:TEST-ROW",
                              "text": "Иван Иванов. Parents: Мария Петрова, Пётр Иванов"}]}
        common.save_json(page, snapshot)
        result = fs.browser_import([page, page], compile_patterns(surnames=["Петрова"]))
        self.assertEqual(len(result["candidates"]), 1)
        self.assertIsNone(result["hits"]["Петрова"][0]["pid"])
        self.assertIsNone(result["hits"]["Петрова"][0]["principal"])
        self.assertFalse(result["coverage"]["complete"])
        record = result["candidates"][0]["record"]
        self.assertNotIn("rels", record)
        self.assertIn("Мария Петрова", record["browser_text"])
        self.assertNotIn("facts", record["persons"]["principal"])
        output = self.directory / "browser-analysis.json"
        common.save_json(output, result)
        report = register_search.register(self.case, output, "Найти родителей")
        self.assertEqual(report["added_artifacts"], 1)
        self.assertEqual(report["result_status"], "partial")
        self.assertEqual(self.rows("claims-register.csv"), [])

    def test_browser_import_rejects_foreign_urls_and_conflicting_rows(self):
        page = self.directory / "browser.json"
        snapshot = {"url": "https://www.familysearch.org/en/search/record/results", "scope": {},
                    "rows": [{"name": "Иван Иванов", "url": "https://other.invalid/ark:/61903/1:1:TEST", "text": "Иван Иванов"}]}
        common.save_json(page, snapshot)
        with self.assertRaises(common.SourceError):
            fs.browser_import([page], [])
        snapshot["rows"][0]["url"] = "https://www.familysearch.org/ark:/61903/1:1:TEST"
        snapshot["rows"].append({**snapshot["rows"][0], "text": "Исправленная строка"})
        common.save_json(page, snapshot)
        with self.assertRaises(common.SourceError):
            fs.browser_import([page], [])

class HttpAndCliTests(unittest.TestCase):
    def test_cyrillic_search_and_page_context_reach_source_unchanged(self):
        # Live GWAR returned a false empty result until the source's UTF-8 JSON
        # representation and /heroes/ page context were preserved in the port.
        client = common.SourceClient(gwar.BASE, interval=0, referer=gwar.BASE + "/heroes/")
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b'{"hits":{"total":0,"hits":[]}}'
        with patch.object(client.opener, "open", return_value=Response()) as opened:
            client.request("/gt_data/?builder=Heroes", {"queryFields": {"last_name": "Иванов"}})
            request = opened.call_args.args[0]
            self.assertIn("Иванов".encode("utf-8"), request.data)
            self.assertEqual(request.get_header("Referer"), gwar.BASE + "/heroes/")

    def test_html_challenge_is_access_failure_even_with_http_200(self):
        client = common.SourceClient(gwar.BASE, interval=0)
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b'<html><div class="smartcaptcha">human verification</div></html>'
        with patch.object(client.opener, "open", return_value=Response()) as opened:
            with self.assertRaises(common.SourceError) as caught:
                client.request("/test")
            self.assertEqual(caught.exception.status, 403)
            self.assertEqual(opened.call_count, 1)

    def test_rate_limit_and_access_denials_are_not_retried_or_echoed(self):
        client = common.SourceClient(gwar.BASE, interval=0)
        for status in (401, 403, 429):
            error = urllib.error.HTTPError(gwar.BASE, status, "synthetic-secret", {}, None)
            with patch.object(client.opener, "open", side_effect=error) as opened:
                with self.assertRaises(common.SourceError) as caught:
                    client.request("/test")
                self.assertEqual(opened.call_count, 1)
                self.assertNotIn("synthetic-secret", str(caught.exception))

    def test_cross_origin_redirect_never_forwards_session(self):
        request = urllib.request.Request(gwar.BASE + "/test", headers={"Cookie": "public-session=synthetic"})
        with self.assertRaises(common.SourceError):
            common.SameOriginRedirect().redirect_request(request, None, 302, "redirect", {}, "https://other.invalid/test")

    def test_command_help_is_available(self):
        for script in ("familysearch.py", "gwar.py", "register_search.py"):
            for flags in ([], ["-I"]):
                result = subprocess.run([sys.executable, *flags, str(SCRIPTS / script), "--help"], capture_output=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_outputs_cannot_be_inside_skill(self):
        for path in (SCRIPTS / "private.json", SCRIPTS.parent):
            with self.assertRaises(common.SourceError):
                common.outside_skill(path)

    def test_state_lock_excludes_another_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lock"
            with common.state_lock(path):
                with self.assertRaises(common.SourceError):
                    with common.state_lock(path):
                        self.fail("concurrent writer")
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
