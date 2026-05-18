#!/usr/bin/env python3
"""Render a polished Chinese composition onto A4 composition-paper pages.

This script is intentionally deterministic: it draws the grid, body text,
red marks, side comments, and a combined PDF without asking an image model
to reproduce long Chinese text.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


A4_W, A4_H = 2480, 3508
BG = (255, 254, 248)
GRID_DEFAULT = (135, 160, 145)
BLACK = (25, 25, 22)
RED = (198, 18, 18)
RED2 = (232, 58, 50)
GRAY = (130, 130, 130)

FONT_DIR = Path(r"C:\Windows\Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in text.replace("\r\n", "\n").split("\n") if p.strip()]


def distribute_paragraphs(paragraphs: list[str], page_count: int) -> list[list[str]]:
    if page_count <= 1:
        return [paragraphs]
    char_counts = [len(p) for p in paragraphs]
    target = sum(char_counts) / page_count
    pages: list[list[str]] = []
    current: list[str] = []
    count = 0
    remaining_pages = page_count
    for i, para in enumerate(paragraphs):
        current.append(para)
        count += len(para)
        remaining_paras = len(paragraphs) - i - 1
        if remaining_pages > 1 and count >= target and remaining_paras >= remaining_pages - 1:
            pages.append(current)
            current = []
            count = 0
            remaining_pages -= 1
    if current:
        pages.append(current)
    while len(pages) < page_count:
        pages.append([])
    return pages[:page_count]


def wrap_note(text: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    cur = ""
    for ch in text:
        cur += ch
        if len(cur) >= max_chars or ch in "。，；！：":
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


class Renderer:
    def __init__(
        self,
        title: str,
        page_count: int,
        grid_color: tuple[int, int, int],
        body_size: int,
        note_size: int,
    ) -> None:
        self.title = title
        self.page_count = page_count
        self.grid_color = grid_color
        self.cols = 20
        self.rows = 25 if page_count == 2 else 22
        self.cell_w = 88 if page_count == 2 else 82
        self.cell_h = 112 if page_count == 2 else 104
        self.grid_x = 125
        self.grid_y = 235 if page_count == 2 else 300
        self.grid_w = self.cols * self.cell_w
        self.grid_h = self.rows * self.cell_h
        self.note_x = self.grid_x + self.grid_w + 58
        self.note_w = A4_W - self.note_x - 105
        self.body_font = font("simkai.ttf", body_size)
        self.title_font = font("simkai.ttf", max(body_size + 9, 68))
        self.note_font = font("simkai.ttf", note_size)
        self.head_font = font("msyhbd.ttc", 32)
        self.footer_font = font("msyh.ttc", 26)

    @staticmethod
    def text_size(ft: ImageFont.FreeTypeFont, s: str) -> tuple[int, int]:
        box = ft.getbbox(s)
        return box[2] - box[0], box[3] - box[1]

    def cell_pos(self, ch: str, col: int, row: int, ft: ImageFont.FreeTypeFont | None = None) -> tuple[float, float]:
        ft = ft or self.body_font
        x = self.grid_x + col * self.cell_w
        y = self.grid_y + row * self.cell_h
        tw, th = self.text_size(ft, ch)
        return x + (self.cell_w - tw) / 2, y + (self.cell_h - th) / 2 - 4

    def draw_grid(self, draw: ImageDraw.ImageDraw, page_no: int) -> None:
        draw.text((self.grid_x + self.grid_w - 430, self.grid_y - 76), "共    页  第    页", fill=(145, 145, 145), font=self.head_font)
        draw.text((self.grid_x + self.grid_w - 300, self.grid_y - 76), str(self.page_count), fill=GRAY, font=self.head_font)
        draw.text((self.grid_x + self.grid_w - 90, self.grid_y - 76), str(page_no), fill=GRAY, font=self.head_font)
        for r in range(self.rows + 1):
            y = self.grid_y + r * self.cell_h
            draw.line((self.grid_x, y, self.grid_x + self.grid_w, y), fill=self.grid_color, width=2)
        for c in range(self.cols + 1):
            x = self.grid_x + c * self.cell_w
            draw.line((x, self.grid_y, x, self.grid_y + self.grid_h), fill=self.grid_color, width=2)
        draw.text((self.grid_x, self.grid_y + self.grid_h + 24), f"20×{self.rows}={20 * self.rows}", fill=(120, 120, 120), font=self.footer_font)

    def write_text(self, draw: ImageDraw.ImageDraw, page_no: int, paragraphs: Iterable[str]) -> int:
        row = 0
        if page_no == 1 and self.title:
            start_col = max(0, (self.cols - len(self.title)) // 2)
            for i, ch in enumerate(self.title):
                x, y = self.cell_pos(ch, start_col + i, row, self.title_font)
                draw.text((x, y - 5), ch, fill=BLACK, font=self.title_font)
            row = 2
        for para in paragraphs:
            col = 2
            for ch in para:
                if row >= self.rows:
                    raise RuntimeError(f"page {page_no} overflow near character {ch!r}")
                x, y = self.cell_pos(ch, col, row)
                draw.text((x, y), ch, fill=BLACK, font=self.body_font)
                col += 1
                if col >= self.cols:
                    row += 1
                    col = 0
            row += 1
        return row

    def draw_note(self, draw: ImageDraw.ImageDraw, text: str, y: int, max_chars: int = 5) -> None:
        lines = wrap_note(text, max_chars)
        line_h = int(self.note_font.size * 1.18)
        pad = 20
        height = pad * 2 + line_h * len(lines)
        x = self.note_x
        draw.rounded_rectangle((x, y, x + self.note_w, y + height), radius=16, outline=RED, width=4)
        yy = y + pad - 8
        for line in lines:
            draw.text((x + pad, yy), line, fill=RED, font=self.note_font)
            yy += line_h

    @staticmethod
    def draw_check(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
        pts = [(x, y + 32 * scale), (x + 18 * scale, y + 52 * scale), (x + 58 * scale, y)]
        draw.line(pts, fill=RED, width=max(4, int(5 * scale)), joint="curve")

    def draw_red_marks(self, draw: ImageDraw.ImageDraw, page_no: int) -> None:
        if page_no == 1:
            draw.ellipse((self.grid_x + 360, self.grid_y + 8, self.grid_x + 820, self.grid_y + 102), outline=RED2, width=5)
            self.draw_check(draw, self.grid_x - 70, self.grid_y + 250)
            draw.arc((self.grid_x + 20, self.grid_y + 225, self.grid_x + self.grid_w - 20, self.grid_y + self.cell_h * 5), start=5, end=175, fill=RED2, width=5)
        else:
            self.draw_check(draw, self.grid_x - 62, self.grid_y + 225)
            draw.arc((self.grid_x + 25, self.grid_y + 160, self.grid_x + self.grid_w - 10, self.grid_y + self.cell_h * 4), start=8, end=175, fill=RED2, width=5)

    def draw_page(self, page_no: int, paragraphs: list[str], comments: list[str]) -> Image.Image:
        img = Image.new("RGB", (A4_W, A4_H), BG)
        draw = ImageDraw.Draw(img)
        draw.rectangle((55, 55, A4_W - 55, A4_H - 55), outline=(232, 232, 222), width=3)
        self.draw_grid(draw, page_no)
        self.write_text(draw, page_no, paragraphs)
        self.draw_red_marks(draw, page_no)

        if comments:
            available_top = 395
            available_bottom = 2240 if self.page_count == 2 else 2350
            step = max(1, (available_bottom - available_top) // max(1, len(comments)))
            for i, comment in enumerate(comments):
                self.draw_note(draw, comment, available_top + i * step)

        img = ImageEnhance.Brightness(img).enhance(1.03)
        return ImageEnhance.Contrast(img).enhance(1.05)


def parse_rgb(value: str) -> tuple[int, int, int]:
    parts = [int(x.strip()) for x in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("RGB must be r,g,b")
    return tuple(parts)  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--text-file", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--basename", default="完整作文_宽版批注")
    parser.add_argument("--comments", default="")
    parser.add_argument("--pages", type=int, choices=[2, 3], default=2)
    parser.add_argument("--grid-rgb", type=parse_rgb, default=GRID_DEFAULT)
    parser.add_argument("--body-size", type=int, default=61)
    parser.add_argument("--note-size", type=int, default=61)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8")
    paragraphs = split_paragraphs(text)
    page_paragraphs = distribute_paragraphs(paragraphs, args.pages)
    comments = [c.strip() for c in args.comments.split("|") if c.strip()]
    page_comments = distribute_paragraphs(comments, args.pages)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    renderer = Renderer(args.title, args.pages, args.grid_rgb, args.body_size, args.note_size)

    images: list[Image.Image] = []
    for i, paras in enumerate(page_paragraphs, start=1):
        image = renderer.draw_page(i, paras, page_comments[i - 1] if i - 1 < len(page_comments) else [])
        path = args.out_dir / f"{args.basename}_page{i}.png"
        image.save(path, dpi=(300, 300))
        images.append(image)
        print(path)

    pdf_path = args.out_dir / f"{args.basename}_打印版.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=300.0)
    print(pdf_path)


if __name__ == "__main__":
    main()
