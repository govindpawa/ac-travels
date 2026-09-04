from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = landscape(A4)

DARK_BLUE = HexColor("#1a2a4a")
ORANGE = HexColor("#e89b3e")
LIGHT_BG = HexColor("#F0F4F8")
CARD_BG = HexColor("#F8F9FA")
DARK_GRAY = HexColor("#333333")
MID_GRAY = HexColor("#BBBBBB")
CARD_DARK = HexColor("#243a5e")

def draw_rect(c, x, y, w, h, color):
    c.setFillColor(color)
    c.rect(x, y, w, h, fill=1, stroke=0)

def draw_text(c, text, x, y, size=18, color=white, bold=False, align="left", max_width=None):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center" and max_width:
        lines = simpleSplit(text, font, size, max_width)
        for line in lines:
            tw = c.stringWidth(line, font, size)
            c.drawString(x + (max_width - tw) / 2, y, line)
            y -= size + 2
        return y
    elif max_width:
        lines = simpleSplit(text, font, size, max_width)
        for line in lines:
            c.drawString(x, y, line)
            y -= size + 2
        return y
    else:
        c.drawString(x, y, text)
        return y - size - 2

def draw_header(c, title):
    draw_rect(c, 0, H - 70, W, 70, DARK_BLUE)
    draw_text(c, title, 40, H - 48, size=28, color=white, bold=True)
    draw_rect(c, 40, H - 74, 180, 4, ORANGE)

# ========== PDF ==========
pdf_path = "/Users/govindpawar/Plt/ac-travels/KP_Travels_Vendor_Presentation.pdf"
c = canvas.Canvas(pdf_path, pagesize=landscape(A4))

# ===== SLIDE 1: Title =====
draw_rect(c, 0, 0, W, H, DARK_BLUE)
draw_rect(c, 0, H - 5, W, 5, ORANGE)
draw_rect(c, 0, 0, W, 5, ORANGE)

draw_text(c, "KP Travels", 0, H - 160, size=44, color=white, bold=True, align="center", max_width=W)
draw_text(c, "Bring the Happiness", 0, H - 220, size=28, color=ORANGE, align="center", max_width=W)
draw_rect(c, W/2 - 80, H - 240, 160, 3, ORANGE)
draw_text(c, "Your Trusted Partner for Safe & Comfortable Travel in Bangalore", 0, H - 275, size=16, color=white, align="center", max_width=W)
draw_text(c, "Phone: +91 99454 98275  |  Email: admin@actoursandtravels.com", 0, 100, size=13, color=MID_GRAY, align="center", max_width=W)
draw_text(c, "www.actoursandtravels.com", 0, 75, size=13, color=ORANGE, align="center", max_width=W)
c.showPage()

# ===== SLIDE 2: About Us =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "About KP Travels")

about = ("KP Travels Solutions Pvt. Ltd. is a trusted transportation service provider based in Bangalore. "
         "We specialize in providing safe, comfortable, and reliable travel solutions for "
         "individuals and corporate clients. Our team of professionally trained drivers ensures "
         "that every journey is smooth and pleasant.")
draw_text(c, about, 40, H - 120, size=13, color=DARK_GRAY, max_width=440)

# Key Highlights
draw_rect(c, 520, H - 330, 280, 250, LIGHT_BG)
draw_text(c, "Key Highlights", 540, H - 110, size=17, color=DARK_BLUE, bold=True)
highlights = ["Trained Professional Drivers", "Well-Maintained Vehicles", "Transparent Pricing",
              "On-time Service", "GPS Enabled Vehicles", "24/7 Customer Support"]
for i, h in enumerate(highlights):
    draw_text(c, f"✓  {h}", 540, H - 145 - i * 28, size=12, color=DARK_GRAY)

# Stats
stats = [("50+", "Professional Drivers"), ("1000+", "Happy Customers"), ("30+", "Vehicles"), ("5+", "Years Experience")]
for i, (num, label) in enumerate(stats):
    x = 40 + i * 120
    draw_rect(c, x, 40, 110, 100, DARK_BLUE)
    draw_text(c, num, x, 110, size=24, color=ORANGE, bold=True, align="center", max_width=110)
    draw_text(c, label, x, 80, size=9, color=white, align="center", max_width=110)
c.showPage()

# ===== SLIDE 3: Our Services =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "Our Services")

services = [
    ("Local Rentals", "Hourly and daily car rentals for city travel. Perfect for meetings, shopping, or personal errands."),
    ("Airport Transfer", "Punctual pickup and drop to Kempegowda International Airport."),
    ("Outstation Trips", "Travel to Mysore, Coorg, Ooty, Goa and more. One-way and round-trip packages."),
    ("Corporate Travel", "Employee transportation for IT companies. Dedicated fleet and monthly billing."),
    ("Wedding & Events", "Decorated cars for weddings, parties, and special occasions."),
    ("24/7 Support", "Book anytime, travel anytime. Support available round the clock."),
]

for i, (title, desc) in enumerate(services):
    row = i // 3
    col = i % 3
    x = 30 + col * 270
    y = H - 130 - row * 170

    draw_rect(c, x, y - 120, 255, 140, CARD_BG)
    draw_rect(c, x + 10, y - 5, 40, 8, ORANGE)
    draw_text(c, title, x + 10, y - 25, size=15, color=DARK_BLUE, bold=True)
    draw_text(c, desc, x + 10, y - 50, size=10, color=DARK_GRAY, max_width=230)
c.showPage()

# ===== SLIDE 4: Our Fleet =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "Our Fleet")

draw_text(c, "4 Seaters", 40, H - 100, size=20, color=ORANGE, bold=True)

four_seaters = [
    ("Maruti Swift / Dzire", "4 Seater | AC | Comfortable", "Best for City Travel"),
    ("Toyota Etios", "4 Seater | AC | Reliable", "Best for Airport & Outstation"),
]
for i, (name, spec, best) in enumerate(four_seaters):
    x = 40 + i * 250
    draw_rect(c, x, H - 245, 230, 115, LIGHT_BG)
    draw_text(c, name, x + 15, H - 155, size=14, color=DARK_BLUE, bold=True)
    draw_text(c, spec, x + 15, H - 178, size=11, color=DARK_GRAY)
    draw_text(c, best, x + 15, H - 200, size=11, color=ORANGE, bold=True)

draw_text(c, "7+ Seaters", 40, H - 275, size=20, color=ORANGE, bold=True)

seven_seaters = [
    ("Maruti Ertiga", "6-7 Seater | AC | Family Friendly", "Best for Family Trips"),
    ("Toyota Innova Crysta", "6-7 Seater | AC | Spacious", "Best for Groups & Outstation"),
    ("Tempo Traveller", "12-17 Seater | AC | Spacious", "Best for Large Groups & Tours"),
]
for i, (name, spec, best) in enumerate(seven_seaters):
    x = 40 + i * 270
    draw_rect(c, x, H - 420, 250, 115, LIGHT_BG)
    draw_text(c, name, x + 15, H - 330, size=14, color=DARK_BLUE, bold=True)
    draw_text(c, spec, x + 15, H - 353, size=11, color=DARK_GRAY)
    draw_text(c, best, x + 15, H - 375, size=11, color=ORANGE, bold=True)
c.showPage()

# ===== SLIDE 5: Why Choose Us =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "Why Choose Us")

reasons = [
    ("Punctuality", "We value your time. Our drivers arrive before scheduled pickup time."),
    ("Safety First", "Verified drivers, sanitized vehicles, and GPS tracking for every trip."),
    ("Best Prices", "Transparent pricing with no hidden charges. Competitive rates guaranteed."),
    ("24/7 Service", "Book anytime, travel anytime. We're available round the clock."),
]
for i, (title, desc) in enumerate(reasons):
    x = 40 + i * 200
    draw_rect(c, x, H - 310, 185, 210, DARK_BLUE)
    # Orange circle
    c.setFillColor(ORANGE)
    c.circle(x + 92, H - 140, 30, fill=1, stroke=0)
    draw_text(c, title, x, H - 195, size=16, color=white, bold=True, align="center", max_width=185)
    draw_text(c, desc, x + 10, H - 225, size=10, color=MID_GRAY, max_width=165)

# Tagline
draw_rect(c, 40, 60, W - 80, 60, CARD_BG)
draw_text(c, "\"We don't just provide rides, we deliver experiences.\"", 40, 85, size=16, color=DARK_BLUE, align="center", max_width=W - 80)
c.showPage()

# ===== SLIDE 6: Popular Destinations =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "Popular Destinations")

destinations = [
    ("Mysore", "Heritage palaces, royal city — ~150 km"),
    ("Coorg", "Coffee plantations, waterfalls — ~260 km"),
    ("Ooty", "Hill station, scenic beauty — ~270 km"),
    ("Goa", "Beaches, nightlife, churches — ~560 km"),
    ("Tirupati", "Temple town, spiritual hub — ~250 km"),
    ("Hampi", "UNESCO heritage, ruins — ~340 km"),
]
for i, (place, desc) in enumerate(destinations):
    row = i // 3
    col = i % 3
    x = 30 + col * 270
    y = H - 130 - row * 170

    draw_rect(c, x, y - 120, 255, 140, DARK_BLUE)
    draw_text(c, place, x, y - 35, size=22, color=ORANGE, bold=True, align="center", max_width=255)
    draw_text(c, desc, x, y - 70, size=12, color=white, align="center", max_width=255)
c.showPage()

# ===== SLIDE 7: Our Trusted Clients =====
draw_rect(c, 0, 0, W, H, white)
draw_header(c, "Our Trusted Clients")

draw_text(c, "Proud to serve leading companies and organizations",
          0, H - 105, size=15, color=DARK_GRAY, align="center", max_width=W)

clients = [
    ("Pluto Rides", "Ride-hailing & mobility platform"),
    ("Diligent", "Global governance & compliance leader"),
    ("OpenText", "Enterprise information management"),
    ("Operations Insights", "Business analytics & operations"),
]

for i, (name, desc) in enumerate(clients):
    x = 40 + i * 200
    y = H - 160

    # Card background
    draw_rect(c, x, y - 180, 185, 180, LIGHT_BG)
    # Orange accent at top
    draw_rect(c, x, y, 185, 4, ORANGE)

    # Client name
    draw_text(c, name, x, y - 60, size=17, color=DARK_BLUE, bold=True, align="center", max_width=185)

    # Orange divider
    draw_rect(c, x + 60, y - 80, 65, 3, ORANGE)

    # Description
    draw_text(c, desc, x + 10, y - 105, size=11, color=DARK_GRAY, align="center", max_width=165)

draw_text(c, "We provide dedicated corporate transportation solutions tailored to each client's needs.",
          0, 60, size=12, color=HexColor("#888888"), align="center", max_width=W)
c.showPage()

# ===== SLIDE 8: Contact Us =====
draw_rect(c, 0, 0, W, H, DARK_BLUE)
draw_rect(c, 0, H - 5, W, 5, ORANGE)
draw_rect(c, 0, 0, W, 5, ORANGE)

draw_text(c, "Let's Work Together", 0, H - 120, size=36, color=white, bold=True, align="center", max_width=W)
draw_rect(c, W/2 - 80, H - 135, 160, 3, ORANGE)
draw_text(c, "Contact us for corporate tie-ups, bulk bookings, and vendor partnerships", 0, H - 170, size=14, color=MID_GRAY, align="center", max_width=W)

contact_items = [
    ("Phone", "+91 99454 98275"),
    ("Email", "admin@actoursandtravels.com"),
    ("Website", "www.actoursandtravels.com"),
    ("WhatsApp", "+91 99454 98275"),
]
for i, (label, value) in enumerate(contact_items):
    x = 60 + i * 200
    draw_rect(c, x, H - 330, 185, 120, CARD_DARK)
    draw_text(c, label, x, H - 240, size=13, color=ORANGE, bold=True, align="center", max_width=185)
    draw_text(c, value, x + 10, H - 270, size=11, color=white, align="center", max_width=165)

draw_text(c, "Address: No.33-2, Kudlu Main Road, Kudlu, Bommanahalli Post, Bangalore - 560068",
          0, 80, size=12, color=MID_GRAY, align="center", max_width=W)

c.save()
print(f"PDF saved to: {pdf_path}")
