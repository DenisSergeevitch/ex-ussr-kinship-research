"""Ленты-обзоры: выбор кадров по номерам, вырезка графы и разбиение на ленты."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.scan_montage import frame_number, main, parse_box, select_frames

try:
    from PIL import Image, ImageDraw
except ImportError:  # Pillow — необязательная зависимость
    Image = None


class FrameSelection(unittest.TestCase):
    def test_frame_number_is_last_number_in_name(self):
        self.assertEqual(frame_number(Path("-archive-d1764-0007.jpg")), 7)
        self.assertEqual(frame_number(Path("00000116.jpg")), 116)
        self.assertIsNone(frame_number(Path("cover.jpg")))

    def test_range_filters_and_ignores_non_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("0001.jpg", "0002.jpg", "0003.png", "0004.jpg", "SHA256SUMS", "notes.txt"):
                (Path(tmp) / name).write_bytes(b"")
            names = [p.name for p in select_frames(Path(tmp), 2, 3)]
            self.assertEqual(names, ["0002.jpg", "0003.png"])

    def test_box_validation(self):
        self.assertEqual(parse_box("0.1,0.2,0.5,0.6"), (0.1, 0.2, 0.5, 0.6))
        for bad in ("0.5,0.2,0.1,0.6", "0,0,1", "0,0,1.5,1"):
            with self.subTest(bad=bad), self.assertRaises(Exception):
                parse_box(bad)


@unittest.skipIf(Image is None, "Pillow не установлен")
class Montage(unittest.TestCase):
    def make_frames(self, folder: Path, count: int, landscape: bool):
        size = (400, 200) if landscape else (200, 400)
        for i in range(1, count + 1):
            image = Image.new("L", size, 255)
            ImageDraw.Draw(image).rectangle((size[0] - 60, 20, size[0] - 10, 40), fill=0)
            image.save(folder / f"{i:04d}.jpg")

    def test_sheets_are_split_and_labelled_by_frame_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 5, landscape=True)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(out), "--box", "0,0,1,0.5",
                             "--half", "auto", "--per-sheet", "2", "--width", "300"])
            self.assertEqual(code, 0)
            names = sorted(p.name for p in out.iterdir())
            self.assertEqual(names, ["strip-0001-0002.jpg", "strip-0003-0004.jpg", "strip-0005-0005.jpg"])
            with Image.open(out / "strip-0001-0002.jpg") as sheet:
                self.assertEqual(sheet.size[0], 370)

    def test_output_reports_completed_sheets_and_skipped_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 3, landscape=True)
            (src / "0002.jpg").unlink()
            Image.new("L", (10, 10)).save(src / "cover.jpg")
            output, error = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                code = main([str(src), "--out", str(out), "--box", "0,0,1,0.5", "--half", "auto",
                             "--rotate", "90", "--per-sheet", "2"])
            self.assertEqual(code, 0)
            self.assertIn("strip-0001-0003.jpg", output.getvalue())
            self.assertIn("cover.jpg", error.getvalue())
            self.assertEqual(len(output.getvalue().splitlines()), 1)
            self.assertNotIn("strip-0001-0003.jpg", error.getvalue())
            self.assertNotIn("0001.jpg", error.getvalue())

    def test_failure_reports_completed_sheets_and_safe_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 4, landscape=False)
            (src / "0004.jpg").write_bytes(b"not an image")
            output, error = io.StringIO(), io.StringIO()
            args = [str(src), "--out", str(out), "--box", "0,0,1,1", "--per-sheet", "2"]
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                code = main(args)
            self.assertEqual(code, 2)
            self.assertIn("strip-0001-0002.jpg", output.getvalue())
            self.assertIn("--first 3", error.getvalue())
            self.assertIn("0004.jpg", error.getvalue())
            self.assertNotIn("0003.jpg", output.getvalue())
            Image.new("L", (200, 400)).save(src / "0004.jpg")
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(args + ["--first", "3"]), 0)
            self.assertTrue((out / "strip-0003-0004.jpg").exists())

    def test_close_failure_removes_partial_sheet_and_allows_retry(self):
        class CloseFails:
            def __init__(self, file):
                self.file = file

            def __enter__(self):
                return self.file

            def __exit__(self, *args):
                self.file.close()
                raise OSError("simulated close failure")

        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 1, landscape=False)
            original_open = Path.open

            def fail_close(path, *args, **kwargs):
                file = original_open(path, *args, **kwargs)
                return CloseFails(file) if args and args[0] == "xb" else file

            args = [str(src), "--out", str(out), "--box", "0,0,1,1"]
            error = io.StringIO()
            with patch.object(Path, "open", fail_close), contextlib.redirect_stderr(error):
                self.assertEqual(main(args), 2)
            self.assertIn("--first 1", error.getvalue())
            self.assertFalse((out / "strip-0001-0001.jpg").exists())
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(args + ["--first", "1"]), 0)

    def test_empty_range_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            self.make_frames(src, 2, landscape=False)
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(src / "o"), "--box", "0,0,1,1", "--first", "9"])
            self.assertEqual(code, 1)

    def test_existing_output_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            out.mkdir()
            self.make_frames(src, 3, landscape=True)
            existing = out / "strip-0003-0003.jpg"
            existing.write_bytes(b"preserve existing output")
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(out), "--box", "0,0,1,1", "--per-sheet", "2"])
            self.assertEqual(code, 2)
            self.assertEqual(list(out.iterdir()), [existing])
            self.assertEqual(existing.read_bytes(), b"preserve existing output")

    def test_source_image_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            original = src / "0001-0001.jpg"
            Image.new("L", (200, 100), 127).save(original)
            before = original.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(src), "--box", "0,0,1,1", "--prefix", ""])
            self.assertEqual(code, 2)
            self.assertEqual(original.read_bytes(), before)

    def test_duplicate_frame_numbers_do_not_replace_sheets(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 1, landscape=True)
            (src / "copy-0001.jpg").write_bytes((src / "0001.jpg").read_bytes())
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(out), "--box", "0,0,1,1", "--per-sheet", "1"])
            self.assertEqual(code, 2)
            self.assertEqual(list(out.iterdir()), [])

    def test_crop_rounding_to_empty_pixels_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 1, landscape=True)
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                code = main([str(src), "--out", str(out), "--box", "0,0,0.001,0.5"])
            self.assertEqual(code, 2)
            self.assertIn("после округления пуста", error.getvalue())
            self.assertEqual(list(out.iterdir()), [])

    def test_prefix_cannot_escape_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            src.mkdir()
            self.make_frames(src, 1, landscape=True)
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(src), "--out", str(out), "--box", "0,0,1,1", "--prefix", "../escape-"])
            self.assertEqual(code, 2)
            self.assertFalse(Path(tmp, "escape-0001-0001.jpg").exists())


if __name__ == "__main__":
    unittest.main()
