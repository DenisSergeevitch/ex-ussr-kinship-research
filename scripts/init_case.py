#!/usr/bin/env python3
"""Create a portable case directory from the bundled assets."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ASSET_FILES = {
    "case-intake.template.yaml": "case-intake.yaml",
    "person-register.csv": "person-register.csv",
    "artifact-register.csv": "artifact-register.csv",
    "claims-register.csv": "claims-register.csv",
    "relationship-register.csv": "relationship-register.csv",
    "search-log.csv": "search-log.csv",
    "final-report.template.md": "final-report.md",
    "research-state.template.md": "research-state.md",
}
PHOTOS_README = "photos-readme.template.md"


def quote_yaml(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Создаёт структуру дела для исследования родственных связей."
    )
    parser.add_argument("--case-dir", required=True, help="Директория нового дела")
    parser.add_argument("--research-question", required=True, help="Главный исследовательский вопрос")
    parser.add_argument("--subject-label", default="", help="Краткая метка основного человека")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Перезаписать только файлы шаблонов; не удаляет иные файлы",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    assets_dir = script_dir.parent / "assets"
    case_dir = Path(args.case_dir).expanduser().resolve()

    if case_dir == script_dir.parent or script_dir.parent in case_dir.parents:
        print(
            "Ошибка: храните дело вне папки навыка, например ~/kinship-cases/my-case.",
            file=sys.stderr,
        )
        return 2

    missing = [name for name in ASSET_FILES if not (assets_dir / name).is_file()]
    if missing:
        print(
            "Ошибка: в skill отсутствуют шаблоны: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    if case_dir.exists() and not case_dir.is_dir():
        print(f"Ошибка: {case_dir} существует и не является директорией.", file=sys.stderr)
        return 2

    case_dir.mkdir(parents=True, exist_ok=True)
    conflicts = [dest for dest in ASSET_FILES.values() if (case_dir / dest).exists()]
    if conflicts and not args.force:
        print(
            "Ошибка: целевые файлы уже существуют: "
            + ", ".join(conflicts)
            + ". Продолжайте работу с существующим делом. Для намеренного сброса шаблонов есть --force.",
            file=sys.stderr,
        )
        return 2

    for source_name, dest_name in ASSET_FILES.items():
        shutil.copyfile(assets_dir / source_name, case_dir / dest_name)

    photos_dir = case_dir / "photos"
    photos_dir.mkdir(exist_ok=True)
    photos_readme = photos_dir / "README.md"
    if not photos_readme.exists() and (assets_dir / PHOTOS_README).is_file():
        shutil.copyfile(assets_dir / PHOTOS_README, photos_readme)

    intake_path = case_dir / "case-intake.yaml"
    text = intake_path.read_text(encoding="utf-8")
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    case_id = case_dir.name
    replacements = {
        'case_id: ""': f"case_id: {quote_yaml(case_id)}",
        'created_at: ""': f"created_at: {quote_yaml(created_at)}",
        'research_question: ""': f"research_question: {quote_yaml(args.research_question)}",
        'subject_label: ""': f"subject_label: {quote_yaml(args.subject_label)}",
        '    label: ""': f"    label: {quote_yaml(args.subject_label)}",
    }
    for old, new in replacements.items():
        if old not in text:
            print(f"Ошибка: маркер шаблона не найден: {old}", file=sys.stderr)
            return 3
        text = text.replace(old, new, 1)
    intake_path.write_text(text, encoding="utf-8")

    print(f"Дело создано: {case_dir}")
    for dest_name in ASSET_FILES.values():
        print(f"- {dest_name}")
    print("- photos/README.md")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from research_common import configure_utf8_stdio

    configure_utf8_stdio()
    raise SystemExit(main())
