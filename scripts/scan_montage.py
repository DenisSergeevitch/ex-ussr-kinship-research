#!/usr/bin/env python3
"""Собирает из одинаково устроенных сканов ленты-обзоры одной графы.

Из каждого кадра вырезается одна и та же область (например, графа родителей
в метрической книге или строка «Фамилия, имя и отчество домохозяина»
в подворной карточке), при необходимости поворачивается, усиливается по
контрасту и подписывается номером кадра. Полосы складываются в ленты по
N кадров, чтобы просматривать сотни кадров быстро, а кандидатов затем
открывать в полном разрешении. Требует Pillow (`pip install pillow`).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def frame_number(path: Path) -> int | None:
    match = re.search(r"(\d+)(?!.*\d)", path.stem)
    return int(match.group(1)) if match else None


def select_frames(directory: Path, first: int | None, last: int | None,
                  skipped: list[Path] | None = None) -> list[Path]:
    frames = []
    for path in sorted(directory.iterdir()):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        number = frame_number(path)
        if number is None:
            if skipped is not None:
                skipped.append(path)
            continue
        if first is not None and number < first:
            continue
        if last is not None and number > last:
            continue
        frames.append(path)
    return sorted(frames, key=lambda p: (frame_number(p), p.name))


def parse_box(value: str) -> tuple[float, float, float, float]:
    parts = [float(x) for x in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("нужно четыре доли через запятую: x0,y0,x1,y1")
    x0, y0, x1, y1 = parts
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise argparse.ArgumentTypeError("доли должны быть в [0, 1], x0 < x1, y0 < y1")
    return x0, y0, x1, y1


def make_strip(path: Path, box, half: str, rotate: int, width: int, contrast: float):
    from PIL import Image, ImageEnhance, ImageOps

    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("L")
    w, h = image.size
    if half == "right" or (half == "auto" and w > h):
        image = image.crop((w // 2, 0, w, h))
    elif half == "left":
        image = image.crop((0, 0, w // 2, h))
    if rotate:
        image = image.rotate(rotate, expand=True)
    w, h = image.size
    x0, y0, x1, y1 = box
    pixels = (int(w * x0), int(h * y0), int(w * x1), int(h * y1))
    if pixels[2] <= pixels[0] or pixels[3] <= pixels[1]:
        raise ValueError(f"область после округления пуста: {path.name}")
    strip = image.crop(pixels)
    if contrast != 1.0:
        strip = ImageEnhance.Contrast(strip).enhance(contrast)
    height = max(1, round(width * strip.size[1] / strip.size[0]))
    return strip.resize((width, height))


class MontageFailure(Exception):
    def __init__(self, cause, next_frame, failed_source):
        super().__init__(str(cause))
        self.next_frame = next_frame
        self.failed_source = failed_source


def build_sheets(frames, box, half, rotate, width, contrast, per_sheet, out_dir: Path, prefix: str,
                 on_sheet=None):
    from PIL import Image, ImageDraw

    if "/" in prefix or "\\" in prefix:
        raise ValueError("--prefix должен быть префиксом имени, а не путём")
    numbers = [frame_number(path) for path in frames]
    if len(numbers) != len(set(numbers)):
        raise ValueError("номера кадров повторяются; выберите серию с однозначными номерами")
    chunks = [frames[start : start + per_sheet] for start in range(0, len(frames), per_sheet)]
    targets = [out_dir / f"{prefix}{frame_number(chunk[0]):04d}-{frame_number(chunk[-1]):04d}.jpg"
               for chunk in chunks]
    for target in targets:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"файл уже существует, перезапись запрещена: {target}")

    label_width = 70
    written = []
    for chunk, target in zip(chunks, targets):
        path = None
        try:
            rows = []
            for path in chunk:
                strip = make_strip(path, box, half, rotate, width, contrast)
                row = Image.new("L", (label_width + width, strip.size[1] + 4), 255)
                row.paste(strip, (label_width, 0))
                ImageDraw.Draw(row).text((4, 4), str(frame_number(path)), fill=0)
                rows.append(row)
            path = None
            sheet = Image.new("L", (label_width + width, sum(r.size[1] for r in rows)), 255)
            y = 0
            for row in rows:
                sheet.paste(row, (0, y))
                y += row.size[1]
            output = target.open("xb")
            try:
                with output:
                    sheet.save(output, format="JPEG", quality=82)
            except BaseException:
                target.unlink(missing_ok=True)
                raise
        except (OSError, ValueError, Image.DecompressionBombError) as exc:
            raise MontageFailure(exc, frame_number(chunk[0]), path) from exc
        written.append(target)
        if on_sheet is not None:
            on_sheet(target)
    return written


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Собирает ленты-обзоры одной графы из серии сканов.")
    parser.add_argument("directory", help="Папка с кадрами; номер кадра — последнее число в имени файла")
    parser.add_argument("--out", required=True, help="Папка для лент (создаётся при необходимости)")
    parser.add_argument("--box", type=parse_box, required=True, help="Область графы долями кадра после поворота: x0,y0,x1,y1")
    parser.add_argument("--first", type=int, help="Первый номер кадра")
    parser.add_argument("--last", type=int, help="Последний номер кадра")
    parser.add_argument("--half", choices=["none", "left", "right", "auto"], default="none",
                        help="Половина разворота; auto берёт правую половину у альбомных кадров")
    parser.add_argument("--rotate", type=int, choices=[0, 90, -90, 180], default=0, help="Поворот перед вырезкой, градусы")
    parser.add_argument("--per-sheet", type=int, default=12, help="Кадров на ленту (по умолчанию 12)")
    parser.add_argument("--width", type=int, default=1000, help="Ширина полосы в пикселях")
    parser.add_argument("--contrast", type=float, default=1.0, help="Усиление контраста (1.0 — без изменений)")
    parser.add_argument("--prefix", default="strip-", help="Префикс имён лент")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Ошибка: нужен Pillow (pip install pillow)", file=sys.stderr)
        return 2
    directory = Path(args.directory).expanduser()
    if not directory.is_dir():
        print(f"Ошибка: папка не найдена: {directory}", file=sys.stderr)
        return 2
    if args.per_sheet < 1 or args.width < 50:
        print("Ошибка: --per-sheet должно быть ≥ 1, --width ≥ 50", file=sys.stderr)
        return 2
    out_dir = Path(args.out).expanduser()
    try:
        skipped = []
        frames = select_frames(directory, args.first, args.last, skipped)
        for path in skipped:
            print(f"Пропущено изображение без номера кадра: {path}", file=sys.stderr)
        if not frames:
            print("Ошибка: в заданном диапазоне нет кадров", file=sys.stderr)
            return 1
        out_dir.mkdir(parents=True, exist_ok=True)
        written = build_sheets(frames, args.box, args.half, args.rotate, args.width, args.contrast,
                               args.per_sheet, out_dir, args.prefix,
                               on_sheet=lambda target: print(target, flush=True))
    except MontageFailure as exc:
        failed = f"; исходный файл: {exc.failed_source}" if exc.failed_source else ""
        print(f"Ошибка: {exc}{failed}. После устранения причины продолжите с --first {exc.next_frame}",
              file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    print(f"Кадров: {len(frames)}; лент: {len(written)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from research_common import configure_utf8_stdio

    configure_utf8_stdio()
    raise SystemExit(main())
