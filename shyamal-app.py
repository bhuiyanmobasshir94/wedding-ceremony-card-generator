import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Shyamal's Wedding Invitation Card Generator",
    page_icon="💍",
    layout="centered",
)

# App title and description
st.title("💍 Shyamal's Wedding Invitation Card Generator")
st.markdown(
    "Generate a personalized wedding invitation card by entering the guest's name below."
)

# Only take guest name as input
guest_name = st.text_input("Guest Name", placeholder="Enter guest's name")

# Set default values for other fields
groom_name = "Shyamal Roy"
bride_name = "Tropa Rani Shill"
groom_parents = "Gouranga Chandra Roy & Jharna Rani Roy"
invocation = "SHREE SHREE GANESHAYA NAMAH"
blessing_quote = (
    "With the grace of the Almighty and His divine blessings, we are delighted "
    "to celebrate a beautiful new beginning in our family’s journey."
)
invitation = (
    f"We, {groom_parents}, cordially invite you to grace the auspicious "
    "occasion of the wedding ceremony of our beloved younger son"
)
closing_note = (
    "Your gracious presence, warm wishes, and heartfelt blessings will make "
    "this joyous occasion even more special and memorable for our family."
)
wedding_date = datetime(2026, 12, 11)  # Shubho Bibaho
reception_date = datetime(2026, 12, 13)
reception_time = "8:00 PM"  # Dinner
venue_name = "Grand Prince Chinese Restaurant"
venue_address = "Mirpur-1, Dhaka-1216, Bangladesh"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_font(filename, size):
    """Load a bundled font, falling back the same way groom-app.py does."""
    try:
        return ImageFont.truetype(os.path.join(SCRIPT_DIR, filename), size)
    except IOError:
        try:
            return ImageFont.truetype("Times New Roman", size)
        except IOError:
            return ImageFont.load_default()


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


def wrap_text(draw, text, font, max_width):
    """Wrap text into the fewest lines that fit max_width, with evenly balanced
    line lengths so no paragraph ends on a single stranded word."""
    words = text.split()

    def greedy(width):
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if not current or draw.textlength(trial, font=font) <= width:
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


def draw_centered_lines(draw, center_x, y, lines, font, fill, line_height):
    for line in lines:
        draw.text((center_x, y), line, font=font, fill=fill, anchor="mm")
        y += line_height
    return y


def draw_spaced_text(draw, center_x, y, text, font, fill, spacing):
    """Draw letter-spaced text centred on center_x; returns its total width."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total_width = sum(widths) + spacing * (len(text) - 1)
    x = center_x - total_width / 2
    for ch, width in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += width + spacing
    return total_width


def draw_double_danda(draw, center_x, y, height, fill):
    """Draw '॥' as two vertical strokes (the bundled fonts have no Devanagari)."""
    for offset in (-4, 4):
        draw.line(
            [(center_x + offset, y - height / 2), (center_x + offset, y + height / 2)],
            fill=fill,
            width=2,
        )


def draw_divider(draw, center_x, y, half_width, fill):
    """Thin gold rule with a small diamond in the middle."""
    draw.line([(center_x - half_width, y), (center_x - 10, y)], fill=fill, width=1)
    draw.line([(center_x + 10, y), (center_x + half_width, y)], fill=fill, width=1)
    draw.polygon(
        [(center_x, y - 5), (center_x + 5, y), (center_x, y + 5), (center_x - 5, y)],
        fill=fill,
    )


def generate_card(
    guest_name,
    groom_name,
    bride_name,
    invocation,
    blessing_quote,
    invitation,
    closing_note,
    wedding_date,
    reception_date,
    reception_time,
    venue_name,
    venue_address,
):
    # Create a blank card (vertical format)
    card_width, card_height = 800, 1100
    center_x = card_width / 2

    # Load floral background image
    try:
        floral_bg = Image.open(
            os.path.join(SCRIPT_DIR, "floral_background.png")
        ).resize((card_width, card_height))
    except FileNotFoundError:
        floral_bg = Image.new("RGB", (card_width, card_height), (240, 240, 240))

    card = floral_bg.copy()
    draw = ImageDraw.Draw(card)

    # Fonts
    invocation_font = load_font("Lora-Bold.ttf", 21)
    quote_font = load_font("Lora-Italic.ttf", 20)
    regular_font = load_font("Lora-Regular.ttf", 22)
    small_font = load_font("Lora-Regular.ttf", 20)
    with_font = load_font("Lora-Italic.ttf", 22)
    heading_font = load_font("Lora-Bold.ttf", 19)
    venue_font = load_font("Lora-Regular.ttf", 24)
    names_font = load_font("GreatVibes-Regular.ttf", 46)

    # Draw border rectangle
    border_margin = 60
    border_color = (180, 150, 100)  # Soft gold
    draw.rectangle(
        [
            (border_margin, border_margin),
            (card_width - border_margin, card_height - border_margin),
        ],
        outline=border_color,
        width=2,
    )

    # Text color
    text_color = (50, 50, 50)
    highlight_color = (120, 40, 60)

    y_position = 158

    # ॥ SHREE SHREE GANESHAYA NAMAH ॥
    text_width = draw_spaced_text(
        draw, center_x, y_position, invocation, invocation_font, highlight_color, 3
    )
    cap_top, cap_bottom = invocation_font.getbbox("H", anchor="lm")[1::2]
    danda_height = (cap_bottom - cap_top) + 6
    danda_y = y_position + (cap_top + cap_bottom) / 2
    danda_gap = 22
    draw_double_danda(
        draw, center_x - text_width / 2 - danda_gap, danda_y, danda_height, highlight_color
    )
    draw_double_danda(
        draw, center_x + text_width / 2 + danda_gap, danda_y, danda_height, highlight_color
    )
    y_position += 45

    # Blessing quote
    quote_lines = wrap_text(draw, f"“{blessing_quote}”", quote_font, 560)
    y_position = draw_centered_lines(
        draw, center_x, y_position, quote_lines, quote_font, text_color, 28
    )
    y_position += 30

    # Guest Greeting: shrinks for long names, then wraps rather than overflowing
    if guest_name:
        guest_greeting = f"Dear {guest_name}"
        max_width = 580
        size = 42
        greeting_font = load_font("GreatVibes-Regular.ttf", size)
        while (
            size > 32
            and draw.textlength(guest_greeting, font=greeting_font) > max_width
        ):
            size -= 2
            greeting_font = load_font("GreatVibes-Regular.ttf", size)
        greeting_lines = wrap_text(draw, guest_greeting, greeting_font, max_width)
        if len(greeting_lines) > 1:
            y_position -= 8  # keep a two-line greeting clear of the bottom flowers
        y_position = draw_centered_lines(
            draw, center_x, y_position, greeting_lines, greeting_font, text_color, 36
        )
        y_position += 16 if len(greeting_lines) == 1 else 6

    # Parents' invitation
    invitation_lines = wrap_text(draw, invitation, regular_font, 600)
    y_position = draw_centered_lines(
        draw, center_x, y_position, invitation_lines, regular_font, text_color, 30
    )
    y_position += 30

    # Groom and Bride names
    draw.text(
        (center_x, y_position),
        groom_name,
        font=names_font,
        fill=highlight_color,
        anchor="mm",
    )
    y_position += 42
    draw.text(
        (center_x, y_position), "with", font=with_font, fill=text_color, anchor="mm"
    )
    y_position += 42
    draw.text(
        (center_x, y_position),
        bride_name,
        font=names_font,
        fill=highlight_color,
        anchor="mm",
    )
    y_position += 52

    # Closing note
    closing_lines = wrap_text(draw, closing_note, small_font, 540)
    y_position = draw_centered_lines(
        draw, center_x, y_position, closing_lines, small_font, text_color, 28
    )
    y_position += 10

    draw_divider(draw, center_x, y_position, 130, border_color)
    y_position += 34

    # Events: Shubho Bibaho (left) and Reception (right), weekday derived from date
    left_x, right_x = center_x - 140, center_x + 140
    wedding_lines = list(format_event_date(wedding_date))
    reception_lines = list(format_event_date(reception_date)) + [
        f"Dinner: {reception_time}"
    ]
    draw_spaced_text(
        draw, left_x, y_position, "SHUBHO BIBAHO", heading_font, highlight_color, 2
    )
    draw_spaced_text(
        draw, right_x, y_position, "RECEPTION", heading_font, highlight_color, 2
    )
    line_height = 27
    draw.line(
        [
            (center_x, y_position - 8),
            (center_x, y_position + 30 + line_height * (len(reception_lines) - 1) + 8),
        ],
        fill=border_color,
        width=1,
    )
    y_position += 30
    draw_centered_lines(
        draw, left_x, y_position, wedding_lines, small_font, text_color, line_height
    )
    y_position = draw_centered_lines(
        draw, right_x, y_position, reception_lines, small_font, text_color, line_height
    )
    y_position += 18

    # Venue
    draw_spaced_text(draw, center_x, y_position, "VENUE", heading_font, highlight_color, 2)
    y_position += 32
    draw.text(
        (center_x, y_position),
        venue_name,
        font=venue_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    draw.text(
        (center_x, y_position),
        venue_address,
        font=small_font,
        fill=text_color,
        anchor="mm",
    )

    return card


def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = (
        f'<a href="data:image/png;base64,{img_str}" download="{filename}">💾 {text}</a>'
    )
    return href


# Generate card button
if st.button("Generate Card", type="primary"):
    if not guest_name:
        st.warning("Please enter the guest name to generate a personalized card.")
    else:
        # Generate the card
        card = generate_card(
            guest_name,
            groom_name,
            bride_name,
            invocation,
            blessing_quote,
            invitation,
            closing_note,
            wedding_date,
            reception_date,
            reception_time,
            venue_name,
            venue_address,
        )

        # Display the card
        st.subheader("Your Wedding Invitation Card")
        st.image(card, use_column_width=True)

        # Download link
        st.markdown(
            get_image_download_link(
                card,
                f"shyamal_wedding_invitation_{guest_name.replace(' ', '_')}.png",
                "Download Wedding Invitation Card",
            ),
            unsafe_allow_html=True,
        )

        st.success("Card generated successfully! Click the link above to download.")

# Footer
st.markdown("---")
st.markdown("💕 Create beautiful personalized wedding invitation cards in seconds!")
