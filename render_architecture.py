#!/usr/bin/env python3
"""Render solution architecture diagrams from JSON input.

Usage:
  python render_architecture.py --input examples/sample_input.json --output outputs/sample_architecture.png

This renderer intentionally uses simple shapes and layout patterns rather than copying
any proprietary reference artwork. Extend TEMPLATE_RENDERERS to add more specialized layouts.
"""
from __future__ import annotations

import argparse
import json
import math
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple, Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
REFERENCE_PATH = ROOT / "data" / "reference_architecture_patterns.json"


def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


FONT = {
    "title": load_font(34, True),
    "subtitle": load_font(18),
    "h1": load_font(21, True),
    "h2": load_font(15, True),
    "body": load_font(13),
    "small": load_font(11),
    "tiny": load_font(9),
}


def hex_to_rgb(x: str) -> Tuple[int, int, int]:
    x = x.strip().lstrip("#")
    return tuple(int(x[i:i+2], 16) for i in (0, 2, 4))


def lighten(hex_color: str, factor: float = 0.86) -> Tuple[int, int, int]:
    r, g, b = hex_to_rgb(hex_color)
    return (int(r + (255-r)*factor), int(g + (255-g)*factor), int(b + (255-b)*factor))


def wrap_text(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=False))


def centered_text(draw: ImageDraw.ImageDraw, box, text, font, fill="#222222", line_spacing=4):
    x, y, w, h = box
    lines = str(text).split("\n")
    heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_h = sum(heights) + line_spacing * (len(lines)-1)
    cy = y + (h-total_h)/2
    for line, lh in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (w-tw)/2, cy), line, font=font, fill=fill)
        cy += lh + line_spacing


def arrow(draw, start, end, fill="#444444", width=3, label=None, label_font=None):
    x1, y1 = start; x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    ang = math.atan2(y2-y1, x2-x1)
    size = 13
    p1 = (x2 - size*math.cos(ang-math.pi/6), y2 - size*math.sin(ang-math.pi/6))
    p2 = (x2 - size*math.cos(ang+math.pi/6), y2 - size*math.sin(ang+math.pi/6))
    draw.polygon([(x2, y2), p1, p2], fill=fill)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        font = label_font or FONT["tiny"]
        txt = wrap_text(label, 18)
        bbox = draw.multiline_textbbox((0,0), txt, font=font, spacing=2)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.rounded_rectangle((mx-tw/2-5, my-th/2-4, mx+tw/2+5, my+th/2+4), radius=4, fill="#FFFFFF", outline="#CBD5E1")
        draw.multiline_text((mx-tw/2, my-th/2), txt, font=font, fill="#111827", spacing=2, align="center")


def draw_icon(draw, cx, cy, r, color, label=""):
    # simple neutral architecture-icon substitute: circle + three connected dots
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=color, width=3, fill="#FFFFFF")
    for dx, dy in [(-r*0.35, 0), (r*0.28, -r*0.28), (r*0.28, r*0.28)]:
        draw.ellipse((cx+dx-3, cy+dy-3, cx+dx+3, cy+dy+3), fill=color)
    draw.line((cx-r*0.35, cy, cx+r*0.28, cy-r*0.28), fill=color, width=2)
    draw.line((cx-r*0.35, cy, cx+r*0.28, cy+r*0.28), fill=color, width=2)


def draw_lane(draw, x, y, w, h, title, items, palette, side="left"):
    draw.rounded_rectangle((x, y, x+w, y+h), radius=14, fill="#FFFFFF", outline="#CBD5E1", width=2)
    centered_text(draw, (x+10, y+8, w-20, 28), title, FONT["h2"], fill=palette["primary"])
    item_h = min(58, (h-60) / max(1, len(items)))
    cy = y + 48
    for item in items:
        draw_icon(draw, x+30, cy+item_h/2, 13, palette["primary"])
        draw.text((x+52, cy+item_h/2-8), wrap_text(item, 16), font=FONT["small"], fill="#111827")
        cy += item_h


def draw_zone(draw, x, y, w, h, zone, palette):
    fill = lighten(zone.get("color", palette["primary"]), 0.84)
    draw.rounded_rectangle((x, y, x+w, y+h), radius=16, fill=fill, outline="#D0D7E2", width=1)
    draw_icon(draw, x+w/2, y+55, 24, zone.get("color", palette["primary"]))
    centered_text(draw, (x+12, y+88, w-24, 25), wrap_text(zone.get("title", "Capability"), 22), FONT["h2"], fill="#111827")
    if zone.get("subtitle"):
        centered_text(draw, (x+12, y+114, w-24, 26), wrap_text(zone["subtitle"], 26), FONT["small"], fill="#4B5563")
    items = zone.get("items", [])[:8]
    if items:
        item_y = y + 155
        chip_w = (w - 34) / 2 if len(items) > 3 else w - 30
        for i, item in enumerate(items):
            col = i % (2 if len(items) > 3 else 1)
            row = i // (2 if len(items) > 3 else 1)
            cx = x + 15 + col*(chip_w+8)
            cy = item_y + row*31
            draw.rounded_rectangle((cx, cy, cx+chip_w, cy+24), radius=6, fill="#FFFFFF", outline="#CBD5E1")
            centered_text(draw, (cx+4, cy+2, chip_w-8, 18), wrap_text(item, 18), FONT["tiny"], fill="#1F2937")


def render_platform_value_chain(spec: Dict[str, Any], refs: Dict[str, Any]) -> Image.Image:
    defaults = refs["canvas_defaults"]
    W = int(spec.get("style", {}).get("width", defaults["width"]))
    H = int(spec.get("style", {}).get("height", defaults["height"]))
    img = Image.new("RGB", (W, H), defaults["background"])
    draw = ImageDraw.Draw(img)
    template = next(t for t in refs["templates"] if t["id"] == "platform_value_chain")
    palette = template["default_palette"] | spec.get("style", {}).get("palette", {})

    centered_text(draw, (0, 28, W, 45), spec.get("title", "Solution Architecture"), FONT["title"], fill=palette["primary"])
    if spec.get("subtitle"):
        centered_text(draw, (0, 76, W, 28), spec["subtitle"], FONT["subtitle"], fill="#374151")

    # side lanes
    lanes = spec.get("lanes", [])
    left_items = next((l.get("items", []) for l in lanes if l.get("side") == "left"), ["Files", "Databases", "Applications", "Real-time"])
    right_items = next((l.get("items", []) for l in lanes if l.get("side") == "right"), ["Reports", "AI apps", "Business apps", "Automation"])
    draw_lane(draw, 30, 225, 150, 430, "Inputs", left_items, palette, "left")
    draw_lane(draw, W-180, 225, 150, 430, "Outputs", right_items, palette, "right")

    main_x, main_y, main_w, main_h = 205, 195, W-410, 520
    draw.rounded_rectangle((main_x, main_y, main_x+main_w, main_y+main_h), radius=24, fill="#FFFFFF", outline=palette["primary"], width=3)

    # ribbons
    ribbons = ["Low-code", "Collaborative user experience", "Open, flexible, and extensible"]
    rx = main_x + 55
    for i, r in enumerate(ribbons):
        rw = [230, 330, 350][i]
        draw.rounded_rectangle((rx, main_y-22, rx+rw, main_y+18), radius=18, fill="#111111")
        centered_text(draw, (rx, main_y-18, rw, 27), r, FONT["body"], fill="#FFFFFF")
        rx += rw + 95

    zones = spec.get("zones", [])
    if not zones:
        zones = [{"id":"a", "title":"Capability", "items":[]}]
    gap = 22
    top_y = main_y + 60
    band_h = 300
    zone_w = (main_w - 60 - gap*(len(zones)-1)) / len(zones)
    zone_positions = {}
    x = main_x + 30
    for z in zones:
        z["color"] = z.get("color", palette["primary"])
        draw_zone(draw, x, top_y, zone_w, band_h, z, palette)
        zone_positions[z.get("id", z.get("title"))] = (x, top_y, zone_w, band_h)
        x += zone_w + gap

    # arrows between zones
    for i in range(len(zones)-1):
        a = zone_positions[zones[i].get("id", zones[i].get("title"))]
        b = zone_positions[zones[i+1].get("id", zones[i+1].get("title"))]
        arrow(draw, (a[0]+a[2]+4, a[1]+a[3]/2), (b[0]-5, b[1]+b[3]/2), fill="#111111", width=3)

    # operations band
    ops = spec.get("operations", ["User management and single sign-on", "Workflow automation", "ModelOps", "Audit"])
    op_y = main_y + main_h - 105
    draw.rounded_rectangle((main_x+30, op_y, main_x+main_w-30, op_y+70), radius=0, fill="#E5EDF8")
    centered_text(draw, (main_x+30, op_y+8, main_w-60, 22), "Operations", FONT["h2"], fill="#111827")
    centered_text(draw, (main_x+35, op_y+34, main_w-70, 22), "  |  ".join(ops), FONT["body"], fill="#374151")

    # side arrows
    arrow(draw, (180, 430), (main_x-5, 430), fill="#444444", width=3)
    arrow(draw, (main_x+main_w+5, 430), (W-180, 430), fill="#444444", width=3)

    # footer
    footer = spec.get("footer", "Any public or private cloud")
    draw.rectangle((main_x-10, H-72, main_x+main_w+10, H-35), fill="#EFEFEF")
    centered_text(draw, (main_x, H-66, main_w, 22), footer, FONT["h2"], fill="#222222")
    return img


def render_generic(spec: Dict[str, Any], refs: Dict[str, Any]) -> Image.Image:
    # A flexible fallback: title + macro lanes + central grid, suitable for all patterns.
    spec = dict(spec)
    if spec.get("template") != "platform_value_chain":
        spec.setdefault("style", {})
        spec["style"].setdefault("palette", {})
        template = next((t for t in refs["templates"] if t["id"] == spec.get("template")), None)
        if template:
            spec["style"]["palette"] = template.get("default_palette", {}) | spec["style"].get("palette", {})
    return render_platform_value_chain(spec, refs)


def render(spec: Dict[str, Any]) -> Image.Image:
    refs = json.loads(REFERENCE_PATH.read_text())
    template = spec.get("template", "platform_value_chain")
    if template == "platform_value_chain":
        return render_platform_value_chain(spec, refs)
    return render_generic(spec, refs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input architecture specification JSON")
    ap.add_argument("--output", required=True, help="Output PNG path")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    img = render(spec)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
