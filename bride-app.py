# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import base64
# from datetime import datetime

# # Set page config
# st.set_page_config(
#     page_title="Mobasshir's Wedding Reception Card Generator",
#     page_icon="💍",
#     layout="centered",
# )

# # App title and description
# st.title("💍 Mobasshir's Wedding Reception Card Generator")
# st.markdown(
#     "Generate a personalized wedding reception card by entering the guest's name below."
# )

# # Only take guest name as input
# guest_name = st.text_input("Guest Name", placeholder="Enter guest's name")

# # Set default values for other fields
# bride_name = "Samira Rahman Eva"
# groom_name = "Mobasshir Bhuiya Shagor"
# bride_parents = "Hafizur Rahman & Shilpy Begum"
# groom_parents = "Ishaque Bhuiyan & Sheikh Hazera Begum"
# wedding_date = datetime(2025, 4, 25)
# wedding_day = "FRIDAY"
# wedding_time = "2:00 PM"
# venue_name = "Grand Darbar Restaurant & Party Center"
# venue_address = "Delwar Complex, 26 Hatkhola Road (1st Floor), Tikatuli, Dhaka-1203"
# rsvp_contact = "01712821193, 01913315151"

# def generate_card(
#     guest_name,
#     bride_name,
#     groom_name,
#     bride_parents,
#     groom_parents,
#     wedding_date,
#     wedding_day,
#     wedding_time,
#     venue_name,
#     venue_address,
#     rsvp_contact,
# ):
#     # Create a blank card (vertical format)
#     card_width, card_height = 800, 1100

#     # Load floral background image (ensure you have the correct floral image file)
#     try:
#         floral_bg = Image.open("floral_background_01.png").resize(
#             (card_width, card_height)
#         )
#     except FileNotFoundError:
#         floral_bg = Image.new("RGB", (card_width, card_height), (240, 240, 240))

#     card = floral_bg.copy()
#     draw = ImageDraw.Draw(card)

#     # Try to load fonts
#     try:
#         small_font = ImageFont.truetype("Lora-Regular.ttf", 20)  # Reduced from 24
#         regular_font = ImageFont.truetype("Lora-Regular.ttf", 24)  # Reduced from 28
#         names_font = ImageFont.truetype("GreatVibes-Regular.ttf", 42)  # Reduced from 48
#         title_font = ImageFont.truetype("Lora-Regular.ttf", 26)  # Reduced from 30
#         date_font = ImageFont.truetype("Lora-Regular.ttf", 40)  # Reduced from 48
#         script_font = ImageFont.truetype("GreatVibes-Regular.ttf", 48)  # Reduced from 54
#         guest_font = ImageFont.truetype("Lora-Regular.ttf", 30)  # Reduced from 36
#         bismillah_font = ImageFont.truetype("Lora-Regular.ttf", 34)  # Reduced from 40
#     except IOError:
#         small_font = ImageFont.truetype("Times New Roman", 20)
#         regular_font = ImageFont.truetype("Times New Roman", 24)
#         names_font = ImageFont.truetype("Times New Roman", 42)
#         title_font = ImageFont.truetype("Times New Roman", 26)
#         date_font = ImageFont.truetype("Times New Roman", 40)
#         script_font = ImageFont.truetype("Times New Roman", 48)
#         guest_font = ImageFont.truetype("Times New Roman", 30)
#         bismillah_font = ImageFont.truetype("Times New Roman", 34)

#     # Draw border rectangle
#     border_margin = 60  # Increased from 50 to provide more padding
#     border_color = (180, 150, 100)  # Soft gold
#     draw.rectangle(
#         [
#             (border_margin, border_margin),
#             (card_width - border_margin, card_height - border_margin),
#         ],
#         outline=border_color,
#         width=2,
#     )

#     # Format date
#     formatted_date = wedding_date.strftime("%d")
#     formatted_month = wedding_date.strftime("%B")
#     formatted_year = wedding_date.strftime("%Y")

#     # Text color
#     text_color = (50, 50, 50)  # Soft charcoal gray
#     highlight_color = (120, 40, 60)  # Muted burgundy

#     y_position = 200  # Start slightly higher to fit content

#     # Bismillah Text
#     bismillah_transliteration = "Bismillahir Rahmanir Raheem"
#     draw.text(
#         (card_width / 2, y_position),
#         bismillah_transliteration,
#         font=bismillah_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 50  # Reduced from 60

#     # Islamic opening
#     subtitle = "In the Name of Almighty Allah,"
#     subtitle2 = "The most Gracious & the most Merciful"
#     draw.text(
#         (card_width / 2, y_position),
#         subtitle,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     draw.text(
#         (card_width / 2, y_position),
#         subtitle2,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 40  # Reduced from 60

#     # Guest Greeting
#     if guest_name:
#         guest_greeting = f"Dear {guest_name}"
#         draw.text(
#             (card_width / 2, y_position),
#             guest_greeting,
#             font=guest_font,
#             fill=text_color,
#             anchor="mm",
#         )
#         y_position += 50  # Reduced from 60

#     # Parents invitation text
#     invitation_text = f"{groom_parents}, with great joy,"
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     invitation_text2 = (
#         "cordially invite you to honor them with your presence & blessings"
#     )
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text2,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     invitation_text3 = "at the wedding reception of their younger son"
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text3,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Bride and Groom names
#     y_position += 50  # Reduced from 70
#     draw.text(
#         (card_width / 2, y_position),
#         groom_name,
#         font=names_font,
#         fill=highlight_color,
#         anchor="mm",
#     )
#     y_position += 40  # Reduced from 60
#     draw.text(
#         (card_width / 2, y_position), "&", font=title_font, fill=text_color, anchor="mm"
#     )
#     y_position += 40  # Reduced from 60
#     draw.text(
#         (card_width / 2, y_position),
#         bride_name,
#         font=names_font,
#         fill=highlight_color,
#         anchor="mm",
#     )

#     # Bride's parents
#     y_position += 40  # Reduced from 60
#     draw.text(
#         (card_width / 2, y_position),
#         "beloved daughter of",
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     draw.text(
#         (card_width / 2, y_position),
#         bride_parents,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Save the Date
#     y_position += 70  # Reduced from 90
#     draw.text(
#         (card_width / 2, y_position),
#         "Save the Date",
#         font=script_font,
#         fill=highlight_color,
#         anchor="mm",
#     )

#     # Date display
#     y_position += 60  # Reduced from 80
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_month,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 50  # Reduced from 60

#     # Day of week with underline
#     day_x = card_width / 2 - 150
#     draw.text(
#         (day_x, y_position),
#         wedding_day,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     draw.line(
#         [(day_x - 50, y_position + 15), (day_x + 50, y_position + 15)],
#         fill=text_color,
#         width=1,
#     )

#     # Day number
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_date,
#         font=date_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Time with underline
#     time_x = card_width / 2 + 150
#     draw.text(
#         (time_x, y_position),
#         f"at {wedding_time}",
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     draw.line(
#         [(time_x - 50, y_position + 15), (time_x + 50, y_position + 15)],
#         fill=text_color,
#         width=1,
#     )

#     # Year
#     y_position += 40  # Reduced from 60
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_year,
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Venue
#     y_position += 40  # Reduced from 60
#     draw.text(
#         (card_width / 2, y_position),
#         "Venue:",
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     draw.text(
#         (card_width / 2, y_position),
#         venue_name,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30  # Reduced from 35
#     draw.text(
#         (card_width / 2, y_position),
#         venue_address,
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # RSVP - Removed to fit content (optional, can be re-added if needed)
#     # y_position += 60
#     # draw.text(
#     #     (card_width / 2, y_position),
#     #     "RSVP:",
#     #     font=regular_font,
#     #     fill=text_color,
#     #     anchor="mm",
#     # )
#     # y_position += 35
#     # draw.text(
#     #     (card_width / 2, y_position),
#     #     rsvp_contact,
#     #     font=regular_font,
#     #     fill=text_color,
#     #     anchor="mm",
#     # )

#     return card

# def get_image_download_link(img, filename, text):
#     buffered = io.BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     href = (
#         f'<a href="data:image/png;base64,{img_str}" download="{filename}">💾 {text}</a>'
#     )
#     return href

# # Generate card button
# if st.button("Generate Card", type="primary"):
#     if not guest_name:
#         st.warning("Please enter the guest name to generate a personalized card.")
#     else:
#         # Generate the card
#         card = generate_card(
#             guest_name,
#             bride_name,
#             groom_name,
#             bride_parents,
#             groom_parents,
#             wedding_date,
#             wedding_day,
#             wedding_time,
#             venue_name,
#             venue_address,
#             rsvp_contact,
#         )

#         # Display the card
#         st.subheader("Your Wedding Reception Card")
#         st.image(card, use_column_width=True)

#         # Download link
#         st.markdown(
#             get_image_download_link(
#                 card,
#                 f"wedding_invitation_{guest_name.replace(' ', '_')}.png",
#                 "Download Wedding Card",
#             ),
#             unsafe_allow_html=True,
#         )

#         st.success("Card generated successfully! Click the link above to download.")

# # Footer
# st.markdown("---")
# st.markdown(
#     "💕 Create beautiful personalized Islamic wedding reception cards in seconds!"
# )







# import streamlit as st
# from PIL import Image, ImageDraw, ImageFont
# import io
# import base64
# from datetime import datetime

# # Set page config
# st.set_page_config(
#     page_title="Samira's Wedding Ceremony Card Generator",
#     page_icon="💍",
#     layout="centered",
# )

# # App title and description
# st.title("💍 Samiras's Wedding Ceremony Card Generator")
# st.markdown(
#     "Generate a personalized wedding ceremony card by entering the guest's name below."
# )

# # Only take guest name as input
# guest_name = st.text_input("Guest Name", placeholder="Enter guest's name")

# # Set default values for other fields
# bride_name = "Samira Rahman Eva"
# groom_name = "Mobasshir Bhuiya Shagor"
# bride_parents = "Hafizur Rahman & Shilpy Begum"
# groom_parents = "Ishaque Bhuiyan & Sheikh Hazera Begum"
# wedding_date = datetime(2025, 4, 18)
# wedding_day = "FRIDAY"
# wedding_time = "8:30 PM"
# venue_name = "Grand Buffet Taj Convention Center"
# venue_address = "Rankin Street, Wari, Dhaka-1203"
# rsvp_contact = "01711854797, 01970707001"

# def generate_card(
#     guest_name,
#     bride_name,
#     groom_name,
#     bride_parents,
#     groom_parents,
#     wedding_date,
#     wedding_day,
#     wedding_time,
#     venue_name,
#     venue_address,
#     rsvp_contact,
# ):
#     # Create a blank card (vertical format)
#     card_width, card_height = 800, 1100

#     # Load floral background image (ensure you have the correct floral image file)
#     try:
#         floral_bg = Image.open("floral_background_01.png").resize(
#             (card_width, card_height)
#         )
#     except FileNotFoundError:
#         floral_bg = Image.new("RGB", (card_width, card_height), (240, 240, 240))

#     card = floral_bg.copy()
#     draw = ImageDraw.Draw(card)

#     # Try to load fonts
#     try:
#         small_font = ImageFont.truetype("Lora-Regular.ttf", 20)
#         regular_font = ImageFont.truetype("Lora-Regular.ttf", 24)
#         names_font = ImageFont.truetype("GreatVibes-Regular.ttf", 42)
#         title_font = ImageFont.truetype("Lora-Regular.ttf", 26)
#         date_font = ImageFont.truetype("Lora-Regular.ttf", 40)
#         script_font = ImageFont.truetype("GreatVibes-Regular.ttf", 48)
#         guest_font = ImageFont.truetype("Lora-Regular.ttf", 30)
#         bismillah_font = ImageFont.truetype("Lora-Regular.ttf", 34)
#     except IOError:
#         small_font = ImageFont.truetype("Times New Roman", 20)
#         regular_font = ImageFont.truetype("Times New Roman", 24)
#         names_font = ImageFont.truetype("Times New Roman", 42)
#         title_font = ImageFont.truetype("Times New Roman", 26)
#         date_font = ImageFont.truetype("Times New Roman", 40)
#         script_font = ImageFont.truetype("Times New Roman", 48)
#         guest_font = ImageFont.truetype("Times New Roman", 30)
#         bismillah_font = ImageFont.truetype("Times New Roman", 34)

#     # Draw border rectangle
#     border_margin = 60
#     border_color = (180, 150, 100)  # Soft gold
#     draw.rectangle(
#         [
#             (border_margin, border_margin),
#             (card_width - border_margin, card_height - border_margin),
#         ],
#         outline=border_color,
#         width=2,
#     )

#     # Format date
#     formatted_date = wedding_date.strftime("%d")
#     formatted_month = wedding_date.strftime("%B")
#     formatted_year = wedding_date.strftime("%Y")

#     # Text color
#     text_color = (50, 50, 50)  # Soft charcoal gray
#     highlight_color = (120, 40, 60)  # Muted burgundy

#     y_position = 200  # Start position

#     # Bismillah Text
#     bismillah_transliteration = "Bismillahir Rahmanir Raheem"
#     draw.text(
#         (card_width / 2, y_position),
#         bismillah_transliteration,
#         font=bismillah_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 50

#     # Islamic opening
#     subtitle = "In the Name of Almighty Allah,"
#     subtitle2 = "The most Gracious & the most Merciful"
#     draw.text(
#         (card_width / 2, y_position),
#         subtitle,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     draw.text(
#         (card_width / 2, y_position),
#         subtitle2,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 40

#     # Guest Greeting
#     if guest_name:
#         guest_greeting = f"Dear {guest_name}"
#         draw.text(
#             (card_width / 2, y_position),
#             guest_greeting,
#             font=guest_font,
#             fill=text_color,
#             anchor="mm",
#         )
#         y_position += 50

#     # Parents invitation text - Updated to bride's parents
#     invitation_text = f"{bride_parents}, with great joy,"
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     invitation_text2 = (
#         "cordially invite you to honor them with your presence & blessings"
#     )
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text2,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     invitation_text3 = "at the wedding reception of their beloved daughter"
#     draw.text(
#         (card_width / 2, y_position),
#         invitation_text3,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Bride and Groom names
#     y_position += 50
#     draw.text(
#         (card_width / 2, y_position),
#         bride_name,  # Bride's name first
#         font=names_font,
#         fill=highlight_color,
#         anchor="mm",
#     )
#     y_position += 40
#     draw.text(
#         (card_width / 2, y_position), "&", font=title_font, fill=text_color, anchor="mm"
#     )
#     y_position += 40
#     draw.text(
#         (card_width / 2, y_position),
#         groom_name,  # Groom's name second
#         font=names_font,
#         fill=highlight_color,
#         anchor="mm",
#     )

#     # Groom's parents (equivalent to "beloved daughter of" section)
#     y_position += 40
#     draw.text(
#         (card_width / 2, y_position),
#         "younger son of",
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     draw.text(
#         (card_width / 2, y_position),
#         groom_parents,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Save the Date
#     # y_position += 70
#     # draw.text(
#     #     (card_width / 2, y_position),
#     #     "Save the Date",
#     #     font=script_font,
#     #     fill=highlight_color,
#     #     anchor="mm",
#     # )

#     # Date display
#     y_position += 50
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_month,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 40

#     # Day of week with underline
#     day_x = card_width / 2 - 150
#     draw.text(
#         (day_x, y_position),
#         wedding_day,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     draw.line(
#         [(day_x - 50, y_position + 15), (day_x + 50, y_position + 15)],
#         fill=text_color,
#         width=1,
#     )

#     # Day number
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_date,
#         font=date_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Time with underline
#     time_x = card_width / 2 + 150
#     draw.text(
#         (time_x, y_position),
#         f"at {wedding_time}",
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     draw.line(
#         [(time_x - 50, y_position + 15), (time_x + 50, y_position + 15)],
#         fill=text_color,
#         width=1,
#     )

#     # Year
#     y_position += 40
#     draw.text(
#         (card_width / 2, y_position),
#         formatted_year,
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # Venue
#     y_position += 50
#     draw.text(
#         (card_width / 2, y_position),
#         "Venue:",
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     draw.text(
#         (card_width / 2, y_position),
#         venue_name,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 30
#     draw.text(
#         (card_width / 2, y_position),
#         venue_address,
#         font=small_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     # RSVP - Kept commented out as in the original code
#     y_position += 50
#     draw.text(
#         (card_width / 2, y_position),
#         "RSVP:",
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )
#     y_position += 35
#     draw.text(
#         (card_width / 2, y_position),
#         rsvp_contact,
#         font=regular_font,
#         fill=text_color,
#         anchor="mm",
#     )

#     return card

# def get_image_download_link(img, filename, text):
#     buffered = io.BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     href = (
#         f'<a href="data:image/png;base64,{img_str}" download="{filename}">💾 {text}</a>'
#     )
#     return href

# # Generate card button
# if st.button("Generate Card", type="primary"):
#     if not guest_name:
#         st.warning("Please enter the guest name to generate a personalized card.")
#     else:
#         # Generate the card
#         card = generate_card(
#             guest_name,
#             bride_name,
#             groom_name,
#             bride_parents,
#             groom_parents,
#             wedding_date,
#             wedding_day,
#             wedding_time,
#             venue_name,
#             venue_address,
#             rsvp_contact,
#         )

#         # Display the card
#         st.subheader("Your Wedding Ceremony Card")
#         st.image(card, use_column_width=True)

#         # Download link
#         st.markdown(
#             get_image_download_link(
#                 card,
#                 f"wedding_invitation_{guest_name.replace(' ', '_')}.png",
#                 "Download Wedding Ceremony Card",
#             ),
#             unsafe_allow_html=True,
#         )

#         st.success("Card generated successfully! Click the link above to download.")

# # Footer
# st.markdown("---")
# st.markdown(
#     "💕 Create beautiful personalized wedding ceremony cards in seconds!"
# )


import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Samira's Wedding Ceremony Card Generator",
    page_icon="💍",
    layout="centered",
)

# App title and description
st.title("💍 Samira's Wedding Ceremony Card Generator")
st.markdown(
    "Generate a personalized wedding ceremony card by entering the guest's name below."
)

# Only take guest name as input
guest_name = st.text_input("Guest Name", placeholder="Enter guest's name")

# Set default values for other fields
bride_name = "Samira Rahman Eva"
groom_name = "Mobasshir Bhuiya Shagor"
bride_parents = "Hafizur Rahman & Shilpy Begum"
groom_parents = "Ishaque Bhuiyan & Sheikh Hazera Begum"
wedding_date = datetime(2025, 4, 18)
wedding_day = "FRIDAY"
wedding_time = "8:30 PM"
venue_name = "Grand Buffet Taj Convention Center"
venue_address = "Rankin Street, Wari, Dhaka-1203"
rsvp_contact = "01711854797, 01970707001"

def generate_card(
    guest_name,
    bride_name,
    groom_name,
    bride_parents,
    groom_parents,
    wedding_date,
    wedding_day,
    wedding_time,
    venue_name,
    venue_address,
    rsvp_contact,
):
    # Create a blank card (vertical format)
    card_width, card_height = 800, 1100

    # Load floral background image
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        floral_bg = Image.open(os.path.join(script_dir, "floral_background_01.png")).resize(
            (card_width, card_height)
        )
    except FileNotFoundError:
        floral_bg = Image.new("RGB", (card_width, card_height), (240, 240, 240))

    card = floral_bg.copy()
    draw = ImageDraw.Draw(card)

    # Try to load fonts with absolute paths
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        small_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 20)
        regular_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 24)
        names_font = ImageFont.truetype(os.path.join(script_dir, "GreatVibes-Regular.ttf"), 42)
        title_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 26)
        date_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 40)
        script_font = ImageFont.truetype(os.path.join(script_dir, "GreatVibes-Regular.ttf"), 48)
        guest_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 30)
        bismillah_font = ImageFont.truetype(os.path.join(script_dir, "Lora-Regular.ttf"), 34)
    except IOError:
        try:
            small_font = ImageFont.truetype("Times New Roman", 20)
            regular_font = ImageFont.truetype("Times New Roman", 24)
            names_font = ImageFont.truetype("Times New Roman", 42)
            title_font = ImageFont.truetype("Times New Roman", 26)
            date_font = ImageFont.truetype("Times New Roman", 40)
            script_font = ImageFont.truetype("Times New Roman", 48)
            guest_font = ImageFont.truetype("Times New Roman", 30)
            bismillah_font = ImageFont.truetype("Times New Roman", 34)
        except IOError:
            small_font = ImageFont.load_default()
            regular_font = ImageFont.load_default()
            names_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            date_font = ImageFont.load_default()
            script_font = ImageFont.load_default()
            guest_font = ImageFont.load_default()
            bismillah_font = ImageFont.load_default()

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

    # Format date
    formatted_date = wedding_date.strftime("%d")
    formatted_month = wedding_date.strftime("%B")
    formatted_year = wedding_date.strftime("%Y")

    # Text color
    text_color = (50, 50, 50)
    highlight_color = (120, 40, 60)

    y_position = 200

    # Bismillah Text
    bismillah_transliteration = "Bismillahir Rahmanir Raheem"
    draw.text(
        (card_width / 2, y_position),
        bismillah_transliteration,
        font=bismillah_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 50

    # Islamic opening
    subtitle = "In the Name of Almighty Allah,"
    subtitle2 = "The most Gracious & the most Merciful"
    draw.text(
        (card_width / 2, y_position),
        subtitle,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    draw.text(
        (card_width / 2, y_position),
        subtitle2,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 40

    # Guest Greeting
    if guest_name:
        guest_greeting = f"Dear {guest_name}"
        draw.text(
            (card_width / 2, y_position),
            guest_greeting,
            font=guest_font,
            fill=text_color,
            anchor="mm",
        )
        y_position += 50

    # Parents invitation text - Updated to bride's parents
    invitation_text = f"{bride_parents}, with great joy,"
    draw.text(
        (card_width / 2, y_position),
        invitation_text,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    invitation_text2 = (
        "cordially invite you to honor them with your presence & blessings"
    )
    draw.text(
        (card_width / 2, y_position),
        invitation_text2,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    invitation_text3 = "at the wedding reception of their beloved daughter"
    draw.text(
        (card_width / 2, y_position),
        invitation_text3,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )

    # Bride and Groom names
    y_position += 50
    draw.text(
        (card_width / 2, y_position),
        bride_name,
        font=names_font,
        fill=highlight_color,
        anchor="mm",
    )
    y_position += 40
    draw.text(
        (card_width / 2, y_position), "&", font=title_font, fill=text_color, anchor="mm"
    )
    y_position += 40
    draw.text(
        (card_width / 2, y_position),
        groom_name,
        font=names_font,
        fill=highlight_color,
        anchor="mm",
    )

    # Groom's parents
    y_position += 40
    draw.text(
        (card_width / 2, y_position),
        "younger son of",
        font=small_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    draw.text(
        (card_width / 2, y_position),
        groom_parents,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )

    # Date display
    y_position += 50
    draw.text(
        (card_width / 2, y_position),
        formatted_month,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 40

    # Day of week with underline
    day_x = card_width / 2 - 150
    draw.text(
        (day_x, y_position),
        wedding_day,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    draw.line(
        [(day_x - 50, y_position + 15), (day_x + 50, y_position + 15)],
        fill=text_color,
        width=1,
    )

    # Day number
    draw.text(
        (card_width / 2, y_position),
        formatted_date,
        font=date_font,
        fill=text_color,
        anchor="mm",
    )

    # Time with underline
    time_x = card_width / 2 + 150
    draw.text(
        (time_x, y_position),
        f"at {wedding_time}",
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    draw.line(
        [(time_x - 50, y_position + 15), (time_x + 50, y_position + 15)],
        fill=text_color,
        width=1,
    )

    # Year
    y_position += 40
    draw.text(
        (card_width / 2, y_position),
        formatted_year,
        font=small_font,
        fill=text_color,
        anchor="mm",
    )

    # Venue
    y_position += 50
    draw.text(
        (card_width / 2, y_position),
        "Venue:",
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    draw.text(
        (card_width / 2, y_position),
        venue_name,
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 30
    draw.text(
        (card_width / 2, y_position),
        venue_address,
        font=small_font,
        fill=text_color,
        anchor="mm",
    )

    # RSVP
    y_position += 50
    draw.text(
        (card_width / 2, y_position),
        "RSVP:",
        font=regular_font,
        fill=text_color,
        anchor="mm",
    )
    y_position += 35
    draw.text(
        (card_width / 2, y_position),
        rsvp_contact,
        font=regular_font,
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
            bride_name,
            groom_name,
            bride_parents,
            groom_parents,
            wedding_date,
            wedding_day,
            wedding_time,
            venue_name,
            venue_address,
            rsvp_contact,
        )

        # Display the card
        st.subheader("Your Wedding Ceremony Card")
        st.image(card, use_column_width=True)

        # Download link
        st.markdown(
            get_image_download_link(
                card,
                f"wedding_invitation_{guest_name.replace(' ', '_')}.png",
                "Download Wedding Ceremony Card",
            ),
            unsafe_allow_html=True,
        )

        st.success("Card generated successfully! Click the link above to download.")

# Footer
st.markdown("---")
st.markdown(
    "💕 Create beautiful personalized wedding ceremony cards in seconds!"
)