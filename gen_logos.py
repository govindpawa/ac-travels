from PIL import Image, ImageDraw, ImageFont
import os

out = "/Users/govindpawar/Plt/ac-travels/images/clients"

def create_logo(filename, texts, colors, bg=(255,255,255,0)):
    img = Image.new('RGBA', (400, 160), bg)
    draw = ImageDraw.Draw(img)

    try:
        font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
        font_reg = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        font_bold = ImageFont.load_default()
        font_reg = ImageFont.load_default()

    y_offset = 20
    for text, color, is_bold, size in texts:
        try:
            f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            f = font_bold if is_bold else font_reg
        draw.text((20, y_offset), text, fill=color, font=f)
        y_offset += size + 10

    # Draw shapes if needed
    if 'shapes' in colors:
        for shape in colors['shapes']:
            shape(draw)

    img.save(os.path.join(out, filename))
    print(f"Created {filename}")

# Pluto Rides - Green theme
img = Image.new('RGBA', (400, 160), (255,255,255,0))
draw = ImageDraw.Draw(img)
# Green rounded square icon
draw.rounded_rectangle([15, 30, 95, 110], radius=18, fill=(100, 200, 100))
# P letter in icon
try:
    icon_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
    main_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
except:
    icon_font = ImageFont.load_default()
    main_font = ImageFont.load_default()
draw.text((38, 35), "P", fill=(255,255,255), font=icon_font)
draw.text((110, 45), "Pluto", fill=(100, 200, 100), font=main_font)
img.save(os.path.join(out, "pluto-rides.png"))
print("Created pluto-rides.png")

# Diligent - Red theme
img = Image.new('RGBA', (400, 160), (255,255,255,0))
draw = ImageDraw.Draw(img)
# Red D shape
draw.pieslice([10, 20, 100, 130], start=270, end=90, fill=(220, 50, 50))
draw.pieslice([30, 40, 90, 110], start=270, end=90, fill=(180, 40, 40))
try:
    main_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
except:
    main_font = ImageFont.load_default()
draw.text((110, 45), "Diligent", fill=(30, 30, 30), font=main_font)
img.save(os.path.join(out, "diligent.png"))
print("Created diligent.png")

# OpenText - Blue theme
img = Image.new('RGBA', (400, 160), (255,255,255,0))
draw = ImageDraw.Draw(img)
# Blue rounded square with "ot"
draw.rounded_rectangle([15, 35, 85, 105], radius=15, fill=(20, 40, 100))
try:
    icon_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    main_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
except:
    icon_font = ImageFont.load_default()
    main_font = ImageFont.load_default()
draw.text((23, 43), "ot", fill=(255,255,255), font=icon_font)
draw.text((100, 40), "opentext", fill=(20, 40, 100), font=main_font)
img.save(os.path.join(out, "opentext.png"))
print("Created opentext.png")

# Operations Insights - Blue/Orange theme
img = Image.new('RGBA', (400, 160), (255,255,255,0))
draw = ImageDraw.Draw(img)
# Chart bars icon
draw.rectangle([20, 80, 38, 120], fill=(26, 54, 93))
draw.rectangle([44, 55, 62, 120], fill=(246, 173, 85))
draw.rectangle([68, 35, 86, 120], fill=(26, 54, 93))
try:
    main_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
except:
    main_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()
draw.text((100, 40), "Operations", fill=(26, 54, 93), font=main_font)
draw.text((100, 80), "Insights", fill=(246, 173, 85), font=sub_font)
img.save(os.path.join(out, "operations-insights.png"))
print("Created operations-insights.png")
