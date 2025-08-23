from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "numbers"
FONT_PATH = "arial.ttf"  
TARGET_PX_HEIGHT = 6     
SCALE_FACTOR = 6         

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load font at high-res size
font = ImageFont.truetype(FONT_PATH, TARGET_PX_HEIGHT * SCALE_FACTOR)

def create_number_image(text, filename):
    # Measure high-res text
    bbox = font.getbbox(text)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Draw at high res
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0], -bbox[1]), text, font=font, fill=(0,0,0,255))

    # Scale down to target pixel height
    scale = TARGET_PX_HEIGHT / height
    final_size = (int(width * scale), int(height * scale))
    img = img.resize(final_size, Image.LANCZOS)

    img.save(os.path.join(OUTPUT_DIR, filename), "PNG")

# Generate images 1–50 and 50+
for i in range(1, 51):
    create_number_image(str(i), f"{i}.png")
create_number_image("50+", "50plus.png")

print("Done")
