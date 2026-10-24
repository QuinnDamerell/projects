"""Build the site logo and favicons.

The mark is Inter SemiBold's Q, stretched to 115% width as in the original logo, scaled to 90%
and optically centered on a circle with the "Electric" diagonal gradient.

Usage (needs the Inter variable font, fontTools, numpy and Pillow):
    python design/logo/build_logo.py path/to/Inter-VariableFont_opsz,wght.ttf

Writes docs/assets/logo.svg, logo.png, logo.webp, apple-touch-icon.png and docs/favicon.ico.
"""
import sys
from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw

DOCS = Path(__file__).resolve().parents[2] / "docs"
GRADIENT = ("#8B6DFF", "#4A2AD4")  # top-left to bottom-right
CANVAS = 1000


def glyph_transform(units_per_em):
    # The original logo placed the Q with translate(131.51 798.02) scale(1.15 1) at 831.11px,
    # then this design shrinks it to 90% and nudges it up so the ring sits optically centered.
    s = 831.11 / units_per_em
    return (0.9 * 1.15 * s, 0, 0, -0.9 * s, 0.9 * 131.51 + 50, 0.9 * 798.02 + 43.97)


class ContourPen(BasePen):
    """Collects each contour as a flattened list of points."""

    def __init__(self, glyph_set, steps=32):
        super().__init__(glyph_set)
        self.contours, self.points, self.steps = [], [], steps

    def _moveTo(self, pt):
        self.points = [pt]

    def _lineTo(self, pt):
        self.points.append(pt)

    def _qCurveToOne(self, p1, p2):
        p0 = self.points[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            u = 1 - t
            self.points.append(tuple(u * u * a + 2 * u * t * b + t * t * c for a, b, c in zip(p0, p1, p2)))

    def _curveToOne(self, p1, p2, p3):
        p0 = self.points[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            u = 1 - t
            self.points.append(tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3)))

    def _closePath(self):
        self.contours.append(self.points)
        self.points = []

    _endPath = _closePath


def load_q(font_path):
    font = instantiateVariableFont(TTFont(font_path), {"wght": 600, "opsz": 14})
    glyph_set = font.getGlyphSet()
    glyph = glyph_set[font.getBestCmap()[ord("Q")]]
    transform = glyph_transform(font["head"].unitsPerEm)

    svg_pen = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    glyph.draw(TransformPen(svg_pen, transform))
    contour_pen = ContourPen(glyph_set)
    glyph.draw(TransformPen(contour_pen, transform))
    return svg_pen.getCommands(), contour_pen.contours


def signed_area(points):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1])) / 2


def coverage(size, supersample, contours=None, circle=False):
    """Anti-aliased coverage in [0, 1], filled with the nonzero winding rule."""
    big = size * supersample
    scale = big / CANVAS
    if circle:
        mask = Image.new("L", (big, big), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=1)
        filled = np.asarray(mask, dtype=bool)
    else:
        winding = np.zeros((big, big), dtype=np.int16)
        for points in contours:
            mask = Image.new("L", (big, big), 0)
            ImageDraw.Draw(mask).polygon([(x * scale, y * scale) for x, y in points], fill=1)
            winding += np.where(np.asarray(mask) > 0, 1 if signed_area(points) > 0 else -1, 0).astype(np.int16)
        filled = winding != 0
    return filled.reshape(size, supersample, size, supersample).mean(axis=(1, 3))


def render(size, contours, round_tile=True):
    supersample = max(4, 512 // size)
    centers = (np.arange(size) + 0.5) / size
    t = (centers[None, :] + centers[:, None]) / 2  # diagonal position, 0 at top-left, 1 at bottom-right
    start, end = (np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32) for c in GRADIENT)
    color = start * (1 - t[..., None]) + end * t[..., None]

    q = coverage(size, supersample, contours)[..., None]
    color = color * (1 - q) + 255 * q
    alpha = coverage(size, supersample, circle=True) if round_tile else np.ones((size, size))
    rgba = np.dstack([color, alpha[..., None] * 255])
    return Image.fromarray(np.clip(np.rint(rgba), 0, 255).astype(np.uint8), "RGBA")


def main():
    path_data, contours = load_q(sys.argv[1])
    assets = DOCS / "assets"

    (assets / "logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">\n'
        "  <title>Quinn Damerell</title>\n"
        '  <defs>\n'
        f'    <linearGradient id="qd-logo" x1="0" y1="0" x2="1000" y2="1000" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{GRADIENT[0]}"/><stop offset="1" stop-color="{GRADIENT[1]}"/></linearGradient>\n'
        "  </defs>\n"
        '  <circle cx="500" cy="500" r="500" fill="url(#qd-logo)"/>\n'
        f'  <path fill="#fff" d="{path_data}"/>\n'
        "</svg>\n",
        encoding="utf-8",
    )

    logo = render(1000, contours)
    logo.save(assets / "logo.png", optimize=True)
    logo.save(assets / "logo.webp", quality=92, method=6)

    # iOS masks home-screen icons itself and fills transparency with black, so this one is full bleed.
    render(180, contours, round_tile=False).save(assets / "apple-touch-icon.png", optimize=True)

    icons = [render(s, contours) for s in (48, 32, 16)]
    icons[0].save(DOCS / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)], append_images=icons[1:])


if __name__ == "__main__":
    main()
