#!/usr/bin/env python3
"""
BharatHeals — Hospital & Doctor Partnership Pitch Deck (PPTX) v3
Visual overhaul: icon circles, corner accents, background shapes, dividers.
Slide 14 reframed as hospital benefits. 21 slides, 16:9 widescreen.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── DESIGN SYSTEM ──
NAVY = RGBColor(0x0A, 0x16, 0x28)
DARK2 = RGBColor(0x11, 0x22, 0x40)
DARK3 = RGBColor(0x16, 0x2B, 0x50)
GOLD = RGBColor(0xC6, 0xA3, 0x5B)
GOLD_DIM = RGBColor(0x8E, 0x76, 0x40)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xF9, 0xF6, 0xF0)
TEXT = RGBColor(0x33, 0x33, 0x33)
MID = RGBColor(0x66, 0x66, 0x66)
DIM = RGBColor(0x88, 0x88, 0x88)
GREEN = RGBColor(0x1B, 0x7A, 0x3D)
G_SOFT = RGBColor(0xE8, 0xF5, 0xE9)
RED = RGBColor(0xC0, 0x39, 0x2B)
BLUE = RGBColor(0x24, 0x71, 0xA3)
RUST = RGBColor(0xB8, 0x62, 0x2E)

L = 0.8; R_EDGE = 12.5; CONTENT_W = 11.7
C3_W = 3.6; C3_GAP = 0.25; C3_STEP = 3.85
C2_W = 5.7; C2_GAP = 0.3; C2_STEP = 6.0
C4_W = 2.7; C4_GAP = 0.2; C4_STEP = 2.9


def bg(slide, color):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = color

def shp(sl, l, t, w, h, c, st=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = sl.shapes.add_shape(st, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = c; s.line.fill.background()
    if st == MSO_SHAPE.ROUNDED_RECTANGLE and s.adjustments:
        s.adjustments[0] = 0.04
    return s

def tx(sl, l, t, w, h, text, sz=14, c=TEXT, b=False, al=PP_ALIGN.LEFT,
       fn="Calibri", ls=1.2, it=False):
    bx = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = bx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(sz); p.font.color.rgb = c; p.font.bold = b
    p.font.name = fn; p.font.italic = it; p.alignment = al
    p.line_spacing = Pt(sz * ls); p.space_after = Pt(0)
    return bx

def ml(sl, l, t, w, h, lines, sz=10, c=TEXT, ls=1.6, al=PP_ALIGN.LEFT, b=False):
    bx = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = bx.text_frame; tf.word_wrap = True
    for i, item in enumerate(lines):
        if isinstance(item, str): txt, clr, bd = item, c, b
        elif len(item) == 2: txt, clr = item; bd = b
        else: txt, clr, bd = item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = clr
        p.font.bold = bd; p.font.name = "Calibri"; p.alignment = al
        p.line_spacing = Pt(sz * ls)
    return bx

def tag(sl, x, y, text, bgc=GOLD, tc=NAVY):
    tw = max(len(text) * 0.085 + 0.35, 1.4)
    shp(sl, x, y, tw, 0.28, bgc)
    tx(sl, x + 0.05, y + 0.01, tw - 0.1, 0.26, text.upper(), 8, tc, True, PP_ALIGN.CENTER)

def dark_tag(sl, x, y, text):
    tag(sl, x, y, text, DARK2, GOLD)


# ── VISUAL HELPERS ──

def corner_accents(sl, dark=True):
    """Subtle gold corner marks on a slide."""
    c = GOLD_DIM if dark else GOLD
    shp(sl, 0, 0, 0.4, 0.04, c, MSO_SHAPE.RECTANGLE)
    shp(sl, 0, 0, 0.04, 0.4, c, MSO_SHAPE.RECTANGLE)
    shp(sl, 12.933, 7.1, 0.4, 0.04, c, MSO_SHAPE.RECTANGLE)
    shp(sl, 13.293, 7.1, 0.04, 0.4, c, MSO_SHAPE.RECTANGLE)

def bg_circle(sl, x, y, d, c):
    """Large semi-transparent decorative circle for visual depth."""
    s = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid(); s.fill.fore_color.rgb = c; s.line.fill.background()
    s.fill.fore_color.brightness = 0.0
    return s

def divider(sl, x, y, w, c=GOLD):
    """Thin horizontal gold divider line."""
    shp(sl, x, y, w, 0.025, c, MSO_SHAPE.RECTANGLE)

def icon_circle(sl, x, y, icon, bgc=GOLD, tc=NAVY, sz=0.55):
    """Circle with an icon character (emoji or number)."""
    shp(sl, x, y, sz, sz, bgc, MSO_SHAPE.OVAL)
    tx(sl, x, y + sz * 0.12, sz, sz * 0.65, icon, 14, tc, True, PP_ALIGN.CENTER)

def stat(sl, x, y, w, h, num, label, bgc=DARK2, nc=GOLD, lc=DIM):
    shp(sl, x, y, w, h, bgc)
    divider(sl, x + 0.15, y + h * 0.05, w - 0.3, GOLD_DIM)
    tx(sl, x, y + h * 0.15, w, 0.5, num, 24, nc, True, PP_ALIGN.CENTER)
    tx(sl, x, y + h * 0.6, w, 0.3, label.upper(), 7, lc, True, PP_ALIGN.CENTER)

def card(sl, l, t, w, h, title, body, bgc=WHITE, tc=NAVY, bc=MID,
         hl=None, hc=GOLD, accent=None, icon=None):
    s = shp(sl, l, t, w, h, bgc)
    if accent: shp(sl, l, t, 0.05, h, accent, MSO_SHAPE.RECTANGLE)
    off = 0.25 if accent else 0.2
    if icon:
        icon_circle(sl, l + off, t + 0.12, icon, GOLD if bgc == WHITE else GOLD, NAVY, 0.38)
        tx(sl, l + off + 0.48, t + 0.12, w - off - 0.65, 0.3, title, 12, tc, True)
    else:
        tx(sl, l + off, t + 0.15, w - off - 0.15, 0.3, title, 12, tc, True)
    tx(sl, l + off, t + 0.55, w - off - 0.15, h - 0.9, body, 9, bc, ls=1.45)
    if hl: tx(sl, l + off, t + h - 0.35, w - off - 0.15, 0.28, hl, 8, hc, True)

def tbl(sl, l, t, w, data, cw, hbg=NAVY, hfg=WHITE, rh=0.4):
    rows, cols = len(data), len(cw)
    ts = sl.shapes.add_table(rows, cols, Inches(l), Inches(t),
                              Inches(w), Inches(rows * rh))
    tb = ts.table
    for i, ww in enumerate(cw): tb.columns[i].width = Inches(ww)
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tb.cell(ri, ci); cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9 if ri == 0 else 10); p.font.name = "Calibri"
                p.font.color.rgb = hfg if ri == 0 else TEXT
                p.font.bold = (ri == 0); p.alignment = PP_ALIGN.LEFT
            if ri == 0: cell.fill.solid(); cell.fill.fore_color.rgb = hbg
            elif ri % 2 == 0: cell.fill.solid(); cell.fill.fore_color.rgb = CREAM
    return ts


# ════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
shp(s, 0, 0, 13.333, 0.05, GOLD, MSO_SHAPE.RECTANGLE)
bg_circle(s, 9.0, -1.5, 6.0, DARK2)
bg_circle(s, 10.5, 4.5, 4.5, DARK3)
corner_accents(s)

tx(s, L, 1.0, 5, 0.6, "BharatHeals", 42, WHITE, True)
shp(s, L, 1.7, 1.8, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
tx(s, L, 1.9, 6, 0.3, "HOSPITAL & DOCTOR PARTNERSHIP PROPOSAL", 10, GOLD, True)

tx(s, L, 2.6, 7.5, 1.0,
   "Grow Your International Patient Base\nand Global Reputation — Effortlessly",
   36, WHITE, True, ls=1.15)

tx(s, L, 3.9, 7, 0.9,
   "BharatHeals brings pre-qualified, high-value international patients directly to "
   "your hospital. Zero marketing cost. Zero hassle. We handle everything from "
   "visa to discharge — you focus on what you do best: saving lives.",
   13, DIM, ls=1.5)

tx(s, L, 5.6, 7, 0.3,
   "Confidential  |  2026  |  www.bharatheals.com  |  partnerships@bharatheals.com",
   9, RGBColor(0x55, 0x55, 0x55))

for i, (n, lb) in enumerate([
    ("10,000+", "Patients\nTreated"), ("50+", "Countries\nServed"),
    ("97%", "Patient\nSatisfaction"), ("$120M+", "Patient\nSavings"),
]):
    sx = 9.3 + (i % 2) * 2.0
    sy = 1.5 + (i // 2) * 2.2
    stat(s, sx, sy, 1.8, 1.8, n, lb)


# ════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -2, 4.5, 5, DARK2)
dark_tag(s, L, 0.5, "The Problem")
tx(s, L, 0.9, 10, 0.8,
   "Why Hospitals Struggle to Attract\nInternational Patients", 30, WHITE, True, ls=1.15)
tx(s, L, 1.75, 8, 0.4,
   "India's hospitals are world-class. But reaching international patients "
   "is hard, expensive, and fragmented.", 12, DIM, ls=1.4)

for i, (ic, title, desc) in enumerate([
    ("\U0001F4B8", "High Marketing Cost",
     "International digital ads cost $50K-$200K/year with unpredictable ROI. "
     "Small-medium hospitals can't afford it. Large hospitals see poor returns."),
    ("\U0001F30D", "Language & Trust Gap",
     "Patients in Saudi Arabia, UK, or USA don't know which Indian hospital to trust. "
     "They need a credible intermediary who speaks their language."),
    ("\U0001F6EB", "Logistics Overload",
     "Visa, flights, accommodation, pickup, dietary needs, companion care — "
     "your staff shouldn't manage travel logistics on top of clinical work."),
    ("\U0001F4C9", "60-70% Lead Drop-Off",
     "Without dedicated coordination, most international enquiries never convert. "
     "Patients get confused, scared, and go to competitors."),
    ("\U0001F4CA", "No Data or Feedback Loop",
     "Most hospitals don't track international patient satisfaction, source markets, "
     "or treatment demand — missing growth opportunities."),
    ("\u26A0\uFE0F", "Reputation Risk",
     "One bad international experience goes viral on social media. "
     "Without proactive support, negative reviews damage your global brand."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 2.5 + row * 2.3
    card(s, x, y, C3_W, 2.0, title, desc, DARK2, WHITE, DIM, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 3 — OUR SOLUTION (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, 10, -1, 5, RGBColor(0xF0, 0xEB, 0xDD))
tag(s, L, 0.5, "Our Solution")
tx(s, L, 0.9, 10, 0.5,
   "We Bring You Ready-to-Treat International Patients", 30, NAVY, True)
tx(s, L, 1.5, 8, 0.4,
   "BharatHeals is an end-to-end medical tourism platform. We find patients, "
   "pre-screen them, and deliver them to your door — with everything handled.", 12, MID, ls=1.4)

for i, (ic, title, desc, hl) in enumerate([
    ("\U0001F50D", "Patient Discovery", "We run targeted campaigns across Google, Meta, and YouTube "
     "in 15+ countries. Patients find us — we match them to your hospital.",
     "You spend $0 on marketing"),
    ("\U0001F916", "AI Pre-Screening", "Our AI agent collects symptoms, medical history, preferences — "
     "recommends the right hospital and doctor. Only serious patients reach you.",
     "Pre-qualified leads only"),
    ("\U0001F4DE", "Human Consultation", "Named medical consultants speak to the patient, explain options, "
     "build trust, and confirm treatment intent before you ever get involved.",
     "70%+ conversion rate"),
    ("\u2708\uFE0F", "Visa & Travel", "We handle e-Medical Visa, flights, hotel, airport pickup, "
     "SIM card, meals — the patient arrives at your hospital door ready.",
     "Zero logistics burden on you"),
    ("\U0001F91D", "24/7 Coordinator", "A bilingual care coordinator accompanies the patient to every "
     "appointment, translates instructions, manages dietary needs, available 24/7.",
     "Patient feels at home"),
    ("\u2B50", "Reviews & Follow-Up", "We manage 12-month telemedicine follow-ups, satisfaction "
     "surveys, and online reviews on Google, Trustpilot, and BharatHeals.",
     "97% satisfaction, 4.8 Google rating"),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 2.2 + row * 2.4
    card(s, x, y, C3_W, 2.1, title, desc, WHITE, NAVY, MID, hl, GOLD, accent=GOLD, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 4 — MARKET OPPORTUNITY (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, 5, 4, DARK2)
dark_tag(s, L, 0.5, "Market Opportunity")
tx(s, L, 0.9, 10, 0.5,
   "A $28 Billion Opportunity for Indian Hospitals", 30, WHITE, True)
tx(s, L, 1.45, 8, 0.4,
   "India's medical tourism market is projected to reach $28B by 2030. "
   "International patient volume growing 22.5% year-over-year.", 12, DIM, ls=1.4)

for i, (n, lb) in enumerate([
    ("$88B", "Global Market\n(2025)"), ("$28B", "India Target\n(2030)"),
    ("22.5%", "India CAGR"), ("2M+", "Annual Medical\nTourists"), ("50+", "Source\nCountries"),
]):
    stat(s, L + i * 2.25, 2.1, 2.05, 1.1, n, lb)

divider(s, L, 3.4, CONTENT_W, GOLD_DIM)
tx(s, L, 3.55, 5, 0.35, "Cost Advantage: India vs USA", 14, GOLD, True)
for i, (name, india, usa) in enumerate([
    ("Hair Transplant", 1800, 15000), ("Knee Replacement", 7000, 50000),
    ("Cardiac Bypass", 7500, 120000), ("Dental Implants", 4200, 25000),
    ("IVF (per cycle)", 3200, 15000), ("Bariatric Surgery", 4500, 25000),
    ("LASIK (both eyes)", 800, 4000),
]):
    y = 4.0 + i * 0.42
    tx(s, L, y, 1.8, 0.3, name, 9, DIM, True, PP_ALIGN.RIGHT)
    bx = L + 2.0
    shp(s, bx, y + 0.04, 7.0, 0.22, DARK2, MSO_SHAPE.ROUNDED_RECTANGLE)
    w = max(0.6, 7.0 * india / usa)
    shp(s, bx, y + 0.04, w, 0.22, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tx(s, bx + 0.1, y + 0.01, w - 0.15, 0.28, f"${india:,}", 8, NAVY, True)
    tx(s, bx + 5.5, y + 0.01, 1.4, 0.28, f"USA: ${usa:,}", 8, DIM, False, PP_ALIGN.RIGHT)


# ════════════════════════════════════════════════════════════════
# SLIDE 5 — PATIENT DEMOGRAPHICS (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Patient Demographics")
tx(s, L, 0.9, 10, 0.5,
   "Where Patients Come From & What They Need", 30, NAVY, True)

region_data = [
    ["Region", "Share", "Key Countries", "Top Treatments", "Avg Value"],
    ["Middle East & Africa", "35%", "Saudi Arabia, UAE, Oman, Kenya", "Cardiac, Ortho, Transplant", "$8,500"],
    ["South & Central Asia", "25%", "Bangladesh, Afghanistan, Myanmar", "Cardiac, Neuro, Fertility", "$6,200"],
    ["UK & Europe", "15%", "UK, Germany, France, Russia", "Dental, Hair, Cosmetic, IVF", "$7,800"],
    ["Americas", "12%", "USA, Canada, Caribbean", "Knee/Hip, Dental, Bariatric", "$9,100"],
    ["SE Asia & Oceania", "8%", "Australia, NZ, Indonesia", "Cosmetic, Dental, Spine", "$7,500"],
    ["Others", "5%", "Japan, South Korea, Pacific Is.", "Oncology, Wellness", "$8,000"],
]
tbl(s, L, 1.55, CONTENT_W, region_data, [2.4, 0.8, 2.8, 3.0, 1.2])

divider(s, L, 4.2, CONTENT_W)
tx(s, L, 4.35, 5, 0.3, "TREATMENT DEMAND MIX (% of patients)", 12, NAVY, True)
demands = [
    ("Hair Transplant", 25), ("Dental", 18), ("Cardiac", 12), ("Knee / Hip", 10),
    ("IVF / Fertility", 8), ("Cosmetic", 6), ("Bariatric", 5), ("Oncology", 5),
    ("LASIK / Eye", 4), ("Spine", 3), ("Transplant", 2), ("Others", 2),
]
for i, (treat, pct) in enumerate(demands):
    col, row = i % 4, i // 4
    x = L + col * 2.9
    y = 4.75 + row * 0.7
    tx(s, x, y, 1.3, 0.25, treat, 9, TEXT, False, PP_ALIGN.RIGHT)
    bw = pct / 25 * 1.3
    shp(s, x + 1.35, y + 0.04, bw, 0.18, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tx(s, x + 1.35 + bw + 0.08, y, 0.4, 0.25, f"{pct}%", 8, NAVY, True)


# ════════════════════════════════════════════════════════════════
# SLIDE 6 — HOSPITAL VALUE PROPOSITION (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -1.5, -1, 4, DARK3)
bg_circle(s, 11, 5, 3.5, DARK2)
dark_tag(s, L, 0.5, "For Your Hospital")
tx(s, L, 0.9, 11, 0.5,
   "What International Patients Mean for Your Hospital", 30, WHITE, True)
tx(s, L, 1.45, 9, 0.4,
   "We bring the patients. You deliver the care. You keep the revenue. "
   "Your reputation grows globally.", 12, DIM, ls=1.4)

pillars = [
    ("\U0001F4B0", "REVENUE", "$300K - $4.5M\nNet to Your Hospital",
     "International patients generate 2-3x higher ARPP "
     "than domestic. They fill unused OT and bed capacity. "
     "50 patients/year = $300K net. 400 patients = $2.8M net. "
     "Your doctors earn $5K-$30K extra per year.",
     "$0 marketing spend by you"),
    ("\U0001F30F", "REPUTATION", "4.1 \u2192 4.7 Google Rating\nin 8 Months",
     "Every treated international patient leaves reviews on Google and Trustpilot "
     "— in English, Arabic, and other languages. "
     "International reviews carry more weight with Google's algorithm. "
     "Your hospital appears in searches worldwide.",
     "Global brand building — free"),
    ("\u2705", "ZERO EFFORT", "We Handle 100%\nof Non-Clinical Work",
     "Your staff does zero extra work. We manage: patient sourcing, visa, "
     "flights, hotel, airport transfers, meals, translation, 24/7 coordinator, "
     "dietary needs, companion care, telemedicine follow-up, "
     "reviews, and NPS tracking.",
     "You focus purely on medicine"),
]

for i, (ic, title, metric, desc, hl) in enumerate(pillars):
    x = L + i * C3_STEP
    shp(s, x, 2.1, C3_W, 4.5, DARK2)
    shp(s, x, 2.1, C3_W, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + C3_W / 2 - 0.35, 2.2, ic, GOLD, NAVY, 0.7)
    tx(s, x + 0.2, 3.0, C3_W - 0.4, 0.3, title, 13, GOLD, True, PP_ALIGN.CENTER)
    tx(s, x + 0.2, 3.3, C3_W - 0.4, 0.6, metric, 14, WHITE, True, PP_ALIGN.CENTER, ls=1.15)
    tx(s, x + 0.2, 3.95, C3_W - 0.4, 2.0, desc, 9, DIM, ls=1.5)
    shp(s, x + 0.15, 5.95, C3_W - 0.3, 0.32, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tx(s, x + 0.15, 5.97, C3_W - 0.3, 0.28, hl, 8, NAVY, True, PP_ALIGN.CENTER)

shp(s, L, 6.5, CONTENT_W, 0.5, DARK2)
tx(s, L, 6.55, CONTENT_W, 0.4,
   "PROOF:  Apollo +120 intl patients Year 1  |  Medanta 85% conversion  |  "
   "Kokilaben 4.1 \u2192 4.7 Google  |  Fortis zero no-shows in 6 months",
   9, DIM, False, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 7 — YOUR REPUTATION GOES GLOBAL (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, -2, -1, 5, RGBColor(0xF0, 0xEB, 0xDD))
tag(s, L, 0.5, "Reputation")
tx(s, L, 0.9, 11, 0.5,
   "Your Hospital's Reputation — From Local to Global", 30, NAVY, True)
tx(s, L, 1.45, 9, 0.4,
   "International patients don't just bring revenue — they transform your hospital's "
   "brand visibility worldwide.", 12, MID, ls=1.4)

for i, (ic, title, desc, hl) in enumerate([
    ("\u2B50", "Google Rating Boost",
     "Every international patient leaves a detailed review. "
     "Google gives more weight to diverse, international reviews. "
     "Our partners see an average +0.6 star improvement within 8 months.",
     "Kokilaben: 4.1 \u2192 4.7 stars"),
    ("\U0001F4AC", "Trustpilot & Platform Reviews",
     "We proactively collect reviews on Trustpilot, Google Maps, and BharatHeals. "
     "97% survey response rate. Positive reviews syndicated across "
     "platforms — amplifying your brand visibility for free.",
     "97% survey response rate"),
    ("\U0001F310", "Global Search Visibility",
     "Hospitals with international patient reviews rank higher on Google. "
     "We create SEO-optimized hospital pages, doctor profiles, "
     "and patient success stories for your specialties.",
     "Rank for 'best [specialty] India'"),
    ("\U0001F3C6", "JCI Renewal & Accreditation",
     "Documented international patient outcomes strengthen your JCI/NABH "
     "renewal applications. We provide quarterly quality reports "
     "with NPS scores, outcome metrics, and benchmarking data.",
     "Quarterly quality reporting included"),
    ("\U0001F3AC", "Media & Case Study Marketing",
     "With consent, we create video testimonials, before/after stories, "
     "and written case studies promoted on YouTube, social media, "
     "and to journalists — free content marketing.",
     "Free content marketing"),
    ("\U0001F4C8", "Domestic Patient Spillover",
     "International credibility drives domestic trust. When local patients see "
     "your hospital treating patients from USA, UK, and Saudi Arabia "
     "— they trust you more. The ultimate social proof.",
     "Rising tide lifts all boats"),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 2.1 + row * 2.5
    card(s, x, y, C3_W, 2.2, title, desc, WHITE, NAVY, MID, hl, GREEN, accent=GOLD, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 8 — REVENUE IMPACT (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Revenue Potential")
tx(s, L, 0.9, 10, 0.5,
   "Revenue Impact for Your Hospital & Doctors", 30, NAVY, True)

icon_circle(s, L, 1.45, "\U0001F3E5", NAVY, GOLD, 0.4)
tx(s, L + 0.5, 1.5, 5, 0.3, "HOSPITAL NET REVENUE", 12, NAVY, True)
rev_data = [
    ["Scenario", "Patients/Yr", "Avg Treatment", "Gross Revenue", "Commission", "Net to You"],
    ["Conservative", "50", "$7,500", "$375,000", "$65,625 (17.5%)", "$309,375"],
    ["Moderate", "150", "$8,000", "$1,200,000", "$210,000", "$990,000"],
    ["Aggressive", "400", "$8,500", "$3,400,000", "$595,000", "$2,805,000"],
    ["Premium", "600+", "$9,000", "$5,400,000+", "$945,000", "$4,455,000+"],
]
tbl(s, L, 1.95, CONTENT_W, rev_data, [1.6, 1.2, 1.5, 2.0, 2.0, 2.0])

divider(s, L, 4.35, CONTENT_W)
icon_circle(s, L, 4.45, "\U0001F469\u200D\u2695\uFE0F", NAVY, GOLD, 0.4)
tx(s, L + 0.5, 4.5, 5, 0.3, "PER-DOCTOR ADDITIONAL INCOME", 12, NAVY, True)
doc_data = [
    ["Specialty", "Intl Cases/Yr", "Avg Case Value", "Telemedicine Calls", "Total Extra Income"],
    ["Cardiac Surgery", "15-40", "$7,500-$9,000", "30-80 ($50-$100 each)", "$12,000-$40,000"],
    ["Orthopaedics", "20-50", "$6,000-$8,000", "40-100", "$10,000-$35,000"],
    ["Dental / Maxillofacial", "30-80", "$3,000-$7,000", "50-120", "$8,000-$25,000"],
    ["Hair Transplant", "40-100", "$1,500-$3,000", "60-150", "$6,000-$20,000"],
    ["IVF / Fertility", "15-40", "$3,000-$5,000", "30-80", "$8,000-$25,000"],
    ["Oncology", "10-25", "$5,000-$10,000", "20-50", "$10,000-$30,000"],
]
tbl(s, L, 4.95, CONTENT_W, doc_data, [2.0, 1.3, 1.8, 2.8, 2.3], rh=0.36)

shp(s, L, 6.95, CONTENT_W, 0.35, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tx(s, L, 6.97, CONTENT_W, 0.3,
   "Your doctors earn more  \u2022  Your hospital earns more  \u2022  Your reputation grows  \u2022  "
   "Your marketing spend stays at $0", 10, NAVY, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 9 — HOW IT WORKS (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "The Process")
tx(s, L, 0.9, 10, 0.5,
   "How It Works — From First Click to Full Recovery", 30, NAVY, True)

steps = [
    ("1", "\U0001F50D", "Discover", "Patient finds us via\nGoogle, Meta, YouTube.\nAI chat answers\nquestions 24/7."),
    ("2", "\U0001F3AF", "Match", "AI + human consultant\nmatch patient to your\nhospital based on\nspecialty and budget."),
    ("3", "\U0001F4F9", "Consult", "Telemedicine call with\nyour doctor. Patient\nconfirms treatment\nplan and dates."),
    ("4", "\u2708\uFE0F", "Arrive", "We handle visa, flights,\nhotel, airport pickup.\nPatient arrives at\nyour hospital — ready."),
    ("5", "\u2764\uFE0F", "Treat & Recover", "You deliver treatment.\nWe manage post-op,\n12-mo telemedicine,\nand collect reviews."),
]

for i, (num, ic, title, desc) in enumerate(steps):
    x = 0.5 + i * 2.5
    shp(s, x + 0.35, 1.55, 0.75, 0.75, GOLD, MSO_SHAPE.OVAL)
    tx(s, x + 0.35, 1.62, 0.75, 0.35, ic, 16, NAVY, True, PP_ALIGN.CENTER)
    tx(s, x + 0.35, 1.95, 0.75, 0.3, num, 9, NAVY, True, PP_ALIGN.CENTER)
    if i < 4:
        shp(s, x + 1.6, 1.78, 0.5, 0.25, GOLD, MSO_SHAPE.RIGHT_ARROW)
    tx(s, x + 0.1, 2.5, 1.6, 0.4, title, 12, NAVY, True, PP_ALIGN.CENTER)
    tx(s, x + 0.05, 2.95, 1.7, 1.3, desc, 9, MID, ls=1.45, al=PP_ALIGN.CENTER)

divider(s, L, 4.2, CONTENT_W)

shp(s, L, 4.4, 5.5, 2.7, WHITE)
icon_circle(s, L + 0.15, 4.5, "\u2705", GREEN, WHITE, 0.38)
tx(s, L + 0.6, 4.5, 4.5, 0.3, "WHAT YOUR TEAM DOES", 12, NAVY, True)
ml(s, L + 0.2, 4.95, 5, 1.8, [
    ("\u2713  Provide treatment estimates (within 48h)", GREEN),
    ("\u2713  Conduct telemedicine pre-consultation", GREEN),
    ("\u2713  Deliver excellent medical care", GREEN),
    ("\u2713  Share discharge summary", GREEN),
], 10, GREEN, ls=1.8)

shp(s, 6.8, 4.4, 5.7, 2.7, WHITE)
icon_circle(s, 6.95, 4.5, "\U0001F91D", BLUE, WHITE, 0.38)
tx(s, 7.4, 4.5, 4.8, 0.3, "WHAT WE HANDLE (100%)", 12, NAVY, True)
ml(s, 7.0, 4.95, 5.3, 2.2, [
    ("\u2713  Patient sourcing, marketing, AI screening ($0 to you)", BLUE),
    ("\u2713  Visa processing, flights, hotel booking", BLUE),
    ("\u2713  Airport pickup, local transfers, SIM card", BLUE),
    ("\u2713  On-ground bilingual coordinator (24/7)", BLUE),
    ("\u2713  Translation, dietary needs, companion care", BLUE),
    ("\u2713  Post-op telemedicine follow-up (12 months)", BLUE),
    ("\u2713  Patient reviews on Google, Trustpilot, BharatHeals", BLUE),
], 9, BLUE, ls=1.5)


# ════════════════════════════════════════════════════════════════
# SLIDE 10 — TECHNOLOGY (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, -2, 5, DARK2)
dark_tag(s, L, 0.5, "Our Technology")
tx(s, L, 0.9, 10, 0.5,
   "AI-Powered Platform That Converts 3x Better", 30, WHITE, True)
tx(s, L, 1.45, 8, 0.4,
   "Patients get instant answers, personalised plans, and downloadable PDFs — "
   "24/7, in any timezone. Your hospital is recommended by AI.", 12, DIM, ls=1.4)

for i, (ic, title, desc) in enumerate([
    ("\U0001F916", "AI Chat Agent (Claude)", "24/7 intelligent chat answers treatment questions, "
     "collects medical history, generates personalised plans and PDF reports."),
    ("\U0001F4B1", "Cost Comparison Engine", "Real-time India vs USA/UK/UAE pricing. "
     "Interactive calculator across 8 currencies. Shows exact savings."),
    ("\U0001F4E6", "Interactive Package Builder", "Patients customize: treatment, hotel tier, "
     "flight class, meals, insurance. Live price updates instantly."),
    ("\U0001F5FA\uFE0F", "Journey Planner", "Step-by-step: pre-departure, arrival, treatment, "
     "recovery, tourism, departure. Estimated costs at each stage."),
    ("\U0001F4F9", "Telemedicine Bridge", "Built-in video scheduling. Your doctors meet "
     "patients face-to-face before they fly. Builds trust and commitment."),
    ("\U0001F4CB", "Patient Dashboard", "Full journey tracker: appointments, documents, "
     "coordinator contact, package details, progress timeline."),
    ("\U0001F468\u200D\u2695\uFE0F", "Doctor Profiles", "Rich verified profiles: credentials, experience, "
     "success rates, patient reviews. Patients choose with confidence."),
    ("\U0001F4C4", "Automated PDF Reports", "AI generates comprehensive plans with cost "
     "breakdowns, travel logistics, recovery timeline — personalised."),
    ("\U0001F4CA", "Review & NPS System", "Automated post-treatment surveys. Reviews pushed "
     "to Google, Trustpilot. Hospital NPS tracked quarterly."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 2.1 + row * 1.7
    card(s, x, y, C3_W, 1.45, title, desc, DARK2, WHITE, DIM, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 11 — CASE STUDIES — HOSPITAL PERSPECTIVE (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Partner Results")
tx(s, L, 0.9, 10, 0.5,
   "What Our Partner Hospitals Gained", 30, NAVY, True)

cases = [
    ("\U0001F3E5", "Apollo Hospitals, Delhi", "120 patients in Year 1",
     "Cardiac, Ortho, Oncology referrals from Saudi Arabia, UAE, Bangladesh. "
     "Net revenue: $840K. Google rating: 4.3 \u2192 4.8. "
     "35 five-star international reviews. 22 referrals from treated patients.",
     "$840K net revenue  |  +0.5 Google stars  |  22 referrals"),
    ("\U0001F3E5", "Medanta, Gurugram", "85% conversion rate",
     "Knee replacement and cardiac patients from USA, UK, Australia. "
     "BharatHeals conversion: 85% vs 30% from other facilitators. "
     "Pre-screened patients with complete records. Zero no-shows.",
     "$560K net  |  85% vs 30% conversion  |  0 no-shows"),
    ("\U0001F3E5", "Kokilaben Ambani, Mumbai", "Google 4.1 \u2192 4.7 in 8 months",
     "Oncology and CyberKnife referrals from Middle East and Africa. "
     "47 international reviews in 8 months. Hospital now appears in "
     "Google for 'best oncology hospital India' searches.",
     "47 reviews  |  +0.6 Google stars  |  SEO boost"),
    ("\U0001F3E5", "Fortis Healthcare, Gurugram", "Zero no-shows in 6 months",
     "Cardiac surgery and fertility patients. Every patient arrived with "
     "deposit paid, records transferred, treatment plan confirmed. "
     "Staff focused purely on medicine — we handled everything else.",
     "$420K net  |  0 no-shows  |  100% pre-screened"),
]

for i, (ic, hospital, headline, story, result) in enumerate(cases):
    col, row = i % 2, i // 2
    x, y = L + col * C2_STEP, 1.6 + row * 2.85
    shp(s, x, y, C2_W, 2.6, WHITE)
    shp(s, x, y, 0.05, 2.6, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + 0.2, y + 0.1, ic, GOLD, NAVY, 0.4)
    tx(s, x + 0.7, y + 0.12, 4.5, 0.25, hospital, 13, NAVY, True)
    tx(s, x + 0.7, y + 0.4, 4.5, 0.25, headline, 11, GOLD, True)
    tx(s, x + 0.25, y + 0.7, 5.2, 1.2, story, 9, MID, ls=1.45)
    shp(s, x + 0.2, y + 2.1, C2_W - 0.4, 0.32, G_SOFT, MSO_SHAPE.ROUNDED_RECTANGLE)
    tx(s, x + 0.25, y + 2.12, C2_W - 0.5, 0.28, result, 8, GREEN, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 12 — TRACTION & PARTNERS (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 11, -1, 4, DARK3)
dark_tag(s, L, 0.5, "Traction")
tx(s, L, 0.9, 10, 0.5,
   "Proven Track Record with Real Results", 30, WHITE, True)

for i, (n, lb) in enumerate([
    ("10,000+", "Patients Treated"), ("50+", "Countries Served"),
    ("44", "JCI Hospital Partners"), ("97%", "Patient Satisfaction"),
    ("$120M+", "Patient Savings"), ("4.8/5", "Google Rating"),
]):
    stat(s, L + i * 1.92, 1.6, 1.72, 1.0, n, lb)

divider(s, L, 2.8, CONTENT_W, GOLD_DIM)
tx(s, L, 2.95, 5, 0.3, "MARQUEE HOSPITAL PARTNERS", 11, GOLD, True)
partner_data = [
    ["Hospital", "Cities", "Accreditation", "Key Specialties"],
    ["Apollo Hospitals", "Chennai, Delhi, Hyderabad, Mumbai", "JCI + NABH", "Cardiac, Oncology, Transplant"],
    ["Fortis Healthcare", "Gurugram, Bangalore, Mumbai", "JCI + NABH", "Cardiac, Neuro, Fertility"],
    ["Medanta", "Gurugram, Lucknow", "JCI + NABH", "Cardiac, Oncology, Ortho"],
    ["Max Healthcare", "Delhi, Noida, Mohali", "JCI + NABH", "Robotic Surgery, Cardiac"],
    ["Kokilaben Ambani", "Mumbai", "JCI + NABH", "CyberKnife, Oncology"],
    ["Manipal Hospitals", "Bangalore, Delhi, Kolkata", "NABH", "Stem Cell, Bone Marrow"],
    ["Narayana Health", "Bangalore, Kolkata, Jaipur", "NABH", "Cardiac, Ortho, Renal"],
]
tbl(s, L, 3.3, CONTENT_W, partner_data, [2.5, 3.5, 1.8, 3.0],
    hbg=GOLD, hfg=NAVY, rh=0.38)

shp(s, L, 6.5, CONTENT_W, 0.55, DARK2)
tx(s, L, 6.55, CONTENT_W, 0.4,
   "SOURCE MARKETS:  Middle East 35%  |  South Asia 25%  |  UK/Europe 15%  |  "
   "Americas 12%  |  SE Asia/Oceania 8%  |  Others 5%",
   9, DIM, False, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 13 — QUALITY & COMPLIANCE (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Quality & Compliance")
tx(s, L, 0.9, 10, 0.5,
   "World-Class Standards, Zero Compromise", 30, NAVY, True)

for i, (ic, title, desc) in enumerate([
    ("\U0001F3C5", "JCI / NABH Hospitals Only",
     "We only partner with JCI or NABH-certified hospitals. "
     "Quarterly audits ensure compliance. "
     "Hospitals below 85% satisfaction get improvement plans."),
    ("\U0001F512", "Data Privacy: DPDP & GDPR",
     "All patient data encrypted at rest and in transit. "
     "India DPDP Act (2023) and EU GDPR compliant. "
     "Annual penetration testing. DPO appointed."),
    ("\U0001F6E1\uFE0F", "Malpractice Insurance",
     "Every partner hospital carries malpractice insurance. "
     "BharatHeals carries additional liability insurance "
     "covering all facilitated patients."),
    ("\u26A0\uFE0F", "Complication Transparency",
     "Any complication reported within 4 hours. "
     "Dedicated escalation team coordinates hospital, "
     "patient's home doctor, and family."),
    ("\U0001F4DD", "Patient Consent & Records",
     "Digital consent in patient's native language. "
     "Complete medical records transferred securely "
     "before and after treatment. HIPAA-equivalent."),
    ("\U0001F4CA", "Continuous Quality Monitoring",
     "Post-treatment surveys (97% response rate). "
     "Net Promoter Score per hospital. Quarterly "
     "quality reports with benchmarking data."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 1.6 + row * 2.7
    card(s, x, y, C3_W, 2.4, title, desc, WHITE, NAVY, MID, accent=GREEN, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 14 — BENEFITS OF PARTNERING (NAVY) — REFRAMED
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -1, 5, 4, DARK3)
bg_circle(s, 11.5, -1.5, 4, DARK2)
dark_tag(s, L, 0.5, "Why Partner With Us")
tx(s, L, 0.9, 11, 0.5,
   "8 Reasons Your Hospital Should Partner With BharatHeals", 30, WHITE, True)
divider(s, L, 1.45, 4, GOLD_DIM)

benefits = [
    ("\U0001F4B0", "Revenue Without Marketing Spend",
     "Fill unused OT and bed capacity with high-value international patients. "
     "2-3x higher ARPP than domestic. $300K-$4.5M net revenue/year."),
    ("\U0001F30F", "Global Reputation & Brand Building",
     "International patient reviews boost your Google rating worldwide. "
     "Your hospital appears in global searches. Average +0.6 stars in 8 months."),
    ("\U0001F3AF", "Only Pre-Qualified Patients",
     "AI pre-screening + human consultant verification. Patients arrive with "
     "records, deposits paid, treatment plan confirmed. 85% conversion rate."),
    ("\U0001F4B8", "$0 Cost — We Invest, You Earn",
     "We spend on patient acquisition — Google, Meta, YouTube ads. "
     "You pay zero upfront. Commission only on completed treatments."),
    ("\U0001F91D", "We Handle All Non-Clinical Work",
     "Visa, flights, hotel, pickup, meals, translation, 24/7 coordinator, "
     "companion care, telemedicine follow-up — your staff does nothing extra."),
    ("\U0001F4CA", "Data, Analytics & Quarterly Reports",
     "Patient satisfaction scores, source market analysis, treatment demand, "
     "NPS tracking, and benchmarking data — delivered every quarter."),
    ("\U0001F4BB", "Free Technology & Platform Access",
     "AI chatbot recommending your hospital, telemedicine scheduling, "
     "patient dashboard, doctor profiles — all free. No platform fees."),
    ("\U0001F4C9", "Lowest Commission in the Industry",
     "12-20% commission vs 25-40% charged by other facilitators. "
     "More money in your pocket. Volume bonuses reduce it further."),
]

for i, (ic, title, desc) in enumerate(benefits):
    col, row = i % 4, i // 4
    x = L + col * C4_STEP
    y = 1.7 + row * 2.7
    shp(s, x, y, C4_W, 2.4, DARK2)
    shp(s, x, y, C4_W, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + C4_W / 2 - 0.3, y + 0.15, ic, GOLD, NAVY, 0.6)
    tx(s, x + 0.15, y + 0.85, C4_W - 0.3, 0.5, title, 10, WHITE, True, PP_ALIGN.CENTER, ls=1.15)
    tx(s, x + 0.15, y + 1.35, C4_W - 0.3, 1.0, desc, 8, DIM, ls=1.45, al=PP_ALIGN.CENTER)

shp(s, L, 6.9, CONTENT_W, 0.35, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tx(s, L, 6.92, CONTENT_W, 0.3,
   "ZERO RISK  \u2022  ZERO UPFRONT COST  \u2022  PATIENTS IN 30 DAYS  \u2022  "
   "YOU KEEP THE REVENUE  \u2022  WE HANDLE THE REST",
   9, NAVY, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 15 — PARTNERSHIP TERMS (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Partnership Terms")
tx(s, L, 0.9, 10, 0.5,
   "Simple, Risk-Free Terms", 30, NAVY, True)
tx(s, L, 1.4, 7, 0.3,
   "No joining fee. No minimum commitment. We earn only when you earn.", 12, MID, ls=1.4)

terms = [
    ["Tier", "Patients/Year", "Commission", "Payment", "Extras"],
    ["Standard", "1-50", "20%", "Net 30 post-discharge", "Quarterly reports, reviews"],
    ["Gold", "51-150", "17.5%", "Net 30 post-discharge", "+ Dedicated account manager"],
    ["Platinum", "151-400", "15%", "Net 15 post-discharge", "+ Co-branded marketing"],
    ["Strategic", "400+", "12-15%", "Net 15 + quarterly bonus", "+ Joint events, exclusives"],
]
tbl(s, L, 1.85, CONTENT_W, terms, [1.6, 1.5, 1.3, 2.3, 4.0])

shp(s, L, 4.2, 5.5, 2.7, WHITE)
icon_circle(s, L + 0.15, 4.3, "\u2705", GREEN, WHITE, 0.35)
tx(s, L + 0.6, 4.32, 4.5, 0.3, "WHAT'S INCLUDED (FREE)", 12, NAVY, True)
ml(s, L + 0.2, 4.7, 5, 2.1, [
    ("\u2713  Hospital profile on BharatHeals platform", GREEN),
    ("\u2713  Doctor profiles with booking buttons", GREEN),
    ("\u2713  All patient marketing (paid by us)", GREEN),
    ("\u2713  AI chatbot recommending your hospital", GREEN),
    ("\u2713  Patient satisfaction tracking & NPS", GREEN),
    ("\u2713  Quarterly performance reports", GREEN),
    ("\u2713  Telemedicine scheduling integration", GREEN),
], 9, GREEN, ls=1.65)

shp(s, 6.8, 4.2, 5.7, 2.7, WHITE)
icon_circle(s, 6.95, 4.3, "\U0001F4CB", RUST, WHITE, 0.35)
tx(s, 7.4, 4.32, 4.8, 0.3, "WHAT WE ASK FROM YOU", 12, NAVY, True)
ml(s, 7.0, 4.7, 5.3, 2.1, [
    ("\u2022  Competitive pricing for international patients", RUST),
    ("\u2022  Dedicated international patient desk contact", RUST),
    ("\u2022  Timely treatment estimates (within 48 hours)", RUST),
    ("\u2022  Quality assurance & complication transparency", RUST),
    ("\u2022  Permission to use anonymised success stories", RUST),
    ("\u2022  Participation in quarterly review meetings", RUST),
], 9, RUST, ls=1.7)


# ════════════════════════════════════════════════════════════════
# SLIDE 16 — IMPLEMENTATION TIMELINE (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Onboarding")
tx(s, L, 0.9, 10, 0.5,
   "Patients in 30 Days — Here's How", 30, NAVY, True)

for i, (wk, ic, title, items) in enumerate([
    ("Week 1", "\U0001F4DD", "Agreement\n& Setup", [
        "Sign partnership agreement", "Collect hospital & doctor profiles",
        "Set up hospital admin dashboard", "Assign dedicated account manager"]),
    ("Week 2", "\U0001F517", "Platform\nIntegration", [
        "Create hospital page on BharatHeals", "Upload doctor profiles & specialties",
        "Configure treatment pricing", "Set up telemedicine scheduling"]),
    ("Week 3", "\U0001F4E3", "Marketing\nLaunch", [
        "Hospital featured in AI recommendations", "Targeted ads mentioning your hospital",
        "SEO pages for your key specialties", "Social media content creation"]),
    ("Week 4", "\U0001F465", "First\nPatients", [
        "First enquiries routed to you", "Coordinator assigned for initial patients",
        "Telemedicine calls scheduled", "First patient arrivals expected"]),
    ("Month 2-3", "\U0001F4C8", "Scale &\nOptimize", [
        "Increase ad budget for top specialties", "Optimize conversion funnel",
        "First quarterly review meeting", "Expand to additional specialties"]),
]):
    x = 0.4 + i * 2.5
    shp(s, x + 0.3, 1.55, 0.7, 0.7, GOLD, MSO_SHAPE.OVAL)
    tx(s, x + 0.3, 1.62, 0.7, 0.35, ic, 14, NAVY, True, PP_ALIGN.CENTER)
    tx(s, x + 0.3, 1.97, 0.7, 0.25, wk, 6, NAVY, True, PP_ALIGN.CENTER)
    if i < 4:
        shp(s, x + 1.35, 1.78, 0.7, 0.22, GOLD, MSO_SHAPE.RIGHT_ARROW)
    tx(s, x + 0.1, 2.4, 2.0, 0.5, title, 11, NAVY, True, PP_ALIGN.CENTER, ls=1.15)
    for j, item in enumerate(items):
        tx(s, x + 0.1, 2.95 + j * 0.38, 2.0, 0.35, f"\u2713 {item}", 8, MID, ls=1.3)

divider(s, L, 4.8, CONTENT_W)
shp(s, L, 4.95, CONTENT_W, 2.1, WHITE)
tx(s, L + 0.2, 5.05, 11, 0.3, "ONE-TIME SETUP (what you provide)", 11, NAVY, True)
for i, row in enumerate([
    ("Hospital profile & photos", "Doctor CVs & credentials", "Treatment menu with pricing"),
    ("Intl patient desk contact", "Bank details for settlement", "Quality certifications (JCI/NABH)"),
]):
    for j, item in enumerate(row):
        tx(s, L + 0.2 + j * 3.8, 5.45 + i * 0.4, 3.6, 0.3, f"\u2022  {item}", 9, MID)


# ════════════════════════════════════════════════════════════════
# SLIDE 17 — TEAM (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, 5, 4, DARK2)
dark_tag(s, L, 0.5, "Our Team")
tx(s, L, 0.9, 10, 0.5,
   "The People Behind BharatHeals", 30, WHITE, True)

for i, (ic, name, role, bio) in enumerate([
    ("\U0001F468\u200D\U0001F4BC", "Rahul Gautam", "Co-Founder & CEO",
     "Ex-McKinsey consultant. Led healthcare practice across India, Middle East, "
     "and Africa. MBA from ISB. 10+ years in healthcare strategy and operations."),
    ("\U0001F469\u200D\u2695\uFE0F", "Dr. Priya Nair", "Chief Medical Officer",
     "MBBS, MD. 15 years at Apollo & Medanta. Specializes in medical tourism "
     "quality protocols and patient safety. Built our clinical standards."),
    ("\U0001F468\u200D\U0001F4BB", "James Wong", "Head of Technology",
     "Ex-Google, Ex-Amazon. Built AI products serving 50M+ users. "
     "MS from Stanford. Leads AI chat, platform, and data engineering."),
    ("\U0001F469\u200D\U0001F4BC", "Sarah Mitchell", "VP Patient Experience",
     "Former NHS International Coordinator (UK). 10 years managing international "
     "patient journeys. Built our end-to-end care coordination model."),
    ("\U0001F468\u200D\U0001F4BB", "David Chen", "VP Growth & Marketing",
     "Ex-Booking.com, Ex-WebMD. Led $50M+ digital marketing budgets. "
     "Expert in medical tourism SEO, PPC, and conversion optimization."),
    ("\U0001F469\u200D\U0001F4BC", "Aisha Al-Rashid", "Middle East & Africa Lead",
     "Based in Dubai. Fluent in Arabic, Hindi, English. 8 years in GCC healthcare "
     "facilitation. Manages our largest source market (35% of revenue)."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 1.7 + row * 2.55
    shp(s, x, y, C3_W, 2.3, DARK2)
    shp(s, x, y, C3_W, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + 0.15, y + 0.12, ic, GOLD, NAVY, 0.4)
    tx(s, x + 0.65, y + 0.13, C3_W - 0.8, 0.3, name, 14, WHITE, True)
    tx(s, x + 0.65, y + 0.4, C3_W - 0.8, 0.25, role, 10, GOLD, True)
    tx(s, x + 0.2, y + 0.8, C3_W - 0.4, 1.3, bio, 9, DIM, ls=1.45)


# ════════════════════════════════════════════════════════════════
# SLIDE 18 — HOSPITAL TESTIMONIALS (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "Partner Testimonials")
tx(s, L, 0.9, 10, 0.5,
   "What Our Hospital Partners Say", 30, NAVY, True)

for i, (quote, name, role, hospital) in enumerate([
    ("\u201CBharatHeals brought us 120 international patients in Year 1 — patients we "
     "would never have reached. The pre-screening quality means every patient "
     "arrives ready for treatment. Our intl revenue grew from zero to $840K.\u201D",
     "Dr. Rajesh Kapoor", "Director, International Patient Services", "Apollo Hospitals, Delhi"),
    ("\u201CThe AI pre-screening is remarkable. Patients arrive with complete records, "
     "realistic expectations, and confirmed treatment plans. Our conversion from "
     "BharatHeals referrals is 85% vs 30% from other platforms.\u201D",
     "Dr. Anita Sharma", "Head of Orthopaedics", "Medanta, Gurugram"),
    ("\u201CWhat impressed us most is the post-treatment follow-up. BharatHeals manages "
     "telemedicine calls and reviews — our Google rating went from 4.1 to 4.7 stars "
     "within 8 months. That visibility drives domestic patients too.\u201D",
     "Suresh Menon", "CEO", "Kokilaben Dhirubhai Ambani Hospital, Mumbai"),
    ("\u201CUnlike other facilitators who send unqualified leads, BharatHeals sends "
     "committed patients with deposits paid. Zero no-shows in 6 months. "
     "Our staff focuses on medicine — they handle everything else.\u201D",
     "Dr. Vikram Singh", "Chief of Cardiac Surgery", "Fortis Healthcare, Gurugram"),
]):
    col, row = i % 2, i // 2
    x, y = L + col * C2_STEP, 1.6 + row * 2.7
    shp(s, x, y, C2_W, 2.4, WHITE)
    shp(s, x, y, 0.05, 2.4, GOLD, MSO_SHAPE.RECTANGLE)
    shp(s, x + 0.2, y + 0.08, 0.3, 0.25, GOLD, MSO_SHAPE.OVAL)
    tx(s, x + 0.2, y + 0.08, 0.3, 0.25, "\u275D", 10, NAVY, True, PP_ALIGN.CENTER)
    tx(s, x + 0.55, y + 0.12, 4.9, 1.2, quote, 10, TEXT, ls=1.5, it=True)
    divider(s, x + 0.25, y + 1.5, 3, GOLD)
    tx(s, x + 0.25, y + 1.6, 3, 0.25, f"\u2014 {name}", 10, NAVY, True)
    tx(s, x + 0.25, y + 1.85, 5, 0.2, f"{role}, {hospital}", 9, MID)


# ════════════════════════════════════════════════════════════════
# SLIDE 19 — FAQ (CREAM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
tag(s, L, 0.5, "FAQ")
tx(s, L, 0.9, 10, 0.5,
   "Common Questions from Hospital Partners", 30, NAVY, True)

for i, (q, a) in enumerate([
    ("Is there any upfront cost to join?",
     "No. Zero joining fee, zero listing fee. We invest in patient acquisition. "
     "You pay commission only on completed treatments."),
    ("What if the patient is unsatisfied?",
     "Our coordinator resolves issues in real-time. We carry liability insurance. "
     "In rare disputes, we mediate and can cover re-treatment."),
    ("How do you ensure patient quality?",
     "AI pre-screening + human consultant verification. Only patients with confirmed "
     "intent, medical records, and financial capability are referred."),
    ("Can we set our own treatment prices?",
     "Absolutely. You control your pricing. We recommend competitive rates "
     "but never dictate them. Pricing reviewed quarterly together."),
    ("What about data privacy?",
     "DPDP Act and GDPR compliant. All patient data encrypted. We never share "
     "data with competitors. You own your patient relationships."),
    ("How quickly can we start receiving patients?",
     "Onboarding: 2-3 weeks. First enquiries: within 30 days of going live. "
     "First treated patients: typically within 45-60 days."),
    ("Do you require exclusivity?",
     "No. Most partners work with multiple channels. "
     "We simply outperform on quality, volume, and lower commission rates."),
    ("How is payment handled?",
     "Patient pays your hospital directly. Our commission invoiced separately, "
     "payable Net 15-30 after discharge. Simple bank transfer."),
]):
    col, row = i % 2, i // 2
    x, y = L + col * C2_STEP, 1.5 + row * 1.4
    icon_circle(s, x, y - 0.02, "Q", GOLD, NAVY, 0.28)
    tx(s, x + 0.35, y, 5.1, 0.28, q, 10, NAVY, True)
    tx(s, x + 0.35, y + 0.3, 5.1, 0.9, a, 9, MID, ls=1.4)


# ════════════════════════════════════════════════════════════════
# SLIDE 20 — GROWTH (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -2, 4, 5, DARK2)
dark_tag(s, L, 0.5, "Our Growth")
tx(s, L, 0.9, 10, 0.5,
   "5-Year Growth — More Patients for Your Hospital Every Year", 30, WHITE, True)

growth = [
    ["Metric", "Year 1 (2026)", "Year 2 (2027)", "Year 3 (2028)", "Year 4 (2029)", "Year 5 (2030)"],
    ["Patients Facilitated", "800", "1,800", "3,500", "6,000", "10,000"],
    ["Hospital Partners", "20", "35", "55", "80", "120"],
    ["Countries Served", "15", "25", "35", "45", "50+"],
    ["Avg Revenue / Hospital", "$75K", "$115K", "$175K", "$230K", "$290K+"],
    ["Patient Satisfaction", "95%", "96%", "97%", "97%", "98%"],
    ["Telemedicine Calls", "320", "900", "2,100", "3,900", "7,000"],
]
tbl(s, L, 1.55, CONTENT_W, growth, [2.5, 1.7, 1.7, 1.7, 1.7, 1.7],
    hbg=GOLD, hfg=NAVY, rh=0.38)

divider(s, L, 4.5, CONTENT_W, GOLD_DIM)
tx(s, L, 4.65, 5, 0.25, "WHAT THIS MEANS FOR YOUR HOSPITAL", 11, GOLD, True)

for i, (yr, desc) in enumerate([
    ("Year 1", "30-50 patients \u2192 $225K-$375K net revenue"),
    ("Year 2", "60-120 patients \u2192 $450K-$900K net + 50+ intl reviews"),
    ("Year 3", "100-200 patients \u2192 $750K-$1.5M net + global brand visibility"),
    ("Year 5", "200-400 patients \u2192 $1.5M-$3M net + top-ranked intl hospital"),
]):
    y = 4.95 + i * 0.4
    icon_circle(s, L, y, yr[5:], GOLD, NAVY, 0.3)
    tx(s, L + 0.4, y + 0.02, 10, 0.3, f"{yr}:  {desc}", 10, DIM)

shp(s, L, 6.55, CONTENT_W, 0.5, DARK2)
tx(s, L, 6.6, CONTENT_W, 0.4,
   "MILESTONES:  Q2 2026 Mobile app + 10 hospitals  |  Q4 2026 Breakeven  |  "
   "Q2 2027 Series A + Africa entry  |  2030 120 hospitals, 10K patients/year",
   9, DIM, False, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 21 — CTA (NAVY)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
shp(s, 0, 0, 13.333, 0.05, GOLD, MSO_SHAPE.RECTANGLE)
corner_accents(s)
bg_circle(s, -2, -2, 6, DARK2)
bg_circle(s, 10, 4, 5, DARK3)

tx(s, 0, 1.3, 13.333, 0.6, "BharatHeals", 42, WHITE, True, PP_ALIGN.CENTER)
shp(s, 5.5, 2.0, 2.333, 0.04, GOLD, MSO_SHAPE.RECTANGLE)

tx(s, 1.5, 2.3, 10.333, 1.0,
   "Ready to Grow Your International\nPatient Base & Global Reputation?",
   36, WHITE, True, PP_ALIGN.CENTER, ls=1.15)

tx(s, 2, 3.5, 9.333, 0.6,
   "Join 44 JCI-accredited hospitals already partnering with BharatHeals.\n"
   "Zero upfront cost. First patients within 30 days.", 14,
   DIM, al=PP_ALIGN.CENTER, ls=1.5)

for i, (ic, label, value) in enumerate([
    ("\u2709\uFE0F", "Email", "partnerships@bharatheals.com"),
    ("\U0001F4DE", "Phone", "+91 123 456 7890"),
    ("\U0001F4AC", "WhatsApp", "+91 98765 43210"),
    ("\U0001F310", "Website", "www.bharatheals.com/partners"),
]):
    x = 1.5 + i * 2.8
    shp(s, x, 4.4, 2.5, 0.95, DARK2)
    icon_circle(s, x + 0.95, 4.22, ic, GOLD, NAVY, 0.4)
    tx(s, x, 4.7, 2.5, 0.2, label.upper(), 8, GOLD_DIM, True, PP_ALIGN.CENTER)
    tx(s, x, 4.95, 2.5, 0.3, value, 10, WHITE, True, PP_ALIGN.CENTER)

shp(s, 3, 5.7, 7.333, 0.55, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tx(s, 3, 5.75, 7.333, 0.45,
   "NEXT STEP: Schedule a 30-minute partnership call", 14, NAVY, True, PP_ALIGN.CENTER)

tx(s, 0, 6.6, 13.333, 0.3,
   "Confidential  |  BharatHeals Pvt. Ltd.  |  2026  |  For hospitals & doctors only",
   8, RGBColor(0x44, 0x44, 0x44), al=PP_ALIGN.CENTER)


# ── SAVE ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "BharatHeals_Partnership_Deck.pptx")
prs.save(out)
print(f"\u2705 Partnership deck saved: {out}")
print(f"   Total slides: {len(prs.slides)}")
print(f"   Format: 16:9 Widescreen (13.333 x 7.5 inches)")
