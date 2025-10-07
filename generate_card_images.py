import json
import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    """
    Tries to load a series of common Chinese fonts.
    Falls back to Pillow's default font if none are found.
    """
    font_paths = [
        "SimHei.ttf",           # Windows (Simplified Chinese)
        "msyh.ttf",             # Windows (Microsoft YaHei)
        "PingFang.ttc",         # macOS
        "Arial Unicode MS.ttf", # Often available on various systems
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" # Linux (if Noto CJK is installed)
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except IOError:
            continue # Font not found, try the next one

    print("Warning: No common Chinese fonts found on the system.")
    print("Using Pillow's default font. Chinese characters may not render correctly.")
    return ImageFont.load_default()

def draw_text_center(draw, text, font, width, height, y_offset=0):
    """Draws text centered on the image with a vertical offset."""
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    x = (width - text_width) / 2
    y = ((height - text_height) / 2) + y_offset
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

def generate_taijitu_back(width, height, color_bg, color_light, color_dark, output_path):
    """Generates and saves a card back image with a correctly drawn Taijitu symbol."""
    img = Image.new('RGB', (width, height), color=color_bg)
    draw = ImageDraw.Draw(img)

    center_x, center_y = width / 2, height / 2
    radius = min(width, height) / 4.5 # Slightly smaller radius for better padding

    # 1. Draw the black half (as a pieslice)
    draw.pieslice([center_x - radius, center_y - radius, center_x + radius, center_y + radius], 90, 270, fill=color_dark)
    # 2. Draw the white half
    draw.pieslice([center_x - radius, center_y - radius, center_x + radius, center_y + radius], -90, 90, fill=color_light)

    # 3. Draw the S-curve illusion with two overlapping circles
    s_radius = radius / 2
    # Black upper circle
    draw.ellipse([center_x - s_radius, center_y - radius, center_x + s_radius, center_y], fill=color_dark)
    # White lower circle
    draw.ellipse([center_x - s_radius, center_y, center_x + s_radius, center_y + radius], fill=color_light)

    # 4. Draw the "eyes"
    eye_radius = s_radius / 4
    # White eye in black area
    draw.ellipse([center_x - eye_radius, center_y - s_radius - eye_radius, center_x + eye_radius, center_y - s_radius + eye_radius], fill=color_light)
    # Black eye in white area
    draw.ellipse([center_x - eye_radius, center_y + s_radius - eye_radius, center_x + eye_radius, center_y + s_radius + eye_radius], fill=color_dark)

    img.save(output_path)
    print(f"  - Saved new, correct Taijitu card back to {output_path}")


def generate_images():
    """
    Reads card data from cards.json and generates an image for each card.
    """
    # --- Configuration ---
    WIDTH, HEIGHT = 300, 500
    FONT_SIZE = 40

    COLOR_MAP = {
        "道之牌 (Path)": "#483D8B",
        "木 (Wood)": "#28a745",
        "火 (Fire)": "#dc3545",
        "土 (Earth)": "#8B4513",
        "金 (Metal)": "#6c757d",
        "水 (Water)": "#007bff",
        "Back": "#1a1a2e"
    }

    # --- Load Data ---
    try:
        with open('cards.json', 'r', encoding='utf-8') as f:
            cards_data = json.load(f)
    except FileNotFoundError:
        print("Error: cards.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode cards.json.")
        return

    # --- Create Image Directory ---
    if not os.path.exists('images'):
        os.makedirs('images')
        print("Created 'images' directory.")

    # --- Generate Card Images ---
    print(f"Generating {len(cards_data)} card images...")
    font = get_font(FONT_SIZE)

    for card in cards_data:
        card_name = card.get('name', 'Unknown')
        image_path = card.get('image')

        if not image_path:
            print(f"Warning: Skipping card '{card_name}' due to missing image path.")
            continue

        card_type = card.get('type')
        card_suit = card.get('suit')

        if card_type == "道之牌 (Path)":
            bg_color = COLOR_MAP["道之牌 (Path)"]
        elif card_suit in COLOR_MAP:
            bg_color = COLOR_MAP[card_suit]
        else:
            bg_color = "#000000"

        img = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
        draw = ImageDraw.Draw(img)

        chinese_name = card_name.split(' ')[0]
        draw_text_center(draw, chinese_name, font, WIDTH, HEIGHT)

        img.save(image_path)
        print(f"  - Saved {image_path}")

    # --- Generate New Card Back ---
    print("\nGenerating new card back...")
    generate_taijitu_back(WIDTH, HEIGHT, COLOR_MAP["Back"], "#FFFFFF", "#000000", "images/card_back.png")

    print("\nImage generation complete!")

if __name__ == '__main__':
    generate_images()