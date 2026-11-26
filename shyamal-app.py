import functools
import io
import math
import os
import re
from datetime import datetime

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Set page config
st.set_page_config(
    page_title="Shyamal's Wedding Invitation Card Generator",
    page_icon="💍",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Wedding details
# ---------------------------------------------------------------------------
groom_name = "Shyamal Roy"
bride_name = "Tropa Rani Shill"
groom_parents = "Gouranga Chandra Roy & Jharna Rani Roy"
invocation = "SHREE SHREE GANESHAYA NAMAH"
blessing = "By the grace of the Almighty, a beautiful new beginning."
invitation = "joyfully invite you to the wedding of their beloved younger son"
closing_note = "Your presence and blessings will make our joy complete."
wedding_date = datetime(2026, 12, 11)  # Shubho Bibaho
reception_date = datetime(2026, 12, 13)
reception_time = "8:00 PM"  # Dinner
venue_name = "Grand Prince Chinese Restaurant"
venue_address = "Mirpur-1, Dhaka"

# ---------------------------------------------------------------------------
# Rendering setup
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DESIGN_W, DESIGN_H = 800, 1100  # layout grid, in design units
RENDER_SCALE = 4  # draw at 4x so ornaments are smooth after downsampling
OUTPUT_SCALE = 2  # final card is 1600 x 2200 px

GOLD_LIGHT = (250, 228, 160)
GOLD = (218, 178, 92)
GOLD_DEEP = (150, 104, 38)

THEMES = {
    "Royal maroon & gold": {
        "style": "royal",
        "caption": "Maroon & gold with a marigold garland",
        "region": (150, 1036),  # invocation centre .. lotus base, in design units
        "text": (247, 236, 218),
        "soft_text": (234, 214, 188),
        "heading": (228, 190, 106),
        "greeting": (242, 216, 150),
        "names": "foil",
        "accent": (214, 174, 88),
    },
    "Classic floral": {
        "style": "floral",
        "caption": "Soft pink watercolour florals",
        "region": (165, 958),  # invocation centre .. venue address centre
        "text": (50, 50, 50),
        "soft_text": (50, 50, 50),
        "heading": (120, 40, 60),
        "greeting": (50, 50, 50),
        "names": (120, 40, 60),
        "accent": (180, 150, 100),
    },
}


def load_font(filename, size):
    """Load a bundled font, falling back the same way groom-app.py does."""
    try:
        return ImageFont.truetype(os.path.join(SCRIPT_DIR, filename), size)
    except IOError:
        try:
            return ImageFont.truetype("Times New Roman", size)
        except IOError:
            return ImageFont.load_default(size=size)


def ordinal(n):
    """11 -> '11th', 22 -> '22nd'."""
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_event_date(date):
    """datetime(2026, 12, 11) -> ('Friday', '11th December 2026')."""
    return date.strftime("%A"), f"{ordinal(date.day)} {date.strftime('%B %Y')}"


class Painter:
    """Draws in 800 x 1100 design units onto a canvas scaled by `k`.
    With dry=True nothing is drawn: used to measure a layout before placing it."""

    def __init__(self, image, k, dry=False):
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self.k = k
        self.dry = dry

    def s(self, value):
        return value * self.k

    def pt(self, x, y):
        return (x * self.k, y * self.k)

    def font(self, filename, size):
        return load_font(filename, round(size * self.k))

    def textlength(self, text, font):
        return self.draw.textlength(text, font=font) / self.k

    def text(self, x, y, text, font, fill, anchor="mm"):
        if self.dry:
            return
        self.draw.text(self.pt(x, y), text, font=font, fill=fill, anchor=anchor)

    def line(self, points, fill, width=1):
        if self.dry:
            return
        self.draw.line(
            [self.pt(x, y) for x, y in points],
            fill=fill,
            width=max(1, round(width * self.k)),
            joint="curve",
        )

    def polygon(self, points, fill=None, outline=None, width=1):
        if self.dry:
            return
        self.draw.polygon(
            [self.pt(x, y) for x, y in points],
            fill=fill,
            outline=outline,
            width=max(1, round(width * self.k)),
        )

    def circle(self, x, y, r, fill=None, outline=None, width=1):
        if self.dry:
            return
        self.draw.ellipse(
            [self.pt(x - r, y - r), self.pt(x + r, y + r)],
            fill=fill,
            outline=outline,
            width=max(1, round(width * self.k)),
        )

    def rectangle(self, x0, y0, x1, y1, outline, width=1):
        if self.dry:
            return
        self.draw.rectangle(
            [self.pt(x0, y0), self.pt(x1, y1)],
            outline=outline,
            width=max(1, round(width * self.k)),
        )


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------
def wrap_text(p, text, font, max_width):
    """Wrap text into the fewest lines that fit max_width, with evenly balanced
    line lengths so no paragraph ends on a single stranded word."""
    words = text.split()

    def greedy(width):
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if not current or p.textlength(trial, font) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    line_count = len(greedy(max_width))
    low, high = 1, max_width
    while low < high:
        mid = (low + high) // 2
        if len(greedy(mid)) <= line_count:
            high = mid
        else:
            low = mid + 1
    return greedy(low)


def draw_centered_lines(p, center_x, y, lines, font, fill, line_height):
    for line in lines:
        p.text(center_x, y, line, font, fill)
        y += line_height
    return y


def draw_spaced_text(p, center_x, y, text, font, fill, spacing):
    """Draw letter-spaced text centred on center_x; returns its total width."""
    widths = [p.textlength(ch, font) for ch in text]
    total_width = sum(widths) + spacing * (len(text) - 1)
    x = center_x - total_width / 2
    for ch, width in zip(text, widths):
        p.text(x, y, ch, font, fill, anchor="lm")
        x += width + spacing
    return total_width


def draw_foil_text(p, x, y, text, font):
    """Gold-foil text: a soft shadow, then a vertical gold gradient through the
    glyph mask."""
    if p.dry:
        return
    box = [round(v) for v in p.draw.textbbox(p.pt(x, y), text, font=font, anchor="mm")]
    pad = round(p.s(6))
    left, top = box[0] - pad, box[1] - pad
    width, height = box[2] - box[0] + 2 * pad, box[3] - box[1] + 2 * pad

    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).text(
        (p.s(x) - left, p.s(y) - top), text, font=font, fill=255, anchor="mm"
    )

    shadow = mask.filter(ImageFilter.GaussianBlur(p.s(1.6)))
    offset = round(p.s(1.5))
    p.image.paste((34, 4, 12), (left + offset, top + offset), shadow)

    stops = [(0.0, GOLD_LIGHT), (0.42, GOLD), (0.55, (255, 236, 176)), (1.0, GOLD_DEEP)]
    t = np.linspace(0, 1, height)
    column = np.stack(
        [np.interp(t, [s for s, _ in stops], [c[i] for _, c in stops]) for i in range(3)],
        axis=1,
    )
    gradient = np.repeat(column[:, None, :], width, axis=1).astype("uint8")
    p.image.paste(Image.fromarray(gradient, "RGB"), (left, top), mask)


# ---------------------------------------------------------------------------
# Ornaments (royal theme)
# ---------------------------------------------------------------------------
def petal(cx, cy, angle, r0, length, width, steps=18):
    """Lens-shaped petal pointing outwards from (cx, cy) at `angle`."""
    ca, sa = math.cos(angle), math.sin(angle)
    left, right = [], []
    for i in range(steps + 1):
        u = i / steps
        r = r0 + u * length
        w = (width / 2) * math.sin(math.pi * u) ** 0.8
        px, py = cx + ca * r, cy + sa * r
        left.append((px - sa * w, py + ca * w))
        right.append((px + sa * w, py - ca * w))
    return left + right[::-1]


def royal_background(width, height):
    """Deep maroon radial gradient (computed small, then smoothly enlarged)."""
    sw, sh = 200, 275
    y, x = np.mgrid[0:sh, 0:sw].astype("float32")
    d = np.sqrt(((x - sw / 2) / (sw * 0.72)) ** 2 + ((y - sh * 0.46) / (sh * 0.62)) ** 2)
    d = np.clip(d, 0, 1)[..., None] ** 1.35
    inner = np.array([132, 26, 46], dtype="float32")
    outer = np.array([54, 5, 17], dtype="float32")
    small = (inner + (outer - inner) * d).astype("uint8")
    return Image.fromarray(small, "RGB").resize((width, height), Image.BICUBIC)


def draw_mandala_watermark(p, cx, cy, radius, color, alpha):
    """Faint line-art mandala on its own layer, blended onto the card."""
    size = round(p.s(radius * 2 + 8))
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    lp = Painter(layer, p.k)
    c = radius + 4
    stroke = (*color, alpha)
    for ring_r in (0.12, 0.40, 0.72, 0.97):
        lp.circle(c, c, radius * ring_r, outline=stroke, width=1)
    for n, r0, length, w in ((8, 0.12, 0.26, 0.16), (16, 0.40, 0.30, 0.11), (32, 0.72, 0.24, 0.07)):
        for i in range(n):
            a = 2 * math.pi * i / n + (math.pi / n if n == 16 else 0)
            lp.polygon(petal(c, c, a, radius * r0, radius * length, radius * w), outline=stroke, width=1)
    for i in range(48):
        a = 2 * math.pi * i / 48
        lp.circle(c + math.cos(a) * radius * 0.68, c + math.sin(a) * radius * 0.68, 2.2, fill=stroke)
    p.image.paste(layer, (round(p.s(cx - c)), round(p.s(cy - c))), layer)


MARIGOLD_COLORS = [
    ((206, 92, 14), (238, 126, 28), (252, 168, 58)),  # orange
    ((222, 148, 8), (248, 188, 36), (255, 222, 104)),  # yellow
]


def draw_marigold(p, x, y, r, variant):
    dark, main, light = MARIGOLD_COLORS[variant % 2]
    for i in range(12):
        a = 2 * math.pi * i / 12
        p.circle(x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55, r * 0.48, fill=dark)
    p.circle(x, y, r * 0.78, fill=main)
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.3
        p.circle(x + math.cos(a) * r * 0.32, y + math.sin(a) * r * 0.32, r * 0.36, fill=light)
    p.circle(x, y, r * 0.2, fill=dark)


def draw_leaf(p, x, y, angle, length, width):
    p.polygon(petal(x, y, angle, 0, length, width), fill=(52, 116, 54), outline=(30, 78, 36), width=0.8)
    p.line(
        [(x, y), (x + math.cos(angle) * length * 0.9, y + math.sin(angle) * length * 0.9)],
        fill=(108, 168, 92),
        width=0.6,
    )


def draw_bell(p, x, y):
    p.circle(x, y - 6, 2.2, fill=GOLD)
    p.polygon(petal(x, y - 4, math.pi / 2, 0, 12, 11), fill=GOLD, outline=GOLD_DEEP, width=0.6)
    p.circle(x, y + 8, 1.8, fill=GOLD_LIGHT)


def draw_strand(p, x, y_top, count, spacing, r):
    for i in range(count):
        draw_marigold(p, x, y_top + i * spacing, r, i)
    end = y_top + (count - 1) * spacing
    draw_leaf(p, x - 1, end + r * 0.6, math.pi / 2 + 0.55, 15, 7)
    draw_leaf(p, x + 1, end + r * 0.6, math.pi / 2 - 0.55, 15, 7)
    draw_bell(p, x, end + r + 12)


def draw_garland(p):
    """Marigold toran: mango leaves, swags across the top and strands down the
    sides."""
    left, right, top = 46, DESIGN_W - 46, 46
    for i in range(23):  # mango leaves hanging from the top rail
        x = left + 6 + i * (right - left - 12) / 22
        draw_leaf(p, x, top - 4, math.pi / 2 + (0.18 if i % 2 else -0.18), 24, 9)

    anchors = np.linspace(left, right, 7)
    for a, b in zip(anchors[:-1], anchors[1:]):
        count = 11
        for i in range(count):
            u = i / (count - 1)
            draw_marigold(p, a + (b - a) * u, top + 36 * math.sin(math.pi * u), 8.5, i)
    for x in anchors[1:-1]:
        draw_strand(p, x, top + 2, 3, 13, 8)
    for x in (anchors[0], anchors[-1]):
        draw_strand(p, x, top + 2, 17, 13.5, 8.5)


def draw_rosette(p, x, y, r):
    for i in range(8):
        p.polygon(petal(x, y, 2 * math.pi * i / 8, r * 0.15, r * 0.85, r * 0.5), fill=GOLD, outline=GOLD_DEEP, width=0.6)
    p.circle(x, y, r * 0.28, fill=GOLD_LIGHT, outline=GOLD_DEEP, width=0.6)


def draw_lotus(p, x, y):
    """Gold lotus with a flourished rule, sitting above the bottom frame."""
    for side in (-1, 1):
        p.line([(x + side * 62, y), (x + side * 230, y)], fill=GOLD, width=1.2)
        for d in (90, 150, 210):
            p.circle(x + side * d, y, 2.6, fill=GOLD_LIGHT)
        p.polygon(petal(x + side * 236, y, 0 if side > 0 else math.pi, 0, 14, 8), fill=GOLD)
    for angle, length, width in ((-70, 30, 20), (-35, 40, 22), (0, 48, 24)):
        for sign in ((1,) if angle == 0 else (1, -1)):
            a = math.radians(-90 + sign * angle)
            p.polygon(
                petal(x, y + 4, a, 0, length, width),
                fill=(124, 22, 40),
                outline=GOLD,
                width=1.4,
            )
    p.polygon(petal(x, y + 4, -math.pi / 2, 0, 30, 12), fill=GOLD, outline=GOLD_DEEP, width=0.8)
    p.line([(x - 34, y + 5), (x + 34, y + 5)], fill=GOLD, width=1.6)


def draw_royal_frame(p):
    gold_line = (214, 174, 88)
    p.rectangle(28, 28, DESIGN_W - 28, DESIGN_H - 28, outline=gold_line, width=2.2)
    p.rectangle(38, 38, DESIGN_W - 38, DESIGN_H - 38, outline=gold_line, width=0.9)
    draw_rosette(p, 38, DESIGN_H - 38, 15)
    draw_rosette(p, DESIGN_W - 38, DESIGN_H - 38, 15)


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=len(THEMES))
def card_base(theme_name):
    """Background, frame and ornaments: identical for every guest, so built
    once per theme and reused."""
    theme = THEMES[theme_name]
    k = RENDER_SCALE
    size = (DESIGN_W * k, DESIGN_H * k)

    if theme["style"] == "royal":
        base = royal_background(*size)
    else:
        try:
            base = Image.open(os.path.join(SCRIPT_DIR, "floral_background.png")).convert("RGB").resize(size, Image.LANCZOS)
        except FileNotFoundError:
            base = Image.new("RGB", size, (240, 240, 240))
    p = Painter(base, k)

    if theme["style"] == "royal":
        draw_mandala_watermark(p, DESIGN_W / 2, 560, 270, GOLD, 34)
        draw_royal_frame(p)
        draw_garland(p)
    else:
        p.rectangle(60, 60, DESIGN_W - 60, DESIGN_H - 60, outline=theme["accent"], width=2)
    return base


@functools.lru_cache(maxsize=None)
def fonts(k):
    """All fonts used on the card, at render scale (loaded once)."""
    f = lambda name, size: load_font(name, round(size * k))  # noqa: E731
    return {
        "invocation": f("Lora-Bold.ttf", 21),
        "blessing": f("Lora-Italic.ttf", 21),
        "hosts": f("Lora-Regular.ttf", 25),
        "invite": f("Lora-Italic.ttf", 21),
        "with": f("Lora-Italic.ttf", 23),
        "names": f("GreatVibes-Regular.ttf", 58),
        "closing": f("Lora-Italic.ttf", 21),
        "heading": f("Lora-Bold.ttf", 19),
        "detail": f("Lora-Regular.ttf", 21),
        "venue": f("Lora-Regular.ttf", 25),
    }


def greeting_layout(p, guest_name):
    """Font and lines for "Dear <guest>": shrinks for long names, then wraps."""
    greeting = f"Dear {guest_name}"
    size = 44
    font = p.font("GreatVibes-Regular.ttf", size)
    while size > 32 and p.textlength(greeting, font) > 590:
        size -= 2
        font = p.font("GreatVibes-Regular.ttf", size)
    return font, wrap_text(p, greeting, font, 590)


def compose(p, guest_name, theme, y):
    """Lay out every line of text from y downwards; returns the last line's y.
    Run once on a dry Painter to measure, then for real at the centred position."""
    f = fonts(p.k)
    cx = DESIGN_W / 2
    text, soft, heading, accent = theme["text"], theme["soft_text"], theme["heading"], theme["accent"]

    # ॥ SHREE SHREE GANESHAYA NAMAH ॥  (dandas drawn: the fonts have no Devanagari)
    width = draw_spaced_text(p, cx, y, invocation, f["invocation"], heading, 3)
    cap_top, cap_bottom = (v / p.k for v in f["invocation"].getbbox("H", anchor="lm")[1::2])
    mid, half = y + (cap_top + cap_bottom) / 2, (cap_bottom - cap_top) / 2 + 3
    for side in (-1, 1):
        dx = cx + side * (width / 2 + 22)
        for offset in (-4, 4):
            p.line([(dx + offset, mid - half), (dx + offset, mid + half)], heading, 2)
    y += 46

    lines = wrap_text(p, f"“{blessing}”", f["blessing"], 590)
    y = draw_centered_lines(p, cx, y, lines, f["blessing"], soft, 28) + 30

    if guest_name:
        font, lines = greeting_layout(p, guest_name)
        y = draw_centered_lines(p, cx, y, lines, font, theme["greeting"], 38) + 16

    p.text(cx, y, groom_parents, f["hosts"], text)
    y += 32
    lines = wrap_text(p, invitation, f["invite"], 600)
    y = draw_centered_lines(p, cx, y, lines, f["invite"], soft, 28) + 40

    for i, name in enumerate((groom_name, bride_name)):
        if theme["names"] == "foil":
            draw_foil_text(p, cx, y, name, f["names"])
        else:
            p.text(cx, y, name, f["names"], theme["names"])
        if i == 0:
            y += 50
            p.text(cx, y, "with", f["with"], theme["greeting"])
            y += 52
    y += 60

    lines = wrap_text(p, closing_note, f["closing"], 590)
    y = draw_centered_lines(p, cx, y, lines, f["closing"], soft, 28) + 8

    # thin rule with a diamond
    p.line([(cx - 130, y), (cx - 10, y)], accent, 1)
    p.line([(cx + 10, y), (cx + 130, y)], accent, 1)
    p.polygon([(cx, y - 5), (cx + 5, y), (cx, y + 5), (cx - 5, y)], fill=accent)
    y += 40

    # Shubho Bibaho (left) | Reception (right); weekdays come from the dates
    left_x, right_x = cx - 140, cx + 140
    wedding_lines = list(format_event_date(wedding_date))
    reception_lines = list(format_event_date(reception_date)) + [f"Dinner: {reception_time}"]
    draw_spaced_text(p, left_x, y, "SHUBHO BIBAHO", f["heading"], heading, 2)
    draw_spaced_text(p, right_x, y, "RECEPTION", f["heading"], heading, 2)
    line_height = 28
    p.line([(cx, y - 8), (cx, y + 31 + line_height * (len(reception_lines) - 1) + 8)], accent, 1)
    y += 31
    draw_centered_lines(p, left_x, y, wedding_lines, f["detail"], text, line_height)
    y = draw_centered_lines(p, right_x, y, reception_lines, f["detail"], text, line_height) + 22

    draw_spaced_text(p, cx, y, "VENUE", f["heading"], heading, 2)
    y += 33
    p.text(cx, y, venue_name, f["venue"], text)
    y += 31
    p.text(cx, y, venue_address, f["detail"], soft)
    return y


LOTUS_GAP = 64  # royal template: lotus base sits this far below the last line


def generate_card(guest_name, theme_name="Royal maroon & gold"):
    theme = THEMES[theme_name]
    card = card_base(theme_name).copy()

    # Measure, then centre the whole block in the template's free area
    top, bottom = theme["region"]
    extra = LOTUS_GAP if theme["style"] == "royal" else 0
    height = compose(Painter(card, RENDER_SCALE, dry=True), guest_name, theme, 0) + extra
    y0 = top + max(0, (bottom - top - height) / 2)

    p = Painter(card, RENDER_SCALE)
    y_end = compose(p, guest_name, theme, y0)
    if theme["style"] == "royal":
        draw_lotus(p, DESIGN_W / 2, min(1036, y_end + LOTUS_GAP))

    return card.resize((DESIGN_W * OUTPUT_SCALE, DESIGN_H * OUTPUT_SCALE), Image.LANCZOS)


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
# Lora and Great Vibes cover Latin script only (incl. accents); Bangla etc. would
# print as empty boxes, so such names are caught before generating.
ALLOWED_EXTRA = set("‘’“”–—·•")


def clean_name(raw):
    return " ".join(raw.split())


def unsupported_chars(name):
    return sorted({c for c in name if ord(c) > 0x24F and c not in ALLOWED_EXTRA})


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "guest"


@st.cache_data(show_spinner=False, max_entries=16)
def render_card_files(guest_name, theme_name):
    """Card as a full-size PNG (download) and a light JPEG (on-screen preview).
    Cached, so regenerating a name or re-running after a download is instant."""
    card = generate_card(guest_name, theme_name)
    png = io.BytesIO()
    card.save(png, format="PNG", compress_level=6)
    preview = io.BytesIO()
    card.resize((800, 1100), Image.LANCZOS).save(preview, format="JPEG", quality=88)
    return png.getvalue(), preview.getvalue()


st.title("💍 Shyamal's Wedding Invitation Card Generator")
st.markdown("Type a guest's name, pick a template, and download a personalized card.")

with st.form("card_form", border=False):
    guest_input = st.text_input("Guest Name", placeholder="e.g. Mr. Rahim Uddin", max_chars=80)
    template = st.radio(
        "Template",
        list(THEMES),
        captions=[t["caption"] for t in THEMES.values()],
        horizontal=True,
    )
    submitted = st.form_submit_button("Generate Card", type="primary", use_container_width=True)

if submitted:
    name = clean_name(guest_input)
    bad = unsupported_chars(name)
    if not name:
        st.warning("Please enter the guest name to generate a personalized card.")
    elif bad:
        st.warning(
            "Please type the name in English letters. The card's fonts can't draw: "
            + " ".join(bad)
        )
    else:
        with st.spinner("Designing the card..."):
            png, preview = render_card_files(name, template)
        st.session_state["card"] = {"guest": name, "template": template, "png": png, "preview": preview}

card = st.session_state.get("card")
if card:
    st.download_button(
        "⬇️ Download PNG",
        card["png"],
        file_name=f"shyamal_wedding_invitation_{safe_filename(card['guest'])}.png",
        mime="image/png",
        type="primary",
        use_container_width=True,
        key="download_png",
    )
    st.image(card["preview"], caption=f"{card['guest']} · {card['template']}", use_column_width=True)

# Footer
st.markdown("---")
st.markdown("💕 Create beautiful personalized wedding invitation cards in seconds!")
